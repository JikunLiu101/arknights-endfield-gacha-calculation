
import collections
import random
import collections, statistics
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False
from zmd_pool import CharacterPoolZmd
import zmd_pool
from gs_pool import CharacterPoolGs
import gs_pool

    
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

POOL_1_ZMD = CharacterPoolZmd(TARGET_CHAR_1, TARGET_CHAR_2, TARGET_CHAR_3, NORMAL_CHAR_CODES)
POOL_2_ZMD = CharacterPoolZmd(TARGET_CHAR_2, TARGET_CHAR_1, TARGET_CHAR_3, NORMAL_CHAR_CODES)
POOL_3_ZMD = CharacterPoolZmd(TARGET_CHAR_3, TARGET_CHAR_1, TARGET_CHAR_2, NORMAL_CHAR_CODES)
POOL_4_ZMD = CharacterPoolZmd(TARGET_CHAR_4, TARGET_CHAR_3, TARGET_CHAR_2, NORMAL_CHAR_CODES)
POOL_5_ZMD = CharacterPoolZmd(TARGET_CHAR_5, TARGET_CHAR_4, TARGET_CHAR_3, NORMAL_CHAR_CODES)
POOL_6_ZMD = CharacterPoolZmd(TARGET_CHAR_6, TARGET_CHAR_5, TARGET_CHAR_4, NORMAL_CHAR_CODES)
POOL_7_ZMD = CharacterPoolZmd(TARGET_CHAR_7, TARGET_CHAR_6, TARGET_CHAR_5, NORMAL_CHAR_CODES)
POOL_8_ZMD = CharacterPoolZmd(TARGET_CHAR_8, TARGET_CHAR_7, TARGET_CHAR_6, NORMAL_CHAR_CODES)
POOL_LIST_ZMD = [POOL_1_ZMD, POOL_2_ZMD, POOL_3_ZMD, POOL_4_ZMD, POOL_5_ZMD, POOL_6_ZMD, POOL_7_ZMD, POOL_8_ZMD]

POOL_1_GS = CharacterPoolGs(TARGET_CHAR_1, TARGET_CHAR_2, TARGET_CHAR_3, NORMAL_CHAR_CODES)
POOL_2_GS = CharacterPoolGs(TARGET_CHAR_2, TARGET_CHAR_1, TARGET_CHAR_3, NORMAL_CHAR_CODES)
POOL_3_GS = CharacterPoolGs(TARGET_CHAR_3, TARGET_CHAR_1, TARGET_CHAR_2, NORMAL_CHAR_CODES)
POOL_4_GS = CharacterPoolGs(TARGET_CHAR_4, TARGET_CHAR_3, TARGET_CHAR_2, NORMAL_CHAR_CODES)
POOL_5_GS = CharacterPoolGs(TARGET_CHAR_5, TARGET_CHAR_4, TARGET_CHAR_3, NORMAL_CHAR_CODES)
POOL_6_GS = CharacterPoolGs(TARGET_CHAR_6, TARGET_CHAR_5, TARGET_CHAR_4, NORMAL_CHAR_CODES)
POOL_7_GS = CharacterPoolGs(TARGET_CHAR_7, TARGET_CHAR_6, TARGET_CHAR_5, NORMAL_CHAR_CODES)
POOL_8_GS = CharacterPoolGs(TARGET_CHAR_8, TARGET_CHAR_7, TARGET_CHAR_6, NORMAL_CHAR_CODES)
POOL_LIST_GS = [POOL_1_GS, POOL_2_GS, POOL_3_GS, POOL_4_GS, POOL_5_GS, POOL_6_GS, POOL_7_GS, POOL_8_GS]


def print_result_no_of_targets(results: list, title: str):
    print("-" * 80)
    # Targets set
    TARGET_SET = {p.target_char_code for p in POOL_LIST_ZMD}

    # For each scenario count how many unique targets were obtained
    targets_count_1 = [len(TARGET_SET.intersection(set(scenario))) for scenario in results]
    avg_targets = sum(targets_count_1) / len(targets_count_1)
    median_targets = statistics.median(targets_count_1)
    pct_avg_1 = (avg_targets / len(TARGET_SET)) * 100
    print(f"Average targets obtained: {avg_targets:.2f} / {len(TARGET_SET)} ({pct_avg_1:.1f}%)")
    print(f"Median targets obtained: {median_targets:.2f}")
    dist1 = collections.Counter(targets_count_1)
    print("Distribution of number of targets obtained (Test 1):")
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
        # Add percentage labels on each bar (>= 5%)
        for x, y in zip(xs, ys):
            pct = (y / total) * 100
            if pct >= 1:
                plt.text(x, y, f"{pct:.1f}%", ha='center', va='bottom')

        plt.xlabel('Number of targets obtained')
        plt.ylabel('Number of scenarios')
        plt.title(f'{title}')
        plt.tight_layout()
        plt.savefig(f'{title.replace(" ", "_")+".png"}')
        print(f'Saved plot: {title.replace(" ", "_")+".png"}')


    print()


def print_result_no_of_topups(results: list, title:str):
    print("-" * 80)
    avg_topups = sum(results) / len(results)
    median_topups = statistics.median(results)
    ok_targets = statistics.quantiles(results, n=100)[79]
    print(f"Average topups needed to get all targets: {avg_topups:.2f}")
    print(f"Median topups needed to get all targets: {median_topups:.2f}")
    print(f"80% people top up less than: {ok_targets:.2f}")
    topup_dist = collections.Counter(results)
    print("Topup distribution (Test 3):")
    for topup_count in sorted(topup_dist.keys()):
        freq = topup_dist[topup_count]
        pct = (freq / len(results)) * 100
        bar = "█" * int(pct / 2)
        if pct > 1:
            print(f"{topup_count:2d} topups: {freq:4d} scenarios ({pct:5.1f}%) {bar}") 

    if MATPLOTLIB_AVAILABLE:
        plt.figure(figsize=(8,4))
        xs = sorted(topup_dist.keys())
        ys = [topup_dist[x] for x in xs]
        bars = plt.bar(xs, ys, color='green')

        total = len(results)
        # Add percentage labels on each bar (>= 5%)
        for x, y in zip(xs, ys):
            pct = (y / total) * 100
            if pct >= 3:
                plt.text(x, y, f"{pct:.1f}%", ha='center', va='bottom')

        plt.xlabel('Topups')
        plt.ylabel('Number of scenarios')
        plt.title(f'{title}')
        plt.tight_layout()
        plt.savefig(f'{title.replace(" ", "_")+".png"}')
        print(f'Saved plot: {title.replace(" ", "_")+".png"}')


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Running character pull simulations...")
    print("="*80 + "\n")
    
    #Endfield pool: 40 basic balance, 70 release balance -> 开服110抽，后续每版本70抽
    zmd_result_1 = zmd_pool.pull_only_when_have_80_pulls_till_get_target_no_topup(100000, 40, 70, POOL_LIST_ZMD)
    print_result_no_of_targets(zmd_result_1, "Test 1 xiao bao pai")
    zmd_result_2 = zmd_pool.pull_only_when_have_120_pulls_till_get_target_no_topup(100000, 40, 70, POOL_LIST_ZMD)
    print_result_no_of_targets(zmd_result_2, "Test 2 da bao pai")
    zmd_result_3 = zmd_pool.pull_for_each_target_char_with_topup(100000, 40, 70, POOL_LIST_ZMD)
    print_result_no_of_topups(zmd_result_3, "Test 3 quan tu jian dang")

    # Gacha Standard pool: 40 basic, 70 release balance -> 开服110抽，后续每版本70抽
    gs_result_1 = gs_pool.pull_for_each_pool_till_get_target_no_topup(100000, 40, 70, POOL_LIST_GS)
    print_result_no_of_targets(gs_result_1, "Test 4 dian chi zi")
    gs_result_2 = gs_pool.pull_only_when_have_90_pulls_till_get_target_no_topup(100000, 40, 70, POOL_LIST_GS)    
    print_result_no_of_targets(gs_result_2, "Test 5 xiao bao pai")
    gs_result_3 = gs_pool.pull_for_each_target_char_with_topup(100000, 40, 70, POOL_LIST_GS)
    print_result_no_of_topups(gs_result_3, "Test 6 quan tu jian dang")

    
    

