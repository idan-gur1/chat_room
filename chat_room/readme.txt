README

Author: Idan Gur

Title:
    Client Server application

Description:
    this project connects a server with multiple clients and let them communicate between them and the server.
    I used multiple technologies while writing this program such as: sockets for networking and connecting the
    server with the clients, os handling known as select for the server to handle clients and struct for prefixing the
    message sent over socket with its length.

How to connect:
    In order to run the project you need first to run the port server and then change the ip of the port server in both the client and the server
    then choose name for the server after running it, and then finally in the client enter the name of the server you chose.
    And you are connected :)

client commands:
    An additional RFC file is added to explain all the functions that the client can use.