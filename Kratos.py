import random
import time

from DataModels.Resources import *
from dataclasses import dataclass, asdict
from Systems.DatabaseManagementSystem import DatabaseManagementSystem


class Kratos(DatabaseManagementSystem):
    """
    Named after a character from god of war,
    Kratos acts as a tough father figure who disciplines me in various parts of my life.
    Kratos has the following responsibilities
    1. Pull various pieces of information regarding my health and habits, organize it and send it me.
    2. If I respond to certain messages, Jarvis sends my message to Kratos and he knows how to handle it.
    3. Kratos recommends everyday what exercise I must do and based on the feedback
    I give he updates his recommendation.
    """

    def __init__(self):
        super().__init__()
        self.name = "Kratos"

    # TODO: Handle upper and lower limits
    def get_workout(self):
        self.change_database(db_name="Resources")
        record, status = self.get_a_record(collection="exercises", key="exercise", value="exercise")
        exercise_recommendation = None
        if status:
            data = record['document']['data']
            activities = []
            workouts = []
            for activity in data['activities']:
                act = Activity(title=activity['title'],
                               metric=activity['metric'],
                               metric_indicator=activity['metric_indicator'],
                               update_rule=activity['update_rule'],
                               is_recommended=activity['is_recommended'])
                activities.append(act)
            for workout in data['workouts']:
                wk = Workout(title=workout['title'],
                             metric=workout['metric'],
                             metric_indicator=workout['metric_indicator'],
                             update_rule=workout['update_rule'],
                             upper_limit=workout['upper_limit'],
                             lower_limit=workout['lower_limit'],
                             is_recommended=workout['is_recommended'])
                workouts.append(wk)

            options = ['workouts', 'activities']
            option = random.choices(options, k=1)[0]
            if option == 'workouts':
                # sample 3
                workouts = random.choices(workouts, k=3)
                result = []
                for i, workout in enumerate(workouts):
                    result.append(f"{i + 1}. {workout.title}-{workout.metric} {workout.metric_indicator}\n")
                    workout.is_recommended = True
                exercise_recommendation = ''.join(result)
                # set is_recommended to true
            if option == 'activities':
                # sample 1
                activity = random.choices(activities, k=1)[0]
                activity.is_recommended = True
                result = f"{activity.title}-{activity.metric} {activity.metric_indicator}"
                exercise_recommendation = result

            # Update records
            self.delete_a_record(collection="exercises", key="exercise", value="exercise")
            time.sleep(2)
            self.add_a_record(collection="exercises",
                              key="exercise",
                              value="exercise",
                              content=asdict(Exercise(workouts=workouts, activities=activities)))

        return exercise_recommendation

    def get_food_recommendation(self):
        pass

    def process_feedback(self, feedback):
        self.change_database(db_name="Resources")
        record, status = self.get_a_record(collection="exercises", key="exercise", value="exercise")
        if status:
            data = record['document']['data']
            activities = []
            workouts = []
            for activity in data['activities']:
                act = Activity(title=activity['title'],
                               metric=activity['metric'],
                               metric_indicator=activity['metric_indicator'],
                               update_rule=activity['update_rule'],
                               is_recommended=activity['is_recommended'])
                if act.is_recommended:
                    if feedback:
                        act.metric += act.update_rule
                    else:
                        act.metric -= act.update_rule
                    act.is_recommended = False
                activities.append(act)
            for workout in data['workouts']:
                wk = Workout(title=workout['title'],
                             metric=workout['metric'],
                             metric_indicator=workout['metric_indicator'],
                             update_rule=workout['update_rule'],
                             upper_limit=workout['upper_limit'],
                             lower_limit=workout['lower_limit'],
                             is_recommended=workout['is_recommended'])
                if wk.is_recommended:
                    if feedback:
                        wk.metric += wk.update_rule
                    else:
                        wk.metric -= wk.update_rule
                    wk.is_recommended = False
                workouts.append(wk)

            # Update records
            self.delete_a_record(collection="exercises", key="exercise", value="exercise")
            time.sleep(2)
            self.add_a_record(collection="exercises",
                              key="exercise",
                              value="exercise",
                              content=asdict(Exercise(workouts=workouts, activities=activities)))
            return True
        return False
