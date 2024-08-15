import asyncio
import logging

logger = logging.getLogger(__name__)

# Event manager manages the event's for all control loops.
class EventManager:
    def __init__(self):
        self.events = {}

    def create_event(self, name):
        event = asyncio.Event()
        self.events[name] = event
        return event

    def get_event(self, name):
        return self.events.get(name)

    async def set_all_events(self):
        for event in self.events.values():
            event.set()

# Controller Manager created the control_loop by running a function in infinite loop 
# by calling it again and again after provided interval. 
class ControllerManager:
    def __init__(self):
        self.event_manager = EventManager()
    
    def control_loop(self, event_name, interval):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                event = self.event_manager.create_event(event_name)

                while not event.is_set():
                    await func(*args, **kwargs)
                    await asyncio.sleep(interval)
                logger.info("%s has stopped", func.__name__)

            return wrapper
        return decorator
    
    async def set_all_events(self):
        await self.event_manager.set_all_events()
        logger.info("All events have been set.")
