import base64
import socket
import ssl


def request(socket, request):
    socket.send((request + '\n').encode())
    recv_data = socket.recv(65536).decode()
    return recv_data


def read_msg():
    with open('msg.txt.') as file:
        return '\n'.join(file.readlines())


def read_pict():
    with open("icon.png", 'rb') as file:
        return base64.b64encode(file.read()).decode()


def create_message():
    head = ""
    head += "From: " + user_name + '\n'
    head += "To: " + target + '\n'
    head += "Subject: " + "=?utf-8?B?" + base64.b64encode("Тестовое письмо".encode()).decode() + "?=" + '\n'
    head += "MIME-Version: 1.0" + '\n'
    bound = "bound123456789"
    head += 'Content-Type: multipart/mixed; boundary = "' + bound + '"' +'\n'
    head += '\n'
    body = ""
    body += "--" + bound + '\n'
    body += "Content-Transfer-Encoding: utf-8" + '\n'
    body += "Content-Type: text/plain" + '\n' + '\n'
    body += read_msg() + '\n'
    body += "--" + bound + '\n'
    body += 'Content-Disposition: attachment; filename="icon.png"' \
            '\nContent-Transfer-Encoding: base64' \
            '\nContent-Type: image/png; name="icon.png' + '\n' + '\n'
    body += read_pict() + '\n'
    body += "--" + bound + "--" + '\n'
    body += '.' + '\n'
    return head + body


host_addr = 'smtp.yandex.ru'
port = 465
target = 'original-account-forIP@yandex.ru'
user_name = 'original-account-forIP@yandex.ru'
password = "originalpassword"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host_addr, port))
    client = ssl.wrap_socket(client)
    print(client.recv(1024))
    print(request(client, 'EHLO ' + user_name))
    base64login = base64.b64encode(user_name.encode()).decode()
    base64password = base64.b64encode(password.encode()).decode()
    print(request(client, "AUTH LOGIN"))
    print(request(client, base64login))
    print(request(client, base64password))
    print(request(client, "MAIL FROM: " + user_name))
    print(request(client, "RCPT TO: " + target))
    print(request(client, 'DATA'))
    print(request(client, create_message()))
