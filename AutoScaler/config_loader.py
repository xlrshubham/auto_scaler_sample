# Please go through README.md to know about config params.

import json

class Config:
    def __init__(self, config_path=None):
        self.config={
            "LOG_LEVEL" : "ERROR",
            "SERVER_URL" : "http://localhost:8001",
            "APP_STATUS_API": "/app/status",
            "SET_REPLICA_API": "/app/replicas",
            "STATUS_CHECK_INTERVAL" : 2,
            "DECIDE_REPLICA_INTERVAL" : 2,
            "SCALING_INTERVAL" : 15,
            "DESIRED_CPU_UTILIZATION" : 0.80,
            "SCALE_DOWN_TOLERATION" : 0.1,
            "RESTCLIENT_MAX_RETRIES" : 3, 
            "RESTCLIENT_RETRY_INTERVAL" : 2,
        }

        if config_path == None: return
        with open(config_path, 'r') as file:
            self.config.update(json.load(file))
    
    def get_config(self):
        return self.config
    
    