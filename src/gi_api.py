import os.path
import json
from typing import List
from enum import Enum


class ElementType(Enum):
    ANEMO = 1  # 风
    GEO = 2  # 岩
    ELECTRO = 3  # 雷
    HYDRO = 4  # 水
    PYRO = 5  # 火
    CRYO = 6  # 冰
    DENDRO = 7  # 草
    PHYSICAL = 8  # 物理
    NONE = 9  # 无


class NationType(Enum):
    MONDSTADT = 1
    LIYUE = 2
    INAZUMA = 3
    SUMERU = 4
    FONTAINE = 5
    NATLAN = 6
    SNEZHNAYA = 7
    KHAENRIAH = 8
    OTHER = 9


class WeaponType(Enum):
    SWORD = 1
    CLAYMORE = 2
    POLEARM = 3
    CATALYST = 4
    BOW = 5


class GIAPI(object):
    stat_trans = {
        'FIGHT_PROP_BASE_HP': 'HP_BASE',
        'FIGHT_PROP_BASE_ATTACK': 'ATK_BASE',
        'FIGHT_PROP_BASE_DEFENSE': 'DEF_BASE',
        'FIGHT_PROP_CRITICAL_HURT': 'CRIT_DMG',
        'FIGHT_PROP_CRITICAL': 'CRIT_RATE',
        'FIGHT_PROP_HP_PERCENT': 'HP_PER',
        'FIGHT_PROP_ATTACK_PERCENT': 'ATK_PER',
        'FIGHT_PROP_DEFENSE_PERCENT': 'DEF_PER',
        'FIGHT_PROP_ELEMENT_MASTERY': 'EM',
        'FIGHT_PROP_CHARGE_EFFICIENCY': 'ER',
        'FIGHT_PROP_HEAL_ADD': 'HEAL_BONUS',
        'FIGHT_PROP_WIND_ADD_HURT': 'ANEMO_DMG',
        'FIGHT_PROP_ROCK_ADD_HURT': 'GEO_DMG',
        'FIGHT_PROP_ELEC_ADD_HURT': 'ELECTRO_DMG',
        'FIGHT_PROP_FIRE_ADD_HURT': 'PYRO_DMG',
        'FIGHT_PROP_WATER_ADD_HURT': 'HYDRO_DMG',
        'FIGHT_PROP_ICE_ADD_HURT': 'CRYO_DMG',
        'FIGHT_PROP_PHYSICAL_ADD_HURT': 'PHYSICAL_DMG',
        'FIGHT_PROP_ADD_HURT': 'ELEM_DMG',
        'FIGHT_PROP_SHIELD_COST_MINUS_RATIO': 'SHIELD_STRENGTH',
        "WEAPON_SWORD_ONE_HAND": 1,
        "WEAPON_CLAYMORE": 2,
        "WEAPON_POLE": 3,
        "WEAPON_CATALYST": 4,
        "WEAPON_BOW": 5
    }

    character_trans = {
        'Ayaka': ['Ayaka', 'CRYO', 'INAZUMA'],
        'Qin': ['Jean', 'ANEMO', 'MONDSTADT'],
        'Lisa': ['Lisa', 'ELECTRO', 'MONDSTADT'],
        'PlayerGirl': ['Traveler', 'NONE', 'OTHER'],
        'Barbara': ['Barbara', 'HYDRO', 'MONDSTADT'],
        'Kaeya': ['Kaeya', 'CRYO', 'MONDSTADT'],
        'Diluc': ['Diluc', 'PYRO', 'MONDSTADT'],
        'Razor': ['Razor', 'ELECTRO', 'MONDSTADT'],
        'Ambor': ['Amber', 'PYRO', 'MONDSTADT'],
        'Venti': ['Venti', 'ANEMO', 'MONDSTADT'],
        'Xiangling': ['Xiangling', 'PYRO', 'LIYUE'],
        'Beidou': ['Beidou', 'ELECTRO', 'LIYUE'],
        'Xingqiu': ['Xingqiu', 'HYDRO', 'LIYUE'],
        'Xiao': ['Xiao', 'ANEMO', 'LIYUE'],
        'Ningguang': ['Ningguang', 'GEO', 'LIYUE'],
        'Klee': ['Klee', 'PYRO', 'MONDSTADT'],
        'Zhongli': ['Zhongli', 'GEO', 'LIYUE'],
        'Fischl': ['Fischl', 'ELECTRO', 'MONDSTADT'],
        'Bennett': ['Bennett', 'PYRO', 'MONDSTADT'],
        'Tartaglia': ['Tartaglia', 'HYDRO', 'SNEZHNAYA'],
        'Noel': ['Noelle', 'GEO', 'MONDSTADT'],
        'Qiqi': ['Qiqi', 'CRYO', 'LIYUE'],
        'Chongyun': ['Chongyun', 'CRYO', 'LIYUE'],
        'Ganyu': ['Ganyu', 'CRYO', 'LIYUE'],
        'Albedo': ['Albedo', 'GEO', 'MONDSTADT'],
        'Diona': ['Diona', 'CRYO', 'MONDSTADT'],
        'Mona': ['Mona', 'HYDRO', 'MONDSTADT'],
        'Keqing': ['Keqing', 'ELECTRO', 'LIYUE'],
        'Sucrose': ['Sucrose', 'ANEMO', 'MONDSTADT'],
        'Xinyan': ['Xinyan', 'PYRO', 'LIYUE'],
        'Rosaria': ['Rosaria', 'CRYO', 'MONDSTADT'],
        'Hutao': ['Hutao', 'PYRO', 'LIYUE'],
        'Kazuha': ['Kazuha', 'ANEMO', 'INAZUMA'],
        'Feiyan': ['Yanfei', 'PYRO', 'LIYUE'],
        'Yoimiya': ['Yoimiya', 'PYRO', 'INAZUMA'],
        'Tohma': ['Thoma', 'PYRO', 'INAZUMA'],
        'Eula': ['Eula', 'CRYO', 'MONDSTADT'],
        'Shougun': ['Shogun', 'ELECTRO', 'INAZUMA'],
        'Sayu': ['Sayu', 'ANEMO', 'INAZUMA'],
        'Kokomi': ['Kokomi', 'HYDRO', 'INAZUMA'],
        'Gorou': ['Gorou', 'GEO', 'INAZUMA'],
        'Sara': ['Sara', 'ELECTRO', 'INAZUMA'],
        'Itto': ['Itto', 'GEO', 'INAZUMA'],
        'Aloy': ['Aloy', 'CRYO', 'OTHER'],
        'Shenhe': ['Shenhe', 'CRYO', 'LIYUE'],
        'Yunjin': ['Yunjin', 'GEO', 'LIYUE']
    }

    weapon_trans = {
        'UI_EquipIcon_Sword_Steel': 'Cool_Steel',
        'UI_EquipIcon_Sword_Dawn': 'Harbinger_of_Dawn',
        'UI_EquipIcon_Sword_Traveler': 'Travelers_Handy_Sword',
        'UI_EquipIcon_Sword_Darker': 'Dark_Iron_Sword',
        'UI_EquipIcon_Sword_Sashimi': 'Fillet_Blade',
        'UI_EquipIcon_Sword_Mitsurugi': 'Skyrider_Sword',
        'UI_EquipIcon_Sword_Zephyrus': 'Favonius_Sword',
        'UI_EquipIcon_Sword_Troupe': 'The_Flute',
        'UI_EquipIcon_Sword_Fossil': 'Sacrificial_Sword',
        'UI_EquipIcon_Sword_Theocrat': 'Royal_Longsword',
        'UI_EquipIcon_Sword_Rockkiller': 'Lions_Roar',
        'UI_EquipIcon_Sword_Proto': 'Prototype_Rancour',
        'UI_EquipIcon_Sword_Exotic': 'Iron_Sting',
        'UI_EquipIcon_Sword_Blackrock': 'Blackcliff_Longsword',
        'UI_EquipIcon_Sword_Bloodstained': 'The_Black_Sword',
        'UI_EquipIcon_Sword_Outlaw': 'The_Alley_Flash',
        'UI_EquipIcon_Sword_Psalmus': 'Sword_of_Descension',
        'UI_EquipIcon_Sword_Magnum': 'Festering_Desire',
        'UI_EquipIcon_Sword_Bakufu': 'Amenoma_Kageuchi',
        'UI_EquipIcon_Sword_Opus': 'Cinnabar_Spindle',
        'UI_EquipIcon_Sword_Falcon': 'Aquila_Favonia',
        'UI_EquipIcon_Sword_Dvalin': 'Skyward_Blade',
        'UI_EquipIcon_Sword_Widsith': 'FreedomSworn',
        'UI_EquipIcon_Sword_Kunwu': 'Summit_Shaper',
        'UI_EquipIcon_Sword_Morax': 'Primordial_Jade_Cutter',
        'UI_EquipIcon_Sword_Narukami': 'Mistsplitter_Reforged',
        'UI_EquipIcon_Claymore_Glaive': 'Ferrous_Shadow',
        'UI_EquipIcon_Claymore_Siegfry': 'Bloodtainted_Greatsword',
        'UI_EquipIcon_Claymore_Tin': 'White_Iron_Greatsword',
        'UI_EquipIcon_Claymore_Quartz': 'Quartz',
        'UI_EquipIcon_Claymore_Reasoning': 'Debate_Club',
        'UI_EquipIcon_Claymore_Mitsurugi': 'Skyrider_Greatsword',
        'UI_EquipIcon_Claymore_Zephyrus': 'Favonius_Greatsword',
        'UI_EquipIcon_Claymore_Troupe': 'The_Bell',
        'UI_EquipIcon_Claymore_Fossil': 'Sacrificial_Greatsword',
        'UI_EquipIcon_Claymore_Theocrat': 'Royal_Greatsword',
        'UI_EquipIcon_Claymore_Perdue': 'Rainslasher',
        'UI_EquipIcon_Claymore_Proto': 'Prototype_Archaic',
        'UI_EquipIcon_Claymore_Exotic': 'Whiteblind',
        'UI_EquipIcon_Claymore_Blackrock': 'Blackcliff_Slasher',
        'UI_EquipIcon_Claymore_Kione': 'Serpent_Spine',
        'UI_EquipIcon_Claymore_Lapis': 'Lithic_Blade',
        'UI_EquipIcon_Claymore_Dragonfell': 'SnowTombed_Starsliver',
        'UI_EquipIcon_Claymore_MillenniaTuna': 'Luxurious_SeaLord',
        'UI_EquipIcon_Claymore_Bakufu': 'Katsuragikiri_Nagamasa',
        'UI_EquipIcon_Claymore_Maria': 'Akuoumaru',
        'UI_EquipIcon_Claymore_Dvalin': 'Skyward_Pride',
        'UI_EquipIcon_Claymore_Wolfmound': 'Wolfs_Gravestone',
        'UI_EquipIcon_Claymore_Widsith': 'Song_of_Broken_Pines',
        'UI_EquipIcon_Claymore_Kunwu': 'The_Unforged',
        'UI_EquipIcon_Claymore_Itadorimaru': 'Redhorn_Stonethresher',
        'UI_EquipIcon_Pole_Ruby': 'White_Tassel',
        'UI_EquipIcon_Pole_Halberd': 'Halberd',
        'UI_EquipIcon_Pole_Noire': 'Black_Tassel',
        'UI_EquipIcon_Pole_Flagpole': 'Flagpole',
        'UI_EquipIcon_Pole_Stardust': 'Dragons_Bane',
        'UI_EquipIcon_Pole_Proto': 'Prototype_Starglitter',
        'UI_EquipIcon_Pole_Exotic': 'Crescent_Pike',
        'UI_EquipIcon_Pole_Blackrock': 'Blackcliff_Pole',
        'UI_EquipIcon_Pole_Gladiator': 'Deathmatch',
        'UI_EquipIcon_Pole_Lapis': 'Lithic_Spear',
        'UI_EquipIcon_Pole_Zephyrus': 'Favonius_Lance',
        'UI_EquipIcon_Pole_Theocrat': 'Royal_Spear',
        'UI_EquipIcon_Pole_Everfrost': 'Dragonspine_Spear',
        'UI_EquipIcon_Pole_Bakufu': 'Kitain_Cross_Spear',
        'UI_EquipIcon_Pole_Mori': 'The_Catch',
        'UI_EquipIcon_Pole_Maria': 'Wavebreakers_Fin',
        'UI_EquipIcon_Pole_Homa': 'Staff_of_Homa',
        'UI_EquipIcon_Pole_Dvalin': 'Skyward_Spine',
        'UI_EquipIcon_Pole_Kunwu': 'Vortex_Vanquisher',
        'UI_EquipIcon_Pole_Morax': 'Primordial_Jade_WingedSpear',
        'UI_EquipIcon_Pole_Santika': 'Calamity_Queller',
        'UI_EquipIcon_Pole_Narukami': 'Engulfing_Lightning',
        'UI_EquipIcon_Catalyst_Intro': 'Magic_Guide',
        'UI_EquipIcon_Catalyst_Pulpfic': 'Thrilling_Tales_of_Dragon_Slayers',
        'UI_EquipIcon_Catalyst_Lightnov': 'Otherworldly_Story',
        'UI_EquipIcon_Catalyst_Jade': 'Emerald_Orb',
        'UI_EquipIcon_Catalyst_Phoney': 'Twin_Nephrite',
        'UI_EquipIcon_Catalyst_Amber': 'Amber',
        'UI_EquipIcon_Catalyst_Zephyrus': 'Favonius_Codex',
        'UI_EquipIcon_Catalyst_Troupe': 'The_Widsith',
        'UI_EquipIcon_Catalyst_Fossil': 'Sacrificial_Fragments',
        'UI_EquipIcon_Catalyst_Theocrat': 'Royal_Grimoire',
        'UI_EquipIcon_Catalyst_Resurrection': 'Solar_Pearl',
        'UI_EquipIcon_Catalyst_Proto': 'Prototype_Amber',
        'UI_EquipIcon_Catalyst_Exotic': 'Mappa_Mare',
        'UI_EquipIcon_Catalyst_Blackrock': 'Blackcliff_Agate',
        'UI_EquipIcon_Catalyst_Truelens': 'Eye_of_Perception',
        'UI_EquipIcon_Catalyst_Outlaw': 'Wine_and_Song',
        'UI_EquipIcon_Catalyst_Everfrost': 'Frostbearer',
        'UI_EquipIcon_Catalyst_Ludiharpastum': 'Dodoco_Tales',
        'UI_EquipIcon_Catalyst_Bakufu': 'Hakushin_Ring',
        'UI_EquipIcon_Catalyst_Dvalin': 'Skyward_Atlas',
        'UI_EquipIcon_Catalyst_Fourwinds': 'Lost_Prayer_to_the_Sacred_Winds',
        'UI_EquipIcon_Catalyst_Kunwu': 'Memory_of_Dust',
        'UI_EquipIcon_Catalyst_Kaleido': 'Everlasting_Moonglow',
        'UI_EquipIcon_Bow_Crowfeather': 'Raven_Bow',
        'UI_EquipIcon_Bow_Arjuna': 'Sharpshooters_Oath',
        'UI_EquipIcon_Bow_Curve': 'Recurve_Bow',
        'UI_EquipIcon_Bow_Sling': 'Slingshot',
        'UI_EquipIcon_Bow_Msg': 'Messenger',
        'UI_EquipIcon_Bow_Hardwood': 'Hardwood',
        'UI_EquipIcon_Bow_Zephyrus': 'Favonius_Warbow',
        'UI_EquipIcon_Bow_Troupe': 'The_Stringless',
        'UI_EquipIcon_Bow_Fossil': 'Sacrificial_Bow',
        'UI_EquipIcon_Bow_Theocrat': 'Royal_Bow',
        'UI_EquipIcon_Bow_Recluse': 'Rust',
        'UI_EquipIcon_Bow_Proto': 'Prototype_Crescent',
        'UI_EquipIcon_Bow_Exotic': 'Compound_Bow',
        'UI_EquipIcon_Bow_Blackrock': 'Blackcliff_Warbow',
        'UI_EquipIcon_Bow_Viridescent': 'The_Viridescent_Hunt',
        'UI_EquipIcon_Bow_Outlaw': 'Alley_Hunter',
        'UI_EquipIcon_Bow_Nachtblind': 'Mitternachts_Waltz',
        'UI_EquipIcon_Bow_Fleurfair': 'Windblume_Ode',
        'UI_EquipIcon_Bow_Bakufu': 'hamayumi',
        'UI_EquipIcon_Bow_Predator': 'Predator',
        'UI_EquipIcon_Bow_Maria': 'Mouuns_Moon',
        'UI_EquipIcon_Bow_Dvalin': 'Skyward_Harp',
        'UI_EquipIcon_Bow_Amos': 'Amos_Bow',
        'UI_EquipIcon_Bow_Widsith': 'Elegy_for_the_End',
        'UI_EquipIcon_Bow_Worldbane': 'Polar_Star',
        'UI_EquipIcon_Bow_Narukami': 'Thundering_Pulse',
    }

    def __init__(self) -> None:
        self.outpath: str = ''
        self.referpath: str = ''

    def setpath(self, outpath='', referpath=''):
        self.outpath = outpath
        self.referpath = referpath

    def get_char_base(self):
        result: List[dict] = []

        # get raw data
        with open(os.path.join(self.referpath, 'AvatarExcelConfigData.json'), 'r') as f:
            data: List[dict] = json.load(f)

            for c in data:
                obj = dict()
                obj["IconName"] = c['IconName'].split('_')[-1]
                obj["QualityType"] = 5 if "QUALITY_ORANGE" ==\
                    c.get('QualityType') else 4
                obj['InitialWeapon'] = (c.get('InitialWeapon')-10000)//1000
                obj["HpBase"] = c.get('HpBase', 0)
                obj["AttackBase"] = c.get('AttackBase', 0)
                obj["DefenseBase"] = c.get('DefenseBase', 0)
                # abort bad data
                if (obj["AttackBase"] <= 7.5) or (obj["HpBase"] <= 720) or (obj["DefenseBase"] <= 40) or (obj["HpBase"] >= 2000):
                    continue
                # id == 2 is special, playerboy is repeated
                obj['AvatarPromoteId'] = c.get('AvatarPromoteId')
                obj['SkillDepotId'] = c.get('SkillDepotId')
                if (obj['AvatarPromoteId'] == 2 and obj['QualityType'] != 5) or (obj['IconName'] == 'PlayerBoy'):
                    continue
                result.append(obj)

        # get asc phase
        with open(os.path.join(self.referpath, 'AvatarPromoteExcelConfigData.json'), 'r') as f:
            data = json.load(f)

            tmp_pos = {}
            for i, o in enumerate(result):
                tmp_pos[o['AvatarPromoteId']] = i
            for pro in data:
                exist = pro.get('ScoinCost', False)
                if not exist:
                    continue
                pid = pro['AvatarPromoteId']
                pos = tmp_pos[pid]
                plv = pro['PromoteLevel']
                add_prop: List[dict] = pro['AddProps']
                if not result[pos].get('AddProps', False):
                    result[pos]['AddProps'] = {plv: []}
                else:
                    result[pos]['AddProps'].update({plv: []})
                for a in add_prop:
                    v = a.get('Value', 0)
                    if v != 0:
                        result[pos]['AddProps'][plv].append([a['PropType'], v])

        # dump raw data
        with open(os.path.join(self.outpath, 'CharacterConfigRaw.json'), 'w') as f:
            json.dump(result, f, indent=4)

        # tranlation
        # add element
        # add nation
        output: List[dict] = {}
        for c in result:
            obj = {}
            obj['name'] = self.character_trans[c['IconName']][0]
            obj['rarity'] = c['QualityType']
            obj['weapon'] = c['InitialWeapon']
            obj['element'] = ElementType[self.character_trans[c['IconName']][1]].value
            obj['region'] = NationType[self.character_trans[c['IconName']][2]].value
            obj['HP_BASE'] = c['HpBase']
            obj['ATK_BASE'] = c['AttackBase']
            obj['DEF_BASE'] = c['DefenseBase']
            extra_asc = self.stat_trans[c['AddProps'][6][-1][0]]
            obj['asc'] = {'HP_BASE': [], 'ATK_BASE': [],
                          'DEF_BASE': [], extra_asc: []}
            for lv_asc in c['AddProps'].values():
                for every_asc in lv_asc:
                    obj['asc'][self.stat_trans[every_asc[0]]].append(
                        every_asc[1])
                if len(lv_asc) == 3:
                    obj['asc'][extra_asc].append(0)
            output[obj['name']] = obj

        with open(os.path.join(self.outpath, 'CharacterConfig.json'), 'w') as f:
            json.dump(output, f, indent=4)

    def get_char_name(self):
        with open(os.path.join(self.outpath, 'CharacterConfig.json'), 'r') as f:
            data = json.load(f)
        with open(os.path.join(self.outpath, 'names.txt'), 'w') as t:
            for c in data:
                t.write(c['name']+'\n')

        with open(os.path.join(self.outpath, 'CharacterConfigRaw.json'), 'r') as f:
            data = json.load(f)
        with open(os.path.join(self.outpath, 'Rawnames.txt'), 'w') as t:
            for c in data:
                t.write(c['IconName']+'\n')

    def get_char_curve(self):
        result = {
            "4": [0 for i in range(101)],
            "5": [0 for i in range(101)]
        }
        with open(os.path.join(self.referpath, 'AvatarCurveExcelConfigData.json'), 'r') as f:
            js = json.load(f)
            for obj in js:
                lv = obj['Level']
                info = obj['CurveInfos']
                for c in info:
                    if c['Type'] == 'GROW_CURVE_HP_S4':
                        result['4'][lv] = c['Value']
                    elif c['Type'] == 'GROW_CURVE_HP_S5':
                        result['5'][lv] = c['Value']

        with open(os.path.join(self.outpath, 'CharacterLevelMultiplier.json'), 'w') as f:
            json.dump(result, f)

    def get_char_skill(self):
        with open(os.path.join(self.outpath, 'CharacterConfigRaw.json'), 'r') as f:
            raw_data = json.load(f)

        with open(os.path.join(self.referpath, 'AvatarSkillDepotExcelConfigData.json'), 'r') as f:
            depot_data = json.load(f)
            depot_data_map = {}
            for i, d in enumerate(depot_data):
                depot_data_map[d['Id']] = i

        with open(os.path.join(self.referpath, 'ProudSkillExcelConfigData.json'), 'r') as f:
            proud_skill_data = json.load(f)
            proud_skill_group_map = {}
            for i, p in enumerate(proud_skill_data):
                proud_skill_group_map.setdefault(
                    p['ProudSkillGroupId'], []).append(i)

        with open(os.path.join(self.referpath, 'AvatarSkillExcelConfigData.json'), 'r') as f:
            skill_config_data = json.load(f)
            skill_config_id_map = {}
            for i, s in enumerate(skill_config_data):
                skill_config_id_map[s['Id']] = i

        # with open(os.path.join(self.referpath, 'AvatarTalentExcelConfigData.json'), 'r') as f:
        #     constellation_data = json.load(f)
        #     constellation_id_map = {}
        #     for i, t in enumerate(constellation_data):
        #         constellation_id_map[t['TalentId']] = i

        result = []
        for c in raw_data:
            obj = {}
            obj['IconName'] = c['IconName']
            depot_id = obj['SkillDepotId'] = c['SkillDepotId']

            depot = depot_data[depot_data_map[depot_id]]
            EnergySkill_id = depot.get('EnergySkill')
            if not EnergySkill_id:
                continue
            energy_skill = skill_config_data[skill_config_id_map[EnergySkill_id]]
            if energy_skill.get('ProudSkillGroupId'):
                tmp_q = [
                    proud_skill_data[i] for i in proud_skill_group_map[energy_skill['ProudSkillGroupId']]
                ]
                obj['Q'] = []
                for q in tmp_q:
                    obj['Q'].append(
                        {'Level': q['Level'], 'ParamList': q['ParamList']})
            tmp_skills = [
                skill_config_data[skill_config_id_map[i]] for i in depot['Skills'] if i
            ]
            for i, s in enumerate(tmp_skills):
                cate_map = {0: 'A', 1: 'E', 2: 'sp'}
                tmp_sk = [
                    proud_skill_data[i] for i in proud_skill_group_map[s['ProudSkillGroupId']]
                ]
                obj[cate_map[i]] = []
                for sk in tmp_sk:
                    obj[cate_map[i]].append(
                        {'Level': sk['Level'], 'ParamList': sk['ParamList']})
            result.append(obj)
        # traveler is special (701-707)
        for depot_id in range(701, 708):
            depot = depot_data[depot_data_map[depot_id]]
            obj = {}
            obj['IconName'] = depot['TalentStarName'].split('_', 1)[-1]
            obj['SkillDepotId'] = depot_id
            EnergySkill_id = depot.get('EnergySkill')
            if EnergySkill_id:
                energy_skill = skill_config_data[skill_config_id_map[EnergySkill_id]]
                if energy_skill.get('ProudSkillGroupId'):
                    tmp_q = [
                        proud_skill_data[i] for i in proud_skill_group_map[energy_skill['ProudSkillGroupId']]
                    ]
                    obj['Q'] = []
                    for q in tmp_q:
                        obj['Q'].append(
                            {'Level': q['Level'], 'ParamList': q['ParamList']})
            else:
                continue
            tmp_skills = [
                skill_config_data[skill_config_id_map[i]] for i in depot['Skills'] if i
            ]
            for i, s in enumerate(tmp_skills):
                cate_map = {0: 'A', 1: 'E', 2: 'sp'}
                tmp_sk = [
                    proud_skill_data[i] for i in proud_skill_group_map[s['ProudSkillGroupId']]
                ]
                obj[cate_map[i]] = []
                for sk in tmp_sk:
                    obj[cate_map[i]].append(
                        {'Level': sk['Level'], 'ParamList': sk['ParamList']})
            result.append(obj)

        with open(os.path.join(self.outpath, 'SkillConfigRaw.json'), 'w') as f:
            json.dump(result, f, indent=4)

        process_data = {}
        for c in result:
            try:
                n = self.character_trans[c['IconName']][0]
            except:
                n = c['IconName']
            process_data[n] = {}
            for k in ['A', 'E', 'Q']:
                process_data[n][k] = {}
                for info in c[k]:
                    process_data[n][k][str(info['Level'])] = [
                        p for p in info['ParamList'] if p]
            if c.get('sp'):
                process_data[n]['sp'] = c['sp'][0]['ParamList']

        with open(os.path.join(self.outpath, 'SkillConfig.json'), 'w') as f:
            json.dump(process_data, f, indent=4)

    def get_weapon_base(self):
        result: List[dict] = []
        id_map = {}

        with open(os.path.join(self.referpath, 'WeaponExcelConfigData.json'), 'r') as f:
            data: List[dict] = json.load(f)

            for w in data:
                rarity = w['RankLevel']
                skill_id = w['SkillAffix'][0]
                if rarity < 3 or not skill_id:
                    continue

                obj = {}
                obj['Icon'] = w['Icon']
                obj['WeaponType'] = w['WeaponType']
                obj['RankLevel'] = rarity
                obj['SkillAffix'] = skill_id
                obj['WeaponProp'] = w['WeaponProp']

                id_map[skill_id] = len(result)
                result.append(obj)

        # with open(os.path.join(self.referpath, 'WeaponPromoteExcelConfigData.json')， 'r') as f:
        # 精确到一位，直接手动
        # 飞天大御剑数值有问题
        # asc_values = {
        #     3: [19.5, 38.9, 58.4, 77.8, 97.3, 116.7],
        #     4: [25.9, 51.9, 77.8, 103.7, 129.7, 155.6],
        #     5: [31.1, 62.2, 93.4, 124.5, 155.6, 186.7]
        # }

        with open(os.path.join(self.referpath, 'EquipAffixExcelConfigData.json'), 'r') as f:
            skill_data: List[dict] = json.load(f)

            for s in skill_data:
                skill_id = s['Id']
                i = id_map.get(skill_id, -1)
                if i < 0:
                    continue
                if not result[i].get('Skill', False):
                    result[i]['Skill'] = {}
                    result[i]['Skill']['AddProps'] = []
                    result[i]['Skill']['ParamList'] = []
                result[i]['Skill']['OpenConfig'] = s['OpenConfig']
                result[i]['Skill']['AddProps'].append(s['AddProps'][0])
                result[i]['Skill']['ParamList'].append(s['ParamList'])

        with open(os.path.join(self.outpath, 'WeaponConfigRaw.json'), 'w') as f:
            json.dump(result, f)

        process_result = []
        for w in result:
            obj = {}
            obj['name'] = self.weapon_trans[w['Icon']]
            obj['weapon_type'] = self.stat_trans[w['WeaponType']]
            obj['rarity'] = w['RankLevel']
            obj['sub_stat'] = self.stat_trans.get(
                w['WeaponProp'][1].get('PropType', ''))
            obj['stat_base'] = w['WeaponProp'][1].get('InitValue', 0)
            obj['stat_curve'] = w['WeaponProp'][1]['Type']
            obj['ATK_BASE'] = w['WeaponProp'][0]['InitValue']
            obj['atk_curve'] = w['WeaponProp'][0]['Type']
            obj['skill'] = {}
            obj['skill']['skill_name'] = w['Skill']['OpenConfig'].split(
                '_')[-1]
            stat_name = w['Skill']['AddProps'][0].get('PropType', None)
            obj['skill']['bonus_stat'] = self.stat_trans[stat_name] if stat_name else ''
            obj['skill']['bonus_stat_value'] = [a['Value']
                                                for a in w['Skill']['AddProps']] if stat_name else []
            obj['skill']['param_list'] = w['Skill']['ParamList']
            process_result.append(obj)

        with open(os.path.join(self.outpath, 'WeaponConfig.json'), 'w') as f:
            json.dump(process_result, f)

    def get_weapon_name(self):
        with open(os.path.join(self.outpath, 'weapon_name.txt'), 'w') as f:
            f.writelines([''.join([str(v), '\n'])
                         for v in self.weapon_trans.values()])

    def get_weapon_curve(self):
        # level 1 - 100, skip 0
        result = {}

        curve_names = ['GROW_CURVE_ATTACK_101',
                       'GROW_CURVE_ATTACK_102',
                       'GROW_CURVE_ATTACK_103',
                       'GROW_CURVE_ATTACK_104',
                       'GROW_CURVE_ATTACK_105',
                       'GROW_CURVE_CRITICAL_101',
                       'GROW_CURVE_ATTACK_201',
                       'GROW_CURVE_ATTACK_202',
                       'GROW_CURVE_ATTACK_203',
                       'GROW_CURVE_ATTACK_204',
                       'GROW_CURVE_ATTACK_205',
                       'GROW_CURVE_CRITICAL_201',
                       'GROW_CURVE_ATTACK_301',
                       'GROW_CURVE_ATTACK_302',
                       'GROW_CURVE_ATTACK_303',
                       'GROW_CURVE_ATTACK_304',
                       'GROW_CURVE_ATTACK_305',
                       'GROW_CURVE_CRITICAL_301']

        with open(os.path.join(self.referpath, 'WeaponCurveExcelConfigData.json'), 'r') as f:
            js = json.load(f)

        for curve_name in curve_names:
            result[curve_name] = [0 for i in range(101)]

        for obj in js:
            lv = obj['Level']
            info = obj['CurveInfos']
            for c in info:
                result[c['Type']][lv] = c['Value']

        with open(os.path.join(self.outpath, 'WeaponLevelMultiplier.json'), 'w') as f:
            json.dump(result, f)

    def get_react_curve(self):
        # level 1 - 100, skip 0
        with open(os.path.join(self.referpath, 'ElementCoeffExcelConfigData.json')) as f:
            js = json.load(f)

        result = {'player':[0], 'environment':[0], 'shield':[0]}
        for obj in js:
            if obj.get('Level', False):
                if 1 <= obj['Level'] <= 100:
                    result['player'].append(obj['PlayerElementLevelCo'])
                    result['environment'].append(obj['ElementLevelCo'])
                    result['shield'].append(obj['PlayerShieldLevelCo'])

        with open(os.path.join(self.outpath, 'ReactionLevelMultiplier.json'), 'w') as f:
            json.dump(result, f)


if __name__ == '__main__':
    g = GIAPI()
    g.setpath('./', './reference')
    # g.get_char_base()
    # g.get_char_skill()
    # g.get_weapon_curve()
    # g.get_react_curve()
