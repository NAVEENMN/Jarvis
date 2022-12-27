import emoji
from Services.raven import Raven
from Kamaji import Kamaji
from Kratos import Kratos
from datetime import datetime
from datetime import date


def generate_progress_bar(current_value, target_value, BARSIZE=20):
    percent_complete = 1.0 - ((target_value - current_value) / target_value)
    _val = (int(percent_complete*BARSIZE))
    pc = ['.'] * _val
    bars = pc + [' '] * (BARSIZE-_val)
    return ''.join(bars)


class Jarvis:
    """
    Named after a character from iron man, jarvis acts as a life management system automating various parts of my life.
    Jarvis has the following responsibilities
    1. Pull various pieces of information, organize it and send it me
    2. If I respond to certain messages, Jarvis knows how to handle my responses.
    """
    def __init__(self):
        self.name = "Jarvis"
        self.start_date = date(2022, 12, 15)
        self.kamaji = Kamaji()
        self.kratos = Kratos()

    def process_feedbacks(self, feedback):
        self.kratos.process_feedback(feedback=feedback)
        return

    def run_evening_routines(self):
        days_elapsed = date.today() - self.start_date
        line1 = f"{emoji.emojize(':crescent_moon:')} Day {days_elapsed.days} \n\n"
        # 1. Fetch character sheet
        profile = self.kamaji.get_character_sheet()
        # 2. Sync gold
        gold = self.kamaji.get_gold()
        profile.resources.gold = gold
        self.kamaji.sync_gold(profile=profile)

        level_targets = self.kamaji.get_level_target(level=profile.level)
        resources = profile.resources

        bars = generate_progress_bar(current_value=resources.gold, target_value=level_targets.target_gold)
        line2 = line1 + f"{emoji.emojize(':money_bag:')} {resources.gold}:{bars}:{level_targets.target_gold}"
        bars = generate_progress_bar(current_value=resources.xp, target_value=level_targets.target_xp)
        line3 = line2 + f"\n{emoji.emojize(':rocket:')} {resources.xp}:{bars}:{level_targets.target_xp}"
        bars = generate_progress_bar(current_value=resources.shield, target_value=level_targets.target_shield)
        line4 = line3 + f"\n{emoji.emojize(':shield:')} {resources.shield}:{bars}:{level_targets.target_shield}"

        line5 = line4 + "\n\n Please complete the checklist \n"
        checklist = ['Update your tracking journal',
                     'Update your Journal',
                     'Settle gold',
                     'Settle XP',
                     'Give feedback to Kratos',
                     'Check calender for key events',
                     'Check Weekly tasks',
                     'Revisit goals']
        for id, chk in enumerate(checklist):
            line5 += f"{id+1}. {chk} \n"

        report = line5
        # 6. Send raven
        raven = Raven(identity=self.name)
        raven.send_a_message(body=report)

    def run_noon_routines(self):
        recommendation = self.kratos.get_workout()
        days_elapsed = date.today() - self.start_date
        line1 = f"{emoji.emojize(':sun_with_face:')} Day {days_elapsed.days} \n\n"
        line2 = line1 + "Here are your recommendations boy!!\n"
        line3 = line2 + recommendation
        raven = Raven(identity=self.kratos.name)
        raven.send_a_message(body=line3)
        # Get exercise and Food recommendation from Kratos

    def run_morning_routines(self):
        # 1. Fetch character sheet
        profile = self.kamaji.get_character_sheet()
        # 2. Sync gold
        gold = self.kamaji.get_gold()
        profile.resources.gold = gold
        self.kamaji.sync_gold(profile=profile)
        # 3. Get gold, xp, shield
        # 4. Compose progress bar
        # 5. Sample goals and gems
        snippet = self.kamaji.get_snippet()
        report = self.get_morning_report(resources=profile.resources,
                                         snippet=snippet,
                                         goals=profile.goals,
                                         level=profile.level)
        print(report)
        # 6. Send raven
        raven = Raven(identity=self.name)
        raven.send_a_message(body=report)

    def get_morning_report(self, resources, snippet, goals, level=0):
        level_targets = self.kamaji.get_level_target(level=level)
        days_elapsed = date.today() - self.start_date
        line1 = f"{emoji.emojize(':sun_with_face:')} Day {days_elapsed.days} \n\n"
        bars = generate_progress_bar(current_value=resources.gold, target_value=level_targets.target_gold)
        line2 = line1 + f"{emoji.emojize(':money_bag:')} {resources.gold}:{bars}:{level_targets.target_gold}"
        bars = generate_progress_bar(current_value=resources.xp, target_value=level_targets.target_xp)
        line3 = line2 + f"\n{emoji.emojize(':rocket:')} {resources.xp}:{bars}:{level_targets.target_xp}"
        bars = generate_progress_bar(current_value=resources.shield, target_value=level_targets.target_shield)
        line4 = line3 + f"\n{emoji.emojize(':shield:')} {resources.shield}:{bars}:{level_targets.target_shield}"

        line4 = line4 + f"\n\n{emoji.emojize(':gem:')}\n{snippet.text}\n{snippet.author}-{snippet.book}\n"

        line5 = line4 + f"\n{emoji.emojize(':dart:')}Goals"
        for i, _goal in enumerate(goals):
            line5 += f"\n\n{i+1}.{_goal.title}\n{_goal.reward}"

        return line5

    def run_routines(self):
        if datetime.now().hour < 10:
            self.run_morning_routines()
        elif datetime.now().hour < 15:
            self.run_noon_routines()
        else:
            self.run_evening_routines()


def main():
    jarvis = Jarvis()
    jarvis.run_routines()


if __name__ == "__main__":
    main()