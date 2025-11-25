from typing import List, Dict, Any, Optional
from Card.SpellCard import SpellCard
from Card.BaseCard import BaseCard

class GenericSpellCard(SpellCard):
    def __init__(self, card_data: Dict[str, Any], effects: List[Dict[str, Any]]):
        # 提取基类需要的参数
        # 注意：这里需要根据你的 BaseCard/SpellCard __init__ 签名来调整
        # SpellCard.__init__(self, card_id, name, cost, **kwargs)
        super().__init__(
            card_id=card_data.get("id"),
            name=card_data.get("name"),
            cost=card_data.get("cost"),
            rarity=card_data.get("rarity"),
            target_type=card_data.get("target_type"),
            description=card_data.get("description", "")
        )
        self.effects_data = effects

    def cast_effect(self, target: Optional[BaseCard]):
        # 这里是一个简易的效果处理器
        for effect in self.effects_data:
            action = effect.get("action")
            if action == "deal_damage":
                amount = effect.get("value", 0)
                if target and hasattr(target, "take_damage"):
                    print(f"{self.name} 对 {target.name} 造成 {amount} 点伤害")
                    target.take_damage(amount)
                else:
                    print("无效的目标")
            # 可以扩展更多效果，比如 draw_card, heal 等
            elif action == "heal":
                pass

