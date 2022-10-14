# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/6 13:20
# @Author   : Perye(Li Pengyu)
# @FileName : app.py
# @Software : PyCharm

import os
import time

from flask import Flask, request, send_from_directory
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        record_id = time.time().hex()[4:-4]
        file = request.files['file']
        file.save(f'cache/pdf/{record_id}.pdf')
        return record_id


@app.route('/download', methods=['GET'])
def download_file():
    if request.method == 'GET':
        filename = request.args.get('record_id') + '.docx'
        if filename in os.listdir('cache/pdf'):
            if filename in os.listdir('cache/docx'):
                return {'message': 'The file is converting. Please try again later.'}
            else:
                return {'message': 'To be convert. Please try again later.'}
        else:
            if filename in os.listdir('cache/docx'):
                return send_from_directory('cache/docx', filename, as_attachment=True)
            else:
                return {'message': 'File not found. Please check your record ID.'}


if __name__ == '__main__':
    app.run()
