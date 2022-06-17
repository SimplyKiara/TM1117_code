import paho.mqtt.client as mqtt
import time
import Adafruit_DHT
import json

mqtt_broker = "ia.ic.polyu.edu.hk"
mqtt_port = 1883
mqtt_qos = 1

mqtt_client = mqtt.Client("iot-21103411d") # Create a Client Instance
mqtt_client.connect(mqtt_broker, mqtt_port) # Establish a connection to a broker
print("Connect to MQTT broker")

mqtt_topic = "iot/control"
mqtt_client.subscribe(mqtt_topic, mqtt_qos)
    
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

IotData = {}

def mqtt_on_message(client, userdata, msg):
    d_control = msg.payload.decode("utf-8")
    jsonControl = json.loads(d_control)
    if jsonControl['id'] == '7' and jsonControl['type'] == 'request':
        IotData = {}
        IotData['id'] = '7'
        IotData['type'] = 'response'
        IotData['loc'] = 'w502g'
        if jsonControl['action'] == 'T':
            IotData['T'] = temperature
            mqtt_client.publish(mqtt_topic, json.dumps(IotData), mqtt_qos)
        elif jsonControl['action'] == 'H':
            IotData['H'] = humidity
            mqtt_client.publish(mqtt_topic, json.dumps(IotData), mqtt_qos)

mqtt_client.on_message = mqtt_on_message
mqtt_client.loop_start()

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN) # Read the temperature
    time.sleep(1)
