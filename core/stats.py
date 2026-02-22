from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import pandas as pd


class Stats:
    """Gestion des XP et des streaks"""

    def __init__(self, data):
        self.data = data
        self.data.setdefault("history", {})
        self.data.setdefault("player", {})
        self.data["player"].setdefault("streak_general", 0)
        self.data["player"].setdefault("perfect_days", 0)

    # ---------- XP ----------

    def add_daily_xp(self, xp, date1=None):
        """Ajoute l'XP pour une journée"""
        if date1 is None:
            date1 = datetime.date.today().isoformat()
        self.data["history"][date1] = self.data["history"].get(date1, 0) + xp

    def get_daily_xp(self):
        """Retourne un DataFrame des XP journaliers triés par date"""
        history = self.data.get("history", {})
        df = pd.DataFrame(history.items(), columns=["date", "xp"])
        df["date"] = pd.to_datetime(df["date"])
        return df.sort_values("date")

    def plot_progression(self, canvas):
        """Affiche un graphique de l'évolution de l'XP"""
        df = self.get_daily_xp()
        if df.empty:
            return
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(df["date"], df["xp"], marker="o")
        ax.set_title("XP journalier")
        ax.set_ylabel("XP")
        ax.set_xlabel("Date")
        fig.autofmt_xdate()
        canvas.figure = fig
        canvas.draw()

    # ---------- STREAKS ----------

    def compute_streaks(self):
        """Calcule streak général et perfect streak"""

        history = self.data.get("history", {})

        # --- Streak général ---
        sorted_days = sorted(history.keys())
        streak_general = 0
        prev_day = None
        for day_str in sorted_days:
            day_date = datetime.fromisoformat(day_str).date()
            if prev_day is None:
                streak_general = 1
            else:
                if (day_date - prev_day).days == 1:
                    streak_general += 1
                else:
                    streak_general = 1
            prev_day = day_date

        
        # --- Mise à jour des données ---
        player = self.data["player"]
        player["streak_general"] = streak_general
        
        # Debug
        print("[STATS DEBUG] computed streak_general =", streak_general)
        

    def compute_perfect_streak(self):
        tasks = self.data.get("tasks", {})
        player = self.data["player"]
    
        if not tasks:
            player["perfect_days"] = 0
            return
    
        streak = 0
        current_day = date.today() - timedelta(days=1)  # on commence à hier
    
        while True:
            # tâches existantes à cette date
            relevant_tasks = [
                t for t in tasks.values()
                if datetime.fromisoformat(t["created"]).date() <= current_day
            ]
    
            if not relevant_tasks:
                break  # aucun contenu = streak cassée
    
            all_done = all(
                t.get("history", {}).get(current_day.isoformat(), False)
                for t in relevant_tasks
            )
    
            if not all_done:
                break
    
            streak += 1
            current_day -= timedelta(days=1)
    
        # Récupère le streak général
        streak_general = player.get("streak_general", 0)
        
        # Perfect streak ≤ streak général
        streak_perfect = min(streak, streak_general)
        
        # Vérifie si toutes les tâches sont faites aujourd'hui
        all_done_today = all(
            task.get("history", {}).get(date.today().isoformat(), False)
            for task in self.data.get("tasks", {}).values()
        )
        
        # Met à jour les perfect days
        if all_done_today:
            player["perfect_days"] = streak_perfect + 1
        else:
            player["perfect_days"] = streak_perfect
        
        print("[STATS DEBUG] computed perfect_streak =", player["perfect_days"])
        
        
        
    def compute_task_streaks(self):
        """Calcule streaks individuels et streak général"""
        tasks_data = self.data.get("tasks", {})
        
        # --- Streak individuel par tâche ---
        for task_name, task in tasks_data.items():
            task_history = task.get("history", {})
            sorted_task_days = sorted(task_history.keys())
            streak_task = 0
            prev_task_day = None
            for day_str in sorted_task_days:
                day_date = datetime.fromisoformat(day_str).date()
                if prev_task_day is None:
                    streak_task = 1
                else:
                    if (day_date - prev_task_day).days == 1:
                        streak_task += 1
                    else:
                        streak_task = 1
                prev_task_day = day_date
            task["streak"] = streak_task
    
            # Debug
    
        
    # ---------- UTILITAIRES ----------

    def get_top_streak_tasks(self, tasks, n=5):
        """Retourne les n tâches avec la plus longue streak"""
        return sorted(tasks.values(), key=lambda t: t.get("streak", 0), reverse=True)[:n]

    def get_current_streak(self):
        return self.data["player"].get("streak_general", 0)

    def get_perfect_days(self):
        return self.data["player"].get("perfect_days", 0)
    
    def refresh(self):
        """Met à jour tout : streak général, perfect streak, etc."""
        self.compute_streaks()
        self.compute_perfect_streak()
        self.compute_task_streaks()
    
