# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/6 13:20
# @Author   : Perye(Li Pengyu)
# @FileName : app.py
# @Software : PyCharm
import sys
sys.path.append('/usr/local/pdf2docx')

import socket

import uuid
import uhashring
from flask import Flask, request, send_from_directory, make_response, redirect

from constant import OutputFormat, Status, OUTPUT_DIR, ip_dict
from service import task_service

app = Flask(__name__)


@app.after_request
def after(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE, PATCH'
    resp.headers['Access-Control-Max-Age'] = '100'
    resp.headers['Access-Control-Allow-Headers'] = '*, Authorization, token, accept, user-agent, content-type, ' \
                                                   'Access-Control-Expose-Headers '
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Expose-Headers'] = 'token, Authorization, accept, user-agent, content-type'
    return resp


@app.route('/')
def hello_world():
    return 'Hello Pdf2Docx!'


@app.route('/task_id')
def get_task_id():
    return str(uuid.uuid4())


@app.route('/allowed_output_format', methods=['GET'])
def get_allowed_output_format():
    return OutputFormat.list()


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            task_id = str(uuid.UUID(request.args.get('task_id')))
            if 'redirected' not in request.args.keys():
                return redirect(
                    'http://' + ip_dict.get(hash_ring.get_node(task_id)) +
                    f'/upload?task_id={task_id}&output_format={request.args.get("output_format")}&redirected=1'
                ), 307
        except ValueError:
            return {'message': 'Invalid task ID.'}, 400
        token = request.headers.get('Authorization', None)
        # user_id = user_service.decrypt_token(token) or user_service.generate_user_id()
        # return {'task_id': task_service.create_a_task(task_id, request.files, user_id, request.args.get('output_format'))
        #         }, 200, user_service.renewed_header(user_id)
        return {'task_id': task_service.create_a_task(task_id, request.files, '1',
                                                      request.args.get('output_format'))
                }, 200


@app.route('/history', methods=['GET'])
def get_history():
    token = request.headers.get('Authorization')
    # user_id = user_service.decrypt_token(token)
    user_id = '1'
    if not user_id:
        return []
    else:
        # return task_service.find_task_list_by_user_id(user_id), 200, \
        #        user_service.renewed_header(user_id)
        return task_service.find_task_list_by_user_id(user_id), 200


@app.route('/download/<task_id>', methods=['GET'])
def download_file(task_id):
    try:
        task_id = str(uuid.UUID(task_id))
    except ValueError:
        return {'message': 'Invalid task ID.'}, 400
    token = request.args.get('token')
    user_id = '1'
    # user_id = user_service.decrypt_token(token)
    status = task_service.find_task_status_by_task_id(task_id, user_id)
    if status is None:
        return {'message': 'Task not found. Please check your task ID.'}
    elif Status.TO_BE_CONVERTED == status:
        return {'message': 'To be convert. Please try again later.'}
    elif Status.CONVERTING == status:
        return {'message': 'The file is under conversion. Please try again later.'}
    elif Status.COMPRESSING == status:
        return {'message': 'The file is under compressing. Please try again later.'}
    else:
        if task_service.find_task_node_by_task_id(task_id) != local_address:
            return redirect(hash_ring.get_node(task_id)), 302
        return send_from_directory(OUTPUT_DIR, task_id + '.zip', as_attachment=True)


if __name__ == '__main__':

    local_address = socket.gethostbyname(socket.gethostname()) + ':5001'
    hash_ring = uhashring.HashRing([
        'bbb117e19ce8',
        'ee9a831c03a2',
        '3c26663a4fa3',
        '851657df746f',
        '5c6a81750f67'
    ])

    app.run(host='0.0.0.0', port=5000)
