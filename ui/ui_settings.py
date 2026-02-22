import customtkinter as ctk
import shutil
import os
from datetime import datetime
from ui.styles import THEME, ALL_THEMES, ALL_FONTS, set_active_theme, set_active_font, get_fonts

class SettingsPopup(ctk.CTkToplevel):
    def __init__(self, app, data_manager):
        super().__init__(app)
        self.app = app
        self.data_manager = data_manager
        
        current_theme = self.data_manager.data.get("settings", {}).get("theme", "Dark Standard")
        current_font = self.data_manager.data.get("settings", {}).get("font_family", "Cambria")
        
        self.title("Paramètres Généraux")
        self.geometry("500x600")
        self.configure(fg_color=THEME["bg_main"])
        self.grab_set()

        # --- SECTION 1 : THÈMES ---
        ctk.CTkLabel(self, text="🎨 Personnalisation du Thème", font=app.font_widget, text_color=THEME["text_primary"]).pack(pady=(20, 10))
        self.theme_option = ctk.CTkOptionMenu(
            self, 
            values=list(ALL_THEMES.keys()),
            command=self.change_theme,
            fg_color=THEME["accent_color"],
            button_color=THEME["accent_color"],
            text_color="black"
        )
        self.theme_option.pack(pady=5)
        self.theme_option.set(current_theme)

        # --- SECTION 2 : POLICE ---
        ctk.CTkLabel(self, text="🔤 Police d'écriture", font=app.font_widget, text_color=THEME["text_primary"]).pack(pady=(20, 10))
        self.font_option = ctk.CTkOptionMenu(
            self, 
            values=ALL_FONTS,
            command=self.change_font,
            fg_color=THEME["accent_color"],
            button_color=THEME["accent_color"],
            text_color="black"
        )
        self.font_option.pack(pady=5)
        self.font_option.set(current_font)

        # --- SECTION 3 : ACTIONS DONNÉES ---
        ctk.CTkLabel(self, text="⚙️ Gestion des Données", font=app.font_widget, text_color=THEME["text_primary"]).pack(pady=(30, 10))
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10, padx=20, fill="x")

        # Bouton Backup
        ctk.CTkButton(
            btn_frame, text="💾 Sauvegarder (Backup)", 
            command=self.backup_data,
            fg_color="#3498db",
            text_color="black"
        ).pack(side="left", padx=5, expand=True)

        # Bouton Reset
        ctk.CTkButton(
            btn_frame, text="⚠️ Réinitialiser", 
            command=self.reset_data,
            fg_color="#e74c3c", hover_color="#c0392b",
            text_color="black"
        ).pack(side="left", padx=5, expand=True)

        # Idées Bonus : Stats Rapides
        ctk.CTkButton(
            self, text="📊 Exporter l'historique (CSV)", 
            command=self.export_csv,
            fg_color=THEME["accent_color"],
            text_color="black"
        ).pack(pady=10)

        ctk.CTkButton(self, text="Fermer", command=self.destroy, 
                      text_color="black", 
                      fg_color=THEME["accent_color"]).pack(side="bottom", pady=20)

    def change_theme(self, choice):
        set_active_theme(choice, self.data_manager)
        self.app.apply_theme_globally()
        self.app.refresh_ui() # On appelle la fonction de refresh globale de ton app
        self.destroy() # On ferme pour appliquer proprement
        self.app.open_settings()
        
    

    def change_font(self, choice):
        from ui.styles import set_active_font, get_fonts
        # 1. Mise à jour de la config et du JSON
        set_active_font(choice, self.data_manager)
        
        new_fonts = get_fonts()
        self.app.fonts = new_fonts
        self.app.font_title = new_fonts["title"]
        self.app.font_widget = new_fonts["widget"]
        self.app.font_small = new_fonts["small"]
        
        # 2. Reset de l'UI pour appliquer la nouvelle police partout
        # On utilise la même méthode de "Gros Reset" que pour le thème
        self.app.apply_theme_globally() 
        self.destroy()
        self.app.open_settings()


    def backup_data(self):
        filename = f"backup_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        shutil.copy("data.json", filename)
        print(f"Backup créé : {filename}")

    def reset_data(self):
        # Ajouter un message de confirmation serait idéal ici
        self.data_manager.data = {"player": {"xp": 0, "level": 1}, "tasks": {}, "history": {}, "quests": {}}
        self.data_manager.save_data()
        self.app.refresh_ui()
        self.destroy()

    def export_csv(self):
        # Idée : Transformer le JSON history en fichier .csv lisible sur Excel
        import pandas as pd
        df = pd.DataFrame(list(self.data_manager.data.get("history", {}).items()), columns=["Date", "XP"])
        df.to_csv("mon_evolution_xp.csv", index=False)
        print("Export CSV réussi !")
        
