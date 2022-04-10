import socket

print('Для выхода из чата наберите: `exit`, `quit` или `q`.')

host = '127.0.0.1'
port = 7897
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    while True:
        mess = input('\nВведите сообщение: >>> ')
        if any(mess.lower() in ext for ext in ['quit', 'exit', 'q']):
            break
        mess = mess.encode('utf-8')
        s.sendall(mess)
        data = s.recv(1024)
        print('\nПолучено: ', data.decode('utf-8'))
