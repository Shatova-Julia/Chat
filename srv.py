import select
import socket


print('Для выключения сервера нажмите Ctrl+C.')
sock = socket.socket()
sock.bind(('127.0.0.1', 7897))
sock.listen(5)
sock.setblocking(False)
inputs = [sock]
outputs = []
clients = list()
messages = {}

print('\nОжидание подключения...')
while True:
    reads, send, excepts = select.select(inputs, outputs, inputs)
    for conn in reads:
        if conn == sock:
            new_conn, client_addr = conn.accept()
            print('Успешное подключение!')
            new_conn.setblocking(False)
            inputs.append(new_conn)
        else:
            if conn not in clients:
                for client in clients:
                    client.send('Подключился новый клиент'.encode())

                clients.append(conn)

            data = conn.recv(1024)
            if data:
                if messages.get(conn, None):
                    messages[conn].append(data)
                else:
                    messages[conn] = [data]

                if conn not in outputs:
                    outputs.append(conn)
            else:
                print('Клиент отключился...')
                if conn in outputs:
                    outputs.remove(conn)

                for client in clients:
                    client.send('Клиент отключился'.encode())
                inputs.remove(conn)
                clients.remove(conn)
                conn.close()
                del messages[conn]

    for conn in send:
        msg = messages.get(conn, None)

        if len(msg):
            temp = msg.pop(0).decode('utf-8').upper()
            for client in clients:
                if client != conn:
                    client.send(temp.encode())
        else:
            outputs.remove(conn)

    for conn in excepts:
        print('Клиент отключился...')
        inputs.remove(conn)
        clients.remove(conn)

        for client in clients:
            client.send('Клиент отключился из-за ошибки'.encode())
        if conn in outputs:
            outputs.remove(conn)

        conn.close()
        del messages[conn]
