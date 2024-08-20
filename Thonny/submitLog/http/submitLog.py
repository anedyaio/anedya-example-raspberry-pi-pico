""""
                            Room Monitoring Using Raspberry pi pico + DHT sensor with log submission (http)
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
import urequests as requests
import ujson as json
import time
import utime
import random
from dht import DHT11
from machine import Pin

#---------------- settings ------------------------
# Emulate Hardware Sensor?
virtual_sensor = True

#---------------------- Anedya essential credentials ----------------------
REGION_CODE = "ap-in-1"
CONNECTION_KEY = "CONNECTION_KEY"  # Fil your Connection Key
PHYSICAL_DEVICE_ID = "PHYSICAL_DEVICE_ID"  # Fill your unique Physical Device ID
#  ----------------WiFi Credentials-----------------------
SSID = "SSID"  # SSID of the WiFi network
PASSWORD = "PASSWORD"  # Password of the WiFi network

#---------------- Sensors -----------------------------
dht_pin = 16
myPin = Pin(dht_pin, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(myPin)

#---------------- Helper varaibles -----------------------------
counter = 0

def main():
    connect_to_wifi(SSID, PASSWORD)
    anedya_set_device_time()

    while True:
        if virtual_sensor:
            temperature = random.randint(1, 50)
            humidity = random.randint(10, 70)
        else:
            try:
                sensor.measure()
            except:
                anedya_submitLog("", "Failed to read from DHT !")
            temperature = sensor.temperature()
            humidity = sensor.humidity()

        print("=============================================")
        print(f"Humidity :{humidity}%")
        anedya_submitData("humidity", humidity)
        anedya_submitLog("", f"Humidity: {humidity}%","DATA")
        print(f"Temperature :{temperature}°C")
        anedya_submitData("temperature", temperature)
        anedya_submitLog("", f"Temperature: {temperature}C","DATA")
        print("=============================================")

        time.sleep(2)


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

def anedya_set_device_time():
    print("Synchronizing device time...")
    url = "https://device.ap-in-1.anedya.io/v1/time"
    # Get the current uptime since the device started in seconds
    uptime_seconds = utime.ticks_ms()
    payload = {"deviceSendTime": uptime_seconds}  # Adjust the deviceSendTime as needed
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Auth-mode": "key",
        "Authorization": CONNECTION_KEY,
    }
    try:
        # Make the POST request to get serverSendTime
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            time_message = response.text
            parsed_data = json.loads(time_message)
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

        else:
            print(
                "Failed to fetch time from server. Status code:", response.status_code
            )
            print("Response:", response.text)
    except Exception as e:
        print("Error:", e)


# Function to submit data to Anedya
def anedya_submitData(param_variable_identifier: str, param_variable_value: float):
    url = f"https://device.{REGION_CODE}.anedya.io/v1/submitData"

    current_time_ms=int(time.time()*1000)

    payload = json.dumps(
        {
            "data": [
                {
                    "variable": param_variable_identifier,
                    "value": param_variable_value,
                    "timestamp": current_time_ms,  # convert to milliseconds
                }
            ]
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Auth-mode": "key",
        "Authorization": CONNECTION_KEY,
    }
    response = requests.post(url, headers=headers, data=payload, timeout=10)

    # Optional: Print the response for debugging
    if response.status_code == 200:
        print("Data pushed to anedya cloud!!")
    else:
        print("Failed to push data!!")
        error_code = json.loads(response.text).get("errorcode")
        if error_code == 4020:
            print("Error: Unknown variable identifier!!")
        else:
            print(response.text)
    response.close()  # Close the response to free resources


# Function to submit log to Anedya
def anedya_submitLog(param_req_id: str, param_log: str, param_logType: str = "INFO"):
    global counter
    counter += 1
    url = f"https://device.{REGION_CODE}.anedya.io/v1/logs/submitLogs"

    current_time_ms=int(time.time())*1000
    log_with_counter = f"[{param_logType}][{counter}]-{param_log}"
    payload = json.dumps(
        {"reqId": param_req_id, "data": [{"timestamp": current_time_ms, "log": log_with_counter}]}
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Auth-mode": "key",
        "Authorization": CONNECTION_KEY,
    }

    response = requests.post(url, headers=headers, data=payload, timeout=10)

    # Optional: Print the response for debugging
    if response.status_code == 200:
        print(f"{log_with_counter} Sent!!")
    else:
        print("Failed to push data!!")
        error_code = json.loads(response.text).get("errorcode")
        if error_code == 4020:
            print("Error: Unknown variable identifier!!")
        else:
            print(response.text)
    response.close()  # Close the response to free resources


if __name__ == "__main__":
    main()
