""""
                            Store-Device-Info - Example-ValueStore(mqtt)
                Disclaimer: This code is for hobbyists for learning purposes. Not recommended for production use!!

                           # Dashboard Setup
                             - Create account and login to the dashboard
                             - Create new project.
                             - Create a node (e.g., for home- Room1 or study room).

                  Note: The code is tested on the "Raspberry Pi Pico W"
                  For more info, visit- https://docs.anedya.io/valuestore/intro

                                                                                           Dated: 20-August-2024
"""

import network
import ujson as json
import time
import utime
import ssl
from umqtt.simple import MQTTClient
import machine
import ubinascii
import os


# --------------------settings--------------------
# Emulate Hardware Sensor?
virtual_sensor = True

# ---------------------- Anedya essential credentials ----------------------
REGION_CODE = "ap-in-1"
CONNECTION_KEY = b"CONNECTION_KEY"  # Fil your Connection Key
PHYSICAL_DEVICE_ID = "PHYSICAL_DEVICE_ID"  # Fill your unique Physical Device ID
#  ----------------WiFi Credentials-----------------------
SSID = "SSID"  # SSID of the WiFi network
PASSWORD = "PASSWORD"  # Password of the WiFi network

# ----------------------- sensor config --------------------------------
# 0----------------------- helper variables --------------------------------
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

        if utime.ticks_ms() - interval_time > 5000:  # interval
            # Update interval time
            interval_time = utime.ticks_ms()

            print("=============================================")
            # Get Chip ID (using MAC address as an equivalent)
            chip_id = ubinascii.hexlify(machine.unique_id()).decode()

            # Get CPU frequency in MHz
            cpu_frequency = machine.freq() // 1000000

            # Get Flash size (filesystem size)
            flash_size = os.statvfs("/")[0] * os.statvfs("/")[1] // 1024 // 1024

            # Get Free filesystem space
            total_sketch_space = os.statvfs("/")[2] * os.statvfs("/")[0] // 1024
            free_sketch_space = os.statvfs("/")[3] * os.statvfs("/")[0] // 1024

            # Get Flash speed (fixed for Pico W)
            flash_speed = 133  # The Pico W typically runs at 133 MHz

            # Create JSON object
            board_info = {
                "Chip ID": chip_id,
                "CPU Frequency": f"{cpu_frequency} MHz",
                "Flash Size": f"{flash_size} MB",
                "Total Filesystem Space": f"{total_sketch_space} KB",
                "Free Filesystem Space": f"{free_sketch_space} KB",
                "Flash Speed": f"{flash_speed} MHz",
            }

            str_boardInfo = json.dumps(board_info)
            anedya_setValue("Device Info", "string", str_boardInfo)
            anedya_setValue("flash_speed", "float", flash_speed)
            print("=============================================")

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
    else:
        if res_json.get("errorcode") == 0:
            print("value set!!")
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


def anedya_setValue(param_key: str, param_value_type: str, param_value):

    PUBLISH_TOPIC = f"$anedya/device/{PHYSICAL_DEVICE_ID}/valuestore/setValue/json"
    valueStore_payload = json.dumps(
        {
            "reqId": "",
            "key": param_key,
            "value": param_value,
            "type": param_value_type,
        }
    )
    mqtt_client.publish(
        PUBLISH_TOPIC, valueStore_payload, qos=0
    )  # Publish humidity payload
    time.sleep(1)
    mqtt_client.check_msg()  # Check for incoming messages


if __name__ == "__main__":
    # Call the main function
    main()
