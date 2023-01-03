'''
@README

In CentOS/RHEL operating system side one have to reserve a range of ports needed by the third-party application,
and it is important to be aware that the port range will not strictly reserve the port for a any specific application
but in the application side is where one has to set the port to be used by that specific application.

Script for testing if Linux files for setting ranges and reserving ports are working correctly.
If you bind a socket to port 0, the kernel will assign it a free port. It works for windows and Linux.

File with port ranges which Kernel will choose from:
> cat /proc/sys/net/ipv4/ip_local_port_range

Set port ranges:
> sudo sysctl -w net.ipv4.ip_local_port_range="60990 60999"

File with ports which are not in the current ip_local_port_range:
> cat /proc/sys/net/ipv4/ip_local_reserved_ports

Set list of reserved ports:
> sudo sysctl -w net.ipv4.ip_local_reserved_ports="60993,60995,60997"

ip_local_port_range and ip_local_reserved_ports settings are independent
and both are considered by the kernel when determining which ports are available for automatic port assignments.

Tested with:
> python2 portTest.py (2.7.18)
> python3 portTest.py (3.8.5)
'''

import socket

def free_port():
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    free_socket.bind(('0.0.0.0', 0))
    free_socket.listen(5)
    port = free_socket.getsockname()[1]
    free_socket.close()
    return port

if __name__ == "__main__":

    pathToFile = '/proc/sys/net/ipv4/ip_local_reserved_ports'
    reservedPortsFile = open(pathToFile, 'r').read()
    reservedPortsList = reservedPortsFile.rstrip().split(",")

    pathToFile = '/proc/sys/net/ipv4/ip_local_port_range'
    portsRange = open(pathToFile, 'r').read()
    portsRangeList = portsRange.strip().split("\t")

    print("Ports range: {}".format(' '.join(portsRangeList)))
    print("Reserved ports: {}".format(' '.join(reservedPortsList)))

    portsList = []
    for i in range(1000):
        freePortAddress = free_port()
        portsList.append(freePortAddress)

    checkIfContainsAnyReservedPort = any(item in portsList for item in reservedPortsList)

    if checkIfContainsAnyReservedPort is True:
        print("Whoops, there is a restricted port in list!")
    else:
        print("Yay, list of reserved ports works correctly!")
