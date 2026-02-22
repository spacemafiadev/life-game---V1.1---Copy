import datetime
from core.xp_system import XPSystem

class TaskManager:
    XP_BY_DIFFICULTY = {"facile": 25, "moyen": 50, "difficile": 100}

    def __init__(self, data):
        self.data = data
        self.data.setdefault("tasks", {})

    def remove_task(self, name):
        if name in self.data["tasks"]:
            self.data["tasks"].pop(name)

    # def complete_task(self, name):
    #     today = datetime.date.today().isoformat()
    #     task = self.data["tasks"][name]
    #     task.setdefault("history", {})[today] = True

    #     # --- Calcul streak global (avant XP) ---
    #     player = self.data.setdefault("player", {})
    #     player["streak_general"] = player.get("streak_general", 0) + 1

    #     # --- Perfect day ---
    #     if all(today in t.get("history", {}) for t in self.data["tasks"].values()):
    #         player["perfect_days"] = player.get("perfect_days", 0) + 1

    #     # --- Calcul streak de la tâche (optionnel) ---
    #     task["streak"] = self.calculate_task_streak(task)
    #     task["last_done"] = today

    #     # --- Calcul XP avec multiplicateurs ---
    #     xp_system = XPSystem(self.data)
    #     base_xp = self.XP_BY_DIFFICULTY[task["difficulty"]]
    #     xp_gain = xp_system.calculate_xp(task, task_type="task")  # inclut tous les multiplicateurs
    #     xp_system.apply_xp(xp_gain)  # ajoute réellement l'XP au joueur et au total

    #     return xp_gain

    def calculate_xp_for_task(self, task):
        """Renvoie l'XP de base pour cette tâche"""
        diff = task["difficulty"].lower()
        return self.XP_BY_DIFFICULTY.get(diff, 0)
    
    
    def calculate_task_streak(self, task):
        """Calcule la streak basée sur l'historique des jours consécutifs"""
        streak = 0
        today = datetime.date.today()
        for i in range(30):  # max 30 jours consécutifs
            day = (today - datetime.timedelta(days=i)).isoformat()
            if task.get("history", {}).get(day):
                streak += 1
            else:
                break
        return streak
