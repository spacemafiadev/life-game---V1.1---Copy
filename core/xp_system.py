class XPSystem:
    LEVEL_MULTIPLIER = 1.5
    BASE_XP = 100

    def __init__(self, data):
        self.data = data
        # Initialiser xp_total si absent
        self.data.setdefault("player", {})
        self.data["player"].setdefault("xp_total", self.data.get("xp", 0))
        self.data.setdefault("xp", 0)
        self.data.setdefault("level", 1)

    # --- Calcul multiplicateur total ---
    def calculate_multiplier(self, task):
        player = self.data["player"]

        # Multiplicateur streak tâche
        streak_task = task.get("streak", 0)
        mult_task = 1 + 0.1 * streak_task

        # Multiplicateur streak global
        streak_global = player.get("streak_general", 0)
        mult_global = 1 + 0.1 * streak_global

        # Multiplicateur perfect streak
        perfect_days = player.get("perfect_days", 0)
        if perfect_days >= 8:
            mult_perfect = 2.0
        elif perfect_days >= 4:
            mult_perfect = 1.6
        elif perfect_days >= 1:
            mult_perfect = 1.3
        else:
            mult_perfect = 1.0

        # Multiplicateur total
        total_multiplier = mult_task * mult_global * mult_perfect
        return total_multiplier


    def add_xp(self, xp_gain):
        """Ajoute XP et gère le niveau + XP total"""
        self.data.setdefault("player", {})
        self.data["xp"] += xp_gain
        self.data["player"]["xp_total"] = self.data["player"].get("xp_total", 0) + xp_gain
        self.update_level()
        
        # Sauvegarde dans le JSON
        self.data_manager.save_data()
        

    def apply_xp(self, xp_gain):
        self.data.setdefault("player", {})
        self.data["xp"] += xp_gain
        self.data["player"]["xp_total"] = self.data["player"].get("xp_total", 0) + xp_gain
        self.update_level()

    def update_level(self):
        """Met à jour le niveau selon l'XP actuel"""
        xp = self.data["xp"]
        level = self.data["level"]
        next_level_xp = self.BASE_XP * (self.LEVEL_MULTIPLIER ** (level - 1))
        while xp >= next_level_xp:
            xp -= next_level_xp
            level += 1
            next_level_xp = self.BASE_XP * (self.LEVEL_MULTIPLIER ** (level - 1))
        self.data["xp"] = xp
        self.data["level"] = level

    def xp_for_next_level(self):
        """Retourne l'XP nécessaire pour le niveau suivant"""
        level = self.data["level"]
        return int(self.BASE_XP * (self.LEVEL_MULTIPLIER ** (level - 1)))

    def get_progress_ratio(self):
        """Ratio de progression dans le niveau actuel (0 à 1)"""
        return self.data["xp"] / self.xp_for_next_level()

    def get_xp_total(self):
        """Retourne l'XP total cumulé"""
        return self.data["player"].get("xp_total", 0)


    def _task_streak_multiplier(self, streak):
        return 1
    
    
    def _general_streak_multiplier(self, streak):
        return 1 + 0.1 * streak
    
    
    def _perfect_streak_multiplier(self, perfect_days):
        if perfect_days >= 8:
            return 2.0
        elif perfect_days >= 4:
            return 1.6
        elif perfect_days >= 1:
            return 1.3
        return 1.0
