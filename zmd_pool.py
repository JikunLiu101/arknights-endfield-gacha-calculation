import random
CURRENT_CHARACTER_WATER_LEVEL_ZMD = 0 # 继承的角色池水位（保底，小保底）

class CharacterPoolZmd:
    """
    Class of Character pool for Endfield.
    """
    def __init__(self, target_char_code, non_target_char_code_1, non_target_char_code_2, normal_char_codes):
        self.target_char_code = target_char_code
        self.base_rate = 0.008 # 6星基础概率，0.8%
        self.target_rate = 0.5 # 6星为当期Up的概率，50%
        self.non_target_chars = []
        self.non_target_chars.extend([non_target_char_code_1, non_target_char_code_2])
        self.non_target_chars.extend(normal_char_codes)
        self.accumulation = 0 # 不继承的卡池井数，用于计算120必出（大保底）

    def get_current_rate(self, current_water_level)-> float:
        if current_water_level <= 65:
            return self.base_rate
        elif current_water_level > 65 and current_water_level < 80:
            return self.base_rate + (current_water_level - 65) * 0.05 # 65抽后每抽提升5%概率
        elif current_water_level == 80: # 80抽时6星概率为100%
            return 1
        else:
            raise ValueError("Wrong current water level for calculating rates")


    def pull(self)->str|Exception|None:
        global CURRENT_CHARACTER_WATER_LEVEL_ZMD
        try:
            # 获取当次抽卡出6星概率
            rate = self.get_current_rate(CURRENT_CHARACTER_WATER_LEVEL_ZMD)

            # 第一步，如果120抽，必出up，清空水位和井
            if self.accumulation > 119:
                self.accumulation = 0
                CURRENT_CHARACTER_WATER_LEVEL_ZMD = 0
                return self.target_char_code

            # 第二步，利用random判断是否出6星
            if random.random() >= rate:
                # 未出则水位与井+1
                self.accumulation += 1
                CURRENT_CHARACTER_WATER_LEVEL_ZMD += 1
                return None
            
            # 出6星则利用random判断是否为当期up，并清空水位（小保底）
            CURRENT_CHARACTER_WATER_LEVEL_ZMD = 0
            if random.random() < self.target_rate:
                # 是当期up，清空井
                self.accumulation = 0
                return self.target_char_code
            else:
                # 非当期up，累积井，并出一个随机非up
                self.accumulation += 1
                return random.choice(self.non_target_chars)

        except Exception as e:
            return e


class WeaponPoolZmd:
    """
    Docstring for WeaponPoolZmd
    """
    def __init__(self, target_weapon_code):
        self.target_weapon_code = target_weapon_code
        self.base_rate = 0.04
        self.target_rate = 0.25 # 6星武器25%概率不歪
        self.accumulation_4 = 0 # 井1，不继承的卡池井数1，用于计算40抽必6星
        self.accumulation_8 = 0 # 井2，不继承的卡池井数2，用于计算80抽必up
        pass

    def get_current_rate(self):
            return self.base_rate

    def pull_x10(self, owned_weapons: dict) -> dict[str]|Exception:
        # 由于yj说的是一次申领等于10连，3次申领没出6星的情况下第四次申领才出，所以这里不能直接用40抽必出和80抽必出的算法，而应该进行4次loop(10)必出
        try:
            # 进行一次申领等于10连
            get_6_star = False
            get_target_weapon = False
            for i in range(1, 11):  # 10连应该是10次抽取
                # 判断单抽是否出6星
                if random.random() < self.get_current_rate():
                    # 出6星，判断是否为当期up
                    if random.random() < self.target_rate:
                        # 是当期up，清空井
                        get_6_star = True
                        get_target_weapon = True
                        self.accumulation_4 = 0
                        self.accumulation_8 = 0
                        owned_weapons[self.target_weapon_code] = owned_weapons.get(self.target_weapon_code, 0) + 1
                    else:
                        # 非当期up，清空井1，累积井2，并出一个随机非up
                        get_6_star = True
                        self.accumulation_4 = 0
                        self.accumulation_8 += 1
                        owned_weapons["non_target_weapon"] = owned_weapons.get("non_target_weapon", 0) + 1
            # 若10连未出6星，井1与井2均+1
            if not get_6_star:
                self.accumulation_4 += 1
                self.accumulation_8 += 1
            # 出了6星但不是up，井2+1 (这个逻辑已经在上面处理过了，此处无需额外操作)
            return owned_weapons
        except Exception as e:
            return e



def pull_only_when_have_80_pulls_till_get_target_no_topup(number_of_scenarios: int, basic_balance_char: int, release_balance_char: int, pool_list: list[(CharacterPoolZmd,WeaponPoolZmd)], basic_balance_weap: int, release_balance_weap: int):
    """
    策略：小保派，手里至少有80抽角色池才开始抽，抽出角色且有至少4次申领机会才开始抽武器，不垫池子也不额外充值，计算最终角色和武器拥有情况，抽出up角色就在角色池收手，抽出up武器就在武器池收手

    测试number_of_scenarios个玩家
        每个玩家开服版本拥有basic_balance抽角色池
            每个版本获得release_balance抽角色池
    共模拟pool_list个版本池子

    默认：每1抽角色池送0.02抽武器池，每个角色池6星送1抽武器池
    """
    global CURRENT_CHARACTER_WATER_LEVEL_ZMD
    total_results = []
    
    for _ in range(number_of_scenarios):
        owned_chars = set()
        owned_weapons = {}
        pull_balance_char = basic_balance_char
        pull_balance_weap = basic_balance_weap
        CURRENT_CHARACTER_WATER_LEVEL_ZMD = 0
        temp_balance_char = 0
        
        for pool_idx, pool in enumerate(pool_list):
            char_pool, weap_pool = pool
            pull_balance_char += release_balance_char
            pull_balance_weap += release_balance_weap
            char_pool.accumulation = 0
            weap_pool.accumulation_4 = 0
            weap_pool.accumulation_8 = 0
            count = 0
            got_target = False
            
            target = char_pool.target_char_code
            
            # 检查是否已经拥有该up角色
            if target in owned_chars:
                continue
            if temp_balance_char + pull_balance_char >= 80:
                while temp_balance_char > 0 or pull_balance_char > 0:
                    result = char_pool.pull()
                    count += 1
                    if temp_balance_char > 0:
                        temp_balance_char -= 1
                    else:
                        pull_balance_char -= 1
                    
                    # 每1抽送0.02抽武器池
                    pull_balance_weap += 0.02
                    
                    if result == target:
                        owned_chars.add(target)
                        pull_balance_weap += 1  # 6星送1抽武器池
                        got_target = True
                        break
                    elif result is not None:
                        owned_chars.add(result)
                        pull_balance_weap += 1  # 6星送1抽武器池
                
                # 抽到目标角色后，且拥有至少4次申领机会才开始抽武器
                if got_target and pull_balance_weap >= 4:
                    # 抽到目标武器或余额用完为止
                    while pull_balance_weap >= 1:
                        pull_balance_weap -= 1
                        weap_pool.pull_x10(owned_weapons)
                        if weap_pool.target_weapon_code in owned_weapons and owned_weapons[weap_pool.target_weapon_code] > 0:
                            break
                        # 如果4次申领还没出6星，强制出
                        if weap_pool.accumulation_4 >= 4:
                            if random.random() < weap_pool.target_rate:
                                weap_pool.accumulation_4 = 0
                                weap_pool.accumulation_8 = 0
                                owned_weapons[weap_pool.target_weapon_code] = owned_weapons.get(weap_pool.target_weapon_code, 0) + 1
                            else:
                                weap_pool.accumulation_4 = 0
                                weap_pool.accumulation_8 += 1
                                owned_weapons["non_target_weapon"] = owned_weapons.get("non_target_weapon", 0) + 1
                            break
                        # 如果8次申领还没出up，强制出up
                        if weap_pool.accumulation_8 >= 8:
                            weap_pool.accumulation_4 = 0
                            weap_pool.accumulation_8 = 0
                            owned_weapons[weap_pool.target_weapon_code] = owned_weapons.get(weap_pool.target_weapon_code, 0) + 1
                            break
            
            temp_balance_char = 0
            if count >= 60:
                # 在当前角色池花费超过60抽，下个角色卡池获得10抽角色池余额，仅限下个角色池使用
                temp_balance_char = 10
        
        total_results.append((owned_chars, owned_weapons))
    
    return total_results

def pull_only_when_have_120_pulls_till_get_target_no_topup(number_of_scenarios: int, basic_balance_char: int, release_balance_char: int, pool_list: list[(CharacterPoolZmd,WeaponPoolZmd)], basic_balance_weap: int, release_balance_weap: int):
    """
    策略：大保派，手里至少有120抽角色池才开始抽，抽出角色且有至少4次申领机会才开始抽武器，不垫池子也不额外充值，计算最终角色和武器拥有情况，抽出up角色就在角色池收手，抽出up武器就在武器池收手

    测试number_of_scenarios个玩家
        每个玩家开服版本拥有basic_balance抽角色池
            每个版本获得release_balance抽角色池
    共模拟pool_list个版本池子

    默认：每1抽角色池送0.02抽武器池，每个角色池6星送1抽武器池
    """
    global CURRENT_CHARACTER_WATER_LEVEL_ZMD
    total_results = []
    
    for _ in range(number_of_scenarios):
        owned_chars = set()
        owned_weapons = {}
        pull_balance_char = basic_balance_char
        pull_balance_weap = basic_balance_weap
        CURRENT_CHARACTER_WATER_LEVEL_ZMD = 0
        temp_balance_char = 0
        
        for pool_idx, pool in enumerate(pool_list):
            char_pool, weap_pool = pool
            pull_balance_char += release_balance_char
            pull_balance_weap += release_balance_weap
            char_pool.accumulation = 0
            weap_pool.accumulation_4 = 0
            weap_pool.accumulation_8 = 0
            count = 0
            got_target = False
            
            target = char_pool.target_char_code
            
            # 检查是否已经从之前的池子获得该目标角色
            if target in owned_chars:
                continue
            
            if pull_balance_char + temp_balance_char >= 120:
                # 抽卡直到获得目标或用完抽数
                while temp_balance_char + pull_balance_char > 0:
                    result = char_pool.pull()
                    count += 1
                    if temp_balance_char > 0:
                        temp_balance_char -= 1
                    else:
                        pull_balance_char -= 1
                    
                    # 每1抽送0.02抽武器池
                    pull_balance_weap += 0.02
                    
                    if result == target:
                        owned_chars.add(target)
                        pull_balance_weap += 1  # 6星送1抽武器池
                        got_target = True
                        break
                    elif result is not None:
                        owned_chars.add(result)
                        pull_balance_weap += 1  # 6星送1抽武器池
                
                # 抽到目标角色后，且拥有至少4次申领机会才开始抽武器
                if got_target and pull_balance_weap >= 4:
                    while pull_balance_weap >= 1:
                        pull_balance_weap -= 1
                        weap_pool.pull_x10(owned_weapons)
                        if weap_pool.target_weapon_code in owned_weapons and owned_weapons[weap_pool.target_weapon_code] > 0:
                            break
                        # 4次申领必出6星
                        if weap_pool.accumulation_4 >= 4:
                            if random.random() < weap_pool.target_rate:
                                weap_pool.accumulation_4 = 0
                                weap_pool.accumulation_8 = 0
                                owned_weapons[weap_pool.target_weapon_code] = owned_weapons.get(weap_pool.target_weapon_code, 0) + 1
                            else:
                                weap_pool.accumulation_4 = 0
                                weap_pool.accumulation_8 += 1
                                owned_weapons["non_target_weapon"] = owned_weapons.get("non_target_weapon", 0) + 1
                            break
                        # 8次申领必出up
                        if weap_pool.accumulation_8 >= 8:
                            weap_pool.accumulation_4 = 0
                            weap_pool.accumulation_8 = 0
                            owned_weapons[weap_pool.target_weapon_code] = owned_weapons.get(weap_pool.target_weapon_code, 0) + 1
                            break
            
            temp_balance_char = 0
            if count >= 60:
                temp_balance_char += 10
        
        total_results.append((owned_chars, owned_weapons))
    
    return total_results

def pull_for_each_target_with_topup(number_of_scenarios: int, basic_balance_char: int, release_balance_char: int, pool_list: list[(CharacterPoolZmd,WeaponPoolZmd)], basic_balance_weap: int, release_balance_weap: int):
    """
    策略：0+1全图鉴党，以必得每期up角色一次+up武器一次为目标，在弥补额外抽数的情况下，计算最终需要充值多少抽角色池和多少抽武器池，（注意使用充值的角色抽数也可以按照默认规则获得武器池抽数），抽到up角色且有至少4次申领机会才开始抽武器

    测试number_of_scenarios个玩家
        每个玩家开服版本拥有basic_balance_char抽角色池，basic_balance_weap抽武器池
            每个版本获得release_balance_char抽角色池，release_balance_weap抽武器池
    共模拟pool_list个版本池子

    默认：每1抽角色池送0.02抽武器池，每个角色池6星送1抽武器池
    """
    global CURRENT_CHARACTER_WATER_LEVEL_ZMD
    total_results = []
    
    for _ in range(number_of_scenarios):
        owned_chars = set()
        owned_weapons = {}
        pull_balance_char = basic_balance_char
        pull_balance_weap = basic_balance_weap
        CURRENT_CHARACTER_WATER_LEVEL_ZMD = 0
        temp_balance_char = 0
        topup_char = 0
        topup_weap = 0
        
        for pool_idx, pool in enumerate(pool_list):
            char_pool, weap_pool = pool
            pull_balance_char += release_balance_char
            pull_balance_weap += release_balance_weap
            char_pool.accumulation = 0
            weap_pool.accumulation_4 = 0
            weap_pool.accumulation_8 = 0
            count = 0
            
            target = char_pool.target_char_code
            
            # 检查是否已经从之前的池子获得该目标角色
            if target in owned_chars:
                continue
            
            # 抽卡直到获得目标
            while True:
                if pull_balance_char + temp_balance_char > 0:
                    if temp_balance_char > 0:
                        temp_balance_char -= 1
                    else:
                        pull_balance_char -= 1
                else:
                    topup_char += 1
                
                result = char_pool.pull()
                count += 1
                
                # 每1抽送0.02抽武器池
                pull_balance_weap += 0.02
                
                if result == target:
                    owned_chars.add(target)
                    pull_balance_weap += 1  # 6星送1抽武器池
                    break
                elif result is not None:
                    owned_chars.add(result)
                    pull_balance_weap += 1  # 6星送1抽武器池
            
            # 抽到up角色后，确保有至少4次申领机会才开始抽武器，否则先补充至4次
            while pull_balance_weap < 4:
                topup_weap += 1
                pull_balance_weap += 1
            
            # 抽武器直到获得目标武器
            while True:
                if pull_balance_weap >= 1:
                    pull_balance_weap -= 1
                else:
                    topup_weap += 1
                
                weap_pool.pull_x10(owned_weapons)
                
                if weap_pool.target_weapon_code in owned_weapons and owned_weapons[weap_pool.target_weapon_code] > 0:
                    break
                
                # 4次申领必出6星
                if weap_pool.accumulation_4 >= 4:
                    if random.random() < weap_pool.target_rate:
                        weap_pool.accumulation_4 = 0
                        weap_pool.accumulation_8 = 0
                        owned_weapons[weap_pool.target_weapon_code] = owned_weapons.get(weap_pool.target_weapon_code, 0) + 1
                    else:
                        weap_pool.accumulation_4 = 0
                        weap_pool.accumulation_8 += 1
                        owned_weapons["non_target_weapon"] = owned_weapons.get("non_target_weapon", 0) + 1
                    if weap_pool.target_weapon_code in owned_weapons and owned_weapons[weap_pool.target_weapon_code] > 0:
                        break
                
                # 8次申领必出up
                if weap_pool.accumulation_8 >= 8:
                    weap_pool.accumulation_4 = 0
                    weap_pool.accumulation_8 = 0
                    owned_weapons[weap_pool.target_weapon_code] = owned_weapons.get(weap_pool.target_weapon_code, 0) + 1
                    break
            
            temp_balance_char = 0
            if count >= 60:
                temp_balance_char += 10
        
        total_results.append((topup_char, topup_weap))
    
    return total_results