__author__ = 'Maira'
from flask import Flask, render_template, request
import webbrowser
import threading
import time
from dbnormalizer.core.importdata.XMLImport import XMLImport
from dbnormalizer.core.importdata.DBImport import DBImport
import json
from dbnormalizer.core.util.funcs import get_attributes_list, get_fds_list
from dbnormalizer.core.table.FD import FD
from dbnormalizer.core.normalizer.NF import NF

app = Flask(__name__)
schema = []


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
    global schema
    print(button)
    try:
        if button == "xmlButton":
            xml_data = request.form["data"]
            xml_structure = XMLImport(xml_data, False)
            xml_structure.init_objects()
            schema = xml_structure.get_schema()
            js_object = get_display_tables_js_object()
            return js_object
        elif button == "insertDBButton":
            url = request.form.get('url')
            username = request.form.get('user')
            pwd = request.form.get('pwd')
            db_name = request.form.get('dbName')
            schema_name = request.form.get('schema')
            schema_structure = DBImport(url, username, pwd, schema_name, db_name)
            if None == schema_structure.get_error():
                schema = schema_structure.map_tables()
                js_object = get_display_tables_js_object()
                return js_object
            else:
                error = schema_structure.get_error()
                print(error)
                return error
        elif button == "requestFD":
            table_name = request.form['table']
            attrs = schema.get_table_attributes(table_name)
            js_object = get_add_fds_js_object(attrs)
            return js_object
        elif button == "insertFDButton":
            table_name = request.form['table']
            lhs = []
            rhs = []
            lhs_list = request.form['lhs'].split(',')
            rhs_list = request.form['rhs'].split(',')
            table = schema.get_table_by_name(table_name)
            for l in lhs_list:
                lhs.append(table.get_attribute_by_name(l))
            for r in rhs_list:
                lhs.append(table.get_attribute_by_name(r))
            fd = FD(lhs, rhs)
            table.add_fd(fd)
            return "success"
        elif button == "editFDButton":
            table_name = request.form['table']
            lhs_list = request.form['lhs'].split(',')
            rhs_list = request.form['rhs'].split(',')
            lhs = []
            rhs = []
            fd_id = request.form['id']
            table = schema.get_table_by_name(table_name)
            for l in lhs_list:
                lhs.append(table.get_attribute_by_name(l))
            for r in rhs_list:
                lhs.append(table.get_attribute_by_name(r))
            fd = table.get_fd_by_id(int(fd_id))
            fd.set_lhs(lhs)
            fd.set_rhs(rhs)
            return "success"
        elif button == "minimalCover":
            table_name = request.form['table']
            table = schema.get_table_by_name(table_name)
            nf = NF(table)
            mc = nf.get_min_cover()
            js_object = get_display_fd_js_object(mc)
            return js_object
        return "Undefined button: " + button
    except Exception as e:
        print(str(e))


def get_display_fd_js_object(fds):
    fds_obj = get_fds_list(fds)
    return json.dumps(fds_obj)


def get_display_tables_js_object():
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


def get_add_fds_js_object(attributes):
    attr_list = []
    for attr in attributes:
        attr_list.append(attr.get_name)
    return json.dumps(attr_list)

if __name__ == "__main__":
    t = threading.Thread(target=open_browser)
    t.daemon = True
    t.start()
    app.run()
