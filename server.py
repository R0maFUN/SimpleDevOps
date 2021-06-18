# -*- coding: utf-8 -*-

import socket

OK_RESPONSE = """HTTP/1.1 200 OK
Content-Type: text/html

{}"""

NOT_FOUND_RESPONSE = """HTTP/1.1 404 NOT FOUND
Content-Type: text/html

{}"""

UNAUTHORIZED_RESPONSE = """HTTP/1.1 401 NOT AUTHORIZED
Content-Type: text/html

{}"""

SET_AUTH_RESPONSE = """HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: authorized=1;

ok!
"""


def r_ok(response):
    return OK_RESPONSE.format(response).encode()


def r_404(response):
    return NOT_FOUND_RESPONSE.format(response).encode()


def r_401(response):
    return UNAUTHORIZED_RESPONSE.format(response).encode()


def r_auth():
    return SET_AUTH_RESPONSE.encode()


def parse_request(raw):
    data = raw.decode()
    url = data.split('/', 1)[1].split(' ')[0]
    method = data.split(' ')[0]
    head_body = data.split('\r\n\r\n')
    if len(head_body) == 1:
        head = head_body[0]
        body = ''
    else:
        head, body = head_body
    request = {
        'url': url,
        'method': method,
        'head': head,
        'body': body
    }
    print(data)
    return request


def prepare_response(request):
    return r_ok('OK123')


def v_index(request):
    return r_ok(read_file('index.html'))


def v_secret(request):
    if 'authorized=1' in request['head']:
        return r_ok(read_file('secret.html'))
    else:
        return r_401('Login first!')
    

def v_login(request):
    if 'authorized=1' in request['head']:
        return r_ok('You are authorized')
    if request['method'] == 'GET':
        return r_ok(read_file('login.html'))
    elif request['method'] == 'POST':
        return r_auth()
    
    return r_401('Unknown method')


def v_icon(request):
    img = read_file('favicon.ico', mode='rb')
    return 'HTTP/1.1 200 OK\r\nContent-Type: image/ico\r\n\r\n'.encode() + img


def read_file(path, mode='r'):
    with open(path, mode) as f:
        return f.read()
    
    
def run():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 5000))
    sock.listen(1)
    print("Server is running on x:5000")
    while True:
        conn, addr = sock.accept()
        print(f'------ Connected: {addr}')
        raw = conn.recv(1000)
        # request = parse_request(raw)
        request = ''
        response = prepare_response(request)
        conn.send(response)
        conn.close()
        print(f'------ Bye \n\n')
        
        
if __name__ == '__main__':
    run()
    
