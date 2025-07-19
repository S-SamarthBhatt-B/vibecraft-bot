import os
import json
import requests
from flask import Flask, session, redirect, url_for, request, render_template
from dotenv import load_dotenv
from urllib.parse import urlencode
import config

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

DISCORD_API_BASE = "https://discord.com/api"

# 🏠 Home Page
@app.route("/")
def home():
    return render_template("home.html", user=session.get("user"))

# 🔐 Login with Discord
@app.route("/login")
def login():
    params = {
        "client_id": config.CLIENT_ID,
        "redirect_uri": config.REDIRECT_URI,
        "response_type": "code",
        "scope": config.OAUTH_SCOPE
    }
    return redirect(f"{DISCORD_API_BASE}/oauth2/authorize?{urlencode(params)}")

# 🔁 OAuth2 Callback
@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return redirect(url_for("home"))

    data = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI,
        "scope": config.OAUTH_SCOPE
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(f"{DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)

    if r.status_code != 200:
        return "❌ Failed to get token from Discord.", 400

    token = r.json()
    session["token"] = token

    # 🔍 Fetch user info
    auth_headers = {
        "Authorization": f"{token['token_type']} {token['access_token']}"
    }
    user_resp = requests.get(f"{DISCORD_API_BASE}/users/@me", headers=auth_headers)
    if user_resp.status_code != 200:
        return "❌ Failed to fetch user information.", 400

    session["user"] = user_resp.json()
    return redirect(url_for("dashboard"))

# 🚪 Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# 📊 Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session or "token" not in session:
        return redirect(url_for("login"))

    headers = {
        "Authorization": f"{session['token']['token_type']} {session['token']['access_token']}"
    }

    r = requests.get(f"{DISCORD_API_BASE}/users/@me/guilds", headers=headers)
    if r.status_code != 200:
        return "❌ Failed to get user guilds", 400

    user_guilds = r.json()

    # Get bot guilds
    try:
        with open("bot_guilds.json", "r") as f:
            bot_guild_ids = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        bot_guild_ids = []

    # Only show mutual guilds
    mutual_guilds = [g for g in user_guilds if g["id"] in bot_guild_ids]

    return render_template("dashboard.html", user=session["user"], guilds=mutual_guilds)

# 📄 Terms of Service
@app.route("/terms")
def terms():
    return render_template("terms.html", user=session.get("user"))

# 🔐 Privacy Policy
@app.route("/privacy")
def privacy():
    return render_template("privacy.html", user=session.get("user"))

# ✅ Run App
if __name__ == "__main__":
    app.run(debug=True)
