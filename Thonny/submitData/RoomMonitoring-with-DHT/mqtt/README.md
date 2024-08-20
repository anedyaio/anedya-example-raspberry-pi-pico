[<img src="https://img.shields.io/badge/Anedya-Documentation-blue?style=for-the-badge">](https://docs.anedya.io?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico)

# Room Monitoring - Submit-data-with-Pico+DHT (mqtt)

<p align="center">
    <img src="https://cdn.anedya.io/anedya_black_banner.png" alt="Logo">
</p>

This micropython script allows you to connect your device to a WiFi network and send data to a server. It fetches the live time from the anedya server to synchronize the device time and sends data to the anedya.

## Getting Started

To get started with the examples:

1. Choose the code, create the .py file, and upload it in the pico space.
2. Fill in your Wi-Fi credentials, physical device ID, and connection key (obtained from the dashboard).
3. Upload the .cer file(Anedya ca-certificate) in the certs folder of pico. Obtain it from Anedya Documentation, [click here](https://docs.anedya.io/device/mqtt-endpoints/#tls)
   - Download `Anedya Root CA 1 (RSA - 2048)` `DER` file.
   - move it from Download folder to `C:\certs` in you local pc c drive.
   ![upload-doc](/Thonny/basic-home-automation/pico/doc/upload_cert_pico.png)
   - Now, open thonny and upload cert folder in pico space.

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

## Usage

1. Connect your device to a WiFi network.
2. Save this code to your device.
3. Open the Serial Monitor to view the device's output.
4. The device will connect to the WiFi network, read temperature and humidity data from the DHT sensor, and start sending data to the Anedya.

## Documentation

For detailed documentation, refer to the official documentation [here](https://docs.anedya.io/).

## License

This project is licensed under the [MIT License](https://github.com/anedyaio/anedya-example-nodemcu/blob/main/LICENSE).

> [!TIP]
> Looking for Python SDK? Visit [PyPi](https://pypi.org/project/anedya-dev-sdk/) or [Github Repository](https://github.com/anedyaio/anedya-dev-sdk-python)

>[!TIP]
> For more information, visit [anedya.io](https://anedya.io/?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico) 