from ui.ui_main import GamificationApp
from core.task_manager import TaskManager
from core.quest_manager import QuestManager
from core.xp_system import XPSystem
from core.stats import Stats
from core.data_manager import DataManager

DATA_FILE = "data.json"

# Charge ou crée le JSON
data_manager = DataManager(DATA_FILE)
data = data_manager.data

# Managers
task_manager = TaskManager(data)
quest_manager = QuestManager(data)
xp_system = XPSystem(data)
stats = Stats(data)

# Lancement UI
app = GamificationApp(
    task_manager=task_manager,
    quest_manager=quest_manager,
    xp_system=xp_system,
    stats=stats,
    data_file=DATA_FILE
)
app.mainloop()


