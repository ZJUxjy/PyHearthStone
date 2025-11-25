import os


from typing import List, Dict, Union, Optional
from Card.BaseCard import *
from Card.SpellCard import *
from Card.MinionCard import *
class HandManager:
    def __init__(self, max_hand_size: int = 10):
        self.max_hand_size = max_hand_size
        
        # 1. 列表：保证顺序 (UI渲染从左到右)
        self._cards_list: List[BaseCard] = []
        
        # 2. 字典：保证查找速度 (Key 是 uuid)
        self._cards_map: Dict[str, BaseCard] = {}

    def add_card(self, card: BaseCard) -> bool:
        """添加卡牌到手牌（通常添加到最右侧）"""
        if len(self._cards_list) >= self.max_hand_size:
            print("手牌已满，卡牌被爆掉！")
            return False
        
        # 双向绑定
        self._cards_list.append(card)
        self._cards_map[card.uuid] = card
        card.zone = "HAND" # 假设卡牌有 zone 属性
        return True

    def remove_card(self, identifier: Union[int, str, BaseCard]) -> Optional[BaseCard]:
        """
        移除卡牌，支持传入：索引、UUID字符串、或卡牌对象本身
        """
        card_to_remove = None

        # 情况 A: 传入的是卡牌对象
        if isinstance(identifier, BaseCard):
            card_to_remove = identifier
            
        # 情况 B: 传入的是 UUID 字符串
        elif isinstance(identifier, str):
            card_to_remove = self._cards_map.get(identifier)
            
        # 情况 C: 传入的是 Index (位置)
        elif isinstance(identifier, int):
            if 0 <= identifier < len(self._cards_list):
                card_to_remove = self._cards_list[identifier]

        if card_to_remove:
            # 从两个结构中移除
            try:
                self._cards_list.remove(card_to_remove) # O(N) 但 N<=10 可忽略
                del self._cards_map[card_to_remove.uuid] # O(1)
                return card_to_remove
            except (ValueError, KeyError):
                pass # 处理多线程或脏数据的情况
                
        return None

    def get_card_by_pos(self, index: int) -> Optional[BaseCard]:
        """数组特性：通过位置获取"""
        if 0 <= index < len(self._cards_list):
            return self._cards_list[index]
        return None

    def get_card_by_uuid(self, uuid: str) -> Optional[BaseCard]:
        """字典特性：通过ID获取"""
        return self._cards_map.get(uuid)

    # --- Python 魔术方法 (让类用起来像原生集合) ---

    def __getitem__(self, key: Union[int, str]):
        """
        核心特性：支持 hand[0] 和 hand['uuid-string']
        """
        if isinstance(key, int):
            return self._cards_list[key]
        elif isinstance(key, str):
            return self._cards_map[key]
        else:
            raise TypeError("Invalid argument type")

    def __iter__(self):
        """支持 for card in hand:"""
        return iter(self._cards_list)

    def __len__(self):
        """支持 len(hand)"""
        return len(self._cards_list)

    def __str__(self):
        return f"Hand({len(self)}/{self.max_hand_size}): {self._cards_list}"

