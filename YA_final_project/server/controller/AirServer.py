import time
import os
import json
from .BaseServer import BaseServer
from datetime import datetime
import pickle


class AirServer(BaseServer):
    def __init__(self, ip, port, database):
        """
        setting up the class of the airbnb server which handle the client requests
        :param ip: str - server ip to bind
        :param port: int - server port to bind
        """
        super().__init__(ip, port)
        self.database = database
        self.server_time = datetime.now()

        if os.path.exists("attractions.json"):
            with open("attractions.json", "r") as f:
                self.attractions = json.load(f)
        else:
            self.attractions = []

        self.views = {}

    def handle_admin_data(self, client, msg: str, dict_data: dict, bytes_data: bytes):
        """
        function that handles requests of admins
        :param client: socket - admin socket object
        :param msg: str - the admin request
        :param dict_data: dict - data for the admin to send
        :param bytes_data: bytes - data that the admin to send
        :return: None
        """

        # handling authentication
        if not ("admin_id" in dict_data and "admin_password" in dict_data):
            self.send_message(client, "admin fail missing data")
            return

        if not self.database.check_admin_exists(dict_data["admin_id"], dict_data["admin_password"]):
            self.send_message(client, "admin fail bad auth")
            return

        # handling the different admin requests

        if msg == "admin_login":
            # sending the admin his user credentials
            admin = self.database.get_admin_by_id(dict_data["admin_id"])
            admin_user = self.database.get_user_by_email(admin[3])
            self.send_message(client, "login ok", {"email": admin_user[1], "password": admin_user[2], "user_id": admin_user[0], "name": admin_user[3]})

        elif msg == "change date":
            # changing the server date

            self.server_time = datetime.strptime(dict_data["date"], "%d/%m/%Y")
            self.send_message(client, "date ok")

        elif msg == "get all users":
            # sending all the users and their info about purchases and rooms to the admin

            db_users = self.database.get_all_users()

            users = []

            for user in db_users:
                user_income = self.database.get_user_total_income(user[0])
                user_purchases = len(self.database.get_purchases_by_user(user[0]))

                users.append({"user_id": user[0], "name": user[3], "email": user[1], "total_income": 0 if user_income is None else round(user_income, 1), "purchases": user_purchases})

            self.send_message(client, "users", bytes_data=pickle.dumps(users))

        elif msg == "get all rooms":
            # sending all the rooms information to the admin

            db_rooms = self.database.get_all_rooms()
            rooms = []

            for db_room in db_rooms:
                pictures = []
                for photo_name in db_room[5].split(","):
                    if photo_name == '':
                        continue
                    with open(f"pictures/{photo_name}", "rb") as f:
                        pictures.append(f.read())
                owner_name = self.database.get_name_by_id(db_room[1])
                rooms.append(
                    {"room_id": db_room[0], "owner_name": owner_name, "room_name": db_room[2], "price": db_room[3],
                     "location": db_room[4],
                     "total_income": db_room[6], "conditions": db_room[7],
                     "rating": 0 if db_room[8] == 0 else round(db_room[9] / db_room[8], 1), "photos": pictures})
            self.send_message(client, "rooms", bytes_data=pickle.dumps(rooms))

        elif msg == "set attractions":
            # setting attractions file that admin sent

            with open("attractions.json", "wb") as f:
                f.write(bytes_data)
            with open("attractions.json", "r") as f:
                self.attractions = json.load(f)

            self.send_message(client, "attractions ok")

    def _handle_data(self, client, msg: str, dict_data: dict, bytes_data: bytes):
        """
        function that handles the requests of the clients
        :param client: socket - socket object of the client
        :param msg: str - the client request
        :param dict_data: dict - data for the client to send
        :param bytes_data: bytes - data that the client to send
        :return: None
        """

        if "admin" in dict_data:
            # checking if the requests is an admin request

            self.handle_admin_data(client, msg, dict_data, bytes_data)
            return

        # handling the different client requests

        if msg == "register":
            # checking if the client can be added to the database and adding the client to the database

            if "email" in dict_data and "password" in dict_data and "name" in dict_data:
                email = dict_data['email']
                password = dict_data['password']
                name = dict_data['name']

                success = self.database.add_user(email, password, name)

                if success:
                    self.send_message(client, "register ok")
                else:
                    self.send_message(client, "register fail email exists")
            else:
                self.send_message(client, "register fail missing data")

        elif msg == "login":
            # checking if the client email and password exists in the database and sending him the credentials

            if "email" in dict_data and "password" in dict_data:
                email = dict_data['email']
                password = dict_data['password']

                exists = self.database.check_user_exists(email, password)

                if exists:
                    user_id, name = self.database.get_user_id_and_name_by_email(email)
                    self.send_message(client, "login ok", {"email": email, "password": password, "user_id": user_id, "name": name})
                else:
                    self.send_message(client, "login fail user doesn't exists")
            else:
                self.send_message(client, "login fail missing data")

        elif msg == "add room":
            # checking user credentials and adding the room to the database and saving the pictures locally

            if "email" in dict_data and "password" in dict_data and "user_id" in dict_data:
                email = dict_data['email']
                password = dict_data['password']
                user_id = dict_data["user_id"]

                exists = self.database.check_user_exists(email, password)

                if exists:
                    all_rooms = self.database.get_all_rooms()
                    room_id = 1 if len(all_rooms) == 0 else all_rooms[-1][0] + 1
                    room_data: dict = pickle.loads(bytes_data)

                    names = [f"{room_id}_{i}.png" for i in range(len(room_data["photos"]))]

                    for i, name in enumerate(names):
                        with open(f"pictures/{name}", "wb") as f:
                            f.write(room_data["photos"][i])

                    room_data["photos"] = ",".join(names)
                    room_data["room_name"] = room_data["room_name"].replace("'", r"''")

                    self.database.add_room(user_id, room_data)

                    self.send_message(client, "room ok")

                else:
                    self.send_message(client, "room fail bad auth")
            else:
                self.send_message(client, "room fail bad auth")

        elif msg == "delete room":
            # checking user credentials and deleting the client's room

            if not ("email" in dict_data and "password" in dict_data and "user_id" in dict_data and "room_id" in dict_data):
                self.send_message(client, "delete_room fail missing data")
                return
            authenticated = self.check_auth(dict_data['email'], dict_data['password'])

            if not authenticated:
                self.send_message(client, "delete_room fail bad auth")
                return

            wanted_deleted_room = self.database.get_room_by_id(dict_data["room_id"])

            if wanted_deleted_room[1] == dict_data["user_id"]:
                self.database.remove_room_by_id(dict_data["room_id"])
                self.database.remove_purchases_by_room(dict_data["room_id"])
                self.send_message(client, "delete_room ok")
            else:
                self.send_message(client, "delete_room fail bad user")

        elif msg == "get rooms":
            # sending all the rooms to the client with the needed data

            db_rooms = self.database.get_all_rooms()
            rooms = []

            for db_room in db_rooms:
                pictures = []
                for photo_name in db_room[5].split(","):
                    if photo_name == '':
                        continue
                    with open(f"pictures/{photo_name}", "rb") as f:
                        pictures.append(f.read())
                rooms.append({"room_id": db_room[0], "room_name": db_room[2], "price": db_room[3], "location": db_room[4], "total_income": db_room[6], "conditions": db_room[7], "rating": 0 if db_room[8] == 0 else round(db_room[9] / db_room[8], 1), "photos": pictures})
            self.send_message(client, "rooms", bytes_data=pickle.dumps(rooms))

        elif msg == "get my rooms":
            # sending the rooms that the user owns to him with the needed data
            if not ("email" in dict_data and "password" in dict_data and "user_id" in dict_data):
                self.send_message(client, "get_purchases fail missing data")
                return
            authenticated = self.check_auth(dict_data['email'], dict_data['password'])

            if not authenticated:
                self.send_message(client, "get_my_rooms fail bad auth")
                return
            db_rooms = self.database.get_rooms_by_user_id(dict_data["user_id"])
            rooms = []

            for db_room in db_rooms:
                pictures = []
                for photo_name in db_room[5].split(","):
                    if photo_name == '':
                        continue
                    with open(f"pictures/{photo_name}", "rb") as f:
                        pictures.append(f.read())
                rooms.append({"room_id": db_room[0], "room_name": db_room[2], "price": db_room[3], "location": db_room[4], "total_income": db_room[6], "conditions": db_room[7], "rating": 0 if db_room[8] == 0 else round(db_room[9] / db_room[8], 1), "photos": pictures})
            self.send_message(client, "rooms", bytes_data=pickle.dumps(rooms))

        elif msg == "get rooms by dates":
            # sending all the available rooms in a given dates to the client with the needed data

            if "start_date" not in dict_data or "end_date" not in dict_data:
                self.send_message(client, "room fail missing data")
                return

            db_rooms = self.database.get_all_rooms()
            rooms = []

            wanted_start_date = datetime.strptime(dict_data["start_date"], "%d/%m/%Y")
            wanted_end_date = datetime.strptime(dict_data["end_date"], "%d/%m/%Y")

            for db_room in db_rooms:
                room_dates = self.get_dates_from_room(db_room[0])

                if any((wanted_start_date <= end_date and start_date <= wanted_end_date for start_date, end_date in room_dates)):
                    continue

                pictures = []
                for photo_name in db_room[5].split(","):
                    if photo_name == '':
                        continue
                    with open(f"pictures/{photo_name}", "rb") as f:
                        pictures.append(f.read())
                rooms.append({"room_id": db_room[0], "room_name": db_room[2], "price": db_room[3], "location": db_room[4], "conditions": db_room[7], "rating": 0 if db_room[8] == 0 else round(db_room[9] / db_room[8], 1), "photos": pictures})
            self.send_message(client, "rooms", bytes_data=pickle.dumps(rooms))

        elif msg == "attractions":
            # sending the attractions to the client

            self.send_message(client, "attractions", bytes_data=pickle.dumps(self.attractions))

        elif msg == "viewing":
            # to check if someone else is viewing the room

            if "room_id" not in dict_data:
                self.send_message(client, "no")
                return

            if dict_data["room_id"] not in self.views:
                self.views[dict_data["room_id"]] = time.time()
                self.send_message(client, "ok")
                return

            if time.time() - self.views[dict_data["room_id"]] > 30:
                self.views[dict_data["room_id"]] = time.time()
                self.send_message(client, "ok")
            else:
                self.send_message(client, "no")

        elif msg == "purchase":
            # checking if the room can be purchased and adding the purchase to the database and incrementing the income of the room

            if "email" in dict_data and "password" in dict_data and "user_id" in dict_data:
                email = dict_data['email']
                password = dict_data['password']

                exists = self.database.check_user_exists(email, password)
                if exists:
                    user_id = dict_data["user_id"]
                else:
                    user_id = -1
            else:
                user_id = -1

            if "room_id" in dict_data and "start_date" in dict_data and "end_date" in dict_data:
                room_dates = self.get_dates_from_room(dict_data["room_id"])

                wanted_start_date = datetime.strptime(dict_data["start_date"], "%d/%m/%Y")
                wanted_end_date = datetime.strptime(dict_data["end_date"], "%d/%m/%Y")

                if any((wanted_start_date <= end_date and start_date <= wanted_end_date for start_date, end_date in room_dates)):
                    self.send_message(client, "purchase fail overlapping dates")
                else:
                    room = self.database.get_room_by_id(dict_data["room_id"])
                    price_per_day = room[3]
                    total_days = wanted_end_date - wanted_start_date
                    total_days = total_days.days
                    total_price = total_days * price_per_day

                    self.database.increment_room_income_by_x(dict_data["room_id"], total_price)
                    self.database.add_purchase(dict_data["room_id"], user_id, f"{dict_data['start_date']}-{dict_data['end_date']}")
                    self.send_message(client, "purchase ok")
            else:
                self.send_message(client, "purchase fail missing data")

        elif msg == "get purchases":
            # validating user credentials and sending the user all of his purchases

            if not ("email" in dict_data and "password" in dict_data and "user_id" in dict_data):
                self.send_message(client, "get_purchases fail missing data")
                return
            authenticated = self.check_auth(dict_data['email'], dict_data['password'])

            if not authenticated:
                self.send_message(client, "get_purchases fail bad auth")
                return

            user_id = dict_data["user_id"]

            db_purchases = self.database.get_purchases_by_user(user_id)

            purchases = []

            for db_purchase in db_purchases:
                purchases.append({"purchase_id": db_purchase[0],
                                  "room_name": self.database.get_room_by_id(db_purchase[1])[2],
                                  # "dates": db_purchase[3],
                                  "start_date": db_purchase[3].split("-")[0],
                                  "end_date": db_purchase[3].split("-")[1],
                                  "can_dispute": self.server_time < datetime.strptime(db_purchase[3].split("-")[0], "%d/%m/%Y")})

            self.send_message(client, "get_purchases ok", bytes_data=pickle.dumps(purchases))

        elif msg == "dispute":
            # checking user and purchase information and canceling the purchase and decrementing the income of the room

            if not ("email" in dict_data and "password" in dict_data and "user_id" in dict_data and "purchase_id" in dict_data):
                self.send_message(client, "dispute fail missing data")
                return
            authenticated = self.check_auth(dict_data['email'], dict_data['password'])

            if not authenticated:
                self.send_message(client, "dispute fail bad auth")
                return

            wanted_purchase = self.database.get_purchase_by_id(dict_data["purchase_id"])

            if len(wanted_purchase) == 0:
                self.send_message(client, "dispute fail bad purchase_id")
                return

            purchase_start_date = datetime.strptime(wanted_purchase[3].split("-")[0], "%d/%m/%Y")
            purchase_end_date = datetime.strptime(wanted_purchase[3].split("-")[1], "%d/%m/%Y")

            if self.server_time >= purchase_start_date:
                self.send_message(client, "dispute fail over date")
                return

            total_days = purchase_end_date - purchase_start_date
            total_days = total_days.days

            room_id = wanted_purchase[1]
            room_price_per_day = self.database.get_room_by_id(room_id)[3]

            total_price = total_days * room_price_per_day

            self.database.remove_purchase_by_id(dict_data["purchase_id"])
            self.database.decrement_room_income_by_x(room_id, total_price)

            self.send_message(client, "dispute ok")

        elif msg == "time":
            # sending the client the server time

            self.send_message(client, f"{self.server_time.strftime('%d/%m/%Y')}")

        elif msg == "get need to rate":
            # sending the user all the rooms that he need to rate after he's been in them

            if not ("email" in dict_data and "password" in dict_data and "user_id" in dict_data):
                self.send_message(client, "get_need_to_rate fail missing data")
                return
            authenticated = self.check_auth(dict_data['email'], dict_data['password'])

            if not authenticated:
                self.send_message(client, "get_need_to_rate fail bad auth")
                return

            rooms_to_rate = []

            user_purchases = self.database.get_purchases_by_user(dict_data["user_id"])

            for purchase in user_purchases:
                purchase_end_date = datetime.strptime(purchase[3].split("-")[1], "%d/%m/%Y")
                if self.server_time > purchase_end_date and purchase[4] == "no":
                    room = self.database.get_room_by_id(purchase[1])
                    rooms_to_rate.append({"purchase_id": purchase[0], "room_name": room[2]})

            self.send_message(client, "get_need_to_rate ok", bytes_data=pickle.dumps(rooms_to_rate))

        elif msg == "rate":
            # saving the room rating to the database

            if not ("email" in dict_data and "password" in dict_data and "user_id" in dict_data and "purchase_id" in dict_data and "rating" in dict_data):
                self.send_message(client, "get_purchases fail missing data")
                return
            authenticated = self.check_auth(dict_data['email'], dict_data['password'])

            if not authenticated:
                self.send_message(client, "get_my_rooms fail bad auth")
                return

            purchase = self.database.get_purchase_by_id(dict_data["purchase_id"])

            purchase_end_date = datetime.strptime(purchase[3].split("-")[1], "%d/%m/%Y")
            if self.server_time > purchase_end_date and purchase[4] == "no":
                self.database.rate_room(purchase[1], dict_data["rating"], purchase[0])
                self.send_message(client, "rate ok")
            else:
                self.send_message(client, "rate fail")

    def check_auth(self, email, password):
        """
        function that checks with the database model if the user exists
        :param email: str - user email
        :param password: str - user password
        :return: bool - user exists or not
        """
        exists = self.database.check_user_exists(email, password)

        return exists

    def get_dates_from_room(self, room_id):
        """
        function that returns all the dates that the room is not available in
        :param room_id:
        :return: list[tuple[datetime-object, datetime-object]]
        """
        dates = []
        purchases = self.database.get_purchases_by_room(room_id)

        for purchase in purchases:
            start_str_date, end_str_date = purchase[3].split("-")
            dates.append((datetime.strptime(start_str_date, "%d/%m/%Y"), datetime.strptime(end_str_date, "%d/%m/%Y")))
        return dates
