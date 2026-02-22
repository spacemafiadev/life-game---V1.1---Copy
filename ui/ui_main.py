import customtkinter as ctk
from core.data_manager import DataManager
from ui.ui_tasks import build_tasks_ui, add_task_popup
from ui.ui_quests import build_quests_ui, add_quest_popup
from ui.ui_center_high import CenterHigh
from ui.ui_center_middle import update_middle
from ui.ui_center_low import CenterLow
from ui.styles import THEME, get_fonts, update_fonts, set_active_theme


class GamificationApp(ctk.CTk):
    def __init__(self, task_manager, quest_manager, xp_system, stats, data_file):
        super().__init__()
        
        self.data_manager = DataManager(json_file=data_file)
        self.task_manager = task_manager
        self.quest_manager = quest_manager
        self.xp_system = xp_system
        self.stats = stats
        
        
        saved_theme = self.data_manager.data.get("settings", {}).get("theme", "Dark Standard")
        saved_font = self.data_manager.data.get("settings", {}).get("font_family", "Cambria")
        
        set_active_theme(saved_theme, self.data_manager) # Initialise le dictionnaire THEME
        update_fonts(saved_font) # Initialise FONTS_CONFIG

        self.title("Life Gamifier")
        self.geometry("1800x1000")
        self.configure(fg_color=THEME["bg_main"])
        
        # ---- Polices globales ----
        fonts = get_fonts()
        self.font_title = fonts["title"]
        self.font_widget = fonts["widget"]
        self.font_small = fonts["small"]
        
        self.fonts = get_fonts()
        self.font_title = self.fonts["title"]
        self.font_widget = self.fonts["widget"]
        
        self.create_ui()
        self.refresh_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        print("[DEBUG] Closing app...")
        try:
            self.data_manager.save_data()
            # On arrête proprement la boucle Tkinter avant de détruire
            self.quit()     # Arrête le mainloop
            self.destroy()  # Détruit la fenêtre
        except Exception as e:
            print(f"Erreur lors de la fermeture : {e}")

    def create_ui(self):
        self.task_widgets = []
        self.quest_widgets = []
    
        # ===== CONTENEUR VERTICAL GLOBAL =====
        self.root_column = ctk.CTkFrame(self, fg_color=THEME["bg_main"])
        self.root_column.pack(fill="both", expand=True)
    
        # ===== BANDEAU HAUT PLEINE LARGEUR =====
        self.top_bar = ctk.CTkFrame(self.root_column, height=210, fg_color=THEME["bg_main"])
        self.top_bar.pack(side="top", fill="x")
        self.top_bar.pack_propagate(False)
    
        self.center_high = CenterHigh(
            self.top_bar,
            self.data_manager,
            font_title=self.font_title,
            font_widget=self.font_widget
        )
    
        # ===== CONTENEUR PRINCIPAL HORIZONTAL =====
        self.main_row = ctk.CTkFrame(self.root_column, fg_color="transparent")
        self.main_row.pack(fill="both", expand=True)
    
        # ===== TACHES (GAUCHE) =====
        self.left_frame = ctk.CTkFrame(self.main_row, width=450, fg_color=THEME["bg_main"])
        self.left_frame.pack(side="left", fill="both", expand=True)
    
        ctk.CTkLabel(
            self.left_frame,
            text="Tâches journalières",
            font=self.font_title,
            text_color=THEME["text_primary"]
        ).pack(pady=10)
    
        ctk.CTkButton(
            self.left_frame,
            text="+ Ajouter tâche",
            font=self.font_widget,
            command=lambda: add_task_popup(self),
            fg_color=THEME["accent_color"],
            hover_color=THEME["hover_color"]
        ).pack(pady=10)
    
        # ===== CENTER =====
        self.center_frame = ctk.CTkFrame(self.main_row, width=900, fg_color="transparent")
        self.center_frame.pack(side="left", fill="both", expand=True)
        self.center_frame.pack_propagate(False)
    
        # ===== CENTER MILIEU : Graphiques =====
        self.middle_frame = ctk.CTkFrame(self.center_frame, fg_color=THEME["bg_card"])
        self.middle_frame.pack(side="top", fill="both", expand=True, pady=5)
    
        # ===== CENTER BAS : Badges =====
        self.center_bottom_frame = CenterLow(
            self.center_frame,
            self.data_manager,
            font_widget=self.font_widget,
            fg_color=THEME["bg_main"])
        
        self.center_bottom_frame.pack(side="bottom", fill="x", pady=5)
        self.center_bottom_frame.configure(height=180)
        self.center_bottom_frame.pack_propagate(False)
    
        # ===== QUETES (DROITE) =====
        self.right_frame = ctk.CTkFrame(self.main_row, width=450, fg_color=THEME["bg_main"])
        self.right_frame.pack(side="right", fill="both", expand=True)
    
        ctk.CTkLabel(
            self.right_frame,
            text="Quêtes",
            font=self.font_title,
            text_color=THEME["text_primary"]
        ).pack(pady=10)
    
        ctk.CTkButton(
            self.right_frame,
            text="+ Ajouter quête",
            font=self.font_widget,
            command=lambda: add_quest_popup(self),
            fg_color=THEME["accent_color"],
            hover_color=THEME["hover_color"]
        ).pack(pady=10)
    
        # ===== BUILD UI =====
        build_tasks_ui(self)
        build_quests_ui(self)
        update_middle(self)


    def refresh_ui(self):

        # Rebuild tâches
        build_tasks_ui(self)
        
        # Rebuild quêtes  <-- C’EST ÇA QUI MANQUAIT
        build_quests_ui(self)
        
        self.center_high.update()
        update_middle(self)  # met à jour graphiques du milieu
        self.center_bottom_frame.update_badges()


    def apply_theme_globally(self):
        """Met à jour les couleurs de TOUS les widgets existants"""

        # 1. On détruit TOUS les widgets attachés à la fenêtre principale
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkToplevel):
                continue
            widget.destroy()
    
        # 2. On réinitialise la couleur de fond de la fenêtre elle-même
        self.configure(fg_color=THEME["bg_main"])
    
        # 3. On relance la création de l'interface
        # Cela va recréer les frames, boutons, etc. avec les couleurs à jour de THEME
        self.create_ui()
        
        # 4. On rafraîchit les données (XP, tâches, etc.)
        self.refresh_ui()
    
    def _update_widget_colors(self, parent):
        for child in parent.winfo_children():
            try:
                # On adapte selon le type de widget
                if isinstance(child, ctk.CTkFrame):
                    # Si c'est une "carte", on utilise bg_card, sinon bg_main
                    color = THEME["bg_card"] if child.cget("fg_color") != "transparent" else "transparent"
                    child.configure(fg_color=color)
                
                elif isinstance(child, ctk.CTkLabel):
                    child.configure(text_color=THEME["text_primary"])
                    
                elif isinstance(child, ctk.CTkButton):
                    child.configure(fg_color=THEME["accent_color"], hover_color=THEME["hover_color"])
                    
                elif isinstance(child, ctk.CTkProgressBar):
                    child.configure(progress_color=THEME["accent_color"], fg_color=THEME["bg_card"])
                
                elif isinstance(child, ctk.CTkEntry):
                    child.configure(fg_color=THEME["bg_card"], text_color=THEME["text_primary"], border_color=THEME["border_color"])
    
                # Appel récursif pour les sous-enfants
                self._update_widget_colors(child)
            except:
                continue # Certains widgets n'ont pas toutes les options
                
                
    def open_settings(self):
        """Méthode pour ouvrir le popup de réglages."""
        from ui.ui_settings import SettingsPopup
        # On vérifie si un popup n'est pas déjà ouvert pour éviter les doublons
        if hasattr(self, "settings_window") and self.settings_window.winfo_exists():
            self.settings_window.lift()
            self.settings_window.focus_force()
        else:
            self.settings_window = SettingsPopup(self, self.data_manager)