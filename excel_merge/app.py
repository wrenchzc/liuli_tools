from flask import Flask
from flask import render_template
from flask import Response
from flask import request
from tempfile import gettempdir
import time

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

    return Response("aaa")


if __name__ == '__main__':
    app.run()
