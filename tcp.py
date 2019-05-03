import socket
import json


HOST = '127.0.0.1'    # The remote host
PORT = 12000               # The same port as used by the server
count=0


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP) as s:
    s.connect((HOST, PORT))
    data = {}
    data['method'] = 'act'
    data['data'] = 'Hello,world!'
    s.sendall(bytes(json.dumps(data, ensure_ascii=False), encoding='utf-8'))

    while count<10:
        count+=1
        data = s.recv(1024)
        print(data)
        print(data)
        print(str(type(data)))
        #print(str(type(count)))
        #data=data+data
        #data=data+bytes(count)
        s.sendall(data)

        print('Received', repr(data))
