0. From CMD/Bash go inside parent folder of submitted zip file. 
1. Please run the scaleit server, if docker is installed, running .\run_scaleit_server.cmd should start it on localhost port 8001
2. Please set the configuration file in AutoScaler/config.json , for reference, please go through AutoScaler/README.md file
3. Run the AutoScaler using following command:
```
python AutoScaler/auto_scaler.py --config AutoScaler/config.json
```