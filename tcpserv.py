import socket
server=socket.socket()
adre=('127.0.0.1',12000)
server.bind(adre)
server.listen(5)   #最多排队数5
conn,adress= server.accept()
while True:
#    conn,adress= server.accept()   #如果需要排队聊天
#   while True:
    data = conn.recv(1024)
    print(str(data, 'utf8'))
    if str(data, 'utf8') == 'exit':
        break
    send_info=input('>>>')
    conn.sendall(bytes(send_info,'utf8'))
server.close()
