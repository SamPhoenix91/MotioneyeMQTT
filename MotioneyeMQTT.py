import paho.mqtt.client as mqtt
import time
import glob
import os
import sys

## CONFIGURATION // EDIT HERE ##------------------------------------------------
#Enter MQTT Broker Information here
mqttBroker =""
mqttClientName = ""
mqttUsername = ""
mqttPassword = ""

#Only change if you used a different MQTT topic, don't set to specific camera locations, we will insert those with an argument.
mqttTopic = "motioncameras"


##END OF CONFIGURATION ##----------------------------------------------------

#Logging Function
Logtext = ""
def Log(newmsg):
        global Logtext
        Logtext = Logtext + newmsg + "\n"

# On Message Function
def on_message(client, userdata, message):
    if not("picture" in message.topic): 
        Log("Received message: " + str(message.payload.decode("utf-8")))
        #On First Message, Make sure the message is recieved
        if "Test" == str(message.payload.decode("utf-8")):
            Log("Connection Successful")
def WriteToLog():
    #Write to log on exit
    logfile = open("log.txt", "w")
    logfile.write(Logtext)
    logfile.close()

#Check that script launched with correct number of arguments
if len(sys.argv) != 3:
    Log("Expected 2 arguments (MqttMessage, Camera) got " + str(len(sys.argv) - 1))
    WriteToLog()
    quit()

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
mqttMessage = sys.argv[1] 
camera = sys.argv[2] 

#Publish Message
client.publish(mqttTopic + "/" + camera + "/sensor",mqttMessage)
Log("Published '"+ mqttMessage +"' to '"+ mqttTopic + "'")

#Publish Picture
imageSearch = camera + "/*.jpg"
list_of_files = glob.glob(imageSearch) # * means all if need specific format then *.csv
if list_of_files:
    latest_file = max(list_of_files, key=os.path.getctime)
    Log(latest_file)
    image = open(latest_file, "rb")
    client.publish(mqttTopic + "/" + camera + "/picture",image.read())
    Log("Published camera snapshot to '"+ mqttTopic + "'")
else:
    Log("No JPG files found for camera")





client.loop_start()
#Read subscribed messages
client.on_message=on_message 
time.sleep(1)
client.loop_stop()


WriteToLog()
