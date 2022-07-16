import socket
import pickle
from .client import Client, SERVER_ADDR


class AdminClient(Client):
    def __init__(self):
        """
        setting up the admin interface that communicate with the server over sockets
        """

        super().__init__()
        self.admin_credentials = {}

    def admin_login(self, admin_id, admin_password):
        """
        creates socket connection to the server and logging in and getting user credentials
        :param admin_id: str
        :param admin_password: str
        :return: tuple[bool - logged in or not, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False, False

        self.send_to_sock(sock, "admin_login", {"admin": "yes", "admin_id": admin_id, "admin_password": admin_password})

        msg, dict_data, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False, False

        if msg.split(" ", maxsplit=2)[1] == "ok":
            self.credentials = dict_data
            self.admin_credentials = {"admin_id": admin_id, "admin_password": admin_password}
            return True, True
        return False, True

    def change_time(self, date):
        """
        creates socket connection to the server and sends to the server the new server time
        :param date: str
        :return: bool - error or not
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False

        self.send_to_sock(sock, "change date", {"admin": "yes", "date": date, **self.admin_credentials})

        msg, _, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False

        return True

    def get_all_rooms(self):
        """
        creates socket connection to the server and getting the rooms
        :return: tuple[list, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return [], False

        self.send_to_sock(sock, "get all rooms", {"admin": "yes", **self.admin_credentials})

        msg, _, bytes_data, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return [], False

        try:
            rooms = pickle.loads(bytes_data)
        except:
            return [], False

        return rooms, True

    def get_all_users(self):
        """
        creates socket connection to the server and getting the users
        :return: tuple[list, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return [], False

        self.send_to_sock(sock, "get all users", {"admin": "yes", **self.admin_credentials})

        msg, _, bytes_data, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return [], False

        try:
            rooms = pickle.loads(bytes_data)
        except:
            return [], False

        return rooms, True

    def set_attractions(self, path_to_json):
        """
        creates socket connection to the server and sends an attractions file
        :return: bool - error or not
        """

        with open(path_to_json, "rb") as f:
            data = f.read()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False

        self.send_to_sock(sock, "set attractions", {"admin": "yes", **self.admin_credentials}, data)

        msg, _, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False

        return True
