# styles.py
import customtkinter as ctk

# --- LES 11 THÈMES ---

# 1. Thème Clair Simple (Clean & Professional)
THEME_LIGHT = {
    "bg_main": "#F0F2F5",
    "bg_card": "#FFFFFF",
    "text_primary": "#1C1E21",
    "accent_color": "#007BFF",
    "hover_color": "#0056b3",
    "border_color": "#DADDE1"
}

# 2. Thème Dark Standard (Windows Style)
THEME_DARK = {
    "bg_main": "#202020",
    "bg_card": "#2C2C2C",
    "text_primary": "#FFFFFF",
    "accent_color": "#0078D4",
    "hover_color": "#2B88D8",
    "border_color": "#333333"
}

# 3. Nord (Bleu Arctique Sombre - Très populaire)
THEME_NORD = {
    "bg_main": "#2E3440",
    "bg_card": "#3B4252",
    "text_primary": "#ECEFF4",
    "accent_color": "#88C0D0",
    "hover_color": "#81A1C1",
    "border_color": "#434C5E"
}

# 4. Dracula (Violet & Rose Sombre)
THEME_DRACULA = {
    "bg_main": "#282A36",
    "bg_card": "#44475A",
    "text_primary": "#F8F8F2",
    "accent_color": "#BD93F9",
    "hover_color": "#FF79C6",
    "border_color": "#6272A4"
}

# 5. Cyberpunk (Néon contrasté)
THEME_CYBERPUNK = {
    "bg_main": "#0D0221",
    "bg_card": "#261447",
    "text_primary": "#00F5D4",
    "accent_color": "#FF0054",
    "hover_color": "#9D00FF",
    "border_color": "#542E71"
}

# 6. Forest (Vert Nature Apaisant)
THEME_FOREST = {
    "bg_main": "#1B241B",
    "bg_card": "#2D3B2D",
    "text_primary": "#E8F5E9",
    "accent_color": "#66BB6A",
    "hover_color": "#4CAF50",
    "border_color": "#3E4F3E"
}

# 7. Pastel Peach (Doux et chaleureux)
THEME_PEACH = {
    "bg_main": "#FFF5F5",
    "bg_card": "#FFE3E3",
    "text_primary": "#4A4A4A",
    "accent_color": "#FF8E8E",
    "hover_color": "#FF7171",
    "border_color": "#FAD0C4"
}

# 8. Midnight Gold (Luxe Sombre)
THEME_MIDNIGHT = {
    "bg_main": "#0B0C10",
    "bg_card": "#1F2833",
    "text_primary": "#C5C6C7",
    "accent_color": "#66FCF1",
    "hover_color": "#45A29E",
    "border_color": "#1F2833"
}

# 9. Lavender Mist (Pastel Sombre)
THEME_LAVENDER = {
    "bg_main": "#1E1E2E",
    "bg_card": "#302D41",
    "text_primary": "#D9E0EE",
    "accent_color": "#C9CBFF",
    "hover_color": "#B5BFE3",
    "border_color": "#575268"
}

# 10. Oceanic (Profondeur Bleue)
THEME_OCEANIC = {
    "bg_main": "#0F172A",
    "bg_card": "#1E293B",
    "text_primary": "#F1F5F9",
    "accent_color": "#38BDF8",
    "hover_color": "#0EA5E9",
    "border_color": "#334155"
}

# 11. Solarized Dark (Vintage Codeur)
THEME_SOLARIZED = {
    "bg_main": "#002B36",
    "bg_card": "#073642",
    "text_primary": "#93A1A1",
    "accent_color": "#268BD2",
    "hover_color": "#2AA198",
    "border_color": "#586E75"
}


ALL_THEMES = {
    "Dark Standard": THEME_DARK,
    "Light": THEME_LIGHT,
    "Nord": THEME_NORD,
    "Dracula": THEME_DRACULA,
    "Cyberpunk": THEME_CYBERPUNK,
    "Forest": THEME_FOREST,
    "Peach": THEME_PEACH,
    "Midnight": THEME_MIDNIGHT,
    "Lavender": THEME_LAVENDER,
    "Oceanic": THEME_OCEANIC,
    "Solarized": THEME_SOLARIZED
}

ALL_FONTS = ["Cambria", "Arial", "Consolas", "Segoe UI", "Courier New"]

THEME = {}
FONTS_CONFIG = {}

# --- FONCTIONS ---

def change_theme_color(new_color):
    THEME["bg_main"] = new_color

def set_active_theme(theme_name, data_manager):
    global THEME
    new_theme_colors = ALL_THEMES.get(theme_name, THEME_DARK)
    THEME.update(new_theme_colors)
    
    # Sauvegarde dans le JSON
    if "settings" not in data_manager.data:
        data_manager.data["settings"] = {}
    data_manager.data["settings"]["theme"] = theme_name
    data_manager.save_data()

def init_fonts():
    update_fonts("Cambria")

def get_fonts():
    """Retourne le dictionnaire de polices actuel."""
    return FONTS_CONFIG

def update_fonts(family_name):
    """Met à jour les objets polices sans changer leurs noms de clés."""
    global FONTS_CONFIG
    FONTS_CONFIG.update({
        "title": ctk.CTkFont(family=family_name, size=34, weight="bold"),
        "widget": ctk.CTkFont(family=family_name, size=24),
        "small": ctk.CTkFont(family=family_name, size=18)
    })
    
def set_active_font(font_name, data_manager):
    """Change la police globalement et sauvegarde dans le JSON."""
    update_fonts(font_name)
    
    # Sauvegarde dans le JSON
    if "settings" not in data_manager.data:
        data_manager.data["settings"] = {}
    data_manager.data["settings"]["font_family"] = font_name
    data_manager.save_data()
    
    
# THEME.update(THEME_DARK)
# init_fonts()