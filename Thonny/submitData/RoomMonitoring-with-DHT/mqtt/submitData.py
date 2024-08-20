""""
                            Room Monitoring Using Raspberry pi pico + DHT sensor (MQTT)
                Disclaimer: This code is for hobbyists for learning purposes. Not recommended for production use!!

                            # Dashboard Setup
                             - Create account and login to the dashboard
                             - Create new project.
                             - Create variables: temperature and humidity.
                             - Create a node (e.g., for home- Room1 or study room).
                            Note: Variable Identifier is essential; fill it accurately.

                            # Hardware Setup
                             - connect the dht sensor to pin 16

                  Note: The code is tested on the "Raspberry Pi Pico W"

                                                                                           Dated: 20-August-2024
"""

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
virtual_sensor = True

REGION_CODE = "ap-in-1"  # Anedya region code (e.g., "ap-in-1" for Asia-Pacific/India) | For other country code, visity [https://docs.anedya.io/device/#region]
CONNECTION_KEY = b"CONNECTION_KEY"  # Fil your Connection Key
PHYSICAL_DEVICE_ID = "PHYSICAL_DEVICE_ID"  # Fill your unique Physical Device ID
# WiFi Credentials
SSID = "SSID"  # SSID of the WiFi network
PASSWORD = "PASSWORD"  # Password of the WiFi network

# Sensor Pin
dataPin = 16
myPin = Pin(dataPin, Pin.OUT, Pin.PULL_DOWN)  # Initialize sensor pin
sensor = DHT11(myPin)

global mqtt_client
time_res = ""


def main():
    """
    The main function that connects to the Anedya broker and subscribes to topics.

    This function connects to the Anedya broker using the provided WiFi credentials and connection key.
    It then subscribes to three topics:
    - `$anedya/device/{PHYSICAL_DEVICE_ID}/response` - topic to receive response from the broker.
    - `$anedya/device/{PHYSICAL_DEVICE_ID}/errors` - topic to receive error messages from the broker.
    - `$anedya/device/{PHYSICAL_DEVICE_ID}/commands` - topic to receive commands from the broker.

    """
    global mqtt_client
    connect_to_wifi(ssid=SSID, password=PASSWORD)
    # Connecting to Anedya broker....
    connect_to_mqtt()
    anedya_set_device_time()
    # Initialize interval time
    interval_time = utime.ticks_ms()

    while True:
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
            print("===============================================")
            print(f"Temperature :{temperature}°C")  # Print temperature
            anedya_submitData("temperature", temperature)
            print(f"Humidity :{humidity}%")  # Print humidity
            anedya_submitData("humidity", humidity)
            print("===============================================")

        if False:  # Example of blocking wait for message
            mqtt_client.wait_msg()
        else:  # Example of non-blocking wait for message
            mqtt_client.check_msg()  # Check for incoming messages
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
        time.sleep(2)
        # mqtt_client.publish(PUBLISH_TOPIC ,payload,qos=0)
        # time_variable+=1000# mqtt_client.disconnect()
    mqtt_client.disconnect()


def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # Create a station interface
    wlan.active(True)  # Activate the interface

    # Attempt to connect to the WiFi network
    print(f"Connecting to {ssid}...")
    wlan.connect(ssid, password)

    # Wait for connection with a timeout
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts and not wlan.isconnected():
        print(f"Attempt {attempt + 1} of {max_attempts}...")
        attempt += 1
        time.sleep(1)  # Wait a bit before checking again

    if wlan.isconnected():
        print("Connected to WiFi network!")
        # print('Network config:', wlan.ifconfig())
    else:
        print("Failed to connect to WiFi network.")


def connect_to_mqtt():
    global mqtt_client
    broker = f"mqtt.{REGION_CODE}.anedya.io"
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Create SSL context
    context.load_verify_locations(cafile="/certs/anedya_rca.cer")  # Load CA certificate
    mqtt_client = MQTTClient(
        client_id=PHYSICAL_DEVICE_ID,  # Create mqtt_client
        server=broker,
        port=8883,
        user=PHYSICAL_DEVICE_ID,
        password=CONNECTION_KEY,
        ssl=context,
    )  # Use SSL context for secure connection
    mqtt_client.set_callback(callback)  # Set callback function for incoming messages
    resp = mqtt_client.connect()  # Connect to broker
    if not resp:  # Check if connection was successful
        print("Connected to Anedya Broker")
    time.sleep(1)
    RES_TOPIC = f"$anedya/device/{PHYSICAL_DEVICE_ID}/response".encode(
        "ASCII"
    )  # Define response topic
    ERR_TOPIC = f"$anedya/device/{PHYSICAL_DEVICE_ID}/errors".encode(
        "ASCII"
    )  # Define error topic
    mqtt_client.subscribe(topic=RES_TOPIC)  # Subscribe to response topic
    mqtt_client.subscribe(topic=ERR_TOPIC)  # Subscribe to error topic


def callback(topic, msg):
    global time_res
    # Extract command and data from the JSON message
    res_json = json.loads(msg)
    if res_json.get("serverReceiveTime"):
        time_res = msg
        # print(msg)
    else:
        if res_json.get("errCode") == 0:
            print("Data pushed to Anedya!!")
        else:
            print("Failed to push data to Anedya!!")
            # Print the received message
            print(msg)


def anedya_set_device_time():
    global time_res
    print("Synchronizing device time...")
    time_topic = f"$anedya/device/{PHYSICAL_DEVICE_ID}/time/json"
    # Get the current uptime since the device started in seconds
    uptime_seconds = utime.ticks_ms()
    time_payload = json.dumps(
        {"deviceSendTime": uptime_seconds}
    )  # Adjust the deviceSendTime as needed
    time_sync_check = False

    while time_sync_check is False:
        try:
            mqtt_client.publish(time_topic, time_payload, qos=0)
            res_check = False
            counter = 0
            while res_check is False:
                mqtt_client.check_msg()  # Check for incoming messages
                if time_res != "":
                    parsed_data = json.loads(time_res)
                    # Extract serverSendTime in milliseconds
                    server_send_time_ms = parsed_data["serverSendTime"]
                    # print("Server Send Time (ms):", server_send_time_ms)

                    # Convert milliseconds to seconds (Unix timestamp)
                    server_send_time_sec = server_send_time_ms // 1000

                    # Set Pico's RTC time
                    # Set Pico's RTC time with India timezone (UTC+5:30)
                    rtc = machine.RTC()
                    tm = utime.localtime(server_send_time_sec)
                    rtc.datetime((tm[0], tm[1], tm[2], 0, tm[3], tm[4], tm[5], 0))
                    print("Time set successfully.")
                    res_check = True
                    time_sync_check = True
                    time_res = ""
                    break
                counter += 1
                print(f"[{counter}] waiting for response...")
                time.sleep(0.5)
                if counter > 10:
                    print("[failed] re-publishing on the topic")
                    break

        except Exception as e:
            print("Error:", e)


def anedya_submitData(variable, value):
    # Publish Topic
    PUBLISH_TOPIC = f"$anedya/device/{PHYSICAL_DEVICE_ID}/submitdata/json".encode(
        "ASCII"
    )

    current_time_ms = int(time.time()) * 1000  # time in milliseconds
    payload_hum = json.dumps(
        {  # Dictionary containing humidity data
            "data": [  # List containing humidity data
                {
                    "variable": variable,  # Variable identifier for humidity
                    "value": value,  # Humidity value
                    "timestamp": current_time_ms,  # Not used in this example
                }
            ]
        }
    )
    mqtt_client.publish(PUBLISH_TOPIC, payload_hum, qos=0)  # Publish humidity payload
    time.sleep(1)
    mqtt_client.check_msg()  # Check for incoming messages

if __name__ == "__main__":
    # Call the main function
    main()
