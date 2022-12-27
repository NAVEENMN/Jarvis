from dataclasses import dataclass, field


@dataclass
class Workout:
    title: str
    metric: float
    update_rule: float
    metric_indicator: str
    upper_limit: float
    lower_limit: float
    is_recommended: bool


@dataclass
class Activity:
    title: str
    metric: float
    metric_indicator: str
    update_rule: float
    is_recommended: bool


@dataclass
class Snippet:
    text: str
    author: str
    book: str


@dataclass
class Snippets:
    snippets: list[Snippet]


@dataclass
class Exercise:
    workouts: list[Workout]
    activities: list[Activity]
