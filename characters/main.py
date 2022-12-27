from Systems.DatabaseManagementSystem import DatabaseManagementSystem
from DataModels.CharacterSheet import *


def get_profile():
    db = DatabaseManagementSystem()
    db.change_database(db_name="Characters")
    record, status = db.get_a_record(collection="Naveen")
    data = record['document']['data']

    profile = Profile()
    profile.__setattr__("level", data['level'])
    profile.identity.__setattr__("name", data['identity']['name'])
    profile.biodata.__setattr__("age", data['biodata']['age'])
    profile.biodata.__setattr__("height", data['biodata']['height'])
    profile.biodata.__setattr__("weight", data['biodata']['weight'])

    profile.traits.fears.clear()
    for fear in data['traits']['fears']:
        _fear = Fear(title=fear['title'],
                     is_conquered=fear['is_conquered'],
                     reward=fear['reward'],
                     description=fear['description'],
                     target_metric=fear['target_metric'],
                     current_metric=fear['current_metric'])
        profile.traits.fears.append(_fear)

    profile.habits.good_habits.clear()
    profile.habits.bad_habits.clear()
    for habit in data['habits']['good_habits']:
        _habit = GoodHabits(title=habit['title'],
                            description=habit['description'],
                            reward=habit['reward'],
                            target_metric=habit['target_metric'],
                            current_metric=habit['current_metric'])
        profile.habits.good_habits.append(_habit)
    for habit in data['habits']['bad_habits']:
        _habit = BadHabits(title=habit['title'],
                           description=habit['description'],
                           penalty=habit['penalty'],
                           target_metric=habit['target_metric'],
                           current_metric=habit['current_metric'])
        profile.habits.bad_habits.append(_habit)

    return profile


