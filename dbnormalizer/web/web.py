__author__ = 'Maira'
from flask import Flask, render_template, request
import webbrowser
import threading
import time

app = Flask(__name__)


def open_browser():
    """
    opens the browser for "gui"
    """
    time.sleep(2)
    url = "http://localhost:5000"
    webbrowser.open(url)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/<button>", methods=["GET"])
def click(button):
    """
    Simple button click, only with GET
    :param button: the domId of the button that was clicked
    :return:
    """
    if button == "insertData":
        return "lol"

    return "test"


@app.route("/<button>", methods=["POST"])
def upload(button):
    """
    More complex button-click handler
    :param button: the domId of the button that was clicked
    :return:
    """
    if button == "xmlButton":
        xml = request.form["data"]
        #TODO implement stuff
        return xml

    return "nope"

if __name__ == "__main__":
    t = threading.Thread(target=open_browser)
    t.daemon = True
    t.start()
    app.run()
