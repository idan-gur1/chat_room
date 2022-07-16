import customtkinter
import tkinter
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from .view import App


class AdminApp(App):
    def __init__(self, admin_client, *args, **kwargs):
        """
        setting up admin graphical user interface
        :param args: customtkinter CTk args
        :param kwargs: customtkinter CTk kwargs
        """

        super().__init__(admin_client, *args, **kwargs)
        self.client = admin_client
        self.admin_login()

    def admin_login(self):
        """
        admin login screen
        :return: None
        """

        self.clear()

        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = customtkinter.CTkFrame(master=self)
        frame.grid(row=0, column=0, padx=15, pady=15, sticky=tkinter.NSEW)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=0)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure((4, 6), weight=2)
        frame.grid_rowconfigure(2, weight=4)
        label_home = customtkinter.CTkLabel(master=frame,
                                            text=f"Welcome to IdanB admin client\nplease login with you admin user",
                                            fg_color=("white", "gray40"),
                                            height=100,
                                            text_font=("Arial", -22),
                                            justify=tkinter.CENTER)
        label_home.grid(column=0, row=1, sticky="nwe", padx=15, pady=15)

        id_entry = customtkinter.CTkEntry(master=frame, corner_radius=20, width=300, height=50,
                                          placeholder_text="admin id")
        id_entry.grid(column=0, row=3, padx=15, pady=15)

        password_entry = customtkinter.CTkEntry(master=frame, corner_radius=20, width=300, height=50,
                                                placeholder_text="admin password")
        password_entry.grid(column=0, row=5, padx=15, pady=15)

        login_btn = customtkinter.CTkButton(master=frame, text="Login", text_font=("Arial", -22),
                                            corner_radius=6,
                                            command=lambda: self.handle_admin_login(id_entry.get(),
                                                                                    password_entry.get()),
                                            width=200)
        login_btn.grid(column=0, row=7, sticky="nwe", padx=15, pady=15)

    def handle_admin_login(self, admin_id: str, admin_password: str):
        """
        validating user input and sending it to the sever with the admin network interface
        :param admin_id: str
        :param admin_password: str
        :return: None
        """

        if admin_id == "" or admin_id.isspace():
            messagebox.showerror("Login", "please fill the admin id field")
            return
        if admin_password == "" or admin_password.isspace():
            messagebox.showerror("Login", "please fill the admin password field")
            return
        if len(admin_password) < 6:
            messagebox.showerror("Login", "admin password must be at least 6 characters")
            return

        login_ok, success = self.client.admin_login(admin_id, admin_password)

        if not success:
            messagebox.showerror("Login", "Error has accord while communicating with the server")
            return

        if login_ok:
            messagebox.showinfo("Login", "You have successfully logged in!")
            self.logged_in = True
            self.home()
        else:
            messagebox.showerror("Login", "admin id or password are wrong")

    def change_date(self):
        """
        change date screen
        :return: None
        """
        main_frame = self.layout()

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure((0, 6), weight=1)
        main_frame.rowconfigure(4, weight=2)
        main_frame.rowconfigure(2, weight=4)

        label_offer = customtkinter.CTkLabel(master=main_frame,
                                             text=f"Enter new server time",
                                             fg_color=("white", "gray40"),
                                             height=100,
                                             text_font=("Arial", -26),
                                             justify=tkinter.CENTER)
        label_offer.grid(column=0, row=1, sticky="nwe", padx=15, pady=15)

        date_entry = DateEntry(master=main_frame, date_pattern="d/m/yyyy",
                               font=("Arial", 18))
        date_entry.grid(column=0, row=3, padx=15, pady=15)

        date_btn = customtkinter.CTkButton(master=main_frame,
                                           text="Change server time",
                                           command=lambda: self.handle_change_date(date_entry.get()),
                                           width=200, height=50,
                                           text_font=("Arial", -22),
                                           border_width=0,
                                           corner_radius=8)
        date_btn.grid(pady=10, padx=20, row=5, column=0, sticky=tkinter.EW)

    def handle_change_date(self, date):
        """
        send to the server the new date with the admin network interface
        :param date: str
        :return: None
        """
        success = self.client.change_time(date)

        if not success:
            messagebox.showerror("change date", "Error has accord while communicating with the server")
        else:
            messagebox.showinfo("change date", "Server time has been changed")

    def all_rooms(self):
        """
        screen that gets from the server all of the rooms with the admin network interface and shows them
        :return: None
        """
        my_rooms, success = self.client.get_all_rooms()

        if not success:
            messagebox.showerror("all rooms", "Error has accord while communicating with the server")
            return

        main_frame = self.layout()

        for room in my_rooms:
            room["distance"] = 0

        customtkinter.CTkButton(master=main_frame,
                                text="all rooms in map",
                                text_font=("Arial", -18),
                                corner_radius=8,
                                border_width=0,
                                command=lambda: self.show_offers(my_rooms, "", "", "", "", False)).place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)

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
                                                  text=f"room owner",
                                                  fg_color=("white", "gray60"),
                                                  text_font=("Arial", -18, "bold"),
                                                  justify=tkinter.CENTER,
                                                  pady=4, padx=4)
        label_start_date.grid(column=1, row=0, padx=4, pady=4)
        label_start_date = customtkinter.CTkLabel(master=table_frame,
                                                  text=f"total income",
                                                  fg_color=("white", "gray60"),
                                                  text_font=("Arial", -18, "bold"),
                                                  justify=tkinter.CENTER,
                                                  pady=4, padx=4)
        label_start_date.grid(column=2, row=0, padx=4, pady=4)
        label_end_date = customtkinter.CTkLabel(master=table_frame,
                                                text=f"in map",
                                                fg_color=("white", "gray60"),
                                                text_font=("Arial", -18, "bold"),
                                                justify=tkinter.CENTER,
                                                pady=4, padx=4)
        label_end_date.grid(column=3, row=0, padx=4, pady=4)
        label_dispute = customtkinter.CTkLabel(master=table_frame,
                                               text=f"view",
                                               fg_color=("white", "gray60"),
                                               text_font=("Arial", -18, "bold"),
                                               justify=tkinter.CENTER,
                                               pady=4, padx=4)
        label_dispute.grid(column=4, row=0, padx=4, pady=4)

        my_rooms.sort(key=lambda offer: offer["room_id"])

        for row, room in enumerate(my_rooms):
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{room['room_name']}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=0, row=row + 1, padx=4, pady=4)
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{room['owner_name']}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=1, row=row + 1, padx=4, pady=4)
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{round(room['total_income'], 1)}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=2, row=row + 1, padx=4, pady=4)
            customtkinter.CTkButton(master=table_frame,
                                    text="map",
                                    text_font=("Arial", -18),
                                    corner_radius=8,
                                    border_width=0,
                                    command=lambda x=room: self.show_room_in_map(x)).grid(column=3,
                                                                                          row=row + 1,
                                                                                          padx=4,
                                                                                          pady=4)
            customtkinter.CTkButton(master=table_frame,
                                    text="view",
                                    text_font=("Arial", -18),
                                    corner_radius=8,
                                    border_width=0,
                                    command=lambda x=room: self.show_room(x, "", "", False)).grid(column=4,
                                                                                                  row=row + 1,
                                                                                                  padx=4,
                                                                                                  pady=4)

    def all_users(self):
        """
        screen that gets from the server all of the users with the admin network interface and shows them
        :return: None
        """
        users, success = self.client.get_all_users()

        if not success:
            messagebox.showerror("all users", "Error has accord while communicating with the server")
            return

        main_frame = self.layout()

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        table_frame = customtkinter.CTkFrame(master=main_frame)
        table_frame.grid(column=0, row=0)

        label_start_date = customtkinter.CTkLabel(master=table_frame,
                                                  text=f"name",
                                                  fg_color=("white", "gray60"),
                                                  text_font=("Arial", -18, "bold"),
                                                  justify=tkinter.CENTER,
                                                  pady=4, padx=4)
        label_start_date.grid(column=0, row=0, padx=4, pady=4, sticky=tkinter.EW)
        label_end_date = customtkinter.CTkLabel(master=table_frame,
                                                text=f"email",
                                                fg_color=("white", "gray60"),
                                                text_font=("Arial", -18, "bold"),
                                                justify=tkinter.CENTER,
                                                pady=4, padx=4)
        label_end_date.grid(column=1, row=0, padx=4, pady=4, sticky=tkinter.EW)
        label_dispute = customtkinter.CTkLabel(master=table_frame,
                                               text=f"total income",
                                               fg_color=("white", "gray60"),
                                               text_font=("Arial", -18, "bold"),
                                               justify=tkinter.CENTER,
                                               pady=4, padx=4)
        label_dispute.grid(column=2, row=0, padx=4, pady=4, sticky=tkinter.EW)
        label_remove = customtkinter.CTkLabel(master=table_frame,
                                              text=f"purchases",
                                              fg_color=("white", "gray60"),
                                              text_font=("Arial", -18, "bold"),
                                              justify=tkinter.CENTER,
                                              pady=4, padx=4)
        label_remove.grid(column=3, row=0, padx=4, pady=4, sticky=tkinter.EW)

        users.sort(key=lambda offer: offer["user_id"])

        for row, user in enumerate(users):
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{user['name']}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=0, row=row + 1, padx=4, pady=4, sticky=tkinter.EW)
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{user['email']}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=1, row=row + 1, padx=4, pady=4, sticky=tkinter.EW)
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{user['total_income']}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=2, row=row + 1, padx=4, pady=4, sticky=tkinter.EW)
            customtkinter.CTkLabel(master=table_frame,
                                   text=f"{user['purchases']}",
                                   fg_color=("white", "gray40"),
                                   text_font=("Arial", -18),
                                   justify=tkinter.CENTER,
                                   pady=4, padx=4).grid(column=3, row=row + 1, padx=4, pady=4, sticky=tkinter.EW)

    def set_attractions(self):
        """
        opens up file dialog to choose a file and then sends it to the server with the admin network interface
        :return: None
        """

        filetypes = (
            ('json files', '*.json'),
        )
        filename = filedialog.askopenfilename(
            title='Open files',
            initialdir='/',
            filetypes=filetypes)

        if filename == "" or filename.isspace():
            return

        success = self.client.set_attractions(filename)

        if not success:
            messagebox.showerror("attractions", "Error has accord while communicating with the server")
        else:
            messagebox.showinfo("attractions", "attractions has been changed")

    def admin_panel(self):
        """
        admin panel screen
        :return: None
        """

        main_frame = self.layout()

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure((0, 10), weight=1)
        main_frame.rowconfigure((4, 6, 8), weight=2)
        main_frame.rowconfigure(2, weight=4)

        label_offer = customtkinter.CTkLabel(master=main_frame,
                                             text=f"Admin Panel",
                                             fg_color=("white", "gray40"),
                                             height=100,
                                             text_font=("Arial", -26),
                                             justify=tkinter.CENTER)
        label_offer.grid(column=0, row=1, sticky="nwe", padx=15, pady=15)

        date_btn = customtkinter.CTkButton(master=main_frame,
                                           text="Change server time",
                                           command=self.change_date,
                                           width=200, height=50,
                                           text_font=("Arial", -22),
                                           border_width=0,
                                           corner_radius=8)
        date_btn.grid(pady=10, padx=20, row=3, column=0)

        all_rooms_btn = customtkinter.CTkButton(master=main_frame,
                                                text="All rooms",
                                                command=self.all_rooms,
                                                width=200, height=50,
                                                text_font=("Arial", -22),
                                                border_width=0,
                                                corner_radius=8)
        all_rooms_btn.grid(pady=10, padx=20, row=5, column=0)

        all_rooms_btn = customtkinter.CTkButton(master=main_frame,
                                                text="All users",
                                                command=self.all_users,
                                                width=200, height=50,
                                                text_font=("Arial", -22),
                                                border_width=0,
                                                corner_radius=8)
        all_rooms_btn.grid(pady=10, padx=20, row=7, column=0)

        all_rooms_btn = customtkinter.CTkButton(master=main_frame,
                                                text="Set attractions",
                                                command=self.set_attractions,
                                                width=200, height=50,
                                                text_font=("Arial", -22),
                                                border_width=0,
                                                corner_radius=8)
        all_rooms_btn.grid(pady=10, padx=20, row=9, column=0)

    def change_btn(self, frame):
        """
        grids a button in a frame
        :param frame: CTkFrame
        :return: None
        """

        admin_btn = customtkinter.CTkButton(master=frame,
                                            text="Admin panel",
                                            fg_color="red",
                                            hover_color="red3",
                                            command=self.admin_panel,
                                            width=120, height=30,
                                            border_width=0,
                                            corner_radius=8)
        admin_btn.grid(pady=10, padx=20, row=7, column=0, sticky=tkinter.EW)

    def layout(self, function_use=None):
        """
        overrides the layout function to switch the logout button to admin panel button
        :param function_use: function
        :return: CTkFrame
        """
        frame = super().layout(self.change_btn)
        return frame
