"""
Author: Idan Gur
air bnb server app
"""

from models.Database import Database
from controller.AirServer import AirServer

if __name__ == '__main__':
    database = Database()
    server = AirServer("0.0.0.0", 55555, database)
    server.start()
