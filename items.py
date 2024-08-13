class Item:
    def __init__(self, name, effect, price):
        self.name = name
        self.effect = effect
        self.price = price

    def use(self, target):
        if self.effect == "heal":
            # 체력 회복
            target.health = min(target.health + 20, target.max_health)
            print(f"{target.name}가 20 HP를 회복했습니다.")
        elif self.effect == "buff":
            # 공격력 증가
            target.attack += 5
            print(f"{target.name}의 공격력이 5 증가했습니다.")
        else:
            print(f"아이템 효과 '{self.effect}'는 지원하지 않습니다.")

    def to_dict(self):
        return {
            "name": self.name,
            "effect": self.effect,
            "price": self.price,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], effect=data["effect"], price=data["price"])


def get_items():
    return [Item("Potion", "heal", 20), Item("Elixir", "buff", 50)]


def buy_item(character, item_name):
    items = get_items()
    item = next(
        (item for item in items if item.name.lower() == item_name.lower()), None
    )

    if item:
        if character.gold >= item.price:
            character.gold -= item.price
            character.inventory.append(item)
            return True, f"아이템 '{item.name}'을(를) 구매했습니다."
        else:
            return False, "골드가 부족합니다."
    else:
        return False, f"아이템 '{item_name}'을(를) 찾을 수 없습니다."
