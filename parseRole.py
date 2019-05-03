# -*- coding: utf-8 -*-
from roleNameConf import xyqSetting
import re
import json
import time
import math
import operator
import datetime
import traceback
import asyncio


class parseRole:
    def __init__(self):
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
        }
        self.RACE_INFO = {0: "", 1: "人", 2: "魔", 3: "仙"}
        self.CHINESE_NUM_CONFIG = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九", 10: "十"}
        self.ROLE_ZHUAN_ZHI_CONFIG = {0: "未飞升", 1: "飞升", 2: "渡劫"}
        self.RoleKindNameInfo = {1: "逍遥生", 2: "剑侠客", 3: "飞燕女", 4: "英女侠", 5: "巨魔王", 6: "虎头怪", 7: "狐美人", 8: "骨精灵",
                                 9: "神天兵", 10: "龙太子", 11: "舞天姬", 12: "玄彩娥", 203: "巫蛮儿", 205: "杀破狼", 209: "羽灵神",
                                 201: "偃无师", 207: "鬼潇潇", 211: "桃夭夭"}
        self.PROP_KEPT_KEYS = {"iStr": "力量", "iMag": "魔力", "iSpe": "敏捷", "iCor": "体质", "iRes": "耐力"}
        self.PROP_KEPT_KEYS_ORDER = ['iStr', 'iMag', 'iSpe', 'iCor', 'iRes']
        self.ATTR_NAME_KEEP = {"力量": "str", "魔力": "mag", "速度": "spe", "体质": "cor", "耐力": "res", "力魔": "strmag",
                               "力敏": "strspe", "力体": "strcor", "力耐": "strres", "魔敏": "magspe", "敏体": "specor",
                               "敏耐": "speres", "体耐": "corres", "耐体": "corres"}
        self.LI_SHI_FU_SKILL = ["文韬武略", "佛光普照", "神道无边", "香飘兰麝", "天罡气", "龙附", "修仙术", "金刚经", "牛逼神功", "拘魂术", "狂兽诀", "蛛丝阵法",
                                "探奥索隐", "混元神功", "神木恩泽", "金刚之躯", "藻光灵狱", "啸傲"]
        self.ResUrl = ''
        self.result = {}
        self.result['where'] = {}
        # self.result['highlight'] = []
        self.serverId = ''
        self.xyqConf = xyqSetting()
        # self.highClothes = ['青花瓷','冰寒绡','落星织','冰雪玉兔','夜之幽兰','夜之孤煞','铃儿叮当','云龙梦']
        self.highClothes = ['青花瓷', '冰寒绡']
        self.highRider = ['天使猪猪', '猪猪小侠', '神行小驴', '玉脂福羊', '七彩小驴', '粉红小驴', '甜蜜猪猪', '萌动猪猪']
        self.result['highlight_attr'] = []
        self.schoolSkiGold = [6, 12, 19, 28, 38, 51, 67, 86, 110, 139, 174, 216, 266, 325, 393, 472, 563, 667, 786, 919,
                              1070, 1238, 1426, 1636, 1868, 2124, 2404, 2714, 3050, 3420, 3820, 4255, 4725, 5234, 5783,
                              6374, 7009, 7690, 8419, 9199, 10032, 10920, 11865, 12871, 13938, 15070, 16270, 17540,
                              18882, 20299, 21795, 23371, 25031, 26777, 28613, 30541, 32565, 34687, 36911, 39240, 41676,
                              44224, 46886, 49666, 52568, 55595, 58749, 62036, 65458, 69019, 72723, 76574, 80575, 84730,
                              89043, 93518, 98160, 102971, 107956, 113119, 118465, 123998, 129721, 135640, 141758,
                              148080, 154611, 161355, 168316, 175500, 182910, 190551, 198429, 206548, 214913, 223529,
                              232400, 241533, 250931, 260599, 270544, 280770, 291283, 302087, 313188, 324592, 336303,
                              348328, 360672, 373339, 386337, 399671, 413346, 427368, 441743, 456477, 471576, 487045,
                              502891, 519120, 535737, 552749, 570163, 587984, 606218, 624873, 643954, 663468, 683421,
                              703819, 724671, 745981, 767757, 790005, 812733, 835947, 859653, 883860, 908573, 933799,
                              959547, 985822, 1012633, 1039986, 1067888, 1096347, 1125371, 1154965, 1185139, 1215900,
                              2494508, 2558419, 2623549, 2689914, 2757527, 4239607, 4344845, 4452027, 4561177, 4672319,
                              450041, 4594563, 4680138, 4766769, 4854465, 4943226, 5033064, 5123985, 5215995, 5309100,
                              7204407, 7331490, 7460064, 7590129, 7721700, 9818475, 9986727, 10156893, 10328979,
                              12252600]
        self.exptSkiGold = [15, 21, 29, 39, 51, 65, 81, 99, 119, 141, 165, 191, 219, 249, 281, 315, 351, 389, 429, 471,
                            515, 561, 609, 659, 711]
        self.exptGold = [30000, 20000, 30000, 20000, 30000]  # 攻 防 法 抗法 猎 【gold储备金 money现金 rmb人民币】
        self.gold2money = 0.85
        self.money2rmb = 245
        self.xlgmoney = 60

    async def get_role_iconid(self, type_id):
        need_fix_range = [[13, 24], [37, 48], [61, 72], [213, 224], [237, 248], [261, 272]]
        for range in need_fix_range:
            if (type_id >= range[0] and type_id <= range[1]):
                type_id = type_id - 12
                break
        return type_id

    async def get_role_kind_name(self, icon):
        if (icon > 200):
            kindid = ((icon - 200 - 1) % 12 + 1) + 200
        else:
            kindid = ((icon - 1) % 12 + 1)
        return self.RoleKindNameInfo[kindid]

    async def parse_role_kind_name(self, icon_id):
        icon_id = await self.get_role_iconid(icon_id)
        # print(icon_id)
        self.result['where']['race'] = int(icon_id)
        return await self.get_role_kind_name(icon_id)

    async def RoleInfoParser(self, roleInfo, merger_info, servertime):
        if isinstance(roleInfo, dict):
            raw_info = roleInfo
        elif isinstance(roleInfo, str):
            raw_info = self.replaceByDict(roleInfo.strip())
            self.result['xingjia'] = math.ceil(await self.costPrice(raw_info))
            self.result['xingjia_bi'] = int(
                round((self.result['xingjia'] - int(float(merger_info['price']))) / int(float(self.result['xingjia'])),
                      2) * 100)
            if (self.result['xingjia_bi'] < 0):
                self.result['xingjia_bi'] = 0

            self.result['where']['xingjia_bi'] = self.result['xingjia_bi']
        # print(raw_info)
        else:
            'roleInfo should be Object or String.'
            return {}
        # options = {
        #     "conf": self.xyqConf,
        #     "resUrl": self.ResUrl,
        #     "serverId": '',
        #     #"equipRequestTime": EquipRequestTime
        #     #"serverCurrentTime": ServerCurrentTime
        # }
        # #conf = options['conf']
        # #resUrl = options['resUrl']
        # #serverId = options['serverId']
        # #equipRequestTime = options['equipRequestTime']
        # #serverCurrentTime = options['serverCurrentTime']

        return await self.parse_role(raw_info, merger_info, servertime)

    def replaceByDict(self, content):
        # dict = {"([": "{", "])": "}", ",])": "}", "({": "[", "})": "]", ",})": "]"}
        reg = "\(\[|,?\s*\]\)|\(\{|,?\s*\}\)"
        pattern = re.compile(reg)
        res = re.sub(pattern, self.preg_replace, content)
        res = re.sub('\'', '\"', res)
        res = self.ext_json_decode(res)
        # print(res[6620:])
        return json.loads(res)

    def ext_json_decode(self, str):
        p1 = "\w:"
        pattern = re.compile(p1)
        match = pattern.findall(str)
        if len(match) > 0:
            # str = re.sub('(\d+):{', '"\\1":{', str)
            # str = re.sub('(\d+):\[', '"\\1":[', str)
            str = re.sub('([,{])(\d+):', '\\1"\\2":', str)
        return str

    def preg_replace(self, obj):
        # print(dir(obj))
        dict = {"([": "{", "])": "}", ",])": "}", "({": "[", "})": "]", ",})": "]"}
        if obj.group(0) in dict.keys():
            spa = re.compile("\s+")
            rr = re.sub(spa, '', obj.group(0))
            # print(dict[rr])
            return dict[rr]

    async def get_role_icon(self, icon_id):
        role_type = await self.get_role_iconid(icon_id)
        return "{0}/images/bigface/{1}.gif".format(self.ResUrl, role_type)

    async def get_goodness(self, raw_info):
        if (raw_info.get("iGoodness", None) == None):
            return raw_info["iBadness"]
        else:
            return raw_info["iGoodness"]

    async def get_marry_info(self, marry):
        if (marry == None):
            return ["未知", "未知"]
        if (marry != None and marry != 0):
            return ["是", marry]
        else:
            return ["否", "不存在"]

    async def get_tongpao_info(self, tongpao):
        if (tongpao == None):
            return ["未知", "未知"]
        if (tongpao != None and tongpao != 0):
            return ["是", tongpao]
        else:
            return ["否", "不存在"]

    async def parse_basic_role_info(self, raw_info):
        # ResUrl = self.ResUrl
        # EquipRequestTime = that.equipRequestTime
        # ServerCurrentTime = that.serverCurrentTime
        self.result['where']['school'] = int(raw_info['iSchool'])
        school_name = self.xyqConf.SchoolNameInfo.get(raw_info["iSchool"], '')
        marry_info = await self.get_marry_info(raw_info.get("iMarry", None))
        tongpao_info = await self.get_tongpao_info(raw_info.get("iMarry2", None))
        relation = "否"
        if (marry_info[0] == "未知" and tongpao_info[0] == "未知"):
            relation = "未知"

        elif (marry_info[0] == "否" and tongpao_info[0] == "否"):
            relation = "否"

        else:
            if (marry_info[0] == "是"):
                relation = "已婚"

            elif (tongpao_info[0] == "是"):
                relation = "同袍"

        community_info = ""
        if (raw_info.get("commu_name", None) != None and raw_info.get("commu_gid", None) != None):
            community_info = "{0}&nbsp;{1}".format(raw_info["commu_name"], raw_info["commu_gid"])
        elif (raw_info.get("commu_name", None) == None or raw_info.get("commu_gid", None) == None):
            community_info = "未知"
        else:
            community_info = "无"
        sum_exp = ""
        if (raw_info.get("sum_exp", None) == None):
            sum_exp = "未知"
        elif (raw_info["sum_exp"] == 0):
            sum_exp = "<1亿"
        else:
            sum_exp = "{0}亿".format(raw_info["sum_exp"])
        self.result['where']['sum_exp'] = int(raw_info['sum_exp'])
        fly_status = ""
        if (raw_info.get("i3FlyLv",False) and raw_info.get("i3FlyLv",0) > 0):
            fly_status = "化圣" + self.CHINESE_NUM_CONFIG[raw_info["i3FlyLv"]]
            self.result['where']['zhuangzhi'] = int(raw_info["i3FlyLv"]) * 10
        else:
            if (raw_info.get("iZhuanZhi",-1) >= 0):
                fly_status = self.ROLE_ZHUAN_ZHI_CONFIG[raw_info["iZhuanZhi"]]
                self.result['where']['zhuangzhi'] = int(raw_info["iZhuanZhi"])
        self.result["allow_pet_count"] = raw_info['iSumAmount']
        # print(self.result['where']['zhuangzhi'])

        role_info = {
            "sum_exp": sum_exp,
            "icon": await self.get_role_icon(raw_info["iIcon"]),
            "role_kind_name": await self.parse_role_kind_name(raw_info["iIcon"]),
            "role_level": raw_info["iGrade"],
            "nickname": raw_info["cName"],
            "is_fei_sheng": "是" if raw_info["iZhuanZhi"] >= 1 else "否",
            "fly_status": fly_status,
            "pride": raw_info["iPride"],
            "org": raw_info["cOrg"],
            "org_offer": raw_info["iOrgOffer"],
            "school": school_name,
            "school_offer": raw_info["iSchOffer"],
            "hp_max": raw_info["iHp_Max"],
            "mp_max": raw_info["iMp_Max"],
            "att_all": raw_info["iAtt_All"],
            "cor_all": raw_info["iCor_All"],
            "damage_all": raw_info["iDamage_All"],
            "mag_all": raw_info["iMag_All"],
            "def_all": raw_info["iDef_All"],
            "str_all": raw_info["iStr_All"],
            "dex_all": raw_info["iDex_All"],
            "res_all": raw_info["iRes_All"],
            "dod_all": raw_info["iDod_All"],
            "spe_all": raw_info["iSpe_All"],
            "mag_def_all": raw_info["iMagDef_All"],
            "point": raw_info["iPoint"],
            "cash": raw_info["iCash"],
            "saving": raw_info["iSaving"],
            "learn_cash": raw_info["iLearnCash"],
            "upexp": await self.get_real_upexp(raw_info),
            "badness": await self.get_goodness(raw_info),
            "goodness_sav": raw_info.get("igoodness_sav", "未知"),
            "qian_neng_guo": raw_info["iNutsNum"],
            "is_married": marry_info[0],
            "partner_id": marry_info[1],
            "is_tongpao": tongpao_info[0],
            "community_info": community_info,
            "fangwu_info": await self.get_fangwu_info(relation, raw_info.get("rent_level", None)),
            "tingyuan_info": await self.get_tingyuan_info(relation, raw_info.get("outdoor_level", None)),
            "muchang_info": await self.get_muchang_info(relation, raw_info["farm_level"]),
            # "qian_yuan_dan": self.get_qian_yuan_dan(),
            "is_du_jie": "已完成" if raw_info["iZhuanZhi"] == 2 else "未完成",
            "caiguo": raw_info.get("iCGTotalAmount",0),
            "body_caiguo": raw_info.get("iCGBodyAmount",0),
            "box_caiguo": raw_info.get("iCGBoxAmount",0),
            "chengjiu": raw_info.get("AchPointTotal", "未知"),
            "xianyu": raw_info.get("xianyu", "未知"),
            "energy": raw_info.get("energy", "未知"),
            "add_point": raw_info.get("addPoint", "未知"),
            "ji_yuan": raw_info.get("jiyuan", "未知"),
            "changesch": await self.get_change_school_list(raw_info.get("changesch", None)),
            "propkept": await self.get_prop_kept(raw_info.get("propKept",None), raw_info.get("iGrade",None)),
            "hero_score": raw_info.get("HeroScore", "未知"),
            "sanjie_score": raw_info.get("datang_feat", "未知"),
            "sword_score": raw_info.get("sword_score", "未知"),
            "total_caiguo": raw_info.get("iCGTotalAmount", "未知"),
            "total_avatar": raw_info["total_avatar"],
            "total_horse": raw_info["total_horse"],
            "fa_shang": raw_info["iTotalMagDam_all"],
            "fa_fang": raw_info["iTotalMagDef_all"]
        }
        # print(role_info)
        self.result['where']['shanghai'] = role_info['damage_all']
        self.result['where']['ming_zhong'] = role_info['att_all']
        self.result['where']['fang_yu'] = role_info['def_all']
        self.result['where']['hp'] = role_info['hp_max']
        self.result['where']['speed'] = role_info['dex_all']
        self.result['where']['fa_shang'] = role_info['fa_shang']
        self.result['where']['fa_fang'] = role_info['fa_fang']
        self.result['where']['qian_neng_guo'] = role_info['qian_neng_guo']

        # 储备金，现金
        #print(role_info.get("cash",0))
        if int(role_info.get("cash",0)) + int(role_info.get("saving",0)) > 3000*10000:
            self.result['highlight_attr'].append("现金加钱庄：{0}".format(role_info['cash']))
        if int(role_info.get("learn_cash",0)) > 4000 * 10000:
            self.result['highlight_attr'].append("储备金：{0}".format(role_info['learn_cash']))

        # print(role_info)
        if (raw_info.get("more_attr", None) != None and raw_info.get("more_attr", {}).get("attrs", None) != None):
            role_info['other_attr'] = {}
            for item in raw_info["more_attr"]["attrs"]:
                role_info['other_attr'][item['idx']] = item['lv']

        if (raw_info.get("ori_race", None) == None):
            role_info["ori_race"] = await self.get_race_by_school(raw_info["iSchool"])

        else:
            race_name = self.RACE_INFO[raw_info["ori_race"]]
            if (raw_info["ori_race"] != raw_info["iRace"]):
                race_name = '<span style="color:#FFCC00">' + race_name + '</span>'
            role_info["ori_race"] = race_name
        self.result['where']['ori_race'] = int(raw_info['ori_race'])
        package_num = int(raw_info.get("iPcktPage", 0))
        if (package_num > 0 and package_num <= 3):
            role_info["package_num"] = package_num
        elif (package_num == 0):
            role_info["package_num"] = "无"
        else:
            role_info["package_num"] = "未知"

        self.result["basic_info"] = role_info

    async def get_change_school_list(self, change_list):
        if (change_list == None):
            return "未知"
        if (len(change_list) == 0):
            return "无"
        school_list = []
        where = {}
        school_names = []
        for school_name in change_list:
            if (str(school_name) not in school_list):
                school_names.append(xyqSetting().SchoolNameInfo.get(school_name, ''))
                school_list.append(str(school_name))
        where['school_change_list'] = [int(v) for v in school_list]
        if len(school_names) > 0:
            self.result['highlight_attr'].append("历史门派：{0}".format("|".join(school_names)))
        self.result['where'] = dict(self.result['where'], **where)
        return ",".join(school_list)

    async def get_prop_kept(self, propKept, grade):
        res = []
        attr_point_strategy = []
        if (propKept):
            # print(propKept)
            for key, prop in propKept.items():
                s = await self.parse_single_prop_kept(prop, grade)
                s and res.append(s)
                s and attr_point_strategy.append(self.ATTR_NAME_KEEP.get(s, ''))
        self.result['where']['attr_point_strategy'] = attr_point_strategy
        # print(attr_point_strategy)
        return ",".join(res) if len(res) > 0 else '无'

    async def parse_single_prop_kept(self, prop, grade):
        if (prop == None):
            return None
        attr_list = []
        for key in prop.keys():
            if (self.PROP_KEPT_KEYS[key] and prop[key] >= (grade * 2 + 10)):
                attr_list.append({"key": key, "value": prop[key], "name": self.PROP_KEPT_KEYS[key]})
        # print(attr_list)
        if (len(attr_list) < 1):
            return None
        if (len(attr_list) < 2):
            return attr_list[0]['name']
        attr_list = sorted(attr_list, key=(
            operator.itemgetter('value') if operator.itemgetter('value') else self.PROP_KEPT_KEYS_ORDER[
                operator.itemgetter('key')]), reverse=True)

        return attr_list[0]['name'][0:1] + attr_list[1]['name'][0:1]

    async def get_qian_yuan_dan(self):
        print("乾元丹")

    async def get_muchang_info(self, relation, muchang_grade):
        return await self.get_married_info(relation, muchang_grade, self.xyqConf.muchang_info)

    async def get_tingyuan_info(self, relation, tingyuan_grade):
        return await self.get_married_info(relation, tingyuan_grade, self.xyqConf.tingyuan_info)

    async def get_fangwu_info(self, relation, fangwu_grade):
        return await self.get_married_info(relation, fangwu_grade, self.xyqConf.fangwu_info)

    async def get_married_info(self, relation, grade, r_setting):
        if (relation == "未知" or grade == None):
            return "未知"
        if (grade == 0):
            return "无"
        if (relation == "已婚"):
            return "夫妻共有"
        elif (relation == "同袍"):
            return "同袍共有"
        else:
            return r_setting[int(grade)]

    async def get_real_upexp(self, raw_info):
        exp_num = raw_info["iUpExp"]
        if (raw_info.get("ExpJw", None) == None or raw_info.get("ExpJwBase", None) == None):
            return exp_num
        exp_num += raw_info["ExpJw"] * raw_info["ExpJwBase"]
        return exp_num

    async def get_race_by_school(self, school):
        if (school in [1, 2, 3, 4, 13, 17]):
            return "人"
        elif (school in [9, 10, 11, 12, 15, 16]):
            return "魔"
        elif (school in [5, 6, 7, 8, 14, 18]):
            return "仙"
        else:
            return "未知"

    async def get_skill_icon(self, skill_id):
        skill_img = await self.make_img_name(skill_id) + ".gif"
        return self.ResUrl + "/images/role_skills/" + skill_img

    async def parse_role_skill(self, raw_info):
        life_skill = []
        school_skill = []
        ju_qing_skill = []
        conf = self.xyqConf.skill
        # print(conf['life_skill'])
        raw_skill_info = raw_info["all_skills"]
        self.result["yu_shou_shu"] = raw_info["all_skills"].get("221", '')
        # print(raw_skill_info)
        where = {}
        school = []

        for skill in raw_skill_info:

            info = {"skill_id": skill, "skill_grade": raw_skill_info[skill], "skill_pos": 0}
            info["skill_icon"] = await self.get_skill_icon(skill)
            if (conf["life_skill"].get(skill, None) != None):
                info["skill_name"] = conf["life_skill"][skill]
                life_skill.append(info)
                if info['skill_name'] == '强身术':
                    where['skill_qiang_shen'] = int(info['skill_grade'])
                elif info['skill_name'] == '冥想':
                    where['skill_ming_xiang'] = int(info['skill_grade'])
                elif info['skill_name'] == '暗器技巧':
                    where['skill_anqi'] = int(info['skill_grade'])
                elif info['skill_name'] == '打造技巧':
                    where['skill_dazao'] = int(info['skill_grade'])
                elif info['skill_name'] == "裁缝技巧":
                    where['skill_caifeng'] = int(info['skill_grade'])
                elif info['skill_name'] == "中药医理":
                    where['skill_zhongyao'] = int(info['skill_grade'])
                elif info['skill_name'] == "炼金术":
                    where['skill_lianjin'] = int(info['skill_grade'])
                elif info['skill_name'] == "烹饪技巧":
                    where['skill_pengren'] = int(info['skill_grade'])
                elif info['skill_name'] == "追捕技巧":
                    where['skill_zhuibu'] = int(info['skill_grade'])
                elif info['skill_name'] == "逃离技巧":
                    where['skill_taoli'] = int(info['skill_grade'])
                elif info['skill_name'] == "养生之道":
                    where['skill_yangshen'] = int(info['skill_grade'])
                elif info['skill_name'] == "健身术":
                    where['skill_jianshen'] = int(info['skill_grade'])
                elif info['skill_name'] == "巧匠之术":
                    where['skill_qiaojiang'] = int(info['skill_grade'])
                elif info['skill_name'] == "熔炼技巧":
                    where['skill_ronglian'] = int(info['skill_grade'])
                elif info['skill_name'] == "灵石技巧":
                    where['skill_lingshi'] = int(info['skill_grade'])
                elif info['skill_name'] == "强壮":
                    where['skill_qiang_zhuang'] = int(info['skill_grade'])
                elif info['skill_name'] == "淬灵之术":
                    where['skill_cuiling'] = int(info['skill_grade'])
                elif info['skill_name'] == "神速":
                    where['skill_shensu'] = int(info['skill_grade'])


            elif (conf["school_skill"].get(skill, None)):
                info["skill_name"] = conf["school_skill"][skill]["name"]
                info["skill_pos"] = conf["school_skill"][skill]["pos"]
                school_skill.append(info)
                school.append(int(skill))
                if info["skill_name"] in self.LI_SHI_FU_SKILL:
                    self.result['where']['lin_shi_fu'] = int(info['skill_grade'])
            elif (conf["ju_qing_skill"].get(skill, None)):
                info["skill_name"] = conf["ju_qing_skill"][skill]
                if info['skill_name'] == '古董评估':
                    where['skill_gudong'] = int(info['skill_grade'])
                elif info['skill_name'] == '建筑之术':
                    where['skill_jianzhu'] = int(info['skill_grade'])
                elif info['skill_name'] == '丹元济会':
                    where['skill_danyuan'] = int(info['skill_grade'])
                elif info['skill_name'] == '变化之术':
                    where['skill_bianhua'] = int(info['skill_grade'])
                elif info['skill_name'] == '火眼金睛':
                    where['skill_huoyan'] = int(info['skill_grade'])
                elif info['skill_name'] == '调息':
                    where['skill_tiaoxi'] = int(info['skill_grade'])
                elif info['skill_name'] == '打坐':
                    where['skill_dazuo'] = int(info['skill_grade'])
                elif info['skill_name'] == '奇门遁甲':
                    where['skill_qimen'] = int(info['skill_grade'])
                elif info['skill_name'] == '妙手空空':
                    where['skill_miaoshou'] = int(info['skill_grade'])
                elif info['skill_name'] == '仙灵店铺':
                    where['skill_xianling'] = int(info['skill_grade'])
                elif info['skill_name'] == '宝石工艺':
                    where['skill_baoshi'] = int(info['skill_grade'])

                # print(where)
            if (skill == '170' or skill == '197'):
                if (info['skill_grade'] > 0):
                    info['skill_grade'] -= 1
                    ju_qing_skill.append(info)
                else:
                    ju_qing_skill.append(info)
                if info.get('skill_name',None) == '翰墨之道':
                    where['skill_hanmo'] = int(info['skill_grade'])
                elif info.get('skill_name',None) == '丹青之道':
                    where['skill_danqing'] = int(info['skill_grade'])
                else:
                    print("未知")

        shuliandu = {
            "smith_skill": raw_info.get("iSmithski", '未知'),
            "sew_skill": raw_info.get("iSewski", '未知')
        }
        where['smith_skill'] = shuliandu['smith_skill']
        where['sew_skill'] = shuliandu['sew_skill']
        result = {
            "life_skill": life_skill,
            "school_skill": school_skill,
            "ju_qing_skill": ju_qing_skill,
            "left_skill_point": raw_info["iSkiPoint"],
            "shuliandu": shuliandu
        }

        where['school_skill'] = school
        self.result['where'] = dict(self.result['where'], **where)
        # print(result)
        self.result["role_skill"] = result

    async def parse_role_xiulian(self, raw_info):
        result = []
        result.append(
            {"name": "攻击修炼", "info": "{0}/{1}".format(raw_info["iExptSki1"], raw_info.get("iMaxExpt1", "未知"))})
        result.append(
            {"name": "防御修炼", "info": "{0}/{1}".format(raw_info["iExptSki2"], raw_info.get("iMaxExpt2", "未知"))})
        result.append(
            {"name": "法术修炼", "info": "{0}/{1}".format(raw_info["iExptSki3"], raw_info.get("iMaxExpt3", "未知"))})
        result.append(
            {"name": "抗法修炼", "info": "{0}/{1}".format(raw_info["iExptSki4"], raw_info.get("iMaxExpt4", "未知"))})
        result.append({"name": "猎术修炼", "info": raw_info.get("iExptSki5", "未知")})
        self.result['where']['expt_gongji'] = int(raw_info['iExptSki1'])
        self.result['where']['max_expt_gongji'] = int(raw_info['iMaxExpt1'])
        self.result['where']['expt_fangyu'] = int(raw_info['iExptSki2'])
        self.result['where']['max_expt_fangyu'] = int(raw_info['iMaxExpt2'])
        self.result['where']['expt_fashu'] = int(raw_info['iExptSki3'])
        self.result['where']['max_expt_fashu'] = int(raw_info['iMaxExpt3'])
        self.result['where']['expt_kangfa'] = int(raw_info['iExptSki4'])
        self.result['where']['max_expt_kangfa'] = int(raw_info['iMaxExpt4'])
        self.result['where']['expt_total'] = int(raw_info['iExptSki1']) + int(raw_info['iExptSki2']) + int(
            raw_info['iExptSki3']) + int(raw_info['iExptSki4'])
        self.result['where']['expt_lieshu'] = int(raw_info['iExptSki5'])
        self.result["role_xiulian"] = result
        # print(result)

    async def parse_pet_ctrl_skill(self, raw_info):
        result = []
        result.append({"name": "攻击控制力", "grade": raw_info["iBeastSki1"]})
        result.append({"name": "防御控制力", "grade": raw_info["iBeastSki2"]})
        result.append({"name": "法术控制力", "grade": raw_info["iBeastSki3"]})
        result.append({"name": "抗法控制力", "grade": raw_info["iBeastSki4"]})
        self.result['where']['bb_expt_fashu'] = int(raw_info["iBeastSki3"])
        self.result['where']['bb_expt_gonji'] = int(raw_info['iBeastSki1'])
        self.result['where']['bb_expt_kangfa'] = int(raw_info['iBeastSki4'])
        self.result['where']['bb_expt_fangyu'] = int(raw_info['iBeastSki2'])
        self.result["pet_ctrl_skill"] = result

    async def make_img_name(self, img_name):
        img_id = int(img_name)
        addon = ""
        if (img_id < 10):
            addon = "000"
        elif (img_id >= 10 and img_id < 100):
            addon = "00"
        elif (img_id >= 100 and img_id < 1000):
            addon = "0"
        return addon + str(img_name)

    async def get_pet_name(self, itype):
        return self.xyqConf.pet_info.get(itype,'')

    async def get_pet_skill_icon(self, skill_id):
        return self.ResUrl + "/images/pet_child_skill/" + await self.make_img_name(skill_id) + ".gif"

    async def get_pet_icon(self, itype):
        return "{0}/images/pets/small/{1}.gif".format(self.ResUrl, itype)

    async def get_ending_name(self, itype):
        return self.xyqConf.ending_info.get(itype, '无')

    async def get_child_icon(self, child_id):
        return self.ResUrl + "/images/child_icon/" + await self.make_img_name(child_id) + ".gif"

    async def get_child_name(self, itype):
        return self.xyqConf.child_info[itype]

    async def get_child_skill_icon(self, skill_id):
        return self.ResUrl + "/images/pet_child_skill/" + await self.make_img_name(skill_id) + ".gif"

    async def get_pet_equip_icon(self, typeid):
        return "{0}/images/equip/small/{1}.gif".format(self.ResUrl, typeid)

    async def get_lock_types(self, equip):
        locks = []
        if (equip.get("iLock", None)):
            locks.append(equip["iLock"])
        if (equip.get("iLockNew", None)):
            locks.append(equip["iLockNew"])
        return locks

    async def get_pet_info(self, pet, is_child, ServerTime):
        get_icon = self.get_pet_icon
        get_skill_icon = self.get_pet_skill_icon
        get_name = self.get_pet_name
        info = {}
        if (is_child):
            if (pet.get('isnew', None) != None and pet.get('isnew', 0) == 1):
                info["isnew"] = pet["isnew"]
                info["iMagDam_all"] = pet["iMagDam_all"];
                info["school"] = self.xyqConf.SchoolNameInfo.get(pet["school"], "无")
                info["ending"] = await self.get_ending_name(pet["ending"])
                info["gg"] = pet["gg"]
                info["zl"] = pet["zl"]
                info["wl"] = pet["wl"]
                info["dl"] = pet["dl"]
                info["nl"] = pet["nl"]
                info["nl"] = pet["nl"]
                info["lm"] = pet["lm"]

            get_icon = self.get_child_icon
            get_skill_icon = self.get_child_skill_icon
            get_name = self.get_child_name
        info["type_id"] = pet["iType"]
        info["pet_grade"] = pet["iGrade"]
        info["is_baobao"] = "否" if pet["iBaobao"] == 0 else "是"
        info["icon"] = await get_icon(pet["iType"])
        info["pet_name"] = await get_name(pet["iType"])
        info["kind"] = await get_name(pet["iType"])
        info["blood"] = pet["iHp"]
        info["magic"] = pet["iMp"]
        info["blood_max"] = pet["iHp_max"]
        info["magic_max"] = pet["iMp_max"]
        info["attack"] = pet["iAtt_all"]
        info["defence"] = pet["iDef_All"]
        info["speed"] = pet["iDex_All"]
        info["ling_li"] = pet["iMagDef_all"]
        info["lifetime"] = "永生" if pet["life"] >= 65432 else pet["life"]
        info["ti_zhi"] = pet["iCor_all"]
        info["fa_li"] = pet["iMag_all"]
        info["li_liang"] = pet["iStr_all"]
        info["nai_li"] = pet["iRes_all"]
        info["min_jie"] = pet["iSpe_all"]
        info["qian_neng"] = pet["iPoint"]
        info["cheng_zhang"] = pet["grow"] / 1000
        # info["wu_xing"] = wuxing_info[pet["iAtt_F"]]
        info["gong_ji_zz"] = pet["att"]
        info["fang_yu_zz"] = pet["def"]
        info["ti_li_zz"] = pet["hp"]
        info["fa_li_zz"] = pet["mp"]
        info["su_du_zz"] = pet["spe"]
        info["duo_shan_zz"] = pet["dod"]
        # info["used_yuanxiao"] = get_yuanxiao(pet["yuanxiao"]);
        # info["used_ruyidan"] = get_ruyidan(pet["ruyidan"]);
        # info["used_qianjinlu"] = that.safe_attr(pet["qianjinlu"]);
        # info["used_lianshou"] = get_lianshou(pet["lianshou"]);
        info["child_sixwx"] = pet.get("child_sixwx", '')
        info["is_child"] = is_child
        info["color"] = pet.get("iColor", '')
        info['summon_color'] = pet.get('summon_color', '')
        # info['PET_WUXING_INFO'] = window.PET_WUXING_INFO | | {};
        if (pet.get('core_close', None) == None or pet['core_close'] == 0):
            info['core_close'] = "已开启" if pet.get('core_close', None) == 0 or pet.get('core_close',
                                                                                      None) == None else "已关闭"
        info["genius"] = pet.get("iGenius", 0)
        highlight = []
        if (info["genius"] != 0):
            # highlight.append("特殊技能{0}".format(xyqSetting().PetSkillInfo['']))
            info["genius_skill"] = {"icon": await get_skill_icon(pet["iGenius"]), "skill_type": pet["iGenius"]}
        else:
            info["genius_skill"] = {}

        info["skill_list"] = []
        all_skills = pet["all_skills"]

        if isinstance(all_skills, list) and len(all_skills) > 7:
            highlight.append("{0}技能".format(len(all_skills)))
        if info['lifetime'] == '永生' and info['is_child'] == False:
            highlight.append("神兽：{0}".format(info['pet_name']))
        if (all_skills):
            all_skill_str = []
            senior_yaojue = []  # 高级要诀数量统计
            for typeid in all_skills:
                all_skill_str.append(str(typeid))
                ski = xyqSetting().PetSkillInfo[str(typeid)]
                # print(ski)
                if ski not in xyqSetting().PRIMARY_YAO_JUE:
                    senior_yaojue.append(ski)
                    if ski.find('高级') == -1 and info['is_child'] == False:
                        highlight.append("特殊技能:{0}".format(ski))
                if ski in xyqSetting().SENIOR_YAO_JUE:
                    senior_yaojue.append(ski)
                if (int(typeid) == info["genius"]):
                    continue
                info["skill_list"].append({
                    "icon": await get_skill_icon(typeid),
                    "skill_type": typeid,
                    "level": all_skills[typeid]
                })
            info['all_skill'] = "|".join(all_skill_str)
            # print(senior_yaojue)
            if len(senior_yaojue) > 5:
                highlight.append('{0}红'.format(len(senior_yaojue)))
            if len(highlight) > 0:
                self.result['highlight_attr'].append("{0}({2})亮点：{1}".format(info['pet_name'], "|".join(highlight),
                                                                             "宝宝" if info[
                                                                                         'is_baobao'] == '是' else '野生'))
            # print(self.result['highlight_attr'])

        else:
            info['all_skill'] = ''
        info['all_skills'] = re.split('\|', info['all_skill'])
        info["equip_list"] = []
        for i in range(1, 4):
            item = pet.get("summon_equip{0}".format(i), None)
            if (item):
                equip_name_info = self.xyqConf.get_equip_info(item["iType"])
                info["equip_list"].append({
                    "name": equip_name_info["name"],
                    "icon": await self.get_pet_equip_icon(item["iType"]),
                    "type": item["iType"],
                    "desc": item["cDesc"],
                    "lock_type": await self.get_lock_types(item),
                    "static_desc": re.sub("#R", "<br />", equip_name_info["desc"])
                })
            else:
                info["equip_list"].append(None)
        info["shipin_list"] = []
        if (pet.get('summon_equip4_type', None) != None):
            # print(type(self.xyqConf.pet_shipin_info))
            # print(pet['summon_equip4_type'])
            info["shipin_list"].append({
                "name": self.xyqConf.pet_shipin_info.get(pet['summon_equip4_type'], ''),
                # "icon": self.get_pet_shipin_icon(pet['summon_equip4_type']),
                "type": pet['summon_equip4_type'],
                "desc": pet['summon_equip4_desc']
            })

        info["empty_skill_img"] = self.ResUrl + "/images/role_skills/empty_skill.gif"
        info["neidan"] = []
        if (pet.get("summon_core", None) != None):
            for p in pet["summon_core"]:
                p_core = pet["summon_core"][p]
                info["neidan"].append({
                    "name": self.xyqConf.PetNeidanInfo.get(p, ''),
                    "icon": await self.get_neidan_icon(p),
                    "level": p_core[0]
                })

        info["jinjie"] = pet.get("jinjie", {})
        info["lock_type"] = await self.get_lock_types(pet)
        try:
            if (pet.get("csavezz", None)):
                await self.get_pet_ext_zz(info, {
                    "attrs": 'gong_ji_ext,fang_yu_ext,su_du_ext,duo_shan_ext,ti_li_ext,fa_li_ext',
                    "total_attrs": 'gong_ji_zz,fang_yu_zz,su_du_zz,duo_shan_zz,ti_li_zz,fa_li_zz',
                    "csavezz": pet['csavezz'],
                    "carrygradezz": pet['carrygradezz'],
                    "lastchecksubzz": pet['lastchecksubzz'],
                    "pet_id": info['type_id']
                }, ServerTime)
        except:
            print("额外资质计算异常忽略")
        return info

    async def is_shenshou_pet(self, petId):
        if (isinstance(petId, str)):
            petId = int(petId)
        if (petId < 100000):
            petId += 100000
        try:
            index = self.xyqConf.SHENSHOU_ITYPES.index(petId)
            return index >= 0
        except:
            return False

    async def get_pet_battle_level(self, petId):
        for li in self.xyqConf.PetBattleLevelTypes:
            id = +li[0] + 100000
            if (petId == id):
                return li[1]
        return -1

    async def get_pet_ext_zz(self, data, options, ServerTime):
        defdict = {
            "attrs": 'gong_ji_ext,fang_yu_ext,su_du_ext,duo_shan_ext,ti_li_ext,fa_li_ext',
            "total_attrs": 'gong_ji_zz,fang_yu_zz,su_du_zz,duo_shan_zz,ti_li_zz,fa_li_zz',
            "csavezz": '',
            "carrygradezz": -1,
            "pet_id": -1,
            "lastchecksubzz": 0
        }
        options = dict(defdict, **options)

        if (await self.is_shenshou_pet(options.get('pet_id', None))):
            return
        attrs = re.split(',', options['attrs'])
        totalAttrs = re.split(',', options['total_attrs'])
        csavezz = options['csavezz']
        carrygradezz = options['carrygradezz']
        lastchecksubzz = options.get("lastchecksubzz", 0)
        currentDate = ServerTime if (ServerTime and ServerTime.find('<!--') < 0) else datetime.datetime.now()
        if (csavezz == ''):
            return
        csavezz = re.split("\|", csavezz)
        if (carrygradezz < 0 or carrygradezz == 0):
            carrygradezz = await self.get_pet_battle_level(options['pet_id'])
            if (carrygradezz < 0):
                return
        maxZZ = [[1550, 1550, 1550, 1800, 5500, 3050], [1600, 1600, 1600, 2000, 6500, 3500],
                 [1650, 1650, 1650, 2000, 7000, 3600]]
        zz = maxZZ[carrygradezz]
        for i, z in enumerate(zz):
            extKey = attrs[i]
            totalKey = totalAttrs[i]
            if (totalKey in data.keys()):
                value = data[totalKey] - (z if int(z) > int(csavezz[i]) else int(csavezz[i]))
                ext = data[extKey] = value if value > 0 else 0
                orgZZ = data[totalKey] - data[extKey]
                data[totalKey] = orgZZ
                if (ext > 0):
                    year = lastchecksubzz if lastchecksubzz else 2017
                    currentYear = currentDate.year
                    currentTotalZZ = orgZZ + ext
                    for y in range(currentYear - year, 0, -1):
                        decay = math.floor(ext / 2)
                        currentTotalZZ = max(currentTotalZZ - decay, orgZZ)
                        ext = currentTotalZZ - orgZZ
                        if (ext <= 0):
                            break
                    downExtZZ = data[extKey] - ext
                    data[extKey] = ext
                    if (downExtZZ > 0):
                        await self.fix_pet_decay_attr(data, i, downExtZZ)

    async def fix_pet_decay_attr(self, pet, type, downzz):
        grade = + pet.get("pet_grade", 0)
        growth = (pet.get("growth", None) or pet.get("cheng_zhang", None) or 0) * 1000
        for type in range(0, 5):
            if (type == 0):
                decay = math.ceil(downzz * grade * 2 / 1000 * (700 + growth / 2) / 1000 * 4 / 3)
                await self.tryDecay('attack', pet, decay)
                break
            if (type == 1):
                decay = math.ceil(downzz * grade * 7 / 4000 * (700 + growth / 2) / 1000)
                await self.tryDecay('defence', pet, decay)
                break
            if (type == 2):
                speed = pet.get("smartness", 0) or pet.get("min_jie", 0)
                if (speed != 0):
                    decay = math.ceil(downzz * speed / 1000)
                    await self.tryDecay('speed', pet, decay)
                break
            if (type == 4):
                decay = math.ceil(downzz * grade / 1000)
                keys = ['max_blood', 'blood_max']
                await self.tryDecay(keys, pet, decay)
                await self.fixMax('blood', keys, pet)
                break
            if (type == 5):
                decayMp = math.ceil(downzz * grade / 500)
                mpKeys = ['max_magic', 'magic_max']
                await self.tryDecay(mpKeys, pet, decayMp)
                await self.fixMax('magic', pet, mpKeys)
                decayLingli = math.ceil(downzz * 3 / 10 * grade / 1000)
                await self.tryDecay(['wakan', 'ling_li'], pet, decayLingli)
                break

    async def fixMax(self, key, maxKeys, pet):
        if (key in pet):
            for mk in maxKeys:
                if (mk in pet):
                    pet[key] = min(pet[key], pet[mk])
                return

    async def tryDecay(self, keyArr, pet, val):
        if (isinstance(keyArr, str)):
            keyArr = [keyArr]
        for key in keyArr:
            if (key in pet):
                pet[key] = max(pet[key] - val, 0) or 0

    async def get_neidan_icon(self, neidan_id):
        return self.ResUrl + "/images/neidan/" + neidan_id + '.jpg'

    async def parse_pet_info(self, raw_info, servertime):
        all_pets = raw_info.get("AllSummon", [])
        pet_info = []
        for info in all_pets:
            info = await self.get_pet_info(info, False, servertime)
            pet_info.append(info)
        self.result["pet_info"] = pet_info
        # print(self.result["pet_info"])
        if (raw_info.get("child", None) and raw_info.get("child", {}).get("iType", None)):
            self.result["child_info"] = [await self.get_pet_info(raw_info["child"], True, servertime)]
        else:
            self.result["child_info"] = []
        if (raw_info.get("child2", None) and raw_info.get("child2", {}).get("iType", None)):
            self.result["child_info"].append(await self.get_pet_info(raw_info["child2"], True, servertime))
        highlight = []
        if len(raw_info['pet']) > 0:
            for ab in raw_info['pet']:
                for ski in ab['all_skills']:
                    if ski['value'] != 0:
                        highlight.append("特殊宠物：{0}{1}剩余次数{2}".format(ab['cName'], ski['name'], ski['value']))
            if len(highlight) > 0:
                self.result['highlight_attr'].append("|".join(highlight))
        self.result["special_pet_info"] = raw_info["pet"]
        # print(self.result["special_pet_info"])

    async def parse_equip_info(self, raw_info):
        ResUrl = self.ResUrl
        all_equips = raw_info["AllEquip"]
        using_equips = []
        not_using_equips = []
        for equip in all_equips:
            equip_info = self.xyqConf.get_equip_info(all_equips[equip]["iType"])
            info = {
                "pos": int(equip),
                "type": all_equips[equip]["iType"],
                "name": equip_info["name"],
                "desc": all_equips[equip]["cDesc"],
                "lock_type": await self.get_lock_types(all_equips[equip]),
                "static_desc": re.sub("#R", "<br />", equip_info["desc"]),
                "small_icon": "{0}/images/equip/small/{1}.git".format(self.ResUrl, all_equips[equip]["iType"]),
                "big_icon": "{0}/images/big/{1}.git".format(self.ResUrl, all_equips[equip]["iType"])
            }
            pos = int(equip)
            if ((pos >= 1 and pos <= 6) or pos in [187, 188, 189, 190]):
                using_equips.append(info)
            else:
                not_using_equips.append(info)
        self.result["using_equips"] = using_equips
        try:
            from parseEquip import parser
            not_in = ["4244", "4243", "4034", "3149"]
            highlight = []
            equip_hole = {}
            for vv in using_equips:
                equip_type = str(vv['type'])
                equip_name = vv['name']
                if ((len(equip_type) == 4 or (
                        len(equip_type) == 5 and equip_type[0: 2] == '31')) and equip_type not in not_in):
                    # 人物装备
                    equip_info = await parser().htmlToEquip(content=vv['desc'], merge_param={})
                    if equip_info.get("highlight", None) != None:
                        highlight.append("装备:{0}({1}级)-{2}".format(equip_name, equip_info['level'],
                                                                   equip_info.get("highlight", None)))
                    if equip_info.get("hole_num", 0) >= 4:
                        if (equip_hole.get(equip_info['hole_num'], 0) == 0):
                            equip_hole[equip_info['hole_num']] = 1
                        else:
                            equip_hole[equip_info['hole_num']] += 1
                elif (len(equip_type) == 5 and equip_type[0: 2] == '27'):
                    # 灵饰
                    lingshi_info = await parser().htmlToLingShi(content=vv['desc'], merge_params={})
                    if lingshi_info.get("highlight", '') != '':
                        highlight.append("灵饰:{0}({1}级)-{2}".format(equip_name, lingshi_info['level'],
                                                                   lingshi_info.get("highlight", None)))
            if len(equip_hole) > 0:
                for kk, vv in equip_hole.items():
                    highlight.append("{0}孔装备{1}件".format(kk, vv))
            if len(highlight) > 0:
                highlight = "|".join(highlight)
                self.result['highlight_attr'].append(highlight)
                # print(self.result['highlight_attr'])
        except KeyError:
            print("字典键异常")
            traceback.print_exc()
            # print(tasks.result().count())
        except IndexError:
            print("索引异常")
            traceback.print_exc()
        # except:
        #     print("忽略警告")

        # print(highlight)
        self.result["not_using_equips"] = not_using_equips

    async def parse_rider_info(self, raw_info):
        rider_name_info = self.xyqConf.rider_info
        all_rider = raw_info.get("AllRider", {})
        result = []
        # print(all_rider)
        for rider in all_rider:
            rider_info = raw_info["AllRider"][rider]
            # print(rider_info)
            info = {
                "type": rider_info["iType"],
                "grade": rider_info["iGrade"],
                "grow": rider_info.get("iGrow", 0) / 100,
                "exgrow": round(rider_info.get("exgrow", 0) / 10000) if rider_info.get("exgrow", None) != None else (
                        rider_info.get("iGrow", 0) / 100),
                "ti_zhi": rider_info.get("iCor", ''),
                "magic": rider_info.get("iMag", 0),
                "li_liang": rider_info.get("iStr", 0),
                "nai_li": rider_info.get("iRes", 0),
                "min_jie": rider_info.get("iSpe", 0),
                "qian_neng": rider_info.get("iPoint", 0),
                "icon": "{0}/images/riders/{1}.gif".format(self.ResUrl, rider_info['iType']),
                "type_name": rider_name_info.get(rider_info["iType"], ''),
                "mattrib": rider_info.get("mattrib", "未选择"),
                # "empty_skill_icon": this.get_empty_skill_icon()
                "empty_skill_icon": "{0}/images/role_skills/empty_skill.gif".format(self.ResUrl)
            }
            info["all_skills"] = []
            all_skills = rider_info["all_skills"]
            for typeid in all_skills:
                info["all_skills"].append({
                    "type": typeid,
                    "icon": "{0}/images/rider_skill/{1}.gif".format(self.ResUrl, await self.make_img_name(typeid)),
                    "grade": all_skills[typeid]
                })
            result.append(info)
        self.result["rider_info"] = result

    async def parse_clothes_info(self, raw_info):
        all_clothes_info = self.xyqConf.clothes_info
        all_clothes = raw_info.get("ExAvt", None)
        if (all_clothes == None):
            return
        result = []
        # print(all_clothes)
        highlight = []
        clothe_types = []
        for pos in all_clothes:
            clothes_info = all_clothes[pos]
            clothe_name = clothes_info.get('cName', False) or all_clothes_info.get(clothes_info["iType"], None)
            for v in self.highClothes:
                if clothe_name.find(v) > -1:
                    highlight.append(clothe_name)
                    break
            info = {
                "type": clothes_info["iType"],
                "name": clothe_name,
                "icon": "{0}/images/clothes/{1}.gif".format(self.ResUrl, clothes_info["iType"]),
                "order": clothes_info["order"],
                "static_desc": ""
            }
            clothe_types.append(int(clothes_info["iType"]))
            result.append(info)
        # print(result)
        # print(highlight)
        self.result['where']['limit_clothes'] = clothe_types
        if len(highlight) > 0:
            self.result['highlight_attr'].append("限量锦衣：" + "|".join(highlight))
        self.result["clothes"] = result

    async def parse_xiangrui_info(self, raw_info):
        all_xiangrui_info = self.xyqConf.xiangrui_info
        all_skills = self.xyqConf.xiangrui_skill
        nosale_xiangrui = self.xyqConf.nosale_xiangrui
        all_xiangrui = raw_info.get("HugeHorse", None)
        result = []
        nosale_result = []
        highlight = []
        for pos in all_xiangrui:

            xiangrui_info = all_xiangrui[pos]
            type = xiangrui_info["iType"]
            info = {
                "type": type,
                "name": xiangrui_info.get('cName', '') or all_xiangrui_info.get(type, ''),
                "icon": "{0}/images/xiangrui/{1}.git".format(self.ResUrl, type),
                "skill_name": all_skills.get(xiangrui_info['iSkill'], ''),
                "order": xiangrui_info["order"]
            }

            if (xiangrui_info.get("iSkillLevel", None) != None):
                info["skill_level"] = "{0}级".format(xiangrui_info["iSkillLevel"])
            else:
                info["skill_level"] = ""
            pos = int(pos)
            # print(xiangrui_info)
            if (self.xyqConf.nosale_to_sale_xiangrui.get(pos, False)):
                nosale = False
            else:
                nosale = (xiangrui_info.get("nosale", False) == 1)
            if (nosale == False):
                nosale = nosale_xiangrui.get(pos, False)

            nosale_xiangrui = []
            if (nosale):

                for nn in self.highRider:
                    nosale_xiangrui.append(info['name'])
                    if info['name'].find(nn) > -1:
                        highlight.append(info['name'])
                nosale_result.append(info)
            else:
                result.append(info)

            # print(nosale_result)
        self.result["xiangrui"] = result
        nosale_result = sorted(nosale_result, key=operator.itemgetter('order') if operator.itemgetter(
            'order') else operator.itemgetter('type'), reverse=True)
        # print(nosale_result)
        if (len(nosale_result) > 22):
            nosale_result = nosale_result[22:len(nosale_result)]
        self.result["nosale_xiangrui"] = nosale_result

        self.result['where']['xiangrui_list'] = nosale_xiangrui

        if len(highlight) > 0:
            self.result['highlight_attr'].append("限量祥瑞：" + "|".join(highlight))
        # print(self.result['highlight_rider'])
        if (raw_info.get("normal_horse",None)!=None):
            self.result["normal_xiangrui_num"] = raw_info["normal_horse"]

    async def merge(self, target_list, n):
        sum = 0
        for i in range(0, n - 4):
            sum += int(target_list[i])
        return sum

    async def goldLoss(self, maxExpt):
        goldLoss = 0
        de = maxExpt - 20
        for dec in range(1, 5):
            if de == dec and de == 0:
                goldLoss = 0
                break
            if de == dec and de == 1:
                goldLoss = self.exptSkiGold[12]
                break  # 损失修炼等级13
            if de == dec and de == 2:
                goldLoss = self.exptSkiGold[12] + self.exptSkiGold[13]
                break
            if de == dec and de == 3:
                goldLoss = self.exptSkiGold[13] + self.exptSkiGold[14] + self.exptSkiGold[15]
                break
            if de == dec and de == 4:
                goldLoss = self.exptSkiGold[14] + self.exptSkiGold[15] + self.exptSkiGold[16] + self.exptSkiGold[17]
                break
            if de == dec and de == 5:
                goldLoss = self.exptSkiGold[14] + self.exptSkiGold[15] + self.exptSkiGold[16] + self.exptSkiGold[17] + \
                           self.exptSkiGold[22]
                break
        return goldLoss

    # 角色性价比计算
    async def costPrice(self, roleInfo):
        try:
            gold2money = self.gold2money
            money2rmb = self.money2rmb
            xlgmoney = self.xlgmoney
            # exptSkiGold = [15, 21, 29, 39, 51, 65, 81, 99, 119, 141, 165, 191, 219, 249, 281, 315, 351, 389, 429, 471, 515,561, 609, 659, 711]
            # exptGold = [30000, 20000, 30000, 20000, 30000]  # 攻防法抗法猎
            exptSki = [roleInfo['iExptSki1'], roleInfo['iExptSki2'], roleInfo['iExptSki3'], roleInfo['iExptSki4'],
                       roleInfo['iExptSki5']]
            exptSkiGoldSum = 0
            for i in range(0, 4):
                exptSkiGoldSum += await self.merge(self.exptSkiGold, exptSki[i]) * self.exptGold[i]
            # 修炼上限

            exptSkiMaxGoldSum = 0
            iMaxExpt = [roleInfo['iMaxExpt1'], roleInfo['iMaxExpt2'], roleInfo['iMaxExpt3'], roleInfo['iMaxExpt4']]
            for i in range(0, 4):
                exptSkiMaxGoldSum += await self.goldLoss(iMaxExpt[i]) * self.exptGold[i]

            # 宠物修炼
            beastSki = [roleInfo['iBeastSki1'], roleInfo['iBeastSki2'], roleInfo['iBeastSki3'], roleInfo['iBeastSki4']]
            # print(beastSki)
            SumExp = 0
            for i in range(0, 4):
                n = await self.merge(self.exptSkiGold, beastSki[i])
                # print(n)
                SumExp += await self.merge(self.exptSkiGold, beastSki[i])
            beastSkiMoney = math.ceil(SumExp / 15) * xlgmoney * 10000

            # 角色师门
            schoolSki = []
            # print(roleInfo['all_skills'])
            for i in range(1, 133):
                if (isinstance(roleInfo['all_skills'].get(str(i), None), int)):
                    schoolSki.append(min(roleInfo['all_skills'][str(i)], 180))  # 技能大于180的为符石加成不考虑，低等级的符石加成暂不处理。
                    if (len(schoolSki) >= 7):
                        break  # 找到全部7个技能等级跳出循环
            schoolSkiGoldSum = 0
            for i in range(0, 6):
                schoolSkiGoldSum += await self.merge(self.schoolSkiGold, schoolSki[i])

            # 生活技能 只考虑40级以上  201-218；230 // 普通，打造技巧，强身，灵石，强壮
            # 普通 最大160，前150为师门花费的一半  淬灵之术231 没查到当普通处理
            comLifeSkiGold = [3, 6, 9, 14, 19, 25, 33, 43, 55, 69, 87, 108, 133, 162, 196, 236, 281, 333, 393, 459, 535,
                              619, 713, 818, 934, 1062, 1202, 1357, 1525, 1710, 1910, 2127, 2362, 2617, 2891, 3187,
                              3504, 3845, 4209, 4599, 5016, 5460, 5932, 6435, 6969, 7535, 8135, 8770, 9441, 10149,
                              10897, 11685, 12515, 13388, 14306, 15270, 16282, 17343, 18455, 19620, 20838, 22112, 23443,
                              24833, 26284, 27797, 29374, 31018, 32729, 34509, 36361, 38287, 40287, 42365, 44521, 46759,
                              49080, 51485, 53978, 56559, 59232, 61999, 64860, 67820, 70879, 74040, 77305, 80677, 84158,
                              87750, 91455, 95275, 99214, 103274, 107456, 111764, 116200, 120766, 125465, 130299,
                              135272, 140385, 145641, 151043, 156594, 162296, 168151, 174164, 180336, 186669, 193168,
                              199835, 206673, 213684, 220871, 228238, 235788, 243522, 251445, 259560, 267868, 276374,
                              285081, 293992, 303109, 312436, 321977, 331734, 341710, 351909, 362335, 372990, 383878,
                              395002, 406366, 417973, 429826, 441930, 454286, 466899, 479773, 492911, 506316, 519993,
                              533944, 548173, 562685, 577482, 592569, 607950, 997803, 1023367, 1049419, 1075965,
                              1103010, 1695843, 1737938, 1780810, 1824471, 1868927]
            # 打造204 前150同普通，151-160有区别
            daZaoGold = [3, 6, 9, 14, 19, 25, 33, 43, 55, 69, 87, 108, 133, 162, 196, 236, 281, 333, 393, 459, 535, 619,
                         713, 818, 934, 1062, 1202, 1357, 1525, 1710, 1910, 2127, 2362, 2617, 2891, 3187, 3504, 3845,
                         4209, 4599, 5016, 5460, 5932, 6435, 6969, 7535, 8135, 8770, 9441, 10149, 10897, 11685, 12515,
                         13388, 14306, 15270, 16282, 17343, 18455, 19620, 20838, 22112, 23443, 24833, 26284, 27797,
                         29374, 31018, 32729, 34509, 36361, 38287, 40287, 42365, 44521, 46759, 49080, 51485, 53978,
                         56559, 59232, 61999, 64860, 67820, 70879, 74040, 77305, 80677, 84158, 87750, 91455, 95275,
                         99214, 103274, 107456, 111764, 116200, 120766, 125465, 130299, 135272, 140385, 145641, 151043,
                         156594, 162296, 168151, 174164, 180336, 186669, 193168, 199835, 206673, 213684, 220871, 228238,
                         235788, 243522, 251445, 259560, 267868, 276374, 285081, 293992, 303109, 312436, 321977, 331734,
                         341710, 351909, 362335, 372990, 383878, 395002, 406366, 417973, 429826, 441930, 454286, 466899,
                         479773, 492911, 506316, 519993, 533944, 548173, 562685, 577482, 592569, 607950, 623627, 639604,
                         655887, 672478, 689381, 706601, 724140, 742004, 760196, 778719]
            # 强身201 最大140 前120同普通，121-140有区别
            qiangShenGold = [3, 6, 9, 14, 19, 25, 33, 43, 55, 69, 87, 108, 133, 162, 196, 236, 281, 333, 393, 459, 535,
                             619, 713, 818, 934, 1062, 1202, 1357, 1525, 1710, 1910, 2127, 2362, 2617, 2891, 3187, 3504,
                             3845, 4209, 4599, 5016, 5460, 5932, 6435, 6969, 7535, 8135, 8770, 9441, 10149, 10897,
                             11685, 12515, 13388, 14306, 15270, 16282, 17343, 18455, 19620, 20838, 22112, 23443, 24833,
                             26284, 27797, 29374, 31018, 32729, 34509, 36361, 38287, 40287, 42365, 44521, 46759, 49080,
                             51485, 53978, 56559, 59232, 61999, 64860, 67820, 70879, 74040, 77305, 80677, 84158, 87750,
                             91455, 95275, 99214, 103274, 107456, 111764, 116200, 120766, 125465, 130299, 135272,
                             140385, 145641, 151043, 156594, 162296, 168151, 174164, 180336, 186669, 193168, 199835,
                             206673, 213684, 220871, 228238, 235788, 243522, 251445, 259560, 247868, 276374, 285081,
                             293992, 303109, 331734, 312436, 321977, 351909, 341710, 362335, 372990, 383878, 395002,
                             406366, 417973, 429826, 441930, 454286, 466899]
            # 灵石218 最大120
            lingShiGold = [189, 225, 267, 314, 367, 428, 495, 571, 654, 747, 849, 962, 1085, 1220, 1368, 1528, 1702,
                           1890, 2093, 2313, 2549, 2803, 3076, 3367, 3679, 4012, 4368, 4746, 5148, 5575, 6028, 6508,
                           7015, 7552, 8119, 8718, 9348, 10012, 10711, 11445, 12216, 13026, 13875, 14764, 15696, 16670,
                           17689, 18754, 19866, 21027, 22237, 23499, 24814, 26183, 27607, 29089, 30629, 32230, 33892,
                           35617, 37407, 39264, 41188, 43182, 45247, 47386, 49599, 51888, 54256, 56703, 59232, 61844,
                           64542, 67326, 70200, 73164, 76220, 79371, 82619, 85965, 134117, 139440, 144919, 150558,
                           156359, 162326, 168462, 174769, 181252, 187913, 194755, 201782, 208997, 216403, 224003,
                           231802, 239802, 248007, 256421, 265046, 273886, 282945, 292227, 301734, 311472, 321442,
                           331649, 342097, 352790, 363731, 374923, 386372, 398080, 410052, 422291, 434802, 447588,
                           460654, 474003, 487640]
            # 强壮230 最大40 同神速237
            qiangZhuangGold = [430000, 495000, 570000, 655000, 750000, 855000, 970000, 1095000, 1230000, 1375000,
                               1530000, 1870000, 2250000, 1695000, 2455000, 2055000, 2670000, 2895000, 3130000, 3375000,
                               3630000, 3895000, 4455000, 4170000, 4750000, 5055000, 5695000, 5370000, 6030000, 6730000,
                               7095000, 6375000, 7470000, 7855000, 9070000, 8250000, 8655000, 9495000, 9930000,
                               10375000]

            lifeSki = []
            # 201: "强身术", 202: "冥想", 203: "暗器技巧", 204: "打造技巧", 205: "裁缝技巧", 206: "中药医理",
            # 207: "炼金术", 208: "烹饪技巧", 209: "追捕技巧", 210: "逃离技巧", 211: "养生之道", 212: "健身术",
            # 216: "巧匠之术", 217: "熔炼技巧", 218: "灵石技巧", 230: "强壮", 231: "淬灵之术", 237: "神速"
            for i in range(201, 217):
                lifeSki.append(
                    roleInfo['all_skills'][str(i)] if isinstance(roleInfo['all_skills'].get(str(i), None), int) else 0)
            lifeSki.append(
                roleInfo['all_skills']['231'] if isinstance(roleInfo['all_skills'].get('231', None), int) else 0)
            lifeSki.append(
                roleInfo['all_skills']['218'] if isinstance(roleInfo['all_skills'].get('218', None), int) else 0)
            lifeSki.append(
                roleInfo['all_skills']['230'] if isinstance(roleInfo['all_skills'].get('230', None), int) else 0)
            lifeSki.append(
                roleInfo['all_skills']['237'] if isinstance(roleInfo['all_skills'].get('237', None), int) else 0)

            # 调整顺序 为强身，打造，暗器，冥想...
            tem = 0
            tem = lifeSki[1]
            lifeSki[1] = lifeSki[3]
            lifeSki[3] = tem

            lifeSkiGoldSum = 0
            for i in range(2, len(lifeSki) - 4):
                lifeSkiGoldSum += await self.merge(comLifeSkiGold, lifeSki[i] if lifeSki[i] > 40 else 0)
            lifeSkiGoldSum += await self.merge(qiangShenGold, lifeSki[0] if lifeSki[0] > 40 else 0)
            lifeSkiGoldSum += await self.merge(daZaoGold, lifeSki[1] if lifeSki[1] > 40 else 0)
            lifeSkiGoldSum += await self.merge(lingShiGold,
                                               lifeSki[len(lifeSki) - 3] if lifeSki[len(lifeSki) - 3] > 40 else 0)
            lifeSkiGoldSum += await self.merge(qiangZhuangGold, lifeSki[len(lifeSki) - 2])
            lifeSkiGoldSum += await self.merge(qiangZhuangGold, lifeSki[len(lifeSki) - 1])

            lifeBG = []
            for i in range(0, 159):
                lifeBG.append(i + 1)
            lifeSkiBGSum = 0
            for vv in lifeSki:
                lifeSkiBGSum += await self.merge(lifeBG, vv if vv > 40 else 0)

            # 返回金钱总消耗
            rmbPrice = ((
                                exptSkiGoldSum + schoolSkiGoldSum + exptSkiMaxGoldSum + lifeSkiGoldSum) * gold2money + beastSkiMoney) * money2rmb / 3000e4 + lifeSkiBGSum / 50.0

            return rmbPrice
        except:
            print("角色性价计算异常！")

    async def parse_role(self, raw_info, merge_info, servertime):
        try:
            await self.parse_basic_role_info(raw_info)
            # print(self.result)
            # basic_info
            await self.parse_role_skill(raw_info)
            # role_skill
            await self.parse_equip_info(raw_info)
            # using_equip
            # no_using_equip
            await self.parse_role_xiulian(raw_info)
            # role_xiulian
            await self.parse_pet_ctrl_skill(raw_info)
            # pet_ctrl_skill
            await self.parse_pet_info(raw_info, servertime)
            # special_pet_info
            # pet_info
            await self.parse_rider_info(raw_info)
            # rider_info
            await self.parse_clothes_info(raw_info)
            # clothes
            await self.parse_xiangrui_info(raw_info)
            # nosale_xiangrui
            # xiangrui
            self.result['where']['equip_level'] = int(merge_info.get('equip_level', 0))
            self.result['where']['price_fen'] = float(merge_info.get('price', 0)) * 100
            self.result['where']['server_name'] = merge_info.get("server_name",'')

            # print(self.result)
        except KeyError:
            print("字典键异常")
            traceback.print_exc()
            # print(tasks.result().count())
        except IndexError:
            print("索引异常")
            traceback.print_exc()
        # except:
        #     print("有异常")
        # print(self.role_params.keys()-self.result['where'].keys())
        # print(self.result['highlight_attr'])
        # print(self.result)
        return dict(self.result, **merge_info)

# role = parseRole()
# desc = '(["iGrade":109,"iPcktPage":0,"iStr_All":593,"TA_iAllNewPoint":0,"iSumAmount":6,"iPride":713,"ExpJw":0,"iAtt_All":1038,"normal_horse":1,"iSpe_All":129,"total_avatar":0,"more_attr":(["attrs":({(["idx":6,"lv":0,]),(["idx":3,"lv":0,]),(["idx":8,"lv":0,]),(["idx":1,"lv":0,]),(["idx":12,"lv":0,]),(["idx":5,"lv":0,]),(["idx":9,"lv":0,]),(["idx":7,"lv":0,]),(["idx":11,"lv":0,]),(["idx":10,"lv":0,]),(["idx":4,"lv":0,]),(["idx":2,"lv":0,]),(["idx":13,"lv":264,]),(["idx":14,"lv":481,]),}),]),"shenqi":([]),"HeroScore":0,"iMp_Max":665,"commu_gid":0,"iMarry2":0,"iLearnCash":4781018,"energy":46,"iPoint":0,"HugeHorse":([113:(["iSkill":0,"order":1,"iType":11098,"nosale":0,"cName":"流云玉佩","iSkillLevel":0,]),]),"iTotalMagDam_all":481,"iBadness":0,"iHp_Eff":1271,"farm_level":0,"iCGBoxAmount":0,"usernum":56072554,"shenqi_pos":({0,0,}),"datang_feat":6000,"jiyuan":0,"iOrgOffer":865,"iExptSki5":0,"idbid_desc":({}),"iTotalMagDef_all":481,"iHp":1271,"iSkiPoint":21,"iSumAmountEx":0,"AllRider":([1:(["mattrib":"耐力","all_skills":([]),"iGrade":114,"exgrow":12635,"iType":503,"ExtraGrow":0,]),]),"icolor_ex":0,"cName":"迪☆少","sword_score":0,"iErrantry":0,"iExptSki4":6,"AchPointTotal":732,"fabao":([17:(["cDesc":"0#W【回合限制】1#r#Y#Y灵气：#G72 #Y 五行：#G金#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6013,]),16:(["cDesc":"0#Y灵气：#G11 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6031,]),13:(["cDesc":"0#Y灵气：#G300#Y 五行：#G金#Y#r修炼境界：第#G10#Y层 #cFF6F28道满根归#Y","iType":6072,]),18:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G70 #Y 五行：#G木#Y#r修炼境界：第#G5#Y层 #c01FEC5移星换斗#Y","iType":6023,]),11:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G3#Y层 #cB7BFF8心领神会#Y","iType":6004,]),]),"iBeastSki2":0,"iMaxExpt2":20,"ExAvt":([]),"ExpJwBase":1000000000,"iSchool":5,"iGoodness":171,"sum_exp":5,"iExptSki2":7,"iMag_All":116,"rent":27724277,"all_skills":(["198":1,"206":13,"170":1,"52031":1,"169":1,"179":1,"73":100,"76":50,"173":1,"72":95,"208":6,"202":37,"52016":1,"174":1,"216":36,"154":6,"74":80,"52032":1,"75":1,"201":58,"70":109,"197":1,"71":109,"196":1,]),"iDod_All":264,"iRace":3,"iSmithski":0,"changesch":({}),"iRes_All":191,"xianyu":85,"addPoint":2,"iDef_All":474,"iIcon":10,"iMarry":0,"iDamage_All":791,"iMaxExpt4":20,"iMp":665,"pet":({}),"iCash":406230,"iCGBodyAmount":0,"iMagDef_All":481,"commu_name":"","total_horse":1,"outdoor_level":1,"igoodness_sav":399,"bid":0,"iCGTotalAmount":0,"iHp_Max":1271,"iSaving":1000000,"propKept":([]),"cOrg":"〃精锐班子．","iBeastSki4":0,"iZhuanZhi":0,"shenqi_yellow":"","iSchOffer":417,"iDesc":0,"AllSummon":({(["HP_MAX":5500,"jj_extra_add":0,"iDod_All":170,"iGrade":115,"all_skills":(["304":1,"416":1,"301":1,]),"lianshou":0,"DEF_MAX":1550,"iMagDef_all":536,"att":1384,"SPD_MAX":1550,"mp":1308,"summon_equip4_desc":"","qianjinlu":0,"summon_core":([]),"MP_MAX":3050,"lastchecksubzz":2019,"iDef_All":611,"iMp":807,"iColor":1,"ATK_MAX":1550,"carrygradezz":0,"iMp_max":807,"iAtt_all":1320,"left_qlxl":7,"csavezz":"1384|1477|1425|1235|5034|1308","att_rate":0,"iPoint":0,"iType":102576,"ruyidan":0,"jinjie":(["cnt":0,"core":([]),"lx":0,]),"MS_MAX":1800,"core_close":0,"dod":1235,"life":3685,"growthMax":1277,"iRealColor":1,"iAtt_F":8,"iHp":2380,"iStr_all":606,"def":1477,"hp":5034,"summon_equip4_type":0,"spe":1425,"grow":1252,"iHp_max":2380,"iGenius":0,"summon_color":0,"yuanxiao":0,"iSpe_all":138,"tmp_lingxing":0,"iBaobao":1,"iRes_all":131,"iJjFeedCd":0,"sjg":0,"iMag_all":135,"iCor_all":240,"iDex_All":196,]),(["HP_MAX":5500,"jj_extra_add":0,"iDod_All":256,"iGrade":115,"all_skills":(["304":1,"305":1,"301":1,"325":1,"316":1,]),"lianshou":0,"DEF_MAX":1550,"iMagDef_all":581,"att":1296,"summon_equip1":(["cDesc":"#r等级 55  #r伤害 +20 命中率 +7%#r耐久度 200  修理失败 1次#r#G#G敏捷 +10#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4惊心一剑#Y#Y#r#r镶嵌效果 #r+50伤害 镶嵌等级：5","iType":9306,]),"SPD_MAX":1550,"mp":2592,"summon_equip4_desc":"","qianjinlu":0,"summon_core":([]),"MP_MAX":3050,"lastchecksubzz":2019,"iDef_All":593,"iMp":1066,"iColor":2,"ATK_MAX":1550,"carrygradezz":0,"iMp_max":1066,"iAtt_all":1473,"left_qlxl":7,"csavezz":"1296|1259|1283|1701|3434|2592","att_rate":7,"iPoint":0,"iType":102577,"ruyidan":0,"jinjie":(["cnt":0,"core":([]),"lx":0,]),"MS_MAX":1800,"core_close":0,"dod":1701,"life":3145,"growthMax":1266,"iRealColor":2,"iAtt_F":16,"iHp":1701,"iStr_all":664,"summon_equip2":(["cDesc":"#r等级 55  #r速度 +20 伤害 +20#r耐久度 113  修理失败 1次#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4惊心一剑#Y#Y#r#r镶嵌效果 #r+24速度 镶嵌等级：4","iType":9206,]),"def":1259,"hp":3434,"summon_equip4_type":0,"spe":1283,"grow":1217,"iHp_max":1851,"summon_equip3":(["cDesc":"#r等级 55  #r伤害 +20 防御 +42#r耐久度 19#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4惊心一剑#Y#Y#r#r镶嵌效果 #r+150气血 镶嵌等级：5","iType":9106,]),"iGenius":0,"summon_color":0,"yuanxiao":0,"iSpe_all":151,"tmp_lingxing":0,"iBaobao":1,"iRes_all":137,"iJjFeedCd":0,"sjg":0,"iMag_all":129,"iCor_all":179,"iDex_All":237,]),(["HP_MAX":5500,"jj_extra_add":0,"iDod_All":31,"iGrade":10,"all_skills":(["312":1,]),"lianshou":0,"DEF_MAX":1550,"iMagDef_all":58,"att":1409,"SPD_MAX":1550,"mp":1248,"summon_equip4_desc":"","qianjinlu":0,"summon_core":([]),"MP_MAX":3050,"lastchecksubzz":2019,"iDef_All":84,"iMp":169,"ATK_MAX":1550,"carrygradezz":0,"iMp_max":169,"iAtt_all":76,"left_qlxl":7,"csavezz":"1409|1357|1100|1155|4284|1248","att_rate":0,"iPoint":50,"iType":102076,"ruyidan":0,"jinjie":(["cnt":0,"core":([]),"lx":0,]),"MS_MAX":1800,"core_close":0,"dod":1155,"life":5580,"growthMax":1277,"iRealColor":0,"iAtt_F":8,"iHp":250,"iStr_all":23,"def":1357,"hp":4284,"summon_equip4_type":0,"spe":1100,"grow":1240,"iHp_max":250,"iGenius":0,"summon_color":0,"yuanxiao":0,"iSpe_all":27,"tmp_lingxing":0,"iBaobao":1,"iRes_all":33,"iJjFeedCd":0,"sjg":0,"iMag_all":39,"iCor_all":28,"iDex_All":29,]),(["HP_MAX":5500,"jj_extra_add":0,"iDod_All":15,"iGrade":0,"all_skills":(["312":1,"503":1,"301":1,]),"lianshou":0,"DEF_MAX":1550,"iMagDef_all":27,"att":1416,"SPD_MAX":1550,"mp":2180,"summon_equip4_desc":"","qianjinlu":0,"summon_core":([]),"MP_MAX":3050,"lastchecksubzz":2019,"iDef_All":63,"iMp":36,"ATK_MAX":1550,"carrygradezz":0,"iMp_max":36,"iAtt_all":26,"left_qlxl":7,"csavezz":"1416|1133|1254|1545|3540|2180","att_rate":0,"iPoint":0,"iType":102077,"ruyidan":0,"jinjie":(["cnt":0,"core":([]),"lx":0,]),"MS_MAX":1800,"core_close":0,"dod":1545,"life":8000,"growthMax":1266,"iRealColor":0,"iAtt_F":8,"iHp":140,"iStr_all":22,"def":1133,"hp":3540,"summon_equip4_type":0,"spe":1254,"grow":1230,"iHp_max":140,"iGenius":0,"summon_color":0,"yuanxiao":0,"iSpe_all":10,"tmp_lingxing":0,"iBaobao":1,"iRes_all":39,"iJjFeedCd":0,"sjg":0,"iMag_all":10,"iCor_all":19,"iDex_All":12,]),(["HP_MAX":5500,"jj_extra_add":0,"iDod_All":44,"iGrade":18,"all_skills":(["312":1,"503":1,"301":1,"325":1,]),"lianshou":0,"DEF_MAX":1550,"iMagDef_all":82,"att":1272,"SPD_MAX":1550,"mp":2140,"summon_equip4_desc":"","qianjinlu":0,"summon_core":([]),"MP_MAX":3050,"lastchecksubzz":2019,"iDef_All":115,"iMp":211,"ATK_MAX":1550,"carrygradezz":0,"iMp_max":211,"iAtt_all":132,"left_qlxl":7,"csavezz":"1272|1309|1298|1590|3540|2140","att_rate":0,"iPoint":90,"iType":102077,"ruyidan":0,"jinjie":(["cnt":0,"core":([]),"lx":0,]),"MS_MAX":1800,"core_close":0,"dod":1590,"life":7542,"growthMax":1266,"iRealColor":0,"iAtt_F":8,"iHp":398,"iStr_all":44,"def":1309,"hp":3540,"summon_equip4_type":0,"spe":1298,"grow":1242,"iHp_max":398,"iGenius":0,"summon_color":0,"yuanxiao":0,"iSpe_all":28,"tmp_lingxing":0,"iBaobao":1,"iRes_all":37,"iJjFeedCd":0,"sjg":0,"iMag_all":36,"iCor_all":45,"iDex_All":36,]),}),"AllEquip":([17:(["cDesc":"#r等级 80  五行 金#r#r防御 +136#r耐久度 238  修理失败 1次#r锻炼等级 3  镶嵌宝石 月亮石#r#G#G体质 +2#Y #G敏捷 -4#Y#Y#r#c4DBAF4套装效果：附加状态逆鳞#Y#Y#r#G开运孔数：3孔/3孔#G#r符石: 力量 +1#n#Y  ","iType":2609,]),13:(["cDesc":"等级 80#r法术防御 +16#r耐久度 287#r精炼等级 3#r#G法术暴击等级 +8 #cEE82EE[+12]#r#G物理暴击等级 +8 #cEE82EE[+12]#r#G物理暴击等级 +8 #cEE82EE[+12]#r#W制造者：Mc：安可儿强化打造#","iType":27102,]),16:(["cDesc":"#r等级 100  五行 木#r#r伤害 +350 命中 +557#r耐久度 185  修理失败 3次#r锻炼等级 6  镶嵌宝石 红玛瑙#Y#r#W制造者：イ╄·麽ǎ！强化打造#Y  ","iType":1551,]),26:(["cDesc":"#r等级 80  #r灵力 +101#r耐久度 30  修理失败 1次#r锻炼等级 4  镶嵌宝石 舍利子#Y#r#c4DBAF4套装效果：附加状态逆鳞#Y#Y#r#G开运孔数：3孔/3孔#G#r符石: 耐力 +1#n#G#r符石: 敏捷 +1#n#G#r符石: 伤害 +1.5#n#r#cEE82EE符石组合: 天雷地火#r门派条件：天宫 #r部位条件：无#r使用天雷斩、雷霆万钧时增加人物等级/1.5的伤害，装备该组合时降低5%的防御，同时降低5%的气血，仅对NPC使用时有效#Y  ","iType":2815,]),11:(["cDesc":"等级 80#r防御 +16#r耐久度 310#r精炼等级 3#r#G物理暴击等级 +8 #cEE82EE[+12]#r#G物理暴击等级 +8 #cEE82EE[+12]#r#G法术伤害结果 +9 #cEE82EE[+9]#r#W制造者：冯铁匠·强化打造#","iType":27002,]),9:(["cDesc":"#r等级 70  五行 金#r#r防御 +88#r耐久度 450#r#G#G体质 +6#Y #G敏捷 -3#Y#Y  ","iType":2608,]),21:(["cDesc":"#r等级 140  五行 火#r#r魔法 +152 防御 +85#r耐久度 685#Y#r#c4DBAF4特技：#c4DBAF4流云诀#Y#Y#r#W制造者：″遗忘の尕娜强化打造#Y  ","iType":2556,]),20:(["cDesc":"#r等级 80  #r气血 +400 防御 +34#r耐久度 451  修理失败 1次#r锻炼等级 6  镶嵌宝石 光芒石#Y#r#c4DBAF4套装效果：附加状态逆鳞#Y#Y#r#G开运孔数：3孔/3孔#Y   ","iType":2915,]),14:(["cDesc":"#r等级 70  #r敏捷 +32 防御 +34#r耐久度 151  修理失败 1次#r锻炼等级 4  镶嵌宝石 黑宝石#r#G#G速度 +32#Y#Y#r#c4DBAF4套装效果：附加状态逆鳞#Y#Y#r#G开运孔数：3孔/3孔#G#r符石: 体质 +1#n#G#r符石: 耐力 +1#n#G#r符石: 耐力 +1 命中 +4#n#r#cEE82EE符石组合: 天雷地火#r门派条件：天宫 #r部位条件：无#r使用天雷斩、雷霆万钧时增加人物等级/1.5的伤害，装备该组合时降低5%的防御，同时降低5%的气血，仅对NPC使用时有效#Y  ","iType":2708,]),25:(["cDesc":"#r等级 70  #r魔法 +80 防御 +39#r耐久度 637#r锻炼等级 6  镶嵌宝石 太阳石、 红玛瑙#r#G#G命中 +100#Y #G伤害 +16#Y#Y#r#c4DBAF4套装效果：附加状态逆鳞#Y#Y#r#G开运孔数：3孔/3孔#Y   ","iType":2508,]),]),"iMaxExpt1":20,"rent_level":1,"ori_desc":73,"iMaxExpt3":20,"iExptSki3":0,"iBeastSki3":4,"iNutsNum":8,"iUpExp":5248380,"iCor_All":126,"i3FlyLv":0,"ori_race":3,"TA_iAllPoint":0,"iBeastSki1":0,"iDex_All":181,"iExptSki1":7,"iSewski":0,])'
# desc = '(["total_horse":13,"fabao":([33:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G143#Y 五行：#G木#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y","iType":6075,]),17:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G362#Y 五行：#G水#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6023,]),48:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6060,]),13:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#c7D7E82（未生效）#Y","iType":6098,]),16:(["cDesc":"0#Y灵气：#G123#Y 五行：#G土#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6039,]),29:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G5#Y层 #c01FEC5移星换斗#Y","iType":6022,]),27:(["cDesc":"0#Y灵气：#G52 #Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y#r传送至魔王寨（32，30）","iType":6020,]),15:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G342#Y 五行：#G火#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6033,]),22:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G161#Y 五行：#G水#Y#r修炼境界：第#G13#Y层 #cFF6F28法力无边#Y","iType":6026,]),11:(["cDesc":"0#Y灵气：#G37 #Y 五行：#G木#Y#r修炼境界：第#G14#Y层 #cFF6F28返璞归真#Y#r#n#Y最佳五行属性奖励：触发时额外减少10点所受伤害#G（已生效）#Y","iType":6088,]),12:(["cDesc":"0#W【回合限制】8#r#Y#Y灵气：#G48 #Y 五行：#G金#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：回合限制缩短为7回合#G（已生效）#Y","iType":6091,]),18:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G188#Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6030,]),44:(["cDesc":"0#Y灵气：#G200#Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6067,]),41:(["cDesc":"0#Y灵气：#G56 #Y 五行：#G土#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6009,]),30:(["cDesc":"0#Y灵气：#G167#Y 五行：#G水#Y#r修炼境界：第#G9#Y层 #cFF6F28不堕轮回#Y","iType":6006,]),21:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G445#Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6028,]),38:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G50 #Y 五行：#G金#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6005,]),36:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G45 #Y 五行：#G金#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6015,]),32:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G190#Y 五行：#G水#Y#r修炼境界：第#G9#Y层 #cFF6F28不堕轮回#Y","iType":6018,]),24:(["cDesc":"0#Y灵气：#G500#Y 五行：#G水#Y#r修炼境界：第#G18#Y层 #cFF6F28浴火涅槃#Y#r#n#Y最佳五行属性奖励：额外增加1％封印命中率和1％抵抗封印命中率,地府不增加抗封#G（已生效）#Y","iType":6084,]),2:(["cDesc":"0#Y灵气：#G60 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6069,]),20:(["cDesc":"0#W【回合限制】15#r#Y#Y灵气：#G42 #Y 五行：#G木#Y#r修炼境界：第#G6#Y层 #cA6F101变幻莫测#Y#r#n#Y最佳五行属性奖励：额外减少1%的物理伤害#G（已生效）#Y","iType":6089,]),34:(["cDesc":"0#W【回合限制】6#r#Y#Y灵气：#G176#Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6029,]),14:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G土#Y#r修炼境界：第#G3#Y层 #cB7BFF8负海担山#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#c7D7E82（未生效）#Y","iType":6104,]),50:(["cDesc":"0#W【回合限制】1#r#Y#Y灵气：#G45 #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6062,]),49:(["cDesc":"0#Y灵气：#G1  #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6073,]),42:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6010,]),3:(["cDesc":"0#Y灵气：#G108#Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6066,]),46:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6059,]),39:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G500#Y 五行：#G土#Y#r修炼境界：第#G3#Y层 #cB7BFF8负海担山#Y","iType":6057,]),37:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G50 #Y 五行：#G金#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6014,]),19:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G500#Y 五行：#G水#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6019,]),40:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G500#Y 五行：#G火#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6017,]),35:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G300#Y 五行：#G火#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y","iType":6064,]),23:(["cDesc":"0#W【回合限制】1#r#Y#Y灵气：#G495#Y 五行：#G金#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6013,]),45:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G500#Y 五行：#G火#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6065,]),43:(["cDesc":"0#Y灵气：#G65 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6011,]),31:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G50 #Y 五行：#G火#Y#r修炼境界：第#G4#Y层 #c13E1EC预知福祸#Y","iType":6016,]),]),"iCor_All":120,"igoodness_sav":15971,"iSpe_All":119,"datang_feat":226,"iOrgOffer":0,"iZhuanZhi":0,"iMarry2":0,"iSchool":4,"iStr_All":120,"addPoint":12,"AllEquip":([189:(["cDesc":"等级 100#r抵抗封印等级 +21#r耐久度 289  修理失败 2次#r精炼等级 3#r#G抗物理暴击等级 +21 #cEE82EE[+24]#r#G气血 +78 #cEE82EE[+84]#r#G法术防御 +20 #cEE82EE[+24]#r#W制造者：Lonely小胖强化打造#","iType":27203,]),190:(["cDesc":"等级 100#r速度 +23#r耐久度 459#r精炼等级 3#r#G气血 +80 #cEE82EE[+84]#r#G法术防御 +29 #cEE82EE[+24]#r#W制造者：蓝翔灵饰＇强化打造#","iType":27303,]),21:(["iLock":1,"cDesc":"#r等级 105  #r命中率 +11%#r耐久度 535#r#G#G敏捷 +20#Y#Y#r#W制造者：风不正经τ#Y  ","iType":9311,]),]),"shenqi_pos":({0,0,}),"iIcon":2,"iBeastSki1":17,"commu_name":"","AllSummon":({(["ATK_MAX":1550,"hp":4060,"lianshou":0,"yuanxiao":0,"iCor_all":547,"left_qlxl":0,"summon_equip1":(["cDesc":"#r等级 115  #r命中率 +13% 伤害 +50#r耐久度 139#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4善恶有报#Y#Y#r#W制造者：哇灬丨陌黎丶#Y#r#r镶嵌效果 #r+70伤害 镶嵌等级：7","iType":9312,]),"iGenius":0,"jinjie":(["lx":110,"core":(["effect":"#Y进场时，若己方四个及以上单位处于被封印状态，则#G100%#Y解除我方所有单位异常状态；防御力下降#R26%#Y。","name":"逆境","fix_st":0,"id":721,]),"new_type":0,"cnt":7,]),"summon_equip4_desc":"#Y#r玄天灵力 378","sjg":0,"life":4628,"core_close":0,"iAtt_all":1689,"iRealColor":6,"iAtt_F":4,"lastchecksubzz":2018,"summon_color":1,"summon_equip2":(["cDesc":"#r等级 105  #r速度 +39 伤害 +56#r耐久度 87#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4善恶有报#Y#Y#r#W制造者：′雨ぺ夜◇#Y","iType":9211,]),"tmp_lingxing":110,"iType":102077,"iBaobao":1,"jj_extra_add":(["iMag":9,"iStr":8,"iSpe":9,"iCor":10,"iRes":11,]),"carrygradezz":0,"spe":785,"iMp_max":1135,"mp":2570,"ruyidan":0,"summon_equip4_type":3561,"all_skills":(["408":1,"403":1,"416":1,"425":1,"417":1,"411":1,"404":1,"401":1,"405":1,]),"att":1438,"MS_MAX":1800,"qianjinlu":6,"def":1146,"iSpe_all":138,"growthMax":1266,"grow":1266,"iRes_all":140,"dod":869,"iGrade":119,"iStr_all":600,"iMagDef_all":679,"iMag_all":138,"iHp":5012,"iDod_All":119,"HP_MAX":5500,"summon_core":([907:({5,0,([]),}),901:({5,0,([]),}),935:({5,0,([]),}),]),"iPoint":0,"DEF_MAX":1550,"csavezz":"1438|1146|785|869|4060|2570","SPD_MAX":1550,"summon_equip3":(["cDesc":"#r等级 105  #r气血 +70 防御 +82 伤害 +49#r耐久度 350#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4善恶有报#Y#Y#r#W制造者：剑煮酒°云溪#Y#r#r镶嵌效果 #r+210气血 镶嵌等级：7","iType":9111,]),"iMp":1135,"att_rate":13,"iDex_All":167,"iJjFeedCd":0,"iDef_All":634,"MP_MAX":3050,"iHp_max":5012,]),(["ATK_MAX":1550,"hp":3612,"lianshou":0,"yuanxiao":0,"iCor_all":528,"left_qlxl":0,"iGenius":0,"jinjie":(["lx":110,"core":(["effect":"#Y对召唤兽物理伤害结果增加#G20%#Y；对人物角色伤害结果减少#R59#Y。","name":"争锋","fix_st":0,"id":707,]),"new_type":0,"cnt":7,]),"summon_equip4_desc":"","sjg":0,"life":7941,"core_close":0,"iAtt_all":1448,"iRealColor":4,"iAtt_F":16,"lastchecksubzz":2018,"summon_color":1,"tmp_lingxing":110,"iType":102077,"iBaobao":1,"jj_extra_add":(["iMag":14,"iStr":11,"iSpe":8,"iCor":16,"iRes":11,]),"carrygradezz":0,"spe":1136,"iMp_max":938,"mp":1669,"ruyidan":0,"summon_equip4_type":0,"all_skills":(["403":1,"416":1,"425":1,"417":1,"411":1,"404":1,"401":1,"405":1,"422":1,"551":1,]),"att":1501,"MS_MAX":1800,"qianjinlu":7,"def":1055,"iSpe_all":139,"growthMax":1266,"grow":1262,"iRes_all":140,"dod":1247,"iGrade":119,"iStr_all":627,"iMagDef_all":655,"iMag_all":143,"iHp":4521,"iDod_All":173,"HP_MAX":5500,"summon_core":([907:({5,0,([]),}),919:({5,0,([]),}),901:({5,0,([]),}),]),"iPoint":0,"DEF_MAX":1550,"csavezz":"1501|1055|1136|1247|3612|1669","SPD_MAX":1550,"iMp":938,"att_rate":0,"iDex_All":177,"iJjFeedCd":0,"iDef_All":525,"MP_MAX":3050,"iHp_max":4521,]),(["ATK_MAX":1550,"hp":5177,"lianshou":0,"yuanxiao":0,"iCor_all":244,"left_qlxl":0,"summon_equip1":(["cDesc":"#r等级 105  #r命中率 +11%#r耐久度 252#r#G#G法力 +16#Y #G灵力 +7#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级法术暴击#Y#Y#r#W制造者：平淡江湖#Y#r#r镶嵌效果 #r+24灵力 镶嵌等级：6","iType":9311,]),"iGenius":429,"jinjie":(["lx":110,"core":(["effect":"#Y第二回合以后进场时，#G83%#Y概率对血量百分比最低的单位使用随机法术；气血上限降低#R10%#Y。（效果与魔力有关）","name":"瞬法","fix_st":0,"id":717,]),"new_type":0,"cnt":7,]),"summon_equip4_desc":"#r修理失败 1次#Y#r玄天灵力 355 （已染色）","sjg":0,"life":1004,"core_close":0,"iAtt_all":690,"iRealColor":5,"iAtt_F":16,"lastchecksubzz":2018,"summon_color":1,"summon_equip2":(["cDesc":"#r等级 105  #r速度 +26#r耐久度 101#r#G#G法力 +17#Y #G灵力 +7#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级法术暴击#Y#Y#r#r镶嵌效果 #r+30速度 镶嵌等级：5","iType":9211,]),"tmp_lingxing":110,"iType":102150,"iBaobao":1,"jj_extra_add":(["iMag":11,"iStr":8,"iSpe":12,"iCor":8,"iRes":8,]),"carrygradezz":0,"spe":1081,"iMp_max":4020,"mp":2421,"ruyidan":0,"summon_equip4_type":3578,"all_skills":(["578":1,"429":1,"424":1,"573":1,"661":1,"412":1,]),"att":1269,"MS_MAX":1800,"qianjinlu":6,"def":1465,"iSpe_all":141,"growthMax":1277,"grow":1210,"iRes_all":139,"dod":723,"iGrade":119,"iStr_all":137,"iMagDef_all":1018,"iMag_all":949,"iHp":2368,"iDod_All":101,"HP_MAX":5500,"summon_core":([928:({5,0,([]),}),936:({5,0,([]),}),904:({5,0,([]),}),906:({5,0,([]),}),]),"iPoint":0,"DEF_MAX":1550,"csavezz":"1269|1465|1081|723|5177|2421","SPD_MAX":1550,"summon_equip3":(["cDesc":"#r等级 105  #r防御 +70#r耐久度 232#r#G#G法力 +14#Y #G灵力 +9#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级法术暴击#Y#Y#r#W制造者：我有辣条约吗#Y#r#r镶嵌效果 #r+150气血 镶嵌等级：5","iType":9111,]),"iMp":4020,"att_rate":11,"iDex_All":208,"iJjFeedCd":0,"iDef_All":691,"MP_MAX":3050,"iHp_max":2368,]),(["ATK_MAX":1550,"hp":4455,"lianshou":0,"yuanxiao":0,"iCor_all":510,"left_qlxl":0,"iGenius":0,"jinjie":(["lx":110,"core":(["effect":"#Y对召唤兽物理伤害结果增加#G20%#Y；对人物角色伤害结果减少#R115#Y。","name":"争锋","fix_st":0,"id":707,]),"new_type":0,"cnt":7,]),"summon_equip4_desc":"","sjg":0,"life":38486,"core_close":0,"iAtt_all":1200,"iRealColor":6,"iAtt_F":1,"lastchecksubzz":2018,"summon_color":1,"tmp_lingxing":110,"iType":102077,"iBaobao":1,"jj_extra_add":(["iMag":14,"iStr":16,"iSpe":9,"iCor":11,"iRes":10,]),"carrygradezz":0,"spe":1462,"iMp_max":1045,"mp":2254,"ruyidan":0,"summon_equip4_type":0,"all_skills":(["403":1,"416":1,"425":1,"411":1,"422":1,"595":1,"401":1,"434":1,]),"att":1554,"MS_MAX":1800,"qianjinlu":9,"def":1349,"iSpe_all":195,"growthMax":1266,"iLock":1,"grow":1265,"iRes_all":135,"dod":1881,"iGrade":115,"iStr_all":430,"iMagDef_all":584,"iMag_all":139,"iHp":4474,"iDod_All":366,"HP_MAX":5500,"summon_core":([907:({5,0,([]),}),901:({5,0,([]),}),935:({1,1,([]),}),]),"iPoint":130,"DEF_MAX":1550,"csavezz":"1554|1349|1462|1881|4122|2254","SPD_MAX":1550,"iMp":1045,"att_rate":0,"iDex_All":305,"iJjFeedCd":0,"iDef_All":587,"MP_MAX":3050,"iHp_max":4474,]),(["ATK_MAX":1550,"hp":3788,"lianshou":0,"yuanxiao":0,"iCor_all":335,"left_qlxl":0,"summon_equip1":(["cDesc":"#r等级 105  #r命中率 +14% 伤害 +50#r耐久度 289#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4善恶有报#Y#Y#r#W制造者：浅浅依恋．#Y#r#r镶嵌效果 #r+60伤害 镶嵌等级：6","iType":9311,]),"iGenius":0,"jinjie":(["lx":110,"core":(["effect":"#Y忽略人物角色#G158#Y防御力；对召唤兽物理伤害结果减少#R5%#Y。","name":"力破","fix_st":0,"id":706,]),"new_type":0,"cnt":7,]),"summon_equip4_desc":"#Y#r玄天灵力 35 （已染色）","sjg":0,"life":9283,"core_close":0,"iAtt_all":1993,"iRealColor":6,"iAtt_F":1,"lastchecksubzz":2018,"summon_color":1,"summon_equip2":(["cDesc":"#r等级 105  #r速度 +35 伤害 +46#r耐久度 269#r#G#G灵力 +11#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4善恶有报#Y#Y#r#W制造者：悬壶济世一X#Y#r#r镶嵌效果 #r+6速度 镶嵌等级：1","iType":9211,]),"tmp_lingxing":110,"iType":102077,"iBaobao":1,"jj_extra_add":(["iMag":11,"iStr":16,"iSpe":10,"iCor":15,"iRes":12,]),"carrygradezz":0,"spe":1555,"iMp_max":999,"mp":1969,"ruyidan":0,"summon_equip4_type":3561,"all_skills":(["408":1,"416":1,"425":1,"411":1,"404":1,"401":1,"434":1,"405":1,"422":1,]),"att":1550,"MS_MAX":1800,"qianjinlu":6,"def":1449,"iSpe_all":139,"growthMax":1266,"grow":1266,"iRes_all":141,"dod":1114,"iGrade":119,"iStr_all":825,"iMagDef_all":696,"iMag_all":140,"iHp":3238,"iDod_All":154,"HP_MAX":5500,"summon_core":([907:({5,0,([]),}),901:({5,0,([]),}),935:({5,0,([]),}),]),"iPoint":0,"DEF_MAX":1550,"csavezz":"1550|1389|1555|1114|3788|1969","SPD_MAX":1550,"summon_equip3":(["cDesc":"#r等级 105  #r防御 +77 伤害 +48#r耐久度 533#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4善恶有报#Y#Y#r#W制造者：′思想亦裸奔#Y#r#r镶嵌效果 #r+150气血 镶嵌等级：5","iType":9111,]),"iMp":999,"att_rate":14,"iDex_All":277,"iJjFeedCd":0,"iDef_All":715,"MP_MAX":3050,"iHp_max":3238,]),(["ATK_MAX":1550,"hp":3546,"lianshou":0,"yuanxiao":0,"iCor_all":153,"left_qlxl":0,"summon_equip1":(["cDesc":"#r等级 105  #r命中率 +15%#r耐久度 109#r#G#G灵力 +7#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级法术连击#Y#Y#r#W制造者：我是小妞妞〃#Y#r#r镶嵌效果 #r+24灵力 镶嵌等级：6","iType":9311,]),"iGenius":426,"jinjie":(["lx":107,"core":(["effect":"#Y第二回合以后进场时，#G100%#Y概率对血量百分比最低的单位使用随机法术；气血上限降低#R10%#Y。（效果与魔力有关）","name":"瞬法","fix_st":0,"id":717,]),"new_type":1,"cnt":7,]),"summon_equip4_desc":"#Y#r玄天灵力 726","sjg":0,"life":7020,"core_close":0,"iAtt_all":778,"iRealColor":5,"iAtt_F":8,"lastchecksubzz":2018,"summon_color":1,"summon_equip2":(["cDesc":"#r等级 95  #r速度 +31 伤害 +42#r耐久度 222#r#G#G灵力 +10#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级法术连击#Y#Y#r#W制造者：月饮沉风#Y#r#r镶嵌效果 #r+24速度 镶嵌等级：4","iType":9210,]),"tmp_lingxing":107,"iType":102198,"iBaobao":1,"jj_extra_add":0,"carrygradezz":0,"spe":1307,"iMp_max":4161,"mp":2332,"ruyidan":0,"summon_equip4_type":27436,"all_skills":(["578":1,"424":1,"573":1,"661":1,"577":1,"426":1,]),"att":1346,"MS_MAX":1800,"qianjinlu":6,"def":1000,"iSpe_all":139,"growthMax":1266,"iLock":1,"grow":1242,"iRes_all":129,"dod":1017,"iGrade":119,"iStr_all":129,"iMagDef_all":992,"iMag_all":968,"iHp":1432,"iDod_All":141,"HP_MAX":5500,"summon_core":([928:({5,0,([]),}),906:({5,0,([]),}),936:({5,0,([]),}),]),"iPoint":0,"DEF_MAX":1550,"csavezz":"1346|892|1127|1017|3546|2332","SPD_MAX":1550,"summon_equip3":(["cDesc":"#r等级 105  #r防御 +99#r耐久度 279#r#G#G法力 +8#Y #G灵力 +11#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级法术连击#Y#Y#r#W制造者：名字30667914#Y#r#r镶嵌效果 #r+30气血 镶嵌等级：1","iType":9111,]),"iMp":4161,"att_rate":15,"iDex_All":236,"iJjFeedCd":0,"iDef_All":586,"MP_MAX":3050,"iHp_max":1432,]),(["ATK_MAX":1550,"hp":4421,"lianshou":0,"yuanxiao":0,"iCor_all":540,"left_qlxl":0,"summon_equip1":(["cDesc":"#r等级 75  #r命中率 +9% 气血 +52#r耐久度 530#r#G#G法力 +9#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：不离不弃ミ染#Y","iType":9308,]),"iGenius":0,"jinjie":(["lx":110,"core":(["effect":"#Y在场时，我方所有单位物理防御增加#G36#Y；自身受到的法术伤害增加#R18%#Y。（效果与敏捷有关）","name":"抗物","fix_st":0,"id":705,]),"new_type":0,"cnt":7,]),"summon_equip4_desc":"","sjg":0,"life":3756,"core_close":0,"iAtt_all":666,"iRealColor":4,"iAtt_F":1,"lastchecksubzz":2018,"summon_color":1,"summon_equip2":(["cDesc":"#r等级 75  #r速度 +27#r耐久度 113#r#G#G体质 +6#Y #G耐力 +11#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#r镶嵌效果 #r+30速度 镶嵌等级：5","iType":9208,]),"tmp_lingxing":110,"iType":102078,"iBaobao":1,"jj_extra_add":(["iMag":10,"iStr":10,"iSpe":13,"iCor":9,"iRes":14,]),"carrygradezz":0,"spe":1413,"iMp_max":1199,"mp":2598,"ruyidan":0,"summon_equip4_type":0,"all_skills":(["579":1,"418":1,"435":1,"422":1,]),"att":1170,"MS_MAX":1800,"qianjinlu":6,"def":1542,"iSpe_all":556,"growthMax":1266,"grow":1258,"iRes_all":221,"dod":982,"iGrade":119,"iStr_all":139,"iMagDef_all":528,"iMag_all":154,"iHp":5497,"iDod_All":545,"HP_MAX":5500,"summon_core":([907:({5,0,([]),}),916:({5,0,([]),}),904:({5,0,([]),}),]),"iPoint":0,"DEF_MAX":1550,"csavezz":"1170|1492|1413|982|4421|2598","SPD_MAX":1550,"summon_equip3":(["cDesc":"#r等级 75  #r防御 +75#r耐久度 148#r#G#G法力 +6#Y #G耐力 +6#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：Dream″妖娆#Y#r#r镶嵌效果 #r+180气血 镶嵌等级：6","iType":9108,]),"iMp":1199,"att_rate":9,"iDex_All":852,"iJjFeedCd":0,"iDef_All":870,"MP_MAX":3050,"iHp_max":5497,]),(["ATK_MAX":1550,"hp":4084,"lianshou":0,"yuanxiao":0,"iCor_all":150,"left_qlxl":0,"summon_equip1":(["cDesc":"#r等级 105  #r命中率 +16% 伤害 +55#r耐久度 318#r#G#G力量 +12#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：丿神话丶小彬#Y#r#r镶嵌效果 #r+70伤害 镶嵌等级：7","iType":9311,]),"iGenius":0,"jinjie":(["lx":110,"core":(["effect":"#Y第二回合以后进场时，#G100%#Y概率对气血百分比最低的单位发动一次攻击；气血上限降低#R8%#Y。","name":"瞬击","fix_st":0,"id":716,]),"new_type":0,"cnt":7,]),"summon_equip4_desc":"","sjg":0,"life":943,"core_close":0,"iAtt_all":2165,"iRealColor":6,"iAtt_F":8,"lastchecksubzz":2018,"summon_color":1,"summon_equip2":(["cDesc":"#r等级 105  #r速度 +33 伤害 +45#r耐久度 285#r#G#G力量 +21#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：保持似水年华#Y#r#r镶嵌效果 #r+54速度 镶嵌等级：9","iType":9211,]),"tmp_lingxing":110,"iType":102077,"iBaobao":1,"jj_extra_add":(["iMag":10,"iStr":12,"iSpe":15,"iCor":15,"iRes":8,]),"carrygradezz":0,"spe":1426,"iMp_max":938,"mp":1696,"ruyidan":0,"summon_equip4_type":0,"all_skills":(["416":1,"425":1,"571":1,"422":1,"401":1,"434":1,"413":1,]),"att":1593,"MS_MAX":1800,"qianjinlu":6,"def":902,"iSpe_all":283,"growthMax":1266,"grow":1284,"iRes_all":137,"dod":1547,"iGrade":119,"iStr_all":911,"iMagDef_all":652,"iMag_all":139,"iHp":1789,"iDod_All":437,"HP_MAX":5500,"summon_core":([907:({5,0,([]),}),901:({5,0,([]),}),935:({5,0,([]),}),]),"iPoint":0,"DEF_MAX":1550,"csavezz":"1593|902|1426|1547|4084|1696","SPD_MAX":1550,"summon_equip3":(["cDesc":"#r等级 115  #r防御 +105 伤害 +51#r耐久度 395#r#G#G力量 +11#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：′夕颜沁墨痕#Y#r#r镶嵌效果 #r+210气血 镶嵌等级：7","iType":9112,]),"iMp":938,"att_rate":16,"iDex_All":510,"iJjFeedCd":0,"iDef_All":588,"MP_MAX":3050,"iHp_max":1789,]),(["ATK_MAX":1550,"hp":3529,"lianshou":0,"yuanxiao":0,"iCor_all":155,"left_qlxl":0,"summon_equip1":(["cDesc":"#r等级 95  #r命中率 +16%#r耐久度 520#r#G#G法力 +10#Y #G灵力 +11#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级法术暴击#Y#Y#r#W制造者：关不上的窗ペ#Y#r#r镶嵌效果 #r+24灵力 镶嵌等级：6","iType":9310,]),"iGenius":428,"jinjie":(["lx":110,"core":(["effect":"#Y第二回合以后进场时，#G83%#Y概率对血量百分比最低的单位使用随机法术；气血上限降低#R17%#Y。（效果与魔力有关）","name":"瞬法","fix_st":0,"id":717,]),"new_type":1,"cnt":7,]),"summon_equip4_desc":"#Y#r玄天灵力 769","sjg":0,"life":6668,"core_close":0,"iAtt_all":584,"iRealColor":5,"iAtt_F":4,"lastchecksubzz":2018,"summon_color":1,"summon_equip2":(["cDesc":"#r等级 115  #r速度 +38#r耐久度 496#r#G#G法力 +16#Y #G力量 +18#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级法术暴击#Y#Y#r#W制造者：一个人WU#Y#r#r镶嵌效果 #r+30速度 镶嵌等级：5","iType":9212,]),"tmp_lingxing":110,"iType":102198,"iBaobao":1,"jj_extra_add":(["iMag":9,"iStr":11,"iSpe":10,"iCor":6,"iRes":7,]),"carrygradezz":0,"spe":1113,"iMp_max":4386,"mp":2774,"ruyidan":0,"summon_equip4_type":27436,"all_skills":(["578":1,"424":1,"428":1,"573":1,"661":1,"411":1,]),"att":880,"MS_MAX":1800,"qianjinlu":0,"def":943,"iSpe_all":151,"growthMax":1266,"grow":1231,"iRes_all":136,"dod":893,"iGrade":119,"iStr_all":178,"iMagDef_all":1051,"iMag_all":1009,"iHp":1500,"iDod_All":134,"HP_MAX":5500,"summon_core":([928:({1,0,([]),}),936:({5,0,([]),}),904:({5,0,([]),}),]),"iPoint":0,"DEF_MAX":1550,"csavezz":"880|943|844|893|3393|2774","SPD_MAX":1550,"summon_equip3":(["cDesc":"#r等级 105  #r防御 +74#r耐久度 404#r#G#G法力 +12#Y #G力量 +20#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级法术暴击#Y#Y#r#W制造者：只为跳跳萌宝#Y#r#r镶嵌效果 #r+150气血 镶嵌等级：5","iType":9111,]),"iMp":4386,"att_rate":16,"iDex_All":236,"iJjFeedCd":0,"iDef_All":553,"MP_MAX":3050,"iHp_max":1500,]),}),"iBeastSki4":17,"iSumAmountEx":1,"usernum":1315,"outdoor_level":5,"idbid_desc":({100,1,}),"shenqi":(["active":0,"skill_desc":"","skill":0,"skill_level":1,"components":({(["wuxing":({(["status":0,"attr":"气血 +21","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":1,"id":2,]),(["status":0,"attr":"气血 +21","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":1,"id":2,]),(["status":0,"attr":"法术伤害 +3","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":1,"id":16,]),(["status":0,"attr":"封印命中 +3","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":1,"id":8,]),}),"level":1,"unlock":1,]),(["wuxing":({(["status":0,"attr":"抵抗封印 +0","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":0,"id":4,]),(["status":0,"attr":"封印命中 +0","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":0,"id":8,]),(["status":0,"attr":"封印命中 +0","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":0,"id":8,]),(["status":0,"attr":"气血 +0","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":0,"id":2,]),}),"level":0,"unlock":0,]),(["wuxing":({(["status":0,"attr":"抵抗封印 +0","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":0,"id":4,]),(["status":0,"attr":"抵抗封印 +0","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":0,"id":4,]),(["status":0,"attr":"法术伤害 +0","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":0,"id":16,]),(["status":0,"attr":"封印命中 +0","wuxingshi_affix":0,"affix_disable":0,"wuxingshi_level":0,"id":8,]),}),"level":0,"unlock":0,]),}),"full":0,"power":20,"attributes":({(["disable":1,"attr":"速度 +0","id":1,]),(["disable":0,"attr":"气血 +42","id":2,]),(["disable":0,"attr":"封印命中 +3","id":8,]),(["disable":0,"attr":"法术伤害 +3","id":16,]),(["disable":1,"attr":"抵抗封印 +0","id":4,]),}),"id":6206,]),"all_skills":(["50502":1,"167":1,"201":129,"164":3,"230":36,"174":1,"13":119,"160":3,"52031":1,"210":100,"154":6,"212":120,"211":120,"155":6,"231":80,"216":129,"206":141,"205":101,"237":27,"163":1,"209":100,"204":107,"197":3,"52016":1,"207":88,"23806":1,"153":1,"162":1,"173":1,"203":50,"52032":1,"15":119,"11":119,"217":100,"9":119,"14":119,"175":1,"179":1,"198":1,"202":120,"218":100,"208":140,"23802":1,"10":119,"170":7,"159":1,"165":3,"169":1,"12":119,"168":1,"196":1,"166":1,"23808":1,]),"iLearnCash":4881744,"ori_desc":199,"iMarry":14533798,"ExAvt":([70:(["order":3,"iType":12514,"cName":"青花瓷·月白",]),22:(["order":4,"iType":13691,"cName":"萌草发卡",]),58:(["order":17,"iType":12394,"cName":"云渺河汉",]),38:(["order":9,"iType":12652,"cName":"青花瓷",]),93:(["order":10,"iType":12850,"cName":"冰雪玉兔",]),2:(["order":11,"iType":13512,"cName":"夜之孤煞",]),68:(["order":12,"iType":12648,"cName":"青花瓷·月白",]),72:(["order":14,"iType":12498,"cName":"冰寒绡",]),34:(["order":16,"iType":12424,"cName":"兰陵魅影",]),92:(["order":2,"iType":40108,"cName":"冰雪玉兔",]),1:(["order":1,"iType":12246,"cName":"夜之孤煞",]),3:(["order":5,"iType":13983,"cName":"夜之孤煞",]),55:(["order":20,"iType":13320,"cName":"隐者草帽",]),37:(["order":7,"iType":12646,"cName":"青花瓷",]),39:(["order":6,"iType":12512,"cName":"青花瓷",]),35:(["order":19,"iType":12628,"cName":"西域游侠（下衣）",]),4:(["order":15,"iType":14404,"cName":"蓝色妖姬",]),73:(["order":8,"iType":13790,"cName":"冰寒绡",]),45:(["order":18,"iType":13408,"cName":"荒原游侠",]),69:(["order":13,"iType":12654,"cName":"青花瓷·月白",]),]),"iGoodness":2453,"iNutsNum":100,"ExpJwBase":1000000000,"ori_race":1,"iGrade":109,"iExptSki1":5,"icolor_ex":32,"pet":({(["all_skills":({(["value":1,"name":"灵佑",]),}),"iType":4068,"cName":"小象精灵",]),(["all_skills":({(["value":1,"name":"灵佑",]),}),"iType":4069,"cName":"白泽精灵",]),}),"iExptSki3":17,"cName":"朝三晚四τ","iHp":3269,"iSmithski":514,"iHp_Eff":3384,"iPoint":0,"TA_iAllPoint":0,"iDamage_All":514,"HeroScore":1176,"iMagDef_All":792,"iCGTotalAmount":120,"iDex_All":182,"iPride":800,"iMp_Max":5495,"iMaxExpt4":20,"iRace":1,"iCGBodyAmount":30,"iAtt_All":270,"HugeHorse":([161:(["iSkillLevel":0,"iSkill":0,"order":7,"nosale":1,"iType":11150,"cName":"粉红小驴",]),14:(["iSkillLevel":0,"iSkill":0,"order":4,"nosale":0,"iType":11014,"cName":"沉星寒犀",]),119:(["iSkillLevel":0,"iSkill":0,"order":3,"nosale":0,"iType":11116,"cName":"轻云羊驼",]),293:(["iSkillLevel":0,"iSkill":0,"order":6,"nosale":1,"iType":11285,"cName":"九尾冰狐",]),147:(["iSkillLevel":1,"iSkill":622,"order":1,"nosale":1,"iType":11137,"cName":"天使猪猪",]),234:(["iSkillLevel":0,"iSkill":0,"order":2,"nosale":0,"iType":11223,"cName":"野趣灵菇",]),386:(["iSkillLevel":0,"iSkill":0,"order":9,"nosale":1,"iType":11360,"cName":"冰晶雪魄",]),67:(["iSkillLevel":0,"iSkill":0,"order":5,"nosale":1,"iType":11067,"cName":"妙缘暖犀",]),97:(["iSkillLevel":1,"iSkill":622,"order":4,"nosale":1,"iType":11096,"cName":"七彩小驴",]),368:(["iSkillLevel":0,"iSkill":0,"order":3,"nosale":1,"iType":11357,"cName":"冰晶魅灵",]),113:(["iSkillLevel":0,"iSkill":0,"order":1,"nosale":0,"iType":11098,"cName":"流云玉佩",]),127:(["iSkillLevel":0,"iSkill":0,"order":8,"nosale":1,"iType":11124,"cName":"九幽灵虎",]),170:(["iSkillLevel":0,"iSkill":0,"order":2,"nosale":1,"iType":11031,"cName":"神行小驴",]),]),"iTotalMagDef_all":889,"iMag_All":806,"iUpExp":438284196,"AchPointTotal":6184,"iRes_All":119,"changesch":({4,13,4,13,}),"normal_horse":4,"rent_level":1,"iSchOffer":10031,"iExptSki5":5,"iBadness":0,"shenqi_yellow":"","cOrg":"","iBeastSki2":17,"iErrantry":0,"propKept":([1:(["iMag":119,"iStr":119,"iSpe":808,"iCor":119,"iRes":119,]),2:(["iMag":119,"iStr":119,"iSpe":275,"iCor":306,"iRes":465,]),0:(["iMag":806,"iStr":120,"iSpe":119,"iCor":120,"iRes":119,]),]),"iPcktPage":1,"bid":1,"farm_level":0,"commu_gid":0,"iSewski":874,"ExpJw":0,"iBeastSki3":17,"sword_score":1000,"energy":838,"TA_iAllNewPoint":3,"iDesc":0,"AllRider":([12:(["all_skills":([]),"iGrade":0,"mattrib":"","exgrow":10625,"ExtraGrow":0,"iType":501,]),11:(["all_skills":([]),"iGrade":0,"mattrib":"","exgrow":10892,"ExtraGrow":0,"iType":500,]),8:(["all_skills":([602:2,603:3,]),"iGrade":125,"mattrib":"耐力","exgrow":23001,"ExtraGrow":100,"iType":504,]),5:(["all_skills":([]),"iGrade":7,"mattrib":"敏捷","exgrow":12647,"ExtraGrow":0,"iType":509,]),4:(["all_skills":([600:3,601:1,608:1,]),"iGrade":125,"mattrib":"体质","exgrow":23033,"ExtraGrow":100,"iType":504,]),6:(["all_skills":([600:3,605:2,]),"iGrade":125,"mattrib":"魔力","exgrow":22635,"ExtraGrow":100,"iType":505,]),]),"iExptSki4":17,"sum_exp":126,"jiyuan":27,"xianyu":30,"iTotalMagDam_all":792,"iDod_All":508,"iExptSki2":17,"iMaxExpt1":20,"iSumAmount":9,"total_avatar":93,"more_attr":(["attrs":({(["lv":0,"idx":11,]),(["lv":45,"idx":9,]),(["lv":0,"idx":10,]),(["lv":21,"idx":2,]),(["lv":0,"idx":8,]),(["lv":0,"idx":1,]),(["lv":0,"idx":12,]),(["lv":0,"idx":7,]),(["lv":0,"idx":6,]),(["lv":0,"idx":5,]),(["lv":0,"idx":4,]),(["lv":0,"idx":3,]),(["lv":508,"idx":13,]),(["lv":792,"idx":14,]),}),]),"i3FlyLv":0,"iHp_Max":3586,"rent":21953689,"iMp":2703,"iDef_All":395,"iMaxExpt3":20,"iCash":1353078,"iCGBoxAmount":4,"iMaxExpt2":20,"iSaving":0,"iSkiPoint":0,])'
# desc = '(["propKept":([1:(["iRes":187,"iStr":1336,"iCor":187,"iMag":180,"iSpe":185,]),0:(["iRes":187,"iStr":186,"iCor":187,"iMag":1330,"iSpe":185,]),]),"igoodness_sav":4549,"iGrade":175,"iMaxExpt4":25,"rent_level":5,"iSumAmount":10,"ExpJw":0,"iDamage_All":2967,"iPride":800,"commu_gid":0,"iAtt_All":3548,"ori_desc":5859,"iTotalMagDam_all":1539,"iPoint":0,"iMp_Max":3129,"iSumAmountEx":2,"iMagDef_All":1257,"addPoint":40,"changesch":({2,4,2,4,2,1,4,2,15,7,5,7,2,15,4,2,5,}),"HugeHorse":([97:(["iSkillLevel":1,"iSkill":623,"order":2,"iType":11096,"nosale":1,"cName":"七彩小驴",]),38:(["iSkillLevel":0,"iSkill":0,"order":4,"iType":11038,"nosale":0,"cName":"瑞彩祥云",]),113:(["iSkillLevel":0,"iSkill":0,"order":1,"iType":11098,"nosale":0,"cName":"流云玉佩",]),31:(["iSkillLevel":0,"iSkill":0,"order":1,"iType":11031,"nosale":1,"cName":"神行小驴",]),69:(["iSkillLevel":0,"iSkill":0,"order":3,"iType":11069,"nosale":0,"cName":"叠彩仙蜗",]),24:(["iSkillLevel":0,"iSkill":0,"order":2,"iType":11024,"nosale":0,"cName":"璇彩灵仙",]),]),"iLearnCash":23829781,"usernum":38058980,"iNutsNum":200,"iZhuanZhi":2,"iPcktPage":1,"ori_race":1,"xianyu":440,"normal_horse":4,"child":(["iDod_All":23,"iHp_max":410,"iGrade":5,"iAtt_F":1,"iMagDef_all":52,"life":65432,"qianjinlu":0,"all_skills":(["412":1,"410":1,"568":1,"560":1,]),"mp":1775,"att_rate":0,"dl":0,"iDef_All":60,"iPoint":0,"iRes_all":25,"iMp":112,"lm":0,"iMagDam_all":52,"wl":0,"desc":0,"iStr_all":25,"iMp_max":112,"iAtt_all":46,"nl":0,"iCor_all":50,"grow":1273,"iMag_all":25,"def":1603,"iType":100106,"change_598_times":0,"att":992,"child_sixwx":0,"dod":954,"iHp":410,"school":6,"hp":5860,"iSpe_all":25,"spe":979,"yuanxiao":0,"iBaobao":1,"isnew":0,"ruyidan":0,"ending":0,"gg":0,"zl":0,"iDex_All":24,]),"iHp_Eff":4886,"iRes_All":189,"fabao":([33:(["cDesc":"0#Y灵气：#G300#Y 五行：#G水#Y#r修炼境界：第#G10#Y层 #cFF6F28道满根归#Y","iType":6073,]),15:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G500#Y 五行：#G水#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6019,]),26:(["cDesc":"0#Y灵气：#G500#Y 五行：#G水#Y#r修炼境界：第#G12#Y层 #cFF6F28笑傲西游#Y#r#n#Y最佳五行属性奖励：额外增加1％封印命中率和1％抵抗封印命中率,地府不增加抗封#G（已生效）#Y","iType":6084,]),29:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G500#Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6057,]),44:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：起效次数增加1次#c7D7E82（未生效）#Y","iType":6086,]),21:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G500#Y 五行：#G火#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6023,]),30:(["cDesc":"0#Y灵气：#G500#Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6063,]),32:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G300#Y 五行：#G木#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y","iType":6061,]),36:(["cDesc":"0#W【回合限制】1#r#Y#Y灵气：#G500#Y 五行：#G土#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6013,]),2:(["cDesc":"0#Y灵气：#G500#Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y#r#n#Y最佳五行属性奖励：额外增加5点速度#c7D7E82（未生效）#Y","iType":6094,]),24:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G500#Y 五行：#G火#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6033,]),34:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G288#Y 五行：#G水#Y#r修炼境界：第#G9#Y层 #cFF6F28不堕轮回#Y","iType":6021,]),47:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G土#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#c7D7E82（未生效）#Y","iType":6099,]),42:(["cDesc":"0#W【回合限制】150#r#Y#Y灵气：#G50 #Y 五行：#G土#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#c7D7E82（未生效）#Y","iType":6107,]),39:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6011,]),4:(["cDesc":"0#Y灵气：#G475#Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6046,]),23:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G500#Y 五行：#G火#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6017,]),40:(["cDesc":"0#W【回合限制】15#r#Y#Y灵气：#G8  #Y 五行：#G火#Y#r修炼境界：第#G3#Y层 #cB7BFF8负海担山#Y#r#n#Y最佳五行属性奖励：额外减少1%的物理伤害#c7D7E82（未生效）#Y","iType":6089,]),43:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加召唤兽等级*3％的物抗和法抗#c7D7E82（未生效）#Y","iType":6083,]),17:(["cDesc":"0#Y灵气：#G496#Y 五行：#G木#Y#r修炼境界：第#G18#Y层 #cFF6F28浴火涅槃#Y#r#n#Y最佳五行属性奖励：触发时额外减少10点所受伤害#G（已生效）#Y","iType":6088,]),13:(["cDesc":"0#Y灵气：#G500#Y 五行：#G金#Y#r修炼境界：第#G13#Y层 #cFF6F28法力无边#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#G（已生效）#Y","iType":6101,]),16:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#c7D7E82（未生效）#Y","iType":6106,]),27:(["cDesc":"0#W【回合限制】8#r#Y#Y灵气：#G500#Y 五行：#G金#Y#r修炼境界：第#G18#Y层 #cFF6F28浴火涅槃#Y#r#n#Y最佳五行属性奖励：回合限制缩短为7回合#G（已生效）#Y","iType":6090,]),22:(["cDesc":"0#W【回合限制】8#r#Y#Y灵气：#G500#Y 五行：#G金#Y#r修炼境界：第#G18#Y层 #cFF6F28浴火涅槃#Y#r#n#Y最佳五行属性奖励：回合限制缩短为7回合#G（已生效）#Y","iType":6091,]),11:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G土#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#c7D7E82（未生效）#Y","iType":6105,]),12:(["cDesc":"0#Y灵气：#G292#Y 五行：#G木#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y","iType":6072,]),18:(["cDesc":"0#Y灵气：#G46 #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#c7D7E82（未生效）#Y","iType":6102,]),41:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外造成10点伤害#c7D7E82（未生效）#Y","iType":6093,]),20:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G500#Y 五行：#G水#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6028,]),14:(["cDesc":"0#Y灵气：#G500#Y 五行：#G木#Y#r修炼境界：第#G14#Y层 #cFF6F28返璞归真#Y#r#n#Y最佳五行属性奖励：额外提升3点法术伤害#c7D7E82（未生效）#Y","iType":6097,]),1:(["cDesc":"0#Y灵气：#G158#Y 五行：#G土#Y#r修炼境界：第#G18#Y层 #cFF6F28浴火涅槃#Y#r#n#Y最佳五行属性奖励：额外提升5点物理伤害#c7D7E82（未生效）#Y","iType":6096,]),28:(["cDesc":"0#Y灵气：#G500#Y 五行：#G土#Y#r修炼境界：第#G18#Y层 #cFF6F28浴火涅槃#Y#r#n#Y最佳五行属性奖励：额外增加5点治疗量#G（已生效）#Y","iType":6095,]),50:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#G（已生效）#Y","iType":6103,]),49:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外降低目标2％物理命中率#c7D7E82（未生效）#Y","iType":6092,]),25:(["cDesc":"0#Y灵气：#G500#Y 五行：#G土#Y#r修炼境界：第#G14#Y层 #cFF6F28返璞归真#Y#r传送至大唐境外（629，75）","iType":6020,]),37:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G金#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#G（已生效）#Y","iType":6100,]),19:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G485#Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6030,]),35:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G384#Y 五行：#G金#Y#r修炼境界：第#G9#Y层 #cFF6F28不堕轮回#Y","iType":6015,]),45:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G金#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#c7D7E82（未生效）#Y","iType":6104,]),31:(["cDesc":"0#Y灵气：#G500#Y 五行：#G水#Y#r修炼境界：第#G18#Y层 #cFF6F28浴火涅槃#Y#r#n#Y最佳五行属性奖励：额外增加召唤兽等级*3％的物攻和法攻#G（已生效）#Y","iType":6082,]),]),"AllSummon":({}),"iHp":4881,"AllEquip":([187:(["cDesc":"等级 100#r伤害 +20#r耐久度 86#r精炼等级 8#r#G速度 +8 #cEE82EE[+24]#r#G伤害 +10 #cEE82EE[+32]#r#G伤害 +10 #cEE82EE[+32]#r#W制造者：＊专出极品＂强化打造#","iLockNew":9,"iType":27003,]),188:(["cDesc":"等级 100#r法术防御 +25#r耐久度 97#r精炼等级 8#r#G伤害 +13 #cEE82EE[+32]#r#G速度 +8 #cEE82EE[+24]#r#G伤害 +10 #cEE82EE[+32]#r#W制造者：你的一言一语强化打造#","iLockNew":9,"iType":27103,]),9:(["cDesc":"#r等级 120  五行 火#r#r敏捷 +53 防御 +65#r耐久度 231#r锻炼等级 8  镶嵌宝石 黑宝石#r#G#G速度 +64#Y#r#G临时速度 122 12/30 16:09#Y#r#c4DBAF4特效：#c4DBAF4永不磨损#Y#r#c4DBAF4套装效果：附加状态逆鳞#Y#Y#r#G开运孔数：4孔/4孔#G#r符石: 命中 +4#n#G#r符石: 力量 +1#n#G#r符石: 魔力 +1#n#G#r符石: 敏捷 +1 法术防御 +2#n#r#cEE82EE符石组合: 烟雨飘摇#r门派条件：五庄观 #r部位条件：无#r使用烟雨剑法、飘渺式时增加人物等级*1的伤害，装备该组合时降低5%的防御，同时降低5%的气血，仅对NPC使用时有效#Y#r#W制造者：′鸟人#Y#r#Y熔炼效果：#r#Y#r+2防御#Y  ","iLockNew":9,"iType":2754,]),2:(["cDesc":"#r等级 130  五行 火#r#r防御 +431#r耐久度 150#r锻炼等级 13  镶嵌宝石 月亮石#r#G#G力量 +29#Y #G敏捷 +29#Y#Y#r#c4DBAF4套装效果：追加法术满天花雨#Y#Y#r#G开运孔数：5孔/5孔#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r星位：伤害 +2.5#n#G#r星相互合：耐力 +2#r#cEE82EE符石组合: 生死搏符石#r门派条件：狮驼岭 #r部位条件：铠甲/女衣 #r增加门派技能生死搏6级#Y#r#W制造者：′帅帅猫咪°强化打造#Y  ","iLockNew":9,"iType":2655,]),6:(["cDesc":"#r等级 160  五行 土#r#r伤害 +663 命中 +966#r耐久度 69  修理失败 1次#r锻炼等级 14  镶嵌宝石 太阳石、 红玛瑙#Y#r#G开运孔数：5孔/5孔#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 敏捷 +1 伤害 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r星位：速度 +3.5#n#G#r星相互合：体质 +2#r#cEE82EE符石组合: 无双一击符石#r门派条件：大唐官府 #r部位条件：武器 #r增加门派技能无双一击等级6级#Y#r#W制造者：木木夕‖强化打造#Y  ","iLockNew":9,"iType":2280,]),1:(["iLock":1,"cDesc":"#r等级 130  五行 木#r#r魔法 +157 防御 +81#r耐久度 335  修理失败 1次#r锻炼等级 13  镶嵌宝石 太阳石、 红玛瑙#r#G#G伤害 +32#Y #G命中 +225#Y#Y#r#c4DBAF4特技：#c4DBAF4野兽之力#Y#Y#r#c4DBAF4套装效果：追加法术满天花雨#Y#Y#r#G开运孔数：5孔/5孔#G#r符石: 力量 +1 速度 +1.5#n#G#r符石: 敏捷 +1 气血 +10#n#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 力量 +1 速度 +1.5#n#G#r符石: 魔力 +1 伤害 +1.5#n#G#r星位：速度 +2.5#n#r#cEE82EE符石组合: 天降大任#r门派条件：无#r部位条件：无#r无视召唤兽15%的物理防御进行攻击(该组合全身只有一件装备起效)#Y#r#W制造者：LOVE豆豆#Y#r#Y熔炼效果：#r#Y#r+8防御 +17魔法 #r#Y  ","iType":2555,]),3:(["cDesc":"#r等级 130  五行 金#r#r敏捷 +46 防御 +73#r耐久度 405  修理失败 2次#r锻炼等级 13  镶嵌宝石 黑宝石#r#G#G速度 +104#Y#Y#r#c4DBAF4特技：#c4DBAF4破碎无双#Y#Y#r#c4DBAF4套装效果：追加法术满天花雨#Y#Y#r#G开运孔数：5孔/5孔#G#r符石: 力量 +1 速度 +1.5#n#G#r符石: 魔力 +1 伤害 +1.5#n#G#r符石: 敏捷 +1 伤害 +1.5#n#G#r符石: 速度 +1.5#n#G#r符石: 气血 +10#n#G#r星位：防御 +5#n#r#cEE82EE符石组合: 百无禁忌#r门派条件：无#r部位条件：靴 #r提高自身12%对抗封印类技能的能力#Y#r#W制造者：脾气有点怪强化打造#Y#r#Y熔炼效果：#r#Y#r+5防御 +4敏捷 #r#Y  ","iLockNew":9,"iType":2755,]),10:(["iAddLevel":10,"cDesc":"灵气：10  ","iType":17320,]),8:(["cDesc":"#r等级 100  #r灵力 +183#r耐久度 32  修理失败 1次#r锻炼等级 7  镶嵌宝石 舍利子#Y#r#c4DBAF4特技：#c4DBAF4破甲术#Y#Y#r#c4DBAF4特效：#c4DBAF4珍宝#Y#r#c4DBAF4套装效果：变身术之混沌兽#Y#Y#r#G开运孔数：4孔/4孔#G#r符石: 法防 +1#n#G#r符石: 法防 +1#n#G#r符石: 伤害 +1.5#n#G#r符石: 敏捷 +1 法术防御 +2#n#r#cEE82EE符石组合: 天雷地火#r门派条件：天宫 #r部位条件：无#r使用天雷斩、雷霆万钧时增加人物等级*1的伤害，装备该组合时降低5%的防御，同时降低5%的气血，仅对NPC使用时有效#Y#r#W制造者：狂秒チ阿衰ぴ#Y#r#Y熔炼效果：#r#Y#r+5灵力#Y  ","iLockNew":9,"iType":2852,]),7:(["cDesc":"#r等级 130  #r灵力 +267#r耐久度 291  修理失败 3次#r锻炼等级 10  镶嵌宝石 舍利子#Y#r#c4DBAF4特技：#c4DBAF4水清诀#Y#Y#r#c4DBAF4特效：化生寺专用#r#c4DBAF4套装效果：变身术之律法女娲#Y#Y#r玩家38058980专用#r#G开运孔数：5孔/5孔#b#G#r符石: 敏捷 +1#n#G#r符石: 力量 +1 躲避 +3#n#G#r符石: 魔力 +1 法术防御 +2#n#G#r符石: 敏捷 +1 固定伤害 +2#n#G#r符石: 灵力 +1.5#n#G#r星位：法伤 +1.5#n#r#cEE82EE符石组合: 神道无念符石#r门派条件：方寸山 #r部位条件：项链 #r增加门派技能神道无念6级#Y#r#W制造者：紫欣冷雨强化打造#Y#r#Y熔炼效果：#r#Y#r+7灵力#Y  ","iType":2855,]),5:(["iLock":1,"cDesc":"#r等级 130  五行 水#r#r气血 +270 防御 +70#r耐久度 308#r锻炼等级 13  镶嵌宝石 黑宝石#r#G#G速度 +104#Y#Y#r#c4DBAF4特效：#c4DBAF4愤怒#Y#r#c4DBAF4套装效果：追加法术满天花雨#Y#Y#r#G开运孔数：5孔/5孔 (双5孔)#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 魔力 +1 伤害 +1.5#n#G#r符石: 力量 +1 速度 +1.5#n#G#r符石: 敏捷 +1 伤害 +1.5#n#r#cEE82EE符石组合: 文韬武略符石#r门派条件：大唐官府 #r部位条件：腰带 #r增加门派技能文韬武略6级#Y#r#W制造者：说什么不可能#Y#r#Y熔炼效果：#r#Y#r+8防御 +16气血 #r#Y  ","iType":2955,]),4:(["iLock":1,"cDesc":"#r等级 130  #r灵力 +250#r耐久度 294#r锻炼等级 10  镶嵌宝石 舍利子#Y#r#c4DBAF4特技：#c4DBAF4破血狂攻#Y#Y#r#c4DBAF4套装效果：追加法术满天花雨#Y#Y#r#G开运孔数：5孔/5孔#Y #r#W制造者：イ┼·麽á！强化打造#Y#r#Y熔炼效果：#r#Y#r+3灵力#Y  ","iType":2855,]),]),"icolor_ex":0,"shenqi_yellow":"0神器灵气：78#r","cName":"V→aqiu0112","iCGBoxAmount":13,"iExptSki4":25,"iGoodness":3623,"iMaxExpt3":20,"iMarry":0,"iMaxExpt1":25,"iSchool":8,"iBeastSki1":25,"total_avatar":17,"iExptSki2":25,"bid":1,"AchPointTotal":5455,"iUpExp":59211518,"iBeastSki3":25,"iExptSki5":15,"iMag_All":183,"rent":144032,"more_attr":(["attrs":({(["lv":0,"idx":3,]),(["lv":0,"idx":2,]),(["lv":0,"idx":10,]),(["lv":0,"idx":1,]),(["lv":0,"idx":6,]),(["lv":0,"idx":12,]),(["lv":0,"idx":5,]),(["lv":0,"idx":8,]),(["lv":0,"idx":4,]),(["lv":0,"idx":9,]),(["lv":0,"idx":7,]),(["lv":0,"idx":11,]),(["lv":962,"idx":13,]),(["lv":1257,"idx":14,]),}),]),"ExpJwBase":1000000000,"iDod_All":962,"shenqi_pos":({3,6227,}),"iRace":3,"commu_name":"","idbid_desc":({1,}),"all_skills":(["166":1,"82":180,"81":180,"27824":1,"198":1,"27821":1,"52031":1,"80":180,"221":20,"169":1,"83":180,"40081":1,"205":160,"52032":1,"201":140,"237":40,"27815":1,"78":180,"160":5,"197":2,"207":160,"27827":1,"153":4,"196":1,"168":1,"211":160,"27809":1,"77":180,"220":5,"219":5,"231":140,"1642":3,"210":100,"230":40,"27818":1,"165":4,"222":5,"162":1,"27812":1,"173":1,"27805":1,"179":1,"208":140,"27803":1,"218":120,"216":134,"164":3,"170":6,"206":160,"175":1,"163":1,"212":160,"167":1,"204":160,"223":5,"79":180,"52016":1,"174":1,"209":110,"202":160,"154":6,"217":85,"203":52,]),"outdoor_level":4,"iDef_All":1388,"iIcon":209,"iOrgOffer":0,"iMp":3129,"iCGTotalAmount":310,"iCash":517826,"iBadness":0,"sword_score":1000,"total_horse":6,"HeroScore":15534,"iHp_Max":4886,"iSmithski":3786,"iSaving":0,"iSewski":7426,"sum_exp":616,"energy":60,"cOrg":"","farm_level":"1","iSkiPoint":4,"iSchOffer":124,"iDesc":0,"iTotalMagDef_all":1282,"iStr_All":1369,"TA_iAllPoint":0,"pet":({}),"iSpe_All":268,"iMarry2":0,"iErrantry":0,"datang_feat":4608,"shenqi":(["components":({(["unlock":1,"wuxing":({(["wuxingshi_level":2,"attr":"伤害 +5","affix_disable":0,"wuxingshi_affix":0,"id":8,"status":1,]),(["wuxingshi_level":2,"attr":"伤害 +5","affix_disable":0,"wuxingshi_affix":0,"id":8,"status":1,]),(["wuxingshi_level":2,"attr":"速度 +3.7","affix_disable":0,"wuxingshi_affix":0,"id":1,"status":1,]),(["wuxingshi_level":2,"attr":"伤害 +5","affix_disable":0,"wuxingshi_affix":0,"id":8,"status":1,]),}),"level":2,]),(["unlock":1,"wuxing":({(["wuxingshi_level":2,"attr":"伤害 +5","affix_disable":0,"wuxingshi_affix":0,"id":8,"status":1,]),(["wuxingshi_level":2,"attr":"伤害 +5","affix_disable":0,"wuxingshi_affix":0,"id":8,"status":1,]),(["wuxingshi_level":2,"attr":"伤害 +5","affix_disable":0,"wuxingshi_affix":0,"id":8,"status":1,]),(["wuxingshi_level":2,"attr":"速度 +3.7","affix_disable":0,"wuxingshi_affix":0,"id":1,"status":1,]),}),"level":2,]),(["unlock":1,"wuxing":({(["wuxingshi_level":2,"attr":"速度 +3.7","affix_disable":0,"wuxingshi_affix":0,"id":1,"status":1,]),(["wuxingshi_level":2,"attr":"伤害 +5","affix_disable":0,"wuxingshi_affix":0,"id":8,"status":1,]),(["wuxingshi_level":2,"attr":"伤害 +5","affix_disable":0,"wuxingshi_affix":0,"id":8,"status":1,]),(["wuxingshi_level":2,"attr":"伤害 +5","affix_disable":0,"wuxingshi_affix":0,"id":8,"status":1,]),}),"level":2,]),}),"full":0,"skill_level":2,"skill":53082,"skill_desc":"每次击杀敌方单位，增加120点伤害，最多叠加2层，死亡后清零。","active":1,"power":0,"id":6227,"attributes":({(["disable":0,"attr":"速度 +11.2","id":1,]),(["disable":1,"attr":"气血 +0","id":2,]),(["disable":0,"attr":"伤害 +45","id":8,]),(["disable":1,"attr":"封印命中 +0","id":16,]),(["disable":1,"attr":"抵抗封印 +0","id":4,]),}),]),"iCGBodyAmount":30,"iBeastSki2":25,"iExptSki3":6,"AllRider":([1:(["iGrade":170,"exgrow":22057,"mattrib":"耐力","all_skills":([600:3,601:3,]),"iType":502,"ExtraGrow":90,]),5:(["iGrade":170,"exgrow":17640,"mattrib":"力量","all_skills":([608:3,611:3,]),"iType":503,"ExtraGrow":50,]),4:(["iGrade":170,"exgrow":23433,"mattrib":"力量","all_skills":([600:3,601:3,]),"iType":502,"ExtraGrow":100,]),6:(["iGrade":170,"exgrow":20531,"mattrib":"体质","all_skills":([600:3,601:3,]),"iType":508,"ExtraGrow":80,]),]),"iCor_All":189,"iBeastSki4":25,"iMaxExpt2":25,"jiyuan":5,"ExAvt":([17:(["order":6,"iType":12372,"cName":"夏日清凉",]),13:(["order":13,"iType":21571,"cName":"幸运彩虹",]),16:(["order":12,"iType":13768,"cName":"缎夜星语",]),15:(["order":11,"iType":14406,"cName":"糖果武器",]),12:(["order":15,"iType":14797,"cName":"甜蜜糖果",]),11:(["order":10,"iType":13326,"cName":"红色圣诞帽",]),9:(["order":2,"iType":12246,"cName":"夜之孤煞",]),2:(["order":17,"iType":13105,"cName":"蟠桃童子炫卡",]),6:(["order":5,"iType":14404,"cName":"蓝色妖姬",]),14:(["order":14,"iType":14875,"cName":"空山秋雨",]),1:(["order":9,"iType":21511,"cName":"星光熠熠",]),3:(["order":8,"iType":13962,"cName":"火凤披风",]),10:(["order":1,"iType":13983,"cName":"夜之孤煞",]),7:(["order":7,"iType":21517,"cName":"月影婆娑",]),8:(["order":4,"iType":12370,"cName":"夏日清凉",]),5:(["order":16,"iType":19257,"cName":"怀旧逍遥生炫卡",]),4:(["order":3,"iType":13512,"cName":"夜之孤煞",]),]),"iDex_All":770,"i3FlyLv":9,"TA_iAllNewPoint":9,"iExptSki1":25,])'
# desc = '(["iGrade":109,"iPcktPage":0,"iStr_All":120,"TA_iAllNewPoint":2,"iSumAmount":8,"iPride":800,"ExpJw":0,"iAtt_All":234,"normal_horse":2,"iSpe_All":121,"total_avatar":5,"more_attr":(["attrs":({(["idx":6,"lv":0,]),(["idx":3,"lv":0,]),(["idx":8,"lv":0,]),(["idx":1,"lv":0,]),(["idx":12,"lv":0,]),(["idx":5,"lv":0,]),(["idx":9,"lv":0,]),(["idx":7,"lv":0,]),(["idx":11,"lv":0,]),(["idx":10,"lv":0,]),(["idx":4,"lv":0,]),(["idx":2,"lv":0,]),(["idx":13,"lv":362,]),(["idx":14,"lv":762,]),}),]),"shenqi":(["active":0,"components":({(["unlock":1,"wuxing":({(["wuxingshi_affix":0,"attr":"抵抗封印 +6","wuxingshi_level":1,"status":0,"affix_disable":0,"id":4,]),(["wuxingshi_affix":0,"attr":"法术暴击 +3","wuxingshi_level":1,"status":0,"affix_disable":0,"id":16,]),(["wuxingshi_affix":0,"attr":"法术暴击 +3","wuxingshi_level":1,"status":0,"affix_disable":0,"id":16,]),(["wuxingshi_affix":0,"attr":"抵抗封印 +6","wuxingshi_level":1,"status":0,"affix_disable":0,"id":4,]),}),"level":1,]),(["unlock":0,"wuxing":({(["wuxingshi_affix":0,"attr":"速度 +0","wuxingshi_level":0,"status":0,"affix_disable":0,"id":1,]),(["wuxingshi_affix":0,"attr":"法术暴击 +0","wuxingshi_level":0,"status":0,"affix_disable":0,"id":16,]),(["wuxingshi_affix":0,"attr":"抵抗封印 +0","wuxingshi_level":0,"status":0,"affix_disable":0,"id":4,]),(["wuxingshi_affix":0,"attr":"气血 +0","wuxingshi_level":0,"status":0,"affix_disable":0,"id":2,]),}),"level":0,]),(["unlock":0,"wuxing":({(["wuxingshi_affix":0,"attr":"气血 +0","wuxingshi_level":0,"status":0,"affix_disable":0,"id":2,]),(["wuxingshi_affix":0,"attr":"抵抗封印 +0","wuxingshi_level":0,"status":0,"affix_disable":0,"id":4,]),(["wuxingshi_affix":0,"attr":"法术伤害 +0","wuxingshi_level":0,"status":0,"affix_disable":0,"id":8,]),(["wuxingshi_affix":0,"attr":"抵抗封印 +0","wuxingshi_level":0,"status":0,"affix_disable":0,"id":4,]),}),"level":0,]),}),"skill":53070,"full":0,"skill_level":1,"power":10,"id":6211,"attributes":({(["disable":1,"attr":"速度 +0","id":1,]),(["disable":1,"attr":"气血 +0","id":2,]),(["disable":1,"attr":"法术伤害 +0","id":8,]),(["disable":0,"attr":"法术暴击 +6","id":16,]),(["disable":0,"attr":"抵抗封印 +12","id":4,]),}),"skill_desc":"",]),"HeroScore":0,"iMp_Max":3488,"commu_gid":0,"iMarry2":0,"iLearnCash":207040,"energy":48,"iPoint":0,"HugeHorse":([225:(["iSkill":0,"order":2,"iType":11214,"nosale":0,"cName":"风火飞轮","iSkillLevel":0,]),253:(["iSkill":0,"order":1,"iType":11245,"nosale":0,"cName":"仙缘战鹿","iSkillLevel":0,]),]),"iTotalMagDam_all":822,"iBadness":0,"iHp_Eff":1667,"farm_level":0,"iCGBoxAmount":0,"usernum":49323644,"shenqi_pos":({0,0,}),"datang_feat":6000,"jiyuan":0,"iOrgOffer":0,"iExptSki5":0,"idbid_desc":({}),"iTotalMagDef_all":762,"iHp":1619,"iSkiPoint":15,"iSumAmountEx":0,"AllRider":([1:(["mattrib":"力量","all_skills":([]),"iGrade":20,"exgrow":10552,"iType":500,"ExtraGrow":0,]),3:(["mattrib":"力量","all_skills":([600:3,]),"iGrade":107,"exgrow":13162,"iType":508,"ExtraGrow":0,]),2:(["mattrib":"力量","all_skills":([611:1,]),"iGrade":83,"exgrow":12519,"iType":503,"ExtraGrow":0,]),]),"icolor_ex":0,"cName":"糖糖！乖","sword_score":0,"iErrantry":0,"iExptSki4":17,"AchPointTotal":947,"fabao":([12:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6064,]),]),"iBeastSki2":9,"iMaxExpt2":20,"ExAvt":([1:(["order":3,"iType":11159,"cName":"方天画戟",]),3:(["order":5,"iType":13359,"cName":"明光宝甲",]),5:(["order":4,"iType":14401,"cName":"动物装饰篮",]),4:(["order":2,"iType":12094,"cName":"明光宝甲",]),2:(["order":1,"iType":11169,"cName":"狼牙棒",]),]),"ExpJwBase":1000000000,"iSchool":7,"iGoodness":852,"sum_exp":28,"iExptSki2":17,"iMag_All":762,"rent":192365,"all_skills":(["198":1,"40072":1,"29":119,"170":1,"25":119,"52031":1,"169":1,"26805":1,"32":119,"179":1,"30":119,"230":9,"34":119,"173":1,"208":28,"202":27,"31":119,"52016":1,"174":1,"154":5,"26802":1,"52032":1,"160":5,"201":114,"33":82,"197":1,"40071":1,"196":1,"225":1,]),"iDod_All":362,"iRace":3,"iSmithski":0,"changesch":({5,}),"iRes_All":121,"xianyu":200,"addPoint":0,"iDef_All":410,"iIcon":9,"iMarry":0,"iDamage_All":507,"iMaxExpt4":20,"iMp":3488,"pet":({}),"iCash":59741,"iCGBodyAmount":0,"iMagDef_All":762,"commu_name":"","total_horse":2,"outdoor_level":1,"igoodness_sav":1938,"bid":0,"iCGTotalAmount":0,"iHp_Max":1667,"iSaving":0,"propKept":([]),"cOrg":"","iBeastSki4":0,"iZhuanZhi":0,"shenqi_yellow":"","iSchOffer":105,"iDesc":0,"AllSummon":({}),"AllEquip":([14:(["cDesc":"#W等级 50#W#r#Y未鉴定物品#Y  ","iType":2908,]),12:(["cDesc":"#r等级 30  #r气血 +60 防御 +15#r耐久度 199#Y  ","iType":2904,]),9:(["cDesc":"#r等级 50  #r敏捷 +25 防御 +27#r耐久度 349#Y#r#c4DBAF4套装效果：变身术之蛟龙#Y#Y  ","iType":2706,]),23:(["iAddLevel":8,"cDesc":"灵气：8  ","iType":17320,]),]),"iMaxExpt1":20,"rent_level":1,"ori_desc":146,"iMaxExpt3":20,"iExptSki3":17,"iBeastSki3":9,"iNutsNum":100,"iUpExp":109499115,"iCor_All":121,"i3FlyLv":0,"ori_race":3,"TA_iAllPoint":0,"iBeastSki1":9,"iDex_All":120,"iExptSki1":1,"iSewski":0,])'
# desc = '(["propKept":([1:(["iRes":185,"iStr":186,"iCor":188,"iMag":1318,"iSpe":186,]),3:(["iRes":185,"iStr":185,"iCor":1315,"iMag":185,"iSpe":185,]),0:(["iRes":435,"iStr":186,"iCor":188,"iMag":1065,"iSpe":186,]),2:(["iRes":546,"iStr":186,"iCor":186,"iMag":959,"iSpe":186,]),]),"igoodness_sav":462,"iGrade":175,"iMaxExpt4":25,"rent_level":5,"iSumAmount":10,"ExpJw":0,"iDamage_All":1790,"iPride":800,"commu_gid":0,"iAtt_All":976,"ori_desc":5714,"iTotalMagDam_all":2139,"iPoint":0,"iMp_Max":11855,"iSumAmountEx":2,"iMagDef_All":1809,"addPoint":34,"changesch":({7,}),"HugeHorse":([154:(["iSkillLevel":0,"iSkill":0,"order":6,"iType":11142,"nosale":0,"cName":"开明天兽",]),44:(["iSkillLevel":0,"iSkill":0,"order":9,"iType":11044,"nosale":0,"cName":"琉璃宝象",]),226:(["iSkillLevel":0,"iSkill":0,"order":4,"iType":11215,"nosale":0,"cName":"风火飞轮",]),60:(["iSkillLevel":0,"iSkill":0,"order":3,"iType":11060,"nosale":0,"cName":"逐日天辇",]),55:(["iSkillLevel":0,"iSkill":0,"order":5,"iType":11055,"nosale":0,"cName":"魔骨战熊",]),7:(["iSkillLevel":1,"iSkill":623,"order":1,"iType":11007,"nosale":0,"cName":"金鳞仙子",]),5:(["iSkillLevel":0,"iSkill":0,"order":8,"iType":11006,"nosale":0,"cName":"玄霜玉兔",]),368:(["iSkillLevel":1,"iSkill":622,"order":1,"iType":11357,"nosale":1,"cName":"冰晶魅灵",]),53:(["iSkillLevel":0,"iSkill":0,"order":7,"iType":11053,"nosale":0,"cName":"踏雪灵熊",]),45:(["iSkillLevel":0,"iSkill":0,"order":2,"iType":11045,"nosale":0,"cName":"莽林猛犸",]),]),"iLearnCash":3039311,"usernum":1879,"iNutsNum":200,"iZhuanZhi":2,"iPcktPage":1,"ori_race":3,"xianyu":0,"normal_horse":9,"child":(["summon_equip3":(["cDesc":"#r等级 115  #r气血 +91 防御 +102#r耐久度 501#r#G#G耐力 +18#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：Supermodel#Y#r#r镶嵌效果 #r+56防御 镶嵌等级：7","iType":9112,]),"iDod_All":22,"iHp_max":440,"iGrade":5,"iAtt_F":4,"summon_equip2":(["cDesc":"#r等级 5  #r速度 +7#r耐久度 478#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y","iType":9201,]),"iMagDef_all":52,"life":65432,"summon_equip1":(["cDesc":"#r等级 125  #r气血 +91 命中率 +15%#r耐久度 604#r#G#G耐力 +18#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：梦想满罐#Y#r#r镶嵌效果 #r+20灵力 镶嵌等级：5","iType":9313,]),"qianjinlu":0,"all_skills":(["637":1,"569":1,"435":1,"648":1,"505":1,"649":1,]),"mp":1564,"att_rate":0,"dl":0,"iDef_All":72,"iPoint":0,"iRes_all":32,"iMp":111,"lm":0,"iMagDam_all":52,"wl":0,"desc":17,"iStr_all":25,"iMp_max":111,"iAtt_all":48,"nl":0,"iCor_all":53,"grow":1287,"iMag_all":25,"def":1606,"iType":100109,"change_598_times":0,"att":997,"child_sixwx":1111,"dod":911,"iHp":440,"school":15,"hp":6250,"iSpe_all":25,"spe":913,"yuanxiao":0,"iBaobao":1,"isnew":0,"ruyidan":0,"ending":0,"gg":0,"zl":0,"iDex_All":29,]),"iHp_Eff":4596,"iRes_All":215,"fabao":([33:(["cDesc":"0#W【回合限制】2#r#Y#Y灵气：#G255#Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6027,]),15:(["cDesc":"0#Y灵气：#G222#Y 五行：#G金#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y#r传送至大唐境外（616，17）","iType":6020,]),29:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G300#Y 五行：#G金#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6064,]),44:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6060,]),21:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G375#Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6030,]),30:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G480#Y 五行：#G土#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6019,]),32:(["cDesc":"0#Y灵气：#G192#Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6070,]),36:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G土#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6011,]),2:(["cDesc":"0#Y灵气：#G199#Y 五行：#G木#Y#r修炼境界：第#G9#Y层 #cFF6F28不堕轮回#Y","iType":6004,]),24:(["cDesc":"0#W【回合限制】6#r#Y#Y灵气：#G270#Y 五行：#G木#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y","iType":6029,]),34:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G20 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6014,]),47:(["cDesc":"0#Y灵气：#G490#Y 五行：#G土#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6063,]),42:(["cDesc":"0#W【回合限制】150#r#Y#Y灵气：#G260#Y 五行：#G土#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6024,]),39:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G500#Y 五行：#G金#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6065,]),4:(["cDesc":"0#Y灵气：#G25 #Y 五行：#G水#Y#r修炼境界：第#G18#Y层 #cFF6F28浴火涅槃#Y#r#n#Y最佳五行属性奖励：额外提升3点法术伤害#G（已生效）#Y","iType":6097,]),23:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G378#Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6021,]),43:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：起效次数增加1次#c7D7E82（未生效）#Y","iType":6087,]),17:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G465#Y 五行：#G水#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6023,]),48:(["cDesc":"0#Y灵气：#G0  #Y 五行：#G木#Y#r修炼境界：第#G18#Y层 #cFF6F28浴火涅槃#Y#r#n#Y最佳五行属性奖励：触发时额外减少10点所受伤害#G（已生效）#Y","iType":6088,]),13:(["cDesc":"0#Y灵气：#G90 #Y 五行：#G水#Y#r修炼境界：第#G9#Y层 #cFF6F28不堕轮回#Y","iType":6032,]),16:(["cDesc":"0#Y灵气：#G200#Y 五行：#G水#Y#r修炼境界：第#G9#Y层 #cFF6F28不堕轮回#Y","iType":6058,]),27:(["cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G280#Y 五行：#G土#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6033,]),22:(["cDesc":"0#Y灵气：#G255#Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6072,]),11:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G450#Y 五行：#G土#Y#r修炼境界：第#G14#Y层 #cFF6F28返璞归真#Y","iType":6028,]),12:(["cDesc":"0#Y灵气：#G200#Y 五行：#G火#Y#r修炼境界：第#G3#Y层 #cB7BFF8心领神会#Y","iType":6066,]),18:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G300#Y 五行：#G木#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y","iType":6075,]),41:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G299#Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6061,]),20:(["cDesc":"0#Y灵气：#G120#Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y","iType":6068,]),14:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G190#Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6016,]),1:(["cDesc":"0#Y灵气：#G28 #Y 五行：#G金#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y","iType":6074,]),28:(["cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G152#Y 五行：#G土#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6026,]),50:(["cDesc":"0#Y灵气：#G152#Y 五行：#G金#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6010,]),49:(["cDesc":"0#Y灵气：#G140#Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加5点治疗量#c7D7E82（未生效）#Y","iType":6095,]),25:(["cDesc":"0#Y灵气：#G147#Y 五行：#G水#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y","iType":6073,]),46:(["cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G500#Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6017,]),37:(["cDesc":"0#W【回合限制】1#r#Y#Y灵气：#G81 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y","iType":6013,]),19:(["cDesc":"0#Y灵气：#G42 #Y 五行：#G金#Y#r修炼境界：第#G18#Y层 #cFF6F28浴火涅槃#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#G（已生效）#Y","iType":6101,]),35:(["cDesc":"0#W【回合限制】150#r#Y#Y灵气：#G15 #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y","iType":6025,]),45:(["cDesc":"0#W【回合限制】8#r#Y#Y灵气：#G42 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：回合限制缩短为7回合#c7D7E82（未生效）#Y","iType":6090,]),31:(["cDesc":"0#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#G（已生效）#Y","iType":6098,]),]),"AllSummon":({(["DEF_MAX":1650,"summon_equip3":(["cDesc":"#r等级 115  #r伤害 +52 气血 +93 防御 +107#r耐久度 464#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级反震#Y#Y#r#W制造者：棺材租号贷款#Y#r#r镶嵌效果 #r+210气血 镶嵌等级：7","iType":9112,]),"summon_color":1,"iDod_All":250,"iHp_max":8919,"iGrade":180,"iAtt_F":16,"core_close":0,"lianshou":0,"iMagDef_all":859,"life":8728,"summon_equip2":(["cDesc":"#r等级 115  #r速度 +38 伤害 +57 气血 +80#r耐久度 464#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级反震#Y#Y#r#W制造者：Brother紫苇#Y#r#r镶嵌效果 #r+42速度 镶嵌等级：7","iType":9212,]),"HP_MAX":7000,"summon_equip1":(["cDesc":"#r等级 135  #r伤害 +56 气血 +86 命中率 +16%#r耐久度 591#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级反震#Y#Y#r#W制造者：糖醋里脊肉#Y#r#r镶嵌效果 #r+80伤害 镶嵌等级：8","iType":9314,]),"MP_MAX":3600,"qianjinlu":10,"mp":1811,"all_skills":(["595":1,"414":1,"401":1,"408":1,"413":1,"416":1,"435":1,"411":1,"425":1,"404":1,]),"att_rate":16,"iDef_All":1456,"iPoint":0,"iRes_all":417,"iMp":1385,"ATK_MAX":1650,"iStr_all":365,"iMp_max":1385,"iAtt_all":1822,"summon_equip4_type":27462,"iCor_all":964,"grow":1288,"iMag_all":190,"def":1504,"iType":102246,"left_qlxl":7,"csavezz":"1400|1406|1385|1319|2827|1811","att":1506,"iRealColor":5,"iGenius":0,"dod":1319,"growthMax":1297,"iHp":8858,"iJjFeedCd":0,"hp":3162,"carrygradezz":2,"iSpe_all":190,"jj_extra_add":0,"spe":1385,"lastchecksubzz":2019,"sjg":0,"tmp_lingxing":50,"yuanxiao":10,"SPD_MAX":1650,"summon_equip4_desc":"#Y#r玄天灵力 733 （已染色）","iBaobao":1,"summon_core":([929:({5,0,([]),}),907:({5,0,([]),}),915:({5,0,([]),}),913:({5,0,([]),}),901:({5,0,([]),}),904:({5,0,([]),}),]),"MS_MAX":2000,"ruyidan":0,"jinjie":(["new_type":1,"core":(["effect":"#Y对召唤兽物理伤害结果增加#G20%#Y；对人物角色伤害结果减少#R112#Y。","fix_st":0,"name":"争锋","id":707,]),"lx":108,"cnt":0,]),"iDex_All":397,]),(["DEF_MAX":1550,"summon_equip3":(["iLock":1,"cDesc":"#r等级 125  #r防御 +115#r耐久度 568#r#G#G耐力 +10#Y #G敏捷 +19#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：乱世れ双儿#Y#r#r镶嵌效果 #r+210气血 镶嵌等级：7","iType":9113,]),"summon_color":1,"iDod_All":425,"iHp_max":9670,"iGrade":180,"iAtt_F":16,"core_close":0,"lianshou":0,"iMagDef_all":849,"life":5575,"summon_equip2":(["iLock":1,"cDesc":"#r等级 115  #r速度 +38 气血 +80#r耐久度 621#r#G#G耐力 +18#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：海贼王ぃ白星#Y#r#r镶嵌效果 #r+36速度 镶嵌等级：6","iType":9212,]),"HP_MAX":5500,"summon_equip1":(["iLock":1,"cDesc":"#r等级 105  #r命中率 +13%#r耐久度 555#r#G#G耐力 +16#Y #G敏捷 +18#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：我为刘庆代言#Y#r#r镶嵌效果 #r+24灵力 镶嵌等级：6","iType":9311,]),"MP_MAX":3050,"qianjinlu":10,"mp":2168,"all_skills":(["403":1,"417":1,"579":1,"422":1,"435":1,"553":1,]),"att_rate":13,"iDef_All":1728,"iPoint":0,"iRes_all":388,"iMp":1515,"ATK_MAX":1550,"iStr_all":190,"iMp_max":1515,"iAtt_all":1057,"summon_equip4_type":0,"iCor_all":1039,"grow":1291,"iMag_all":190,"def":1600,"iType":102164,"left_qlxl":0,"csavezz":"1176|1600|1399|1064|4900|2168","att":1176,"iRealColor":5,"iLock":1,"iGenius":553,"dod":1064,"growthMax":1297,"iHp":9670,"iJjFeedCd":0,"hp":5000,"carrygradezz":0,"iSpe_all":400,"jj_extra_add":0,"spe":1430,"lastchecksubzz":2019,"sjg":0,"tmp_lingxing":108,"yuanxiao":0,"SPD_MAX":1550,"summon_equip4_desc":"","iBaobao":1,"summon_core":([907:({5,0,([]),}),917:({5,0,([]),}),901:({5,0,([]),}),910:({5,0,([]),}),904:({5,0,([]),}),]),"MS_MAX":1800,"ruyidan":0,"jinjie":(["new_type":0,"core":(["effect":"#Y进场时，若己方四个及以上单位处于被封印状态，则#G100%#Y解除我方所有单位异常状态；防御力下降#R15%#Y。","fix_st":0,"name":"逆境","id":721,]),"lx":108,"cnt":7,]),"iDex_All":700,]),(["DEF_MAX":1600,"summon_equip3":(["iLock":1,"cDesc":"#r等级 115  #r气血 +94 防御 +110#r耐久度 251#r#G#G耐力 +19#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：梦想满罐#Y#r#r镶嵌效果 #r+80防御 镶嵌等级：10","iType":9112,]),"summon_color":1,"iDod_All":277,"iHp_max":6805,"iGrade":180,"iAtt_F":16,"core_close":0,"lianshou":0,"iMagDef_all":1132,"life":3307,"summon_equip2":(["iLock":1,"cDesc":"#r等级 115  #r速度 +35 气血 +86#r耐久度 292#r#G#G法力 +17#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：长情丶2#Y","iType":9212,]),"HP_MAX":6500,"summon_equip1":(["iLock":1,"cDesc":"#r等级 105  #r命中率 +11%#r耐久度 411#r#G#G耐力 +14#Y #G法力 +17#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：い繁☆伴月#Y#r#r镶嵌效果 #r+36灵力 镶嵌等级：9","iType":9311,]),"MP_MAX":3500,"qianjinlu":10,"mp":2367,"all_skills":(["578":1,"408":1,"303":1,"424":1,"426":1,"661":1,"577":1,"573":1,]),"att_rate":11,"iDef_All":1428,"iPoint":0,"iRes_all":350,"iMp":3675,"ATK_MAX":1600,"iStr_all":190,"iMp_max":3675,"iAtt_all":1024,"summon_equip4_type":3550,"iCor_all":687,"grow":1300,"iMag_all":724,"def":1490,"iType":102128,"left_qlxl":6,"csavezz":"1200|1394|1265|1219|4640|2188","att":1200,"iRealColor":5,"iLock":1,"iGenius":426,"dod":1219,"growthMax":1287,"iHp":6805,"iJjFeedCd":0,"hp":4640,"carrygradezz":1,"iSpe_all":228,"jj_extra_add":0,"spe":1265,"lastchecksubzz":2019,"sjg":0,"tmp_lingxing":58,"yuanxiao":0,"SPD_MAX":1600,"summon_equip4_desc":"#Y#r玄天灵力 392 （已染色）","iBaobao":1,"summon_core":([907:({5,0,([]),}),928:({5,0,([]),}),904:({5,0,([]),}),906:({5,0,([]),}),936:({5,0,([]),}),]),"MS_MAX":2000,"ruyidan":0,"jinjie":(["new_type":0,"core":(["effect":"#Y对气血百分低于70%的单位法术伤害力增加#G150#Y；对其余单位法术伤害力降低#R112#Y。","fix_st":0,"name":"顺势","id":712,]),"lx":101,"cnt":1,]),"iDex_All":350,]),(["DEF_MAX":1650,"summon_equip3":(["cDesc":"#r等级 125  #r伤害 +59 防御 +102#r耐久度 632#r#G#G体质 +6#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级防御#Y#Y#r#W制造者：【非凡】哥#Y#r#r镶嵌效果 #r+240气血 镶嵌等级：8","iType":9113,]),"summon_color":1,"iDod_All":224,"iHp_max":6814,"iGrade":180,"iAtt_F":1,"core_close":0,"lianshou":0,"iMagDef_all":904,"life":9994,"summon_equip2":(["cDesc":"#r等级 125  #r速度 +39 伤害 +54#r耐久度 501#r#G#G耐力 +16#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级防御#Y#Y#r#W制造者：豹纹添衣．ι#Y#r#r镶嵌效果 #r+42速度 镶嵌等级：7","iType":9213,]),"HP_MAX":7000,"summon_equip1":(["cDesc":"#r等级 105  #r伤害 +53 命中率 +15%#r耐久度 580#r#G#G耐力 +12#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级防御#Y#Y#r#W制造者：丶萌宝Grace#Y#r#r镶嵌效果 #r+80伤害 镶嵌等级：8","iType":9311,]),"MP_MAX":3600,"qianjinlu":10,"mp":1970,"all_skills":(["403":1,"417":1,"416":1,"411":1,"425":1,"401":1,"404":1,"571":1,]),"att_rate":15,"iDef_All":1314,"iPoint":0,"iRes_all":373,"iMp":1428,"ATK_MAX":1650,"iStr_all":651,"iMp_max":1428,"iAtt_all":2153,"summon_equip4_type":0,"iCor_all":758,"grow":1263,"iMag_all":190,"def":1402,"iType":102246,"left_qlxl":0,"csavezz":"1349|1005|1116|1183|2717|1970","att":1515,"iRealColor":5,"iGenius":0,"dod":1183,"growthMax":1297,"iHp":6814,"iJjFeedCd":0,"hp":3013,"carrygradezz":2,"iSpe_all":190,"jj_extra_add":0,"spe":1116,"lastchecksubzz":2019,"sjg":5,"tmp_lingxing":109,"yuanxiao":15,"SPD_MAX":1650,"summon_equip4_desc":"","iBaobao":1,"summon_core":([907:({5,0,([]),}),922:({5,0,([]),}),901:({5,0,([]),}),923:({5,0,([]),}),935:({5,0,([]),}),904:({5,0,([]),}),]),"MS_MAX":2000,"ruyidan":0,"jinjie":(["new_type":1,"core":(["effect":"#Y对召唤兽物理伤害结果增加#G20%#Y；对人物角色伤害结果减少#R90#Y。","fix_st":0,"name":"争锋","id":707,]),"lx":109,"cnt":7,]),"iDex_All":329,]),(["DEF_MAX":1550,"summon_equip3":(["iLock":1,"cDesc":"#r等级 115  #r气血 +94 防御 +110#r耐久度 460#r#G#G耐力 +16#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级敏捷#Y#Y#r#W制造者：乱世れ双儿#Y#r#r镶嵌效果 #r+80防御 镶嵌等级：10","iType":9112,]),"summon_color":1,"iDod_All":684,"iHp_max":9201,"iGrade":180,"iAtt_F":16,"core_close":0,"lianshou":0,"iMagDef_all":801,"life":5723,"summon_equip2":(["iLock":1,"cDesc":"#r等级 115  #r速度 +38#r耐久度 564#r#G#G耐力 +17#Y #G敏捷 +17#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级敏捷#Y#Y#r#W制造者：太ぢ委屈#Y#r#r镶嵌效果 #r+48速度 镶嵌等级：8","iType":9212,]),"HP_MAX":5500,"summon_equip1":(["iLock":1,"cDesc":"#r等级 125  #r气血 +85 命中率 +14%#r耐久度 539#r#G#G敏捷 +23#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级敏捷#Y#Y#r#W制造者：＇风行水上。#Y#r#r镶嵌效果 #r+28灵力 镶嵌等级：7","iType":9313,]),"MP_MAX":3050,"qianjinlu":10,"mp":2349,"all_skills":(["432":1,"579":1,"552":1,"435":1,"411":1,"328":1,"414":1,]),"att_rate":14,"iDef_All":1313,"iPoint":0,"iRes_all":305,"iMp":1629,"ATK_MAX":1550,"iStr_all":200,"iMp_max":1629,"iAtt_all":1060,"summon_equip4_type":0,"iCor_all":913,"grow":1275,"iMag_all":205,"def":1444,"iType":102078,"left_qlxl":0,"csavezz":"1170|1386|1387|1068|4123|2349","att":1170,"iRealColor":3,"iLock":1,"iGenius":328,"dod":1068,"growthMax":1266,"iHp":9201,"iJjFeedCd":0,"hp":4123,"carrygradezz":0,"iSpe_all":641,"jj_extra_add":(["iRes":12,"iStr":10,"iCor":16,"iMag":13,"iSpe":10,]),"spe":1406,"lastchecksubzz":2019,"sjg":0,"tmp_lingxing":110,"yuanxiao":0,"SPD_MAX":1550,"summon_equip4_desc":"","iBaobao":1,"summon_core":([907:({5,0,([]),}),916:({5,0,([]),}),901:({5,0,([]),}),]),"MS_MAX":1800,"ruyidan":0,"jinjie":(["new_type":0,"core":(["effect":"#Y第二回合以后进场时，我方伤害最高的单位提高#G122#Y伤害力，持续2回合；法术伤害力降低#R8%#Y。（效果与体质、耐力较小值有关）","fix_st":0,"name":"怒吼","id":714,]),"lx":110,"cnt":7,]),"iDex_All":1041,]),(["DEF_MAX":1650,"summon_equip3":(["cDesc":"#r等级 95  #r伤害 +49 防御 +88#r耐久度 197#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4善恶有报#Y#Y#r#W制造者：え九五之尊え#Y#r#r镶嵌效果 #r+150气血 镶嵌等级：5","iType":9110,]),"summon_color":1,"iDod_All":222,"iHp_max":6000,"iGrade":180,"iAtt_F":8,"core_close":1,"lianshou":0,"iMagDef_all":934,"life":3411,"summon_equip2":(["cDesc":"#r等级 95  #r速度 +32 伤害 +48#r耐久度 200  修理失败 1次#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4善恶有报#Y#Y#r#W制造者：女人づ如梦#Y#r#r镶嵌效果 #r+30速度 镶嵌等级：5","iType":9210,]),"HP_MAX":7000,"summon_equip1":(["cDesc":"#r等级 95  #r伤害 +49 命中率 +15%#r耐久度 196  修理失败 1次#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4善恶有报#Y#Y#r#W制造者：弑神丿∴灭世#Y#r#r镶嵌效果 #r+50伤害 镶嵌等级：5","iType":9310,]),"MP_MAX":3600,"qianjinlu":10,"mp":2350,"all_skills":(["405":1,"417":1,"416":1,"411":1,"425":1,"401":1,"404":1,]),"att_rate":15,"iDef_All":872,"iPoint":0,"iRes_all":193,"iMp":1583,"ATK_MAX":1650,"iStr_all":890,"iMp_max":1583,"iAtt_all":2421,"summon_equip4_type":3611,"iCor_all":636,"grow":1281,"iMag_all":192,"def":1084,"iType":102321,"left_qlxl":0,"csavezz":"1431|1084|1087|1109|4147|2350","att":1502,"iRealColor":4,"iLock":1,"iGenius":0,"dod":1109,"growthMax":1300,"iHp":6000,"iJjFeedCd":0,"hp":4147,"carrygradezz":2,"iSpe_all":201,"jj_extra_add":0,"spe":1087,"lastchecksubzz":2019,"sjg":0,"tmp_lingxing":101,"yuanxiao":0,"SPD_MAX":1650,"summon_equip4_desc":"#Y#r玄天灵力 352 （已染色）","iBaobao":1,"summon_core":([907:({5,0,([]),}),901:({5,0,([]),}),902:({5,0,([]),}),913:({5,0,([]),}),932:({5,0,([]),}),935:({2,0,([]),}),]),"MS_MAX":2000,"ruyidan":0,"jinjie":(["new_type":0,"core":(["effect":"#Y使用药品效果上升#G3.2%#Y；受到的所有伤害增加#R15%#Y。（效果与敏捷有关）","fix_st":0,"name":"识药","id":701,]),"lx":101,"cnt":7,]),"iDex_All":334,]),(["DEF_MAX":1650,"summon_equip3":(["iLock":1,"cDesc":"#r等级 115  #r伤害 +60 防御 +108#r耐久度 435#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级偷袭#Y#Y#r#W制造者：依旧。淡笑#Y#r#r镶嵌效果 #r+210气血 镶嵌等级：7","iType":9112,]),"summon_color":1,"iDod_All":243,"iHp_max":7742,"iGrade":180,"iAtt_F":1,"core_close":0,"lianshou":0,"iMagDef_all":950,"life":7824,"summon_equip2":(["iLock":1,"cDesc":"#r等级 125  #r速度 +39 伤害 +60#r耐久度 124#r#G#G力量 +19#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级偷袭#Y#Y#r#W制造者：ミ潮つ小子#Y#r#r镶嵌效果 #r+54速度 镶嵌等级：9","iType":9213,]),"HP_MAX":7000,"summon_equip1":(["iLock":1,"cDesc":"#r等级 105  #r伤害 +49 命中率 +13%#r耐久度 601#r#G#G力量 +20#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级偷袭#Y#Y#r#W制造者：低调ペ☆#Y#r#r镶嵌效果 #r+80伤害 镶嵌等级：8","iType":9311,]),"MP_MAX":3600,"qianjinlu":10,"mp":2184,"all_skills":(["434":1,"403":1,"416":1,"411":1,"401":1,"404":1,"571":1,]),"att_rate":13,"iDef_All":952,"iPoint":0,"iRes_all":195,"iMp":1520,"ATK_MAX":1650,"iStr_all":762,"iMp_max":1520,"iAtt_all":2336,"summon_equip4_type":27462,"iCor_all":821,"grow":1288,"iMag_all":190,"def":1208,"iType":102246,"left_qlxl":0,"csavezz":"1326|1075|1219|1226|4200|2184","att":1501,"iRealColor":5,"iLock":1,"iGenius":0,"dod":1226,"growthMax":1297,"iHp":7742,"iJjFeedCd":0,"hp":4200,"carrygradezz":2,"iSpe_all":199,"jj_extra_add":0,"spe":1219,"lastchecksubzz":2019,"sjg":0,"tmp_lingxing":109,"yuanxiao":0,"SPD_MAX":1650,"summon_equip4_desc":"#Y#r玄天灵力 735","iBaobao":1,"summon_core":([907:({5,0,([]),}),901:({5,0,([]),}),902:({5,0,([]),}),913:({5,0,([]),}),935:({5,0,([]),}),904:({5,0,([]),}),]),"MS_MAX":2000,"ruyidan":0,"jinjie":(["new_type":1,"core":(["effect":"#Y对召唤兽物理伤害结果增加#G20%#Y；对人物角色伤害结果减少#R90#Y。","fix_st":0,"name":"争锋","id":707,]),"lx":109,"cnt":7,]),"iDex_All":389,]),(["DEF_MAX":1650,"summon_equip3":(["iLock":1,"cDesc":"#r等级 125  #r伤害 +54 防御 +84#r耐久度 54#r#G#G力量 +31#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级偷袭#Y#Y#r#W制造者：秋雨潇°逸#Y#r#r镶嵌效果 #r+270气血 镶嵌等级：9","iType":9113,]),"summon_color":1,"iDod_All":484,"iHp_max":5004,"iGrade":180,"iAtt_F":4,"core_close":0,"lianshou":0,"iMagDef_all":887,"life":2628,"summon_equip2":(["iLock":1,"cDesc":"#r等级 125  #r速度 +37 伤害 +59#r耐久度 241#r#G#G敏捷 +15#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级偷袭#Y#Y#r#W制造者：安静あ#Y#r#r镶嵌效果 #r+42速度 镶嵌等级：7","iType":9213,]),"HP_MAX":7000,"summon_equip1":(["iLock":1,"cDesc":"#r等级 125  #r伤害 +50 命中率 +14%#r耐久度 184#r#G#G敏捷 +24#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级偷袭#Y#Y#r#W制造者：小小宝°#Y#r#r镶嵌效果 #r+70伤害 镶嵌等级：7","iType":9313,]),"MP_MAX":3600,"qianjinlu":10,"mp":1809,"all_skills":(["422":1,"401":1,"408":1,"434":1,"405":1,"416":1,"411":1,"407":1,"404":1,]),"att_rate":14,"iDef_All":923,"iPoint":0,"iRes_all":197,"iMp":1442,"ATK_MAX":1650,"iStr_all":894,"iMp_max":1442,"iAtt_all":2545,"summon_equip4_type":0,"iCor_all":494,"grow":1300,"iMag_all":203,"def":1176,"iType":102246,"left_qlxl":0,"csavezz":"1531|1176|1308|1015|3298|1809","att":1601,"iRealColor":5,"iLock":1,"iGenius":0,"dod":1015,"growthMax":1297,"iHp":5004,"iJjFeedCd":0,"hp":3298,"carrygradezz":2,"iSpe_all":477,"jj_extra_add":(["iRes":7,"iStr":16,"iCor":14,"iMag":13,"iSpe":15,]),"spe":1411,"lastchecksubzz":2019,"sjg":0,"tmp_lingxing":110,"yuanxiao":0,"SPD_MAX":1650,"summon_equip4_desc":"","iBaobao":1,"summon_core":([907:({5,0,([]),}),919:({5,0,([]),}),901:({5,0,([]),}),913:({5,0,([]),}),932:({5,0,([]),}),904:({5,0,([]),}),]),"MS_MAX":2000,"ruyidan":0,"jinjie":(["new_type":1,"core":(["effect":"#Y忽略人物角色#G200#Y防御力；对召唤兽物理伤害结果减少#R5%#Y。","fix_st":0,"name":"力破","id":706,]),"lx":110,"cnt":7,]),"iDex_All":788,]),(["DEF_MAX":1650,"summon_equip3":(["cDesc":"#r等级 125  #r伤害 +63 气血 +88 防御 +114#r耐久度 494#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4死亡召唤#Y#Y#r#W制造者：°淡妆#Y#r#r镶嵌效果 #r+72防御 镶嵌等级：9","iType":9113,]),"summon_color":1,"iDod_All":142,"iHp_max":2024,"iGrade":126,"iAtt_F":4,"core_close":0,"lianshou":5,"iMagDef_all":368,"life":4011,"summon_equip2":(["cDesc":"#r等级 115  #r速度 +33 伤害 +53#r耐久度 456#r#G#G耐力 +19#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4死亡召唤#Y#Y#r#W制造者：爱我就操我阿#Y#r#r镶嵌效果 #r+6速度 镶嵌等级：1","iType":9212,]),"HP_MAX":7000,"summon_equip1":(["cDesc":"#r等级 125  #r伤害 +50 命中率 +15%#r耐久度 556#r#G#G耐力 +20#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4死亡召唤#Y#Y#r#W制造者：こ小姐#Y#r#r镶嵌效果 #r+90伤害 镶嵌等级：9","iType":9313,]),"MP_MAX":3600,"qianjinlu":0,"mp":1435,"all_skills":(["403":1,"417":1,"406":1,"414":1,"401":1,"434":1,"405":1,"416":1,"435":1,"411":1,"425":1,"404":1,]),"att_rate":15,"iDef_All":906,"iPoint":846,"iRes_all":185,"iMp":874,"ATK_MAX":1650,"iStr_all":145,"iMp_max":874,"iAtt_all":1220,"summon_equip4_type":0,"iCor_all":154,"grow":1250,"iMag_all":137,"def":1415,"iType":102246,"left_qlxl":0,"csavezz":"1134|1388|922|964|3823|1435","att":1484,"iRealColor":5,"iGenius":0,"dod":964,"growthMax":1297,"iHp":2024,"iJjFeedCd":0,"hp":3823,"carrygradezz":2,"iSpe_all":148,"jj_extra_add":0,"spe":922,"lastchecksubzz":2019,"sjg":5,"tmp_lingxing":108,"yuanxiao":15,"SPD_MAX":1650,"summon_equip4_desc":"","iBaobao":1,"summon_core":([907:({5,0,([]),}),913:({5,0,([]),}),901:({5,0,([]),}),932:({5,0,([]),}),935:({1,1,([]),}),904:({5,0,([]),}),]),"MS_MAX":2000,"ruyidan":0,"jinjie":(["new_type":1,"core":(["effect":"#Y忽略人物角色#G84#Y防御力；对召唤兽物理伤害结果减少#R8%#Y。","fix_st":0,"name":"力破","id":706,]),"lx":108,"cnt":7,]),"iDex_All":211,]),(["DEF_MAX":1650,"summon_equip3":(["cDesc":"#r等级 105  #r气血 +74 防御 +74#r耐久度 223#r#G#G法力 +15#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：我是卖面膜的#Y#r#r镶嵌效果 #r+60气血 镶嵌等级：2","iType":9111,]),"summon_color":1,"iDod_All":268,"iHp_max":4211,"iGrade":180,"iAtt_F":4,"core_close":1,"lianshou":0,"iMagDef_all":1353,"life":1123,"summon_equip2":(["cDesc":"#r等级 125  #r速度 +39#r耐久度 75#r#G#G力量 +22#Y #G法力 +17#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：安静あ#Y#r#r镶嵌效果 #r+36速度 镶嵌等级：6","iType":9213,]),"HP_MAX":7000,"summon_equip1":(["cDesc":"#r等级 125  #r命中率 +16%#r耐久度 92#r#G#G灵力 +10 #G法力 +18#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#W制造者：哈⌒〓⌒哈#Y#r#r镶嵌效果 #r+28灵力 镶嵌等级：7","iType":9313,]),"MP_MAX":3600,"qianjinlu":6,"mp":2513,"all_skills":(["578":1,"424":1,"426":1,"661":1,"575":1,"577":1,"573":1,]),"att_rate":16,"iDef_All":848,"iPoint":0,"iRes_all":202,"iMp":5300,"ATK_MAX":1650,"iStr_all":216,"iMp_max":5300,"iAtt_all":833,"summon_equip4_type":3611,"iCor_all":400,"grow":1245,"iMag_all":1177,"def":1060,"iType":102321,"left_qlxl":0,"csavezz":"894|785|1072|1350|3654|2513","att":894,"iRealColor":4,"iGenius":426,"dod":1350,"growthMax":1300,"iHp":4211,"iJjFeedCd":0,"hp":3654,"carrygradezz":2,"iSpe_all":199,"jj_extra_add":0,"spe":1072,"lastchecksubzz":2019,"sjg":0,"tmp_lingxing":108,"yuanxiao":0,"SPD_MAX":1650,"summon_equip4_desc":"#Y#r玄天灵力 303 （已染色）","iBaobao":1,"summon_core":([907:({5,0,([]),}),928:({3,1,([]),}),905:({5,0,([]),}),904:({5,0,([]),}),906:({5,0,([]),}),936:({5,0,([]),}),]),"MS_MAX":2000,"ruyidan":0,"jinjie":(["new_type":0,"core":(["effect":"#Y第二回合以后进场时，#G100%#Y概率对血量百分比最低的单位使用随机法术；气血上限降低#R10%#Y。（效果与魔力有关）","fix_st":0,"name":"瞬法","id":717,]),"lx":108,"cnt":7,]),"iDex_All":315,]),}),"iHp":4596,"AllEquip":([17:(["cDesc":"#r等级 130  五行 水#r#r防御 +246#r耐久度 315  修理失败 2次#r锻炼等级 5  镶嵌宝石 舍利子#r#G#G灵力 +30#Y #G魔力 +15#Y #G耐力 +29#Y#Y#r#W制造者：′Soul、芸ミ强化打造#Y#r#Y熔炼效果：#r#Y#r+4防御#Y#r#Y   ","iType":2655,]),16:(["iLock":1,"cDesc":"#r等级 140  五行 土#r#r伤害 +573 命中 +525#r耐久度 378  修理失败 1次#r锻炼等级 8  镶嵌宝石 太阳石#r#G#G魔力 +32#Y #G力量 +30#Y#Y#r#c4DBAF4特效：#c4DBAF4坚固#Y#r#G开运孔数：5孔/5孔#G#r符石: 灵力 +1.5#n#G#r符石: 力量 +1 固定伤害 +2#n#G#r符石: 法伤 +1#n#G#r符石: 命中 +4#n#G#r符石: 敏捷 +1 魔法 +6#n#b#G#r星位：速度 +2.5#n#r#cEE82EE符石组合: 神木恩泽符石#r门派条件：神木林 #r部位条件：武器 #r增加门派技能神木恩泽等级6级#Y#r#W制造者：〃诛仙の观音强化打造#Y  ","iType":1562,]),13:(["cDesc":"等级 60#r防御 +13#r耐久度 95#r精炼等级 4#r#G物理暴击等级 +8 #cEE82EE[+16]#r#G法术伤害 +6 #cEE82EE[+16]#r#G法术伤害 +6 #cEE82EE[+16]#r#W制造者：石石石亲手强化打造#","iType":27001,]),15:(["cDesc":"等级 80#r速度 +14#r耐久度 448  修理失败 1次#r精炼等级 5#r#G防御 +18 #cEE82EE[+40]#r#G抵抗封印等级 +19 #cEE82EE[+40]#r#G气血 +62 #cEE82EE[+140]#r#W制造者：′Ace°强化打造#","iType":27302,]),18:(["iLock":1,"cDesc":"#r等级 80  #r气血 +360 防御 +34#r耐久度 228  修理失败 1次#r锻炼等级 5  镶嵌宝石 光芒石#Y#r#c4DBAF4套装效果：变身术之灵符女娲#Y#Y  ","iType":2914,]),12:(["iLock":1,"cDesc":"等级 120#r法术伤害 +24#r耐久度 85#r精炼等级 4#r#G法术暴击等级 +12 #cEE82EE[+16]#r#G法术伤害 +13 #cEE82EE[+16]#r#W制造者：中了美人计″强化打造#","iType":27104,]),187:(["cDesc":"等级 120#r防御 +25#r耐久度 500#r精炼等级 10#r#G法术暴击等级 +13 #cEE82EE[+40]#r#G法术暴击等级 +12 #cEE82EE[+40]#r#G法术暴击等级 +14 #cEE82EE[+40]#r#W制造者：错过的流年”强化打造#","iType":27004,]),21:(["cDesc":"#r等级 140  #r灵力 +250#r耐久度 395#r锻炼等级 6  镶嵌宝石 舍利子#Y#r#c4DBAF4特效：龙宫专用#r玩家1879专用#r#W制造者：A哥强化打造#Y#r#Y熔炼效果：#r#Y#r+4灵力#Y  ","iType":2856,]),20:(["cDesc":"#r等级 70  #r魔法 +70 防御 +90#r耐久度 233  修理失败 2次#r锻炼等级 5  镶嵌宝石 月亮石#Y#r#c4DBAF4套装效果：变身术之灵符女娲#Y#Y#r#G开运孔数：1孔/3孔#Y   ","iType":2508,]),2:(["cDesc":"#r等级 160  五行 木#r#r防御 +303#r耐久度 68#r锻炼等级 15  镶嵌宝石 舍利子#r#G#G灵力 +90#Y #G魔力 +38#Y #G耐力 +28#Y#r#c4DBAF4套装效果：变身术之金身罗汉#Y#Y#r#G开运孔数：5孔/5孔#G#r符石: 魔力 +1 法术伤害 +2#n#G#r符石: 气血 +15 速度 +1.5#n#b#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r星位：防御 +6#n#r#cEE82EE符石组合: 瞬息万变符石#r门派条件：神木林 #r部位条件：铠甲/女衣 #r增加门派技能瞬息万变等级6级#Y#r#W制造者：水封扫地僧．强化打造#Y#r#Y熔炼效果：#r#Y#r+2耐力 +14防御 #r#Y  ","iType":2658,]),6:(["cDesc":"#r等级 160  五行 水#r#r伤害 +735 命中 +574#r耐久度 58#r锻炼等级 14  镶嵌宝石 太阳石#r#G#G魔力 +29#Y #G体质 +34#Y#Y#r#c4DBAFF法术暴击伤害 +3.53%#Y#r#G开运孔数：5孔/5孔#G#r符石: 魔力 +1 法术伤害 +2#n#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 魔力 +1 法术伤害 +2#n#G#r符石: 气血 +15 速度 +1.5#n#G#r星位：伤害 +1.5#n#r#cEE82EE符石组合: 高山流水#r门派条件：无#r部位条件：无#r对召唤兽增加人物等级+30的法术伤害。(该组合全身只有一件装备起效)#Y#r#W制造者：Aresメ经典强化打造#Y  ","iType":1080,]),14:(["cDesc":"等级 80#r抵抗封印等级 +16#r耐久度 490#r精炼等级 4#r#G抵抗封印等级 +20 #cEE82EE[+32]#r#G防御 +16 #cEE82EE[+32]#r#G气血 +56 #cEE82EE[+112]#r#W制造者：の’小北︷．强化打造#","iType":27202,]),19:(["iLock":1,"cDesc":"#r等级 80  #r敏捷 +31 防御 +29#r耐久度 291  修理失败 2次#r锻炼等级 5  镶嵌宝石 黑宝石#r#G#G速度 +40#Y#Y#r#c4DBAF4套装效果：变身术之灵符女娲#Y#Y  ","iType":2709,]),4:(["cDesc":"#r等级 160  #r灵力 +328#r耐久度 492#r锻炼等级 10  镶嵌宝石 舍利子#Y#r#c4DBAF4特效：神木林专用#r玩家1879专用#r#W制造者：么么◇花眠″强化打造#Y  ","iType":2858,]),]),"icolor_ex":0,"shenqi_yellow":"0神器灵气：233#r","cName":"企1685241765","iCGBoxAmount":6,"iExptSki4":25,"iGoodness":1281,"iMaxExpt3":25,"iMarry":0,"iMaxExpt1":20,"iSchool":13,"iBeastSki1":25,"total_avatar":54,"iExptSki2":25,"bid":1,"AchPointTotal":3489,"iUpExp":258126285,"iBeastSki3":25,"iExptSki5":5,"iMag_All":1391,"rent":170938,"more_attr":(["attrs":({(["lv":0,"idx":3,]),(["lv":0,"idx":2,]),(["lv":0,"idx":10,]),(["lv":0,"idx":1,]),(["lv":0,"idx":6,]),(["lv":0,"idx":12,]),(["lv":0,"idx":5,]),(["lv":0,"idx":8,]),(["lv":0,"idx":4,]),(["lv":0,"idx":9,]),(["lv":249,"idx":7,]),(["lv":0,"idx":11,]),(["lv":538,"idx":13,]),(["lv":1809,"idx":14,]),}),]),"ExpJwBase":1000000000,"iDod_All":538,"shenqi_pos":({3,6222,}),"iRace":1,"commu_name":"","idbid_desc":({1,}),"all_skills":(["166":1,"161":2,"198":1,"32817":1,"52031":1,"96":180,"221":21,"169":1,"32814":1,"95":180,"205":160,"52032":1,"94":180,"201":140,"237":40,"40132":1,"225":1,"160":3,"197":2,"32825":1,"32819":1,"32805":1,"92":180,"207":160,"32822":1,"32802":1,"153":5,"196":1,"97":180,"211":140,"220":5,"219":5,"231":160,"210":125,"230":40,"222":5,"162":1,"32810":1,"173":1,"179":1,"208":140,"218":120,"216":140,"164":1,"170":3,"206":108,"32807":1,"163":1,"212":150,"167":1,"204":160,"223":5,"52016":1,"174":1,"93":180,"1650":1,"209":88,"202":143,"154":6,"217":160,"91":186,"203":11,]),"outdoor_level":7,"iDef_All":1075,"iIcon":25,"iOrgOffer":0,"iMp":11855,"iCGTotalAmount":140,"iCash":3087616,"iBadness":0,"sword_score":1125,"total_horse":10,"HeroScore":4766,"iHp_Max":4596,"iSmithski":6576,"iSaving":0,"iSewski":20391,"sum_exp":405,"energy":744,"cOrg":"东幻い网络","farm_level":"3","iSkiPoint":1,"iSchOffer":186,"iDesc":0,"iTotalMagDef_all":1809,"iStr_All":186,"TA_iAllPoint":0,"pet":({(["all_skills":({(["value":0,"name":"灵佑",]),}),"iType":4071,"cName":"泡泡精灵",]),}),"iSpe_All":186,"iMarry2":0,"iErrantry":0,"datang_feat":2027,"shenqi":(["components":({(["unlock":1,"wuxing":({(["wuxingshi_level":3,"attr":"法术暴击 +8","affix_disable":0,"wuxingshi_affix":0,"id":16,"status":1,]),(["wuxingshi_level":3,"attr":"法术暴击 +8","affix_disable":0,"wuxingshi_affix":0,"id":16,"status":1,]),(["wuxingshi_level":3,"attr":"法术暴击 +8","affix_disable":0,"wuxingshi_affix":0,"id":16,"status":1,]),(["wuxingshi_level":3,"attr":"法术暴击 +8","affix_disable":0,"wuxingshi_affix":9,"id":16,"status":1,]),}),"level":2,]),(["unlock":1,"wuxing":({(["wuxingshi_level":3,"attr":"法术暴击 +7","affix_disable":0,"wuxingshi_affix":0,"id":16,"status":1,]),(["wuxingshi_level":3,"attr":"法术暴击 +7","affix_disable":0,"wuxingshi_affix":0,"id":16,"status":1,]),(["wuxingshi_level":3,"attr":"法术暴击 +7","affix_disable":0,"wuxingshi_affix":0,"id":16,"status":1,]),(["wuxingshi_level":3,"attr":"法术暴击 +7","affix_disable":0,"wuxingshi_affix":0,"id":16,"status":1,]),}),"level":2,]),(["unlock":1,"wuxing":({(["wuxingshi_level":2,"attr":"法术暴击 +6","affix_disable":0,"wuxingshi_affix":9,"id":16,"status":1,]),(["wuxingshi_level":3,"attr":"法术暴击 +8","affix_disable":0,"wuxingshi_affix":0,"id":16,"status":1,]),(["wuxingshi_level":3,"attr":"法术暴击 +8","affix_disable":0,"wuxingshi_affix":0,"id":16,"status":1,]),(["wuxingshi_level":2,"attr":"法术暴击 +7","affix_disable":0,"wuxingshi_affix":14,"id":16,"status":1,]),}),"level":2,]),}),"full":1,"skill_level":2,"skill":53131,"skill_desc":"每点被消耗的风灵增加你80点法术伤害结果，最多叠加3层，死亡后清零。","active":1,"power":0,"id":6222,"attributes":({(["disable":1,"attr":"速度 +0","id":1,]),(["disable":1,"attr":"气血 +0","id":2,]),(["disable":1,"attr":"法术伤害 +0","id":8,]),(["disable":0,"attr":"法术暴击 +90","id":16,]),(["disable":1,"attr":"抵抗封印 +0","id":4,]),}),]),"iCGBodyAmount":0,"iBeastSki2":25,"iExptSki3":25,"AllRider":([1:(["iGrade":170,"exgrow":22672,"mattrib":"魔力","all_skills":([611:1,]),"iType":504,"ExtraGrow":100,]),7:(["iGrade":129,"exgrow":23155,"mattrib":"体质","all_skills":([602:3,]),"iType":504,"ExtraGrow":100,]),5:(["iGrade":68,"exgrow":12592,"mattrib":"","all_skills":([]),"iType":505,"ExtraGrow":0,]),4:(["iGrade":170,"exgrow":23008,"mattrib":"耐力","all_skills":([600:3,601:3,]),"iType":509,"ExtraGrow":100,]),6:(["iGrade":166,"exgrow":23155,"mattrib":"魔力","all_skills":([]),"iType":505,"ExtraGrow":100,]),]),"iCor_All":222,"iBeastSki4":25,"iMaxExpt2":25,"jiyuan":11,"ExAvt":([17:(["order":1,"iType":13790,"cName":"冰寒绡",]),16:(["order":2,"iType":12498,"cName":"冰寒绡",]),22:(["order":5,"iType":12005,"cName":"璀璨新郎服",]),12:(["order":20,"iType":14401,"cName":"动物装饰篮",]),18:(["order":3,"iType":40023,"cName":"冰寒绡·月白",]),9:(["order":19,"iType":13927,"cName":"隐夜鬼蝠",]),41:(["order":9,"iType":12420,"cName":"兰陵魅影",]),6:(["order":18,"iType":13857,"cName":"小熊竹篓",]),24:(["order":11,"iType":12372,"cName":"夏日清凉",]),1:(["order":12,"iType":13119,"cName":"龙马炫卡",]),50:(["order":17,"iType":13282,"cName":"武将脸谱头饰",]),3:(["order":8,"iType":12440,"cName":"华风汉雅",]),10:(["order":7,"iType":12111,"cName":"隐夜鬼蝠",]),51:(["order":16,"iType":14043,"cName":"有凰来栖",]),8:(["order":6,"iType":14404,"cName":"蓝色妖姬",]),54:(["order":15,"iType":14407,"cName":"海洋武器",]),5:(["order":10,"iType":12103,"cName":"雁翎银钩",]),19:(["order":4,"iType":12765,"cName":"冰寒绡·月白",]),45:(["order":14,"iType":12703,"cName":"胡旋回雪",]),31:(["order":13,"iType":13232,"cName":"蓝色顽皮小狗帽",]),]),"iDex_All":262,"i3FlyLv":4,"TA_iAllNewPoint":9,"iExptSki1":5,])'
# desc = '(["iBeastSki1":14,"iSumAmount":8,"commu_name":"","iSkiPoint":1,"iBeastSki3":10,"outdoor_level":1,"iDex_All":303,"iRace":3,"iMarry":0,"iExptSki5":8,"datang_feat":5970,"iMaxExpt4":22,"iTotalMagDef_all":832,"iMarry2":0,"energy":23,"AllEquip":([1:(["iType":2555,"cDesc":"#r等级 130  五行 水#r#r防御 +78 魔法 +143#r耐久度 285#r锻炼等级 8  镶嵌宝石 红玛瑙#r#G#G命中 +200#Y#Y#r#c4DBAF4套装效果：附加状态碎星诀#Y#Y#r#G开运孔数：5孔/5孔#G#r符石: 力量 +1 防御 +3#n#G#r符石: 敏捷 +1 伤害 +1.5#n#G#r符石: 命中 +4#n#G#r符石: 力量 +1#n#G#r符石: 速度 +1.5#n#r#cEE82EE符石组合: 百步穿杨#r门派条件：无#r部位条件：无#r物理攻击时有20%的几率给目标额外造成100点伤害#Y#r#W制造者：山鸡叔叔#Y#r#Y熔炼效果：#r#Y#r-2防御 +16魔法 #r#Y  ",]),190:(["iType":27305,"cDesc":"等级 140#r速度 +20#r耐久度 417  修理失败 1次#r精炼等级 3#r#G抗物理暴击等级 +33 #cEE82EE[+24]#r#G气血 +103 #cEE82EE[+84]#r#W制造者：だ森林→狼だ强化打造#",]),5:(["iType":2952,"cDesc":"#r等级 100  五行 火#r#r气血 +551 防御 +55#r耐久度 286#r锻炼等级 8  镶嵌宝石 光芒石#Y#r#c4DBAF4特效：#c4DBAF4永不磨损#Y#r#c4DBAF4套装效果：附加状态碎星诀#Y#Y#r#G开运孔数：4孔/4孔#G#r符石: 力量 +1#n#Y#r#W制造者：Mighty°月隐#Y#r#Y熔炼效果：#r#Y#r+6防御 +14气血 #r#Y  ",]),6:(["iType":1562,"cDesc":"#r等级 140  五行 土#r#r伤害 +451 命中 +772#r耐久度 415#r锻炼等级 8  镶嵌宝石 红玛瑙#r#G#G敏捷 +17#Y#r#c4DBAF4特效：#c4DBAF4永不磨损#Y#r#G开运孔数：3孔/5孔#Y #r#W制造者：°猫丝〈清风强化打造#Y#r#Y熔炼效果：#r#Y#r+3敏捷#Y  ",]),2:(["iType":2655,"cDesc":"#r等级 130  五行 金#r#r气血 +160 防御 +287#r耐久度 105#r锻炼等级 10  镶嵌宝石 月亮石、 光芒石#r#G#G力量 +27#Y#Y#r#c4DBAF4套装效果：附加状态碎星诀#Y#Y#r#G开运孔数：5孔/5孔#G#r符石: 魔力 +1 命中 +4#n#G#r符石: 体质 +1 防御 +3#n#G#r符石: 耐力 +1 命中 +4#n#G#r符石: 防御 +3#n#G#r符石: 气血 +10#n#r#cEE82EE符石组合: 气吞山河符石#r门派条件：凌波城 #r部位条件：铠甲/女衣 #r增加门派技能气吞山河等级6级#Y#r#W制造者：餐花道人强化打造#Y#r#Y熔炼效果：#r#Y#r+10防御#Y  ",]),]),"idbid_desc":({}),"jiyuan":0,"AchPointTotal":2358,"fabao":([17:(["iType":6061,"cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G300#Y 五行：#G火#Y#r修炼境界：第#G4#Y层 #c13E1EC预知福祸#Y",]),1:(["iType":6076,"cDesc":"0#Y灵气：#G31 #Y 五行：#G金#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y",]),16:(["iType":6064,"cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G290#Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y",]),13:(["iType":6016,"cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G300#Y 五行：#G金#Y#r修炼境界：第#G1#Y层 #cCECECE了然于胸#Y",]),26:(["iType":6029,"cDesc":"0#W【回合限制】6#r#Y#Y灵气：#G295#Y 五行：#G火#Y#r修炼境界：第#G5#Y层 #c01FEC5脱胎换骨#Y",]),22:(["iType":6024,"cDesc":"0#W【回合限制】150#r#Y#Y灵气：#G300#Y 五行：#G金#Y#r修炼境界：第#G3#Y层 #cB7BFF8渐入佳境#Y",]),15:(["iType":6065,"cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G500#Y 五行：#G土#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y",]),3:(["iType":6020,"cDesc":"0#Y灵气：#G367#Y 五行：#G火#Y#r修炼境界：第#G12#Y层 #cFF6F28笑傲西游#Y#r传送至五庄观（40，33）",]),25:(["iType":6073,"cDesc":"0#Y灵气：#G0  #Y 五行：#G水#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y",]),18:(["iType":6022,"cDesc":"0#Y灵气：#G430#Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y",]),12:(["iType":6030,"cDesc":"0#W【回合限制】10#r#Y#Y灵气：#G442#Y 五行：#G木#Y#r修炼境界：第#G13#Y层 #cFF6F28法力无边#Y",]),11:(["iType":6027,"cDesc":"0#W【回合限制】2#r#Y#Y灵气：#G105#Y 五行：#G水#Y#r修炼境界：第#G6#Y层 #cA6F101出神入化#Y",]),21:(["iType":6021,"cDesc":"0#W【回合限制】3#r#Y#Y灵气：#G283#Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y",]),19:(["iType":6025,"cDesc":"0#W【回合限制】150#r#Y#Y灵气：#G24 #Y 五行：#G水#Y#r修炼境界：第#G5#Y层 #c01FEC5脱胎换骨#Y",]),23:(["iType":6097,"cDesc":"0#Y灵气：#G21 #Y 五行：#G水#Y#r修炼境界：第#G12#Y层 #cFF6F28笑傲西游#Y#r#n#Y最佳五行属性奖励：额外提升3点法术伤害#G（已生效）#Y",]),4:(["iType":6078,"cDesc":"0#W【回合限制】5#r#Y#Y灵气：#G300#Y 五行：#G木#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y",]),]),"iSmithski":9,"rent":47071,"iDesc":0,"AllSummon":({(["iRealColor":0,"left_qlxl":7,"iCor_all":240,"iMagDef_all":659,"iDex_All":351,"iBaobao":0,"att_rate":14,"iHp_max":2458,"jinjie":(["cnt":0,"lx":0,"core":([]),]),"carrygradezz":1,"csavezz":"1309|1302|1192|1238|4010|1757","iRes_all":173,"ATK_MAX":1600,"summon_equip4_type":0,"iMag_all":168,"iHp":2458,"lianshou":0,"all_skills":(["416":1,"325":1,"554":1,"304":1,]),"core_close":0,"MS_MAX":2000,"life":407,"iMp_max":1194,"spe":1192,"summon_equip3":(["iType":9112,"cDesc":"#r等级 115  #r防御 +108#r耐久度 542#r#G#G体质 +6#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4嗜血追击#Y#Y#r#W制造者：◇魉◆#Y",]),"DEF_MAX":1600,"def":1302,"summon_core":([903:({1,0,([]),}),]),"MP_MAX":3500,"summon_equip4_desc":"","summon_color":0,"jj_extra_add":0,"summon_equip2":(["iType":9209,"cDesc":"#r等级 85  #r速度 +33#r耐久度 362#r#G#G敏捷 +9#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4嗜血追击#Y#Y#r#W制造者：尘埃湮没思念#Y",]),"iAtt_F":16,"tmp_lingxing":0,"summon_equip1":(["iType":9312,"cDesc":"#r等级 115  #r命中率 +14%#r耐久度 459#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4嗜血追击#Y#Y#r#W制造者：◇魉◆#Y",]),"mp":1757,"iDod_All":330,"iSpe_all":267,"iType":102128,"iPoint":0,"iAtt_all":1604,"lastchecksubzz":2019,"qianjinlu":0,"iGenius":0,"iJjFeedCd":0,"iStr_all":687,"yuanxiao":0,"iGrade":158,"iMp":1194,"growthMax":1287,"hp":4010,"dod":1238,"HP_MAX":6500,"sjg":0,"iDef_All":879,"ruyidan":0,"grow":1268,"SPD_MAX":1600,"att":1309,]),}),"shenqi_pos":({0,0,}),"changesch":({7,14,7,}),"TA_iAllNewPoint":6,"iSumAmountEx":0,"ori_race":3,"cName":"升龙道ジ戊土","cOrg":"国子监最帅的","iHp":4274,"AllRider":([1:(["iType":503,"all_skills":([611:1,]),"ExtraGrow":70,"mattrib":"体质","exgrow":20241,"iGrade":150,]),]),"iLearnCash":1300655,"all_skills":(["166":1,"206":40,"33813":1,"202":87,"197":1,"154":5,"198":1,"216":100,"199":1,"208":41,"167":1,"179":1,"103":162,"52031":1,"98":164,"173":1,"52032":1,"33805":1,"210":10,"211":65,"219":1,"207":10,"101":150,"33802":1,"230":5,"201":121,"203":10,"52016":1,"33816":1,"204":40,"169":1,"209":40,"170":2,"196":1,"217":18,"99":155,"33811":1,"33808":1,"205":35,"174":1,"102":160,"212":65,"162":1,"222":1,"100":155,"159":9,"40141":1,"104":90,"160":5,"218":62,]),"iDamage_All":2234,"iMag_All":165,"iExptSki3":6,"iUpExp":243589218,"iGoodness":1455,"ExpJwBase":1000000000,"iMaxExpt1":25,"iRes_All":172,"addPoint":21,"iHp_Eff":4324,"iExptSki1":25,"TA_iAllPoint":0,"iAtt_All":3038,"ExAvt":([1:(["order":4,"cName":"龙纹光晕","iType":14004,]),3:(["order":1,"cName":"狼牙棒","iType":11169,]),5:(["order":3,"cName":"追风少侠","iType":12808,]),4:(["order":2,"cName":"夏日清凉","iType":12370,]),2:(["order":5,"cName":"怀旧龙太子炫卡","iType":19586,]),]),"iMp_Max":1525,"iSaving":0,"iSewski":0,"shenqi":([]),"pet":({}),"iCGTotalAmount":0,"iMagDef_All":832,"total_horse":3,"iCGBodyAmount":0,"commu_gid":0,"iBeastSki2":10,"shenqi_yellow":"","rent_level":1,"igoodness_sav":632,"iNutsNum":124,"iBeastSki4":9,"iDod_All":200,"iBadness":0,"ori_desc":4672,"iPoint":0,"xianyu":0,"iMaxExpt2":22,"icolor_ex":0,"iCash":5978,"farm_level":0,"iIcon":46,"iExptSki4":16,"propKept":([1:(["iCor":229,"iStr":1067,"iRes":171,"iMag":164,"iSpe":169,]),0:(["iCor":171,"iStr":172,"iRes":171,"iMag":1027,"iSpe":172,]),2:(["iCor":192,"iStr":172,"iRes":171,"iMag":1092,"iSpe":173,]),]),"i3FlyLv":0,"iPcktPage":0,"iMaxExpt3":20,"sword_score":0,"iCor_All":230,"more_attr":(["attrs":({(["lv":0,"idx":12,]),(["lv":57,"idx":9,]),(["lv":0,"idx":7,]),(["lv":0,"idx":8,]),(["lv":0,"idx":4,]),(["lv":0,"idx":2,]),(["lv":0,"idx":5,]),(["lv":0,"idx":3,]),(["lv":0,"idx":10,]),(["lv":0,"idx":6,]),(["lv":0,"idx":1,]),(["lv":0,"idx":11,]),(["lv":200,"idx":13,]),(["lv":832,"idx":14,]),}),]),"iZhuanZhi":2,"iHp_Max":4711,"sum_exp":100,"iTotalMagDam_all":982,"iStr_All":1097,"iGrade":159,"iOrgOffer":4214,"ExpJw":0,"iMp":1520,"iSchool":14,"iExptSki2":22,"total_avatar":5,"iDef_All":1062,"usernum":35976889,"normal_horse":3,"iSchOffer":366,"HeroScore":454,"iCGBoxAmount":1,"HugeHorse":([16:(["nosale":0,"cName":"沉星寒犀","iType":11016,"order":3,"iSkillLevel":1,"iSkill":622,]),219:(["nosale":0,"cName":"烈焰斗猪","iType":11190,"order":2,"iSkillLevel":0,"iSkill":0,]),113:(["nosale":0,"cName":"流云玉佩","iType":11098,"order":1,"iSkillLevel":0,"iSkill":0,]),]),"iSpe_All":190,"bid":0,"iErrantry":0,"iPride":800,])'
# desc = "([\"iSpe_All\":120,\"usernum\":11533488,\"iHp_Eff\":2530,\"iDod_All\":361,\"iBadness\":0,\"iDesc\":0,\"datang_feat\":5307,\"fabao\":([15:([\"cDesc\":\"0#W【回合限制】10#r#Y#Y灵气：#G365#Y 五行：#G火#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y\",\"iType\":6033,]),26:([\"cDesc\":\"0#W【回合限制】3#r#Y#Y灵气：#G166#Y 五行：#G水#Y#r修炼境界：第#G9#Y层 #cFF6F28不堕轮回#Y\",\"iType\":6018,]),29:([\"cDesc\":\"0#Y灵气：#G259#Y 五行：#G木#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y\",\"iType\":6072,]),21:([\"cDesc\":\"0#W【回合限制】1#r#Y#Y灵气：#G50 #Y 五行：#G木#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y\",\"iType\":6062,]),30:([\"cDesc\":\"0#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G7#Y层 #cFFCF2D神乎其技#Y\",\"iType\":6008,]),32:([\"cDesc\":\"0#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y\",\"iType\":6073,]),2:([\"cDesc\":\"0#Y灵气：#G300#Y 五行：#G火#Y#r修炼境界：第#G12#Y层 #cFF6F28法力无边#Y\",\"iType\":6034,]),24:([\"cDesc\":\"0#W【回合限制】5#r#Y#Y灵气：#G414#Y 五行：#G金#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y\",\"iType\":6035,]),34:([\"cDesc\":\"0#Y灵气：#G50 #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y\",\"iType\":6067,]),40:([\"cDesc\":\"0#W【回合限制】10#r#Y#Y灵气：#G59 #Y 五行：#G土#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y\",\"iType\":6023,]),23:([\"cDesc\":\"0#W【回合限制】5#r#Y#Y灵气：#G390#Y 五行：#G水#Y#r修炼境界：第#G14#Y层 #cFF6F28返璞归真#Y\",\"iType\":6019,]),17:([\"cDesc\":\"0#Y灵气：#G48 #Y 五行：#G水#Y#r修炼境界：第#G10#Y层 #cFF6F28举世无双#Y#r#n#Y最佳五行属性奖励：额外增加1层效果#G（已生效）#Y\",\"iType\":6102,]),13:([\"cDesc\":\"0#W【回合限制】3#r#Y#Y灵气：#G89 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82心法初成#Y\",\"iType\":6014,]),27:([\"cDesc\":\"0#W【回合限制】150#r#Y#Y灵气：#G10 #Y 五行：#G木#Y#r修炼境界：第#G5#Y层 #c01FEC5脱胎换骨#Y\",\"iType\":6025,]),22:([\"cDesc\":\"0#W【回合限制】3#r#Y#Y灵气：#G50 #Y 五行：#G火#Y#r修炼境界：第#G5#Y层 #c01FEC5脱胎换骨#Y\",\"iType\":6016,]),11:([\"cDesc\":\"0#Y灵气：#G433#Y 五行：#G木#Y#r修炼境界：第#G5#Y层 #c01FEC5移星换斗#Y\",\"iType\":6022,]),12:([\"cDesc\":\"0#W【回合限制】3#r#Y#Y灵气：#G70 #Y 五行：#G火#Y#r修炼境界：第#G5#Y层 #c01FEC5脱胎换骨#Y\",\"iType\":6064,]),18:([\"cDesc\":\"0#W【回合限制】3#r#Y#Y灵气：#G310#Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y\",\"iType\":6028,]),20:([\"cDesc\":\"0#W【回合限制】5#r#Y#Y灵气：#G212#Y 五行：#G火#Y#r修炼境界：第#G9#Y层 #cFF6F28登峰造极#Y\",\"iType\":6061,]),14:([\"cDesc\":\"0#Y灵气：#G500#Y 五行：#G水#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y\",\"iType\":6063,]),1:([\"cDesc\":\"0#Y灵气：#G0  #Y 五行：#G金#Y#r修炼境界：第#G9#Y层 #cFF6F28不堕轮回#Y#r传送至地狱迷宫四层（96，52）\",\"iType\":6020,]),28:([\"cDesc\":\"0#W【回合限制】3#r#Y#Y灵气：#G50 #Y 五行：#G水#Y#r修炼境界：第#G0#Y层 #c7D7E82元神初具#Y\",\"iType\":6026,]),3:([\"cDesc\":\"0#Y灵气：#G200#Y 五行：#G水#Y#r修炼境界：第#G9#Y层 #cFF6F28不堕轮回#Y\",\"iType\":6002,]),25:([\"cDesc\":\"0#W【回合限制】2#r#Y#Y灵气：#G141#Y 五行：#G木#Y#r修炼境界：第#G9#Y层 #cFF6F28登峰造极#Y\",\"iType\":6027,]),37:([\"cDesc\":\"0#W【回合限制】10#r#Y#Y灵气：#G101#Y 五行：#G木#Y#r修炼境界：第#G15#Y层 #cFF6F28天人合一#Y\",\"iType\":6030,]),31:([\"cDesc\":\"0#W【回合限制】1#r#Y#Y灵气：#G50 #Y 五行：#G火#Y#r修炼境界：第#G0#Y层 #c7D7E82初具法力#Y\",\"iType\":6012,]),]),\"iMaxExpt3\":20,\"HeroScore\":334,\"rent_level\":3,\"iMaxExpt1\":20,\"iHp\":2530,\"commu_gid\":0,\"iOrgOffer\":45,\"ori_desc\":349,\"bid\":1,\"iMagDef_All\":524,\"iMaxExpt4\":20,\"iCash\":83228,\"iIcon\":14,\"propKept\":([1:([\"iSpe\":120,\"iRes\":363,\"iStr\":527,\"iCor\":123,\"iMag\":119,]),0:([\"iSpe\":120,\"iRes\":343,\"iStr\":524,\"iCor\":120,\"iMag\":119,]),]),\"shenqi_yellow\":\"0神器灵气：0#r\",\"iDef_All\":761,\"farm_level\":\"1\",\"iMarry2\":0,\"sword_score\":0,\"iBeastSki1\":17,\"iCor_All\":123,\"iSchool\":1,\"iGrade\":109,\"iSaving\":0,\"jiyuan\":0,\"iSchOffer\":4,\"iSmithski\":7244,\"sum_exp\":70,\"iExptSki2\":17,\"energy\":29,\"iStr_All\":527,\"ExpJw\":0,\"iNutsNum\":100,\"total_avatar\":2,\"iSumAmountEx\":0,\"iBeastSki3\":8,\"TA_iAllPoint\":0,\"iDamage_All\":893,\"iExptSki4\":17,\"normal_horse\":1,\"iCGBoxAmount\":0,\"HugeHorse\":([132:([\"cName\":\"落英纷飞\",\"iType\":11103,\"order\":1,\"iSkill\":622,\"nosale\":0,\"iSkillLevel\":1,]),]),\"iExptSki5\":2,\"shenqi\":([\"skill_desc\":\"每次攻击提升自身7点伤害，最多叠加12层，死亡后清零。\",\"power\":630,\"attributes\":({([\"disable\":0,\"id\":1,\"attr\":\"速度 +4.5\",]),([\"disable\":1,\"id\":2,\"attr\":\"气血 +0\",]),([\"disable\":0,\"id\":8,\"attr\":\"伤害 +3\",]),([\"disable\":0,\"id\":16,\"attr\":\"物理暴击 +3\",]),([\"disable\":1,\"id\":4,\"attr\":\"抵抗封印 +0\",]),}),\"skill\":53012,\"active\":1,\"id\":6200,\"components\":({([\"wuxing\":({([\"status\":0,\"wuxingshi_affix\":0,\"id\":1,\"attr\":\"速度 +2.2\",\"affix_disable\":0,\"wuxingshi_level\":1,]),([\"status\":0,\"wuxingshi_affix\":0,\"id\":1,\"attr\":\"速度 +2.2\",\"affix_disable\":0,\"wuxingshi_level\":1,]),([\"status\":0,\"wuxingshi_affix\":0,\"id\":8,\"attr\":\"伤害 +3\",\"affix_disable\":0,\"wuxingshi_level\":1,]),([\"status\":0,\"wuxingshi_affix\":0,\"id\":16,\"attr\":\"物理暴击 +3\",\"affix_disable\":0,\"wuxingshi_level\":1,]),}),\"level\":1,\"unlock\":1,]),([\"wuxing\":({([\"status\":0,\"wuxingshi_affix\":0,\"id\":2,\"attr\":\"气血 +0\",\"affix_disable\":0,\"wuxingshi_level\":0,]),([\"status\":0,\"wuxingshi_affix\":0,\"id\":2,\"attr\":\"气血 +0\",\"affix_disable\":0,\"wuxingshi_level\":0,]),([\"status\":0,\"wuxingshi_affix\":0,\"id\":8,\"attr\":\"伤害 +0\",\"affix_disable\":0,\"wuxingshi_level\":0,]),([\"status\":0,\"wuxingshi_affix\":0,\"id\":4,\"attr\":\"抵抗封印 +0\",\"affix_disable\":0,\"wuxingshi_level\":0,]),}),\"level\":0,\"unlock\":0,]),([\"wuxing\":({([\"status\":0,\"wuxingshi_affix\":0,\"id\":16,\"attr\":\"物理暴击 +0\",\"affix_disable\":0,\"wuxingshi_level\":0,]),([\"status\":0,\"wuxingshi_affix\":0,\"id\":16,\"attr\":\"物理暴击 +0\",\"affix_disable\":0,\"wuxingshi_level\":0,]),([\"status\":0,\"wuxingshi_affix\":0,\"id\":16,\"attr\":\"物理暴击 +0\",\"affix_disable\":0,\"wuxingshi_level\":0,]),([\"status\":0,\"wuxingshi_affix\":0,\"id\":1,\"attr\":\"速度 +0\",\"affix_disable\":0,\"wuxingshi_level\":0,]),}),\"level\":0,\"unlock\":0,]),}),\"skill_level\":1,\"full\":0,]),\"icolor_ex\":0,\"iMp\":493,\"iRes_All\":363,\"iDex_All\":185,\"outdoor_level\":1,\"iMarry\":0,\"rent\":62519,\"xianyu\":50,\"commu_name\":\"\",\"iHp_Max\":2530,\"iLearnCash\":22585188,\"AllEquip\":([17:([\"cDesc\":\"#r等级 100  五行 金#r#r伤害 +352 命中 +600#r耐久度 0  修理失败 3次#r锻炼等级 6  镶嵌宝石 太阳石、 红玛瑙#r#G#G力量 +13 #G体质 +21#Y#Y#r#G开运孔数：4孔/4孔#Y #r#W制造者：109第一赌神强化打造#Y#r#Y熔炼效果：#r#Y#r+2力量#Y  \",\"iType\":1152,]),18:([\"cDesc\":\"#r等级 100  五行 水#r#r伤害 +325 命中 +385#r耐久度 500#Y#r#W制造者：小六っ．强化打造#Y  \",\"iType\":1151,]),12:([\"cDesc\":\"#r等级 100  五行 水#r#r伤害 +396 命中 +553#r耐久度 8  修理失败 3次#r锻炼等级 7  镶嵌宝石 红玛瑙#Y#r#G开运孔数：2孔/4孔#Y #r#W制造者：ら、糸ˉ沫．强化打造#Y  \",\"iType\":1050,]),11:([\"cDesc\":\"#r等级 70  #r防御 +30 气血 +297#r耐久度 17  修理失败 2次#r锻炼等级 6  镶嵌宝石 光芒石、 黑宝石#r#G#G速度 +24#Y#Y#r#c4DBAF4套装效果：附加状态金刚护法#Y#Y#r#G开运孔数：2孔/3孔#G#r符石: 体质 +1#n#G#r符石: 敏捷 +1 防御 +3#n#r#cEE82EE符石组合: 日落西山#r门派条件：无#r部位条件：无#r提升自身4点速度#Y  \",\"iType\":2913,]),10:([\"cDesc\":\"#r等级 80  #r防御 +34 魔法 +80#r耐久度 416#r锻炼等级 5  镶嵌宝石 红玛瑙#r#G#G命中 +125#Y#Y#r#c4DBAF4特技：#c4DBAF4命归术#Y#Y  \",\"iType\":2509,]),9:([\"cDesc\":\"#r等级 80  #r灵力 +138#r耐久度 333#r锻炼等级 6  镶嵌宝石 舍利子#Y#r#c4DBAF4套装效果：附加状态金刚护法#Y#Y#r#G开运孔数：3孔/3孔#G#r符石: 耐力 +1 速度 +1.5#n#G#r符石: 耐力 +1 速度 +1.5#n#G#r符石: 力量 +1#n#r#cEE82EE符石组合: 无心插柳#r门派条件：无#r部位条件：无#r普通物理攻击时会造成溅射效果，对另外两个目标造成所受伤害20%的伤害，仅对NPC使用时有效。#Y  \",\"iType\":2815,]),8:([\"cDesc\":\"#r等级 100  五行 木#r#r防御 +229#r耐久度 364#r锻炼等级 5  镶嵌宝石 月亮石#r#G#G力量 -2#Y #G体质 +19#Y#Y#r#c4DBAF4特效：#c4DBAF4伪装#Y#r#W制造者：蝶恋い花强化打造#Y#r#Y熔炼效果：#r#Y#r+2防御#Y  \",\"iType\":2652,]),7:([\"cDesc\":\"#r等级 70  五行 木#r#r防御 +44 敏捷 +26#r耐久度 474  修理失败 1次#r锻炼等级 4  镶嵌宝石 黑宝石#r#G#G速度 +32#Y#Y#r#c4DBAF4套装效果：附加状态金刚护法#Y#Y#r#W制造者：★蓝蓝βù哭#Y#r#Y   \",\"iType\":2708,]),19:([\"cDesc\":\"#r等级 100  五行 水#r#r伤害 +370 命中 +503#r耐久度 226  修理失败 1次#r锻炼等级 5  镶嵌宝石 红玛瑙#Y#r#c4DBAF4特效：#c4DBAF4绝杀#Y#r#G开运孔数：1孔/4孔#Y #r#W制造者：天使怪盗Dark强化打造#Y  \",\"iType\":1052,]),20:([\"cDesc\":\"#r等级 95  #r命中率 +11%#r耐久度 491#r#G#G敏捷 -11#Y#Y#r#W制造者：菜花五#Y  \",\"iType\":9310,\"iLock\":1,]),]),\"iZhuanZhi\":0,\"iSumAmount\":8,\"idbid_desc\":({1,}),\"AllSummon\":({}),\"iMaxExpt2\":20,\"iMp_Max\":493,\"shenqi_pos\":({0,0,}),\"iAtt_All\":1344,\"iGoodness\":2401,\"iTotalMagDam_all\":524,\"AllRider\":([1:([\"all_skills\":([]),\"iType\":509,\"ExtraGrow\":0,\"iGrade\":93,\"exgrow\":12831,\"mattrib\":\"体质\",]),3:([\"all_skills\":([]),\"iType\":504,\"ExtraGrow\":0,\"iGrade\":0,\"exgrow\":13075,\"mattrib\":\"\",]),2:([\"all_skills\":([601:3,608:1,]),\"iType\":504,\"ExtraGrow\":95,\"iGrade\":125,\"exgrow\":22318,\"mattrib\":\"耐力\",]),]),\"all_skills\":([\"20804\":1,\"208\":92,\"201\":129,\"7\":119,\"204\":130,\"225\":1,\"230\":26,\"209\":29,\"174\":1,\"216\":65,\"202\":13,\"20809\":1,\"218\":100,\"161\":7,\"179\":1,\"20802\":1,\"167\":1,\"199\":1,\"217\":20,\"1\":119,\"52032\":1,\"170\":2,\"4\":80,\"154\":6,\"6\":119,\"207\":12,\"205\":13,\"211\":44,\"173\":1,\"231\":16,\"160\":5,\"52016\":1,\"198\":1,\"212\":41,\"210\":10,\"8\":82,\"203\":13,\"20805\":1,\"206\":77,\"169\":1,\"52031\":1,\"164\":2,\"196\":1,\"197\":2,\"2\":119,\"165\":1,\"5\":119,]),\"iExptSki1\":17,\"iPoint\":0,\"iSewski\":0,\"iUpExp\":361287071,\"changesch\":({}),\"ori_race\":1,\"AchPointTotal\":2390,\"i3FlyLv\":0,\"iBeastSki2\":10,\"iExptSki3\":0,\"iMag_All\":119,\"ExpJwBase\":1000000000,\"addPoint\":7,\"pet\":({}),\"iPcktPage\":0,\"cName\":\"情不尽的伤ゆ\",\"iSkiPoint\":0,\"total_horse\":1,\"iBeastSki4\":4,\"ExAvt\":([1:([\"cName\":\"怀旧剑侠客炫卡\",\"order\":2,\"iType\":20013,]),2:([\"cName\":\"糖果武器\",\"order\":1,\"iType\":14406,]),]),\"more_attr\":([\"attrs\":({([\"lv\":0,\"idx\":3,]),([\"lv\":0,\"idx\":10,]),([\"lv\":0,\"idx\":1,]),([\"lv\":0,\"idx\":2,]),([\"lv\":0,\"idx\":11,]),([\"lv\":0,\"idx\":5,]),([\"lv\":0,\"idx\":7,]),([\"lv\":0,\"idx\":6,]),([\"lv\":0,\"idx\":12,]),([\"lv\":0,\"idx\":9,]),([\"lv\":0,\"idx\":8,]),([\"lv\":0,\"idx\":4,]),([\"lv\":361,\"idx\":13,]),([\"lv\":524,\"idx\":14,]),}),]),\"igoodness_sav\":1039,\"iCGTotalAmount\":30,\"cOrg\":\"幸福家园\",\"iRace\":1,\"iTotalMagDef_all\":524,\"TA_iAllNewPoint\":3,\"iErrantry\":0,\"iCGBodyAmount\":30,\"iPride\":800,])"
# role = parseRole()
#
# # print(ret)
# tasks = [role.RoleInfoParser(desc, {"price":6000.00,"selling_time_v":"2019-01-10 12:24:25","create_time":"2019-01-10 12:24:35"}, '')]
# loop = asyncio.get_event_loop()
# tasks = asyncio.gather(*(tasks))
# loop.run_until_complete(tasks)
