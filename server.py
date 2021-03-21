import threading
import socket
import datetime

host = '165.22.251.42'
port = 8079

# SOCKET STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# REUSE ADDRESS AND SOCKET
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


server.bind((host, port))
server.listen(10)

# List of client
list_clients = []
# List of username
list_of_username = []


def broadcast(pesan):
    for client in list_clients:
        client.send(pesan)


def handle(koneksi):
    # Greeting
    koneksi.send(
        ("\n =====Selamat datang di shellchat===== \n").encode('ascii'))

    while True:
        try:
            pesan = koneksi.recv(1024)
            broadcast(pesan)
        except:
            """
                Jika koneksi terputus hapus koneksi dari server
            """

            # Cari index dari list client
            index = list_clients.index(koneksi)

            # Hapus koneksi dari list client
            list_clients.remove(index)

            # Tutup koneksi
            koneksi.close()

            # Cari username dari list username
            username = list_of_username[index]

            # Print di server bahwa user tersebut keluar
            print(
                "<| {} |-{}> terkoneksi.".format(username, datetime.datetime.now()))

            # Broadcast ke tiap user bahwa keluar
            broadcast(f'{username} Keluar dari chat !'.encode('ascii'))

            # Hapus username dari list
            list_of_username.remove(username)

            break


def receive():
    """
        This method to receive incoming connection from client
    """

    while True:
        client, alamat = server.accept()

        # Mengirim pesan untuk meminta username klien
        client.send('NICK'.encode('ascii'))

        # Decode ascii code username
        username = client.recv(1090).decode('ascii')

        # Cetak jika user terkoneksi
        print(
            "<|{} {}  |-{}> terkoneksi.".format(alamat[0], username, datetime.datetime.now()))

        # Tampung username ke list username
        list_of_username.append(username)

        # Save client name
        list_clients.append(client)

        broadcast(f'{username} bergabung di chat!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server online di port {}, menunggu koneksi...".format(port))
receive()
