# -*- coding: utf-8 -*-
import re
from roleNameConf import xyqSetting
import json
import time
import asyncio


class parserPet:
    def __init__(self):
        # self.get_ruyidan = self.get_yuanxiao
        self.ResUrl = "https://cbg-xyq.res.netease.com"

        # 搜索条件设置
        self.params = {'skill': 'r_in#all_skill#null', 'type': 'l_in#type#str', 'is_baobao': 'eq#is_baobao#int',
                       'level_min': 'lt#equip_level#int', 'level_max': 'gt#equip_level#int',
                       'skill_num': 'lt#skill_num#int',
                       'attack_aptitude': 'lg#attack_aptitude#int', 'defence_aptitude': 'lt#defence_aptitude#int',
                       'physical_aptitude': 'lg#physical_aptitude#int', 'speed_aptitude_min': 'lg#speed_aptitude#int',
                       'speed_aptitude_max': 'gt#speed_aptitude#int', 'price_min': 'lt#price_fen#int',
                       'price_max': 'gt#price_fen#int',
                       'max_blood': 'lt#blood#int', 'attack': 'lt#attack#int', 'defence': 'lt#defence#int',
                       'speed_min': 'lt#speed#int', 'speed_max': 'gt#speed#int', 'wakan': 'lt#wakan#int',
                       'lingxing': 'lt#lingxing#int', 'growth': 'lt#growth_b#int',
                       'magic_aptitude': 'lt#magic_aptitude#int', 'serverid': 'eq#serverid#int'}

    async def correct_pet_desc(self, pet_desc):
        num_re = '/^[0-9]*$/'
        partern = re.compile(num_re)
        PetAttrNum = 33
        OldAttrNum = 30
        OldestAttrNum = 29
        # print(pet_desc)
        AttrNum = len(re.split(';', pet_desc))
        # print(re.split(';',pet_desc))
        # print(AttrNum)
        if (AttrNum >= PetAttrNum or AttrNum == OldAttrNum or AttrNum == OldestAttrNum):
            return pet_desc
        # sep_num = 0
        # check_num = PetAttrNum - 1 - 1
        new_desc = ""
        for i in range(len(list(pet_desc)) - 1, -1, -1):
            ch = list(pet_desc)[i]
            if (ch != "" and ch != "|" and len(partern.findall(ch)) == 0):
                break
            else:
                new_desc = ch + new_desc
        if (new_desc[0:1] != ""):
            new_desc = "" + new_desc
        return "-" + new_desc

    async def check_undefined(self, item_value):
        if item_value == None:
            return "未知"
        else:
            return item_value

    # def get_yuanxiao(self,input_value=None):
    #     if (input_value == None):
    #         return self.check_undefined(input_value)
    #     agent_time = self.parseDatetime(EquipRequestTime)
    #     cur_time = self.parseDatetime(ServerCurrentTime)
    #
    #     fresh_time = new Date(cur_time.getFullYear(), 0, 1)
    #     if (agent_time > fresh_time):
    #
    #         return input_value
    #     else :
    #         return 0

    # def get_lianshou(self,input_value,EquipRequestTime,ServerCurrentTime) :
    #     if (input_value == None):
    #         return self.check_undefined(input_value)
    #     agent_time = self.parseDatetime(EquipRequestTime)
    #     cur_time = self.parseDatetime(ServerCurrentTime)
    #     #fresh_time = new Date(cur_time.getFullYear(), 8, 1)
    #     #if (cur_time < fresh_time):
    #         #fresh_time.setFullYear(fresh_time.getFullYear() - 1)
    #     #if (agent_time > fresh_time) :
    #         #return input_value
    #     #else :
    #         #return 0
    # def parseDatetime(self,datetime) :
    #     reg = "^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$"
    #     partern = re.compile(reg)
    #     values = partern.findall(datetime)
    #
    #     v = values.slice(1).map(ret(v) {
    #          return int(v, 10)
    #      })
    #     return new Date(v[0], v[1] - 1, v[2], v[3], v[4], v[5])
    async def get_baobao_info(self, is_baobao):
        if (is_baobao == None):
            return "未知"
        if (int(is_baobao)):
            return "是"
        else:
            return "否"

    async def dict_get(self, dict_obj, key, default_value):
        if (dict_obj[key] != None):
            return dict_obj[key]
        else:
            return default_value

    # def testJson(self,json):
    #     dict = {"([":"{", "])":"}", ",])":"}", "({":"[","})":"]", ",})":"]"}
    #     reg = "\(\[|,?\s*\]\)|\(\{|,?\s*\}\)"
    #
    #     return preg_replace_callback(reg,function(matches)use(dict){str = str_replace('/\s+/', '',matches[0])return dict[str]},json)

    def replaceByDict(self, content):
        # dict = {"([": "{", "])": "}", ",])": "}", "({": "[", "})": "]", ",})": "]"}
        reg = "\(\[|,?\s*\]\)|\(\{|,?\s*\}\)"
        pattern = re.compile(reg)
        res = re.sub(pattern, self.preg_replace, content)
        res = re.sub('\'', '\"', res)
        res = self.ext_json_decode(res)
        return json.loads(res)

    def ext_json_decode(self,str):
        p1 = "\w:"
        pattern = re.compile(p1)
        match = pattern.findall(str)
        if len(match) > 0:
            str = re.sub('(\w+):', '"\\1":', str)
        return str


    def preg_replace(self, obj):
        # print(dir(obj))
        dict = {"([": "{", "])": "}", ",])": "}", "({": "[", "})": "]", ",})": "]"}
        if obj.group(0) in dict.keys():
            spa = re.compile("\s+")
            rr = re.sub(spa, '', obj.group(0))
            # print(dict[rr])
            return dict[rr]



    async def get_pet_attrs_info(self, pet_desc , merge_info):
        #print(888888888888888888)
        pet_desc = await self.correct_pet_desc(pet_desc)
        #print(pet_desc)
        attrs = re.split(';', pet_desc)
        #print(attrs)
        # print(attrs[1])
        attrs_info = {
            "pet_name": attrs[0],
            "pet_grade": attrs[2],
            "blood": int(attrs[3]),
            "magic": int(attrs[4]),
            "attack": int(attrs[5]),
            "defence": int(attrs[6]),
            "speed": int(attrs[7]),
            "soma": attrs[9],
            "magic_powner": attrs[10],
            "strength": attrs[11],
            "endurance": attrs[12],
            "smartness": attrs[13],
            "potential": attrs[14],
            "wakan": int(attrs[15]),
            "max_blood": attrs[16],
            "max_magic": attrs[17],
            "lifetime": "永生" if int(attrs[18], 10) >= 65432 else attrs[18],
            "five_aptitude": attrs[19],
            "attack_aptitude": attrs[20],
            "defence_aptitude": attrs[21],
            "physical_aptitude": attrs[22],
            "magic_aptitude": attrs[23],
            "speed_aptitude": attrs[24],
            "avoid_aptitude": attrs[25],
            "growth": int(attrs[26], 10) / 1000,
            "all_skill": attrs[27],
            "sp_skill": attrs[28],
            "is_baobao": await self.get_baobao_info(attrs[29]),
            "used_qianjinlu":await self.check_undefined(attrs[32]),
            "other": attrs[34],
            # "PET_WUXING_INFO": window.PET_WUXING_INFO | | {}
        }

        allSkills = [int(x) for x in re.split('\|', attrs_info['all_skill'])] if attrs_info.get("all_skill",
                                                                                                0) != 0 else []
        #print(allSkills)

        spSkillId = attrs_info.get('sp_skill', '0').strip()
        # print(spSkillId)
        p1 = '(^|\\|){0}($|\\|)'.format(spSkillId)
        parterm = re.compile(p1)
        match = parterm.findall(attrs_info.get("all_skill", 0))
        if (spSkillId != '0' and len(match) == 0):
            allSkills.append(int(spSkillId))
        attrs_info['sp_skill_id'] = spSkillId
        attrs_info['all_skills'] = allSkills
        other_attr = {}

        if (attrs_info["other"]):
            pos = pet_desc.find(attrs_info["other"])
            other = pet_desc[pos:]
            #print(other)
            attrs_info["other"] = self.replaceByDict(other)
            #print(attrs_info["other"])
            # print(self.replaceByDict(pet_desc[pos:]))
            other_attr = attrs_info["other"]
        #print(attrs_info)
        if (other_attr["core_close"] or other_attr["core_close"] == 0):
            attrs_info["core_close"] = "已开启" if other_attr['core_close'] == 0 else "已关闭"
        #print(attrs_info)
        if (other_attr['csavezz']):
            # print(attrs[1])
            xyqSetting().get_pet_ext_zz(attrs_info, {
                "attrs": 'attack_ext,defence_ext,speed_ext,avoid_ext,physical_ext,magic_ext',
                "total_attrs": 'attack_aptitude,defence_aptitude,speed_aptitude,avoid_aptitude,physical_aptitude,magic_aptitude',
                "csavezz": other_attr['csavezz'],
                "carrygradezz": other_attr['carrygradezz'],
                "lastchecksubzz": other_attr['lastchecksubzz'],
                "pet_id": int(attrs[1])
            })
        #print(attrs_info)
        if (attrs_info["other"]):
            attrs_info["equip_list"] =await self.parse_pet_equips(attrs_info["other"])
            attrs_info["neidan"] =await self.parse_neidan(attrs_info["other"])
            attrs_info["color"] = attrs_info["other"].get("iColor", None)
            attrs_info['summon_color'] = attrs_info['other'].get('summon_color', None)

        else:
            attrs_info["neidan"] = []
            jinjie_info = await self.dict_get(other_attr, "jinjie", {})
            attrs_info['jinjie'] = jinjie_info
            attrs_info["lx"] =await self.dict_get(jinjie_info, "lx", 0)
            attrs_info["jinjie_cnt"] =await self.dict_get(jinjie_info, "cnt", "0")
            attrs_info["texing"] =await self.dict_get(jinjie_info, "core", {})
        # if (get_basic) :
        # return attrs_info
        #print(attrs_info)
        # 额外展示属性
        # 技能
        all_skill_name = []
        highlights = []
        senior_num = 0

        for ii in attrs_info.get("all_skills", []):
            skill_name = xyqSetting().PetSkillInfo.get(str(ii), None)
            #print(skill_name)
            if skill_name != None:
                if skill_name.find("高级") > -1:
                    senior_num += 1
                    all_skill_name.append("<font='red'>{}</font>".format(skill_name))
                else:
                    all_skill_name.append(skill_name)
                if skill_name in ['力劈华山', '善恶有报', '须弥真言']:
                    highlights.append(skill_name)
        attrs_info['lingxing'] = attrs_info['other'].get('jinjie', {}).get('lx', 0)
        if attrs_info['other'].get('jinjie', {}).get('lx', 0) == 110:
            highlights.append("110满灵性")
        #print(all_skill_name)
        if len(all_skill_name) > 0:
            skill_desc = "|".join(all_skill_name)
            attrs_info['skill_desc'] = skill_desc
        attrs_info['skill_num'] = len(attrs_info.get("all_skills", []))
        if len(attrs_info.get("all_skills", [])) >= 7:
            highlights.append("技能数量：{0}".format(len(attrs_info.get("all_skills", []))))
        if float(attrs_info['growth']) > 1.264:
            highlights.append(("成长：{0}".format(attrs_info['growth'])))
        if senior_num > 4:
            highlights.append("{0}红".format(senior_num))
        if len(highlights) > 0:
            attrs_info['highlight'] = "|".join(highlights)

        # 资质
        zz = []
        #print(attrs_info)
        attrs_info['attack_aptitude'] = attrs_info['attack_aptitude'] + attrs_info.get('attack_ext',0)
        attrs_info['defence_aptitude'] = attrs_info['defence_aptitude'] + attrs_info.get('defence_ext',0)
        attrs_info['physical_aptitude'] = attrs_info['physical_aptitude'] + attrs_info.get('physical_ext',0)
        attrs_info['magic_aptitude'] = attrs_info['magic_aptitude'] + attrs_info.get('magic_ext',0)
        attrs_info['speed_aptitude'] = attrs_info['speed_aptitude'] + attrs_info.get('speed_ext',0)
        attrs_info['avoid_aptitude'] = attrs_info['avoid_aptitude'] + attrs_info.get('avoid_ext',0)
        zz.append("攻击{0}".format(attrs_info['attack_aptitude']))
        zz.append("防御{0}".format(attrs_info['defence_aptitude']))
        zz.append("体质{0}".format(attrs_info['physical_aptitude']))
        zz.append("魔法{0}".format(attrs_info['magic_aptitude']))
        zz.append("速度{0}".format(attrs_info['speed_aptitude']))
        zz.append("躲避{0}".format(attrs_info['avoid_aptitude']))
        attrs_info['zz'] = "|".join(zz)
        attrs_info['growth_b'] = int(attrs_info['growth'] * 1000)
        attrs_info['price_fen'] = int(merge_info.get("price",0)*100)

        attrs_info = dict(attrs_info, **merge_info)

        # var equip = {
        # 	"eid" : "201812270000113-459-RLOX7PVEYMCM",
        # 	"serversn" : "336",
        # 	"equipid" : "9090013",
        # 	"equip_type" : "102151",
        # 	"status" : "2",
        # 	"kindid" : "66",
        #     "equip_name": "画魂",
        # 	"owner_nickname" : "\u6b63\u5728\u91cd\u65b0\u8f93\u5165",
        # 	"owner_roleid" : "40726112",
        # 	"price" : 998.00,
        # 	"equip_level" : 25,
        # 	"appointed_roleid" : "",
        # 	"expire_time_desc" : "13天23时",
        # 	"create_time" : "2018-12-27 00:13:18",
        # 	"selling_time" : "2019-01-01 17:32:10",
        # 	"request_time": "2018-12-27 00:13:18",
        # 	"fair_show_end_time_left" : "少于1分钟",
        # 	"fair_show_end_time" : "2018-12-31 00:28:18",
        # 	"is_selling":1,
        # 	"is_pass_fair_show":1,
        # 	"game_ordersn" : "336_1545840798_345097410",
        # 	"is_seller_online" : -1,
        # 	"storage_type" : 2,
        # 	"equip_count" : 1,
        # 	"server_id" : 459,
        # 	"highlights" : [],
        # 	"can_bargin" : 1,
        # 	"valid_bargain_resp" : safe_json_decode('null'),
        # 	"equip_detail_type": "<!--equip_detail_type-->",
        # 	"if_seller_have_more_equips" : "1"
        # };

        # attrs_info['used_yuanxiao'] = get_yuanxiao(attrs[30])
        # attrs_info['used_ruyidan'] = get_ruyidan(attrs[31])
        # attrs_info['used_lianshou'] = get_lianshou(attrs[33])
        #print(attrs_info)
        return attrs_info

    async def get_type(self, equip_type):
        if int(equip_type) in xyqSetting().equip_info.keys():
            return 'equip'
        if int(equip_type) in xyqSetting().pet_info.keys():
            return 'pet'
        return 'role'

    async def get_pet_shipin_icon(self, typeid):
        return self.ResUrl + "/images/pet_shipin/small/" + typeid + ".png"

    async def parse_pet_equips(self, pet):
        equip_list = []
        max_equip_num = 3
        img_dir = self.ResUrl + "/images/equip/small/"
        for i in range(max_equip_num):
            item = pet.get("summon_equip{0}".format(i + 1), None)
            if (item):
                equip_name_info = xyqSetting().get_equip_info(item["iType"])
                equip_list.append({
                    "name": equip_name_info["name"],
                    "icon": "{0}{1}.git".format(img_dir,item["iType"]),
                    "type": item["iType"],
                    "desc": item["cDesc"],
                    "static_desc": equip_name_info["desc"].replace("#R", "<br />")
                })
            else:
                equip_list.append(None)

        if (pet['summon_equip4_type']):
            equip_list.append({
                "name": xyqSetting().pet_shipin_info.get(str(pet.get('summon_equip4_type','')),''),
                "icon": await self.get_pet_shipin_icon(str(pet.get('summon_equip4_typ',''))),
                "type": pet['summon_equip4_type'],
                "desc": pet['summon_equip4_desc'],
                "static_desc": ''
            })
            return equip_list

    async def safe_attr(self, attr):
        if (attr == None or attr == None):
            return ""
        else:
            return attr

    async def parse_neidan(self, pet):
        neidan_list = []
        neidan_data = pet['summon_core']
        if (neidan_data != None):
            for p in neidan_data:
                neidan_info = neidan_data[p]
                neidan_list.append({
                    "name": await self.safe_attr(xyqSetting().PetNeidanInfo.get(p,None)),
                    #"icon": self.ResUrl + "/images/neidan/" + p + ".jpg",
                    "icon": "{0}/images/neidan/{1}.jpg".format(self.ResUrl,p),
                    "level": neidan_info[0]
                })
        return neidan_list

    async def fill_format(self, num):
        if (num / 1000 >= 1):
            return num
        if (num / 100 >= 1):
            return "0" + num
        if (num / 10 >= 1):
            return "00" + num
        return "000" + num


# pet = parserPet()
# content = '画魂;102151;27;532;244;193;156;46;94;57;49;39;40;50;135;96;532;244;6770;1;1517;1427;3655;1088;921;1102;1271;328|412|429|325|303|318|322|628|334|317;0;1;0;0;0;0;(["lastchecksubzz":2018,"strengthen":0,"MP_MAX":3050,"carrygradezz":0,"weaken":0,"HP_MAX":5500,"sjg":0,"iRealColor":0,"DEF_MAX":1550,"growthMax":1277,"MS_MAX":1800,"jinjie":(["cnt":0,"core":([]),"lx":0,]),"summon_equip4_desc":"","jj_extra_add":0,"iJjFeedCd":0,"SPD_MAX":1550,"ATK_MAX":1550,"tmp_lingxing":0,"summon_core":([]),"csavezz":"1517|1427|921|1102|3655|1088","left_qlxl":7,"core_close":0,"summon_color":0,"summon_equip4_type":0,])'
# #info = pet.get_pet_attrs_info(content, 1, {})
# #print(info)
# tasks = [pet.get_pet_attrs_info(content, {})]
# loop = asyncio.get_event_loop()
# tasks = asyncio.gather(*(tasks))
# loop.run_until_complete(tasks)
