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
from dbnormalizer.core.normalizer.normalizer import Normalizer

app = Flask(__name__)
schema = []
db_structure = None


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
    global db_structure
    print(button)
    try:
        if button == "xmlButton":
            xml_data = request.form["data"]
            xml_structure = XMLImport(xml_data, False)
            xml_structure.init_objects()
            db_structure = None
            schema = xml_structure.get_schema()
            js_object = get_display_tables_js_object()
            return js_object
        elif button == "insertDBButton":
            url = request.form.get('url')
            username = request.form.get('user')
            pwd = request.form.get('pwd')
            db_name = request.form.get('dbName')
            schema_name = request.form.get('schema')
            db_structure = DBImport(url, username, pwd, schema_name, db_name)
            if None == db_structure.get_error():
                schema = db_structure.map_tables()
                js_object = get_display_tables_js_object()
                return js_object
            else:
                error = db_structure.get_error()
                return error
        elif button == "requestFD" or button == "attributeClosure":
            table_name = request.form['table']
            attrs = schema.get_table_attributes(table_name)
            js_object = get_attr_list_js(attrs)
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
                rhs.append(table.get_attribute_by_name(r))
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
                rhs.append(table.get_attribute_by_name(r))
            fd = table.get_fd_by_id(int(fd_id))
            fd.set_lhs(lhs)
            fd.set_rhs(rhs)
            return "success"
        elif button == "removeFDButton":
            table_name = request.form['table']
            fd_id = request.form['id']
            table = schema.get_table_by_name(table_name)
            fds = table.get_fds
            del fds[int(fd_id)]
            return "success"
        elif button == "minimalCover":
            table_name = request.form['table']
            table = schema.get_table_by_name(table_name)
            nf = NF(table)
            mc = nf.get_min_cover()
            js_object = get_display_fd_js_object(mc)
            return js_object
        elif button == "getAttributeClosure":
            table_name = request.form['table']
            table = schema.get_table_by_name(table_name)
            attributes = []
            attr_list = request.form['attributes'].split(',')
            for attr in attr_list:
                attributes.append(table.get_attribute_by_name(attr))
            nf = NF(table)
            ac = nf.get_attr_closure(attributes)
            return get_attr_list_js(ac)
        elif button == "candidateKeys":
            table_name = request.form['table']
            table = schema.get_table_by_name(table_name)
            nf = NF(table)
            ck = nf.get_candidate_keys()
            return get_candidate_keys_js(ck)
        elif button == "normalForm":
            table_name = request.form['table']
            table = schema.get_table_by_name(table_name)
            nf = NF(table)
            current_nf = nf.determine_nf()
            violated_fd = nf.get_violating_fds()
            js_object = get_nf_js_object(current_nf, violated_fd)

            return js_object
        elif button == "checkfds":
            table_name = request.form['table']
            table = schema.get_table_by_name(table_name)
            fds_hold_object = db_structure.check_fds_hold(table.get_fds, table.get_name)
            js_object = get_hold_fds_js_object(fds_hold_object)
            return js_object
        elif button == "normalizer":
            table_name = request.form['table']
            table = schema.get_table_by_name(table_name)
            nf = NF(table)
            current_nf = nf.determine_nf()
            if current_nf == 'BCNF':
                return 'false'
            normalization = Normalizer(nf)
            normalization.decomposition()
            if normalization.get_nf3_is_not_bcnf():
                table_nf3 = normalization.get_new_tables_nf3()
                table_bcnf = normalization.get_new_tables_bcnf()
                js_object = get_normalized_tables_js_object({'3nf': table_nf3, 'bcnf': table_bcnf})
            else:
                table = normalization.get_new_tables_nf3()
                js_object = get_normalized_tables_js_object({'3nf': table})
            return js_object
        return "Undefined button: " + button
    except Exception as e:
        print(str(e))


def get_hold_fds_js_object(fds_hold_object):
    fds_hold = get_fds_list(fds_hold_object['hold'])
    fds_not_hold = get_fds_list(fds_hold_object['not_hold'])
    return json.dumps({'hold': fds_hold, 'not_hold': fds_not_hold})


def get_nf_js_object(nf, violated_fds):
    fds_obj = get_fds_list(violated_fds)
    return json.dumps({'nf': nf, 'violated_fds': fds_obj})


def get_candidate_keys_js(keys):
    js_object = []
    for key in keys:
        attr_list = []
        for attr in key:
            attr_list.append(attr.get_name)
        js_object.append(attr_list)
    return json.dumps(js_object)


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


def get_normalized_tables_js_object(tables):
    tables_data = {}
    if 'bcnf' in tables:
        tables_bcnf = tables['bcnf']
        tables_3nf = tables['3nf']
        tables_data['bcnf'] = []
        tables_data['3nf'] = []
        for table in tables_bcnf:
            table_structure = create_normalized_table_structure(table)
            tables_data['bcnf'].append(table_structure)
        for table in tables_3nf:
            table_structure = create_normalized_table_structure(table)
            tables_data['3nf'].append(table_structure)
    else:
        tables_3nf = tables['3nf']
        tables_data['3nf'] = []
        for table in tables_3nf:
            table_structure = create_normalized_table_structure(table)
            tables_data['3nf'].append(table_structure)
    return json.dumps(tables_data)


def create_normalized_table_structure(table):
    attributes = get_attributes_list(table.get_attributes)
    fds = get_fds_list(table.get_fds)
    f_keys = []
    for f_key in table.get_foreign_keys():
        f_k = {'attr': f_key.get_attr(),
               'referenced_table': f_key.get_referenced_table(),
               'referenced_attribute': f_key.get_referenced_attribute()}
        f_keys.append(f_k)
    t_nf = NF(table)
    cks = t_nf.get_candidate_keys()
    candidate_keys = []
    for ck in cks:
        ck_a = [a.get_name for a in ck]
        candidate_keys.append(ck_a)
    table_data = {
        'name': table.get_name,
        'attributes': attributes,
        'fds': fds,
        'f_key': f_keys,
        'candidate_keys': candidate_keys
    }
    return table_data


def get_attr_list_js(attributes):
    attr_list = []
    for attr in attributes:
        attr_list.append(attr.get_name)
    return json.dumps(attr_list)

if __name__ == "__main__":
    t = threading.Thread(target=open_browser)
    t.daemon = True
    t.start()
    app.run()
