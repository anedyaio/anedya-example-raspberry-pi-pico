[<img src="https://img.shields.io/badge/Anedya-Documentation-blue?style=for-the-badge">](https://docs.anedya.io?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico)

# Basic-Home-Automation

<p align="center">
    <img src="https://cdn.anedya.io/anedya_black_banner.png" alt="Logo">
</p>

This project is designed for users looking to implement a basic home automation system. The  sketch provided enables users to monitor key environmental parameters such as humidity and temperature, which are crucial for maintaining a comfortable living space. Additionally, the system allows for remote control of connected devices, 
offering convenience and enhancing the overall smart home experience.

With Anedya's platform, you can send commands to your devices and receive real-time updates on your environment's conditions. The integration with the [anedya-streamlit-dashboard-example](https://github.com/anedyaio/anedya-streamlit-dashboard-example) web app provides a user-friendly and customizable interface for interacting with your home automation system. The Anedya dashboard further enhances this by offering advanced features and analytics to help you optimize your home automation setup.

## Getting Started

To get started with the examples:

1. Choose the code, create the .py file, and upload it in the pico space.
2. Fill in your Wi-Fi credentials, physical device ID, and connection key (obtained from the dashboard).
3. Upload the .cer file(Anedya ca-certificate) in the certs folder of pico. Obtain it from Anedya Documentation, [click here](https://docs.anedya.io/device/mqtt-endpoints/#tls)
   - Download `Anedya Root CA 1 (RSA - 2048)` `DER` file.
   - move it from Download folder to `C:\certs` in you local pc c drive.
   ![upload-doc](/Thonny/basic-home-automation/doc/upload_cert_pico.png)
   - Now, open thonny and upload cert folder in pico space.


## Usage
 
### anedya-streamlit-dashboard-example setup

![Image](https://github.com/anedyaio/anedya-streamlit-dashboard-example/blob/main/docs/main_dash.png)


1. Clone the Repository:
Clone [anedya-streamlit-dashboard-example](https://github.com/anedyaio/anedya-streamlit-dashboard-example.git) repo from anedya github.
```
git clone https://github.com/anedyaio/anedya-streamlit-dashboard-example.git
cd anedya-streamlit-dashboard-example

```
2. Install Dependencies:
To ensure the application has all the necessary libraries, you'll need to install the dependencies listed in the requirements.txt file. This file contains a list of all the packages along with their versions that the app depends on.
Here's how to install these dependencies:
- Open a terminal or command prompt.
- Navigate to the directory where you cloned the repository.
- Run the following command to install the dependencies using pip:
```
pip install -r requirements.txt
```
This command reads the `requirements.txt` file and installs all the listed packages.

3. Obtain your nodeid and apikey from the Anedya dashboard. These credentials are necessary for connecting your application to the Anedya platform. Once you have these, You need to replace <PHYSICAL-DEVICE-UUID> and <CONNECTION-KEY> with your actual device ID and connection key, respectively. 

4. Run the Streamlit App:
Start the Streamlit server:
```
streamlit run Home.py

```
This will launch the dashboard in your default web browser. [Host it on the streamlit cloud](https://github.com/anedyaio/anedya-streamlit-dashboard-example/blob/main/README.md#hosting-on-streamlit-cloud)


## Documentation

For detailed documentation, refer to the official documentation [here](https://docs.anedya.io/).

## License

This project is licensed under the [MIT License](https://github.com/anedyaio/anedya-example-raspberry-pi-pico/blob/main/LICENSE).

> [!TIP]
> Looking for Python SDK? Visit [PyPi](https://pypi.org/project/anedya-dev-sdk/) or [Github Repository](https://github.com/anedyaio/anedya-dev-sdk-python)

>[!TIP]
> For more information, visit [anedya.io](https://anedya.io/?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico) 