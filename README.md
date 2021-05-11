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
./OnMotionScript/OnMotion-MotioneyeMQTT/OnMotion-MotioneyeMQTT ON Front_Door
```
set the end command as 
```
./OnMotionScript/OnMotion-MotioneyeMQTT/OnMotion-MotioneyeMQTT OFF Front_Door
```


You need to set the other script to run at startup and from the root directory (so it uses the config file). You run the second script by typing (no arguments needed):
```
ResultProcessScript/ResultProcess-MotioneyeMQTT/ResultProcess-MotioneyeMQTT
```
This scans the result from HA and either deletes or renames the associated image and video file.
