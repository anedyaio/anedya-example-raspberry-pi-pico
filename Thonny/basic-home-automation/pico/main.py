import network
import ujson as json
import time
import utime
import ssl
from umqtt.simple import MQTTClient
from machine import Pin
import random
from dht import DHT11

# Emulate Hardware Sensor?
virtual_sensor = False

# Anedya Connection Key
CONNECTION_KEY = b"CONNECTION_KEY"

# Physical Device ID
PHYSICAL_DEVICE_ID = "PHYSICAL_DEVICE_ID"

# WiFi Credentials
SSID = 'SSID'  # SSID of the WiFi network
PASSWORD = 'PASSWORD'  # Password of the WiFi network

# Anedya Broker
broker = b"mqtt.ap-in-1.anedya.io"

# Publish Topic
PUBLISH_TOPIC = f'$anedya/device/{PHYSICAL_DEVICE_ID}/submitdata/json'.encode('ASCII')

# Update Status Topic
UPDATE_STATUS_TOPIC = f'$anedya/device/{PHYSICAL_DEVICE_ID}/commands/updateStatus/json'.encode('ASCII')

# Sensor Pin
dataPin = 16
myPin = Pin(dataPin, Pin.OUT, Pin.PULL_DOWN)  # Initialize sensor pin
sensor = DHT11(myPin)

# Light and Fan Pins
lightPin = 17
light = Pin(lightPin, Pin.OUT)  # Initialize light pin
fanPin = 18
fan = Pin(fanPin, Pin.OUT)  # Initialize fan pin

# Command ID
command_id = ""
def main():
    """
    The main function that connects to the Anedya broker and subscribes to topics.

    This function connects to the Anedya broker using the provided WiFi credentials and connection key.
    It then subscribes to three topics:
    - `$anedya/device/{PHYSICAL_DEVICE_ID}/response` - topic to receive response from the broker.
    - `$anedya/device/{PHYSICAL_DEVICE_ID}/errors` - topic to receive error messages from the broker.
    - `$anedya/device/{PHYSICAL_DEVICE_ID}/commands` - topic to receive commands from the broker.

    """
    global command_id
    connect_to_wifi(ssid=SSID,password=PASSWORD)

    # Connecting to Anedya broker....
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Create SSL context
    context.load_verify_locations(cafile='/certs/anedya_rca.cer')  # Load CA certificate
    client = MQTTClient(client_id=PHYSICAL_DEVICE_ID,  # Create MQTT client
                        server=broker,
                        port=8883,
                        user=PHYSICAL_DEVICE_ID,
                        password=CONNECTION_KEY,
                        ssl=context)  # Use SSL context for secure connection
    client.set_callback(sub_cb)  # Set callback function for incoming messages
    resp = client.connect()  # Connect to broker
    if not resp:  # Check if connection was successful
        print("Connected to Anedya Broker")
    time.sleep(1)
    RES_TOPIC = f'$anedya/device/{PHYSICAL_DEVICE_ID}/response'.encode('ASCII')  # Define response topic
    ERR_TOPIC = f'$anedya/device/{PHYSICAL_DEVICE_ID}/errors'.encode('ASCII')  # Define error topic
    COMM_TOPIC = f'$anedya/device/{PHYSICAL_DEVICE_ID}/commands'.encode('ASCII')  # Define command topic
    client.subscribe(topic=RES_TOPIC)  # Subscribe to response topic
    client.subscribe(topic=ERR_TOPIC)  # Subscribe to error topic
    client.subscribe(topic=COMM_TOPIC)  # Subscribe to command topic

    # Initialize interval time
    interval_time = utime.ticks_ms()
    # Turn off light and fan
    light.value(0)
    fan.value(0)

    while True:
        # Check if command_id exists
        if command_id:
            # Create status payload
            status_payload = json.dumps({
              "reqId": "",  # reqId is not used in this example
              "commandId": command_id,  # commandId to acknowledge the command
              "status": "success",  # status of the command
              "ackdata": "",  # ackdata is not used in this example
              "ackdatatype": ""  # ackdatatype is not used in this example
             })
            # Publish status payload
            client.publish(UPDATE_STATUS_TOPIC, status_payload, qos=0)
            # Reset command_id
            command_id = ""
            
        # Check if it's time to measure temperature and humidity
        if utime.ticks_ms() - interval_time > 5000:  # interval
            # Update interval time
            interval_time = utime.ticks_ms()
            if virtual_sensor:
                # Generate random temperature and humidity if virtual sensor is used
                temperature = random.randint(1, 50) 
                humidity = random.randint(10, 70)
            else:
                try:
                    # Measure temperature and humidity
                    sensor.measure()
                except:
                    pass
                # Read temperature and humidity
                temperature = sensor.temperature()
                humidity = sensor.humidity()
        
            # Create payload for temperature
            # Create payload for temperature
            payload_temp = json.dumps({  # Dictionary containing temperature data
                "data": [  # List containing temperature data
                    {
                        "variable": "temperature",  # Variable identifier for temperature
                        "value": temperature,  # Temperature value
                        "timestamp": 0  # Not used in this example
                    }
                ]
            })
            print(f"Temperature :{temperature}°C")  # Print temperature
            client.publish(PUBLISH_TOPIC ,payload_temp,qos=0)  # Publish temperature payload
            
            payload_hum = json.dumps({  # Dictionary containing humidity data
                "data": [  # List containing humidity data
                    {
                        "variable": "humidity",  # Variable identifier for humidity
                        "value": humidity,  # Humidity value
                        "timestamp": 0  # Not used in this example
                    }
                ]
            })
            print(f"Humidity :{humidity}%")  # Print humidity
            client.publish(PUBLISH_TOPIC ,payload_hum,qos=0)  # Publish humidity payload
        if False:  # Example of blocking wait for message
            client.wait_msg()
        else:  # Example of non-blocking wait for message
            client.check_msg()  # Check for incoming messages
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
        time.sleep(2)
        #client.publish(PUBLISH_TOPIC ,payload,qos=0)
        #time_variable+=1000# client.disconnect()
    return client


def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # Create a station interface
    wlan.active(True)  # Activate the interface

    # Attempt to connect to the WiFi network
    print(f'Connecting to {ssid}...')
    wlan.connect(ssid, password)

    # Wait for connection with a timeout
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts and not wlan.isconnected():
        print(f'Attempt {attempt + 1} of {max_attempts}...')
        attempt += 1
        time.sleep(1)  # Wait a bit before checking again

    if wlan.isconnected():
        print('Connected to WiFi network!')
        #print('Network config:', wlan.ifconfig())
    else:
        print('Failed to connect to WiFi network.')

def sub_cb(topic, msg):
    # Global variable to store command ID
    global command_id

    # Print the received message
    print(msg)
    
    # Extract command and data from the JSON message
    command = json.loads(msg).get("command")
    data = json.loads(msg).get("data")
    command_id = json.loads(msg).get("commandId")

    # If the command is "Light" or "light"
    if command == "Light" or command == "light":
        # If the data is "on" or "ON"
        if data == "on" or data == "ON":
            # Turn the light on
            light.value(1)
            print("Light ON")

        # If the data is "off" or "OFF"
        if data == "off" or data == "OFF":
            # Turn the light off
            print("Light OFF")
            light.value(0)

    # If the command is "Fan" or "fan"
    if command == "Fan" or command == "fan":
        # If the data is "on" or "ON"
        if data == "on" or data == "ON":
            # Turn the fan on
            fan.value(1)
            print("Fan ON")

        # If the data is "off" or "OFF"
        if data == "off" or data == "OFF":
            # Turn the fan off
            fan.value(0)
            print("Fan OFF")

if __name__ == '__main__':
    # Call the main function
    main()


    

