# ui/ui_center_high.py
import customtkinter as ctk
from math import ceil
from core.stats import Stats
from datetime import date, timedelta, datetime
from ui.styles import THEME

class CenterHigh(ctk.CTkFrame):
    """Zone centrale haute : niveau et barre de progression XP"""
    def __init__(self, master, data_manager, font_title, font_widget, **kwargs):
        super().__init__(master, fg_color=THEME["bg_main"], **kwargs)
        
        self.data_manager = data_manager
        self.font_title = font_title
        self.font_widget = font_widget

        # Frame principale haute
        self.pack(fill="x", padx=10, pady=20)

        # Label niveau
        self.level_label = ctk.CTkLabel(self, text="", font=self.font_title,
                                        text_color=THEME["text_primary"])
        self.level_label.pack(pady=(0, 10))

        # Barre XP
        self.xp_bar = ctk.CTkProgressBar(self,
                                         progress_color=THEME["accent_color"],
                                         fg_color=THEME["bg_card"] )# Fond de la barre
        self.xp_bar.pack(fill="x", padx=20, pady=(0, 5))

        # Label XP
        self.xp_label = ctk.CTkLabel(self, text="", font=self.font_widget,text_color=THEME["text_primary"])
        self.xp_label.pack()
        
        # Label streak général
        self.streak_label = ctk.CTkLabel(self, text="", font=self.font_widget, text_color=THEME["text_primary"])
        self.streak_label.pack(pady=(5, 0))
        
        # Label perfect streak (caché par défaut)
        self.perfect_label = ctk.CTkLabel(self, text="", font=self.font_widget, text_color=THEME["text_primary"])
        self.perfect_label.pack(pady=(0, 5))

        self.bind_all_children(self, self.open_settings)
        # Mettre à jour l'affichage au démarrage
        self.update()

    def xp_for_next_level(self, level):
        """Calcule l'XP nécessaire pour passer au niveau suivant"""
        xp = 100
        for _ in range(1, level):
            xp = ceil(xp * 1.3)
        return xp

    def update(self):
        """Met à jour tout : niveau, barre XP, streaks"""
    
        self.update_level_xp()
        self.update_streak_general()
        self.update_perfect_streak()
    
    
    # ---------------- NIVEAU / XP ----------------
    def update_level_xp(self):
        """Met à jour le niveau, barre XP et XP du jour"""
        player = self.data_manager.data["player"]
        total_xp = player.get("xp", 0)
        today = self.current_day()
    
        today_xp = sum(
            xp for date_str, xp in self.data_manager.data.get("history", {}).items()
            if date_str == today
        )
        
        player["xp_total"] = sum(xp for date_str, xp in self.data_manager.data.get("history", {}).items())
    
        # --- Niveau ---
        level = player.get("level", 1)
        xp_needed = self.xp_for_next_level(level)
        while total_xp >= xp_needed:
            total_xp -= xp_needed
            level += 1
            xp_needed = self.xp_for_next_level(level)
    
        player["level"] = level
        player["xp"] = total_xp
        
    
        # --- UI XP ---
        self.level_label.configure(text=f"Level {level}")
        self.xp_bar.set(total_xp / xp_needed)
        self.xp_label.configure(text=f"XP: {total_xp} / {xp_needed} (+{today_xp} aujourd'hui)")
    
    
    # ---------------- STREAK GENERAL ----------------
    def update_streak_general(self):
        """Met à jour l'affichage de la streak normale"""
        player = self.data_manager.data["player"]
        stats = Stats(self.data_manager.data)
        stats.compute_streaks()
    
        streak_general = player.get("streak_general", 0)
        tasks = self.data_manager.data.get("tasks", {}).values()
    
        # Danger streak général : si streak > 1 et aucune tâche faite aujourd'hui
        streak_danger = False
        if streak_general > 1:
            today = self.current_day()
            any_done_today = any(task.get("history", {}).get(today, False) for task in tasks)
            if not any_done_today:
                streak_danger = True
    
        # --- Affichage streak général ---
        if streak_general > 1:
            mult_general = 1 + 0.1 * streak_general
        
            if streak_danger:
                self.streak_label.configure(
                    text=f"⚠️ Streak en danger : {streak_general} jours  (x{mult_general:.2f})",
                    font=self.font_widget, text_color="#FFA726"
                )
            else:
                self.streak_label.configure(
                    text=f"🔥 Streak actuel : {streak_general} jours  (x{mult_general:.2f})",
                    font=self.font_widget, text_color=THEME["text_primary"]
                )
        else:
            self.streak_label.configure(text="")

    
    
    # ---------------- PERFECT STREAK ----------------
    def update_perfect_streak(self):
        """Met à jour l'affichage du perfect streak avec détection de danger"""
    
        player = self.data_manager.data["player"]
        tasks = list(self.data_manager.data.get("tasks", {}).values())
        today = date.today()
        yesterday = today - timedelta(days=1)
    
        # ---------- CALCUL PERFECT STREAK (jours passés uniquement) ----------
        perfect_streak = 0
        current_day = yesterday
    
        while True:
            # Tâches existantes à cette date
            relevant_tasks = [
                t for t in tasks
                if datetime.fromisoformat(t["created"]).date() <= current_day
            ]
    
            if not relevant_tasks:
                break  # aucun contenu → streak cassée
    
            all_done = all(
                t.get("history", {}).get(current_day.isoformat(), False)
                for t in relevant_tasks
            )
    
            if not all_done:
                break
    
            perfect_streak += 1
            current_day -= timedelta(days=1)
    
        # ---------- COHÉRENCE AVEC STREAK GÉNÉRALE ----------
        streak_general = player.get("streak_general", 0)
        if perfect_streak > streak_general:
            perfect_streak = 0
    
        player["perfect_days"] = perfect_streak
    
        # ---------- DANGER PERFECT STREAK ----------
        perfect_danger = False
        if perfect_streak > 0:
            relevant_today_tasks = [
                t for t in tasks
                if datetime.fromisoformat(t["created"]).date() <= today
            ]
    
            all_done_today = all(
                t.get("history", {}).get(today.isoformat(), False)
                for t in relevant_today_tasks
            )
    
            if not all_done_today:
                perfect_danger = True
    
        # ---------- AFFICHAGE ----------
        if perfect_streak > 0:
            mult_perfect = self.perfect_multiplier_from_days(perfect_streak)
        
            if perfect_danger:
                self.perfect_label.configure(
                    text=f"⚠️ Perfect streak en danger : {perfect_streak}  (x{mult_perfect:.1f})",
                    font=self.font_widget, text_color="#FFA726"
                )
            else:
                self.perfect_label.configure(
                    text=f"⭐ Perfect days : {perfect_streak+1}  (x{mult_perfect:.1f})",
                    font=self.font_widget, text_color=THEME["text_primary"]
                )
        else:
            self.perfect_label.configure(text="")

    def current_day(self):
        """Retourne la date du jour ISO"""
        from datetime import date
        return date.today().isoformat()
    
    def perfect_multiplier_from_days(self, days):
        if days >= 8:
            return 2.0
        elif days >= 4:
            return 1.6
        elif days >= 1:
            return 1.3
        return 1.0

    def bind_all_children(self, widget, callback):
        widget.bind("<Button-1>", callback)
        for child in widget.winfo_children():
            self.bind_all_children(child, callback)

    def open_settings(self, event=None):
        from ui.ui_settings import SettingsPopup
        # On remonte au root (GamificationApp) via master.master si nécessaire
        # En général, self.master est top_bar, self.master.master est root_column, etc.
        # On utilise .winfo_toplevel() pour être sûr d'avoir l'app principale
        root = self.winfo_toplevel()
        SettingsPopup(root, self.data_manager)
