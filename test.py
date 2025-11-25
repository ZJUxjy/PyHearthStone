from Card.MinionCard import MinionCard
from Card.SpellCard import SpellCard
from Card.BaseCard import *
from CardManager.HandleManager import *


# --- 实现具体的卡牌逻辑 ---

class Fireball(SpellCard):
    def __init__(self):
        super().__init__(
            card_id="CS2_029", 
            name="Fireball", 
            cost=4, 
            description="Deal 6 damage.", 
            rarity=Rarity.FREE,
            target_type=TargetType.ANY_TARGET
        )

    def cast_effect(self, target):
        if target and hasattr(target, 'take_damage'):
            print(f"火球术击中了 {target.name}！")
            target.take_damage(6)
        else:
            print("无效的目标！")
            

class RiverCrocolisk(MinionCard):
    def __init__(self):
        super().__init__(
            card_id="CS2_120",
            name="River Crocolisk",
            cost=2,
            attack=2,
            health=3,
            race=Race.BEAST,
            description="Wait for text",
            rarity=Rarity.FREE
        )

# --- 模拟游戏流程 ---

# 1. 实例化卡牌
my_fireball = Fireball()
enemy_croc = RiverCrocolisk()

# 2. 打印状态
print(f"手牌: {my_fireball}") 
print(f"手牌: {enemy_croc}")

# 3. 敌人打出淡水鳄
enemy_croc.play()

# 4. 玩家使用火球术攻击淡水鳄
# 检查费用 (简单模拟)
current_mana = 4
if current_mana >= my_fireball.cost:
    my_fireball.play(target=enemy_croc)


# 模拟两张完全一样的"火球术"
fireball_1 = Fireball()
fireball_2 = Fireball()
rivercrocolisk_1 = RiverCrocolisk()
rivercrocolisk_2 = RiverCrocolisk()
rivercrocolisk_3 = RiverCrocolisk()
rivercrocolisk_4 = RiverCrocolisk()

# 初始化手牌
my_hand = HandManager()

# 1. 添加卡牌 (包含重复卡)
my_hand.add_card(fireball_1)
my_hand.add_card(fireball_2)
my_hand.add_card(rivercrocolisk_1)
my_hand.add_card(rivercrocolisk_2)
my_hand.add_card(rivercrocolisk_3)
my_hand.add_card(rivercrocolisk_4)

print(f"当前手牌: {my_hand}")
# 输出: Hand(2/10): [<Fireball (ID:CS2_029) [a1b2]>, <Fireball (ID:CS2_029) [c3d4]>]
# 注意：虽然名字ID一样，但UUID后缀不同

# 2. 数组特性：获取最左边的一张牌 (用于UI渲染)
left_card = my_hand[0] 
print(f"最左边的卡: {left_card.uuid}")

# 3. 字典特性：服务器发来指令，说 ID 为 'c3d4...' 的卡被使用了
# 假设我们只知道 uuid
target_uuid = fireball_2.uuid
card_from_dict = my_hand[target_uuid]
print(f"通过UUID找到的卡: {card_from_dict.uuid}")

# 4. 遍历特性
print("遍历手牌:")
for card in my_hand:
    print(f" - {card.name}")

# 5. 智能移除
# 玩家拖动了第2张牌打出 (按位置移除)
played_card = my_hand.remove_card(1) 
# 或者 my_hand.remove_card(fireball_2.uuid)
print(f"打出了: {played_card}")
print(f"剩余手牌: {my_hand}")