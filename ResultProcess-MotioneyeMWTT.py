import paho.mqtt.client as mqtt
import time
import glob
import os
import sys
import yaml
from pathlib import Path
import signal

## CONFIGURATION

global mqttBroker
global mqttClientName
global mqttUsername
global mqttPassword
global mqttTopic

def CreateConfig():
    with open("config.yaml", "w") as configFile:
        configFile.write("################################################# \n#                CONFIGURATION                  # \n################################################# \n\nmqttBroker: \nmqttClientName: \nmqttUsername: \nmqttPassword: \n\n#Only change if you used a different MQTT topic for your motion events/pictures, \n#Don't set to specific camera locations, we will insert those with an argument. \nmqttTopic: motioncameras \n")
       
#Get current path and set root folder
source_path = Path(os.path.dirname(sys.argv[0])).resolve()
source_dir = source_path.parent
try:
    os.chdir(source_dir)
except OSError:
    Log("Path not found")

def signal_handler(signal, frame):
  ExitProgram()


#Logging Functions
Logtext = ""
def Log(newmsg):
        global Logtext
        print(str(newmsg))
        Logtext = Logtext + str(newmsg) + "\n"
def WriteToLog():
    #Write to log on exit
    Log("Logfile in :" + str(source_dir))
    logfile = open("log2.txt", "w")
    logfile.write(Logtext)
    logfile.close()

Log(source_dir)
    
#Quit
def ExitProgram():
    WriteToLog()
    sys.exit()


    
# On Message Function
def on_message(client, userdata, message):
    if not("picture" in message.topic): 
        Log("Received message: " + str(message.payload.decode("utf-8")))
        #On First Message, Make sure the message is recieved
        if "Test" == str(message.payload.decode("utf-8")):
            Log("Connection Successful")
        else:
            camera = str(message.topic)
            camera = camera.replace(mqttTopic+"/","")
            camera = camera.replace("/result","")
           
            file = str(message.payload.decode("utf-8"))
            file = file.replace("True | ","")
            file = file.replace("False | ","")
            file = file.replace(".jpg","")
            
            result = str(message.payload.decode("utf-8"))
            result = result.replace(" | " + file + ".jpg","")
            
            
            
            Log("Result for '" + camera + "': " + result + ". File Location: " + file)
            CheckMessage(camera, result, file)


def CheckMessage(cam,mess,fileLoc):
    if (mess == "False"):
    
        #Delete Image
        imageSearch = fileLoc + ".jpg" # Any file in camera folder ending in .jpg
        if os.path.exists(imageSearch):
          os.remove(imageSearch)
          Log("Deleted Image for '"+ cam + "'")
        else:
          Log(imageSearch + " not found")
   
        #Delete Video
        imageSearch = fileLoc + ".mp4" # Any file in camera folder ending in .mp4
        if os.path.exists(imageSearch):
          os.remove(imageSearch)
          Log("Deleted Video for '"+ cam + "'")
        else:
          Log(imageSearch + " not found")
    elif (mess == "True"):
        #Mark Image as confirmed
        imageSearch = fileLoc + ".jpg" # Any file in camera folder ending in .jpg
        if os.path.exists(imageSearch):
          os.rename(imageSearch, fileLoc + "-Confirmed.jpg")
          Log("Confirmed Image for '"+ cam + "'")
        else:
          Log(imageSearch + " not found")
   
        #Delete Video
        imageSearch = fileLoc + ".mp4" # Any file in camera folder ending in .mp4
        if os.path.exists(imageSearch):
          os.rename(imageSearch, fileLoc + "-Confirmed.mp4")
          Log("Confirmed Video for '"+ cam + "'")
        else:
          Log(imageSearch + " not found")
    
    
    
#Check if the config exists and get details, else write it.
configFile = Path('config.yaml')
try:
    with open("config.yaml","r") as configFile:
        configuration = yaml.load(configFile, Loader=yaml.FullLoader)
        if (configuration["mqttBroker"] == None):
            Log("Config file has not been correctly configured. Please enter your MQTT details in the config file")
            ExitProgram()
        elif (("mqttBroker" not in configuration) or ("mqttClientName" not in configuration) or ("mqttUsername" not in configuration) or ("mqttPassword" not in configuration) or ("mqttTopic" not in configuration)):
            configFile.close()
            Log("Error in config file, please correct, or delete and a new one will be created on next run.")
            ExitProgram()
        else:
            mqttBroker = configuration["mqttBroker"]
            mqttClientName = configuration["mqttClientName"] + "2"
            mqttUsername = configuration["mqttUsername"]
            mqttPassword = configuration["mqttPassword"]
            mqttTopic = configuration["mqttTopic"]
except FileNotFoundError:
    Log("Config File doesn't exist, creating one now.")
    Log("Please enter your details into the config file")
    CreateConfig()
    ExitProgram()

#Connect to Broker
client = mqtt.Client(mqttClientName)
client.username_pw_set(mqttUsername, password=mqttPassword)
client.connect(mqttBroker) 

#Subscribe to Topic & Subtopics

client.subscribe(mqttTopic+"/+/result")

#Publish Test payload
client.publish(mqttTopic+"/TEST/result","Test")
Log("Published 'Test' to '"+ mqttTopic + "'")

while True:
    try:
        client.loop_start()
        #Read subscribed messages
        client.on_message=on_message 
        time.sleep(4)
        client.loop_stop()
    except KeyboardInterrupt:
        client.loop_stop()
        Log("Qutting")
        ExitProgram()
