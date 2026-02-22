import customtkinter as ctk
from ui.styles import THEME

LEVELS = [
    "Fer", "Bronze", "Argent", "Or", "Platine",
    "Émeraude", "Diamant", "Master", "GrandMaster", "Challenger"
]

LEVEL_COLORS = {
    "Fer": "#6E6E6E",
    "Bronze": "#CD7F32",
    "Argent": "#C0C0C0",
    "Or": "#FFD700",
    "Platine": "#E5E4E2",
    "Émeraude": "#50C878",
    "Diamant": "#00FFFF",
    "Master": "#800080",
    "GrandMaster": "#FF4500",
    "Challenger": "#FF0000",
    "locked": "#A0A0A0"
}

BADGES = [
    {"name": "XP Collector", "type": "xp"},
    {"name": "Level Up", "type": "level"},
    {"name": "Quest Challenger", "type": "quests"},
    {"name": "Streak Master", "type": "streak"},
    {"name": "Perfect Streak", "type": "perfect_streak"}
]

# Echelles de progression par badge
BADGE_LEVELS = {
    "xp": [0, 1000, 2500, 5000, 10000, 25000, 50000, 100000, 500000, 1000000],
    "level": [1, 5, 10, 15, 25, 50, 75, 100, 150, 250],
    "quests": [0, 1, 3, 5, 10, 15, 20, 30, 50, 100],
    "streak": [0, 5, 10, 15, 25, 50, 100, 250, 500, 1000],
    "perfect_streak": [0, 2, 4, 6, 10, 15, 20, 30, 40, 50]
}




class CenterLow(ctk.CTkFrame):
    def __init__(self, master, data_manager, font_widget, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.font_widget = font_widget
        self.data_manager = data_manager
        self.badge_labels = []
        self.create_ui()
        self.bind_all_children(self, self.open_rewards_table)

    def create_ui(self):
        self.configure(height=200)
        for i, badge in enumerate(BADGES):
            frame = ctk.CTkFrame(self, corner_radius=10, fg_color=THEME["bg_card"])
            frame.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)

            # Label principal du badge
            label = ctk.CTkLabel(frame, text="", corner_radius=10, font=self.font_widget, justify="center", text_color="white")
            label.pack(expand=True, fill="both", padx=5, pady=5)
            self.badge_labels.append(label)

        for i in range(len(BADGES)):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.update_badges()

    def update_badges(self):
        for i, badge in enumerate(BADGES):
            value, level_name, next_value = self.get_badge_progress(badge["type"])
            color = LEVEL_COLORS[level_name] if level_name in LEVEL_COLORS else LEVEL_COLORS["locked"]
            text = f"{level_name}\n{badge['name']}\n{value} / {next_value}"
            self.badge_labels[i].configure(text=text, fg_color=color)
            
            # Vérifie si nouveau niveau atteint pour pop-up récompense
            badge_key = f"last_level_{badge['type']}"
            last_level = self.data_manager.data.get("player", {}).get(badge_key, "")
            if last_level != level_name:
                self.data_manager.data.setdefault("player", {})[badge_key] = level_name
                if level_name not in ["locked", "Fer"]:
                    self.show_reward_popup(badge['name'], level_name)

        self.check_total_rewards()
        
        self.data_manager.save_data()

    def get_badge_progress(self, badge_type):
        data = self.data_manager.data
        self.data_manager.update_max_stats()
        levels = BADGE_LEVELS.get(badge_type, [])
        value = 0

        if badge_type == "xp":
            value = data.get("player", {}).get("xp_total", 0)
        elif badge_type == "level":
            value = data.get("player", {}).get("level", 1)
        elif badge_type == "quests":
            value = data.get("player", {}).get("quests_completed_count", 0)
        elif badge_type == "streak":
            value = data.get("player", {}).get("streak_general_max", 0)
        elif badge_type == "perfect_streak":
            value = data.get("player", {}).get("perfect_days_max", 0)
        

        # Trouve le niveau courant
        for idx, threshold in enumerate(levels):
            if value < threshold:
                level_idx = max(0, idx - 1)
                break
        else:
            level_idx = len(levels) - 1

        current_level = LEVELS[level_idx] if level_idx < len(LEVELS) else "locked"
        next_value = levels[level_idx + 1] if level_idx + 1 < len(levels) else levels[-1]

        return value, current_level, next_value
    
    
    
    def show_reward_popup(self, badge_name, level_name):
        # On cherche la récompense associée dans notre nouveau dictionnaire
        reward_key = f"{level_name}_{badge_name}"
        reward_text = self.data_manager.data.get("custom_rewards", {}).get(reward_key, "").strip()

        # SI LA CASE EST VIDE, ON N'OUVRE PAS LA FENÊTRE
        if not reward_text:
            print(f"Pas de récompense définie pour {reward_key}, pop-up annulé.")
            return
        
        
        # Sinon, on affiche le pop-up avec le texte personnalisé
        popup = ctk.CTkToplevel(self)
        popup.title("Félicitations !")
        popup.geometry("500x250")
        popup.configure(fg_color=THEME["bg_main"])
        popup.transient(self)
        popup.grab_set()

        ctk.CTkLabel(popup, text=f"🏆 Nouveau palier : {level_name} !", font=self.font_widget, text_color=THEME["text_primary"]).pack(pady=10)
        ctk.CTkLabel(popup, text=f"Badge : {badge_name}", font=self.font_widget, text_color=THEME["text_primary"]).pack(pady=5)
        
        # Affichage de la récompense écrite par l'utilisateur
        reward_label = ctk.CTkLabel(popup, text=reward_text, font=self.font_widget, text_color=THEME["accent_color"])
        reward_label.pack(pady=20)
        
        ctk.CTkButton(popup, text="Génial !", command=popup.destroy, 
                      fg_color=THEME["accent_color"],
                      hover_color=THEME["hover_color"],
                      text_color="BLACK"
                      ).pack(pady=10)
        
        
        
        
    def open_rewards_table(self, event=None):
        popup = ctk.CTkToplevel(self)
        popup.title("Configuration des Récompenses")
        popup.geometry("1100x400") # Légèrement plus grand pour le bouton
        popup.configure(fg_color=THEME["bg_main"])
        popup.transient(self)
        popup.grab_set()

        saved_rewards = self.data_manager.data.get("custom_rewards", {})
        columns = [b['name'] for b in BADGES] + ["Total"]
        
        # Liste pour garder une trace des entrées et de leurs clés
        all_entries = []

        # En-têtes
        for col_index, col_name in enumerate(columns):
            header = ctk.CTkLabel(popup, text=col_name, font=self.font_widget, text_color=THEME["accent_color"])
            header.grid(row=0, column=col_index+1, padx=5, pady=5)

        # Grille de saisie
        for row_index, level_name in enumerate(LEVELS[1:]): 
            ctk.CTkLabel(popup, text=level_name, font=self.font_widget,text_color=LEVEL_COLORS.get(level_name, "white")).grid(row=row_index+1, column=0, padx=10)
            
            for col_index, badge_name in enumerate(columns):
                reward_key = f"{level_name}_{badge_name}"
                current_val = saved_rewards.get(reward_key, "")

                entry = ctk.CTkEntry(popup, width=140, fg_color=THEME["bg_card"],
                                     border_color=THEME["border_color"],
                                     text_color=THEME["text_primary"])
                entry.insert(0, current_val)
                entry.grid(row=row_index+1, column=col_index+1, padx=2, pady=2)
                
                # On stocke l'objet et sa clé
                all_entries.append((reward_key, entry))

                # On garde les binds automatiques au cas où
                entry.bind("<FocusOut>", lambda e, k=reward_key, en=entry: self.save_custom_reward(k, en.get()))
                entry.bind("<Return>", lambda e, k=reward_key, en=entry: self.save_custom_reward(k, en.get()))

        # --- Bouton Enregistrer ---
        def save_and_close():
            # On force la sauvegarde de chaque champ
            for key, en in all_entries:
                self.save_custom_reward(key, en.get())
            popup.destroy()

        save_btn = ctk.CTkButton(
            popup, 
            text="Enregistrer et Fermer", 
            command=save_and_close,
            font=self.font_widget,
            fg_color=THEME["accent_color"],
            hover_color=THEME["hover_color"],
            text_color="BLACK"
        )
        # On place le bouton sur la ligne après le dernier niveau, centré
        save_btn.grid(row=len(LEVELS) + 1, column=0, columnspan=len(columns) + 1, pady=20)
        
    def save_custom_reward(self, key, value):
        if "custom_rewards" not in self.data_manager.data:
            self.data_manager.data["custom_rewards"] = {}
        
        # On n'enregistre que si la valeur a changé
        self.data_manager.data["custom_rewards"][key] = value
        self.data_manager.save_data()
        print(f"Sauvegardé : {key} -> {value}")
        

    def bind_all_children(self, widget, callback):
        """Fonction récursive pour lier l'événement, en évitant les popups"""
        # On lie l'événement au widget actuel
        widget.bind("<Button-1>", callback)
        
        for child in widget.winfo_children():
            # IMPORTANT : On ne lie PAS les événements aux fenêtres surgissantes
            # Sinon, cliquer sur "OK" dans un popup déclenche le tableau derrière.
            if not isinstance(child, ctk.CTkToplevel):
                self.bind_all_children(child, callback)



    def check_total_rewards(self):
        """Vérifie si tous les badges ont atteint au moins un certain palier"""
        player_data = self.data_manager.data.get("player", {})
        
        for level_name in LEVELS[1:]:  # On commence après "Fer"
            target_index = LEVELS.index(level_name)
            all_reached = True
            
            for badge in BADGES:
                # On récupère le niveau actuel du badge
                _, current_level, _ = self.get_badge_progress(badge["type"])
                current_index = LEVELS.index(current_level)
                
                # Si UN SEUL badge est en dessous du palier cible, on invalide ce palier
                if current_index < target_index:
                    all_reached = False
                    break
            
            if all_reached:
                # On utilise une clé unique pour ne pas redéclencher le pop-up
                badge_key = f"last_total_level_{level_name}"
                if not player_data.get(badge_key, False):
                    # On marque comme validé et on affiche
                    player_data[badge_key] = True
                    self.show_reward_popup("Total", level_name)
                    self.data_manager.save_data()
                    
                    