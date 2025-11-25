from BaseCard import *
from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import List, Optional, Any


class MinionCard(BaseCard):
    def __init__(
        self,
        card_id: str,
        name: str,
        cost: int,
        attack: int,
        health: int,
        race: Race = Race.NONE,
        **kwargs,
    ):
        super().__init__(card_id, name, cost, **kwargs, card_type=CardType.MINION)

        # 基础属性
        self._base_attack = attack
        self._base_health = health
        self.race = race

        # 动态属性
        self.current_attack = attack
        self.current_health = health
        self.max_health = health

        # 状态标签 (可以通过位运算优化，这里为了可读性用集合)
        self.mechanics = set()  # {'TAUNT', 'DIVINE_SHIELD', 'RUSH'}

        # 状态标记
        self.is_frozen = False
        self.can_attack = False  # 刚下场通常不能攻击(除非冲锋)

    def play(self, target: Optional[BaseCard] = None):
        print(f"随从 {self.name} 进入战场！")
        # 触发战吼 (Battlecry) 逻辑，如果有的话
        self.battlecry(target)
        # 通知游戏管理器：召唤随从
        # game_manager.summon_minion(self)

    def battlecry(self, target):
        """默认为空，特定随从重写此方法"""
        pass

    def take_damage(self, amount: int):
        if "DIVINE_SHIELD" in self.mechanics:
            self.mechanics.remove("DIVINE_SHIELD")
            print(f"{self.name} 的圣盾抵挡了伤害！")
            return

        self.current_health -= amount
        print(f"{self.name} 受到 {amount} 点伤害，剩余生命: {self.current_health}")
        if self.current_health <= 0:
            self.die()

    def die(self):
        print(f"{self.name} 死亡！")
        self.deathrattle()
        # game_manager.remove_minion(self)

    def deathrattle(self):
        """亡语接口"""
        pass
