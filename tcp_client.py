import socket
import json



def tcp_client(target_host=None, target_port=None, send_data=None):
    """ TCP 客户端 """
    target_host = target_host if target_host else "www.baidu.com"
    target_port = target_port if target_port else 80
    send_data = bytes(json.dumps(send_data, ensure_ascii=False), encoding='utf-8')+ b'\r\n' if send_data else b"GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n"

    # 建立一个 socket 对象
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接客户端
    client.connect((target_host, target_port))
    # 发送数据
    client.send(send_data)
    # 接收数据
    response = b''

    while True:
        res = client.recv(1024)
        response += res
        if len(res) < 1024:
            break
    #print(str(response))
    d = json.loads(response)
    if d.get("message","fail") != 'message':
        print(d)
data = {}
data['method'] = 'act'
data['data'] = 'Hello,world!'
tcp_client('*****',9503,data)