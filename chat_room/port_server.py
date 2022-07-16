"""
A server that saves port data for a server, and sends it to clients.
Author: Matan Weinman
"""
import socket as s, _thread as t, re
import select

ADDR = s.gethostbyname(s.gethostname())
PORT = 55555
BUFFER = 1024

NAME_REGEX = re.compile(r'^[\w\d]+([\w\d\-_ ]+)?$')
IP_REGEX = re.compile(r'^([1-2]?\d{1,2}.){3}[1-2]?\d{1,2}$')
PORT_CHECK = lambda x: x.isdigit() and 1 <= int(x) <= 65535

data_dict = {}
messages = {}

read_sockets = []
write_sockets = []

read_from_file = False  # Read the previous run's data from the file 'port_data.txt'
enter_shutdown = True  # Press 'Enter' to shut down the server.

is_running = True
is_waiting = True
comm_count = 0
shutdown_port = 0


def communicate(client, addr, data):
    """
    Handles communication with clients.
    :param client: The client socket.
    :param addr: The client address.
    :param data: The data received.
    """
    global comm_count, shutdown_port, read_sockets, write_sockets

    if addr[0] == ADDR and addr[1] == shutdown_port: return

    comm_count += 1
    print('Connected to ' + str(addr))

    if data.split(':')[0] == 'add': add_connection(client, data.split(':')[1:])
    if data.split(':')[0] == 'get': ask_for_port(client, data.split(':')[1:])
    if data.split(':')[0] == 'del': delete_query(client, data.split(':')[1:])

    read_sockets.remove(client)
    write_sockets.remove(client)
    print(str(addr) + ' has disconnected.')
    comm_count -= 1


def add_connection(client, data):
    """
    Lets a server add its IP and port.
    :param client: The client socket.
    :param data: The data received (name, IP and port).
    """
    name, ip, port = data
    if NAME_REGEX.findall(name) and IP_REGEX.findall(ip) and PORT_CHECK(port):
        if data[0] in data_dict.keys():
            messages[client].append('used'.encode())
        else:
            data_dict[name] = (ip, int(port))
            messages[client].append('ok'.encode())
    else:
        messages[client].append('no'.encode())


def ask_for_port(client, data):
    """
    Sends a server's address to a client.
    :param client: The client socket.
    :param data: The received data (server name).
    """
    name, = data
    if NAME_REGEX.findall(name):
        if name in data_dict.keys():
            messages[client].append(str(data_dict[name]).encode())
        else:
            messages[client].append('no'.encode())
    else:
        messages[client].append('format'.encode())


def delete_query(client, data):
    """
    Deletes a server's data from the server.
    :param client: The client socket.
    :param data: The data received (The server name.)
    """
    name, = data
    if NAME_REGEX.findall(name):
        if name in data_dict.keys():
            del data_dict[name]
            messages[client].append('ok'.encode())
        else:
            messages[client].append('no'.encode())
    else:
        messages[client].append('format'.encode())


def close_server():
    """
    Shuts down the server on Enter press (optional).
    """
    global is_running, is_waiting, comm_count, shutdown_port

    try: input()
    except ValueError: quit()  # Forced shutdown.
    is_running = False
    shutdown = s.socket(s.AF_INET, s.SOCK_STREAM)
    shutdown.connect((ADDR, PORT))
    shutdown_port = shutdown.getsockname()[1]
    print('The server will not receive any more clients.')
    shutdown.close()
    print('Waiting for ' + str(comm_count) + ' communications to end.')
    prev = comm_count
    while comm_count != 0:
        if comm_count != prev:
            print('Waiting for ' + str(comm_count) + ' communications to end.')
        prev = comm_count
    print('The server is shutting down.')
    is_waiting = False
    quit()


def main():
    global is_waiting, is_running, read_sockets, write_sockets

    if read_from_file:  # Reading the previous run's data.
        file = open('port_data.txt', 'r')
        content = file.read()
        file.close()
        for pair in content.split('\n')[:-1]:
            name = pair.split('_sep_')[0].strip(" '")
            content = eval(pair.split('_sep_')[1].strip())
            data_dict[name] = content
        print('Data loaded. Booting up server...')
    else: print('Booting up server...')

    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_socket.bind((ADDR, PORT))
    read_sockets.append(server_socket)

    if enter_shutdown: t.start_new_thread(close_server, ())

    print('Server up and running, awaiting connections.')
    server_socket.listen(3)

    while is_running:
        try: readable, writeable = select.select(read_sockets, write_sockets, [])[:-1]
        except KeyboardInterrupt: quit()
        for socket in readable:
            if socket == server_socket:
                sock, addr = socket.accept()
                read_sockets.append(sock)
                write_sockets.append(sock)
                messages[sock] = []
            else:
                data = socket.recv(BUFFER).decode()
                communicate(socket, socket.getsockname(), data)
        for socket in writeable:
            if messages[socket]:
                socket.send(messages[socket][0])
                if messages[socket]:
                    messages[socket] = messages[socket][1:]

    while is_waiting: pass  # Waiting for communications to end. Is handled from the shutdown thread.


if __name__ == '__main__':
    main()

    # Saving the data.
    print('Saving data...')
    file = open('port_data.txt', 'w')
    data = ''
    for key, value in data_dict.items():
        data += key + ' _sep_ ' + str(value) + '\n'
    file.write(data)
    file.close()
    print('Save successful.')
