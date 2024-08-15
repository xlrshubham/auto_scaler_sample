import asyncio
import argparse
import signal
from controller_manager import ControllerManager
from config_loader import Config
from rest_client import RestClient
import logging

controller_manager = ControllerManager()
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Process the configuration provided.")
parser.add_argument('--config', type=str, required=False, help="Path to the configuration file")
args = parser.parse_args()
config = Config(args.config).get_config()

logging.basicConfig(level=getattr(logging, config.get("LOG_LEVEL")))

class AutoScaler:
    def __init__(self):

        self.shared_data_lock = asyncio.Lock()
        self.shared_data = {
            "current_replica": None,
            "desired_replica": None,
            "cpu_utilization": None
        }
        self.restclient = RestClient(max_retries=config.get("RESTCLIENT_MAX_RETRIES"), retry_interval=config.get("RESTCLIENT_RETRY_INTERVAL"))


    @controller_manager.control_loop("get_status", config.get("STATUS_CHECK_INTERVAL",10) )
    async def get_app_status_loop(self):
    # Controller loop to get the status of current cpu.
    # This function will run after every STATUS_CHECK_INTERVAL. 
        app_status = await self.restclient.get( config.get("SERVER_URL")+ config.get("APP_STATUS_API"))
        if not app_status:
            return
        async with self.shared_data_lock:
            self.shared_data['cpu_utilization'] = app_status["cpu"]["highPriority"]
            self.shared_data["current_replica"] = app_status["replicas"]
            logger.info("App status updated: CPU utilization is %s, Current replicas are %s", 
                        self.shared_data['cpu_utilization'], self.shared_data["current_replica"])

    @controller_manager.control_loop("set_replicas", config.get("SCALING_INTERVAL",20))
    async def set_replicas_loop(self):
    # Controller loop to set the desired replica to server. 
    # This function will run after every SCALING_INTERVAL. 
        async with self.shared_data_lock:
            put_data = {"replicas": self.shared_data["desired_replica"]}
            if not put_data["replicas"] or self.shared_data["desired_replica"] == self.shared_data["current_replica"]:
                logger.debug("Skipping setting replicas, no action needed. Current_replica: %s , desired_replica: %s",self.shared_data["current_replica"], self.shared_data["desired_replica"] )
                return
        await self.restclient.put(config.get("SERVER_URL") + config.get("SET_REPLICA_API"), put_data)
        logger.info("Replicas set to %s", put_data["replicas"])

    @controller_manager.control_loop("decide_replicas", config.get("DECIDE_REPLICA_INTERVAL",10))
    async def decide_replicas_loop(self):
    # Controller loop to set the determine the desired replica based on cpu utilization and current replica. 
    # This function will run after every DECIDE_REPLICA_INTERVAL. 
        DESIRED_CPU_UTILIZATION = config.get("DESIRED_CPU_UTILIZATION", 0.80)
        SCALE_DOWN_TOLERATION = config.get("SCALE_DOWN_TOLERATION", 0.0)
        MIN_REPLICAS = 1

        async with self.shared_data_lock:
            cpu_utilization = self.shared_data.get("cpu_utilization")
            current_replicas = self.shared_data.get("current_replica")

            if cpu_utilization is None or current_replicas is None:
                logger.error("CPU utilization or current replica count is not available.")
                return

            if cpu_utilization > DESIRED_CPU_UTILIZATION:
                self.shared_data["desired_replica"] = current_replicas + 1
                logger.info("Increasing replicas to %s due to high CPU utilization (%s).",
                            self.shared_data['desired_replica'], cpu_utilization)
            elif cpu_utilization < DESIRED_CPU_UTILIZATION * (1.0 - SCALE_DOWN_TOLERATION):
                self.shared_data["desired_replica"] = max(MIN_REPLICAS, current_replicas - 1)
                logger.info("Decreasing replicas to %s due to low CPU utilization (%s).",
                            self.shared_data['desired_replica'], cpu_utilization)
            else:
                logger.info("CPU utilization is at the threshold. No change in replicas.")

    # Signal handler in case CTRL+C or SIGTERM is sent. 
    # This will set all controller manager events so that infinite loops can be closed. 
    def signal_handler(self, sig, frame):
        logger.info('Signal received, stopping all tasks...')
        asyncio.ensure_future(controller_manager.set_all_events())

    # Main function to run all controll loops. 
    async def main(self):
        tasks = [
            asyncio.create_task(self.get_app_status_loop()),
            asyncio.create_task(self.set_replicas_loop()),
            asyncio.create_task(self.decide_replicas_loop()),
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:        
        auto_scaler = AutoScaler()
        signal.signal(signal.SIGINT, auto_scaler.signal_handler)
        signal.signal(signal.SIGTERM, auto_scaler.signal_handler)
        asyncio.run(auto_scaler.main())
    except asyncio.CancelledError:
        logger.error("Loops cancelled.")
    finally:
        logger.info("All loops have been stopped.")
