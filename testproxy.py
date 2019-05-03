# -*- coding: utf-8 -*-
import time
import aiohttp
import asyncio
import json
from lxml import etree
import settings
import server_list
import urllib.parse
import random
import redis
import re
from parsePet import parserPet
from parseEquip import parser
import socket
from search import selec
import traceback
from parseRole import parseRole
import math
#from roleNameConf import xyqSetting
import threading
#import server_mini
import requests


class myRun():
    def __init__(self, server_list):
        self.room = 1
        self.session = {}
        self.last_order = {}
        self.cookies = {}
        self.urls = {}
        self.new_order_list = {}
        # self.loop = asyncio.get_event_loop()
        # 总进程列表
        self.tasks = []
        # 梦幻币进程列表
        self.tasks_mhb = []
        # 订单号进程列表
        self.tasks_ordersn = []
        # 订单详情进程列表
        self.tasks_orderinfo = []
        self.servers = []
        self.currnet_server_index = 0
        self.server_name = {}
        self.new_app_equip_url = {}
        self.total_tasks = []
        self.area_name = {}
        self.agent_index = 0
        self.initServer(server_list)

        self.redisPool = self.initRedis()
        # self.getProxyByRedis()
        self.proxy_pool = []
        self.tcp_host = "122.14.200.59"
        self.tcp_port = 9503
        self.db = selec()
        self.user_data = self.db.init_data()
        self.rssed = []
        self.pojie = {}
        self.current_game_ordersn = {}
        self.role_equipid = []

        self.equip_id_url = "http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=buy_show_equip_info&equip_id={0}&server_id={1}"

        #self.proxy_fail = {}
        self.current_proxy = ""
        self.agents = self.initUserAgent()
        self.role_tasks = []
        self.timer = threading.Timer(5*60, self.get_db_data(), [])
        self.timer.start()
        self.page = 0

        self.petequip_params = {
            "level_min": "lt#equip_level#int",  # 最低等级
            "level_max": "gt#equip_level#int",  # 最高等级
            "addon_sum_min": "lt#addon_sum#int",  # 属性总和
            "equip_pos": "r_in#equip_pos#int",  # 装备类型
            "addon_lingli": "lt#addon_lingli#int",  # 灵力属性
            "addon_minjie_reduce": "gt#addon_minjie_reduce#int",  # 敏捷减少
            "addon_liliang": "lt#addon_liliang#int",  # 力量属性
            "addon_fali": "lt#addon_fali#int",  # 法力属性
            "addon_nali": "lt#addon_nali#int",  # 耐力属性
            "addon_minjie": "lt#addon_minjie#int",  # 敏捷属性
            "addon_tizhi": "lt#addon_tizhi#int",  # 体质属性
            "speed": "lt#speed#int",  # 速度属性
            "fangyu": "lt#fangyu#lt",  # 防御属性
            "mofa": "lt#mofa#int",  # 魔法属性
            "shanghai": "lt#shanghai#int",  # 伤害属性
            "hit_ratio": "lt#hit_ratio#float",  # 命中率
            "hp": "lt#hp#int",  # 气血
            "xiang_qian_level": "lt#xiang_qian_level#int",  # 镶嵌等级
            "price_min": "lt#price_fen#int",  # 最低价
            "price_max": "gt#price_fen#int",  # 最高价
            "addon_status": "eq#addon_status#str",  # 附带技能
            "kindid": "eq#kindid#int",
            "serverid": "eq#serverid#int",
        }
        self.equip_params = {
            "kindid": "l_in#kindid#int",
            "level_min": "lt#equip_level#int",
            "level_max": "gt#equip_level#int",
            "for_role_race": "in_in#for_role_race#none",
            "for_role_sex": "r_in#sex#none",
            "special_effect#and": "r_in#special_effect#int",
            "special_effect#or": "in_in#special_effect#int",
            "special_skill": "l_in#special_skill#none",
            # "suit_effect":"eq#suit_effect#int",
            "init_damage": "lt#init_damege#int",
            "init_damage_raw": "lt#init_damage_raw#int",
            "init_defence": "lt#init_defence#int",
            "init_hp": "lt#init_hp#int",
            "init_dex": "lt#init_dex#int",
            "init_wakan": "lt#init_wakan#int",
            "all_damage": "lt#all_damage#int",
            "damage": "lt#damage#int",
            "sum_attr_type": "l_in#attr_types#none",
            "sum_attr_value": "eq#sum_attr#int",
            "gem_value": "eq#gem_value#int",
            "gem_level": "lt#gem_level#int",
            "hole_num": "eq#hole_num#int",
            "price_min": "lt#price_fen#int",
            "price_max": "gt#price_fen#int",
            "serverid": "eq#server_id#int",
            "transform_skill": "eq#transform_skill#int",
            "added_status": "eq#added_status#int",
            "append_skill": "eq#append_skill#int",
            "transform_charm": "eq#transform_charm#int",
        }

        self.lingshi_params = {
            "equip_level_min": "lt#equip_level#int",
            "equip_level_max": "gt#equip_level#int",
            "added_attr_num": "lt#added_attr_num#int",
            "added_attr_repeat_num": "lt#added_attr_repeat_num#int",
            "kindid": "eq#kindid#int",
            "added_attrs": "r_in#added_attrs#none",
            "special_effect": "eq#special_effect#int",
            "price_min": "lt#price_fen#int",
            "price_max": "gt#price_fen#int",
            "jianlian_level": "lt#jianlian_level#int",
            "serverid": "eq#server_id#int",
        }

        self.role_params = {
            "school": "l_in#school#none",  # 门派
            "school_change_list": "r_in#school_change_list#none",  # 历史门派
            "race": "l_in#race#none",  # 角色
            "ori_race": "l_in#ori_race",  # 种族
            "level_min": "lt#equip_level#int",  # 最低等级
            "level_max": "gt#equip_level#int",  # 最高等级
            "price_min": "lt#price_fen#int",  # 最低价
            "price_max": "gt#price_fen#int",  # 最高价
            "sum_exp_min": "lt#sum_exp#int",  # 总经要最低
            "sum_exp_max": "gt#sum_exp#int",  # 总经验最高
            "zhuangzhi": "l_in#zhuangzhi#none",
            # 1已飞升 2已渡劫  10,20,30,40,50*，90:化圣 未飞升[0,1,2,3,10,20……，90] 飞升[1,2,3,10……，90] 渡劫 [2,3,10……，90] 化圣1 [10,20……，90]
            "shanghai": "lt#shanghai#int",  # 伤害
            "ming_zhong": "lt#ming_zhong#int",  # 命中
            # "ling_li":"lt#ling_li#int", #灵力
            "fang_yu": "lt#fang_yu#int",  # 防御
            "hp": "lt#hp#int",  # 气血
            "speed": "lt#speed#int",  # 速度
            "fa_shang": "lt#fa_shang#int",  # 法伤
            "fa_fang": "lt#fa_fang#int",  # 法防
            "qian_neng_guo": "lt#qian_neng_guo#int",  # 潜能果
            "attr_point_strategy": "r_in#attr_point_strategy#none",  # 属性点保存方案
            "expt_gongji": "lt#expt_gongji#int",  # 攻击修炼
            "max_expt_gongji": "lt#max_expt_gongji#int",  # 攻击修炼上限
            "expt_fangyu": "lt#expt_fangyu#int",  # 防御修炼
            "max_expt_fangyu": "lt#max_expt_fangyu#int",  # 防御修炼上限
            "expt_fashu": "lt#expt_fashu#int",  # 法术修炼
            "max_expt_fashu": "lt#max_expt_fashu#int",  # 法术修炼上限
            "expt_kangfa": "lt#expt_kangfa#int",  # 抗法修炼
            "max_expt_kangfa": "lt#max_expt_kangfa#int",  # 抗法修炼上限
            "expt_total": "lt#expt_total#int",  # 修炼总和
            "expt_lieshu": "lt#expt_lieshu#int",  # 猎术修炼
            "bb_expt_fashu": "lt#bb_expt_fashu#int", #宝宝法术修炼
            "bb_expt_gongji": "lt#bb_expt_gongji#int", #宝宝攻击修炼
            "bb_expt_fangyu": "lt#bb_expt_fangyu#int", #宝宝防御修炼
            "bb_expt_kangfa":"lt#bb_expt_kangfa#int", #宝宝抗法修炼
            # "school_skill_num":"tl#school_skill_num#int", #技能个数（关联查询,特例处理）
            # "school_skill_level":"tl#school_skill#school_skill_num",
            "lin_shi_fu": "lt#lin_shi_fu#int",  # 临时符技能
            # "qian_yuan_dan":"lt#qian_yuan_dan#int", #乾元丹
            "smith_skill": "lt#smith_skill#int",  # 打造熟练度
            "sew_skill": "lt#sew_skill#int",  # 裁缝熟练度
            "skill_qiang_shen": "lt#skill_qiang_shen#int",  # 强身术
            "skill_qiang_zhuang": "lt#skill_qiang_zhuang#int",  # 强壮
            "skill_shensu": "lt#skill_shensu#int",  # 神速
            "skill_ming_xiang": "lt#skill_ming_xiang#int",  # 冥想
            "skill_anqi": "lt#skill_anqi#int",  # 暗器
            "skill_dazao": "lt#skill_dazao#int",  # 打造
            "skill_caifeng": "lt#skill_caifeng#int",  # 裁缝
            "skill_qiaojiang": "lt#skill_qiaojiang#int",  # 巧匠之术
            "skill_lianjin": "lt#skill_lianjin#int",  # 炼金
            "skill_yangsheng": "lt#skill_yangsheng#int",  # 养身之道
            "skill_pengren": "lt#skill_pengren#int",  # 烹饪技巧
            "skill_zhongyao": "lt#skill_zhongyao#int",  # 中药医理
            "skill_lingshi": "lt#skill_lingshi#int",  # 灵石技巧
            "skill_jianshen": "lt#skill_jianshen#int",  # 健身术
            "skill_taoli": "lt#skill_taoli#int",  # 逃离技巧
            "skill_zhuibu": "lt#skill_zhuibu#int",  # 追捕技巧
            "skill_ronglian": "lt#skill_ronglian#int",  # 熔炼
            "skill_cuiling": "lt#skill_cuiling#int",  # 淬灵之术
            "skill_danyuan": "lt#skill_danyuan#int",  # 丹元济会
            "skill_bianhua": "lt#skill_bianhua#int",  # 变化之术
            "skill_xianling": "lt#skill_xianling#int",  # 仙灵店铺
            "skill_jianzhu": "lt#skill_jianzhu#int",  # 建筑
            "skill_miaoshou": "lt#skill_miaoshou#int",  # 妙手空空
            "skill_huoyan": "lt#skill_huoyan#int",  # 火眼金睛
            "skill_baoshi": "lt#skill_baoshi#int",  # 宝石工艺
            "skill_qimen": "lt#skill_qimen#int",  # 奇门遁甲
            "skill_gudong": "lt#skill_gudong#int",  # 股东评估
            "skill_tiaoxi": "lt#skill_tiaoxi#int",  # 调息
            "skill_dazuo": "lt#skill_dazuo#int",  # 打坐
            "skill_hanmo": "lt#skill_hanmo#int",  # 翰墨
            "skill_danqing": "lt#skill_danqing#int",  # 丹青
            # "max_weapon_shang_hai":"lt#max_weapon_shang_hai#int", #携带武器总伤
            # "max_weapon_damage":"lt#max_weapon_damage#int", #携带武器伤害(加宝石伤害，不含命中)
            # "max_weapon_init_damage":"lt#max_weapon_init_damage#int", #携带武初伤（含命中）
            # "max_weapon_init_damage_raw":"lt#max_weapon_init_damage_raw#int", #携带武器初伤（不含命中）
            # "max_necklace_ling_li":"lt#max_necklace_ling_li#int", #总灵力
            # "max_necklace_init_wakan":"lt#max_necklace_init_wakan#int", #初灵力
            # "equip_level_min":"lt#equip_level#int", #装备等级区间（下限）
            # "equip_level_max":"gt#equip_level#int", #下限
            # "teji_list_or":"in_in#teji_list#none", #特技(满足一种)
            # "teji_list_and":"r_in#teji_list#none", #都满足(teji_match_all=1)
            # "texiao_list_or":"in_in#texiao_list#none", #特效（满足一种）
            # "texiao_list_and":"r_in#texiao_list#none", #都满足(texiao_match_all=1)
            # "equip_duanzao_attr_lv_10":"tl#equip_duanzao#none", #特例处理
            # "equip_duanzao_attr_lv_11": "tl#equip_duanzao#none",  # 特例处理
            # "equip_duanzao_attr_lv_12": "tl#equip_duanzao#none",  # 特例处理
            # "equip_duanzao_attr_lv_13": "tl#equip_duanzao#none",  # 特例处理
            # "equip_duanzao_attr_lv_14": "tl#equip_duanzao#none",  # 特例处理
            # "equip_duanzao_attr_lv_15": "tl#equip_duanzao#none",  # 特例处理
            # "equip_duanzao_attr_lv_16": "tl#equip_duanzao#none",  # 特例处理
            # "equip_duanzao_attr_lv_17": "tl#equip_duanzao#none",  # 特例处理
            "xiangrui_list#or": "in_in#xiangrui_list#none",  # 满足一种（祥瑞）#名字
            "xiangrui_list#and": "r_in#xiangrui_list#none",  # xiangrui_match_all=1 都满足
            "limit_clothes#or": "in_in#limit_clothes#none",  # limit_clothes_logic or 满足一种 12512,12513
            "limit_clothes#and": "r_in#limit_clothes#none",  # limit_clothes_logic and 都满足
            "xingjia_bi":"lt#xingjia_bi#int",
            "server_name":"l_in#server_name#none", #服务器
        }

        # 搜索条件设置
        self.pet_params = {'skill': 'r_in#all_skill#null', 'type': 'l_in#type#str', 'is_baobao': 'eq#is_baobao#int',
                           'level_min': 'lt#equip_level#int', 'level_max': 'gt#equip_level#int',
                           'skill_num': 'lt#skill_num#int',
                           'attack_aptitude': 'lg#attack_aptitude#int', 'defence_aptitude': 'lt#defence_aptitude#int',
                           'physical_aptitude': 'lg#physical_aptitude#int',
                           'speed_aptitude_min': 'lg#speed_aptitude#int',
                           'speed_aptitude_max': 'gt#speed_aptitude#int', 'price_min': 'lt#price_fen#int',
                           'price_max': 'gt#price_fen#int',
                           'max_blood': 'lt#blood#int', 'attack': 'lt#attack#int', 'defence': 'lt#defence#int',
                           'speed_min': 'lt#speed#int', 'speed_max': 'gt#speed#int', 'wakan': 'lt#wakan#int',
                           'lingxing': 'lt#lingxing#int', 'growth': 'lt#growth_b#int',
                           'magic_aptitude': 'lt#magic_aptitude#int', 'serverid': 'eq#serverid#int'}

    def getProxyByRedis(self):
        # print(name)
        r = redis.Redis(connection_pool=self.redisPool)
        res = r.hgetall("useful_proxy")
        if len(res) > 0:
            proxys = []
            for key in res.keys():
                print(res[key])
                if int(res[key]) != 0:
                    r.hdel("useful_proxy",key)
                else:
                    proxys.append(key)
            self.proxy_pool = proxys
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

    def get_db_data(self):
        print("初始化删选数据")
        self.user_data = selec().init_data()
        self.timer = threading.Timer(5*60, self.get_db_data)
        self.timer.start()


    # 开服时间表
    def kaifu(self):
        import requests
        content = requests.get("https://xyq.netease.com/thread-1302818-1-1.html?refer_site=chatbot")
        content.encoding = 'gb2312'
        html = etree.HTML(content.text)
        trs = html.xpath("//table[@class='t_table']/tr")
        # print(trs)
        num = 0
        server = {}
        for li in trs:
            num += 1
            if num > 1:
                td_num = len(li.xpath("./td/text()"))
                # print(td_num)
                td_text = li.xpath("./td/text()")
                # print(td_text)

                if td_num == 3:
                    # print(td_text[2].find('-')==-1)
                    if (td_text[2].find('-') == -1):
                        break
                    server[td_text[0]] = math.floor(
                        (int(time.time()) - int(time.mktime(time.strptime(td_text[2], "%Y-%m-%d")))) / (
                                3600 * 24 * 365))
                    if len(server) == 0:
                        break
                if td_num == 2:
                    print(td_text)
        return server
                # server_list.append(server)


    def getServerMhb(self, fetch_num=20):
        try:
            urls = {}
            servers = self.servers[self.currnet_server_index:(self.currnet_server_index + fetch_num)]
            now = int(time.time())
            for i in servers:
                isplit = i.split("|")

                # print((now-int(isplit[2])))
                # dectime = int(isplit[3]) - (now - int(isplit[2]))
                # urls[i] = "https://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&act=recommd_by_role&server_id={1}&areaid=3&server_name={2}&page=1&kindid=23&view_loc=equip_list&count=30&order_by=unit_price%20ASC".format(str(now),isplit[0],urllib.parse.quote(isplit[1]))
                urls[
                    i] = "https://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&act=recommd_by_role&server_id={1}&server_name={2}&page=1&query_order=unit_price+ASC&kindid=23&view_loc=equip_list&count=30".format(
                    str(now), isplit[0], urllib.parse.quote(isplit[1]))
            self.currnet_server_index += fetch_num
            if self.currnet_server_index >= len(self.servers):
                self.currnet_server_index = 0
            # print(urls)
            url_list = []
            #ti = int(time.time())
            dict_my = {
                "459|2008|1547983917|120": "https://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&act=recommd_by_role&server_id=459&server_name=2008&page=1&query_order=unit_price+ASC&kindid=23&view_loc=equip_list&count=30".format(now),
                "554|兰亭序|1547983917|120": "https://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&act=recommd_by_role&server_id=554&server_name=%E5%85%B0%E4%BA%AD%E5%BA%8F&page=1&query_order=unit_price+ASC&kindid=23&view_loc=equip_list&count=30".format(now)}
            for index, value in dict_my.items():
                urls[index] = value
            for index, value in urls.items():
                # 更新时间，防止重复获取
                url_list.append(self.updateServers(index, value))
            #print(url_list)
            return url_list
        except:
            traceback.print_exc()

    # 更新服务器信息
    def updateServers(self, index, url):
        # 更新时间
        urls = {}
        index_split = index.split("|")
        #self.servers.remove(index)
        current_time = int(time.time())
        new_key = '|'.join('%s' % id for id in [index_split[0], index_split[1], current_time, index_split[3]])
        # print(new_key)
        #self.servers.append(new_key)
        urls[new_key] = url
        # print(urls)
        return urls

    # 初始化user-agent
    def initUserAgent(self):
        result = []
        with open('user_agents.txt', 'r') as f:
            for line in f:
                # print(line)
                result.append(line.strip('\n'))
        return result

    # 初始化所有服务器
    def initServer(self, server_list):
        all_server = []
        for i in server_list:
            servers = server_list[i][1]
            # 大区
            area_name = server_list[i][0][0]
            for k in servers:
                self.server_name[k[0]] = k[1]
                self.area_name[k[0]] = area_name
                all_server.append('|'.join(
                    '%s' % id for id in [k[0], k[1], int(time.time()) - 2 * 60, settings.TIMER_SERVER_MHB * 60]))
        # print(all_server)
        self.servers = all_server
        # print(self.server_name)

    def get_proxyip(self):
        # proxy_ip = requests.get("http://122.14.222.102:5010/get/").content.decode("utf-8")
        proxy_ip = random.sample(self.proxy_pool, 1)[0]
        #fail_num = self.proxy_fail.get(proxy_ip, 0)
        # if int(fail_num)>20:
        # self.get_proxy()
        # else:
        return {"http":proxy_ip}


    async def get_proxy(self):
        # proxy_ip = requests.get("http://122.14.222.102:5010/get/").content.decode("utf-8")
        proxy_ip = random.sample(self.proxy_pool, 1)[0]
        #fail_num = self.proxy_fail.get(proxy_ip, 0)
        # if int(fail_num)>20:
        # self.get_proxy()
        # else:
        return "http://{}".format(proxy_ip)

    # 获取网页（文本信息）
    async def fetch(self, session, url):
        proxy_id = await self.get_proxy()
        async with session.get(url, proxy="http://{}".format(proxy_id)) as response:
            return await response.text(encoding='gb18030')

    # 获取cookie
    async def getCookie(self, server_id, server_name):
        try:
            loginUrl = "https://xyq.cbg.163.com/cgi-bin/login.py"
            data = {"act": "do_anon_auth", "server_id": server_id, "server_name": server_name}
            # headers = {"User-Agent": random.sample(self.agents,1)[0]}
            headers = await self.randAgent()
            # jar = aiohttp.CookieJar(unsafe=True)
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                proxy_ip = await self.get_proxy()
                async with session.post(loginUrl, data=data, headers=headers, proxy=proxy_ip, timeout=2) as resp:
                    # print(resp.cookies)
                    if resp.status == 302 or resp.status == 200:
                        # self.session[server_id] = session
                        self.cookies[server_id] = resp.cookies
                        # print(self.cookies)
                    else:
                        #proxy_fail_num = self.proxy_fail.get(self.current_proxy, 0)
                        #self.proxy_fail[self.current_proxy] = int(proxy_fail_num) + 1
                        await self.getCookie(server_id, server_name)
        except:
            # print(server_id)
            #proxy_fail_num = self.proxy_fail.get(self.current_proxy, 0)
            #self.proxy_fail[self.current_proxy] = int(proxy_fail_num) + 1
            await self.getCookie(server_id, server_name)
            # print(4444444444)



    # json接口不需要cookie
    async def getMhb(self, url, server_id, server_name, server_info_key):
        headers = await self.randAgent()
        proxy_ip = await self.get_proxy()
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                async with session.get(url, headers=headers, proxy=proxy_ip, timeout=2) as rp:
                   if rp.status == 200:
                        json_mhb = await rp.text()
                        # print(json_mhb)
                        await self.parser_mhb_api(json_mhb, server_id, server_info_key=server_info_key)
                   else:
                        # 请求失败时重新加入请求队列
                        self.urls[server_info_key].insert(0, url)
        except:
            return False

    # json接口不需要cookie
    async def getMhb_def(self, url, server_id, server_name, server_info_key):
        # print(url)
        # agent = await self.randAgent()
        # agent = {"User-Agent": random.sample(self.agents, 1)[0]}
        # print(agent)
        headers = await self.randAgent()
        proxy_ip = await self.get_proxy()
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                async with session.get(url, headers=headers, proxy=proxy_ip, timeout=2) as rp:
                    if rp.status == 302:
                        # cookie失效，重新匿名登录获取cookie
                        await self.getCookie(server_id, server_name)
                        await self.getMhb(url, server_id, server_name, server_info_key)
                    elif rp.status == 200:
                        json_mhb = await rp.text()
                        # print(json_mhb)
                        await self.parser_mhb_api(json_mhb, server_id, server_info_key=server_info_key)
                    else:
                        # 请求失败时重新加入请求队列
                        self.urls[server_info_key].insert(0, url)
        except:
            # print(555555)
            # proxy_fail_num = self.proxy_fail.get(self.current_proxy, 0)
            # self.proxy_fail[self.current_proxy] = int(proxy_fail_num) + 1
            return False

    def getAgent(self):
        index = self.agent_index
        if index < len(self.agents):
            self.agent_index += 1
            if self.agent_index >= len(self.agents) - 1:
                self.agent_index = 0
        else:
            self.agent_index = 0
        agent = {"User-Agent": self.agents[index]}
        # print(agent)
        return agent

    # 随机获取一个user-agent
    async def randAgent(self):
        index = self.agent_index
        if index < len(self.agents):
            self.agent_index += 1
            if self.agent_index >= len(self.agents) - 1:
                self.agent_index = 0
        else:
            self.agent_index = 0
        agent = {"User-Agent": self.agents[index]}
        # print(agent)
        return agent

    # 解析具体数据（梦幻币列表）
    async def parser_mhb_api(self, str, server_id, **args):
        json_mhb = json.loads(str)
        status = json_mhb.get('status', 0)
        if status == 1:
            mhb_list = json_mhb['equips']
            # print(json_mhb)
            last_order_info = self.last_order.get(server_id, 0)
            # 无历史最终订单信息
            if last_order_info == 0:
                #print("无历史最终订单信息____________________________________________")
                min_euqipid = 0
                max_euqipid = 0
                mhb_list_temp = []
                mhb_equip_ordersn = {}
                mhb_equip_ordersn_time = {}
                for i in mhb_list:
                    equipid = i['equipid']
                    game_ordersn = i['game_ordersn']
                    nowtime = int(time.time())

                    splits_game_ordersn = re.split("_", game_ordersn)
                    # print(splits_game_ordersn)
                    game_ordersn_time = int(splits_game_ordersn[1])
                    mhb_equip_ordersn[equipid] = game_ordersn
                    mhb_equip_ordersn_time[equipid] = game_ordersn_time
                    # print(nowtime - game_ordersn_time)
                    if nowtime - game_ordersn_time < settings.TIMER_MHB * 60:
                        if min_euqipid == 0 or int(equipid) < min_euqipid:
                            min_euqipid = int(equipid)
                        if max_euqipid == 0 or int(equipid) > max_euqipid:
                            max_euqipid = int(equipid)
                        mhb_list_temp.append(equipid)
                if max_euqipid != 0 and min_euqipid != max_euqipid:
                    # 生成equip订单列表
                    await self.sendEquipList(server_id, min_euqipid, max_euqipid, mhb_list_temp)

                if max_euqipid != 0:
                    self.last_order[server_id] = "|".join('%s' % id for id in
                                                      [mhb_equip_ordersn[max_euqipid], max_euqipid,
                                                       mhb_equip_ordersn_time[max_euqipid]])
                    #self.current_game_ordersn[server_id] = mhb_equip_ordersn[max_euqipid]
                    #print(self.last_order[server_id])
            else:
                last_order_info_split = last_order_info.split("|")
                # print(last_order_info+ "____________________________________________________")
                min_euqipid = int(last_order_info_split[1])
                max_euqipid = int(last_order_info_split[1])
                mhb_list_temp = []
                mhb_equip_ordersn = {}
                mhb_equip_ordersn_time = {}
                # print("梦幻币列表…………………………………………………………………………………………………………………………")
                # print(mhb_list)
                # equipids = []
                for i in mhb_list:
                    equipid = i['equipid']
                    game_ordersn = i['game_ordersn']
                    nowtime = int(time.time())
                    # if game_ordersn and equipid:
                    splits_game_ordersn = re.split("_", game_ordersn)
                    game_ordersn_time = int(splits_game_ordersn[1])
                    mhb_equip_ordersn[equipid] = game_ordersn
                    mhb_equip_ordersn_time[equipid] = game_ordersn_time
                    # print("当前最新equip_id:{0}个当前最大equip_id:{1}".format(equipid,max_euqipid))
                    if nowtime - game_ordersn_time <= settings.TIMER_MHB * 60 and int(equipid) > max_euqipid:
                        max_euqipid = int(equipid)
                        mhb_list_temp.append(equipid)
                # print("无最新订单信息{0}和老订单{1}".format(max_euqipid,last_order_info_split[1]))
                if max_euqipid != int(last_order_info_split[1]):
                    self.last_order[server_id] = "|".join('%s' % id for id in
                                                          [mhb_equip_ordersn[max_euqipid], max_euqipid,
                                                           mhb_equip_ordersn_time[max_euqipid]])
                    #self.current_game_ordersn[server_id] = mhb_equip_ordersn[max_euqipid]
                    await self.sendEquipList(server_id, min_euqipid, max_euqipid, mhb_list_temp)
                else:
                    # 更新服务器获取频率(降频)
                    #server_info_key = args.get('server_info_key', 0)
                    #极限破解
                    last_order_info_split = last_order_info.split("|")
                    # print(last_order_info+ "____________________________________________________")
                    max_euqipid = int(last_order_info_split[1])
                    equipid = max_euqipid + 1
                    # print("未获取到最新订单信息")
                    # self.jixian(server_id,equipid)
                    # print(server_info_key)
                    # if server_info_key != 0:
                    # server_info_key_split = server_info_key.split("|")
                    # if int(server_info_key_split[3]) < 300:
                    # pinlv = int(server_info_key_split[3]) + settings.TIMER_SERVER_DEC
                    # else:
                    # pinlv = server_info_key_split[3]
                    # current_time = int(time.time())
                    # self.servers.remove(server_info_key)
                    # self.servers.append("|".join('%s' % id for id in[server_info_key_split[0], server_info_key_split[1], current_time,pinlv]))
    def jixian(self,server_id,equipid):
        try:
            print("开始极限破解！")
            print(server_id)
            hearders = self.getAgent()
            req = requests.session()
            req.keep_alive = False
            loginUrl = "https://xyq.cbg.163.com/cgi-bin/login.py"
            data = {"act": "do_anon_auth", "server_id": server_id}
            proxies = self.get_proxyip()
            resu = req.post(loginUrl,data=data,headers=hearders,proxies=proxies,allow_redirects=1,timeout=2)
            if resu.status_code==200 or resu.status_code==302 or resu.status_code==303:
                url = self.equip_id_url.format(equipid, server_id)
                res = req.get(url, headers=hearders,proxies=proxies,allow_redirects=1,timeout=2)
                if res.status_code==200:
                    res.encoding = 'gbk'
                    orderHtml = res.text
                    p1 = "\"game_ordersn\" : \"[0-9_]+\""
                    # p1 = "var reonsale_identify = \"[0-9a-zA-Z]+\""
                    pattern1 = re.compile(p1)
                    match = pattern1.findall(orderHtml)
                    # print(match)
                    if len(match) > 0:
                        # print(111111)
                        if equipid not in self.rssed:
                            if len(self.rssed) < 200:
                                self.rssed.append(equipid)
                            else:
                                self.rssed.pop(0)
                                self.rssed.append(equipid)
                            game_ordersn = eval((match[0].split(":")[1]).strip())

                            last_order_info = self.last_order.get(server_id, 0)
                            last_order_info_split = re.split("\|", last_order_info)

                            if int(equipid) > int(last_order_info_split[1]) > 1:
                                self.last_order[server_id] = "|".join('%s' % id for id in
                                                                      [game_ordersn,
                                                                       equipid, int(time.time())])

                            self.parseHtmlToEquipInfo(orderHtml)
                    else:
                        print("终止破解")
                    req.close()
        except:

            traceback.print_exc()





    # 生成最新订单列表
    async def sendEquipList(self, server_id, min_equip, max_equip, not_in_list):
        i = 0
        num = int(max_equip) - int(min_equip)
        new_order_list = self.new_order_list.get(server_id, [])
        while i < num:
            i += 1
            temp_equipid = min_equip + i
            if temp_equipid not in not_in_list:
                new_order_list.append(temp_equipid)
        if len(new_order_list) > 0:
            last_new_orser_list = self.new_order_list.get(server_id, [])
            if len(last_new_orser_list) == 0:
                self.new_order_list[server_id] = new_order_list
            else:
                self.new_order_list[server_id].extend(new_order_list)

    # 任务收集
    def task_manager(self):
        try:
            # 获取梦幻币任务
            init_mhb_url = self.getServerMhb(20)
            tasks_mhb = []
            if len(init_mhb_url) > 0:
                for it in init_mhb_url:
                    # print(it)
                    # print(list(it.values())[0])
                    tasks_mhb.append(asyncio.ensure_future(
                        self.getMhb(list(it.values())[0], list(it.keys())[0].split("|")[0],
                                    list(it.keys())[0].split("|")[1], server_info_key=list(it.keys())[0])))
            num = 0
            tasks_ordersn = []
            # print(self.new_order_list)
            for k, items in self.new_order_list.items():
                # print(items)
                if num >= 40:
                    break
                if len(items) > 0:
                    for i in range(len(items) - 1, -1, -1):
                        # print(items[i])
                        # print(num)
                        num += 1
                        # print(num)
                        tasks_ordersn.append(asyncio.ensure_future(self.getGameOrderSn(k, items[i])))
                        self.new_order_list[k].remove(items[i])
                        if num >= 40:
                            break
                    # print(items)
            num = 0
            tasks_orderinfo = []
            for k, items in self.new_app_equip_url.items():
                if len(items) > 0:
                    for v in items:
                        num += 1
                        self.new_app_equip_url[k].remove(v)
                        tasks_orderinfo.append(asyncio.ensure_future(self.getOrderInfo(k, v)))
                        if num >= 40:
                            break
            #self.getRoleList()
            role_tasks = []
            nw = int(time.time())
            urls = [
                'http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&school=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15&act=recommd_by_role&page=1&order_by=expire_time%20DESC&count=15&search_type=overall_search_role'.format(
                    nw),
                'http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&school=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15&act=recommd_by_role&page=2&order_by=expire_time%20DESC&count=15&search_type=overall_search_role'.format(
                    nw),
                'http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&school=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15&act=recommd_by_role&page=3&order_by=expire_time%20DESC&count=15&search_type=overall_search_role'.format(
                    nw),
                'http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&school=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15&act=recommd_by_role&page=4&order_by=expire_time%20DESC&count=15&search_type=overall_search_role'.format(
                    nw),
                'http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&school=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15&act=recommd_by_role&page=5&order_by=expire_time%20DESC&count=15&search_type=overall_search_role'.format(
                    nw)
            ]
            #self.page = 0
            for url in [urls[self.page]]:
                self.page += 1
                if self.page==5:
                    self.page = 0
                print(url)
                role_tasks.append(asyncio.ensure_future(self.pushRole(url)))
            self.tasks = tasks_mhb + tasks_ordersn + tasks_orderinfo + role_tasks
        except:
            print(9999999)

    # def getRoleList(self):
    #     nw = int(time.time())
    #     urls = ['http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&school=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15&act=recommd_by_role&page=1&order_by=expire_time%20DESC&count=15&search_type=overall_search_role'.format(nw),
    #            'http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&school=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15&act=recommd_by_role&page=2&order_by=expire_time%20DESC&count=15&search_type=overall_search_role'.format(nw),
    #            'http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?_={0}&school=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15&act=recommd_by_role&page=3&order_by=expire_time%20DESC&count=15&search_type=overall_search_role'.format(nw)]
    #     for url in urls:
    #         self.role_tasks.append(asyncio.ensure_future(self.pushRole(url)))
        #return tasks
    async def pushRole(self,url):
        headers = await self.randAgent()
        proxy_ip = await self.get_proxy()
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                async with session.post(url, headers=headers, proxy=proxy_ip, timeout=2) as rp:
                    #print(rp.status)
                    if rp.status == 200:
                        roles = await rp.text()
                        roleInfo = json.loads(roles)
                        if roleInfo.get("status",0) == 1:
                            roleList = roleInfo['equips']
                            for li in roleList:
                                if li['equipid'] not in self.role_equipid:
                                    if len(self.role_equipid) < 300:
                                        self.role_equipid.append(li['equipid'])
                                    else:
                                        self.role_equipid.pop(0)
                                        self.role_equipid.append(li['equipid'])
                                    merge_info = {}
                                    merge_info['server_name'] = li['server_name']
                                    merge_info['kaifu'] = settings.KAIFU.get(li['server_name'],0)
                                    merge_info['area_name'] = li['area_name']
                                    merge_info['selling_time_v'] = li['selling_time']
                                    merge_info['selling_time'] = li['selling_time']
                                    merge_info['create_time'] = li['create_time']
                                    merge_info['equip_name'] = li['equip_name']
                                    merge_info['serverid'] = li['serverid']
                                    merge_info['server_id'] = li['serverid']
                                    merge_info['price'] = li['price']
                                    merge_info['equipid'] = li['equipid']
                                    merge_info['game_ordersn'] = li['game_ordersn']
                                    merge_info['equip_level'] = li['equip_level']
                                    role_info = await parseRole().RoleInfoParser(li['desc'],merge_info,servertime='')

                                    # 角色推送
                                    await self.tuisong('role', role_info)
                    await rp.close()

        except:
            print("获取角色数据超时！")
            #traceback.print_exc()




    # 开始异步执行
    def run(self):
        try:
            self.getProxyByRedis()
            self.task_manager()
            if len(self.tasks):
                loop = asyncio.get_event_loop()
                tasks = asyncio.gather(*(self.tasks))
                loop.run_until_complete(tasks)

        except KeyError:
            print("字典键异常")
            traceback.print_exc()
            # print(tasks.result().count())
        except IndexError:
            print("索引异常")
            traceback.print_exc()
        except:
            #traceback.print_exc()
            print("其他异常")

    # 获取订单详情
    async def getOrderInfo(self, server_id, game_ordersn):
        print(game_ordersn)

    # 获取订单game_ordersn
    async def getGameOrderSn_cookie(self, server_id, equipid):
        #cookies = self.cookies.get(server_id, "none")
        #server_name = self.server_name.get(int(server_id), 0)
        url = self.equip_id_url.format(equipid, server_id)
        # if server_name == 0:
        #     # return

        loginUrl = "https://xyq.cbg.163.com/cgi-bin/login.py"
        data = {"act": "do_anon_auth", "server_id": server_id}
        # headers = {"User-Agent": random.sample(self.agents,1)[0]}
        headers = await self.randAgent()
        # jar = aiohttp.CookieJar(unsafe=True)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            proxy_ip = await self.get_proxy()
            async with session.post(loginUrl, data=data, headers=headers, proxy=proxy_ip, timeout=2) as resp:
                # print(resp.cookies)
                if resp.status == 302 or resp.status == 200:
                    # print(proxy_ip)
                    cookies = resp.cookies
                    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False),
                                                     cookies=cookies) as session:
                        async with session.get(url, headers=headers, proxy=proxy_ip, timeout=2) as rp:
                            # print(rp)

                            if rp.status == 200:
                                orderHtml = await rp.text(encoding='gbk')
                                # html = etree.HTML(orderHtml)
                                # print(9999988888)
                                p1 = "\"game_ordersn\" : \"[0-9_]+\""
                                # p1 = "var reonsale_identify = \"[0-9a-zA-Z]+\""
                                pattern1 = re.compile(p1)
                                match = pattern1.findall(orderHtml)
                                # print(match)
                                if len(match) > 0:
                                    # print(111111)
                                    if equipid not in self.rssed:
                                        if len(self.rssed) < 200:
                                            self.rssed.append(equipid)
                                        else:
                                            self.rssed.pop(0)
                                            self.rssed.append(equipid)
                                        # game_ordersn = eval((match[0].split(":")[1]).strip())
                                        # self.current_game_ordersn[server_id] =  game_ordersn
                                        await self.parseHtmlToEquipInfo(orderHtml)
                                    else:
                                        print("{0}已经推送过了**************".format(equipid))
                                    # self.new_app_equip_url[server_id].append(eval((match[0].split(":")[1]).strip()))
                                    # print()
                                else:
                                    #await self.getCookie(server_id, server_name)
                                    await self.getGameOrderSn(server_id, equipid)
                            else:
                                await self.getGameOrderSn(server_id, equipid)






    # 获取订单game_ordersn
    async def getGameOrderSn(self, server_id, equipid):
        cookies = self.cookies.get(server_id, "none")
        server_name = self.server_name.get(int(server_id), 0)
        url = self.equip_id_url.format(equipid, server_id)
        if server_name == 0:
            return
        # try:
        if cookies != 'none':
            # agent = await self.randAgent()
            # agent = {"User-Agent": random.sample(self.agents, 1)[0]}
            # headers = agent if agent else {
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
            headers = await self.randAgent()
            proxy_ip = await self.get_proxy()
            # print(proxy_ip)
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False),
                                             cookies=cookies) as session:
                async with session.get(url, headers=headers, proxy=proxy_ip, timeout=2) as rp:
                    # print(rp)
                    if rp.status == 302:
                        # cookie失效，重新匿名登录获取cookie
                        await self.getCookie(server_id, server_name)
                        await self.getGameOrderSn(server_id, equipid)
                    elif rp.status == 200:
                        orderHtml = await rp.text(encoding='gbk')
                        # html = etree.HTML(orderHtml)
                        # print(9999988888)
                        p1 = "\"game_ordersn\" : \"[0-9_]+\""
                        # p1 = "var reonsale_identify = \"[0-9a-zA-Z]+\""
                        pattern1 = re.compile(p1)
                        match = pattern1.findall(orderHtml)
                        # print(match)
                        if len(match) > 0:
                            # print(111111)
                            if equipid not in self.rssed:
                                if len(self.rssed) < 200:
                                    self.rssed.append(equipid)
                                else:
                                    self.rssed.pop(0)
                                    self.rssed.append(equipid)
                                #game_ordersn = eval((match[0].split(":")[1]).strip())
                                #self.current_game_ordersn[server_id] =  game_ordersn
                                await self.parseHtmlToEquipInfo(orderHtml)
                            else:
                                print("{0}已经推送过了**************".format(equipid))
                            # self.new_app_equip_url[server_id].append(eval((match[0].split(":")[1]).strip()))
                            # print()
                        else:
                            await self.getCookie(server_id, server_name)
                            await self.getGameOrderSn(server_id, equipid)

                            # self.new_order_list[server_id].append(equipid)
                            # print("未匹配到game_ordersn!")
                            # print(orderHtml)
                            # print(22222)
                            # if orderHtml.find("为了您的帐号安全，请登录之后继续访问") > -1:
                            #     await self.getCookie(server_id, server_name)
                            #     await self.getGameOrderSn(server_id, equipid)
                            #
                            # if orderHtml.find("登录超时") > -1:
                            #     await self.getCookie(server_id, server_name)
                            #     await self.getGameOrderSn(server_id, equipid)
                        # print(orderHtml)
                        # await self.parser_order_info(orderInfo)
        else:
            await self.getCookie(server_id, server_name)
            await self.getGameOrderSn(server_id, equipid)
        # except:
        #     print("出现异常")
        #     proxy_fail_num = self.proxy_fail.get(self.current_proxy, 0)
        #     self.proxy_fail[self.current_proxy] = int(proxy_fail_num) + 1
        #     await self.getGameOrderSn(server_id, equipid)

    async def parseHtmlToEquipInfo(self, content):
        # req = requests.session()
        # self.getCookie('459','2008')
        # content = req.get("https://xyq.cbg.163.com/cgi-bin/equipquery.py?act=buy_show_equip_info&equip_id=6237125&server_id=459",cookies = self.cookies['459'] ,headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.11.2 Chrome/65.0.3325.230 Safari/537.36"} ,allow_redirects=1)
        # content.encoding = "gb2312"
        # print(content.text)
        # html = etree.HTML(content)
        p1 = "var reonsale_identify = \"[0-9a-zA-Z]+\""
        pattern1 = re.compile(p1)
        match = pattern1.findall(content)
        if len(match) > 0:
            reonsale_identify = eval((match[0].split("=")[1]).strip())
            # print(reonsale_identify)
        else:
            reonsale_identify = ''
        # var ServerTime = '2019-01-07 23:25:27';
        p3 = "var ServerTime = \"[0-9\-:]+\""
        pattern3 = re.compile(p3)
        match3 = pattern3.findall(content)
        if len(match3) > 0:
            ServerTime = eval((match[0].split("=")[1]).strip())
            # print(reonsale_identify)
        else:
            ServerTime = ''

        p2 = "var equip = \{[^\}]*\};"
        pattern2 = re.compile(p2)
        match_equip = pattern2.findall(content)
        if len(match_equip) > 0:
            json_data = match_equip[0]
            ret = json_data[json_data.index("=") + 1:len(json_data) - 1].replace("\n", '').replace("\r", '').replace(
                "\t", "")
            rt = ret[0:ret.index("valid") - 2] + "}"
            # print(rt)
            equip = json.loads(rt)
            equip['server_name'] = self.server_name.get(equip['server_id'], '')
            #开服年份
            equip['kaifu'] = settings.KAIFU.get(equip['server_name'],0)
            equip['area_name'] = self.area_name.get(equip['server_id'], '')
            equip['create_time_v'] = equip['create_time']
            equip['selling_time_v'] = equip['selling_time']
        else:
            return False
        equip['reonsale_identify'] = reonsale_identify
        # 获取content内容
        html = etree.HTML(content)
        # 召唤兽
        cont1 = html.xpath("//textarea[@id='pet_desc']/text()")
        if len(cont1) > 0:
            myObj = parserPet()
            print("召唤兽**********************")
            # print(cont1[0])
            petinfo = await myObj.get_pet_attrs_info(cont1[0], equip)
            await self.tuisong('pet', petinfo)
            # print(petinfo)
            return
        # print(cont1)
        # 装备、灵饰、召唤兽装备
        cont2 = html.xpath("//textarea[@id='equip_desc_value']/text()")
        # print(cont2)
        # print(equip)
        if len(cont2) > 0:
            equip_type = equip['equip_type']
            kindid = equip['kindid']
            myObj = parser()
            not_in = ["4244", "4243", "4034", "3149"]
            if int(kindid) == 29:
                # if (equip_type[0:1] == 9 and len(equip_type) == 4):
                # 召唤兽装备
                equip['equip_desc'] = cont2[0]
                print("召唤兽装备***********************")
                petequip_info = await myObj.htmlToPetEquip(cont2[0], equip)
                await self.tuisong('pet_equip', petequip_info)
            # print(petequip_info)
            else:

                if ((len(equip_type) == 4 or (len(equip_type) == 5 and equip_type[0: 2] == '31')) and equip_type not in not_in and equip[
                    "equip_name"].isdigit() == False):
                    # 人物装备
                    print("人物装备*****************************")
                    equip['equip_desc'] = cont2[0]

                    # print(cont2[0])
                    equip_info = await myObj.htmlToEquip(cont2[0], equip)


                    await self.tuisong('equip', equip_info)

                elif (len(equip_type) == 5 and equip_type[0: 2] == '27'):
                    # 灵饰
                    equip['equip_desc'] = cont2[0]
                    print("灵饰*******************************")
                    lingshi_info = await myObj.htmlToLingShi(cont2[0], equip)
                    await self.tuisong('lingshi', lingshi_info)
                    # print(lingshi_info)
                elif equip['equip_name'].isdigit() == True:
                    print("角色*******************************")
                    # print(cont2[0])
                    role_info = await parseRole().RoleInfoParser(cont2[0], equip, ServerTime)
                    #print(role_info)
                    await self.tuisong('role', role_info)
            return

    # 删选条件处理
    async def userSearch(self, type, data):
        # da = json.loads(data)
        # print(data)
        # data = self.data
        # print(type)
        dat = []
        for i in data:
            if type != i['type']:
                continue
            ii = json.loads(i.get("arg", None))
            # print(ii)
            if type == 'pet':
                if ii.get("skill", None) != None:
                    ii['skill'] = [int(x) for x in re.split(',', ii.get("skill", None))]
                    # print(ii)
            elif type == 'pet_equip':
                if ii.get("equip_pos", None) != None:
                    ii['equip_pos'] = [int(x) for x in re.split(',', ii.get("equip_pos", None))]
                    # print(ii)
            elif type == 'equip':
                if ii.get("special_effect", None) != None:
                    if ii.get("special_mode", None) != None:
                        ii['special_effect#' + ii.get("special_mode", None)] = [int(x) for x in re.split(',',
                                                                                                          ii.get(
                                                                                                              "special_effect",
                                                                                                              None))]
                        ii.pop("special_mode")
                    else:
                        ii['special_effect#or'] = [int(x) for x in re.split(',', ii.get("special_effect", None))]
                if ii.get("special_skill", None) != None:
                    ii['special_skill'] = [int(x) for x in re.split(',', ii.get("special_skill", None))]
                if ii.get("kindid",None) != None:
                    ii['kindid'] = [int(x) for x in re.split(',', ii.get("kindid", None))]

            elif type == 'lingshi':
                added_attrs = []
                if ii.get("added_attr1", None) != None:
                    added_attrs.append(int(ii.get("added_attr1", None)))
                if ii.get("added_attr2", None) != None:
                    added_attrs.append(int(ii.get("added_attr2", None)))
                if ii.get("added_attr3", None) != None:
                    added_attrs.append(int(ii.get("added_attr3", None)))
                ii['added_attrs'] = added_attrs
            elif type == 'role':
                if ii.get("school_change_list", None) != None:
                    ii['school_change_list'] = re.split(",", ii['school_change_list'])
                if ii.get("school", None) != None:
                    ii['school'] = [int(i) for i in re.split(",", ii['school'])]
                if ii.get("race", None) != None:
                    ii['race'] = re.split(',', ii.get['race'])
                if ii.get("ori_race", None) != None:
                    ii['ori_race'] = re.split(',', ii['ori_race'])
                if ii.get("zhuangzhi", None) != None:
                    if isinstance(ii['zhuangzhi'], int) or isinstance(ii['zhuangzhi'], str):
                        ii['zhuangzhi'] = [int(ii['zhuangzhi'])]
                if ii.get("xiangrui_list", None) != None and ii.get("xiangrui_match_all", None) == None:
                    ii["xiangrui_list#or"] = re.split(",", ii["xiangrui_list"])
                elif ii.get("xiangrui_list", None) != None and ii.get("xiangrui_match_all", None) != None:
                    ii['xiangrui_list#and'] = re.split(",", ii["xiangrui_list"])
                if ii.get("limit_clothes", None) != None and ii.get("limit_clothes_logic", None) != None:
                    ii["limit_clothes#" + ii['limit_clothes_logic']] = re.split(",", ii["limit_clothes"])


            else:
                print(ii)
            i['ret'] = ii
            dat.append(i)
        # print(dat)
        return dat

    # g 过滤条件  vv 数据 params 过滤规则
    async def guolv(self, g, vv, params):
        #print(vv)
        try:
            for k, v in g.items():
                k_v = params.get(k, None)
                #print(k_v)
                if k_v != None:
                    k_v_li = re.split("#",k_v)
                    #print(k_v_li)
                    if len(k_v_li) < 3:
                        continue
                    fuhao = k_v_li[2]

                    if k_v_li[0] == 'r_in':
                        if isinstance(v,list):
                            d = [False for c in v if c not in vv.get(k_v_li[1], [])]
                        else:
                            d = (v in vv.get(k_v_li[1], []))
                        if d:
                            continue
                        else:
                            print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                            print(v)
                            print(vv.get(k_v_li[1], []))
                            return False
                    if k_v_li[0] == 'l_in':
                        if isinstance(vv.get(k_v_li[1], 0),list):
                            d = [False for c in vv.get(k_v_li[1], []) if c not in v]
                        else:
                            if fuhao == 'int':
                                tp = int(vv.get(k_v_li[1], 0))
                            else:
                                tp = vv.get(k_v_li[1], '')
                            d = (tp in v)
                        if d:
                            continue
                        else:
                            print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                            print(v)
                            print(vv.get(k_v_li[1], []))
                            #print(v)
                            #print(vv.get(k_v_li[1], []))
                            return False
                    if k_v_li[0] == 'in_in':

                        tmp = [int(val) for val in vv.get(k_v_li[1]) if int(val) in v]
                        if len(tmp) > 0:
                            continue
                        else:
                            print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                            print(v)
                            print(vv.get(k_v_li[1], []))
                            return False
                    if fuhao == 'int':
                        if k_v_li[0] == 'eq':
                            if int(vv.get(k_v_li[1], 0)) == int(v):
                                continue
                            else:
                                print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                                print(v)
                                print(vv.get(k_v_li[1], 0))
                                return False
                        if k_v_li[0] == 'lt':
                            if int(v) <= int(vv.get(k_v_li[1], 0)):
                                continue
                            else:
                                print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                                print(v)
                                print(vv.get(k_v_li[1], 0))
                                return False
                        if k_v_li[0] == 'gt':
                            if int(v) >= int(vv.get(k_v_li[1], 0)):
                                continue
                            else:
                                print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                                print(v)
                                print(vv.get(k_v_li[1], []))
                                return False
                    elif fuhao == 'float':
                        if k_v_li[0] == 'eq':
                            if float(vv.get(k_v_li[1], 0)) == float(v):
                                continue
                            else:
                                print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                                print(v)
                                print(vv.get(k_v_li[1], []))
                                return False
                        if k_v_li[0] == 'lt':
                            if float(v) <= float(vv.get(k_v_li[1], 0)):
                                continue
                            else:
                                print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                                print(v)
                                print(vv.get(k_v_li[1], []))
                                return False
                        if k_v_li[0] == 'gt':
                            if float(v) >= float(vv.get(k_v_li[1], 0)):
                                continue
                            else:
                                print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                                print(v)
                                print(vv.get(k_v_li[1], []))
                                return False
                    else:
                        if k_v_li[0] == 'eq':
                            if (vv.get(k_v_li[1], 0)) == (v):
                                continue
                            else:
                                print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                                print(v)
                                print(vv.get(k_v_li[1], []))
                                return False
                        if k_v_li[0] == 'lt':
                            if (v) <= (vv.get(k_v_li[1], 0)):
                                continue
                            else:
                                print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                                print(v)
                                print(vv.get(k_v_li[1], []))
                                return False
                        if k_v_li[0] == 'gt':
                            if (v) >= (vv.get(k_v_li[1], 0)):
                                continue
                            else:
                                print("字段：{0}对比字段:{1}不满足".format(k, k_v_li[1]))
                                print(v)
                                print(vv.get(k_v_li[1], []))
                                return False
        except KeyError:
            print("字典键异常")
            traceback.print_exc()
            # print(tasks.result().count())
        except IndexError:
            print("索引异常")
            traceback.print_exc()
        except ArithmeticError:
            print("计算异常")
            traceback.print_exc()
        except:
            print("过滤异常！")
            traceback.print_exc()
        return True

    async def tuisong(self, type, equip_info):
        if equip_info['equipid'] in self.rssed:
            print("{0}已经推送过了********".format(equip_info['equipid']))
            return False
        data = self.user_data
        # print(data)
        da = await self.userSearch(type, data)
        # print(da)
        if (type == 'equip'):
            pv = self.equip_params
        elif type == 'pet_equip':
            pv = self.petequip_params
        elif type == 'pet':
            pv = self.pet_params
        elif type == 'role':
            pv = self.role_params
        elif type == 'lingshi':
            pv = self.lingshi_params
        else:
            pv = {}


        save_types = {}

        for aa in da:
            openid = aa['openid']
            save_type = int(aa['save_type'])
            ret = aa['ret']
            if (type == 'role'):
                isbool = await self.guolv(ret, equip_info['where'], pv)
            else:
                isbool = await self.guolv(ret, equip_info, pv)


            if isbool:
                #print(save_type)
                if openid and save_type:
                    if save_types.get(openid,0) !=0:
                        if save_types.get(openid,0) > save_type:
                            save_types[openid] = save_type
                    else:
                        save_types[openid] = save_type
                    #save_types.append(save_type)
        if 1==1:
            if type == 'pet':
                print("召唤兽推送…………………………………………………………")
                tui = await self.arrToSortKeyWord_pet(equip_info)
                # print(tui)
            elif type == 'pet_equip':
                print("召唤兽装备推送*************************")
                tui = await self.arrToSortKeyWord_pet_equip(equip_info)
            elif type == 'equip':
                print("人物装备推送*****************************")
                tui = await self.arrToSortKeyWord_equip(equip_info)
            elif type == 'lingshi':
                print("灵饰推送***********************************")
                tui = await self.arrToSortKeyWord_lingshi(equip_info)
            elif type == 'role':
                print("角色推送***********************************")
                tui = await self.arrToSortKeyWord_role(equip_info)
            else:
                tui = {}
                return

            tui['save_types'] = save_types

            await self.tcp_client({'method':'tui','data':tui})


    # 数据组装（装备）
    async def arrToSortKeyWord_equip(self, v):
        first = {}
        hStr = "<font color='#9900ff'>亮点：" + v.get('highlight', '无')+"</font>"
        o_hStr = hStr
        # first['value'] = v['equip_name'] + ' ' + v['equip_level'] + '  ' +  v['area_name'] + '-' + v['server_name'] + ' ' + hStr
        first['value'] = "{0}({1}) {2}-{3} {4}".format(v['equip_name'], v['equip_level'], v['area_name'],
                                                       v['server_name'], hStr)
        str_key_word = ''
        ra = ['0', '1', '2', '3', '4', '6', '7', '8', '9']
        # print(first)
        random.shuffle(ra)
        id = "".join(ra)
        # print(id)
        str_key_word += ("<font color='green'>  附加属性: </font><p id='" + id + "' style='display: none'>" + v[
            'equip_desc'] + "</p>") if v['equip_desc'] else ' '
        str_key_word += "<div class='attribute' id='div_" + id + "'></div>"
        str_key_word += "<script type=\"text/javascript\">$(\"#div_" + id + "\").html(parse_style_info($(\"#" + id + "\").text()))</script>"
        str_key_word += o_hStr
        keyword1 = {}
        keyword1['value'] = str_key_word
        keyword1['color'] = '#008000'
        str_key_word2 = ''
        # str_key_word2 += v['price'] + '  ('+ v['selling_time']+')'
        str_key_word2 += "{0}({1})".format(v['price'], v['selling_time'])
        keyword2 = {}
        keyword2['value'] = str_key_word2
        keyword2['color'] = '#6633ff'
        # print(keyword2)

        oneData = {}
        # oneData['url'] = 'http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid='. v['serverid'].'&ordersn='. v['game_ordersn'].'&equip_refer=1#collect_panel'
        # oneData['app_url'] = 'http://xyq-m.cbg.163.com/cgi/mweb/product/detail/'. v['serverid'].'/'. v['game_ordersn'].'?equip_refer=1&from=share'
        # oneData['cross_url'] = 'http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid='. v['serverid'].'&ordersn='. v['game_ordersn'].'&equip_refer=1#collect_panel'
        # oneData['local_url'] = 'http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid='. v['serverid'].'&ordersn='. v['game_ordersn'].'&equip_refer=1#collect_panel'
        oneData['data_name'] = str_key_word2
        oneData['data_price'] = v['price']
        oneData['data_serverid'] = v['server_id']
        oneData['data_ordersn'] = v['game_ordersn']
        oneData['data_equipid'] = v['equipid']
        oneData['type'] = 'equip'  # type十分重要不能掉
        oneData['first'] = first
        oneData['keyword1'] = keyword1
        oneData['keyword2'] = keyword2
        oneData['create_time'] = v['create_time']
        # oneData['selling_time'] = int(time.mktime(time.strptime(v['selling_time_v'],"%Y-%m-%d %H:%M:%S")))
        oneData['selling_time'] = int(time.mktime(time.strptime(v['selling_time_v'], "%Y-%m-%d %H:%M:%S")))
        # oneData['selling_time'] = v['selling_time']
        oneData['reonsale_identify'] = v.get('reonsale_identify','')
        # print(oneData)
        return oneData

    # 角色推送
    async def arrToSortKeyWord_role(self, v):
            #print(v)
        #try:
            first = {}
            hStr = "亮点：<font color='#9900ff'>{0}</font>".format("|".join(v.get("highlight_attr", ['无'])))
            first['value'] = "{0}({1}{5})({6}) {2}-{3}({8}年) {4},<{7}>".format(v['basic_info']['school'], v['equip_level'], v['area_name'],
                                                              v['server_name'], hStr, v['basic_info']['role_kind_name'], v['basic_info']['sum_exp'], v['basic_info'].get('fly_status',''),v['kaifu'])

            #print(first)
            #print(v['role_xiulian'])
            str_key_word = '角色修炼:'
            str_key_word += ' '.join(['{0}:{1}'.format(xiulian['name'][0:1], xiulian['info']) for xiulian in v['role_xiulian']]) + "<br />"
            #print(first)
            str_key_word += 'BB修炼:'
            str_key_word += ' '.join(['{0}:{1}'.format(pet_ctrl['name'][0:1], pet_ctrl['grade']) for pet_ctrl in v['pet_ctrl_skill']])
            str_key_word += "师门技能：" + ",".join([str(vv['skill_grade']) for vv in v['role_skill']['school_skill']])
            str_key_word += "卖符技能：" + str(v['where'].get('lin_shi_fu',''))
            #print(str_key_word)

            keyword1 = {}
            keyword1['value'] = str_key_word + "  "
            keyword1['color'] = '#008000'
            if int(int(v['xingjia'])- math.ceil(float(v['price'])))>=0:
                showbig = 1
                str_key_word2 = "{0}(估价:<font size='18px' color='#FFD70'>{1}</font>) (性价比：{2}%)".format(v['price'],v['xingjia'],v['xingjia_bi'])
                if abs(int(int(v['xingjia'])- math.ceil(float(v['price']))))/math.ceil(float(v['price'])) >=0.5:
                    str_key_word2 = "{0}(估价:<font size='18px' color='red'>{1}</font>) (性价比：{2}%)".format(v['price'],
                                                                                                    v['xingjia'],
                                                                                                    v['xingjia_bi'])
            elif abs(int(int(v['xingjia'])- math.ceil(float(v['price']))))/math.ceil(float(v['price'])) < 0.1 :
                showbig = 1
                str_key_word2 = "{0}(估价:<font size='16px' color='green'>{1}</font>) (性价比：{2}%)".format(v['price'], v['xingjia'],
                                                                                     v['xingjia_bi'])
            else:
                showbig = 0
                str_key_word2 = "{0}(估价:<font color='black'>{1}</font>) (性价比：{2}%)".format(v['price'], v['xingjia'],
                                                                                       v['xingjia_bi'])
            cr_time = int(time.mktime(time.strptime(v['create_time'], "%Y-%m-%d %H:%M:%S")))
            se_time = int(time.mktime(time.strptime(v['selling_time_v'], "%Y-%m-%d %H:%M:%S")))
            if (abs(cr_time-se_time) < 5):
                showbig = 1
                str_key_word2 += "<font color='red'><首次上架></font>"
            else:
                str_key_word2 += "<font color='black'><重新上架></font>"
            keyword2 = {}
            keyword2['value'] = str_key_word2
            keyword2['color'] = '#6633ff'
            oneData = {}
            oneData['data_name'] = str_key_word2
            oneData['data_price'] = v['price']
            oneData['data_serverid'] = v['server_id']
            oneData['data_ordersn'] = v['game_ordersn']
            oneData['data_equipid'] = v['equipid']
            oneData['type'] = 'role'
            oneData['showbig'] = showbig if showbig else 0
            oneData['first'] = first
            oneData['keyword1'] = keyword1
            oneData['keyword2'] = keyword2
            oneData['create_time'] = v['create_time']
            # print(v['selling_time_v'])
            oneData['selling_time'] = int(time.mktime(time.strptime(v['selling_time_v'], "%Y-%m-%d %H:%M:%S")))
            oneData['reonsale_identify'] = v.get('reonsale_identify','')
            return oneData
        # except KeyError:
        #     print("字典键异常")
        #     traceback.print_exc()
        #     # print(tasks.result().count())
        # except IndexError:
        #     print("索引异常")
        #     traceback.print_exc()
        # except:
        #     print("格式化角色信息异常！")



    # 召唤兽装备
    async def arrToSortKeyWord_pet_equip(self, v):
        first = {}
        hStr = "亮点：<font color='#9900ff'>{0}</font>".format(v.get('highlight', ''))
        first['value'] = "{0}({1}) {2}-{3} {4}".format(v['equip_name'], v['equip_level'], v['area_name'],
                                                       v['server_name'], hStr)
        str_key_word = ''
        ra = ['0', '1', '2', '3', '4', '6', '7', '8', '9']
        # print(first)
        random.shuffle(ra)
        id = "".join(ra)
        str_key_word += ("<font color='green'>  附加属性: </font><p id='" + id + "' style='display: none'>" + v[
            'equip_desc'] + "</p>") if v['equip_desc'] else ' '
        str_key_word += "<div class='attribute' id='div_" + id + "'></div>"
        str_key_word += "<script type=\"text/javascript\">$(\"#div_" + id + "\").html(parse_style_info($(\"#" + id + "\").text()))</script>"
        str_key_word += "镶嵌等级：{0}".format(v.get('xiang_qian_level', '0'))

        keyword1 = {}
        keyword1['value'] = str_key_word
        keyword1['color'] = '#008000'

        # print(keyword1)
        str_key_word2 = ''
        str_key_word2 += "{0} ({1})".format(v['price'], v['selling_time'])

        keyword2 = {}
        keyword2['value'] = str_key_word2
        keyword2['color'] = '#6633ff'

        oneData = {}
        oneData['data_name'] = str_key_word2
        oneData['data_price'] = v['price']
        oneData['data_serverid'] = v['server_id']
        oneData['data_ordersn'] = v['game_ordersn']
        oneData['data_equipid'] = v['equipid']
        oneData['type'] = 'equip'
        oneData['first'] = first
        oneData['keyword1'] = keyword1
        oneData['keyword2'] = keyword2
        oneData['create_time'] = v['create_time']
        #print(v['selling_time_v'])
        oneData['selling_time'] = int(time.mktime(time.strptime(v['selling_time_v'],"%Y-%m-%d %H:%M:%S")))
        oneData['reonsale_identify'] = v['reonsale_identify']
        return oneData

    # 灵饰
    async def arrToSortKeyWord_lingshi(self, v):
        first = {}
        hStr = "亮点：<font color='#9900ff'>{0}</font>".format(v.get('highlight', ''))
        first['value'] = "{0}({1}) {2}-{3} {4}".format(v['equip_name'], v['equip_level'], v['area_name'],
                                                       v['server_name'], hStr)
        ra = ['0', '1', '2', '3', '4', '6', '7', '8', '9']
        # print(first)
        random.shuffle(ra)
        id = "".join(ra)
        str_key_word = ''
        str_key_word += ("<font color='green'>  附加属性: </font><p id='" + id + "' style='display: none'>" + v[
            'equip_desc'] + "</p>") if v['equip_desc'] else ' '
        str_key_word += "<div class='attribute' id='div_" + id + "'></div>"
        str_key_word += "<script type=\"text/javascript\">$(\"#div_" + id + "\").html(parse_style_info($(\"#" + id + "\").text()))</script>"
        str_key_word += " 精炼等级：{0}".format(v.get('jinglian_level', '0')) if v.get('jinglian_level', '0') else '0'

        keyword1 = {}
        keyword1['value'] = str_key_word
        keyword1['color'] = '#008000'

        # print(keyword1)

        str_key_word2 = ''
        str_key_word2 += "{0} ({1})".format(v['price'], v['selling_time'])

        keyword2 = {}
        keyword2['value'] = str_key_word2
        keyword2['color'] = '#6633ff'
        oneData = {}
        oneData['data_name'] = str_key_word2
        oneData['data_price'] = v['price']
        oneData['data_serverid'] = v['server_id']
        oneData['data_ordersn'] = v['game_ordersn']
        oneData['data_equipid'] = v['equipid']
        oneData['type'] = 'equip'  # type十分重要不能掉
        oneData['first'] = first
        oneData['keyword1'] = keyword1
        oneData['keyword2'] = keyword2
        oneData['create_time'] = v['create_time']
        oneData['selling_time'] = int(time.mktime(time.strptime(v['selling_time_v'], "%Y-%m-%d %H:%M:%S")))
        oneData['reonsale_identify'] = v['reonsale_identify']
        return oneData

    # 数据组装成格式化展示数据(召唤兽)
    async def arrToSortKeyWord_pet(self, v):
        first = {}
        hStr = v.get("highlight", '')
        # hStr += "  灵性值：" + v.get("jinjie", {"lx": 0}).get('lx', 0) + "  特性：" + (v.get("jinjie", {"name": "无"}).get('name', "无"))
        hStr += "  灵性值：{0}特性：{1}".format(v.get("jinjie", {"lx": 0}).get('lx', 0),
                                         v.get("jinjie", {"name": "无"}).get('name', "无"))
        # first['value'] = v['pet_name'] + "  " + v['level'] + '  ' + v['area_name'] + '-' + v['server_name'] + ' ' + hStr
        first['value'] = "{0} {1} {2}-{3} {4}".format(v['equip_name'], v['equip_level'], v.get('area_name', ''),
                                                      v.get('server_name', ''), hStr)
        tsStr = v.get("highlight", '')
        # str_key_word = '' + v.get('skill_names', '') + "<br />"
        str_key_word = '{0}<br />'.format(v.get('skill_desc', ''))
        str_key_word += '{0}<br />'.format(v['zz'])
        # print(str_key_word)
        # str_key_word.= "技能数量：".$v['skill_num']
        keyword1 = {}
        keyword1['value'] = str_key_word
        keyword1['color'] = '#008000'
        str_key_word2 = "{0}({1})".format(v['price'], v['selling_time'])
        str_key_word2 += '亮点：<font color="red">' + (tsStr if tsStr else '无') + "</font>"
        # $str_key_word2 .= '精准剩余时间:';
        keyword2 = {}
        keyword2['value'] = str_key_word2
        keyword2['color'] = '#6633ff'
        # print(keyword2)
        oneData = {}
        # oneData['url'] = 'http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid={0}&ordersn={1}&equip_refer=1#collect_panel'.format(v['serverid'],v['game_ordersn'])
        # oneData['app_url'] = 'http://xyq-m.cbg.163.com/cgi/mweb/product/detail/{0}/{1}?equip_refer=1&from=share'.format(v['serverid'],v['game_ordersn'])
        # oneData['cross_url'] = 'http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid='. $v['serverid'].'&ordersn='. $v['game_ordersn'].'&equip_refer=1#collect_panel'
        # oneData['local_url'] = 'http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid='. $v['serverid'].'&ordersn='. $v['game_ordersn'].'&equip_refer=1#collect_panel'
        oneData['data_name'] = str_key_word2
        oneData['data_price'] = v['price']
        oneData['data_serverid'] = v['server_id']
        oneData['data_ordersn'] = v['game_ordersn']
        oneData['data_equipid'] = v['equipid']
        oneData['type'] = 'pet'
        oneData['first'] = first
        oneData['keyword1'] = keyword1
        oneData['keyword2'] = keyword2
        oneData['create_time'] = v['create_time']
        # oneData['selling_time'] = int(time.mktime(time.strptime(v['selling_time_v'],"%Y-%m-%d %H:%M:%S")))
        # print(v['selling_time_v'])
        oneData['selling_time'] = int(time.mktime(time.strptime(v['selling_time_v'], "%Y-%m-%d %H:%M:%S")))
        oneData['reonsale_identify'] = v['reonsale_identify']
        # print(oneData)
        return oneData
        # 直接推送
        # oneData['time'] = time()
        # redis = getRedis()
        # redis->hSet("last_orders",v['game_ordersn'], json_encode(oneData, JSON_UNESCAPED_UNICODE))

    # 信息推送
    async def tcp_client(self, send_data=None):
        """ TCP 客户端 """
        # target_host = target_host if target_host else "www.baidu.com"
        # target_port = target_port if target_port else 80
        send_data = bytes(json.dumps(send_data, ensure_ascii=False),
                          encoding='utf-8') + b'\r\n' if send_data else b"GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n"

        # 建立一个 socket 对象
        socket.setdefaulttimeout(2)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接客户端
        client.connect((self.tcp_host, self.tcp_port))
        # 发送数据
        client.send(send_data)
        # 接收数据
        response = b''

        while True:
            res = client.recv(1024)
            response += res
            if len(res) < 1024:
                break
        # print(str(response))
        d = json.loads(response)
        client.close()
        if d.get("message", "fail") != 'success':
            print(d)
            #推送失败重新推送
            #await self.tcp_client(send_data)



my = myRun(server_list.server_data)

while True:
    #time1 = int(time.time())
    my.run()

    #print(sys.getsizeof(my))
    # print(my.new_order_list)
    # print(len(my.total_tasks))

    #time2 = int(time.time())
    # print(len(my.total_tasks)/(time2-time1))
    #print(time2-time1)
