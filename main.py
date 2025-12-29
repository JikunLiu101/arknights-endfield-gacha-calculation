
import collections
import collections, statistics
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False
from zmd_pool import CharacterPoolZmd
import zmd_pool

# 如果自己跑测试，可以调整这些数值：
BASIC_BALANCE_CHAR = 121 # 数据参考：让你爱上学习@B站，不含版本福利与每日 （176-55）
RELEASE_BALANCE_CHAR = 55 # 模拟数据，可调整
BASIC_BALANCE_WEAP = 2 # 无具体数据，可调整
RELEASE_BALANCE_WEAP = 2 # 模拟数据，可调整


# 角色一览
NORMAL_CHAR_1 = "normal_character_1"
NORMAL_CHAR_2 = "normal_character_2"
NORMAL_CHAR_3 = "normal_character_3"
NORMAL_CHAR_4 = "normal_character_4"
NORMAL_CHAR_5 = "normal_character_5"
TARGET_CHAR_1 = "target_character_1"
TARGET_CHAR_2 = "target_character_2"
TARGET_CHAR_3 = "target_character_3"
TARGET_CHAR_4 = "target_character_4"
TARGET_CHAR_5 = "target_character_5"
TARGET_CHAR_6 = "target_character_6"
TARGET_CHAR_7 = "target_character_7"
TARGET_CHAR_8 = "target_character_8"
NORMAL_CHAR_CODES = [NORMAL_CHAR_1, NORMAL_CHAR_2, NORMAL_CHAR_3, NORMAL_CHAR_4, NORMAL_CHAR_5]

# 角色池一览
CHAR_POOL_1_ZMD = CharacterPoolZmd(TARGET_CHAR_1, TARGET_CHAR_2, TARGET_CHAR_3, NORMAL_CHAR_CODES)
CHAR_POOL_2_ZMD = CharacterPoolZmd(TARGET_CHAR_2, TARGET_CHAR_1, TARGET_CHAR_3, NORMAL_CHAR_CODES)
CHAR_POOL_3_ZMD = CharacterPoolZmd(TARGET_CHAR_3, TARGET_CHAR_1, TARGET_CHAR_2, NORMAL_CHAR_CODES)
CHAR_POOL_4_ZMD = CharacterPoolZmd(TARGET_CHAR_4, TARGET_CHAR_3, TARGET_CHAR_2, NORMAL_CHAR_CODES)
CHAR_POOL_5_ZMD = CharacterPoolZmd(TARGET_CHAR_5, TARGET_CHAR_4, TARGET_CHAR_3, NORMAL_CHAR_CODES)
CHAR_POOL_6_ZMD = CharacterPoolZmd(TARGET_CHAR_6, TARGET_CHAR_5, TARGET_CHAR_4, NORMAL_CHAR_CODES)
CHAR_POOL_7_ZMD = CharacterPoolZmd(TARGET_CHAR_7, TARGET_CHAR_6, TARGET_CHAR_5, NORMAL_CHAR_CODES)
CHAR_POOL_8_ZMD = CharacterPoolZmd(TARGET_CHAR_8, TARGET_CHAR_7, TARGET_CHAR_6, NORMAL_CHAR_CODES)

# 武器池一览
from zmd_pool import WeaponPoolZmd
WEAP_POOL_1_ZMD = WeaponPoolZmd("weapon_1")
WEAP_POOL_2_ZMD = WeaponPoolZmd("weapon_2")
WEAP_POOL_3_ZMD = WeaponPoolZmd("weapon_3")
WEAP_POOL_4_ZMD = WeaponPoolZmd("weapon_4")
WEAP_POOL_5_ZMD = WeaponPoolZmd("weapon_5")
WEAP_POOL_6_ZMD = WeaponPoolZmd("weapon_6")
WEAP_POOL_7_ZMD = WeaponPoolZmd("weapon_7")
WEAP_POOL_8_ZMD = WeaponPoolZmd("weapon_8")

# 版本卡池一览
POOL_LIST_ZMD = [
    (CHAR_POOL_1_ZMD, WEAP_POOL_1_ZMD),
    (CHAR_POOL_2_ZMD, WEAP_POOL_2_ZMD),
    (CHAR_POOL_3_ZMD, WEAP_POOL_3_ZMD),
    (CHAR_POOL_4_ZMD, WEAP_POOL_4_ZMD),
    (CHAR_POOL_5_ZMD, WEAP_POOL_5_ZMD),
    (CHAR_POOL_6_ZMD, WEAP_POOL_6_ZMD),
    (CHAR_POOL_7_ZMD, WEAP_POOL_7_ZMD),
    (CHAR_POOL_8_ZMD, WEAP_POOL_8_ZMD)
]

def print_result_no_of_targets(results: list, title: str):
    print("-" * 80)
    # 目标角色集合
    TARGET_SET = {p[0].target_char_code for p in POOL_LIST_ZMD}
    WEAPON_SET = {p[1].target_weapon_code for p in POOL_LIST_ZMD}

    # 对每个场景统计获得了多少个独特目标角色
    # 处理旧格式（集合）和新格式（集合和字典的元组）
    if isinstance(results[0], tuple):
        targets_count_1 = [len(TARGET_SET.intersection(set(scenario[0]))) for scenario in results]
        weapons_count = [sum(1 for w in WEAPON_SET if scenario[1].get(w, 0) > 0) for scenario in results]
    else:
        targets_count_1 = [len(TARGET_SET.intersection(set(scenario))) for scenario in results]
        weapons_count = None
    
    avg_targets = sum(targets_count_1) / len(targets_count_1)
    median_targets = statistics.median(targets_count_1)
    pct_avg_1 = (avg_targets / len(TARGET_SET)) * 100
    print("当前模拟开服{}抽角色，{}抽武器，每版本{}抽角色，{}抽武器".format(
        BASIC_BALANCE_CHAR, BASIC_BALANCE_WEAP, RELEASE_BALANCE_CHAR, RELEASE_BALANCE_WEAP))
    print(f"Average target characters obtained: {avg_targets:.2f} / {len(TARGET_SET)} ({pct_avg_1:.1f}%)")
    print(f"Median target characters obtained: {median_targets:.2f}")
    
    if weapons_count is not None:
        avg_weapons = sum(weapons_count) / len(weapons_count)
        median_weapons = statistics.median(weapons_count)
        pct_avg_weapons = (avg_weapons / len(WEAPON_SET)) * 100
        print(f"Average target weapons obtained: {avg_weapons:.2f} / {len(WEAPON_SET)} ({pct_avg_weapons:.1f}%)")
        print(f"Median target weapons obtained: {median_weapons:.2f}")
    
    dist1 = collections.Counter(targets_count_1)
    print("Distribution of number of target characters obtained:")
    for k in range(0, len(TARGET_SET) + 1):
        freq = dist1.get(k, 0)
        pct = freq / len(targets_count_1) * 100
        bar = "█" * int(pct / 2)
        print(f"{k:2d} targets: {freq:4d} scenarios ({pct:5.1f}%) {bar}")

    if MATPLOTLIB_AVAILABLE:
        plt.figure(figsize=(8,4))
        items = sorted(dist1.items())
        xs = [k for k,_ in items]
        ys = [v for _,v in items]
        bars = plt.bar(xs, ys)

        total = len(targets_count_1)
        # 在每个柱状图上添加百分比标签（>= 1%）
        for x, y in zip(xs, ys):
            pct = (y / total) * 100
            if pct >= 1:
                plt.text(x, y, f"{pct:.1f}%", ha='center', va='bottom')

        plt.xlabel('Number of target characters obtained')
        plt.ylabel('Number of scenarios')
        plt.title(f'{title} - Characters')
        plt.tight_layout()
        plt.savefig(f'{title.replace(" ", "_")+"_characters.png"}')
        print(f'Saved plot: {title.replace(" ", "_")+"_characters.png"}')
        
        # 如果有武器数据，也生成武器分布图
        if weapons_count is not None:
            plt.figure(figsize=(8,4))
            weapon_dist = collections.Counter(weapons_count)
            items_w = sorted(weapon_dist.items())
            xs_w = [k for k,_ in items_w]
            ys_w = [v for _,v in items_w]
            bars_w = plt.bar(xs_w, ys_w, color='orange')
            
            total_w = len(weapons_count)
            # 在每个柱状图上添加百分比标签（>= 1%）
            for x, y in zip(xs_w, ys_w):
                pct = (y / total_w) * 100
                if pct >= 1:
                    plt.text(x, y, f"{pct:.1f}%", ha='center', va='bottom')
            
            plt.xlabel('Number of target weapons obtained')
            plt.ylabel('Number of scenarios')
            plt.title(f'{title} - Weapons')
            plt.tight_layout()
            plt.savefig(f'{title.replace(" ", "_")+"_weapons.png"}')
            print(f'Saved plot: {title.replace(" ", "_")+"_weapons.png"}')

    print()


def print_result_no_of_topups(results: list, title:str):
    print("-" * 80)
    
    # 处理元组结果（角色充值，武器充值）
    if isinstance(results[0], tuple):
        char_topups = [r[0] for r in results]
        weap_topups = [r[1] for r in results]
        
        avg_char_topups = sum(char_topups) / len(char_topups)
        median_char_topups = statistics.median(char_topups)
        ok_char_topups = statistics.quantiles(char_topups, n=100)[79]
        
        avg_weap_topups = sum(weap_topups) / len(weap_topups)
        median_weap_topups = statistics.median(weap_topups)
        ok_weap_topups = statistics.quantiles(weap_topups, n=100)[79]
        print("当前模拟开服{}抽角色，{}抽武器，每版本{}抽角色，{}抽武器".format(
            BASIC_BALANCE_CHAR, BASIC_BALANCE_WEAP, RELEASE_BALANCE_CHAR, RELEASE_BALANCE_WEAP))
        print(f"Average character topups needed: {avg_char_topups:.2f}")
        print(f"Median character topups needed: {median_char_topups:.2f}")
        print(f"80% people top up less than (char): {ok_char_topups:.2f}")
        print()
        print(f"Average weapon topups needed: {avg_weap_topups:.2f}")
        print(f"Median weapon topups needed: {median_weap_topups:.2f}")
        print(f"80% people top up less than (weap): {ok_weap_topups:.2f}")
        
        topup_dist = collections.Counter(char_topups)
        print("\nCharacter topup distribution:")
    else:
        avg_topups = sum(results) / len(results)
        median_topups = statistics.median(results)
        ok_targets = statistics.quantiles(results, n=100)[79]
        print(f"Average topups needed to get all targets: {avg_topups:.2f}")
        print(f"Median topups needed to get all targets: {median_topups:.2f}")
        print(f"80% people top up less than: {ok_targets:.2f}")
        topup_dist = collections.Counter(results)
        print("Topup distribution:")
    for topup_count in sorted(topup_dist.keys()):
        freq = topup_dist[topup_count]
        pct = (freq / len(results) if not isinstance(results[0], tuple) else freq / len(char_topups)) * 100
        bar = "█" * int(pct / 2)
        if pct > 1:
            print(f"{topup_count:2d} topups: {freq:4d} scenarios ({pct:5.1f}%) {bar}")
    
    # 如果可用，展示武器充值分布
    if isinstance(results[0], tuple):
        weap_topup_dist = collections.Counter(weap_topups)
        print("\nWeapon topup distribution:")
        for topup_count in sorted(weap_topup_dist.keys()):
            freq = weap_topup_dist[topup_count]
            pct = (freq / len(weap_topups)) * 100
            bar = "█" * int(pct / 2)
            if pct > 1:
                print(f"{topup_count:2d} topups: {freq:4d} scenarios ({pct:5.1f}%) {bar}")

    if MATPLOTLIB_AVAILABLE:
        # 角色充值分布图
        plt.figure(figsize=(8,4))
        xs = sorted(topup_dist.keys())
        ys = [topup_dist[x] for x in xs]
        bars = plt.bar(xs, ys, color='green')

        total = len(results) if not isinstance(results[0], tuple) else len(char_topups)
        # 在每个柱状图上添加百分比标签（>= 3%）
        for x, y in zip(xs, ys):
            pct = (y / total) * 100
            if pct >= 3:
                plt.text(x, y, f"{pct:.1f}%", ha='center', va='bottom')

        plt.xlabel('Character Topups')
        plt.ylabel('Number of scenarios')
        plt.title(f'{title} - Characters' if isinstance(results[0], tuple) else title)
        plt.tight_layout()
        filename_suffix = "_characters" if isinstance(results[0], tuple) else ""
        plt.savefig(f'{title.replace(" ", "_")+filename_suffix+".png"}')
        print(f'Saved plot: {title.replace(" ", "_")+filename_suffix+".png"}')
        
        # 如果有武器充值数据，生成武器充值分布图
        if isinstance(results[0], tuple):
            plt.figure(figsize=(8,4))
            weap_xs = sorted(weap_topup_dist.keys())
            weap_ys = [weap_topup_dist[x] for x in weap_xs]
            bars_w = plt.bar(weap_xs, weap_ys, color='orange')
            
            total_w = len(weap_topups)
            # 在每个柱状图上添加百分比标签（>= 3%）
            for x, y in zip(weap_xs, weap_ys):
                pct = (y / total_w) * 100
                if pct >= 3:
                    plt.text(x, y, f"{pct:.1f}%", ha='center', va='bottom')
            
            plt.xlabel('Weapon Topups')
            plt.ylabel('Number of scenarios')
            plt.title(f'{title} - Weapons')
            plt.tight_layout()
            plt.savefig(f'{title.replace(" ", "_")+"_weapons.png"}')
            print(f'Saved plot: {title.replace(" ", "_")+"_weapons.png"}')


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Running character and weapon pull simulations...")
    print("="*80 + "\n")
    
    zmd_result_1 = zmd_pool.pull_only_when_have_80_pulls_till_get_target_no_topup(
        100000, BASIC_BALANCE_CHAR, RELEASE_BALANCE_CHAR, POOL_LIST_ZMD, 
        BASIC_BALANCE_WEAP, RELEASE_BALANCE_WEAP)
    print_result_no_of_targets(zmd_result_1, "Test 1 ZMD xiao pao pai")
    
    zmd_result_2 = zmd_pool.pull_only_when_have_120_pulls_till_get_target_no_topup(
        100000, BASIC_BALANCE_CHAR, RELEASE_BALANCE_CHAR, POOL_LIST_ZMD,
        BASIC_BALANCE_WEAP, RELEASE_BALANCE_WEAP)
    print_result_no_of_targets(zmd_result_2, "Test 2 ZMD da bao pai")
    
    zmd_result_3 = zmd_pool.pull_for_each_target_with_topup(
        100000, BASIC_BALANCE_CHAR, RELEASE_BALANCE_CHAR, POOL_LIST_ZMD,
        BASIC_BALANCE_WEAP, RELEASE_BALANCE_WEAP)
    print_result_no_of_topups(zmd_result_3, "Test 3 ZMD 0+1 topup")

    
    

