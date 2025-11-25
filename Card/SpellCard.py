from BaseCard import *
from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import List, Optional, Any


class SpellCard(BaseCard):
    def __init__(self, card_id: str, name: str, cost: int, **kwargs):
        super().__init__(card_id, name, cost, **kwargs, card_type=CardType.SPELL)

    def play(self, target: Optional[BaseCard] = None):
        print(f"施放法术: {self.name}")
        self.cast_effect(target)
        # 施放后进入墓地

    @abstractmethod
    def cast_effect(self, target):
        """具体的法术效果"""
        pass