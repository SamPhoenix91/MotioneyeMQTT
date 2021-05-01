# MotioneyeMQTT

This is my first of two scripts to help improve Motioneye with DeepstackAI. This script takes motion snapshots from Motioneye and sends them to Home Assistant for analysis with Deepstack.

## Installation
I advise following the [full instructions on my website](https://www.samdavis.tech/portfolio/aicameradetection)

First you need to install paho-mqtt
```bash
pip3 install paho-mqtt
```

Grab my code from github and unpack it
```bash
curl -LJO https://github.com/SamPhoenix91/MotioneyeMQTT/archive/refs/tags/0.1.tar.gz
tar -xf MotioneyeMQTT-0.1.tar.gz
```

Move the script into var/lib/motioneye 
```
mv ./MotioneyeMQTT-0.1/MotioneyeMQTT.py /var/lib/motioneye/MotioneyeMQTT.py
```

In motioneye turn on "Run a command" under "Motion Notifications"
set the command as "python MotioneyeMQTT.py ON [Camera Name]" i.e. if you're using your front door camera:
```
python MotioneyeMQTT.py ON Front_Door
```
set the end command as 
```
python MotioneyeMQTT.py OFF Front_Door
```
