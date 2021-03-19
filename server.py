import threading
import socket

host = '127.0.0.1' 
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames  = []

def broadcast(pesan):
    for client in clients:
        client.send(pesan)

def handle(client):
    while True:
        try:
            pesan = client.recv(1024)
            broadcast(pesan)
        except:
            index  = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} Keluar dari chat !'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, alamat = server.accept()
        print(f"tersambung dengan {str(alamat)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1090).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nama yang bergabung dichat adalah {nickname}!')
        broadcast(f'{nickname} bergabung di chat!'.encode('ascii'))
        client.send('Tersambung dalam server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server sedang memproses...")
receive()