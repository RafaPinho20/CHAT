import socket
import threading

HOST = '192.168.0.11' # PUT YOUR IP
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

#broadcast
def broadcast(message):
    for client in clients:
        client.send(message)
        
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
        
#receive
def receive():
    while True:
        client, address = server.accept()
        print(f"Conectado com {str(address)}")
        
        client.send("Digite seu apelido: ".encode('utf-8'))
        nickname = client.recv(1024)
        
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"Apelido do cliente é: {nickname}")
        broadcast(f"{nickname} conectou no server!!!\n".encode('utf-8'))
        client.send("Conectado no server!".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client))
        thread.start()

print("Server running...")
receive()