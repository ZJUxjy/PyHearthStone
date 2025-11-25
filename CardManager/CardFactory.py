import json
import os
from typing import Dict, Any, List

from Card.BaseCard import BaseCard, CardType, Rarity, Race, TargetType
from Card.MinionCard import MinionCard
from Card.GenericSpellCard import GenericSpellCard

class CardFactory:
    _instance = None
    _card_definitions: Dict[str, Dict[str, Any]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CardFactory, cls).__new__(cls)
            cls._instance.load_card_definitions()
        return cls._instance

    def load_card_definitions(self, json_path: str = "data/cards.json"):
        """加载 JSON 定义"""
        if not os.path.exists(json_path):
            print(f"Warning: Card definition file not found at {json_path}")
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            cards_data = json.load(f)
            for card_data in cards_data:
                self._card_definitions[card_data['id']] = card_data

    def create_card(self, card_id: str) -> BaseCard:
        """根据 ID 实例化卡牌"""
        data = self._card_definitions.get(card_id)
        if not data:
            raise ValueError(f"Card ID {card_id} not found in definitions.")

        # 1. 解析通用枚举 (String -> Enum)
        card_type_str = data.get("type", "SPELL")
        rarity_str = data.get("rarity", "FREE")
        target_type_str = data.get("target_type", "NONE")

        # 简单的字符串转枚举映射
        rarity = getattr(Rarity, rarity_str, Rarity.FREE)
        target_type = getattr(TargetType, target_type_str, TargetType.NONE)
        
        # 准备传递给构造函数的参数
        # 注意：BaseCard 需要的是枚举类型，我们在 JSON 里存的是字符串，需要转换
        # 这里为了简单，我们修改一下 GenericSpellCard 和 MinionCard 的调用方式
        # 或者在 Factory 里处理好所有数据转换
        
        # 为了通用性，我们构造一个 kwargs
        common_kwargs = {
            "card_id": data["id"],
            "name": data["name"],
            "cost": data["cost"],
            "rarity": rarity,
            "description": data.get("description", ""),
            "target_type": target_type
        }

        if card_type_str == "MINION":
            race_str = data.get("race", "NONE")
            race = getattr(Race, race_str, Race.NONE)
            
            return MinionCard(
                attack=data["attack"],
                health=data["health"],
                race=race,
                **common_kwargs
            )
            
        elif card_type_str == "SPELL":
            # SpellCard 需要特殊的 GenericSpellCard 来处理 effects
            effects = data.get("effects", [])
            # GenericSpellCard 的构造函数需要适配
            # 我们可以直接传 common_kwargs 进去，但是 GenericSpellCard 需要我们稍微调整一下
            # 让我们重新看一下 GenericSpellCard 的定义
            
            # 现在的 GenericSpellCard.__init__ 是:
            # def __init__(self, card_data: Dict[str, Any], effects: List[Dict[str, Any]]):
            # 这稍微有点不灵活，最好是统一 kwargs
            
            # 让我们稍微修改一下 GenericSpellCard 的调用，或者 Factory 适配它
            # 为了简单起见，我这里直接适配:
            
            # 构造一个包含所有转换后数据的 dict 传给 GenericSpellCard? 
            # 或者修改 GenericSpellCard 让它接收 kwargs?
            # 让我们选择修改 GenericSpellCard 接收 kwargs 的方式 (下一轮工具调用)
            
            # 暂时先用目前的 GenericSpellCard 接口
            # 需要把转换后的 Enum 放回 data 字典里，或者修改 GenericSpellCard
            
            # 让我们构造一个新的 data dict 传进去
            processed_data = data.copy()
            processed_data["rarity"] = rarity
            processed_data["target_type"] = target_type
            
            return GenericSpellCard(processed_data, effects)
            
        else:
            raise NotImplementedError(f"Card type {card_type_str} not supported yet.")


