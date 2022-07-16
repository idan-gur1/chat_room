"""
Author: Idan Gur
air bnb client and gui
"""

from view.view import App
from controller.client import Client

if __name__ == '__main__':
    client = Client()
    app = App(client)
    app.start()
