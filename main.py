# display solutions to NYT spelling bee

from flask import Flask, render_template
import solutions

app = Flask(__name__)

@app.route("/")
def index():

    return render_template('index.html', answers=solutions.answers, pangrams=solutions.pangrams,possible_words=solutions.possible_words,score=solutions.score)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8082, debug=False)