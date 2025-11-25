from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import List, Optional, Any
import uuid

# 1. 卡牌类型
class CardType(Enum):
    MINION = auto()  # 随从
    SPELL = auto()   # 法术
    WEAPON = auto()  # 武器
    HERO = auto()    # 英雄牌

# 2. 稀有度
class Rarity(Enum):
    FREE = auto()
    COMMON = auto()
    RARE = auto()
    EPIC = auto()
    LEGENDARY = auto()

# 3. 种族 (针对随从)
class Race(Enum):
    NONE = auto()
    BEAST = auto()
    MURLOC = auto()
    DRAGON = auto()
    # ... 其他种族

# 4. 目标类型 (决定卡牌打出时是否需要选定目标)
class TargetType(Enum):
    NONE = auto()             # 不需要目标 (如：奥术智慧)
    ANY_TARGET = auto()       # 任意目标 (如：火球术)
    FRIENDLY_MINION = auto()  # 友方随从
    ENEMY_MINION = auto()     # 敌方随从

class BaseCard(ABC):
    def __init__(self, card_id: str, name: str, cost: int, 
                 rarity: Rarity, card_type: CardType, description: str='',
                 target_type: TargetType = TargetType.NONE):
        # --- 静态数据 (来自数据库/JSON) ---
        self.card_id = card_id
        self.name = name
        self.description = description
        self.rarity = rarity
        self.card_type = card_type
        self.target_type = target_type
        self.uuid = str(uuid.uuid4())
        
        # --- 动态状态 (游戏中会改变的数据) ---
        self._base_cost = cost      # 原始费用
        self._current_cost = cost   # 当前费用 (可能被修改)
        self.owner = None           # 所属玩家 (Player对象)
        self.zone = None            # 当前区域 (手牌/牌库/战场/墓地)

    def __repr__(self):
        # 打印时显示 uuid 的前5位以便区分
        return f"<{self.name} (ID:{self.card_id}) [{self.uuid[:5]}]>"
    @property
    def cost(self) -> int:
        """获取当前费用，确保不小于0"""
        return max(0, self._current_cost)

    @cost.setter
    def cost(self, value: int):
        self._current_cost = value

    def modify_cost(self, amount: int):
        """修改费用的通用方法 (例如：索瑞森大帝 -1)"""
        self._current_cost += amount

    # --- 核心抽象方法 (子类必须实现) ---
    
    @abstractmethod
    def play(self, target: Optional['BaseCard'] = None):
        """
        battlecry
        打出卡牌时的逻辑入口。
        target: 选定的目标 (如果是随从或英雄)
        """
        pass

    # --- 生命周期钩子 (Hooks) ---
    # 这些方法默认为空，具体卡牌可以通过重写来实现特效
    
    def on_draw(self):
        """当抽到这张牌时触发 (如：炸弹)"""
        pass

    def on_turn_start(self):
        """回合开始时触发"""
        pass

    def on_turn_end(self):
        """回合结束时触发"""
        pass

    def __str__(self):
        return f"[{self.name}] (Cost: {self.cost})"
