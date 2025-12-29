import random

CURRENT_WATER_LEVEL_GS = 0
IS_BIG = False

class CharacterPoolGs:
    """
    现在，是幻想时间！
    假如终末地使用的是80抽小保底，120抽大保底，大小保底均可继承的角色池机制，那么每个角色池的实现可以使用这个类来模拟。
    """
    def __init__(self, target_char_code, non_target_char_code_1, non_target_char_code_2, normal_char_codes):
        self.target_char_code = target_char_code
        self.base_rate = 0.008
        self.target_rate = 0.5
        self.non_target_chars = []
        self.non_target_chars.extend([non_target_char_code_1, non_target_char_code_2])
        self.non_target_chars.extend(normal_char_codes)

    def get_current_rate(self, current_water_level)-> float:
        if current_water_level <= 60:
            return self.base_rate
        elif current_water_level > 60 and current_water_level < 90:
            return self.base_rate + (current_water_level - 60) * 0.03
        elif current_water_level == 90:
            return 1
        else:
            raise ValueError("Wrong current water level for calculating rates")


    def pull(self)->str|Exception|None:
        global CURRENT_WATER_LEVEL_GS
        global IS_BIG
        _current_water_level = CURRENT_WATER_LEVEL_GS
        try:
            rate = self.get_current_rate(_current_water_level)

            # Second: check whether this pull yields any character at all
            if random.random() >= rate:
                # no character obtained this pull
                CURRENT_WATER_LEVEL_GS += 1
                return None
            
            # Otherwise roll for a target character using target_rate, and clear water level
            CURRENT_WATER_LEVEL_GS = 0
            if IS_BIG or random.random() < self.target_rate:
                # got the target; reset is_big to false
                IS_BIG = False
                return self.target_char_code
            else:
                # non-target obtained: turn to big
                IS_BIG = True
                return random.choice(self.non_target_chars)

        except Exception as e:
            return e

@DeprecationWarning   
def pull_for_each_pool_till_get_target_no_topup(number_of_scenarios: int, basic_balance: int, release_balance: int, pool_list: list[CharacterPoolGs]):
    # mock number of scenarios, where each senario keeps pulling till get the target character, no top up.
    total_results = []
    global CURRENT_WATER_LEVEL_GS
    global IS_BIG
    for _ in range(number_of_scenarios):
        CURRENT_WATER_LEVEL_GS = 0
        IS_BIG = False
        owned_chars = []
        temp_balance = 0
        pull_balance = basic_balance

        for pool_idx, pool in enumerate(pool_list):
            pull_balance += release_balance
            count = 0 # number of pulls spent in current pool, clear after entering next pool
            
            target = pool.target_char_code
            
            # Check if already own target from previous pool
            if target in owned_chars:
                continue
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

@DeprecationWarning   
def pull_only_when_have_90_pulls_till_get_target_no_topup(number_of_scenarios: int, basic_balance: int, release_balance: int, pool_list: list[CharacterPoolGs]):
    # mock number of scenarios, where each senario only pulls when having balance of 80 pulls. Stop pulling after having the target character, no top up.
    global CURRENT_WATER_LEVEL_GS
    global IS_BIG
    total_results = []
    
    for _ in range(number_of_scenarios):
        owned_chars = []
        pull_balance = basic_balance
        CURRENT_WATER_LEVEL_GS = 0
        IS_BIG = False
        temp_balance = 0
        
        for pool_idx, pool in enumerate(pool_list):
            pull_balance += release_balance
            count = 0 # number of pulls spent in current pool, clear after entering next pool
            
            target = pool.target_char_code
            
            # Check if already own target from previous pool
            if target in owned_chars:
                continue
            if temp_balance+pull_balance >=90:
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

@DeprecationWarning
def pull_for_each_target_char_with_topup(number_of_scenarios: int, basic_balance: int, release_balance: int, pool_list: list[CharacterPoolGs]):
    # mock number of scenarios, where each senario only stops pulling after having the target character, top up when needed.
    global CURRENT_WATER_LEVEL_GS
    global IS_BIG
    total_results = []
    
    for _ in range(number_of_scenarios):
        owned_chars = []
        pull_balance = basic_balance
        CURRENT_WATER_LEVEL_GS = 0
        temp_balance = 0
        top_up = 0
        IS_BIG = False
        
        for pool_idx, pool in enumerate(pool_list):
            pull_balance += release_balance
            count = 0 # number of pulls spent in current pool
            
            target = pool.target_char_code
            
            # Check if already own target from previous pool
            if target in owned_chars:
                continue
            
            # Pull until get target
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