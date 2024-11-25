from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json

app = Flask(__name__)
DATA_FILE = "discord_servers.json"
SECRET_CODE = "7895123654"  # Replace with your chosen admin code

# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_servers():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_servers(servers):
    with open(DATA_FILE, "w") as f:
        json.dump(servers, f, indent=4)

@app.route("/")
def index():
    servers = load_servers()
    return render_template("index.html", servers=servers)

@app.route("/add", methods=["GET", "POST"])
def add_server():
    if request.method == "POST":
        admin_code = request.form.get("admin_code")
        if admin_code != SECRET_CODE:
            return "Unauthorized Access!", 403

        image_url = request.form.get("image_url")
        invite_link = request.form.get("invite_link")

        if image_url and invite_link:
            servers = load_servers()
            servers.append({"image_url": image_url, "invite_link": invite_link})
            save_servers(servers)
            return redirect(url_for("index"))
        else:
            return "Both image URL and invite link are required!", 400
    return render_template("add_server.html")

if __name__ == '__main__':
    # Set the port dynamically from the environment, with a fallback to 5000 for local dev
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
