""""
                            Store-Device-Info - Example-ValueStore(http)
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
import urequests as requests
import ujson as json
import ubinascii
import os
import time
import utime
import machine


#---------------------- Anedya essential credentials ----------------------
REGION_CODE = "ap-in-1"
CONNECTION_KEY = "CONNECTION_KEY"  # Fil your Connection Key
PHYSICAL_DEVICE_ID = "PHYSICAL_DEVICE_ID"  # Fill your unique Physical Device ID
#  ----------------WiFi Credentials-----------------------
SSID = "SSID"  # SSID of the WiFi network
PASSWORD = "PASSWORD"  # Password of the WiFi network

# ---------------- Sensors -----------------------------
# ---------------- Helper varaibles -----------------------------


def main():
    connect_to_wifi(SSID, PASSWORD)
    anedya_set_device_time()

    while True:
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
        time.sleep(10)


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


# Function to submit log to Anedya
def anedya_setValue(param_key: str, param_value_type: str, param_value):

    url = f"https://device.{REGION_CODE}.anedya.io/v1/valuestore/setValue"
    payload = json.dumps(
        {
            "reqId": "",
            "key": param_key,
            "value": param_value,
            "type": param_value_type,
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
        print(f"[{param_key}] Value Set!!")
    else:
        print(f"{response.status_code}: {response.text}")
    response.close()  # Close the response to free resources


if __name__ == "__main__":
    main()
