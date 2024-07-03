[<img src="https://img.shields.io/badge/Anedya-Documentation-blue?style=for-the-badge">](https://docs.anedya.io?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico)

# Room Monitoring - Submit-data-with-Pico+DHT (http)

This  file allows you to connect your device to a WiFi network and send data to a server. It fetches the server time and sends data to the anedya.


> [!WARNING]
> This code is for hobbyists for learning purposes. Not recommended for production use!!

## Set-Up Project in Anedya Dashboard

Following steps outline the overall steps to setup a project. You can read more about the steps [here](https://docs.anedya.io/getting-started/quickstart/#create-a-new-project)

1. Create account and login
2. Create new project.
3. Create variables: temperature and humidity.
4. Create a node (e.g., for home- Room1 or study room).

 > [!TIP]
 > For more details, Visit anedya [documentation](https://docs.anedya.io?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico)

> [!IMPORTANT]
> Variable Identifier is essential; fill it accurately.

## Hardware Set-Up

You can run the code without any hardware sensor also,Simply keep `virtual_sensor=true` or

To send hardware sensor value `virtual_Sensor = false`

1. Properly identify your sensor's pins.
2. Connect sensor VCC pin to 3V3.
3. Connect sensor GND pin to GND.
4. Connect sensor signal pin to 16.

### Code Set-Up

1. Replace `<PHYSICAL-DEVICE-UUID>` with your 128-bit UUID of the physical device.
2. Replace `<CONNECTION-KEY>` with your connection key, which you can obtain from the node description.
3. Set up your WiFi credentials by replacing `SSID` and `PASSWORD` with your WiFi network's SSID and password.
4. Specify the pin number connected to the DHT sensor.



> [!TIP]
> Looking for Python SDK? Visit [PyPi](https://pypi.org/project/anedya-dev-sdk/) or [Github Repository](https://github.com/anedyaio/anedya-dev-sdk-python)

>[!TIP]
> For more information, visit [anedya.io](https://anedya.io/?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico)