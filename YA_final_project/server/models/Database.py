import sqlite3 as lite


class Database:

    def __init__(self):
        """
        setting up the interface that communicates with the database
        """
        self.dbPath = 'controller/test.db'
        self.con = lite.connect(self.dbPath)

    def query(self, sql):
        """
        function that execute sql query on the database
        :param sql: str - the sql query
        :return: list - list of the rows of the database
        """

        rows = []

        try:

            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            rows = cur.fetchall()

        except lite.Error as e:
            print(f"sql error: {e}")

        return rows

    def create_table_if_not_exists(self, name, params):
        """
        creates table in the database if the table doesn't exists
        :param name: str - table name
        :param params: tuple (or any iterable) - table params
        :return: None
        """
        table_params = ",".join((param for param in params))
        query = f"CREATE TABLE IF NOT EXISTS {name} ({table_params})"

        self.query(query)

    def check_if_exists(self, name, params):
        """
        checking if data exists in the database
        :param name: str - table name
        :param params - data to check if exists
        :return: bool - exists or not
        """

        search_params = " AND ".join((param[0] + "=" + param[1] for param in params))
        query = f"SELECT * FROM {name} WHERE {search_params}"
        rows = self.query(query)

        return len(rows) != 0

    def add_user(self, email, password, name):
        """
        checking if the user can be added to the database and adding it
        :param email: str - user email
        :param password: str - user password
        :param name: str - user name
        :return: bool - added or not
        """

        self.create_table_if_not_exists("users", (
            "user_id INTEGER PRIMARY KEY AUTOINCREMENT", "email TEXT", "password TEXT", "name TEXT"))

        if self.check_if_exists("users", (("email", f"'{email}'"),)):
            return False

        self.query(f"INSERT INTO users(email, password, name) VALUES('{email}', '{password}', '{name}')")
        return True

    def check_user_exists(self, email, password):
        """
        function that checks if user exists in the database
        :param email: str - user email
        :param password: str - user password
        :return: bool - exists or not
        """

        self.create_table_if_not_exists("users", (
            "user_id INTEGER PRIMARY KEY AUTOINCREMENT", "email TEXT", "password TEXT", "name TEXT"))

        return self.check_if_exists("users", (("email", f"'{email}'"), ("password", f"'{password}'")))

    def get_user_by_email(self, email):
        """
        returning user row by email
        :param email: str - user email
        :return: tuple - user row
        """

        return self.query(f"SELECT * FROM users WHERE email='{email}'")[0]

    def get_all_users(self):
        """
        return all users
        :return: list
        """

        return self.query(f"SELECT * FROM users")

    def get_user_total_income(self, user_id):
        """
        getting a user's total income from all of his rooms
        :param user_id: int
        :return: float - user total income
        """

        return self.query(f"SELECT SUM(total_income) FROM rooms WHERE user_id={user_id}")[0][0]

    def get_name_by_id(self, user_id):
        """
        user name by id
        :param user_id: int
        :return: str
        """

        return self.query(f"SELECT name FROM users WHERE user_id={user_id}")[0][0]

    def get_user_id_and_name_by_email(self, email):
        """
        user id and name by their email
        :param email: str - user email
        :return: tuple[user id, user name]
        """

        data = self.query(f"SELECT user_id, name FROM users WHERE email='{email}'")
        if len(data) == 0:
            return -1
        return data[0][0], data[0][1]

    def add_room(self, user_id, room_details):
        """
        adding the room to the database
        :param user_id: int
        :param room_details: dict
        :return: None
        """

        self.create_table_if_not_exists("rooms", ("room_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                                  "user_id INTEGER", "room_name TEXT", "daily_price REAL",
                                                  "location TEXT", "photos TEXT", "total_income REAL",
                                                  "description TEXT", "num_of_rates INTEGER", "total_rate INTEGER"))
        x = f"INSERT INTO rooms(user_id, room_name, daily_price, location, photos, description, total_income, num_of_rates, total_rate) VALUES({user_id}, '{room_details['room_name']}', {room_details['price']}, '{room_details['location']}', '{room_details['photos']}', '{room_details['description']}', 0, 0, 0)"
        self.query(x)

    def get_all_rooms(self):
        """
        gets all the rooms from the database
        :return: list
        """

        self.create_table_if_not_exists("rooms", ("room_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                                  "user_id INTEGER", "room_name TEXT", "daily_price REAL",
                                                  "location TEXT", "photos TEXT", "total_income REAL",
                                                  "description TEXT", "num_of_rates INTEGER", "total_rate INTEGER"))
        return self.query("SELECT * FROM rooms")

    def get_room_by_id(self, room_id):
        """
        gets a room by its id
        :param room_id: int
        :return: tuple - room row
        """

        self.create_table_if_not_exists("rooms", ("room_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                                  "user_id INTEGER", "room_name TEXT", "daily_price REAL",
                                                  "location TEXT", "photos TEXT", "total_income REAL",
                                                  "description TEXT", "num_of_rates INTEGER", "total_rate INTEGER"))
        data = self.query(f"SELECT * FROM rooms WHERE room_id={room_id}")

        return [] if len(data) == 0 else data[0]

    def remove_room_by_id(self, room_id):
        """
        removes a room from the database
        :param room_id: int
        :return: None
        """

        self.query(f"DELETE FROM rooms WHERE room_id={room_id}")

    def get_rooms_by_user_id(self, user_id):
        """
        gets all the rooms from the database that have the given user id
        :param user_id: int
        :return: list
        """

        self.create_table_if_not_exists("rooms", ("room_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                                  "user_id INTEGER", "room_name TEXT", "daily_price REAL",
                                                  "location TEXT", "photos TEXT", "total_income REAL",
                                                  "description TEXT", "num_of_rates INTEGER", "total_rate INTEGER"))
        return self.query(f"SELECT * FROM rooms WHERE user_id={user_id}")

    def decrement_room_income_by_x(self, room_id, x):
        """
        decrementing room's total income by a number
        :param room_id: int
        :param x: int
        :return: None
        """

        self.query(f"UPDATE rooms SET total_income=total_income-{x} WHERE room_id={room_id}")

    def increment_room_income_by_x(self, room_id, x):
        """
        incrementing room's total income by a number
        :param room_id: int
        :param x: int
        :return: None
        """

        self.query(f"UPDATE rooms SET total_income=total_income+{x} WHERE room_id={room_id}")

    def rate_room(self, room_id, x, purchase_id):
        """
        updates room rating in the database
        :param room_id: int
        :param x: int - rate
        :param purchase_id: int
        :return: None
        """

        self.query(f"UPDATE rooms SET num_of_rates=num_of_rates+1,total_rate=total_rate+{x} WHERE room_id={room_id}")

        self.query(f"UPDATE purchases SET rated='yes' WHERE purchase_id={purchase_id}")

    def add_purchase(self, room_id, user_id, dates):
        """
        adding a purchase to the database
        :param room_id: int
        :param user_id: int
        :param dates: str
        :return: None
        """

        self.create_table_if_not_exists("purchases", ("purchase_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                                      "room_id INTEGER", "user_id INTEGER", "dates TEXT", "rated TEXT"))

        self.query(
            f"INSERT INTO purchases(room_id, user_id, dates, rated) VALUES({room_id}, {user_id}, '{dates}', 'no')")

    def get_purchases_by_room(self, room_id):
        """
        gets all the purchases of a given room
        :param room_id: int
        :return: list
        """

        self.create_table_if_not_exists("purchases", ("purchase_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                                      "room_id INTEGER", "user_id INTEGER", "dates TEXT", "rated TEXT"))

        return self.query(f"SELECT * FROM purchases WHERE room_id={room_id}")

    def get_purchases_by_user(self, user_id):
        """
        gets all the purchases of a given user
        :param user_id: int
        :return: list
        """

        self.create_table_if_not_exists("purchases", ("purchase_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                                      "room_id INTEGER", "user_id INTEGER", "dates TEXT", "rated TEXT"))

        return self.query(f"SELECT * FROM purchases WHERE user_id={user_id}")

    def get_all_purchases(self):
        """
        gets all purchases
        :return: list
        """

        self.create_table_if_not_exists("purchases", ("purchase_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                                      "room_id INTEGER", "user_id INTEGER", "dates TEXT", "rated TEXT"))

        return self.query(f"SELECT * FROM purchases")

    def get_purchase_by_id(self, purchase_id):
        """
        gets a purchase by its id
        :param purchase_id: int
        :return: tuple - purchase row
        """

        self.create_table_if_not_exists("purchases", ("purchase_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                                      "room_id INTEGER", "user_id INTEGER", "dates TEXT", "rated TEXT"))

        data = self.query(f"SELECT * FROM purchases WHERE purchase_id={purchase_id}")

        return [] if len(data) == 0 else data[0]

    def remove_purchase_by_id(self, purchase_id):
        """
        removes a purchase from the database
        :param purchase_id: int
        :return: None
        """

        self.query(f"DELETE FROM purchases WHERE purchase_id={purchase_id}")

    def remove_purchases_by_room(self, room_id):
        """
        removes all the purchases of a given room
        :param room_id:
        :return: None
        """

        self.query(f"DELETE FROM purchases WHERE room_id={room_id}")

    def add_admin(self, admin_id, admin_password):
        """
        checks if the admin can be added and adding it
        :param admin_id: str
        :param admin_password: str
        :return: bool - added or not
        """

        self.create_table_if_not_exists("admins", (
            "admin_primary_id INTEGER PRIMARY KEY AUTOINCREMENT", "admin_id TEXT", "admin_password TEXT", "email text"))

        if self.check_if_exists("admins", (("admin_id", f"'{admin_id}'"),)):
            return False

        self.add_user(f"admin_{admin_id}@admins.com", admin_password, admin_id)

        self.query(f"INSERT INTO admins(admin_id, admin_password, email) VALUES('{admin_id}', '{admin_password}', 'admin_{admin_id}@admins.com')")
        return True

    def get_admin_by_id(self, admin_id):
        """
        gets the admin by its id
        :param admin_id: str
        :return: tuple - admin row
        """

        return self.query(f"SELECT * FROM admins WHERE admin_id='{admin_id}'")[0]

    def check_admin_exists(self, admin_id, admin_password):
        """
        check if an admin exists in the database and his password is correct
        :param admin_id: str
        :param admin_password: str
        :return: bool - exists or not
        """

        self.create_table_if_not_exists("admins", (
            "admin_primary_id INTEGER PRIMARY KEY AUTOINCREMENT", "admin_id TEXT", "admin_password TEXT", "email text"))

        self.add_admin("main", "main_admin123")

        return self.check_if_exists("admins", (("admin_id", f"'{admin_id}'"), ("admin_password", f"'{admin_password}'")))
