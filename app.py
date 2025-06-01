from flask import Flask, request, render_template
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    names = []
    if request.method == "POST":
        cuisine = request.form["cuisine"]
        prompt = f"Suggest 5 creative restaurant names for a {cuisine} restaurant:"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a branding expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        output = response['choices'][0]['message']['content']
        names = [line.strip("-• ") for line in output.split("\n") if line.strip()]
    return render_template("index.html", names=names)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
