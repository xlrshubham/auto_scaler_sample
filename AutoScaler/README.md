# AutoScaler Configuration Guide

To run the AutoScaler, please set the values in the configuration file (`config.json`) as per your requirement. This guide will walk you through each configuration option.

## Sample `config.json`

```json
{
    "LOG_LEVEL" : "DEBUG",
    "SERVER_URL" : "http://localhost:8001",
    "APP_STATUS_API": "/app/status",
    "SET_REPLICA_API": "/app/replicas",
    "STATUS_CHECK_INTERVAL" : 2,
    "DECIDE_REPLICA_INTERVAL" : 2,
    "SCALING_INTERVAL" : 15,
    "DESIRED_CPU_UTILIZATION" : 0.80,
    "SCALE_DOWN_TOLERATION" : 0.1,
    "RESTCLIENT_MAX_RETRIES" : 3, 
    "RESTCLIENT_RETRY_INTERVAL" : 2
}
```

## Configuration Options

### `LOG_LEVEL`
- **Description**: Defines the verbosity of logs.
- **Possible Values**: `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`.
- **Default**: `"INFO"`
- **Note**: The current code logs to STDOUT and STDERR. File logging is not yet supported.

### `SERVER_URL`
- **Description**: The base URL (domain name and port) of the ScaleIt server. This should not include API endpoints, which are defined separately.
- **Example**: `"http://localhost:8001"`

### `APP_STATUS_API`
- **Description**: The API endpoint for retrieving the current status of the application, including CPU utilization and the current number of replicas.
- **Example**: `"/app/status"`
- **Note**: This endpoint will be appended to `SERVER_URL` to form the complete URL.

### `SET_REPLICA_API`
- **Description**: The API endpoint for setting the desired number of replicas.
- **Example**: `"/app/replicas"`
- **Note**: This endpoint will be appended to `SERVER_URL` to form the complete URL.

### `STATUS_CHECK_INTERVAL`
- **Description**: The interval (in seconds) between checks of the application's CPU utilization status.
- **Example**: `2` (checks every 2 seconds)
- **Note**: This determines how often the AutoScaler checks the current status to make scaling decisions.

### `DECIDE_REPLICA_INTERVAL`
- **Description**: The interval (in seconds) at which the AutoScaler decides whether to scale up or scale down based on the current CPU utilization.
- **Example**: `2` (decides every 2 seconds)
- **Note**: This interval controls how frequently scaling decisions are made.

### `SCALING_INTERVAL`
- **Description**: The interval (in seconds) at which the desired replica count is adjusted based on scaling decisions.
- **Example**: `15` (adjusts replicas every 15 seconds)
- **Note**: This interval determines how often the AutoScaler actually changes the number of replicas based on the decisions made.

### `DESIRED_CPU_UTILIZATION`
- **Description**: The target CPU utilization that the AutoScaler aims to achieve by adjusting the number of replicas.
- **Example**: `0.80` (aims for 80% CPU utilization)
- **Note**: The AutoScaler will increase replicas if the actual CPU utilization is above this value and decrease replicas if it is below.

### `SCALE_DOWN_TOLERATION`
- **Description**: The toleration level for scaling down. This is the amount by which the CPU utilization can be below the `DESIRED_CPU_UTILIZATION` before the AutoScaler decides to reduce the number of replicas.
- **Example**: `0.1` (10% tolerance)
- **Note**: This helps prevent frequent scaling down in cases of minor fluctuations in CPU utilization.

### `RESTCLIENT_MAX_RETRIES`
- **Description**: The maximum number of retries the RestClient will attempt if a request to the server fails.
- **Example**: `3` (retries up to 3 times)
- **Note**: This setting is useful in handling transient network issues or temporary server unavailability.

### `RESTCLIENT_RETRY_INTERVAL`
- **Description**: The interval (in seconds) between retries when the RestClient encounters a failed request.
- **Example**: `2` (waits 2 seconds before retrying)
- **Note**: This controls how long the RestClient waits before attempting to retry a failed request.

## Final Notes

- Ensure that the `config.json` file is properly formatted and accessible by the application at runtime.
- Adjust the intervals (`STATUS_CHECK_INTERVAL`, `DECIDE_REPLICA_INTERVAL`, and `SCALING_INTERVAL`) based on your application's performance and scalability requirements.
- The `LOG_LEVEL` should be set according to the environment: use `"DEBUG"` for development and testing, and `"INFO"` or `"ERROR"` for production.

--- 
