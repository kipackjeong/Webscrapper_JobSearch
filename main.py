from flask import Flask, render_template, request, redirect
from scrappers.indeed import IndeedScrapper
from scrappers.stackoverflow import StackoverflowScrapper

app = Flask("JobSearchWeb")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if not word:
        return redirect("/")
    jobs = db.get(word)
    if not jobs:
        jobs = IndeedScrapper(word).extract_jobs()
        db[word] = jobs
    word = word.lower()
    return render_template("report.html",
                           jobs=jobs,
                           resultsNumber=len(jobs),
                           searchingBy=word)


@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
    except:
        return redirect("/")
