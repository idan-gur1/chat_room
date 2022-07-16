"""
client-server application
Author: Idan Gur
"""
import socket
import time
import random
import os
import struct
from select import select
from datetime import datetime


def find_open_port():
    """
    this function finds a free port on the local machine
    :return: int - port number
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


# change if need to be changed
PORT_SERVER = (socket.gethostbyname(socket.gethostname()), 55555)

# setting up Constants
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = find_open_port()
SERVER_NAME = ''
SERVER_PASSWORD = ''

START_TIME = time.time()

BUFF = 1024

WAKE_UP_MSG = ["Wake Up!", "Are you Still here?", "Send a message!", "I don't have all day!"]

# setting up server lists
waiting_for_file_send = {}  # socket:(size sent[bool], file name, file size)
wakeup_times = {}  # socket:(last msg time or last wakeup, wake up time how much)
names = {}  # socket:str
msg_recv_progress = {}  # socket:list[msg size, file size, msg, file(optional)]
clients = []
chat_sockets = []
messages_to_send = []
admins = []


def close_server(s):
    """
    this function handles the closing of the server and removing the server from the port server
    :param s: socket - server socket
    :return:
    """
    s.close()
    port_server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        port_server_s.connect(PORT_SERVER)
    except:
        print("port server is down")
    else:
        port_server_s.send(f'del:{SERVER_NAME}'.encode())
    finally:
        port_server_s.close()


def close_client(s):
    """
    this function handles the closing of a client and removing it from all the lists
    :param s: socket - client socket
    :return: None
    """
    print(f"[SERVER] {s.getpeername()} disconnected")
    if s in clients:
        clients.remove(s)
    if s in chat_sockets:
        chat_sockets.remove(s)
        for c in chat_sockets:
            messages_to_send.append((c, f"{names.get(s, 'user')} left,{len(chat_sockets)} Users are in chat".encode()))
    if s in names:
        names.pop(s)
    if s in wakeup_times:
        wakeup_times.pop(s)
    if s in msg_recv_progress:
        msg_recv_progress.pop(s)
    if s in waiting_for_file_send:
        waiting_for_file_send.pop(s)
    if s in admins:
        admins.remove(s)
    s.close()


def handle_client_data(data: bytes, client, server, file_data=None):
    global SERVER_PASSWORD
    """
    this function handles the user's data and commands
    :param data: bytes - the data received from the socket
    :param client: socket - the client socket
    :param server: socket - the server socket
    :return: None
    """

    str_data = data.decode()

    if client in chat_sockets:
        if str_data == "--leave":
            chat_sockets.remove(client)
            messages_to_send.append((client, f"[CHAT] you have left the chat".encode()))
            for c in chat_sockets:
                messages_to_send.append((c, f"{names.get(client, 'user')} left,{len(chat_sockets)} Users are in chat".encode()))
        elif str_data.startswith("--"):
            messages_to_send.append((client, "[CHAT] commands are not allowed in chat. you may use --leave to leave chat."))
        else:
            for c in chat_sockets:
                messages_to_send.append((c, f"[CHAT] {names.get(client, 'user')}: {str_data}".encode()))

    elif str_data.lower().startswith("--save file "):

        comm_data = str_data[12:].split(":")
        if len(comm_data) != 2:
            messages_to_send.append((client, f"[SERVER] the correct format for saving a file is: --save file <username to save under>:<full file name>".encode()))
        else:
            if not comm_data[0].isalnum():
                messages_to_send.append((client, f"[SERVER] Username can only contain letters and numbers!".encode()))
            elif "-" in comm_data[1]:
                messages_to_send.append((client, f"[SERVER] File name cannot contain -".encode()))
            else:
                file_name = f"{comm_data[0]}-{comm_data[1]}"
                with open(file_name, "wb") as f:
                    f.write(file_data)
                messages_to_send.append((client, f"[SERVER] the file {comm_data[1]} has been saved under the username {comm_data[0]}".encode()))

    elif str_data.lower().startswith("--get file "):
        comm_data = str_data[11:].strip().split(":")
        if len(comm_data) != 2:
            messages_to_send.append((client, f"[SERVER] The correct format for getting a file is: --get file <username the file is saved under>:<full file name>".encode()))
        else:
            if "-" in comm_data[1]:
                messages_to_send.append((client, f"[SERVER] File name cannot contain -".encode()))
            elif not os.path.isfile(f"{comm_data[0]}-{comm_data[1]}"):
                messages_to_send.append((client, f"[SERVER] File does not exists or username is wrong".encode()))
            else:
                file_name = f"{comm_data[0]}-{comm_data[1]}"
                with open(file_name, "rb") as f:
                    read_file = f.read()
                messages_to_send.append((client, read_file, (comm_data[1], os.path.getsize(file_name))))

    elif str_data.lower().startswith("--broadcast "):
        for c in clients:
            messages_to_send.append((c, f"[BROADCAST] {names.get(client, 'user')}: {str_data[12:]}".encode()))

    elif str_data.lower().startswith("--name "):
        if str_data[7:] in names.values():
            messages_to_send.append((client, f"[SERVER] name already exists!".encode()))
        else:
            messages_to_send.append((client, f"[SERVER] name changed to {str_data[7:]}".encode()))
            names[client] = str_data[7:]

    elif str_data.lower() == "--chat" or str_data.lower() == "--join chat":
        chat_sockets.append(client)
        for c in chat_sockets:
            messages_to_send.append((c, f"{names.get(client, 'user')} joined,{len(chat_sockets)} Users are in chat".encode()))

    elif str_data.lower() == "--time" or str_data.lower() == "--server local time":
        messages_to_send.append((client, f"[SERVER] Server local time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}".encode()))

    elif str_data.lower() == "--server up time":
        messages_to_send.append((client, f"[SERVER] Server up time: {round(time.time() - START_TIME, 3)} seconds".encode()))

    elif str_data.lower().startswith("--close"):
        if client in admins or str_data[8:] == SERVER_PASSWORD:
            close_server(server)
            return True
        else:
            messages_to_send.append((client, f"[SERVER] wrong password - log in as admin or supply correct password".encode()))

    elif str_data.lower().startswith("--admin "):
        if str_data[8:] == SERVER_PASSWORD:
            admins.append(client)
            messages_to_send.append((client, f"[SERVER] you are an admin".encode()))
        else:
            messages_to_send.append((client, f"[SERVER] wrong password - {str_data[8:]} is not thee correct password".encode()))

    elif str_data.lower() == "--online":
        if client in admins:
            messages_to_send.append((client, f"[SERVER] {len(clients)} clients are online: {','.join(names.values())}".encode()))
        else:
            messages_to_send.append((client, f"[SERVER] Only admins can use this command!. log in as admin".encode()))

    elif str_data.lower().startswith("--change pwd "):
        if client in admins:
            new_pwd = str_data[13:]
            SERVER_PASSWORD = new_pwd
            with open("password.txt", "w") as f:
                f.write(SERVER_PASSWORD)
            print("Password has been saved.")
            for admin in admins:
                messages_to_send.append((admin, f"[SERVER] Admin password has been changed to: {SERVER_PASSWORD}".encode()))
        else:
            messages_to_send.append((client, f"[SERVER] Only admins can use this command!. log in as admin".encode()))

    elif str_data.startswith("--"):
        messages_to_send.append((client, f"[SERVER] Unknown command!".encode()))

    else:
        messages_to_send.append((client, f"[SERVER] echo: ".encode() + data))

    return False


def send_messages(wlist):
    """
    this function sends the clients messages that are waiting to be sent
    :param wlist: list[socket] - list of sockets that can be send to
    :return: None
    """
    for message in messages_to_send:
        if len(message) == 3:
            client, data, (file_name, file_size) = message
        else:
            client, data = message
            file_size = 0
            file_name = ""
        if client not in clients:
            messages_to_send.remove(message)
            continue
        if client in wlist:
            try:
                if file_size > 0:
                    client.send(struct.pack("I", len(file_name.encode())) + struct.pack("I", file_size) + file_name.encode() + data)
                else:
                    client.send(struct.pack("I", len(data)) + struct.pack("I", 0) + data)
            except:
                pass

            messages_to_send.remove(message)


def send_wakeup():
    """
    this function send and calculate the wake up times for the clients and increasing the time spaces by 5 every wakeup
    :return: None
    """
    curr_time = time.time()

    for client, (last_time, time_space) in wakeup_times.items():
        if curr_time - last_time >= time_space:
            messages_to_send.append((client, f"{random.choice(WAKE_UP_MSG)}".encode()))
            wakeup_times[client] = (curr_time, time_space + 5)


def server_setup():
    global SERVER_NAME, SERVER_PASSWORD
    """
    this function deals with the port server and adds the server to the port server records
    and sets the server password
    :return: None
    """
    # adding this server to to the port server list (port server and server will be run on the same machine)
    port_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        port_server_socket.connect(PORT_SERVER)
    except:
        print("An error occurred while trying to connect to the port server.")
        print(f"Please connect the client manually with the following details:\nip: {SERVER_IP}, port: {SERVER_PORT}")
    else:
        while True:
            name = input("enter server name: ")
            port_server_socket.send(f"add:{name}:{SERVER_IP}:{SERVER_PORT}".encode())
            try:
                data = port_server_socket.recv(BUFF)
            except:
                print("An error occurred while trying to communicate with the port server.")
                print(f"Please connect the client manually with the following details:\nip: {SERVER_IP}, port: {SERVER_PORT}")
                break
            else:
                data = data.decode()
                if not data:
                    if input("The port server didn't answered. try again? (y/n): ") != "y":
                        print(f"Please connect the client manually with the following details:\nip: {SERVER_IP}, port: {SERVER_PORT}")
                        break
                    continue
                if data == 'no':
                    print("An error occurred with choosing the name. try again.")
                    continue
                elif data == 'used':
                    print("The name is already in use. please choose another one.")
                    continue
                else:
                    print(f"the server got added to the port server under the name {name}")
                    print(f"Server ip and port:\nip: {SERVER_IP}, port: {SERVER_PORT}")
                    break

    port_server_socket.close()

    # handling password setting
    if os.path.isfile("password.txt"):
        with open("password.txt", "r") as f:
            password = f.read()
        if input(f"Password file has been found, password - {password}. use it? (y/n): ") == "y":
            SERVER_PASSWORD = password
            return

    while True:
        inp = input("Enter admin password: ")
        if inp != "" and not inp.isspace() and inp.isascii():
            SERVER_PASSWORD = inp
            break
        print("the password can only contain ascii characters and cannot be empty")

    # saving server password if it is not saved
    with open("password.txt", "w") as f:
        f.write(SERVER_PASSWORD)
    print("Password has been saved.")


def main():
    server_setup()
    # setting up sever socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    print("[SERVER] listening for connections")
    run = True
    # main server loop
    while run:
        rlist, wlist, _ = select(clients + [server_socket], clients, [])

        # handling readable sockets
        for sock in rlist:
            # handling new client
            if sock is server_socket:
                try:
                    new_client, addr = server_socket.accept()
                except:
                    close_server(server_socket)
                    run = False
                    break
                print(f"[SERVER] new connection from {addr}")
                clients.append(new_client)
                msg_recv_progress[new_client] = []
                names[new_client] = str(addr)
                messages_to_send.append((new_client, f"welcome!".encode()))
                if len(clients) == 1:
                    messages_to_send.append((new_client, f"you are the first to join, so you are admin. password: {SERVER_PASSWORD}".encode()))
                    admins.append(new_client)
                wakeup_times[new_client] = (time.time(), 10)

            # handling client request
            else:
                try:
                    if len(msg_recv_progress[sock]) == 0 or len(msg_recv_progress[sock]) == 1:
                        # msg size or file size
                        data = sock.recv(struct.calcsize("I"))
                    elif len(msg_recv_progress[sock]) == 2:
                        # msg
                        data = sock.recv(msg_recv_progress[sock][0])
                    elif len(msg_recv_progress[sock]) == 3:
                        # file
                        data = b''
                        while len(data) < msg_recv_progress[sock][1]:
                            fragment = sock.recv(msg_recv_progress[sock][1] - len(data))
                            if not fragment:
                                close_client(sock)
                                continue
                            data = data + fragment
                    else:
                        data = None
                except:
                    close_client(sock)
                    continue

                if not data:
                    close_client(sock)
                    continue

                if len(msg_recv_progress[sock]) == 0 or len(msg_recv_progress[sock]) == 1:
                    try:
                        msg_recv_progress[sock].append(struct.unpack("I", data)[0])
                    except:  # not a integer
                        msg_recv_progress[sock].clear()

                elif len(msg_recv_progress[sock]) == 2:
                    if msg_recv_progress[sock][1] > 0:
                        msg_recv_progress[sock].append(data)
                    else:
                        need_out = handle_client_data(data, sock, server_socket)
                        msg_recv_progress[sock].clear()
                        # if server need to close
                        if need_out:
                            run = False
                            break
                elif len(msg_recv_progress[sock]) == 3:
                    need_out = handle_client_data(msg_recv_progress[sock][2], sock, server_socket, data)
                    msg_recv_progress[sock].clear()
                    if need_out:
                        run = False
                        break

                # updating wakeup
                wakeup_times[sock] = (time.time(), 10)

        # handling server wakeup
        send_wakeup()
        # handling writeable sockets
        send_messages(wlist)


if __name__ == '__main__':
    main()
