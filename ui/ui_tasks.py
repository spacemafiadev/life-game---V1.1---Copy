import customtkinter as ctk
from core.stats import Stats
from datetime import date
from ui.styles import THEME

def build_tasks_ui(app):
    
    difficulty_colors = {
        "facile": "#4CAF50",
        "moyen": "#FFA726",
        "difficile": "#EF5350"
    }

    # Supprime les anciennes frames
    for widget in app.left_frame.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            widget.destroy()

    app.task_widgets.clear()

    tasks = app.data_manager.get_tasks()
    stats = Stats(app.data_manager.data)
    stats.refresh()  # recalculer streaks avant affichage


    for task_name, task in tasks.items():
        row = ctk.CTkFrame(app.left_frame, fg_color=THEME["bg_card"])
        row.pack(fill="x", padx=10, pady=4)
        
        # Configuration des colonnes fixes
        row.grid_columnconfigure(0, minsize=40)    # Checkbox
        row.grid_columnconfigure(1, weight=1)      # Nom
        row.grid_columnconfigure(2, minsize=80)   # Difficulté
        row.grid_columnconfigure(3, minsize=120)   # Streak
        row.grid_columnconfigure(4, minsize=30)    # Bouton supprimer

        # ---------- Checkbox ----------
        done_today = app.data_manager.is_task_done_today(task_name)
        var = ctk.BooleanVar(value=done_today)
        cb = ctk.CTkCheckBox(row, text="", variable=var, width=28,
                             border_color=THEME["accent_color"],
                             hover_color=THEME["hover_color"],
                             checkmark_color=THEME["text_primary"]
                             )
        cb.grid(row=0, column=0, sticky="w")

        if done_today:
            cb.select()
            cb.configure(state="disabled")
        else:
            cb.configure(command=lambda tn=task_name, cb=cb: complete_task(app, tn, cb))

        # ---------- Label texte ----------
        name_label = ctk.CTkLabel(
            row,
            text=task_name,
            font=app.font_widget,
            wraplength=150,
            justify="left",
            anchor="w",
            text_color=THEME["text_primary"]
        )
        name_label.grid(row=0, column=1, sticky="w", padx=(5, 20))

        # ---------- Label difficulté colorée ----------
        diff_label = ctk.CTkLabel(
            row,
            text=task["difficulty"].capitalize(),
            text_color=difficulty_colors.get(task["difficulty"].lower(), "gray"),
            font=app.font_widget
        )
        diff_label.grid(row=0, column=2, sticky="w", padx=(0, 20))

        # ---------- Label streak ----------
        streak_task = task.get("streak", 0)
        mult_task = 1 + 0.1 * streak_task  # 0.1 par jour
        streak_label = ctk.CTkLabel(
            row,
            text=f"Streak: {streak_task} (x{mult_task:.1f})",
            font=app.font_widget,
            text_color=THEME["text_primary"]
        )
        streak_label.grid(row=0, column=3, sticky="w", padx=(0, 20))


        # ---------- Bouton supprimer ----------
        delete_btn = ctk.CTkButton(
            row, text="✕", width=28,
            command=lambda tn=task_name: delete_task(app, tn),
            font=app.font_widget,   
            text_color=THEME["text_primary"],         
            hover_color=THEME["hover_color"]
        )
        delete_btn.grid(row=0, column=4, sticky="w")

        app.task_widgets.append(cb)
        
def complete_task(app, task_name, checkbox):

    checkbox.select()
    checkbox.configure(state="disabled")

    # Marque la tâche faite
    app.data_manager.mark_task_done(task_name)

    # Récupère la tâche
    task = app.data_manager.get_tasks()[task_name]

    # --- Calcul XP ---
    xp_base = app.task_manager.calculate_xp_for_task(task)
    print("[UI_TASK DEBUG] xp_base =", xp_base)
    
    total_multiplier = app.xp_system.calculate_multiplier(task)
    print("[UI_TASK DEBUG] total_multiplier =", total_multiplier)
    
    xp_gain = xp_base * total_multiplier
    xp_gain = round(xp_gain)
    print("[UI_TASK DEBUG] xp_gain =", xp_gain)

    # Ajoute l'XP à l'historique et au joueur
    today = date.today().isoformat()
    app.data_manager.data.setdefault("history", {})
    app.data_manager.data["history"].setdefault(today, 0)
    app.data_manager.data["history"][today] += xp_gain
    app.data_manager.data["player"]["xp"] += xp_gain

    print(f"[UI_TASK DEBUG] Total XP after task: {app.data_manager.data['player']['xp']}")

    # --- Stats : recalcul des streaks ---
    stats = Stats(app.data_manager.data)
    stats.refresh()

    # Sauvegarde
    app.data_manager.save_data()

    # Rafraîchit l'UI
    app.refresh_ui()

def delete_task(app, task_name):
    """Supprime la tâche et rebuild UI immédiatement"""
    app.data_manager.remove_task(task_name)
    build_tasks_ui(app)  # reconstruit la liste de tâches
    app.refresh_ui()     # met à jour le graphique/statistiques

def add_task_popup(app):
    popup = ctk.CTkToplevel(app)
    popup.title("Ajouter une tâche")
    popup.geometry("400x300")
    popup.configure(fg_color=THEME["bg_main"])
    popup.transient(app)
    popup.grab_set()

    ctk.CTkLabel(popup, text="Nom de la tâche", font=app.font_widget).pack(pady=10)
    name_entry = ctk.CTkEntry(popup, fg_color=THEME["bg_card"], border_color=THEME["border_color"])
    name_entry.pack(pady=5, padx=20, fill="x")

    ctk.CTkLabel(popup, text="Difficulté", font=app.font_widget, text_color=THEME["text_primary"]).pack(pady=10)
    difficulty_var = ctk.StringVar(value="Moyen")
    ctk.CTkOptionMenu(
        popup,
        values=["Facile", "Moyen", "Difficile"],
        variable=difficulty_var,
        fg_color=THEME["accent_color"],
        button_color=THEME["accent_color"],
        button_hover_color=THEME["hover_color"]
    ).pack(pady=5)

    def confirm():
        name = name_entry.get().strip()
        if not name:
            return
        app.data_manager.add_task(name, difficulty_var.get())
        build_tasks_ui(app)
        popup.destroy()

    ctk.CTkButton(popup, text="Ajouter", command=confirm, font=app.font_widget,
                  fg_color=THEME["accent_color"],
                  hover_color=THEME["hover_color"]).pack(pady=20)
