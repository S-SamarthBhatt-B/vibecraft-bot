import threading
import os

# 🟢 Run the bot
def run_bot():
    os.system("python main.py")  # 🔁 use python instead of python3

# 🟠 Run the dashboard
def run_web():
    os.system("python app.py")  # 🔁 same here

# Threads
t1 = threading.Thread(target=run_bot)
t2 = threading.Thread(target=run_web)

t1.start()
t2.start()

t1.join()
t2.join()