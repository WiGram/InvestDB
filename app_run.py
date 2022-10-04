from shiny import App
from app_ui import app_ui
from app_server import server

# Combine into a shiny app.
# Note that the variable must be "app".

# To run:
# 
# 1. Open Microsoft PowerShell
# 2. Go to G-drive, type: G:
# 3. Go to folder, type: cd Development\shiny_app_in_python
# 4. Run app, type: shiny run --reload /app_run.py
app = App(app_ui, server)
 