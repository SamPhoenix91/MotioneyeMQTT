# MotioneyeMQTT

This is my first of two scripts to help improve Motioneye with DeepstackAI. This script takes motion snapshots from Motioneye and sends them to Home Assistant for analysis with Deepstack.

## Installation
I advise following the [full instructions on my website](https://www.samdavis.tech/portfolio/aicameradetection)

Grab my code from github and unpack it
```bash
curl -LJO https://github.com/SamPhoenix91/MotioneyeMQTT/releases/download/0.1/MotioneyeMqtt.tar.gz
tar -xf MotioneyeMqtt.tar.gz
```


In motioneye turn on "Run a command" under "Motion Notifications"
set the command as "./MotioneyeMqtt/RunMotioneyeMQTT ON [Camera Name]" 
i.e. if you're using your front door camera:
```
./MotioneyeMqtt/RunMotioneyeMQTT ON Front_Door
```
set the end command as 
```
./MotioneyeMqtt/RunMotioneyeMQTT OFF Front_Door
```
