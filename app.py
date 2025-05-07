from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "secret123"  # needed for session

API_URL = "https://chatgpt-42.p.rapidapi.com/chatgpt"
HEADERS = {
    "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
    "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
    "Content-Type": "application/json"
}

@app.route("/", methods=["GET", "POST"])
def chat():
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        user_msg = request.form["message"]
        payload = {
            "messages": [{"role": "user", "content": user_msg}],
            "web_access": False
        }
        try:
            res = requests.post(API_URL, headers=HEADERS, json=payload)
            data = res.json()
            ai_msg = data.get("result", {}).get("content", "Unexpected response")
        except Exception as e:
            ai_msg = f"Error: {str(e)}"

        session["history"].append({"user": user_msg, "ai": ai_msg})
        session.modified = True
        return redirect("/")

    return render_template("index.html", history=session["history"])

@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
