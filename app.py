from pipeline import work
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')


@app.route("/api/<topic>")
def api_point(topic):
    reply = work(100, topic)
    return {"data": reply}


if __name__ == '__main__':
    app.run(debug=False)
