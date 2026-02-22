import json
from datetime import date
import os

class DataManager:
    def __init__(self, json_file="data.json"):
        self.json_file = json_file
        self.data = self.load_data()

    def load_data(self):
        today = date.today().isoformat()
        if not os.path.exists(self.json_file):
            # Création JSON initial
            data = {
                "meta": {"created": today, "last_open": today},
                "player": {
                    "xp": 0,
                    "streak_general": 0,
                    "perfect_days": 0,
                    "level": 1,
                    "xp_total": 0,
                    "streak_general_max": 0,
                    "perfect_days_max": 0,
                    "quests_completed_count": 0,
                    "badges": []
                },
                "settings": {"theme": "Dark Standard"},
                "tasks": {
                    "Boire de l'eau": {
                        "name": "Boire de l'eau",
                        "difficulty": "facile",
                        "created": today,
                        "history": {},
                        "streak": 0,  
                        "last_done": None
                    }
                },
                "quests": {},
                "history": {},
                "custom_rewards": {}
            }
            self.save_data(data)
            return data
        else:
            with open(self.json_file, "r") as f:
                return json.load(f)
        

    def save_data(self, data=None):
        if data is not None:
            self.data = data
        with open(self.json_file, "w") as f:
            json.dump(self.data, f, indent=4)

    # ================= TASKS =================

    def get_tasks(self):
        """Retourne les tâches sous forme dict {name: task}"""
        return self.data.get("tasks", {})

    def is_task_done_today(self, task_name):
        today = date.today().isoformat()
        task = self.data["tasks"].get(task_name)
        if task and task.get("history", {}).get(today):
            return True
        return False

    def mark_task_done(self, task_name):
        today = date.today().isoformat()
        task = self.data["tasks"].get(task_name)
        if not task:
            return
        task.setdefault("history", {})[today] = True
        self.save_data()

    def add_task(self, name, difficulty="facile"):
        if name in self.data["tasks"]:
            return
        self.data["tasks"][name] = {
            "name": name,
            "difficulty": difficulty.lower(),
            "created": date.today().isoformat(),
            "history": {},
            "streak": 0,  
            "last_done": None
        }
        self.save_data()

    def remove_task(self, name):
        """Supprime une tâche mais conserve l'historique XP"""
        if name in self.data["tasks"]:
            del self.data["tasks"][name]
            self.save_data()
            
            
            
    # ================= QUESTS =================

    def get_quests(self):
        """Retourne toutes les quêtes"""
        return self.data.get("quests", {})
    
    def is_quest_done(self, quest_name):
        """Retourne True si la quête est complétée"""
        quest = self.data["quests"].get(quest_name)
        if quest and quest.get("completed"):
            return True
        return False
    
    def mark_quest_done(self, quest_name):
        """Marque la quête comme complétée et sauvegarde"""
        quest = self.data["quests"].get(quest_name)
        if not quest:
            return
        quest["completed"] = True
        self.save_data()
        
    def add_quest(self, name, difficulty="facile"):
        """Ajoute une quête si elle n'existe pas encore"""
        if name in self.data["quests"]:
            return
        self.data["quests"][name] = {
            "name": name,
            "difficulty": difficulty.lower(),
            "created": date.today().isoformat(),
            "completed": False
            }
        self.save_data()
            
    def remove_quest(self, name):
        """Supprime une quête"""
        if name in self.data["quests"]:
            del self.data["quests"][name]
            self.save_data()



    # ================= BADGES =================
    
    
    def update_max_stats(self):
        """Vérifie et met à jour les records personnels"""
        player = self.data["player"]
        
        # Mise à jour du max pour la streak générale
        if player.get("streak_general", 0) > player.get("streak_general_max", 0):
            player["streak_general_max"] = player["streak_general"]
            
        # Mise à jour du max pour les jours parfaits
        if player.get("perfect_days", 0) > player.get("perfect_days_max", 0):
            player["perfect_days_max"] = player["perfect_days"]