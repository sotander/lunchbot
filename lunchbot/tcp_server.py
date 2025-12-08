#!/usr/bin/env python3
import socket
import threading

HOST = "0.0.0.0"  # listen on all interfaces
PORT = 1024      # change this to the port you want

# Simple chatbot responses
responses = {
    "hello": "Hello! How can I help you?\n",
    "bye": "Goodbye!\n"
}


def handle_client(conn, addr):
    """Handle a single client connection"""
    with conn:
        try:
            data = conn.recv(1024)
            if not data:
                return
            # Decode UTF-8 safely
            message = data.decode("utf-8").strip()
            # Lookup response
            reply = responses.get(message.lower(), "Unknown input.\n")
            conn.sendall(reply.encode("utf-8"))
        except Exception as e:
            print(f"Error handling {addr}: {e}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"LunchBot server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
