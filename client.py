import threading
import socket

nickname = input("Masukan username : ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('165.22.251.42', 8079))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)

        except:
            print("Terjadi kesalahan program")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
