from dataclasses import dataclass

@dataclass
class Level1:
    target_gold: int = pow(10, 1)
    target_xp: int = 100 * 1
    target_shield: int = 7 * 1
    target_social: int = 7

@dataclass
class Level2:
    target_gold: int = pow(10, 2)
    target_xp: int = 100 * 1
    target_shield: int = 7 * 3
    target_social: int = 7

@dataclass
class Level3:
    target_gold: int = pow(10, 3)
    target_xp: int = 100 * 1
    target_shield: int = 7 * 5
    target_social: int = 7

@dataclass
class Level4:
    target_gold: int = pow(10, 4)
    target_xp: int = 100 * 1
    target_shield: int = 7 * 6
    target_social: int = 7

@dataclass
class Level5:
    target_gold: int = pow(10, 5)
    target_xp: int = 100 * 1
    target_shield: int = 7 * 8
    target_social: int = 7

@dataclass
class Level6:
    target_gold: int = pow(10, 6)
    target_xp: int = 100 * 1
    target_shield: int = 7 * 8
    target_social: int = 7

@dataclass
class Level7:
    target_gold: int = pow(10, 7)
    target_xp: int = 100 * 1
    target_shield: int = 7 * 10
    target_social: int = 7

@dataclass
class Level8:
    target_gold: int = pow(10, 8)
    target_xp: int = 100 * 1
    target_shield: int = 7 * 20
    target_social: int = 7

@dataclass
class Level9:
    target_gold: int = pow(10, 9)
    target_xp: int = 100 * 1
    target_shield: int = 7 * 30
    target_social: int = 7

@dataclass
class Level10:
    target_gold: int = pow(10, 10)
    target_xp: int = 100 * 1
    target_shield: int = 7 * 40
    target_social: int = 7
