#!/usr/bin/env python3
import socket
import threading
from lunchbot.chatbot import chat

HOST = "0.0.0.0"  # listen on all interfaces
PORT = 1024


def handle_client(sock):
    try:
        data = sock.recv(4096).decode().strip()
        if not data:
            return
        print(data)

        username = None
        if data.startswith("USER="):
            user_field, msg = data.split(" ", 1)
            username = user_field.split("=", 1)[1]
        else:
            msg = data
        
        reply = chat(username, msg)
        sock.sendall((reply + "\n").encode("utf-8"))
    finally:
        sock.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"LunchBot server listening on {HOST}:{PORT}")
        while True:
            sockett, addr = s.accept()
            threading.Thread(target=handle_client, args=(sockett,)).start()


if __name__ == "__main__":
    main()
