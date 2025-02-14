# character.py

from items import Item, get_items  # `items.py`에서 `Item` 클래스를 임포트
from quest import Quest


class Character:
    def __init__(
        self,
        name,
        health,
        attack,
        defense,
        level=1,
        experience=0,
        max_health=None,
        gold=0,
        inventory=None,
        quests=None,
        level_growth=None,  # 새로운 속성 추가
    ):
        self.name = name
        self.health = health
        self.max_health = max_health if max_health is not None else health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = experience
        self.gold = gold
        self.inventory = inventory if inventory is not None else []
        self.quests = quests if quests is not None else []  # 퀘스트 목록
        self.level_growth = (
            level_growth
            if level_growth is not None
            else {"health": 10, "attack": 2, "defense": 1}
        )  # 기본 성장 값 설정

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health = max(self.health - damage, 0)

    def attack_target(self, target):
        damage = max(self.attack - target.defense, 0)
        if damage > 0:
            target.take_damage(damage)
        return damage

    def gain_experience(self, exp):
        self.experience += exp
        while self.experience >= self.level * 10:
            self.level_up()

    # 레벨업 메소드 수정
    def level_up(self):
        self.level += 1
        self.max_health += self.level_growth["health"]
        self.health = self.max_health  # 레벨업 시 체력 회복
        self.attack += self.level_growth["attack"]
        self.defense += self.level_growth["defense"]
        self.experience = 0  # 경험치 초기화 (혹은 경험치 감소)
        print(f"{self.name}가 레벨업했습니다! 레벨: {self.level}")

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "defense": self.defense,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "inventory": [item.to_dict() for item in self.inventory],
        }

    def add_quest(self, quest):
        self.quests.append(quest)

    def complete_quest(self, quest_name):
        for quest in self.quests:
            if quest.name == quest_name and quest.completed:
                self.quests.remove(quest)
                self.gold += quest.reward
                return (
                    f"퀘스트 '{quest_name}' 완료! {quest.reward} 골드를 획득했습니다."
                )
        return "완료할 수 있는 퀘스트가 없습니다."

    def update_quests(self):
        for quest in self.quests:
            if quest.update_progress():
                print(f"퀘스트 '{quest.name}' 완료!")

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            health=data["health"],
            attack=data["attack"],
            defense=data["defense"],
            level=data["level"],
            experience=data["experience"],
            max_health=data["max_health"],
            gold=data.get("gold", 0),
            inventory=[Item.from_dict(item) for item in data.get("inventory", [])],
        )

    def __str__(self):
        return (
            f"{self.name} - 레벨: {self.level}, HP: {self.health}/{self.max_health}, "
            f"공격력: {self.attack}, 방어력: {self.defense}, 골드: {self.gold}"
        )


class CharacterItem:
    def __init__(self, name, effect, price):
        self.name = name.lower()  # 이름을 소문자로 저장
        self.effect = effect
        self.price = price

    def use(self, target):
        effect_methods = {
            "heal": self.apply_heal,
            "buff": self.apply_buff,
        }
        method = effect_methods.get(self.effect.lower())  # 효과를 소문자로 변환
        if method:
            method(target)
        else:
            print(f"아이템 효과 '{self.effect}'는 지원하지 않습니다.")

    def apply_heal(self, target):
        target.health = min(target.health + 20, target.max_health)
        print(f"{target.name}(이)가 20 HP를 회복했습니다.")

    def apply_buff(self, target):
        target.attack += 5
        print(f"{target.name}의 공격력이 5 증가했습니다.")

    def to_dict(self):
        return {
            "name": self.name,
            "effect": self.effect,
            "price": self.price,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"].lower(),  # 아이템 이름을 소문자로 변환
            effect=data["effect"],
            price=data["price"],
        )
