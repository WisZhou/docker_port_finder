# -*- coding: UTF-8 -*-

import argparse
import sys
import os
import re

# Commands to fetch port, process, and Docker information
GET_PORT_AND_PROCESS_COMMAND = 'ss -Hnlpt | awk \'{print $4" "$6}\''
GET_ALL_DOCKER_INFO_COMMAND = 'docker ps --format "{{.ID}} {{.Names}}"'
GET_DOCKER_PROCESS_ID_COMMAND_FORMAT = 'docker top %s | awk \'{print $2}\' | sed \'1d\''

# Containers for storing mapping information
port_and_process_container = {}
image_id_and_names_container = {}
process_and_image_id_container = {}


def prepare():
    # Fetch and process port and process information
    port_and_process_list = os.popen(GET_PORT_AND_PROCESS_COMMAND).readlines()
    for port_and_process_data in port_and_process_list:
        port_and_process_pairs = port_and_process_data.split(' ')
        port = int(port_and_process_pairs[0].split(':')[-1])
        pid_array = re.findall(r"pid=([0-9]+)", port_and_process_pairs[1])
        pid_array = [int(pid) for pid in pid_array]
        port_and_process_container[port] = pid_array

    # Fetch and process Docker container information
    image_infos = os.popen(GET_ALL_DOCKER_INFO_COMMAND).readlines()
    for image_info in image_infos:
        image_info_pairs = image_info.split(' ')
        image_id = image_info_pairs[0]
        image_name = image_info_pairs[1].strip()
        image_id_and_names_container[image_id] = image_name
        command = GET_DOCKER_PROCESS_ID_COMMAND_FORMAT % image_id
        container_pid_array = os.popen(command).readlines()
        pid_array = [int(pid) for pid in container_pid_array]
        for pid in pid_array:
            process_and_image_id_container[pid] = image_id


def find():
    # Argument parser for specifying the port to search for
    arg_parser = argparse.ArgumentParser(description='Find which Docker container is using a specific port')
    arg_parser.add_argument('port', type=int, help='Port number to search for')
    args = arg_parser.parse_args()
    target_port = args.port

    if target_port not in port_and_process_container:
        print('No container is using port [%d]' % target_port)
        sys.exit()

    pid_array = port_and_process_container[target_port]
    image_id_set = set()
    for pid in pid_array:
        if pid in process_and_image_id_container:
            image_id = process_and_image_id_container[pid]
            image_id_set.add(image_id)

    if not image_id_set:
        print('No container is using port [%d]' % target_port)
        sys.exit()

    print('Container(s) using port [%d]:' % target_port)
    print('##########')
    for image_id in image_id_set:
        print('container_id: %s, container_name: %s' % (image_id, image_id_and_names_container[image_id]))


if __name__ == '__main__':
    prepare()
    find()
