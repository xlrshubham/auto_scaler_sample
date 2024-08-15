import asyncio
import urllib.request
import json
import logging

logger = logging.getLogger(__name__)

class RestClient:
    def __init__(self, max_retries=3, retry_interval=2):
        self.max_retries = max_retries
        self.retry_interval = retry_interval

    async def get(self, url):
        loop = asyncio.get_event_loop()
        attempt = 0
        while attempt < self.max_retries:
            try:
                request = urllib.request.Request(url)
                request.add_header("Accept", "application/json")
                response = await loop.run_in_executor(None, urllib.request.urlopen, request)

                data = json.loads(response.read().decode())
                logger.info("Data fetched from %s: %s", url, json.dumps(data, indent=2))
                return data
            except Exception as e:
                attempt += 1
                logger.error("Attempt %s failed for %s: %s", attempt, url, e)
                if attempt < self.max_retries:
                    logger.info("Retrying in %s seconds...", self.retry_interval)
                    await asyncio.sleep(self.retry_interval)
                else:
                    logger.error("Failed to fetch data from %s after %s attempts.", url, self.max_retries)

    async def put(self, url, data):
        loop = asyncio.get_event_loop()
        attempt = 0
        while attempt < self.max_retries:
            try:
                json_data = json.dumps(data).encode('utf-8')
                request = urllib.request.Request(url, data=json_data, method='PUT')
                request.add_header("Content-Type", "application/json")

                await loop.run_in_executor(None, urllib.request.urlopen, request)
                logger.info("Successfully PUT to %s with data: %s", url, data)
                return True
            except Exception as e:
                attempt += 1
                logger.error("Attempt %s failed for PUT %s: %s", attempt, url, e)
                if attempt < self.max_retries:
                    logger.info("Retrying in %s seconds...", self.retry_interval)
                    await asyncio.sleep(self.retry_interval)
                else:
                    logger.error("Failed to PUT data to %s after %s attempts.", url, self.max_retries)
