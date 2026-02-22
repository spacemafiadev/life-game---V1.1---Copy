# ui/ui_center_middle.py
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import customtkinter as ctk
from datetime import datetime, date
from ui.styles import THEME

# Constantes des noms de graphiques
CHART_XP = "Évolution XP"
CHART_TASKS = "Top Tâches"
CHART_RATIO = "Taux de Succès"

def update_middle(app):
    """Affiche le graphique sélectionné avec gestion du mode Polaire."""
    for widget in app.middle_frame.winfo_children():
        widget.destroy()

    current_chart = getattr(app, "active_chart", CHART_XP)
    history = app.data_manager.data.get("history", {})

    if not history:
        ctk.CTkLabel(app.middle_frame, text="En attente de données...", 
                     font=app.font_widget).pack(expand=True)
        return

    # --- CRÉATION DE LA FIGURE ---
    # Pour le radar, on doit spécifier 'polar' dès le départ

    fig = plt.figure(figsize=(8, 3.5), facecolor=THEME["bg_card"])
    

    ax = fig.add_subplot(111)

    ax.set_facecolor(THEME["bg_card"])
    
    plt.rcParams.update({
        'text.color': THEME["text_primary"],
        'axes.labelcolor': THEME["text_primary"],
        'xtick.color': THEME["text_primary"],
        'ytick.color': THEME["text_primary"]
    })

    # --- ROUTAGE ---
    tasks = app.data_manager.get_tasks()
    if current_chart == CHART_XP:
        render_xp_chart(ax, history)
    elif current_chart == CHART_TASKS:
        render_tasks_chart(ax, tasks)
    elif current_chart == CHART_RATIO:
        render_ratio_chart(ax, app.data_manager)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=app.middle_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.configure(bg=THEME["bg_card"], highlightthickness=0)
    canvas_widget.pack(fill="both", expand=True)
    canvas_widget.bind("<Button-1>", lambda e: open_chart_selector(app))

# --- FONCTIONS DE RENDU (Modifiées pour la stabilité) ---

def render_xp_chart(ax, history):
    xp_df = pd.DataFrame(list(history.items()), columns=["date", "xp"])
    xp_df["xp"] = xp_df["xp"].astype(int)
    xp_df["date"] = pd.to_datetime(xp_df["date"])
    xp_df = xp_df.sort_values("date").tail(30)
    ax.bar(xp_df["date"].dt.strftime("%d-%m"), xp_df["xp"], color=THEME["accent_color"])
    ax.set_title("Progression XP (30j)")

def render_tasks_chart(ax, tasks):
    task_counts = {name: len(t.get("history", {})) for name, t in tasks.items() if len(t.get("history", {})) > 0}
    top = dict(sorted(task_counts.items(), key=lambda x: x[1], reverse=True)[:5])
    if top:
        ax.pie(list(top.values()), labels=list(top.keys()), autopct='%1.0f%%',
               colors=plt.cm.Pastel1(np.linspace(0, 1, len(top))))
        ax.set_title("Top 5 Tâches")

def render_ratio_chart(ax, data_manager):
    tasks = data_manager.get_tasks()
    today = date.today().isoformat()
    done = sum(1 for t in tasks.values() if t.get("history", {}).get(today))
    total = max(1, len(tasks))
    ax.pie([done, total-done], colors=[THEME["accent_color"], "#333333"], startangle=90, wedgeprops={'width': 0.4})
    ax.text(0, 0, f"{int((done/total)*100)}%", ha='center', va='center', fontsize=20, fontweight='bold')

# --- SÉLECTEUR (Agrandi pour 5 choix) ---

def open_chart_selector(app):
    selector = ctk.CTkToplevel(app)
    selector.title("Choisir un graphique")
    selector.geometry("900x250") # Plus large pour 5 boutons
    selector.configure(fg_color=THEME["bg_main"])
    selector.grab_set()

    ctk.CTkLabel(selector, text="Sélectionner une analyse", font=app.font_title, text_color=THEME["text_primary"]).pack(pady=15)
    container = ctk.CTkFrame(selector, fg_color="transparent")
    container.pack(expand=True, fill="both", padx=10, pady=10)

    charts = [
        {"name": CHART_XP, "icon": "📈"},
        {"name": CHART_TASKS, "icon": "🏆"},
        {"name": CHART_RATIO, "icon": "✅"}
    ]

    for item in charts:
        btn = ctk.CTkButton(
            container,
            text=f"{item['icon']}\n{item['name']}",
            font=app.font_widget,
            fg_color=THEME["bg_card"],
            hover_color=THEME["accent_color"],
            text_color=THEME["text_primary"],
            command=lambda n=item['name']: select_and_close(app, selector, n)
        )
        btn.pack(side="left", expand=True, padx=5, fill="both")

def select_and_close(app, window, chart_name):
    app.active_chart = chart_name
    window.destroy()
    update_middle(app)