import requests
from lxml import etree
import re
import random
import aiohttp
import redis
import json
class parseEquipInfo:
    def __init__(self):
        self.agents = self.initUserAgent()
        self.redisPool = self.initRedis()
        self.getProxyByRedis()

        self.cookies = {}


    # 初始化user-agent
    def initUserAgent(self):
        result = []
        with open('user_agents.txt', 'r') as f:
            for line in f:
                # print(line)
                result.append(line.strip('\n'))
        return result

    # var equip = \{[^\}]*\};#Uis'
    def parseHtmlToEquipInfo(self):
        req = requests.session()
        self.getCookie('459','2008')
        content = req.get("https://xyq.cbg.163.com/cgi-bin/equipquery.py?act=buy_show_equip_info&equip_id=6237125&server_id=459",cookies = self.cookies['459'] ,headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.11.2 Chrome/65.0.3325.230 Safari/537.36"} ,allow_redirects=1)
        content.encoding = "gb2312"
        #print(content.text)
        #html = etree.HTML(content)
        p1 = "var reonsale_identify = \"[0-9a-zA-Z]+\""
        pattern1 = re.compile(p1)
        match = pattern1.findall(content.text)
        if len(match) > 0:
            reonsale_identify = eval((match[0].split("=")[1]).strip())
            print(reonsale_identify)
        else:
            reonsale_identify = ''
        p2 = "var equip = \{[^\}]*\};"
        pattern2 = re.compile(p2)
        match_equip = pattern2.findall(content.text)
        if len(match_equip) > 0:
            json_data = match_equip[0]
            ret = json_data[json_data.index("=")+1:len(json_data)-1].replace("\n",'').replace("\r",'').replace("\t","").replace(" ",'')
            rt = ret[0:ret.index("valid") - 2] + "}"
            #print(rt)
            equip = json.loads(rt)
        else:
            return False
        equip['reonsale_identify'] = reonsale_identify

            #print(match_equip)

    # 获取cookie
    def getCookie(self, server_id, server_name):
        try:
            loginUrl = "https://xyq.cbg.163.com/cgi-bin/login.py"
            data = {"act": "do_anon_auth", "server_id": server_id, "server_name": server_name}
            headers = {"User-Agent": random.sample(self.agents, 1)[0]}
            print(headers)
            # jar = aiohttp.CookieJar(unsafe=True)

            rp = requests.session()
            resp = rp.post(loginUrl,data = data,headers = headers,allow_redirects = 0)
            # print(resp.cookies)
            if resp.status_code == 302 or resp.status_code == 200:
                # self.session[server_id] = session
                self.cookies[server_id] = resp.cookies
                # print(self.cookies)
            else:
                # todo(代理ip失败计数)
                self.getCookie(server_id, server_name)
        except:
            self.getCookie(server_id, server_name)
            #proxy_fail_num = self.proxy_fail.get(self.current_proxy, 0)
            #self.proxy_fail[self.current_proxy] = int(proxy_fail_num) + 1
            # print(4444444444)

    def get_proxy(self):
        # proxy_ip = requests.get("http://122.14.222.102:5010/get/").content.decode("utf-8")
        proxy_ip = random.sample(self.proxy_pool, 1)[0]
        #fail_num = self.proxy_fail.get(proxy_ip, 0)
        # if int(fail_num)>20:
        # self.get_proxy()
        # else:
        return "http://{}".format(proxy_ip)

    def getProxyByRedis(self):
        # print(name)
        r = redis.Redis(connection_pool=self.redisPool)
        res = r.hgetall("useful_proxy")
        if len(res) > 0:
            self.proxy_pool = list(res.keys())
            # print(type(self.proxy_pool))
        # self.timer = threading.Timer(30.0, self.getProxyByRedis, [])
        # self.timer.start()

    def initRedis(self):
        try:
            # host is the redis host,the redis server and client are required to open, and the redis default port is 6379
            return redis.ConnectionPool(host='122.14.222.102', password='chenjq9988..', port=6379, db=0,
                                        decode_responses=True)
        except:
            print("could not connect to redis.")

my = parseEquipInfo()
my.parseHtmlToEquipInfo()