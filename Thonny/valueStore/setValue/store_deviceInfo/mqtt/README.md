[<img src="https://img.shields.io/badge/Anedya-Documentation-blue?style=for-the-badge">](https://docs.anedya.io?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico)

# Store-Device-Info - Example (mqtt)

This micropython script allows you to set the your value to the anedya.

## Getting Started

To get started with the examples:

1. Choose the code, create the .py file, and upload it in the pico space.
2. Fill in your Wi-Fi credentials, physical device ID, and connection key (obtained from the dashboard).
3. Upload the .cer file(Anedya ca-certificate) in the certs folder of pico. Obtain it from Anedya Documentation, [click here](https://docs.anedya.io/device/mqtt-endpoints/#tls)
   - Download `Anedya Root CA 1 (RSA - 2048)` `DER` file.
   - move it from Download folder to `C:\certs` in you local pc c drive.
   ![upload-doc](/Thonny/valueStore/setValue/store_deviceInfo/mqtt/doc/upload_cert_pico.png)
   - Now, open thonny and upload cert folder in pico space.

## Set-Up Project in Anedya Dashboard

Following steps outline the overall steps to setup a project. You can read more about the steps [here](https://docs.anedya.io/getting-started/quickstart/#create-a-new-project)

1. Create account and login
2. Create new project.
4. Create a node.

 > [!TIP]
 > For more details, Visit anedya [documentation](https://docs.anedya.io?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico)

## USAGES
To set the key-value, use : 
- `anedya_valueStore("<key>","<data-type>", "<ValuePayload")`
fill:-
  - 1 Parameter- key.
  - 2 Paramter- Data type,  `The value can hold any of the following types of data: string, binary, float, boolean`
  - 3 Parameter- value/message.

### Code Set-Up
1. Replace `<PHYSICAL-DEVICE-UUID>` with your 128-bit UUID of the physical device.
2. Replace `<CONNECTION-KEY>` with your connection key, which you can obtain from the node description.
3. Set up your WiFi credentials by replacing `SSID` and `PASSWORD` with your WiFi network's SSID and password.


> [!TIP]
> Looking for Python SDK? Visit [PyPi](https://pypi.org/project/anedya-dev-sdk/) or [Github Repository](https://github.com/anedyaio/anedya-dev-sdk-python)

>[!TIP]
> For more information, visit [anedya.io](https://anedya.io/?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico)