import datetime
import tkinter
import customtkinter
import re
import tkinter.messagebox as messagebox
import io
import geocoder
import math
from tkintermapview import TkinterMapView
from tkinter import filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from itertools import cycle

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

email_re = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')
EARTH_RADIUS = 6.38e6


class App(customtkinter.CTk):
    APP_NAME = "Idan's AirBnB"
    WIDTH = 1000
    HEIGHT = 600

    def __init__(self, client, *args, **kwargs):
        """
        setting up client graphical user interface
        :param args: customtkinter CTk args
        :param kwargs: customtkinter CTk kwargs
        """

        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.client = client

        self.logged_in = False

        self.pictures = tuple()

        self.home()

    def check_for_rating_after(func):
        """
        decorator to check if rating is needed after every function
        :return: decorated function
        """

        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.check_for_rating()

        return inner

    @check_for_rating_after
    def home(self):
        """
        screen with customtkinter for home screen
        :return: None
        """

        main_frame = self.layout()

        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        image = Image.open("client_images/Logo.png").resize((200, 200))
        image = ImageTk.PhotoImage(image)

        label_logo = tkinter.Label(master=main_frame, image=image)
        label_logo.image = image
        label_logo.grid(column=0, row=0)

        if self.logged_in:
            label_home = customtkinter.CTkLabel(master=main_frame,
                                                text=f"Welcome to IdanB\nplease offer or buy a room",
                                                fg_color=("white", "gray40"),
                                                height=100,
                                                text_font=("Arial", -22),
                                                justify=tkinter.CENTER)
        else:
            label_home = customtkinter.CTkLabel(master=main_frame,
                                                text=f"Welcome to IdanB\nplease login or sign up to view and by the rooms",
                                                fg_color=("white", "gray40"),
                                                height=100,
                                                text_font=("Arial", -22),
                                                justify=tkinter.CENTER)
        label_home.grid(column=0, row=1, sticky="nwe", padx=15, pady=15)

    @check_for_rating_after
    def login(self):
        """
        screen with customtkinter for login screen
        :return: None
        """

        main_frame = self.layout()

        main_frame.rowconfigure((0, 2, 4), weight=1)
        main_frame.rowconfigure(1, weight=0)
        main_frame.columnconfigure(0, weight=1)

        label_login = customtkinter.CTkLabel(master=main_frame,
                                             text=f"Log in to your account",
                                             fg_color=("white", "gray40"),
                                             height=100,
                                             text_font=("Arial", -22),
                                             justify=tkinter.CENTER)
        label_login.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        label_errors = customtkinter.CTkLabel(master=main_frame,
                                              text=f"",
                                              fg_color="gray10",
                                              text_font=("Arial", -22),
                                              justify=tkinter.CENTER)
        label_errors.grid(column=0, row=2, sticky="nwe", padx=15)
        label_errors.grid_forget()

        form_frame = customtkinter.CTkFrame(master=main_frame, width=500)
        form_frame.grid(column=0, row=4, sticky=tkinter.NSEW, padx=100, pady=15)

        email_entry = customtkinter.CTkEntry(master=form_frame, corner_radius=20, width=200, height=35,
                                             placeholder_text="email")
        email_entry.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        password_entry = customtkinter.CTkEntry(master=form_frame, corner_radius=20, width=200, height=35,
                                                placeholder_text="password")
        password_entry.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        login_btn = customtkinter.CTkButton(master=form_frame, text="Login", text_font=("Arial", -18),
                                            corner_radius=6,
                                            command=lambda: self.handle_login(email_entry.get(), password_entry.get(),
                                                                              label_errors),
                                            width=200)
        login_btn.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    def handle_login(self, email: str, password: str, errors_label):
        """
        validating user input and sending it to the sever with the client network interface
        :param email: str
        :param password: str
        :return: None
        """

        if email == "" or email.isspace():
            # messagebox.showerror("Login", "please fill the email field")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="please fill the email field")
            return
        if not email_re.fullmatch(email):
            # messagebox.showerror("Login", "please enter a valid email address")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="please enter a valid email address")
            return
        if password == "" or password.isspace():
            # messagebox.showerror("Login", "please fill the password field")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="please fill the password field")
            return
        if len(password) < 6:
            # messagebox.showerror("Login", "password must be at least 6 characters")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="password must be at least 6 characters")
            return

        login_ok, success = self.client.login(email, password)

        if not success:
            messagebox.showerror("Login", "Error has accord while communicating with the server")
            return

        if login_ok:
            # messagebox.showinfo("Login", "You have successfully logged in!")
            self.logged_in = True
            self.home()
        else:
            # messagebox.showerror("Login", "Email or password are wrong")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="Email or password are wrong")

    @check_for_rating_after
    def sign_up(self):
        """
        screen with customtkinter for sign up screen
        :return: None
        """

        main_frame = self.layout()

        main_frame.rowconfigure((0, 2, 4), weight=1)
        main_frame.rowconfigure(1, weight=0)
        main_frame.columnconfigure(0, weight=1)

        label_sign_up = customtkinter.CTkLabel(master=main_frame,
                                               text=f"Enter your details to create an account",
                                               fg_color=("white", "gray40"),
                                               height=100,
                                               text_font=("Arial", -22),
                                               justify=tkinter.CENTER)
        label_sign_up.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        label_errors = customtkinter.CTkLabel(master=main_frame,
                                              text=f"",
                                              fg_color="gray10",
                                              text_font=("Arial", -22),
                                              justify=tkinter.CENTER)
        label_errors.grid(column=0, row=2, sticky="nwe", padx=15)
        label_errors.grid_forget()

        form_frame = customtkinter.CTkFrame(master=main_frame, width=500)
        form_frame.grid(column=0, row=4, sticky=tkinter.NSEW, padx=100, pady=15)

        name_entry = customtkinter.CTkEntry(master=form_frame, corner_radius=20, width=200, height=35,
                                            placeholder_text="name")
        name_entry.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        email_entry = customtkinter.CTkEntry(master=form_frame, corner_radius=20, width=200, height=35,
                                             placeholder_text="email")
        email_entry.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        password_entry = customtkinter.CTkEntry(master=form_frame, corner_radius=20, width=200, height=35,
                                                placeholder_text="password")
        password_entry.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

        sign_up_btn = customtkinter.CTkButton(master=form_frame, text="Sign Up", text_font=("Arial", -18),
                                              corner_radius=6,
                                              command=lambda: self.handle_sign_up(name_entry.get(),
                                                                                  email_entry.get(),
                                                                                  password_entry.get(), label_errors),
                                              width=200)
        sign_up_btn.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    def handle_sign_up(self, name: str, email: str, password: str, errors_label):
        """
        validating user input and sending it to the sever with the client network interface
        :param name: str
        :param email: str
        :param password: str
        :return: None
        """

        if name == "" or name.isspace():
            # messagebox.showerror("Sign Up", "please fill the name field")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="please fill the name field")
            return
        if email == "" or email.isspace():
            # messagebox.showerror("Sign Up", "please fill the email field")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="please fill the email field")
            return
        if not email_re.fullmatch(email):
            # messagebox.showerror("Sign Up", "please enter a valid email address")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="please enter a valid email address")
            return
        if password == "" or password.isspace():
            # messagebox.showerror("Sign Up", "please fill the password field")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="please fill the password field")
            return
        if len(password) < 6:
            # messagebox.showerror("Sign Up", "password must be at least 6 characters")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="password must be at least 6 characters")
            return

        sign_up_ok, success = self.client.sign_up(name, email, password)

        if not success:
            messagebox.showerror("Sign Up", "Error has accord while communicating with the server")
            return

        if sign_up_ok:
            # messagebox.showinfo("Sign Up", "You have successfully signed up!\nnow, login")
            self.login()
        else:
            # messagebox.showerror("Sign Up", "Email already exists in server!")
            errors_label.grid(column=0, row=2, sticky="nwe", padx=15)
            errors_label.configure(text="Email already exists in server!")

    @check_for_rating_after
    def search_offers(self):
        """
        screen with customtkinter for searching offers by dates
        :return: None
        """

        server_time = self.client.get_server_time()

        if not server_time:
            messagebox.showerror("Sign Up", "Error has accord while communicating with the server")
            return

        main_frame = self.layout()

        main_frame.rowconfigure((0, 2, 3, 4, 5), weight=2)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        label_offer = customtkinter.CTkLabel(master=main_frame,
                                             text=f"Please enter the dates in which\nyou would like to purchase a room",
                                             fg_color=("white", "gray40"),
                                             height=100,
                                             text_font=("Arial", -22),
                                             justify=tkinter.CENTER)
        label_offer.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        label_errors = customtkinter.CTkLabel(master=main_frame,
                                              text=f"",
                                              fg_color=("white", "gray10"),
                                              text_font=("Arial", -22),
                                              justify=tkinter.CENTER)
        label_errors.grid(column=0, row=1, sticky="nwe", padx=15, pady=15)
        label_errors.grid_forget()

        distance_location_entry = customtkinter.CTkEntry(master=main_frame, corner_radius=20, width=300, height=35,
                                                         placeholder_text="distance from location...")
        distance_location_entry.grid(column=0, row=2)

        from_frame = customtkinter.CTkFrame(master=main_frame)
        from_frame.grid(column=0, row=3, padx=100, pady=15, sticky="n")

        from_label = customtkinter.CTkLabel(master=from_frame,
                                            text=f"From",
                                            fg_color=("white", "gray40"),
                                            text_font=("Arial", -14),
                                            justify=tkinter.CENTER)
        from_label.grid(column=0, row=0, padx=15, pady=15)

        from_entry = DateEntry(master=from_frame, date_pattern="d/m/yyyy", mindate=server_time,
                               font=("Arial", 12))
        from_entry.grid(column=1, row=0, padx=15, pady=15)

        to_frame = customtkinter.CTkFrame(master=main_frame)
        to_frame.grid(column=0, row=4, padx=100, pady=15, sticky="n")

        to_label = customtkinter.CTkLabel(master=to_frame,
                                          text=f"To",
                                          fg_color=("white", "gray40"),
                                          text_font=("Arial", -14),
                                          justify=tkinter.CENTER)
        to_label.grid(column=0, row=0, padx=15, pady=15)

        to_entry = DateEntry(master=to_frame, date_pattern="d/m/yyyy",
                             mindate=server_time + datetime.timedelta(days=1),
                             font=("Arial", 12))
        to_entry.grid(column=1, row=0, padx=15, pady=15)

        search_btn = customtkinter.CTkButton(master=main_frame, text="Search rooms", text_font=("Arial", -20),
                                             corner_radius=6,
                                             command=lambda: self.handle_search_rooms(from_entry.get(), to_entry.get(),
                                                                                      distance_location_entry.get(),
                                                                                      label_errors),
                                             width=200)
        search_btn.grid(column=0, row=5, padx=15, pady=15)

    def handle_search_rooms(self, from_date, to_date, base_location, errors_label):
        """
        gets the room within the given dates with the client network interface
        :param base_location: str
        :param from_date: str
        :param to_date: str
        :return: None
        """

        if base_location == "" or base_location.isspace():
            # messagebox.showerror("Search rooms", "Please fill the distance field")
            errors_label.grid(column=0, row=1, sticky="nwe", padx=15)
            errors_label.configure(text="Please fill the distance field")
            return

        location = geocoder.osm(base_location).latlng

        if location is None:
            # messagebox.showerror("Search rooms", "Please enter a valid address in the distance field")
            errors_label.grid(column=0, row=1, sticky="nwe", padx=15)
            errors_label.configure(text="Please enter a valid address in the distance field")
            return

        base_loc_lat, base_loc_lon = location

        base_lat = base_loc_lat * math.pi / 180

        rooms, success = self.client.get_rooms(from_date, to_date)

        if not success:
            messagebox.showerror("Search rooms", "Error has accord while communicating with the server")
            return

        if len(rooms) == 0:
            # messagebox.showerror("Search rooms", "No rooms has been found in these dates")
            errors_label.grid(column=0, row=1, sticky="nwe", padx=15)
            errors_label.configure(text="No rooms has been found in these dates")
            return

        for room in rooms:
            room_loc_lat, room_loc_lon = float(room["location"].split(",")[0]), float(room["location"].split(",")[1])
            room_lat = room_loc_lat * math.pi / 180

            delta_lat = (base_loc_lat - room_loc_lat) * math.pi / 180
            delta_lon = (base_loc_lon - room_loc_lon) * math.pi / 180

            a = (math.sin(delta_lat / 2) ** 2) + (
                    math.cos(room_lat) * math.cos(base_lat) * (math.sin(delta_lon / 2) ** 2))
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

            d = c * EARTH_RADIUS

            room["distance"] = d

        self.show_offers(rooms, from_date, to_date, base_loc_lat, base_loc_lon)

    @check_for_rating_after
    def show_offers(self, rooms, start_date, end_date, base_x, base_y, buy=True):
        """
        screen to show all rooms in a list as well as a map and activating events of pressing rooms in the map
        :param rooms: list
        :param start_date: str
        :param end_date: str
        :param base_x: float
        :param base_y: float
        :param buy: bool - if buying or viewing the rooms
        :return: None
        """

        # sorting the rooms firstly by price
        rooms = list(sorted(rooms, key=lambda x: x['price']))

        # tkinter design
        self.grid_columnconfigure(0, weight=0)

        main_frame = self.layout()
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        map_widget = TkinterMapView(main_frame, corner_radius=9)
        map_widget.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        map_widget.set_address("israel")

        right_frame = customtkinter.CTkFrame(master=self,
                                             width=200)
        right_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        rooms_list = tkinter.Listbox(right_frame)

        # sorting and focusing events
        rooms_list.bind("<<ListboxSelect>>", lambda event: self.focus_map(event, rooms, map_widget))

        customtkinter.CTkButton(master=right_frame,
                                text="Sort by price",
                                command=lambda: self.sort_list(rooms, rooms_list, 'price'),
                                # width=180, height=50,
                                border_width=0,
                                corner_radius=8).pack(padx=8, pady=10)

        customtkinter.CTkButton(master=right_frame,
                                text="Sort by distance",
                                command=lambda: self.sort_list(rooms, rooms_list, 'distance'),
                                # width=180, height=50,
                                border_width=0,
                                corner_radius=8).pack(padx=8, pady=10)

        customtkinter.CTkButton(master=right_frame,
                                text="Sort by rating",
                                command=lambda: self.sort_list(rooms, rooms_list, 'rating'),
                                # width=180, height=50,
                                border_width=0,
                                corner_radius=8).pack(padx=8, pady=10)

        rooms_list.pack(padx=20, pady=10, expand=True, fill=tkinter.BOTH)

        if buy:
            # base location marker
            map_widget.set_marker(base_x, base_y, text="",
                                  marker_color_circle="aquamarine4", marker_color_outside="aquamarine2")

        # adding the rooms to the list and adding the markers with events to the map
        for room in rooms:
            rooms_list.insert(tkinter.END, room["room_name"])
            map_widget.set_marker(float(room["location"].split(",")[0]), float(room["location"].split(",")[1]),
                                  text=room["room_name"],
                                  command=lambda marker, working_room=room: self.show_room(working_room, start_date,
                                                                                           end_date, buy))

        # getting the attractions and showing them on the map
        attractions, success = self.client.get_attractions()

        for attraction in attractions:
            map_widget.set_marker(float(attraction["location"].split(",")[0]),
                                  float(attraction["location"].split(",")[1]),
                                  text=attraction["name"], marker_color_circle="black", marker_color_outside="gray40")

    def focus_map(self, event, rooms, map_widget):
        """
        focusing the map widget to a specific
        :param event: tkinter list box event
        :param rooms: list
        :param map_widget: TkinterMapView
        :return: None
        """

        selection = event.widget.curselection()

        if not selection:
            return

        index = selection[0]

        loc_x, loc_y = rooms[index]["location"].split(",")

        map_widget.set_position(float(loc_x), float(loc_y))

    def sort_list(self, rooms, list_box, sort_key):
        """
        sorts the rooms' list by a key
        :param rooms: list
        :param list_box: tkinter.listBox
        :param sort_key: str
        :return: None
        """

        rooms.sort(key=lambda x: x[sort_key], reverse=True if sort_key == "rating" else False)

        list_box.delete(0, tkinter.END)

        for room in rooms:
            list_box.insert(tkinter.END, room["room_name"])

    def show_room_in_map(self, room):
        """
        shows a room in a map
        :param room: dict
        :return: None
        """

        # tkinter design
        self.grid_columnconfigure(0, weight=0)

        main_frame = self.layout()
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        map_widget = TkinterMapView(main_frame, corner_radius=9)
        map_widget.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        map_widget.set_position(float(room["location"].split(",")[0]), float(room["location"].split(",")[1]))

        # adding the marker with event to the map
        map_widget.set_marker(float(room["location"].split(",")[0]), float(room["location"].split(",")[1]),
                              text=room["room_name"],
                              command=lambda marker, x=room: self.show_room(x, "", "", False))

        # getting the attractions and showing them on the map
        attractions, success = self.client.get_attractions()

        for attraction in attractions:
            map_widget.set_marker(float(attraction["location"].split(",")[0]),
                                  float(attraction["location"].split(",")[1]),
                                  text=attraction["name"], marker_color_circle="black", marker_color_outside="gray40")

    def show_room(self, room, start_date, end_date, buy=True):
        """
        top level window to show a room (and buy it)
        :param room: dict
        :param start_date: str
        :param end_date: str
        :param buy: bool
        :return: None
        """

        if buy:
            can_view, success = self.client.can_view(room["room_id"])

            if not success:
                messagebox.showerror("Room", "Error has accord while communicating with the server")
                return

            if not can_view:
                messagebox.showerror("Room", "Someone else is currently viewing the room")
                return

        surface = customtkinter.CTkToplevel()
        surface.geometry("500x700+40+100")
        surface.minsize(1000, 700)
        surface.title(f"purchase - {room['room_name']}")

        surface.grid_columnconfigure(0, weight=1)
        surface.grid_columnconfigure(1, weight=1, minsize=500)
        surface.grid_rowconfigure(0, weight=1)

        picture_frame = customtkinter.CTkFrame(master=surface)
        picture_frame.grid(column=0, row=0, sticky=tkinter.NSEW, padx=15, pady=15)

        picture_frame.grid_columnconfigure(0, weight=1)
        picture_frame.grid_rowconfigure((0, 2, 4), weight=3)
        picture_frame.grid_rowconfigure((1, 3), weight=1)

        label_logo = tkinter.Label(master=picture_frame, width=450, height=450)
        label_logo.grid(column=0, row=1)

        btn_next = customtkinter.CTkButton(master=picture_frame, text="Next picture", text_font=("Arial", -20),
                                           corner_radius=6,
                                           width=200)
        btn_next.grid(column=0, row=3)

        if len(room["photos"]) == 0:
            image = Image.open("client_images/Logo.png").resize((400, 400))
            image = ImageTk.PhotoImage(image)
            label_logo.configure(image=image)
            btn_next.configure(state=tkinter.DISABLED)
        else:
            rooms_iter = cycle(
                [ImageTk.PhotoImage(Image.open(io.BytesIO(photo_bytes)).resize((450, 450))) for photo_bytes in
                 room["photos"]])
            label_logo.configure(image=next(rooms_iter))
            btn_next.configure(command=lambda: label_logo.configure(image=next(rooms_iter)))

        right_form = customtkinter.CTkFrame(master=surface)
        right_form.grid(column=1, row=0, sticky=tkinter.NSEW, padx=15, pady=15)

        right_form.grid_columnconfigure(0, weight=1)
        right_form.grid_rowconfigure((1, 4, 7, 10), weight=2)
        right_form.grid_rowconfigure((0, 2, 3, 5, 6, 8, 9, 11), weight=1)

        label_name = customtkinter.CTkLabel(master=right_form,
                                            text=f"{room['room_name']}",
                                            fg_color=("white", "gray40"),
                                            text_font=("Arial", -26),
                                            justify=tkinter.CENTER,
                                            pady=30)
        label_name.grid(column=0, row=0, padx=15, sticky=tkinter.EW)
        if buy:
            label_price_h = customtkinter.CTkLabel(master=right_form,
                                                   text=f"Total price",
                                                   fg_color=("white", "gray40"),
                                                   text_font=("Arial", -22),
                                                   justify=tkinter.CENTER,
                                                   pady=15)
            label_price_h.grid(column=0, row=2, padx=15, sticky=tkinter.EW)

            wanted_start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y")
            wanted_end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y")
            total_days = wanted_end_date - wanted_start_date
            total_days = total_days.days

            label_price = customtkinter.CTkLabel(master=right_form,
                                                 text=f"{round(room['price'] * total_days, 1)}",
                                                 fg_color=("white", "gray40"),
                                                 text_font=("Arial", -18),
                                                 justify=tkinter.CENTER,
                                                 pady=8)
            label_price.grid(column=0, row=3, padx=15, sticky=tkinter.EW)

        else:
            label_price_h = customtkinter.CTkLabel(master=right_form,
                                                   text=f"Daily price",
                                                   fg_color=("white", "gray40"),
                                                   text_font=("Arial", -22),
                                                   justify=tkinter.CENTER,
                                                   pady=15)
            label_price_h.grid(column=0, row=2, padx=15, sticky=tkinter.EW)

            label_price = customtkinter.CTkLabel(master=right_form,
                                                 text=f"{round(room['price'], 2)}",
                                                 fg_color=("white", "gray40"),
                                                 text_font=("Arial", -18),
                                                 justify=tkinter.CENTER,
                                                 pady=8)
            label_price.grid(column=0, row=3, padx=15, sticky=tkinter.EW)

        label_rating_h = customtkinter.CTkLabel(master=right_form,
                                                text=f"Rating",
                                                fg_color=("white", "gray40"),
                                                text_font=("Arial", -22),
                                                justify=tkinter.CENTER,
                                                pady=15)
        label_rating_h.grid(column=0, row=5, padx=15, sticky=tkinter.EW)

        label_rating = customtkinter.CTkLabel(master=right_form,
                                              text=f"{room['rating']}",
                                              fg_color=("white", "gray40"),
                                              text_font=("Arial", -18),
                                              justify=tkinter.CENTER,
                                              pady=8)
        label_rating.grid(column=0, row=6, padx=15, sticky=tkinter.EW)

        label_conditions_h = customtkinter.CTkLabel(master=right_form,
                                                    text=f"Conditions",
                                                    fg_color=("white", "gray40"),
                                                    text_font=("Arial", -22),
                                                    justify=tkinter.CENTER,
                                                    pady=15)
        label_conditions_h.grid(column=0, row=8, padx=15, sticky=tkinter.EW)

        span = 5
        words = room['conditions'].split(" ")
        display_conditions = "\n".join([" ".join(words[i:i + span]) for i in range(0, len(words), span)])

        label_conditions = customtkinter.CTkLabel(master=right_form,
                                                  text=f"{display_conditions}",
                                                  fg_color=("white", "gray40"),
                                                  text_font=("Arial", -18),
                                                  justify=tkinter.CENTER,
                                                  pady=8)
        label_conditions.grid(column=0, row=9, padx=15, sticky=tkinter.EW)

        if buy:
            buy_btn = customtkinter.CTkButton(master=right_form, text="Buy", text_font=("Arial", -20),
                                              corner_radius=6,
                                              command=lambda: self.handle_buy(surface, room["room_id"], start_date,
                                                                              end_date),
                                              width=200)
            buy_btn.grid(column=0, row=11, padx=15, sticky=tkinter.EW)

        surface.mainloop()

    def handle_buy(self, surface, room_id, start_date, end_date):
        """
        sending to server purchase info with the client network interface
        :param surface: top level window
        :param room_id: int
        :param start_date: str
        :param end_date: str
        :return: None
        """

        purchase_ok, success = self.client.purchase(room_id, start_date, end_date)

        if not success:
            messagebox.showerror("purchase", "Error has accord while communicating with the server")
            return

        if purchase_ok:
            messagebox.showinfo("purchase", "you have purchased the room.\nyou can view the purchase in my purchases")
            surface.destroy()
        else:
            messagebox.showerror("purchase", "Client side error has accord while purchasing the room")

    @check_for_rating_after
    def show_my_purchases(self):
        """
        screen that gets from the server all of the users purchases with the client network interface and shows them
        :return: None
        """

        purchases, success = self.client.get_purchases()

        if not success:
            messagebox.showerror("purchases", "Error has accord while communicating with the server")
            return

        main_frame = self.layout()

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        table_frame = customtkinter.CTkFrame(master=main_frame)
        table_frame.grid(column=0, row=0)

        label_name = customtkinter.CTkLabel(master=table_frame,
                                            text=f"room name",
                                            fg_color=("white", "gray60"),
                                            text_font=("Arial", -18, "bold"),
                                            justify=tkinter.CENTER,
                                            pady=4, padx=4)
        label_name.grid(column=0, row=0, padx=4, pady=4)
        label_start_date = customtkinter.CTkLabel(master=table_frame,
                                                  text=f"start date",
                                                  fg_color=("white", "gray60"),
                                                  text_font=("Arial", -18, "bold"),
                                                  justify=tkinter.CENTER,
                                                  pady=4, padx=4)
        label_start_date.grid(column=1, row=0, padx=4, pady=4)
        label_end_date = customtkinter.CTkLabel(master=table_frame,
                                                text=f"end date",
                                                fg_color=("white", "gray60"),
                                                text_font=("Arial", -18, "bold"),
                                                justify=tkinter.CENTER,
                                                pady=4, padx=4)
        label_end_date.grid(column=2, row=0, padx=4, pady=4)
        label_dispute = customtkinter.CTkLabel(master=table_frame,
                                               text=f"dispute",
                                               fg_color=("white", "gray60"),
                                               text_font=("Arial", -18, "bold"),
                                               justify=tkinter.CENTER,
                                               pady=4, padx=4)
        label_dispute.grid(column=3, row=0, padx=4, pady=4)

        purchases.sort(key=lambda date: datetime.datetime.strptime(date['start_date'], "%d/%m/%Y"))

        for row, purchase in enumerate(purchases):
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{purchase['room_name']}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=0, row=row + 1, padx=4, pady=4)
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{purchase['start_date']}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=1, row=row + 1, padx=4, pady=4)
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{purchase['end_date']}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=2, row=row + 1, padx=4, pady=4)
            customtkinter.CTkButton(master=table_frame,
                                    text="Dispute",
                                    text_font=("Arial", -18),
                                    corner_radius=8,
                                    border_width=0,
                                    state=tkinter.NORMAL if purchase["can_dispute"] else tkinter.DISABLED,
                                    command=lambda x=purchase["purchase_id"]: self.handle_dispute(x)).grid(column=3,
                                                                                                           row=row + 1,
                                                                                                           padx=4,
                                                                                                           pady=4)

    def handle_dispute(self, purchase_id):
        """
        sending to the server the details of the purchase to cancel with the client network interface
        :param purchase_id: int
        :return: None
        """

        dispute_ok, success = self.client.dispute(purchase_id)

        if not success:
            messagebox.showerror("dispute", "Error has accord while communicating with the server")
            return

        if dispute_ok:
            # messagebox.showinfo("dispute", "The purchase has been disputed")
            self.show_my_purchases()
        else:
            messagebox.showerror("dispute", "Client side error has accord while disputing")

    @check_for_rating_after
    def show_my_offers(self):
        """
        screen that gets from the server all of the users rooms with the client network interface and shows them
        :return: None
        """

        my_rooms, success = self.client.get_my_rooms()

        if not success:
            messagebox.showerror("my_offers", "Error has accord while communicating with the server")
            return

        main_frame = self.layout()

        for room in my_rooms:
            room["distance"] = 0

        customtkinter.CTkButton(master=main_frame,
                                text="all of my rooms in map",
                                text_font=("Arial", -18),
                                corner_radius=8,
                                border_width=0,
                                command=lambda: self.show_offers(my_rooms, "", "", "", "", False)).place(relx=0.5,
                                                                                                         rely=0.05,
                                                                                                         anchor=tkinter.CENTER)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        table_frame = customtkinter.CTkFrame(master=main_frame)
        table_frame.grid(column=0, row=0)

        label_name = customtkinter.CTkLabel(master=table_frame,
                                            text=f"room name",
                                            fg_color=("white", "gray60"),
                                            text_font=("Arial", -18, "bold"),
                                            justify=tkinter.CENTER,
                                            pady=4, padx=4)
        label_name.grid(column=0, row=0, padx=4, pady=4)
        label_start_date = customtkinter.CTkLabel(master=table_frame,
                                                  text=f"total income",
                                                  fg_color=("white", "gray60"),
                                                  text_font=("Arial", -18, "bold"),
                                                  justify=tkinter.CENTER,
                                                  pady=4, padx=4)
        label_start_date.grid(column=1, row=0, padx=4, pady=4)
        label_end_date = customtkinter.CTkLabel(master=table_frame,
                                                text=f"in map",
                                                fg_color=("white", "gray60"),
                                                text_font=("Arial", -18, "bold"),
                                                justify=tkinter.CENTER,
                                                pady=4, padx=4)
        label_end_date.grid(column=2, row=0, padx=4, pady=4)
        label_dispute = customtkinter.CTkLabel(master=table_frame,
                                               text=f"view",
                                               fg_color=("white", "gray60"),
                                               text_font=("Arial", -18, "bold"),
                                               justify=tkinter.CENTER,
                                               pady=4, padx=4)
        label_dispute.grid(column=3, row=0, padx=4, pady=4)
        label_remove = customtkinter.CTkLabel(master=table_frame,
                                              text=f"remove",
                                              fg_color=("white", "gray60"),
                                              text_font=("Arial", -18, "bold"),
                                              justify=tkinter.CENTER,
                                              pady=4, padx=4)
        label_remove.grid(column=4, row=0, padx=4, pady=4)

        my_rooms.sort(key=lambda offer: offer["room_id"])

        for row, room in enumerate(my_rooms):
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{room['room_name']}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=0, row=row + 1, padx=4, pady=4)
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{round(room['total_income'], 1)}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=1, row=row + 1, padx=4, pady=4)

            customtkinter.CTkButton(master=table_frame,
                                    text="map",
                                    text_font=("Arial", -18),
                                    corner_radius=8,
                                    border_width=0,
                                    command=lambda x=room: self.show_room_in_map(x)).grid(column=2,
                                                                                          row=row + 1,
                                                                                          padx=4,
                                                                                          pady=4)

            customtkinter.CTkButton(master=table_frame,
                                    text="view",
                                    text_font=("Arial", -18),
                                    corner_radius=8,
                                    border_width=0,
                                    command=lambda x=room: self.show_room(x, "", "", False)).grid(column=3,
                                                                                                  row=row + 1,
                                                                                                  padx=4,
                                                                                                  pady=4)

            customtkinter.CTkButton(master=table_frame,
                                    text="remove",
                                    text_font=("Arial", -18),
                                    fg_color=("white", "red2"),
                                    hover_color="red4",
                                    corner_radius=8,
                                    border_width=0,
                                    command=lambda x=room["room_id"]: self.handle_remove_my_room(x)).grid(column=4,
                                                                                                          row=row + 1,
                                                                                                          padx=4,
                                                                                                          pady=4)

    def handle_remove_my_room(self, room_id):
        """
        sends to the server room id of the room with the client network interface
        :param room_id:
        :return:
        """

        remove_room_ok, success = self.client.remove_room(room_id)

        if not success:
            messagebox.showerror("Remove offer", "Error has accord while communicating with the server")
            return

        if remove_room_ok:
            # messagebox.showinfo("Remove offer", "The offer has been removed")
            self.show_my_offers()
        else:
            messagebox.showerror("Remove offer", "Client side error has accord while removing the offer")

    @check_for_rating_after
    def add_room(self):
        """
        screen to add a new room
        :return: None
        """

        main_frame = self.layout()

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure((0, 16), weight=1)
        main_frame.rowconfigure((4, 6, 8, 10, 12, 14), weight=2)
        main_frame.rowconfigure(2, weight=4)

        label_add_room = customtkinter.CTkLabel(master=main_frame,
                                                text=f"Add an offer",
                                                fg_color=("white", "gray40"),
                                                height=60,
                                                text_font=("Arial", -22),
                                                justify=tkinter.CENTER)
        label_add_room.grid(column=0, row=1, sticky="nwe", padx=15, pady=15)

        label_errors = customtkinter.CTkLabel(master=main_frame,
                                              text=f"",
                                              fg_color=("white", "gray10"),
                                              text_font=("Arial", -22),
                                              justify=tkinter.CENTER)
        label_errors.grid(column=0, row=3, sticky="nwe", padx=15, pady=15)
        label_errors.grid_forget()

        name_entry = customtkinter.CTkEntry(master=main_frame, corner_radius=20, width=300, height=35,
                                            placeholder_text="room name...")
        name_entry.grid(column=0, row=5)

        price_entry = customtkinter.CTkEntry(master=main_frame, corner_radius=20, width=300, height=35,
                                             placeholder_text="room daily price...")
        price_entry.grid(column=0, row=7)

        description_entry = customtkinter.CTkEntry(master=main_frame, corner_radius=20, width=300, height=35,
                                                   placeholder_text="room description...")
        description_entry.grid(column=0, row=9)

        coords_frame = customtkinter.CTkFrame(master=main_frame, corner_radius=6)
        coords_frame.grid(column=0, row=11)

        coordinates_entry = customtkinter.CTkEntry(master=coords_frame, corner_radius=20, width=300, height=35,
                                                   placeholder_text="room coordinates...")
        coordinates_entry.grid(column=0, row=0, padx=5)

        customtkinter.CTkButton(master=coords_frame,
                                text="Coordinates",
                                image=ImageTk.PhotoImage(Image.open("client_images/map_icon.png").resize((25, 25))),
                                compound="right",
                                text_font=("Arial", -20),
                                corner_radius=6,
                                command=self.map_for_coords,
                                border_width=2).grid(column=1, row=0, padx=5)

        customtkinter.CTkButton(master=main_frame,
                                text="Select pictures",
                                text_font=("Arial", -20),
                                corner_radius=6,
                                command=self.set_pictures,
                                border_width=2).grid(column=0, row=13)

        customtkinter.CTkButton(master=main_frame,
                                text="Add offer",
                                text_font=("Arial", -22),
                                corner_radius=6,
                                command=lambda: self.handle_add_room(name_entry.get(), price_entry.get(),
                                                                     description_entry.get(), coordinates_entry.get(),
                                                                     label_errors),
                                border_width=0).grid(column=0, row=15, sticky=tkinter.EW, padx=15)

    def map_for_coords(self):
        """
        top level window with a map to get coordinates of a location
        :return: None
        """

        surface = customtkinter.CTkToplevel()
        surface.geometry("700x600+40+100")
        surface.minsize(700, 600)
        surface.title(f"map for coords")

        surface.columnconfigure((0, 1), weight=1)
        surface.rowconfigure((0, 4, 7), weight=1)
        surface.rowconfigure(2, weight=3)
        surface.rowconfigure(3, weight=10)

        label_add_room = customtkinter.CTkLabel(master=surface,
                                                text=f"Map for coordinates\nright click the map for coords",
                                                fg_color=("white", "gray40"),
                                                height=60,
                                                text_font=("Arial", -22),
                                                justify=tkinter.CENTER)
        label_add_room.grid(column=0, row=1, columnspan=2, sticky="nwe", padx=15, pady=15)

        map_widget = TkinterMapView(surface, corner_radius=9)
        map_widget.grid(row=3, column=0, columnspan=2, sticky=tkinter.NSEW, padx=15, pady=15)
        map_widget.set_address("israel")

        location_entry = customtkinter.CTkEntry(master=surface, corner_radius=20, width=300, height=35,
                                                placeholder_text="address...")
        location_entry.grid(column=0, row=5)

        customtkinter.CTkButton(master=surface,
                                text="find",
                                text_font=("Arial", -20),
                                corner_radius=6,
                                command=lambda: map_widget.set_address(location_entry.get()),
                                border_width=2).grid(column=1, row=5)

    def set_pictures(self):
        """
        file dialog screen and saves the file name to a variable
        :return: None
        """

        filetypes = (
            ('image files', '.png'),
        )

        filenames = filedialog.askopenfilenames(
            title='Open pictures',
            initialdir='/',
            filetypes=filetypes)

        self.pictures = tuple() if len(filenames) == 0 else filenames

    def handle_add_room(self, name, price, description, location, errors_label):
        """
        validating user input and sending new room data to the server with the client network interface
        :param name: str
        :param price: str
        :param description: str
        :param location: str
        :return: None
        """

        if name == "" or name.isspace():
            # messagebox.showerror("Add offer", "Please fill the name field")
            errors_label.grid(column=0, row=3, sticky="nwe", padx=15)
            errors_label.configure(text="Please fill the name field")
            return

        if price == "" or price.isspace():
            # messagebox.showerror("Add offer", "Please fill the price field")
            errors_label.grid(column=0, row=3, sticky="nwe", padx=15)
            errors_label.configure(text="Please fill the price field")
            return

        try:
            price = float(price)
        except:
            # messagebox.showerror("Add offer", "Please enter valid price")
            errors_label.grid(column=0, row=3, sticky="nwe", padx=15)
            errors_label.configure(text="Please enter valid price")
            return

        if price <= 0:
            # messagebox.showerror("Add offer", "Please enter valid price")
            errors_label.grid(column=0, row=3, sticky="nwe", padx=15)
            errors_label.configure(text="Please enter valid price")
            return

        if description == "" or description.isspace():
            # messagebox.showerror("Add offer", "Please fill the description field")
            errors_label.grid(column=0, row=3, sticky="nwe", padx=15)
            errors_label.configure(text="Please fill the description field")
            return

        if location == "" or location.isspace():
            # messagebox.showerror("Add offer", "Please fill the description field")
            errors_label.grid(column=0, row=3, sticky="nwe", padx=15)
            errors_label.configure(text="Please fill the location field")
            return

        if len(location.split(" ")) != 2:
            # messagebox.showerror("Add offer", "Please enter valid coordinates")
            errors_label.grid(column=0, row=3, sticky="nwe", padx=15)
            errors_label.configure(text="Please enter valid coordinates")
            return

        picture_names = self.pictures

        add_offer_ok, success = self.client.add_room(name, price, description, location.replace(" ", ","),
                                                     picture_names)

        self.pictures = tuple()

        if not success:
            messagebox.showerror("Add offer", "Error has accord while communicating with the server")
            return

        if add_offer_ok:
            # messagebox.showinfo("Add offer", "The offer has been added")
            self.show_my_offers()
        else:
            messagebox.showerror("Add offer", "Client side error has accord while adding the offer")

    def rating(self, purchase_id, room_name):
        """
        top level window to rate a room
        :param purchase_id: int
        :param room_name: str
        :return: None
        """

        surface = customtkinter.CTkToplevel()
        surface.geometry("500x300+40+100")
        surface.minsize(600, 400)
        surface.title(f"rate - {room_name}")

        surface.columnconfigure(0, weight=1)
        surface.rowconfigure((0, 9), weight=1)
        surface.rowconfigure(6, weight=2)
        surface.rowconfigure(2, weight=3)

        label_add_room = customtkinter.CTkLabel(master=surface,
                                                text=f"Rate the room - {room_name}\nfrom 1 to 5",
                                                fg_color=("white", "gray40"),
                                                height=60,
                                                text_font=("Arial", -22),
                                                justify=tkinter.CENTER)
        label_add_room.grid(column=0, row=1, sticky="nwe", padx=15, pady=15)

        label_errors = customtkinter.CTkLabel(master=surface,
                                              text=f"",
                                              fg_color=("white", "gray10"),
                                              text_font=("Arial", -22),
                                              justify=tkinter.CENTER)
        label_errors.grid(column=0, row=3, sticky="nwe", padx=15, pady=15)
        label_errors.grid_forget()

        rate_entry = customtkinter.CTkEntry(master=surface, corner_radius=20, width=100, height=35,
                                            placeholder_text="room rating...")
        rate_entry.grid(column=0, row=5)

        customtkinter.CTkButton(master=surface,
                                text="Rate",
                                text_font=("Arial", -20),
                                corner_radius=6,
                                command=lambda: self.handle_rating(purchase_id, rate_entry.get(), surface,
                                                                   label_errors),
                                border_width=2).grid(column=0, row=7)

        surface.mainloop()

    def handle_rating(self, purchase_id, rating, surface, errors_label):
        """
        validating user input and sending rating to the server with the client network interface
        :param purchase_id: int
        :param rating: str
        :param surface: CTkToplevel
        :return: None
        """

        if rating == "" or rating.isspace():
            # messagebox.showerror("Rating", "Please fill the rating field")
            errors_label.grid(column=0, row=3, sticky="nwe", padx=15, pady=15)
            errors_label.configure(text="Please fill the rating field")
            return

        try:
            rating = int(rating)
        except:
            # messagebox.showerror("Rating", "Please enter valid rating\n(integer from 1 to 5)")
            errors_label.grid(column=0, row=3, sticky="nwe", padx=15, pady=15)
            errors_label.configure(text="Please enter valid rating(integer from 1 to 5)")
            return

        if rating < 1 or rating > 5:
            # messagebox.showerror("Rating", "Please enter valid rating\n(integer from 1 to 5)")
            errors_label.grid(column=0, row=3, sticky="nwe", padx=15, pady=15)
            errors_label.configure(text="Please enter valid rating(integer from 1 to 5)")
            return

        rating_ok, success = self.client.rate_room(purchase_id, rating)

        if not success:
            messagebox.showerror("Rating", "Error has accord while communicating with the server")
            return

        if rating_ok:
            # messagebox.showinfo("Rating", "The room has been rated")
            surface.destroy()
        else:
            messagebox.showerror("Rating", "Client side error has accord while rating the room")

    def layout(self, function_use=None):
        """
        sets up the side menu and main frame and return the main frame
        :param function_use: function to execute -> optional
        :return: CTkFrame
        """

        self.clear()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame_left = customtkinter.CTkFrame(master=self,
                                            width=150)
        frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        frame_right = customtkinter.CTkFrame(master=self,
                                             corner_radius=10)
        frame_right.grid(row=0, column=1, rowspan=1, pady=20, padx=20, sticky="nsew")

        # side_bar_layout

        frame_left.grid_rowconfigure(0, minsize=10)

        image = Image.open("client_images/Logo.png").resize((120, 120))
        image = ImageTk.PhotoImage(image)

        label_logo = tkinter.Label(master=frame_left, image=image)
        label_logo.image = image
        label_logo.grid(column=0, row=0, pady=10, padx=20)

        name_disabled_btn = customtkinter.CTkButton(master=frame_left,
                                                    text=f"Hello, {self.client.get_name()}",
                                                    text_font=("Arial", "11", "bold"),
                                                    width=120, height=30,
                                                    border_width=0,
                                                    corner_radius=8)
        name_disabled_btn.grid(pady=10, padx=20, row=1, column=0)

        home_btn = customtkinter.CTkButton(master=frame_left,
                                           text="Home",
                                           command=self.home,
                                           width=120, height=30,
                                           border_width=0,
                                           corner_radius=8)
        home_btn.grid(pady=10, padx=20, row=2, column=0, sticky=tkinter.EW)

        if not self.logged_in:
            login_btn = customtkinter.CTkButton(master=frame_left,
                                                text="Log in",
                                                command=self.login,
                                                width=120, height=30,
                                                border_width=0,
                                                corner_radius=8)
            login_btn.grid(pady=10, padx=20, row=3, column=0, sticky=tkinter.EW)

            signup_btn = customtkinter.CTkButton(master=frame_left,
                                                 text="Sign up",
                                                 command=self.sign_up,
                                                 width=120, height=30,
                                                 border_width=0,
                                                 corner_radius=8)
            signup_btn.grid(pady=10, padx=20, row=4, column=0, sticky=tkinter.EW)

        else:
            offers_btn = customtkinter.CTkButton(master=frame_left,
                                                 text="Offers",
                                                 command=self.search_offers,
                                                 width=120, height=30,
                                                 border_width=0,
                                                 corner_radius=8)
            offers_btn.grid(pady=10, padx=20, row=3, column=0, sticky=tkinter.EW)

            add_offer_btn = customtkinter.CTkButton(master=frame_left,
                                                    text="Add offer",
                                                    command=self.add_room,
                                                    width=120, height=30,
                                                    border_width=0,
                                                    corner_radius=8)
            add_offer_btn.grid(pady=10, padx=20, row=4, column=0, sticky=tkinter.EW)

            my_offers_btn = customtkinter.CTkButton(master=frame_left,
                                                    text="my offers",
                                                    command=self.show_my_offers,
                                                    width=120, height=30,
                                                    border_width=0,
                                                    corner_radius=8)
            my_offers_btn.grid(pady=10, padx=20, row=5, column=0, sticky=tkinter.EW)

            my_purchases_btn = customtkinter.CTkButton(master=frame_left,
                                                       text="my purchases",
                                                       command=self.show_my_purchases,
                                                       width=120, height=30,
                                                       border_width=0,
                                                       corner_radius=8)
            my_purchases_btn.grid(pady=10, padx=20, row=6, column=0, sticky=tkinter.EW)

            logout_btn = customtkinter.CTkButton(master=frame_left,
                                                 text="Logout",
                                                 fg_color="red",
                                                 command=self.logout,
                                                 width=120, height=30,
                                                 border_width=0,
                                                 corner_radius=8)
            logout_btn.grid(pady=10, padx=20, row=7, column=0, sticky=tkinter.EW)

            if function_use is not None:
                function_use(frame_left)

        return frame_right

    def check_for_rating(self):
        """
        checks with the server with the client network interface if there are rooms to rate and open rating window
        :return: None
        """

        if self.logged_in:
            rooms_to_rate, success = self.client.rooms_to_rate()

            if success:
                for room_to_rate in rooms_to_rate:
                    self.rating(room_to_rate["purchase_id"], room_to_rate["room_name"])

    def logout(self):
        """
        changing logged in to false and going to home screen
        :return: None
        """

        self.logged_in = False
        self.home()

    def clear(self):
        """
        clears all the widgets on the screen
        :return: None
        """

        for w in self.winfo_children():
            w.destroy()

    def on_closing(self):
        self.destroy()

    def start(self):
        self.mainloop()
