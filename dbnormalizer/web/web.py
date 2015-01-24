__author__ = 'Maira'
from flask import Flask, render_template, request
import webbrowser
import threading
import time
from dbnormalizer.core.importdata.XMLImport import XMLImport
import json
from dbnormalizer.core.util.funcs import get_attributes_list, get_fds_list

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
    Upload handler
    :param button: the domId of the button that was clicked
    :return:
    """
    print(button)

    if button == "xmlButton":
        xml_data = request.form["data"]
        xml_structure = XMLImport(xml_data)
        xml_structure.init_objects()
        schema = xml_structure.get_schema()
        js_object = get_js_object(schema)
        return js_object
    elif button == "insertDBButton":
        url = request.form.get('url')
        username = request.form.get('user')
        pwd = request.form.get('pwd')
        #TODO implement
        return "success"
    return "Undefined button: " + button


def get_js_object(schema):
    tables = schema.get_tables()
    tables_data = []
    for table in tables:
        attributes = get_attributes_list(table.get_attributes)
        fds = get_fds_list(table.get_fds)
        tables_data.append({
            'name': table.get_name,
            'attributes': attributes,
            'fds': fds
        })
    return json.dumps(tables_data)

if __name__ == "__main__":
    t = threading.Thread(target=open_browser)
    t.daemon = True
    t.start()
    app.run()
