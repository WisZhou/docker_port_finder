# Docker Port Finder

**Docker Port Finder** is a Python script designed to identify Docker containers that are listening on a specified port. The script outputs the container ID and container name if the port is being used by any running container. If no container is listening on the specified port, the script informs the user accordingly.

## Features

- Quickly find the Docker container that is listening on a specified port.
- Simple and easy-to-use command-line interface.

## Prerequisites

- Python 2.x 3.x
- Docker installed and running on the system

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/WisZhou/docker_port_finder.git 
cd docker_port_finder 
```

## Usage


```bash
root# python find_port.py 8105
Container(s) using port [8105]:
##########
container_id: 184f741c09f2, container_name: my_docer_service_1


root# python find_port.py 6105
No container is using port [6105]
```



