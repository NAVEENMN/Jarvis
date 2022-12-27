from dataclasses import dataclass, field

@dataclass
class Goal:
    title: str
    reward: str
    is_conquered: bool
    description: str

@dataclass
class Resources:
    gold: int
    xp: int
    shield: int
    social: int

@dataclass
class Fear:
    title: str
    is_conquered: bool
    reward: str
    description: str
    target_metric: int
    current_metric: int

@dataclass
class GoodHabits:
    title: str
    description: str
    reward: str
    target_metric: int
    current_metric: int
    is_engaged: bool

@dataclass
class BadHabits:
    title: str
    description: str
    penalty: str
    target_metric: int
    current_metric: int
    is_engaged: bool

@dataclass
class Habits:
    good_habits: list[GoodHabits]
    bad_habits: list[BadHabits]

@dataclass
class Identity:
    name: str = "Naveen"

@dataclass
class Traits:
    fears: list[Fear]

@dataclass
class BioData:
    age: int
    height: float
    weight: int

@dataclass
class Profile:
    level: int
    identity: Identity
    biodata: BioData
    traits: Traits
    habits: Habits
    resources: Resources
    goals: list[Goal]

