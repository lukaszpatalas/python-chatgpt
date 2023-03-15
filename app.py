import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        term = request.form["term"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(term),
            temperature=0.6,
            max_tokens=50,
            n=3,
            top_p=0.9,
            stop=["\n"],
            echo=False
        )
        names = response.choices[0].text.strip().split(', ')
        return redirect(url_for("index", result=names))

    result = request.args.getlist("result")
    return render_template("index.html", result=result)


def generate_prompt(term):
    return """Suggest three names for an oil and gas exploration site or a renewable energy project. In one of these names, make reference to Asco, or ConocoPhillips, or Shell, or BP, or ExxonMobil, or Total

Industry Term: Upstream
Names: Gulf of Mexico Exploration, Shale Basin Ventures, Arctic Offshore Drilling
Industry Term: Midstream
Names: Coastal Pipeline Network, Rocky Mountain Storage Hub, Ethanol Transportation Solutions
Industry Term: Downstream
Names: Gulf Coast Refinery, Western Canadian Petrochemical Plant, Renewable Energy Refining Complex
Industry Term: {}
Names:""".format(
        term.capitalize()
    )
