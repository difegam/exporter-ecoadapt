# Exporter Ecoadapt

The Exporter-Ecoadapt is a ModBus proof of concept project.

The project involves creating a bridge between the ModBus sensor and the webserver backend. The bridge is a device that reads the voltage and frequency from the sensor and sends the data to a server periodically. The server is built using Python and WebSocket technology.

The project uses Docker to manage the different components of the system. The project consists of three services: exporter-ecoadapt, sensorfact-server, and modbus-server. The exporter-ecoadapt service is responsible for reading the data from the ModBus sensor, while the sensorfact-server service receives the data and sends it to the cloud. The modbus-server service provides the ModBus protocol.

The project uses the Autobahn library to implement the WebSocket protocol. The code includes error handlers to handle exceptions in case of connection issues or other errors.

The project is designed to be scalable and easy to maintain. The code is well-documented and follows best practices in software development.

## Services

- **Exporter Ecoadapt** The service that reads the data from the sensor and sends it to the server.
- [**Modbus server** - localhost:5020 - Modbus server for debugging and simulation. .](http://localhost:5020)
- [**Webserver** - localhost:9000: A local webserver to receive message sent by exporter](http://localhost:9000)

---

- Modbus server documentation [ _oitc/modbus-server_](https://hub.docker.com/r/oitc/modbus-server)

## How to use

To use this project, please follow these steps:

1. Clone the git repository to your local machine using the following command:

```bash
git clone https://github.com/difegam/exporter-ecoadapt.git
```

2. Install Docker and Docker Compose on your system. Instructions on how to install Docker and Docker Compose can be found in the official documentation:

- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

3. Navigate to the project directory and run the following command to build and run the Docker containers:

```bash
docker-compose up --build --force-recreate
```

4. Once the containers are up and running, you will see the output of the services.

5. The Docker Compose file includes three services:

- **exporter-ecoadapt:** The service that reads the data from the sensor and sends it to the server.
- **sensorfact-server:** The server that receives the data from the exporter-ecoadapt service and pinrt it on console.
- **modbus-server:** The service that emulates the Eco-Adapt Power Elec sensor and makes the data available via Modbus.

6. To stop the containers, run the following command in the project directory:

```bash
docker-compose down
```

## Documentation

### modbus protocol

- [📄 Modbus interface tutorial](https://www.lammertbies.nl/comm/info/modbus)
- [📄 Detailed description of the Modbus TCP protocol](https://ipc2u.com/articles/knowledge-base/detailed-description-of-the-modbus-tcp-protocol-with-command-examples/)
- [📄 The modbus protocol documentation](https://github.com/pymodbus-dev/pymodbus/blob/dev/doc/source/_static/Modbus_Application_Protocol_V1_1b3.pdf)
- [📺 Using Modbus for IoT Applications](https://www.youtube.com/watch?v=nelI0ErgYuk&list=PL7QFPg5Pk4_UToNB7pyUDfKjn3kGHA1dW)

### PyModbus

- [📄 readthedocs](https://pymodbus.readthedocs.io/en/latest/index.html)

### autobahn-python

- [📄 readthedocs](https://autobahn.readthedocs.io/en/latest/contents.html)
- [💻 github](https://github.com/crossbario/autobahn-python)

### oitc/modbus-server

- [oitc/modbus-server](https://hub.docker.com/r/oitc/modbus-server)

## Authors

- [@difegam](https://github.com/difegam)
