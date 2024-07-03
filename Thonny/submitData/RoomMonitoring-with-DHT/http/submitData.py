import network
import urequests as requests
import ujson as json
import time
import utime
import random
from dht import DHT11
from machine import Pin

# Emulate Hardware Sensor?
virtual_sensor = False

REGION_CODE="ap-in-1"
CONNECTION_KEY = "CONNECTION_KEY"
PHYSICAL_DEVICE_ID = "PHYSICAL_DEVICE_ID"
# WiFi credentials
SSID = 'ssid'
PASSWORD = 'password'

dataPin=16
myPin=Pin(dataPin,Pin.OUT,Pin.PULL_DOWN)
sensor=DHT11(myPin)

def main():
    connect_to_wifi(SSID, PASSWORD)
    anedya_set_device_time()

    while True :
        
        if virtual_sensor:
            temperature = random.randint(1, 50) 
            humidity =random.randint(10, 70)
        else:
            try:
                sensor.measure()
            except:
                pass
            temperature=sensor.temperature()
            humidity=sensor.humidity()

        print(f"Humidity :{humidity}%")
        anedya_submitData("humidity",humidity)
        print(f"Temperature :{temperature}°C")
        anedya_submitData("temperature",temperature)

        
        time.sleep(2)

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
def anedya_set_device_time():
    print("Synchronizing device time...")
    url = "https://device.ap-in-1.anedya.io/v1/time"
    # Get the current uptime since the device started in seconds
    uptime_seconds = utime.ticks_ms() 
    payload = {"deviceSendTime": uptime_seconds}  # Adjust the deviceSendTime as needed
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Auth-mode': 'key',
        'Authorization': CONNECTION_KEY
    }
    try:
        # Make the POST request to get serverSendTime
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            time_message = response.text
            parsed_data = json.loads(time_message)
            # Extract serverSendTime in milliseconds
            server_send_time_ms = parsed_data['serverSendTime']
            #print("Server Send Time (ms):", server_send_time_ms)

            # Convert milliseconds to seconds (Unix timestamp)
            server_send_time_sec = (server_send_time_ms // 1000)

            # Set Pico's RTC time
            # Set Pico's RTC time with India timezone (UTC+5:30)
            rtc = machine.RTC()
            tm = utime.localtime(server_send_time_sec)
            rtc.datetime((tm[0], tm[1], tm[2], 0, tm[3], tm[4], tm[5], 0))
            print("Time set successfully.")

        else:
            print("Failed to fetch time from server. Status code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

# Function to submit data to Anedya
def anedya_submitData(param_variable_identifier: str, param_variable_value: float):
    url = f"https://device.{REGION_CODE}.anedya.io/v1/submitData"

    payload = json.dumps({
        "data": [
            {
                "variable": param_variable_identifier,
                "value": param_variable_value,
                "timestamp": int(time.time() * 1000)  # convert to milliseconds
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Auth-mode': 'key',
        'Authorization': CONNECTION_KEY
    }

    response = requests.post(url, headers=headers, data=payload)

    # Optional: Print the response for debugging
    if response.status_code == 200:
        print("Data pushed to anedya could!!")
    else:
        print("Failed to push data!!")
        print(response.text)
    response.close()  # Close the response to free resources


if __name__ == '__main__':
    main()