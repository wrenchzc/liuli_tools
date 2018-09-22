from flask import Flask
from flask import render_template
from flask import Response, send_file
from flask import request
from tempfile import gettempdir
import time
from excel_merge.excel_handler import merge_excel

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/upload_excel', methods=['POST'])
def do_upload_excel():
    file_data = request.files.get('excelfile')
    file_name = "{dir}/{index}.xlsx".format(dir=gettempdir(), index=round(time.time()))
    with open(file_name, "wb") as f:
        content = file_data.read()
        f.write(content)

    tmp_file = merge_excel(file_name)

    return send_file(tmp_file, as_attachment=True)


if __name__ == '__main__':
    app.run()
