import datetime

class QuestManager:
    XP_BY_DIFFICULTY = {"facile": 100, "moyen": 200, "difficile": 500, "epic": 1500}

    def __init__(self, data):
        self.data = data

    def add_quest(self, name, difficulty):
        self.data["quests"].append({"name": name, "difficulty": difficulty, "streak": 0, "last_done": None})

    def remove_quest(self, index):
        if 0 <= index < len(self.data["quests"]):
            self.data["quests"].pop(index)

    def complete_quest(self, index):
        import xp_system
        quest = self.data["quests"][index]
        xp_gain = xp_system.XPSystem(self.data).calculate_xp(quest, task_type="quest")
        quest["streak"] += 1
        quest["last_done"] = str(datetime.date.today())
        self.data["xp"] += xp_gain
        return xp_gain

    def calculate_xp_for_quest(self, quest):
        diff = quest["difficulty"].lower()
        return self.XP_BY_DIFFICULTY.get(diff, 0)