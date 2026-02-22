import customtkinter as ctk
from core.data_manager import DataManager
from datetime import date
from ui.styles import THEME

def build_quests_ui(app):
    """Reconstruit la zone des quêtes"""
    difficulty_colors = {
        "facile": "#4CAF50",
        "moyen": "#FFA726",
        "difficile": "#EF5350",
        "epic": "#9C27B0"
    }

    for widget in app.right_frame.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            widget.destroy()

    app.quest_widgets.clear()

    quests = app.data_manager.get_quests()

    for row_index, (quest_name, quest) in enumerate(quests.items()):
        row = ctk.CTkFrame(app.right_frame, fg_color=THEME["bg_card"])
        row.pack(fill="x", padx=10, pady=4)

        # colonnes fixes
        row.grid_columnconfigure(0, minsize=40)   # checkbox
        row.grid_columnconfigure(1, weight=1)     # nom
        row.grid_columnconfigure(2, minsize=120)  # difficulté
        row.grid_columnconfigure(3, minsize=40)   # delete

        done = app.data_manager.is_quest_done(quest_name)
        var = ctk.BooleanVar(value=done)

        cb = ctk.CTkCheckBox(
            row,
            text="",
            variable=var,
            width=28,
            border_color=THEME["accent_color"],
            hover_color=THEME["hover_color"],
            checkmark_color=THEME["text_primary"]
        )
        cb.grid(row=0, column=0, sticky="w")

        if done:
            cb.select()
            cb.configure(state="disabled")
        else:
            cb.configure(command=lambda qn=quest_name, cb=cb: complete_quest(app, qn, cb))

        name_label = ctk.CTkLabel(
            row,
            text=quest_name,
            font=app.font_widget,
            text_color=THEME["text_primary"],
            wraplength=150,
            justify="left",
            anchor="w"
        )
        name_label.grid(row=0, column=1, sticky="w", padx=5)

        diff_label = ctk.CTkLabel(
            row,
            text=quest["difficulty"].upper(),
            text_color=difficulty_colors.get(quest["difficulty"], "gray"),
            font=app.font_widget
        )
        diff_label.grid(row=0, column=2, sticky="w")

        delete_btn = ctk.CTkButton(
            row,
            text="✕",
            width=28,
            font=app.font_widget,
            text_color=THEME["text_primary"],
            hover_color=THEME["hover_color"],
            command=lambda qn=quest_name: delete_quest(app, qn)
        )
        delete_btn.grid(row=0, column=3, sticky="e")

        app.quest_widgets.append(cb)

def complete_quest(app, quest_name, checkbox):
    """Marque la quête comme complétée"""
    checkbox.select()
    checkbox.configure(state="disabled")
    app.data_manager.mark_quest_done(quest_name)
    
    app.data_manager.data["player"].setdefault("quests_completed_count", 0)
    app.data_manager.data["player"]["quests_completed_count"] += 1
    
    quest = app.data_manager.get_quests()[quest_name]
    xp_gain = app.quest_manager.calculate_xp_for_quest(quest)
    today = date.today().isoformat()
    app.data_manager.data["history"].setdefault(today, 0)
    app.data_manager.data["history"][today] += xp_gain
    app.data_manager.data["player"]["xp"] += xp_gain
    
    app.data_manager.save_data()
    app.refresh_ui()

def delete_quest(app, quest_name):
    """Supprime la quête et rebuild UI"""
    app.data_manager.remove_quest(quest_name)
    build_quests_ui(app)
    app.refresh_ui()

def add_quest_popup(app):
    """Popup pour ajouter une nouvelle quête"""
    popup = ctk.CTkToplevel(app)
    popup.title("Ajouter une quête")
    popup.geometry("400x300")
    popup.configure(fg_color=THEME["bg_main"])
    popup.transient(app)
    popup.grab_set()

    ctk.CTkLabel(popup, text="Nom de la quête", font=app.font_widget, text_color=THEME["text_primary"]).pack(pady=10)
    name_entry = ctk.CTkEntry(popup, fg_color=THEME["bg_card"], 
                              border_color=THEME["border_color"])
    name_entry.pack(pady=5, padx=20, fill="x")

    ctk.CTkLabel(popup, text="Difficulté", font=app.font_widget, text_color=THEME["text_primary"]).pack(pady=10)
    difficulty_var = ctk.StringVar(value="Moyen")
    ctk.CTkOptionMenu(
        popup,
        values=["Facile", "Moyen", "Difficile", "Epic"],
        variable=difficulty_var,
        fg_color=THEME["accent_color"],
        button_color=THEME["accent_color"],
        button_hover_color=THEME["hover_color"]
    ).pack(pady=5)

    def confirm():
        name = name_entry.get().strip()
        if not name:
            return
        app.data_manager.add_quest(name, difficulty_var.get())
        build_quests_ui(app)
        popup.destroy()

    ctk.CTkButton(popup, text="Ajouter", command=confirm, font=app.font_widget,
                  fg_color=THEME["accent_color"],
                  hover_color=THEME["hover_color"]).pack(pady=20)
