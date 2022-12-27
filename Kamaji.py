import dataclasses
import os
import random
import time
import json
import requests
import stripe
from datetime import date, timedelta
from characters import main
from dataclasses import dataclass, asdict, make_dataclass
from DataModels.Levels import *
from Systems.DatabaseManagementSystem import DatabaseManagementSystem
from DataModels.CharacterSheet import *
from DataModels.Resources import *



class Kamaji(DatabaseManagementSystem):
    """
    Named after a character from spirited away.
    Kamaji acts as a book keeper. When orders come in from various parts of this system,
    Kamaji pulls data from different locations does his magic and sends it how they want.
    Kamaji has the following responsibilities
    1. Listen to request orders and return what is asked.
    2. Every day organize information in the database so we dont loose track of things.
    """
    def __init__(self):
        super().__init__()
        self.name = "Kamaji"

    def get_level_target(self, level=0):
        if level == 0:
            return Level1

    def __make_copy_of_character_sheet(self):
        self.change_database(db_name="Characters")
        yesterdays_record, status = self.get_a_record(collection="Naveen", value=str(date.today() - timedelta(1)))
        if status:
            print(yesterdays_record['document'])
            self.add_a_record(collection="Naveen", content=yesterdays_record['document']['data'])

    def __make_copy_of_resources(self):
        gold = self.get_gold()
        self.change_database(db_name="Stats")
        record, status = self.get_a_record(collection="Resources", value=str(date.today() - timedelta(1)))
        if status:
            data = record['document']['data']
            resources = Resources(gold=Gold(data['gold'], Level1.target_gold),
                                  xp=Xp(data['xp'], Level1.target_xp),
                                  shield=Shield(data['shield'], Level1.target_shield),
                                  social=Social(data['social'], Level1.target_social))
            self.add_a_record(collection="Resources", content=asdict(resources))
            return resources
        return None

    def run_morning_routine(self):
        # 1. Make a copy of Character sheet
        self.__make_copy_of_character_sheet()
        # 2. Make a copy of Resources
        resources = self.__make_copy_of_resources()
        return resources

    def sync_gold(self, profile):
        print("*** INFO: Syncing records")
        self.change_database(db_name="Characters")
        self.delete_a_record(collection="Naveen", key="identity", value="naveen")  # Delete today's record
        self.add_a_record(collection="Naveen", content=asdict(profile), key="identity", value="naveen")

    def get_gold(self):
        # Kamaji gets gold value from the bank and returns and also makes sure database records are in sync
        print("*** INFO: Getting gold info")
        stripe.api_key = os.environ.get('STRIPEKEY')
        resp = stripe.Balance.retrieve()
        _gold = int((resp['available'][0]['amount'] + resp['pending'][0]['amount']) / 100)
        return _gold

    def get_snippet(self):
        self.change_database(db_name="Resources")
        record, status = self.get_a_record(collection="snippets", key="snippet", value="texts")
        if status:
            data = record['document']['data']['snippets']
            snippet = random.choices(data, k=1)[0]
            _snippet = Snippet(text=snippet['text'],
                               author=snippet['author'],
                               book=snippet['book'])
            return _snippet
        return None

    def get_character_sheet(self):
        self.change_database(db_name="Characters")
        record, status = self.get_a_record(collection="Naveen", key="identity", value="naveen")
        profile = None
        if status:
            data = record['document']['data']
            bio_data = BioData(age=data['biodata']['age'],
                               height=data['biodata']['height'],
                               weight=data['biodata']['weight'])
            resources = Resources(gold=data['resources']['gold'],
                                  xp=data['resources']['xp'],
                                  shield=data['resources']['shield'],
                                  social=data['resources']['social'])
            # TODO: Fill fears
            traits = Traits(fears=[])
            # TODO: Fill habits
            habits = Habits(good_habits=[], bad_habits=[])

            goals = []
            for _goal in data['goals']:
                goal = Goal(title=_goal['title'],
                            description=_goal['description'],
                            is_conquered=_goal['is_conquered'],
                            reward=_goal['reward'])
                goals.append(goal)

            # TODO: Fix hardcoded snippets

            profile = Profile(level=data['level'],
                              identity=Identity(name="Naveen"),
                              biodata=bio_data,
                              traits=traits,
                              habits=habits,
                              resources=resources,
                              goals=goals)
        return profile

    def log_profile_data(self):
        print(asdict(main.get_profile()))
        return
        self.change_database(db_name="Characters")
        record, status = self.get_a_record(collection="Naveen")
        print(record['document']['data'])
        profile = CharacterSheet.Profile(record['document']['data'])
        print(profile)
        profile.biodata.weight -= 1
        print(profile)
        self.delete_a_record(collection="Naveen")
        time.sleep(2)
        self.add_a_record(collection="Naveen",
                          key="date",
                          value=str(date.today()),
                          content=asdict(profile))
        time.sleep(1)
        record, status = self.get_a_record(collection="Naveen")
        record = record['document']['data']
        print(CharacterSheet.Profile(record))
        #dataclasses.make_dataclass()





