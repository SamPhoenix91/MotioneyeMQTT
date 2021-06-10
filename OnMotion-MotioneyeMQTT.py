import paho.mqtt.client as mqtt
import time
import glob
import os
import sys
import yaml
from pathlib import Path

## CONFIGURATION

global mqttBroker
global mqttClientName
global mqttUsername
global mqttPassword
global mqttTopic

#Get current path and set root folder
if getattr( sys, 'frozen', False ) :
    source_path = Path(os.path.dirname(sys.executable)).resolve()
else:
    source_path = Path(os.path.dirname(sys.argv[0])).resolve()
source_dir = source_path.parent


def CreateConfig():
    with open("config.yaml", "w") as configFile:
        configFile.write("################################################# \n#                CONFIGURATION                  # \n################################################# \n\nmqttBroker: \nmqttClientName: \nmqttUsername: \nmqttPassword: \n\n#Only change if you used a different MQTT topic for your motion events/pictures, \n#Don't set to specific camera locations, we will insert those with an argument. \nmqttTopic: motioncameras \n")
       
##END OF CONFIGURATION #





#Logging Functions
Logtext = ""
def Log(newmsg):
        global Logtext
        Logtext = Logtext + str(newmsg) + "\n"
def WriteToLog():
    #Write to log on exit
    Log("\n \n" + "Logfile created in: " + str(source_dir) + "/log1.txt")
    logfile = open("log1.txt", "w")
    logfile.write(Logtext)
    logfile.close()
    
    
    
#Quit
def ExitProgram():
    WriteToLog()
    sys.exit()
    
    
#Set rootfolder
try:
    os.chdir(source_dir)
    Log("Root Folder: " + str(source_dir) + "\n \n ")
except OSError:
    Log("Path not found")
    Log("Root directory: " + os.path.dirname() + "\n \n")
    
    
# On Message Function
def on_message(client, userdata, message):
    if not("picture" in message.topic): 
        Log("Received message: " + str(message.payload.decode("utf-8")))
        #On First Message, Make sure the message is recieved
        if "Test" == str(message.payload.decode("utf-8")):
            Log("Connection Successful")
    
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
            mqttClientName = configuration["mqttClientName"]
            mqttUsername = configuration["mqttUsername"]
            mqttPassword = configuration["mqttPassword"]
            mqttTopic = configuration["mqttTopic"]
except FileNotFoundError:
    Log("Config File doesn't exist, creating one now.")
    Log("Please enter your details into the config file")
    CreateConfig()
    ExitProgram()

#Check that script launched with correct number of arguments
if len(sys.argv) != 3:
    Log("Expected 2 arguments (MqttMessage, Camera) got " + str(len(sys.argv) - 1))
    ExitProgram()



#Connect to Broker
client = mqtt.Client(mqttClientName)
client.username_pw_set(mqttUsername, password=mqttPassword)
client.connect(mqttBroker) 

#Subscribe to Topic & Subtopics

client.subscribe(mqttTopic+"/#")

#Publish Test payload
client.publish(mqttTopic,"Test")
Log("Published 'Test' to '"+ mqttTopic + "'")

#Set MQTT Message & camera to arguments
if (sys.argv[1] == "ON" or sys.argv[1] == "On" or sys.argv[1] == "on"):
    mqttMessage = "ON"
elif (sys.argv[1] == "OFF" or sys.argv[1] == "Off" or sys.argv[1] == "off"):
    mqttMessage = "OFF"
elif (sys.argv[1] == "TEST" or "Test" or "test"):
    mqttMessage = "TEST"
else:
    Log("Invalid Argument for motion state.")
    Log("Valid States are: On (ON/On/on), Off(OFF/Off/off), Test(TEST,Test,test)")
camera = sys.argv[2] 

#Publish Message
client.publish(mqttTopic + "/" + camera + "/sensor",mqttMessage)
Log("Published '"+ mqttMessage +"' to '"+ mqttTopic + "'")

#Publish Picture if motion on
if (mqttMessage == "ON"):
    imageSearch =  camera + "/*.jpg" # Any file in camera folder ending in .jpg
    list_of_files = glob.glob(imageSearch)
    if list_of_files:
        latest_file = ""
        latest_file = max(list_of_files, key=os.path.getctime)
        Log("Image File: " + latest_file)
        image = open(latest_file, "rb")
        client.publish(mqttTopic + "/" + camera + "/picture",image.read())
        client.publish(mqttTopic + "/" + camera + "/file",latest_file)
        Log("Published camera snapshot to '"+ mqttTopic + "'")
        Log("Filename :"+ latest_file)
    else:
        Log("No JPG files found for camera '" + camera + "'")





client.loop_start()
#Read subscribed messages
client.on_message=on_message 
time.sleep(1)
client.loop_stop()


ExitProgram()
