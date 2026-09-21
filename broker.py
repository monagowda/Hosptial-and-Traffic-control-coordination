import socket
import threading

# Localhost setup - completely offline
HOST = '127.0.0.1'
PORT = 5555

clients = []

def handle_client(client_socket):
    while True:
        try:
            # Receive data from ambulance
            message = client_socket.recv(4096)
            if not message:
                break
            # Broadcast it to all connected responders (Hospital/Traffic Police)
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(message)
                    except:
                        clients.remove(client)
        except:
            break
    client_socket.close()

def start_broker():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"🖥️  LOCAL SIMULATION HUB ONLINE (Running locally on port {PORT})")
    print("Waiting for Ambulance and Responders to connect...\n")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_broker()