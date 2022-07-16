"""
client-server application
Author: Idan Gur
"""
import _thread
import os
import struct
from socket import *
from tkinter import *
from tkinter import messagebox

PORT_SERVER = (gethostbyname(gethostname()), 55555)


def clear_screen():
    """
    clear the root screen
    :return: None
    """
    for widget in root.winfo_children():
        widget.destroy()


def port_server_screen():
    """
    creates a tkinter screen to connect to the port server
    :return: None
    """
    # server name input screen
    clear_screen()

    title_lbl = Label(root, text='enter the server name:', font=('Ariel', 20, 'bold'), bg='white')
    title_lbl.pack(pady=30)

    name_entry = Entry(root, width=30, font=('Ariel', 14), bd=2)
    name_entry.pack(pady=20)
    name_entry.bind('<Return>', lambda e: communicate_with_port_server(name_entry.get()))

    enter_btn = Button(root, text="Enter", bg="#f3f3f3", bd=0, command=lambda: communicate_with_port_server(
        name_entry.get()),
                       font=('Ariel', 16, 'bold'))
    enter_btn.pack(pady=20)


def communicate_with_port_server(name):
    """
    communicate with port server to get the ip and port of server
    :param name: name of wanted server
    :return: None
    """
    # return port and addr from port server by server name

    PORT_SERVER_ADDR = PORT_SERVER[0]
    PORT_SERVER_PORT = PORT_SERVER[1]

    # create socket to port server
    port_server_sock = socket(AF_INET, SOCK_STREAM)
    try:
        port_server_sock.connect((PORT_SERVER_ADDR, PORT_SERVER_PORT))
    except:
        messagebox.showerror("error", "cannot connect to port server")
        return

    # send get request to port server
    port_server_sock.send(f'get:{name}'.encode())
    try:
        recv = port_server_sock.recv(BUFF).decode()
    except:
        messagebox.showerror("error", "an error has occurred while communicating with port server")
        return
    port_server_sock.close()
    if not recv:
        messagebox.showerror("error", "port server did not answer. try again")
        return
    if recv == 'no':
        messagebox.showerror("error", "this server name does not exists in the port server. try again")
    else:
        addr = eval(recv)
        try:
            sock.connect(addr)
        except:
            messagebox.showerror("error", "cannot connect to server")
            return

        main_screen()


def server_down(client_exit=False):
    """
    tkinter screen to handle disconnect
    :param client_exit: to check if it was client disconnect or server disconnect
    :return: None
    """
    clear_screen()
    sock.close()
    title_lbl = Label(root, text='Connection to the server has been lost.\npress this button to quit'
                      if not client_exit else 'You disconnected.\npress this button to quit',
                      font=('Ariel', 20), bg='white')
    title_lbl.pack(pady=50)

    home_btn = Button(root, text="Quit", bg="#f3f3f3", bd=0, command=lambda: root.quit(),
                      font=('Ariel', 18, 'bold'))
    home_btn.pack(pady=20)


def handle_send_data(lst, entry):
    """
    handle tkinter part of sending message
    :param lst: tkinter list box
    :param entry: tkinter entry
    :return: None
    """
    data = entry.get().strip()
    entry.delete(0, END)
    client_out = False
    if data and not data.isspace():
        client_out = send_to_server(data, lst)
    if not client_out:
        lst.insert(END, f">>{data}")
        lst.see(END)


def send_to_server(data, lst):
    """
    sending data to the server
    :param data: str - data to be sent
    :param lst: tkinter list box
    :return: bool - need to disconnect or not
    """
    global connected

    # if sends EXIT disconnect
    if data == '--quit':
        connected = False
        server_down(True)
        return True

    if data.startswith("--save file "):
        msg = f"{data.strip()}".encode()
        if os.path.isfile(data[12:].strip().split(':')[1]):
            with open(data[12:].strip().split(':')[1], "rb") as f:
                file_data = f.read()

            sock.send(struct.pack("I", len(msg)) + struct.pack("I", os.path.getsize(
                data[12:].strip().split(':')[1])) + msg + file_data)
        else:
            lst.insert(END, f">>[CLIENT] file does not exists!")
            lst.see(END)
    else:
        sock.send(struct.pack("I", len(data.encode())) + struct.pack("I", 0) + data.encode())

    return False


def recv_handler(lst):
    """
    this function runs on a thread and handling the receive of messages from the server
    :param lst: tkinter list box
    :return: None
    """
    while connected:
        try:
            msg_size = sock.recv(struct.calcsize("I"))
            if not msg_size:
                break
            try:
                msg_size = struct.unpack("I", msg_size)[0]
            except:  # not a integer
                continue

            file_size = sock.recv(struct.calcsize("I"))
            if not file_size:
                break
            try:
                file_size = struct.unpack("I", file_size)[0]
            except:  # not a integer
                continue

            msg = sock.recv(msg_size).decode()
            if not msg:
                break
            if int(file_size) > 0:
                file = b''
                while len(file) < file_size:
                    fragment = sock.recv(file_size - len(file))
                    if not fragment:
                        break
                    file = file + fragment

                with open(msg, "wb") as f:
                    f.write(file)

                lst.insert(END, f"[CLIENT] {msg} has been saved")
                lst.see(END)
            else:
                lst.insert(END, f"{msg}")
                lst.see(END)
        except:
            break
    if connected:
        print("error")
        server_down()


def main_screen():
    """
    tkinter of main screen
    :return: None
    """
    clear_screen()

    box_frame = Frame(root, bg='white', bd=2)
    box_frame.pack(pady=(0, 15), fill=BOTH, expand=True)

    scrollbar = Scrollbar(box_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    chat_box = Listbox(box_frame, yscrollcommand=scrollbar.set, width=root.winfo_width(), font='roboto 10')
    chat_box.pack(fill=BOTH, expand=True)

    scrollbar.config(command=chat_box.yview)

    send_frame = Frame(root, bg='white')
    send_frame.pack(pady=10)

    send_entry = Entry(send_frame, width=40, bd=2, font=('Ariel', 14), bg='white')
    send_entry.pack(side=LEFT)
    send_entry.bind('<Return>', lambda e: handle_send_data(chat_box, send_entry))

    send_btn = Button(send_frame, width=4, text='send', command=lambda: handle_send_data(chat_box, send_entry),
                      bd=0, font=('Helvetica', 14), bg='#a6a6a6', fg='white',
                      activeforeground='white', activebackground='#a6a6a6')
    send_btn.pack(side=LEFT)

    _thread.start_new_thread(recv_handler, (chat_box,))


# setting up globals
BUFF = 4096
connected = True

root = Tk()
root.geometry('600x300+400+200')
root.minsize(600, 300)
root.update()
root.configure(bg='white')

sock = socket(AF_INET, SOCK_STREAM)
port_server_screen()

root.mainloop()
