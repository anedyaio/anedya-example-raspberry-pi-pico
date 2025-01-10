[<img src="https://img.shields.io/badge/Anedya-Documentation-blue?style=for-the-badge">](https://docs.anedya.io?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico)

# Value store

<p align="center">
    <img src="https://cdn.anedya.io/anedya_black_banner.png" alt="Logo">
</p>

ValueStore is a highly available and consistent key-value store designed specifically for Internet of Things (IoT) applications, offered as part of the services provided by Anedya. It provides a mechanism for storing and retrieving data using key-value pairs, organized within namespaces for efficient data management. From the overview, it appears as a normal key-value store, but it's designed to solve some of the very important IoT use-case scenarios.

## Operation
### Read Operations​
- **Node-Level Scope:** A node can read data from its own namespace (matching node ID).
- **Global Scope:** All nodes can read data from any global namespace. This facilitates access to shared data sets across the entire system.
### Write Operations
- **Node-Level Scope:** A node can only write data to its own namespace (matching node ID). This restricts nodes from modifying data belonging to other devices or global namespaces.
- **Global Scope:** Only applications can write to or modify global namespaces using Platform APIs or the Anedya Dashboard. This ensures controlled modification of shared data sets to maintain data integrity.


## Documentation

For detailed documentation, refer to the official documentation [here](https://docs.anedya.io/).

## License

This project is licensed under the [MIT License](https://github.com/anedyaio/anedya-example-raspberry-pi-pico/blob/main/LICENSE).

> [!TIP]
> Looking for Python SDK? Visit [PyPi](https://pypi.org/project/anedya-dev-sdk/) or [Github Repository](https://github.com/anedyaio/anedya-dev-sdk-python)

>[!TIP]
> For more information, visit [anedya.io](https://anedya.io/?utm_source=github&utm_medium=link&utm_campaign=github-examples&utm_content=pico) 