import random
CURRENT_WATER_LEVEL_ZMD = 0


class CharacterPoolZmd:
    """
    Class of Character pool for Endfield.
    """
    def __init__(self, target_char_code, non_target_char_code_1, non_target_char_code_2, normal_char_codes):
        self.target_char_code = target_char_code
        self.base_rate = 0.008
        self.target_rate = 0.5
        self.non_target_chars = []
        self.non_target_chars.extend([non_target_char_code_1, non_target_char_code_2])
        self.non_target_chars.extend(normal_char_codes)
        self.accumulation = 0

    def get_current_rate(self, current_water_level)-> float:
        if current_water_level <= 65:
            return self.base_rate
        elif current_water_level > 65 and current_water_level < 80:
            return self.base_rate + (current_water_level - 65) * 0.05
        elif current_water_level == 80:
            return 1
        else:
            raise ValueError("Wrong current water level for calculating rates")


    def pull(self)->str|Exception|None:
        global CURRENT_WATER_LEVEL_ZMD
        _current_water_level = CURRENT_WATER_LEVEL_ZMD
        try:
            rate = self.get_current_rate(_current_water_level)

            # First, if accumulation reached pity threshold, guarantee target
            if self.accumulation > 119:
                self.accumulation = 0
                CURRENT_WATER_LEVEL_ZMD = 0
                return self.target_char_code

            # Second: check whether this pull yields any character at all
            if random.random() >= rate:
                # no character obtained this pull
                self.accumulation += 1
                CURRENT_WATER_LEVEL_ZMD += 1
                return None
            
            # Otherwise roll for a target character using target_rate, and clear water level
            CURRENT_WATER_LEVEL_ZMD = 0
            if random.random() < self.target_rate:
                # got the target; reset accumulation
                self.accumulation = 0
                return self.target_char_code
            else:
                # non-target obtained: increment accumulation (towards pity)
                self.accumulation += 1
                return random.choice(self.non_target_chars)

        except Exception as e:
            return e


def pull_only_when_have_80_pulls_till_get_target_no_topup(number_of_scenarios: int, basic_balance: int, release_balance: int, pool_list: list[CharacterPoolZmd]):
    # mock number of scenarios, where each senario only pulls when having 80 balances. Stop pulling after having the target character, no top up.
    global CURRENT_WATER_LEVEL_ZMD
    total_results = []
    
    for _ in range(number_of_scenarios):
        owned_chars = []
        pull_balance = basic_balance
        CURRENT_WATER_LEVEL_ZMD = 0
        IS_BIG = False
        temp_balance = 0
        
        for pool_idx, pool in enumerate(pool_list):
            pull_balance += release_balance
            pool.accumulation = 0 # number of pulls spent in current pool, clear after getting target character
            count = 0 # number of pulls spent in current pool, clear after entering next pool
            
            target = pool.target_char_code
            
            # Check if already own target from previous pool
            if target in owned_chars:
                continue
            if temp_balance+pull_balance >=80:
                while temp_balance > 0 or pull_balance > 0:
                    result = pool.pull()
                    count +=1
                    if temp_balance > 0:
                        temp_balance -= 1
                    else:
                        pull_balance -= 1
                    if result == target:
                        owned_chars.append(target)
                        break
                    elif result is not None:
                        owned_chars.append(result)
            temp_balance = 0
            if count >= 60:
                temp_balance = 10 # used for next pool
        
        total_results.append(owned_chars)
    
    return total_results

def pull_only_when_have_120_pulls_till_get_target_no_topup(number_of_scenarios: int, basic_balance: int, release_balance: int, pool_list: list[CharacterPoolZmd]):
    # mock number of scenarios, where each senario only pulls when have 120 pulls available. Stop pulling after having the target character, no top up.
    global CURRENT_WATER_LEVEL_ZMD
    total_results = []
    
    for _ in range(number_of_scenarios):
        owned_chars = []
        pull_balance = basic_balance
        CURRENT_WATER_LEVEL_ZMD = 0
        temp_balance = 0
        
        for pool_idx, pool in enumerate(pool_list):
            pull_balance += release_balance
            pool.accumulation = 0
            count = 0 # number of pulls spent in current pool
            
            target = pool.target_char_code
            
            # Check if already own target from previous pool
            if target in owned_chars:
                continue
            
            if pull_balance+temp_balance >= 120:
                # Pull until get target or run out of pulls
                while temp_balance+pull_balance > 0:
                    result = pool.pull()
                    count +=1
                    if temp_balance>0:
                        temp_balance-=1
                    else:
                        pull_balance -= 1
                    if result == target:
                        owned_chars.append(target)
                        break
                    elif result is not None:
                        owned_chars.append(result)
            temp_balance = 0
            if count >= 60:
                temp_balance += 10 # used for next pool
        
        total_results.append(owned_chars)
    
    return total_results

def pull_for_each_target_char_with_topup(number_of_scenarios: int, basic_balance: int, release_balance: int, pool_list: list[CharacterPoolZmd]):
    # mock number of scenarios, where each senario keeps pulling until having the target character, top up when needed.
    global CURRENT_WATER_LEVEL_ZMD
    total_results = []
    
    for _ in range(number_of_scenarios):
        owned_chars = []
        pull_balance = basic_balance
        CURRENT_WATER_LEVEL_ZMD = 0
        temp_balance = 0
        top_up = 0
        
        for pool_idx, pool in enumerate(pool_list):
            pull_balance += release_balance
            pool.accumulation = 0
            count = 0 # number of pulls spent in current pool
            
            target = pool.target_char_code
            
            # Check if already own target from previous pool
            if target in owned_chars:
                continue
            
            # Pull until get target or run out of balances
            while True:
                if pull_balance+temp_balance > 0:
                    result = pool.pull()
                    count +=1
                    if temp_balance>0:
                        temp_balance-=1
                    else:
                        pull_balance -= 1
                else:
                    top_up += 1
                    result = pool.pull()
                    count +=1
                if result == target:
                    owned_chars.append(target)
                    break
                elif result is not None:
                    owned_chars.append(result)
            temp_balance = 0
            if count >= 60:
                temp_balance += 10 # used for next pool
        
        total_results.append(top_up)
    
    return total_results