"""
Author: Idan Gur
air bnb admin client and gui
"""

from view.admin_view import AdminApp
from controller.admin_client import AdminClient

if __name__ == '__main__':
    client = AdminClient()
    app = AdminApp(client)
    app.start()
