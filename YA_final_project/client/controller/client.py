import socket
import struct
import pickle
from datetime import datetime

SERVER_IP = "localhost"
SERVER_PORT = 55555
SERVER_ADDR = (SERVER_IP, SERVER_PORT)


class Client:

    def __init__(self):
        """
        setting up the client interface that communicate with the server over sockets
        """

        self.credentials = {}

    def login(self, email, password):
        """
        creates socket connection to the server and logging in and getting user credentials
        :param email: str
        :param password: str
        :return: tuple[bool - logged in or not, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False, False

        self.send_to_sock(sock, "login", {"email": email, "password": password})

        msg, dict_data, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False, False

        if msg.split(" ", maxsplit=2)[1] == "ok":
            self.credentials = dict_data
            return True, True
        return False, True

    def sign_up(self, name, email, password):
        """
        creates socket connection to the server and sending to the sever new user details
        :param name: str
        :param email: str
        :param password: str
        :return: tuple[bool - added or not, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False, False

        self.send_to_sock(sock, "register", {"email": email, "password": password, "name": name})

        msg, _, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False, False

        if msg.split(" ", maxsplit=2)[1] == "ok":
            return True, True
        return False, True

    def get_name(self):
        """
        get name from the user credentials
        :return: str
        """
        return self.credentials.get("name", "user")

    def add_room(self, name, price, description, location, picture_names):
        """
        creates socket connection to the server and sending to the server new room details
        :param name: str
        :param price: float
        :param description: str
        :param location: str
        :param picture_names: list
        :return: tuple[bool - added or not, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False, False

        pictures = []

        for pic_name in picture_names:
            with open(pic_name, "rb") as f:
                pictures.append(f.read())

        room_data = {"room_name": name, "price": price, "location": location, "photos": pictures, "description": description}

        self.send_to_sock(sock, "add room", {**self.credentials}, pickle.dumps(room_data))

        msg, _, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False, False

        if msg.split(" ", maxsplit=2)[1] == "ok":
            return True, True
        return False, True

    def remove_room(self, room_id):
        """
        creates socket connection to the server and sending to the server room id to remove
        :param room_id: int
        :return: tuple[bool - added or not, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False, False

        self.send_to_sock(sock, "delete room", {**self.credentials, "room_id": room_id})

        msg, _, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False, False

        if msg.split(" ", maxsplit=2)[1] == "ok":
            return True, True
        return False, True

    def get_rooms(self, start_date, end_date):
        """
        creates socket connection to the server and getting the rooms by the dates
        :param start_date: str
        :param end_date: str
        :return: tuple[list, bool - error or not]
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return [], False

        self.send_to_sock(sock, "get rooms by dates", {"start_date": start_date, "end_date": end_date})

        msg, _, bytes_data, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return [], False

        try:
            rooms = pickle.loads(bytes_data)
        except:
            return [], False

        return rooms, True

    def get_my_rooms(self):
        """
        creates socket connection to the server and getting the user's rooms
        :return: tuple[list, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return [], False

        self.send_to_sock(sock, "get my rooms", {**self.credentials})

        msg, _, bytes_data, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return [], False

        try:
            rooms = pickle.loads(bytes_data)
        except:
            return [], False

        return rooms, True

    def can_view(self, room_id):
        """
        creates socket connection to the server and checks if a room can be viewed
        :param room_id:
        :return: tuple[bool - can view or not, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return [], False

        self.send_to_sock(sock, "viewing", {"room_id": room_id})

        msg, _, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False, False

        if msg == "no":
            return False, True
        return True, True

    def purchase(self, room_id, start_date, end_date):
        """
        creates socket connection to the server and sending to the server purchase details
        :param room_id: int
        :param start_date: str
        :param end_date: str
        :return: tuple[bool - purchased or not, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False, False

        self.send_to_sock(sock, "purchase", {**self.credentials, "room_id": room_id, "start_date": start_date, "end_date": end_date})

        msg, _, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False, False

        if msg.split(" ", maxsplit=2)[1] == "ok":
            return True, True
        return False, True

    def get_server_time(self):
        """
        creates socket connection to the server and getting the server time
        :return: datetime object
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False

        self.send_to_sock(sock, "time")

        msg, _, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False
        return datetime.strptime(msg, "%d/%m/%Y")

    def get_purchases(self):
        """
        creates socket connection to the server and getting all of the user's purchases
        :return: tuple[list, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return [], False

        self.send_to_sock(sock, "get purchases", {**self.credentials})

        msg, _, bytes_data, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return [], False

        if msg.split(" ", maxsplit=2)[1] == "ok":
            try:
                purchases = pickle.loads(bytes_data)
            except:
                return [], False
            return purchases, True

        return [], True

    def dispute(self, purchase_id):
        """
        creates socket connection to the server and sending to the server details of a purchase to cancel
        :param purchase_id: int
        :return: tuple[bool - canceled or not, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False, False

        self.send_to_sock(sock, "dispute", {**self.credentials, "purchase_id": purchase_id})

        msg, _, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False, False

        if msg.split(" ", maxsplit=2)[1] == "ok":
            return True, True
        return False, True

    def rooms_to_rate(self):
        """
        creates socket connection to the server and gets list of room that need to be rated
        :return: tuple[list, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return [], False

        self.send_to_sock(sock, "get need to rate", {**self.credentials})

        msg, _, bytes_data, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return [], False

        try:
            rooms_to_rate = pickle.loads(bytes_data)
        except:
            return [], False
        return rooms_to_rate, True

    def rate_room(self, purchase_id, rating):
        """
        creates socket connection to the server and sends rating of a room
        :param purchase_id: int
        :param rating: int
        :return: tuple[bool - rated or not, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return False, False

        self.send_to_sock(sock, "rate", {**self.credentials, "purchase_id": purchase_id, "rating": rating})

        msg, _, _, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return False, False

        if msg.split(" ", maxsplit=2)[1] == "ok":
            return True, True
        return False, True

    def get_attractions(self):
        """
        creates socket connection to the server and getting attractions list
        :return: tuple[list, bool - error or not]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(SERVER_ADDR)
        except:
            return [], False

        self.send_to_sock(sock, "attractions", {**self.credentials})

        msg, _, bytes_data, success = self.recv_from_sock(sock)

        sock.close()

        if not success:
            return [], False

        try:
            attractions = pickle.loads(bytes_data)
        except:
            return [], False
        return attractions, True

    def recv_from_sock(self, sock):
        """
        :param sock: socket
        :return: tuple - (msg/error - str, byte-array(like file)/empty byte-array, status(True for ok, False for error))
        """
        try:
            msg_size = sock.recv(struct.calcsize("I"))
        except:
            return "recv error", {}, b'', False
        if not msg_size:
            return "msg length error", {}, b'', False
        try:
            msg_size = struct.unpack("I", msg_size)[0]
        except:  # not an integer
            return "msg length error", {}, b'', False

        try:
            auth_size = sock.recv(struct.calcsize("I"))
        except:
            return "recv error", {}, b'', False
        if not auth_size:
            return "auth length error", {}, b'', False
        try:
            auth_size = struct.unpack("I", auth_size)[0]
        except:  # not an integer
            return "auth length error", {}, b'', False

        try:
            file_size = sock.recv(struct.calcsize("I"))
        except:
            return "recv error", {}, b'', False
        if not file_size:
            return "file length error", {}, b'', False
        try:
            file_size = struct.unpack("I", file_size)[0]
        except:  # not an integer
            return "file length error", {}, b'', False

        msg = b''
        while len(msg) < msg_size:  # this is a fail - safe -> if the recv not giving the msg in one time
            try:
                msg_fragment = sock.recv(msg_size - len(msg))
            except:
                return "recv error", {}, b'', False
            if not msg_fragment:
                return "msg data is none", {}, b'', False
            msg = msg + msg_fragment

        msg = msg.decode(errors="ignore")

        auth = b''
        while len(auth) < auth_size:  # this is a fail - safe -> if the recv not giving the file in one time
            try:
                auth_fragment = sock.recv(auth_size - len(auth))
            except:
                return "recv error", {}, b'', False
            if not auth_fragment:
                return "auth data is none", {}, b'', False
            auth = auth + auth_fragment

        try:
            auth = pickle.loads(auth)
        except:
            auth = {}

        # not file was sent
        if int(file_size) == 0:
            return msg, auth, b'', True

        file = b''
        while len(file) < file_size:  # this is a fail - safe -> if the recv not giving the file in one time
            try:
                file_fragment = sock.recv(file_size - len(file))
            except:
                return "recv error", {}, b'', False
            if not file_fragment:
                return "file data is none", {}, b'', False
            file = file + file_fragment

        return msg, auth, file, True

    def send_to_sock(self, sock, data, auth=None, bytes_data=b''):
        """
        examples -> send_to_sock(client, "are you there?"), send_to_sock(client, "file_name:pic.png", my_file)
        :param sock: socket
        :param data: str
        :param auth: dict
        :param bytes_data: bytes - default param -> b''
        :return: None
        """
        if auth is None:
            auth = {}

        pickled_auth = pickle.dumps(auth)
        sock.send(struct.pack("I", len(data.encode())) + struct.pack("I", len(pickled_auth)) + struct.pack("I",
                                                                                                           len(bytes_data)) + data.encode() + pickled_auth + bytes_data)
