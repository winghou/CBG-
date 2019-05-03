# -*- coding: utf-8 -*-
from lxml import etree
import settings
from roleNameConf import xyqSetting
import re


class parser:
    def __init__(self):
        self.petequip_params = {
            "level_min":"lt#equip_level#int", #最低等级
            "level_max":"gt#equip_level#int", #最高等级
            "addon_sum_min":"lt#addon_sum#int", #属性总和
            "equip_pos" :"r_in#equip_pos#int", #装备类型
            "addon_lingli":"lt#addon_lingli#int", #灵力属性
            "addon_minjie_reduce":"gt#addon_minjie_reduce#int", #敏捷减少
            "addon_liliang":"lt#addon_liliang#int", #力量属性
            "addon_fali":"lt#addon_fali#int", #法力属性
            "addon_nali":"lt#addon_nali#int", #耐力属性
            "addon_minjie":"lt#addon_minjie#int", #敏捷属性
            "addon_tizhi":"lt#addon_tizhi#int", #体质属性
            "speed":"lt#speed#int", #速度属性
            "fangyu":"lt#fangyu#lt", #防御属性
            "mofa":"lt#mofa#int", #魔法属性
            "shanghai":"lt#shanghai#int", #伤害属性
            "hit_ratio":"lt#hit_ratio#float", #命中率
            "hp":"lt#hp#int", #气血
            "xiang_qian_level":"lt#xiang_qian_level#int", #镶嵌等级
            "price_min":"lt#price_fen#int", #最低价
            "price_max":"gt#price_fen#int", #最高价
            "addon_status":"eq#addon_status#str", #附带技能
            "kindid": "eq#kindid#int",
            "serverid": "eq#serverid#int",
        }
        self.equip_params = {
            "kindid":"eq#kindid#int",
            "level_min":"lt#equip_level#int",
            "level_max":"gt#equip_level#int",
            "for_role_race":"in_in#for_role_race#none",
            "for_role_sex":"r_in#sex#none",
            "special_effect#and":"r_in#special_effect#none",
            "special_effect#or": "in_in#special_effect#none",
            "special_skill":"l_in#special_skill#none",
            #"suit_effect":"eq#suit_effect#int",
            "init_damage":"lt#init_damege#int",
            "init_damage_raw":"lt#init_damage_raw#int",
            "init_defence":"lt#init_defence#int",
            "init_hp":"lt#init_hp#int",
            "init_dex":"lt#init_dex#int",
            "init_wakan":"lt#init_wakan#int",
            "all_damage":"lt#all_damage#int",
            "damage":"lt#damage#int",
            "sum_attr_type":"l_in#attr_types#none",
            "sum_attr_value":"eq#sum_attr#int",
            "gem_value":"eq#gem_value#int",
            "gem_level":"lt#gem_level#int",
            "hole_num":"eq#hole_num#int",
            "price_min":"lt#price_fen#int",
            "price_max":"gt#price_max#int",
            "serverid":"eq#serverid#int",
            "transform_skill":"eq#transform_skill#int",
            "added_status":"eq#added_status#int",
            "append_skill":"eq#append_skill#int",
            "transform_charm":"eq#transform_charm#int",
        }

        self.lingshi_params = {
            "equip_level_min":"lt#equip_level#int",
            "equip_level_max":"gt#equip_level#int",
            "added_attr_num":"lt#added_attr_num#int",
            "added_attr_repeat_num":"lt#added_attr_repeat_num#int",
            "kindid":"eq#kindid#int",
            "added_attrs":"r_in#added_attrs#none",
            "special_effect":"eq#special_effect#int",
            "price_min":"lt#price_fen#int",
            "price_max":"gt#price_fen#int",
            "jinglian_level":"lt#jinglian_level#int",
            "serverid":"eq#serverid#int",
        }
        self.pet_equip = {1: "铠甲", 2: "项圈", 3: "护腕"}
        self.StyleStart = "#"
        self.EquipDescRed = "#R"
        self.EquipDescGreen = "#G"
        self.EquipDescBlue = "#B"
        self.EquipDescBlack = "#K"

        self.equip_highlight = ['浪涌', '满天花雨', '蜃气妖', '炎魔神','永不磨损','晶清诀','罗汉金钟','无级别限制','简易','破血狂攻','狂豹（人型）','猫灵（人型）','混沌兽','长眉灵猴','修罗傀儡鬼','灵鹤']
        self.pet_highlight = ['须弥真言','力劈华山','善恶有报','法术防御','死亡禁锢']
        self.EquipDescYellow = "#Y"
        self.EquipDescWhite = "#W"
        self.EquipDescBlink = "#b"
        self.EquipDescUnderline = "#u"
        self.EquipDescNormal = "#n"
        self.XyqCssSetting = {
            "#R": "equip_desc_red",
            "#G": "equip_desc_green",
            "#B": "equip_desc_blue",
            "#K": "equip_desc_black",
            "#Y": "equip_desc_yellow",
            "#W": "equip_desc_white",
            "#b": "equip_desc_blink",
            "#u": "equip_desc_underline",
            "#n": "equip_desc_white"
        }
        self.CommonStyleSet = [self.EquipDescRed, self.EquipDescGreen, self.EquipDescBlue, self.EquipDescBlack,
                               self.EquipDescYellow, self.EquipDescWhite]
        self.SepicalStyleSet = [self.EquipDescBlink, self.EquipDescUnderline]
        self.ColorLen = 6
        self.ClassStyle = 0
        self.ColorStyle = 1

    async def get_label_head_with_class(self, class_name):
        return "<span class='" + class_name + "'>"

    async def get_label_head_with_color(self, color_value):
        return "<span style='color:#" + color_value + "'>"

    async def get_label_tail(self):
        return "</span>"

    async def has_element(self, el_array, el):
        for i in el_array:
            if i == el:
                return True
        return False

    # 文本转化成html
    async def parse_style_info(self, equip_desc, DefaultCss=None):
        DefaultCss = DefaultCss if DefaultCss else "#Y"
        result = await self.get_label_head_with_class(self.XyqCssSetting[DefaultCss])
        last_common_style = {"kind": self.ClassStyle, "value": DefaultCss}
        spcial_class_stack = []
        i = 0
        length = len(equip_desc)
        num = 0
        temp = 53
        while i < length:
            num = num + 1

            if i == 53:
                temp = i
            if (equip_desc[i: i + 1] != self.StyleStart):
                result += equip_desc[i: i + 1]
                i = i + 1
                continue

            if (i == length - 1):
                i = i + 1
                break

            if (equip_desc[i + 1: i + 1 + 1] == "#"):
                result += "#"
                i = i + 1 + 1
                continue

            if (equip_desc[i + 1: i + 1 + 1] == "r"):
                result += "<br>"
                i = i + 1 + 1
                continue

            if (equip_desc[i + 1: i + 1 + 1] == "c"):
                result += await self.get_label_tail()
                color_start = i + 1 + 1
                color_value = equip_desc[color_start: (color_start + self.ColorLen)]
                result += await self.get_label_head_with_color(color_value)
                i = i + 1 + self.ColorLen + 1
                last_common_style["kind"] = self.ColorStyle
                last_common_style["value"] = color_value
                continue

            class_label = equip_desc[i: i + 2]
            if (await self.has_element(self.CommonStyleSet, class_label)):
                result += await self.get_label_tail()
                result += await self.get_label_head_with_class(self.XyqCssSetting[class_label])
                i = i + 1 + 1
                last_common_style["kind"] = self.ClassStyle
                last_common_style["value"] = class_label
                continue
            elif (await self.has_element(self.SepicalStyleSet, class_label)):

                if (await self.has_element(spcial_class_stack, class_label)):
                    i = i + 1 + 1
                    continue
                result += await self.get_label_tail()
                result += await self.get_label_head_with_class(self.XyqCssSetting[class_label])
                if (last_common_style["kind"] == self.ClassStyle):
                    result += await self.get_label_head_with_class(self.XyqCssSetting[last_common_style["value"]])
                else:
                    result += await self.get_label_head_with_color(last_common_style["value"])
                spcial_class_stack.extend([class_label])
                i = i + 1 + 1
                continue
            elif (class_label == self.EquipDescNormal):
                result += await self.get_label_tail()
                for j in range(1, len(spcial_class_stack)):
                    result += await self.get_label_tail()
                result += await self.get_label_head_with_class(self.XyqCssSetting[DefaultCss])
                spcial_class_stack = []
                i = i + 1 + 1
            else:
                i = i + 1
                continue

        result += await self.get_label_tail()
        for j in range(1, len(spcial_class_stack)):
            result += await self.get_label_tail()
        return result

    #人物装备
    async def htmlToEquip(self, content , merge_param):
        # desc = "#r等级 70  五行 水#r#r防御 +190#r耐久度 449#r锻炼等级 7  镶嵌宝石 月亮石#r#G#G力量 +16#Y #G耐力 -4#Y#r#c4DBAF4特技：#c4DBAF4水清诀#Y#Y#r#c4DBAF4特效：#c4DBAF4简易#Y#r#c4DBAF4套装效果：追加法术满天花雨#Y#Y#r#G开运孔数：3孔/3孔#G#r符石: 伤害 +1.5#n#G#r符石: 伤害 +1.5#n#G#r符石: 力量 +1#n#G#r星位：防御 +5#n#r#cEE82EE符石组合: 无心插柳#r门派条件：无#r部位条件：无#r普通物理攻击时会造成溅射效果，对另外两个目标造成所受伤害20%的伤害，仅对NPC使用时有效。#Y#r#W制造者：＂碧魂．#Y#r#Y熔炼效果：#r#Y#r+3耐力 +9防御 #r#Y "
        # html_str = my.parse_style_info(desc)
        # print(html_str)
        html = await self.parse_style_info(content)
        #print(html)
        html = etree.HTML(html)


        # equip = {
        #     "eid": "201804272000113-459-LDQMWDBNWKXG",
        #     "serversn": "336",
        #     "equipid": "7542474",
        #     "equip_type": "2912",
        #     "status": "2",
        #     "kindid": "20",
        #     "equip_name": "兽王腰带",
        #     "owner_nickname": "qq\u5927\u96c1\u58546",
        #     "owner_roleid": "52385592",
        #     "price": 52.00,
        #     "equip_level": 70,
        #     "appointed_roleid": "",
        #     "expire_time_desc": "13天23时",
        #     "create_time": "2018-04-27 20:20:52",
        #     "selling_time": "2019-01-02 12:50:20",
        #     "request_time": "2018-04-27 20:20:49",
        #     "fair_show_end_time_left": "少于1分钟",
        #     "fair_show_end_time": "2018-05-01 20:35:52",
        #     "is_selling": 1,
        #     "is_pass_fair_show": 1,
        #     "game_ordersn": "336_1524831649_343547238",
        #     "is_seller_online": -1,
        #     "storage_type": 1,
        #     "equip_count": 1,
        #     "server_id": 459,
        #     "highlights": [["\u6124\u6012", 90]],
        #     "can_bargin": 0,
        #     "valid_bargain_resp": safe_json_decode('null'),
        #     "equip_detail_type": "<!--equip_detail_type-->",
        #     "if_seller_have_more_equips": "0"
        # };


        it = html.xpath("//span[@class='equip_desc_yellow']/text()")
        # yellow ['等级 70  五行 水', '防御 +190', '耐久度 449', '锻炼等级 7  镶嵌宝石 月亮石', ' ', '熔炼效果：', '+3耐力 +9防御 ', ' ']
        #print(it)
        equip = {}
        equip['gem_value'] = None  # 宝石种类
        equip['gem_level'] = 0  # 宝石等级
        equip['defense'] = 0  # 防御
        equip['damage'] = 0  # 命中
        equip['damage_raw'] = 0  # 伤害
        equip['level'] = 60  # 等级
        equip['gem_value'] = []  # 宝石种类
        equip['wakan'] = 0  # 灵力
        equip['init_defense'] = 0  # 初始防御
        equip['power'] = 0  # 力量
        equip['magic'] = 0  # 魔力
        equip['endurance'] = 0  # 耐力
        equip['dex'] = 0  # 敏捷
        equip['physique'] = 0  # 体质
        equip['init_damage_raw'] = 0  # 初伤
        equip['init_damage'] = 0  # 初始命中
        equip['init_all_damage'] = 0  # 初总伤
        equip['all_damage'] = -0  # 总伤
        #attr = {}

        for i in it:
            if i.find('：') == -1 and i.find(':') == -1:
                if i.find('等级') == 0:
                    equip['level'] = int(i[3:7])
                if i.find('锻炼等级') > -1:
                    equip['gem_level'] = int(i[i.index("锻炼等级") + 4:i.index("锻炼等级") + 4 + 3])
                if i.find('镶嵌宝石') > -1:
                    Gems = {'红玛瑙': 1, '太阳石': 2, '舍利子': 3, '光芒石': 4, '月亮石': 5, '黑宝石': 6, '神秘石': 7, '翡翠石': 12}
                    value = i[i.index("镶嵌宝石") + 4:len(i)].strip()
                    if value.find('、') > -1 :
                        # 多种宝石
                        lenth = len(value)
                        value_split = []
                        if lenth < 9:
                            value_split.append(value[0:3].strip())
                            value_split.append(value[4:8].strip())
                            #print(value_split)
                        else:
                            value_split.append(value[0:3].strip())
                            value_split.append(value[4:8].strip())
                            value_split.append(value[9:13].strip())
                        for i in value_split:
                            gem_value = Gems.get(i, None)
                            if gem_value != None:
                                equip['gem_value'].append(gem_value)
                    else:
                        gem_value = Gems.get(value, None)
                        if gem_value != None:
                            equip['gem_value'] = [gem_value]
                    # print(equip.gem_value)
                if i.find('防御') == 0:
                    equip['defense'] = i[3:7].strip()

                if i.find('灵力') == 0:
                    equip['wakan'] = i[i.index("灵力") + 2:i.index("灵力") + 2 + 4]
                    # print(wakan)
                if i.find('命中') > -1 and i[(i.index('命中') + 2 + 1):i.index('命中') + 2 + 6].find("%") == -1:
                    equip['damage'] = i[(i.index('命中') + 2 + 1):i.index('命中') + 2 + 6]
                if i.find('伤害') > -1:
                    equip['damage_raw'] = i[(i.index('伤害') + 2 + 1):i.index('伤害') + 2 + 6]

                if equip['gem_value'] != None:
                    # 初防计算（去掉月亮石效果）
                    if 5 in equip['gem_value']:
                        equip['init_defense'] = int(equip['defense']) - equip['gem_level'] * 12
                    # 初灵力计算（去掉舍利子效果）
                    if 3 in equip['gem_value']:
                        equip['init_wakan'] = int(equip['wakan']) - equip['gem_level'] * 6
                    # 初伤考计算
                    if equip['damage_raw'] != None:
                        if 2 in equip['gem_value']:
                            equip['init_damage_raw'] = int(equip['damage_raw']) - equip['gem_level'] * 8
                        else:
                            equip['init_damage_raw'] = int(equip['damage_raw'])
                    # 初始命中计算
                    if equip['damage']:
                        if 1 in equip['gem_value']:
                            equip['init_damage'] = int(equip['damage']) - int(equip['gem_level']) * 25
                        else:
                            equip['init_damage'] = int(equip['damage'])
                    # 初总伤
                    if equip['init_damage_raw'] and equip['init_damage']:
                        equip['init_all_damage'] = int(equip['init_damage_raw']) + int(int(equip['init_damage']) / 3)
                    # 总伤
                    if equip['damage_raw'] and equip['damage']:
                        equip['all_damage'] = int(equip['damage_raw']) + int(int(equip['damage']) / 3)

        # 附加属性，符石效果，星位
        item = html.xpath("//span[@class='equip_desc_green']/text()")

        for i in item:
            if i.find('：') > 0 or i.find(':') > 0:
                # 开运孔数，星位，符石
                if i.find('开运孔数') > -1:
                    # print(i[5:6])
                    equip['hole_num'] = int(i[5:6])
            else:
                sum_attr_value = 0
                if i.find('力量') > -1:
                    equip['power'] = int(i[3:6])
                    sum_attr_value += equip['power']
                if i.find("耐力") > -1:
                    equip['endurance'] = int(i[3:6])
                    sum_attr_value += equip['endurance']
                if i.find("敏捷") > -1:
                    equip['dex'] = int(i[3:6])
                    sum_attr_value += equip['dex']
                if i.find("魔力") > -1:
                    equip['magic'] = int(i[3:6])
                    sum_attr_value += equip['magic']
                if i.find("体质") > -1:
                    equip['physique'] = int(i[3:6])
                    sum_attr_value += equip['physique']

        #print(item)
        # 特技特效处理
        ite = html.xpath("//span[@style='color:#4DBAF4']/text()")
        if len(ite) > 0:
            # 翻转字典(特技)
            SpecialSkills = {k: v for v, k in settings.SpecialSkills.items()}
            equip['special_skill'] = None
            # 翻转字典（特效）
            SpecialEffects = {k: v for v, k in settings.SpecialEffects.items()}
            equip['special_effect'] = []
            # 附加状态
            SuitAddedStatus = settings.SuitAddedStatus
            equip['added_status'] = None
            # 追加法术
            SuitAppendSkills = settings.SuitAppendSkills
            equip['append_skill'] = None
            # 变身术之
            SuitTransformSkills = settings.SuitTransformSkills
            equip['transform_skill'] = None
            # 变化咒之
            SuitTransformCharms = settings.SuitTransformCharms
            equip['transform_charm'] = None
            equip['highlights'] = []
            for i in ite:
                if i.find("特技") > -1:
                    continue
                if i.find("特效") > -1:
                    continue
                skill = SpecialSkills.get(i.strip(), 0)
                if skill != 0:
                    equip['special_skill'] = int(skill)
                    equip['special_skill_name'] = i.strip()
                    if equip['special_skill_name'] in self.equip_highlight:
                        equip['highlights'].append(equip['special_skill_name'])
                    continue
                effect = int(SpecialEffects.get(i.strip(), 0))
                if effect != 0:
                    equip['special_effect'].append(effect)
                    equip['special_effect_name'] = i.strip()
                    if equip['special_effect_name'] in self.equip_highlight:
                        equip['highlights'].append(equip['special_effect_name'])
                    continue
                if i.find('附加状态') > -1:
                    equip['added_status'] = int(SuitAddedStatus.get(i[i.index('附加状态') + 4:len(i)], None))
                    equip['added_status_name'] = i[i.index('附加状态') + 4:len(i)]
                    continue
                if i.find('追加法术') > -1:
                    equip['append_skill'] = int(SuitAppendSkills.get(i[i.index('追加法术') + 4:len(i)], None))
                    equip['append_skill_name'] = i[i.index('追加法术') + 4:len(i)]
                    if equip['append_skill_name'] in self.pet_highlight:
                        equip['highlights'].append(equip['append_skill_name'])
                    continue
                if i.find('变化咒之') > -1:
                    equip['transform_charm'] = int(SuitTransformCharms.get(i[i.index('变化咒之') + 4:len(i)], None))
                    equip['transform_charm_name'] = i[i.index('变化咒之') + 4:len(i)]
                    continue
                if i.find('变身术之') > -1:
                    equip['transform_skill'] = int(SuitTransformSkills.get(i[i.index('变身术之') + 4:len(i)], None))
                    equip['transform_skill_name'] = i[i.index('变身术之') + 4:len(i)].strip()
                    if equip['transform_skill_name'] in self.pet_highlight:
                        equip['highlights'].append(equip['transform_skill_name'])
                    continue
            if len(equip['highlights'])>0:
                equip['highlight'] = '|'.join(equip['highlights'])
        equip = dict(equip,**merge_param)
        equip_type = equip.get("equip_type",1701)
        desc_info = xyqSetting().equip_info.get(int(equip_type),{})
        desc = desc_info.get("desc",'')
        if desc.find("【装备角色】") >-1 :
            #print(desc)
            role_desc = desc[desc.find("【装备角色】")+6:].strip()
            #print(role_desc)
            role_list = {k:v for v,k in settings.RoleKindNameInfo.items()}
            if role_desc=='女':
                equip['sex'] = 2
            elif role_desc=='男':
                equip['sex'] = 1
            else:
                role_split = re.split('，|,',role_desc)
                #print(role_split)
                roles = []
                #equip['for_role_race'] = [int(x) for x in role_split]
                for h in role_split:
                    roleid = role_list.get(h,None)
                    if roleid != None:
                        roles.append(roleid)
                    if roleid in settings.male and roleid not in settings.female:
                        equip['sex'] = [1]
                    elif roleid in settings.female and roleid not in settings.male:
                        equip['sex'] = [2]
                    elif roleid in settings.male and roleid in settings.female:
                        #男女通用
                        equip['sex'] = [1,2]
                if len(roles) > 0:
                    equip['for_role_race'] = roles

        equip['price_fen'] = int(equip.get("price",0)*100)
        #print(equip)
        return equip



    #召唤兽装备
    async def htmlToPetEquip(self, content, merge_param):
        #print(9999999999)
        html = await self.parse_style_info(content)
        html = etree.HTML(html)
        #print(html)
        it = html.xpath("//span[@class='equip_desc_yellow']/text()")
        petequip = {}
        num = 0
        petequip['highlights'] = []
        for i in it:
            num += 1
            if i.find("等级") == 0:
                petequip['level'] = i[-5:].strip()
                continue
            if i.find("伤害") >= 0 and num <=2:
                petequip['addon_damage'] = i[i.index('伤害')+3:i.index('伤害')+3+4].strip()
                petequip['shanghai'] = i[i.index('伤害')+3:i.index('伤害')+3+4].strip()
            if i.find("气血") >= 0 and num <=2:
                petequip['hp'] = i[i.index('气血')+3:i.index('气血')+3+4].strip()
            if i.find("魔法") >= 0 and num <=2:
                petequip['mofa'] = i[i.index('魔法')+3:i.index('魔法')+3+3].strip()
            if i.find("防御") >=0 and num <= 2:
                petequip['fangyu'] = i[i.index('防御')+3:i.index('防御')+3+4].strip()
            if i.find("镶嵌等级") >= 0:
                petequip['xiang_qian_level'] = i[i.index('镶嵌等级：')+5:i.index('镶嵌等级：')+5 + 2].strip()
                continue
            if i.find("速度") >= 0 and num <=2:
                petequip['speed'] = i[i.index('速度')+3:i.index('速度')+3+3].strip()
            if i.find("命中率") >= 0 and num <=2:
                petequip['hit_ratio'] = i[i.index('命中率')+4:i.index('命中率')+4+3].strip()

        #print(it)
        #print(petequip)

        ite = html.xpath("//span[@style='color:#4DBAF4']/text()")
        if len(ite) > 0:
            petequip['addon_status'] = ite[1]
            if ite[1] in ['力劈华山','死亡禁锢'] :
                petequip['highlights'].append("特殊套装效果：{0}".format(ite[1]))
        #print(ite)

        item = html.xpath("//span[@class='equip_desc_green']/text()")
        #print(item)
        add_sum = 0
        if len(item) > 0:
            for ii in item:
                if ii.find("力量") > -1:
                    petequip['addon_liliang'] = int(ii[-3:])
                    add_sum += int(ii[-3:])
                    continue
                if ii.find("体质") > -1:
                    petequip['addon_tizhi'] = int(ii[-3:])
                    add_sum += int(ii[-3:])
                    continue
                if ii.find("灵力") > -1:
                    petequip['addon_lingli'] = int(ii[-3:])
                    add_sum += int(ii[-3:])
                    continue
                if ii.find("法力") > -1:
                    petequip['addon_fali'] = int(ii[-3:])
                    add_sum += int(ii[-3:])
                    continue
                if ii.find("耐力") > -1:
                    petequip['addon_naili'] = int(ii[-3:])
                    add_sum += int(ii[-3:])
                    continue
                if ii.find("敏捷") > -1:
                    petequip['addon_minjie'] = int(ii[-3:])
                    if petequip['addon_minjie'] < 0:
                        petequip['addon_minjie_reduce'] = - petequip['addon_minjie']
                    else:
                        add_sum += int(ii[-3:])
                    continue
        petequip['addon_sum'] = add_sum
        if add_sum > 20:
            petequip['highlights'].append("附加属性总和{0}".format(add_sum))
        if len(petequip['highlights']) > 0:
            petequip['highlight'] = "|".join(petequip['highlights'])
        #print(petequip)
        petequip = dict(petequip,**merge_param)
        if petequip.get("equip_name",'').find("环") > 0 or petequip.get("equip_name",'').find("圈") > 0:
            petequip['equip_pos'] = 2
        if petequip.get("equip_name",'').find("腕") > 0:
            petequip['equip_pos'] = 3
        if petequip.get("equip_name",'').find("甲") > 0:
            petequip['equip_pos'] = 1

        petequip['price_fen'] = int(petequip.get("price",0) * 100)
        return  petequip

    #灵饰
    async def htmlToLingShi(self,content,merge_params={}):
        # var equip = {
            # 	"eid" : "201901021000113-459-I5BJQ3GFVLHM",
            # 	"serversn" : "336",
            # 	"equipid" : "9133437",
            # 	"equip_type" : "9211",
            # 	"status" : "2",
            # 	"kindid" : "29",
            #   "equip_name": "玳瑁环",
            # 	"owner_nickname" : "\u98ce***\u4e36",
            # 	"owner_roleid" : "46381***",
            # 	"price" : 25.00,
            # 	"equip_level" : 105,
            # 	"appointed_roleid" : "",
            # 	"expire_time_desc" : "17天22时",
            # 	"create_time" : "2019-01-02 10:24:36",
            # 	"selling_time" : "2019-01-02 10:24:36",
            # 	"request_time": "2019-01-02 10:24:35",
            # 	"fair_show_end_time_left" : "3天22时",
            # 	"fair_show_end_time" : "2019-01-06 10:39:36",
            # 	"is_selling":1,
            # 	"is_pass_fair_show":0,
            # 	"game_ordersn" : "336_1546395875_345140978",
            # 	"is_seller_online" : 0,
            # 	"storage_type" : 1,
            # 	"equip_count" : 1,
            # 	"server_id" : 459,
            # 	"highlights" : [["\u5077\u88ad", 60]],
            # 	"can_bargin" : 0,
            # 	"valid_bargain_resp" : safe_json_decode('null'),
            # 	"equip_detail_type": "<!--equip_detail_type-->",
            # 	"if_seller_have_more_equips" : "0"
            # };
        #
        html = await self.parse_style_info(content)
        #print(html)
        html = etree.HTML(html)
        it = html.xpath("//span[@class='equip_desc_yellow']/text()")
        #print(it)
        lingshi = {}
        if len(it)>0:
            for v in it:
                v = v.strip()
                #print(v)
                #print(v.find("等级"))
                if v.find("等级") == 0:
                    lingshi['level'] = v[-3:].strip()
                    lingshi['等级'] = v[-3:].strip()
                    continue
                if v.find("防御") == 0:
                    lingshi['defense'] = v[-3:].strip()
                    lingshi['防御'] = v[-3:].strip()
                    continue
                if v.find("精练等级") == 0:
                    lingshi['jinglian_level'] = v[-2:].strip()
                    lingshi['精练等级'] = v[-2:].strip()
                    continue
                if v.find("速度") == 0:
                    lingshi['speed'] = v[-2:].strip()
                    lingshi['速度'] = v[-2:].strip()
                    continue
                if v.find("伤害") == 0:
                    lingshi['damage'] = v[-2:].strip()
                    lingshi['伤害'] = v[-2:].strip()
                    continue
                if v.find("法术伤害") == 0:
                    lingshi['magic_damage'] = v[-2:].strip()
                    lingshi['法术伤害'] = v[-2:].strip()
                    continue
                if v.find("法术防御") == 0:
                    lingshi['magic_defense'] = v[-2:].strip()
                    lingshi['法术防御'] = v[-2:].strip()
                    continue
                if v.find("封印命中等级") == 0:
                    lingshi['fengyin'] = v[-2:].strip()
                    lingshi['封印命中等级'] = v[-2:].strip()
                    continue
                if v.find("抵抗封印命中等级") == 0:
                    lingshi['anti_fengyin'] = v[-2:].strip()
                    lingshi['抵抗封印命中等级'] = v[-2:].strip()
                    continue
        ite = html.xpath("//span[@style='color:#4DBAF4']/text()")
        if len(ite)>0:
            lingshi['special_effect'] = 1

        #print(ite)

        item = html.xpath("//span[@class='equip_desc_green']/text()")
        #print(item)
        #翻转字典（灵饰附加属性）
        AddedAttr1 = {k: v for v,k in settings.AddedAttr1.items()}
        AddedAttr2 = {k: v for v,k in settings.AddedAttr2.items()}
        AddedAttr = dict(AddedAttr1,**AddedAttr2)
        #print(AddedAttr)
        lingshi['added_attr_num'] = len(item)
        lingshi['added_attrs'] = []
        if len(item) > 0:
            for vv in item:
                indexA = vv.find("+")
                attrName = vv[0:indexA].strip()
                #print(attrName)
                val = AddedAttr.get(attrName,0)
                lingshi['added_attrs'].append(int(val))
                if val!=0:
                    num = lingshi.get(attrName,0)
                    if num == 0:
                        lingshi[attrName] = 1
                    else :
                        lingshi[attrName] = int(lingshi[attrName])
                        lingshi[attrName] += 1
                if val!=0:
                    num = lingshi.get(val,0)
                    if num == 0:
                        lingshi[val] = 1
                    else :
                        lingshi[val] += 1
        lingshi['highlight'] = ''
        lingshi['added_attr_repeat_num'] = 1 #默认为1
        for k,v in AddedAttr.items():
            if lingshi.get(v,0) >= 2:
                lingshi['highlight'] = "{0} 条 {1}".format(lingshi.get(v,0),k)
                lingshi['added_attr_repeat_num'] = lingshi.get(v,0)

        lingshi = dict(lingshi,**merge_params)
        lingshi['price_fen'] = int(lingshi.get("price",0)*100)
        #print(lingshi)
        return lingshi


#my = parser()
# 特效，特技，套装
#desc = "#r等级 70  五行 水#r#r防御 +190#r耐久度 449#r锻炼等级 7  镶嵌宝石 月亮石#r#G#G力量 +16#Y #G耐力 -4#Y#r#c4DBAF4特技：#c4DBAF4水清诀#Y#Y#r#c4DBAF4特效：#c4DBAF4简易#Y#r#c4DBAF4套装效果：追加法术满天花雨#Y#Y#r#G开运孔数：3孔/3孔#G#r符石: 伤害 +1.5#n#G#r符石: 伤害 +1.5#n#G#r符石: 力量 +1#n#G#r星位：防御 +5#n#r#cEE82EE符石组合: 无心插柳#r门派条件：无#r部位条件：无#r普通物理攻击时会造成溅射效果，对另外两个目标造成所受伤害20%的伤害，仅对NPC使用时有效。#Y#r#W制造者：＂碧魂．#Y#r#Y熔炼效果：#r#Y#r+3耐力 +9防御 #r#Y "
#my.htmlToEquip(desc)
# 多特效
# desc = "#r等级 60  五行 火#r#r防御 +169#r耐久度 400#r锻炼等级 6  镶嵌宝石 月亮石#r#G#G敏捷 -1#Y #G体质 +11#Y#Y#r#c4DBAF4特效：#c4DBAF4简易#Y #c4DBAF4永不磨损#Y  "
# 项链
# desc = "#r等级 160  #r灵力 +334#r耐久度 95#r锻炼等级 14  镶嵌宝石 舍利子#Y#r#c4DBAF4特效：#c4DBAF4永不磨损#Y#r#c4DBAF4套装效果：附加状态定心术#Y#Y#r#G开运孔数：5孔/5孔 (双5孔)#G#r星位：气血 +10#n#Y#r#W制造者：终极炼金师强化打造#Y#r#Y熔炼效果：#r#Y#r+6灵力#Y  "
# 武器
#desc = "#r等级 160  五行 金#r#r命中 +989 伤害 +531#r耐久度 215#r锻炼等级 11  镶嵌宝石 红玛瑙#r#G#G力量 +26#Y #G体质 +26#Y#Y#r#c4DBAF4特效：#c4DBAF4永不磨损#Y#r#G开运孔数：5孔/5孔#G#r符石: 气血 +15 速度 +1.5#n#b#G#r符石: 气血 +15 速度 +1.5#n#b#G#r符石: 气血 +15 速度 +1.5#n#G#r符石: 气血 +15 速度 +1.5#n#b#G#r符石: 气血 +15 速度 +1.5#n#r#cEE82EE符石组合: 天降大任#r门派条件：无#r部位条件：无#r无视召唤兽15%的物理防御进行攻击(该组合全身只有一件装备起效)#Y#r#W制造者：ξ．青锋°强化打造#Y  "
# 武器双宝石
# desc = "							#r等级 160  五行 金#r#r命中 +907 伤害 +556#r耐久度 265#r锻炼等级 11  镶嵌宝石 太阳石、 红玛瑙#Y#r#c4DBAF4特效：#c4DBAF4永不磨损#Y#r#W制造者：′飘羽グ凌毅强化打造#Y#r#Y   						"
# 召唤兽装备
#desc = "#r等级 105  #r命中率 +11%#r耐久度 678#r#G#G灵力 +10 #G体质 +7#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级再生#Y#Y#r#W制造者：水々萧萧#Y#r#Y镶嵌效果：#r#Y+16灵力 镶嵌等级：4#Y  "
#desc = "#r等级 85  #r伤害 +29 命中率 +10%#r耐久度 184#r#G#G力量 +21#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4高级神佑复生#Y#Y#r#Y镶嵌效果：#r#Y+60伤害 镶嵌等级：6#Y  "
#desc = "#r等级 95  #r速度 +30#r耐久度 580#r#G#G法力 +12#Y #G灵力 +10#Y#Y#r#W制造者：儿时梦丶燕子#Y  "
#desc = "#r等级 105  #r速度 +37 伤害 +38#r耐久度 695#r#G#G耐力 +6#Y#Y#r#c4DBAF4套装效果：附加状态#c4DBAF4偷袭#Y#Y#r#W制造者：з盛屹ψ#Y  "
#my.htmlToPetEquip(desc)
# 灵饰
#desc = "等级 100#r防御 +20#r耐久度 469#r精炼等级 2#r#c4DBAF4特效：超级简易#r#G法术伤害 +10 #cEE82EE[+8]#r#G法术伤害结果 +8 #cEE82EE[+6]#r#G穿刺等级 +8 #cEE82EE[+8]#r#W制造者：紫气东来强化打造#"

#desc = "等级 80#r伤害 +16#r耐久度 500#r#G法术伤害 +8#r#G法术伤害 +8#r#G法术伤害 +12#r#W制造者：七步杀①人パ强化打造#"
#my.htmlToLingShi(desc)

