import paho.mqtt.client as mqtt
import time
import Adafruit_DHT
import drivers

mqtt_broker = "ia.ic.polyu.edu.hk"
mqtt_port = 1883
mqtt_qos = 1

mqtt_client = mqtt.Client("iot-21103411d") # Create a Client Instance
mqtt_client.connect(mqtt_broker, mqtt_port) # Establish a connection to a broker
print("Connect to MQTT broker")

mqtt_topic = "iot/21103411d"
mqtt_client.subscribe(mqtt_topic, mqtt_qos)
msg = "36.0"
mqtt_client.publish(mqtt_topic, msg, mqtt_qos) # Publish a message
print("Publishing message", msg ,"to topic", mqtt_topic)

display = drivers.Lcd()

def mqtt_on_message(client, userdata, msg):
    humid = str(humidity)
    temp = str(temperature)
    d_msg = str(msg.payload.decode("utf-8"))
    if d_msg == 'T':
        display.lcd_display_string('Temperature:', 1)
        display.lcd_display_string(temp, 2)
        time.sleep(2)
        display.lcd_clear()
    elif d_msg == 'H':
        display.lcd_display_string('Humidity:', 1)
        display.lcd_display_string(humid, 2)
        time.sleep(2)
        display.lcd_clear()
        
    
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN) # Read the temperature
    
mqtt_client.on_message = mqtt_on_message
mqtt_client.loop_start()

while True:
    mqtt_client.publish(mqtt_topic, temperature, mqtt_qos) # Publish a message
    print("Publishing message %s and %s to topic %s" % (temperature, humidity, mqtt_topic))
    time.sleep(2)