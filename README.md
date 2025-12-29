# Arknights: Endfield Gacha Calculation / 明日方舟：终末地抽卡模拟计算

[English](#english) | [中文](#中文)

---

## English

### Overview

This project simulates different gacha (pulling) strategies for **Arknights: Endfield**, calculating the expected number of characters and weapons obtainable under various resource constraints and pulling strategies.

### Features

- **Character Pool Simulation**: Simulates the 6-star character gacha with soft pity (65 pulls) and hard pity (80 pulls)
- **Weapon Pool Simulation**: Simulates the weapon gacha with 10-pull claims and pity systems (4 claims for 6-star, 8 claims for rate-up)
- **Multiple Strategies**: 
  - Small pity strategy (pull when having 80 pulls)
  - Large pity strategy (pull when having 120 pulls)
  - Full collection strategy (top-up to get all rate-up characters and weapons)
- **Resource Conversion**: Automatically calculates weapon pool resources gained from character pulls (0.02 per pull, 1 per 6-star)
- **Statistical Analysis**: Provides average, median, and distribution of results across 100,000 simulations
- **Visualization**: Generates separate distribution charts for characters (blue) and weapons (orange) using matplotlib (optional)

### Gacha Mechanics (ZMD Pool)

#### Character Pool
- **Base Rate**: 0.8% for 6-star
- **Rate-up Probability**: 50% chance for the featured character when pulling a 6-star
- **Soft Pity**: Starting from pull 65, rate increases by 5% per pull
- **Hard Pity**: Guaranteed 6-star at pull 80
- **Super Pity**: Guaranteed rate-up character at pull 120 (accumulator)

#### Weapon Pool
- **Base Rate**: 4% for 6-star weapon
- **Rate-up Probability**: 25% chance for the featured weapon when pulling a 6-star
- **10-pull Claim**: Each weapon pull consumes 1 claim (equivalent to 10 pulls)
- **Pity 1**: Guaranteed 6-star weapon after 4 claims (40 pulls)
- **Pity 2**: Guaranteed rate-up weapon after 8 claims (80 pulls)

#### Resource Conversion
- **1 Character Pull** → 0.02 Weapon Claims (more accurate than 10 pulls → 0.2)
- **1 Six-Star Character** → 1 Weapon Claim

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/arknights-endfield-gacha-calculation.git
cd arknights-endfield-gacha-calculation

# Install dependencies (optional, for visualization)
pip install matplotlib
```

### Usage

#### Quick Start

Run the simulation with default parameters:

```bash
python main.py
```

#### Customize Parameters

Edit the values at the top of `main.py`:

```python
BASIC_BALANCE_CHAR = 123    # Initial character pool pulls (opening balance) minus RELEASE_BALANCE_WEAP in 1st version
RELEASE_BALANCE_CHAR = 53   # [Mock] Character pulls per version
BASIC_BALANCE_WEAP = 2      # [Mock] Initial weapon pool claims minus RELEASE_BALANCE_WEAP in 1st version (1 claim = 10 pulls)
RELEASE_BALANCE_WEAP = 2   # Weapon claims per version
```

#### Strategies Tested

1. **Test 1 - Small Pity Strategy**: Only pull when having at least 80 character pulls
2. **Test 2 - Large Pity Strategy**: Only pull when having at least 120 character pulls
3. **Test 3 - Full Collection Strategy**: Top-up as needed to get all rate-up characters and weapons

### File Structure

```
├── main.py           # Main simulation runner and result display
├── zmd_pool.py       # ZMD (Endfield) pool implementation
├── gs_pool.py        # GS (Gacha Standard) pool implementation
├── CHANGELOG.md      # Update history
└── README.md         # This file
```

### Example Output

```
当前模拟开服121抽角色，2抽武器，每版本55抽角色，2抽武器
Average target characters obtained: 6.53 / 8 (81.7%)
Median target characters obtained: 7.00
Average target weapons obtained: 3.97 / 8 (49.6%)
Median target weapons obtained: 4.00
Distribution of number of target characters obtained:
 0 targets:    0 scenarios (  0.0%)
 1 targets:    0 scenarios (  0.0%)
 2 targets:    2 scenarios (  0.0%)
 3 targets:  343 scenarios (  0.3%)
 4 targets: 2677 scenarios (  2.7%) █
 5 targets: 13243 scenarios ( 13.2%) ██████
 6 targets: 30290 scenarios ( 30.3%) ███████████████
 7 targets: 33863 scenarios ( 33.9%) ████████████████
 8 targets: 19582 scenarios ( 19.6%) █████████

Saved plot: Test_2_ZMD_大保派_characters.png
Saved plot: Test_2_ZMD_大保派_weapons.png
```

**Visualization**: The simulation automatically generates distribution charts for both characters and weapons when matplotlib is available.

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

This project is for educational and research purposes only.

---

## 中文

### 项目简介

本项目模拟**明日方舟：终末地**的不同抽卡策略，计算在不同资源约束和抽卡策略下可以获得的角色和武器数量。

### 功能特点

- **角色池模拟**：模拟6星角色抽取，包含软保底（65抽）和硬保底（80抽）机制
- **武器池模拟**：模拟武器抽取，包含10连申领和保底机制（4次申领出6星，8次申领出Up）
- **多种策略**：
  - 小保派策略（有80抽才抽）
  - 大保派策略（有120抽才抽）
  - 全图鉴党策略（充值获取所有Up角色和武器）
- **资源转换**：自动计算角色池抽取获得的武器池资源（每1抽0.02次申领，每个6星1次申领）
- **统计分析**：提供10万次模拟的平均值、中位数和分布情况
- **可视化图表**：使用matplotlib生成角色分布图（蓝色）和武器分布图（橙色）（可选）

### 抽卡机制（终末地卡池）

#### 角色池
- **基础概率**：6星基础概率0.8%
- **Up概率**：抽到6星时，50%概率为当期Up角色
- **软保底**：从第65抽开始，每抽提升5%概率
- **硬保底**：第80抽必出6星
- **大保底**：第120抽必出Up角色（累积井）

#### 武器池
- **基础概率**：6星武器基础概率4%
- **Up概率**：抽到6星武器时，25%概率为当期Up武器
- **10连申领**：每次申领消耗1次机会（相当于10连）
- **保底1**：4次申领必出6星武器（40抽）
- **保底2**：8次申领必出Up武器（80抽）

#### 资源转换规则
- **1抽角色池** → 0.02次武器申领（比10抽0.2更精确）
- **1个6星角色** → 1次武器申领

### 安装方法

```bash
# 克隆仓库
git clone https://github.com/yourusername/arknights-endfield-gacha-calculation.git
cd arknights-endfield-gacha-calculation

# 安装依赖（可选，用于生成图表）
pip install matplotlib
```

### 使用方法

#### 快速开始

使用默认参数运行模拟：

```bash
python main.py
```

#### 自定义参数

编辑 `main.py` 顶部的参数值：

```python
BASIC_BALANCE_CHAR = 123    # 开服初始角色池抽数，176，数据来源@让你爱上学习，减去下面模拟的版本福利53，
RELEASE_BALANCE_CHAR = 53   # 【模拟】每版本获得的角色池抽数，参考数据：0氪无活动18抽，小月卡+20抽，大月卡+5抽，即无活动大小月卡玩家43抽，数据来源@叫我棉被，【模拟】活动+10抽。即0氪28抽，大小月卡53抽
BASIC_BALANCE_WEAP = 2      # 【模拟】开服初始武器池申领次数（注意是申领次数而不是抽数！！！），减去版本福利
RELEASE_BALANCE_WEAP = 2    # 每版本获得的武器池申领次数，无大小月卡则此处减去1.2抽
```

#### 测试策略说明

1. **测试1 - 小保派策略**：手里至少有80抽角色池才开始抽
2. **测试2 - 大保派策略**：手里至少有120抽角色池才开始抽
3. **测试3 - 全图鉴党策略**：充值以获得所有Up角色和武器

### 文件结构

```
├── main.py           # 主程序：模拟运行和结果展示
├── zmd_pool.py       # 终末地卡池实现
├── gs_pool.py        # 标准抽卡池实现
├── CHANGELOG.md      # 更新日志
└── README.md         # 本文件
```

### 示例输出

```
当前模拟开服121抽角色，2抽武器，每版本55抽角色，2抽武器
Average target characters obtained: 6.53 / 8 (81.7%)
Median target characters obtained: 7.00
Average target weapons obtained: 3.97 / 8 (49.6%)
Median target weapons obtained: 4.00
Distribution of number of target characters obtained:
 0 targets:    0 scenarios (  0.0%)
 1 targets:    0 scenarios (  0.0%)
 2 targets:    2 scenarios (  0.0%)
 3 targets:  343 scenarios (  0.3%)
 4 targets: 2677 scenarios (  2.7%) █
 5 targets: 13243 scenarios ( 13.2%) ██████
 6 targets: 30290 scenarios ( 30.3%) ███████████████
 7 targets: 33863 scenarios ( 33.9%) ████████████████
 8 targets: 19582 scenarios ( 19.6%) █████████

Saved plot: Test_2_ZMD_大保派_characters.png
Saved plot: Test_2_ZMD_大保派_weapons.png
```

**可视化图表**：当安装了matplotlib时，模拟会自动生成角色和武器的分布柱状图，橙色柱状图表示武器获取分布。

### 参与贡献

欢迎提交 Pull Request 来改进项目！

### 开源协议

本项目仅用于教育和研究目的。

### 数据来源

- 角色池初始余额数据参考：让你爱上学习@B站
- 其他参数为模拟数据，可根据实际情况调整

### 常见问题

**Q: 为什么武器池用"申领"而不是"抽"？**  
A: 根据游戏机制，武器池每次申领相当于10连抽取，这是游戏的特殊设计。

**Q: 可以修改版本数量吗？**  
A: 可以，在 `main.py` 中修改 `POOL_LIST_ZMD` 的长度，添加或减少池子即可。

**Q: 运行需要多长时间？**  
A: 10万次模拟通常需要30秒到2分钟，取决于你的电脑性能。

**Q: 如何理解"小保底"和"大保底"？**  
A: 
- **小保底**：80抽必出6星角色
- **大保底**：120抽必出Up角色（歪了也能保底）

### 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。

---

**免责声明**: 本项目为独立开发的模拟工具，与游戏官方无关。所有概率和机制基于公开信息和社区研究，可能与实际游戏存在差异。
