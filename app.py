# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/6 13:20
# @Author   : Perye(Li Pengyu)
# @FileName : app.py
# @Software : PyCharm

from flask import Flask, request, send_from_directory, make_response

from constant import OutputFormat, Status, OUTPUT_DIR
from service import user_service, task_service

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


@app.route('/allowed_output_format', methods=['GET'])
def get_allowed_output_format():
    return OutputFormat.list()


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        token = request.headers.get('Authorization', None)
        user_id = user_service.decrypt_token(token) or user_service.generate_user_id()
        return {'task_id': task_service.create_a_task(request.files, user_id, request.args.get('output_format'))
                }, 200, user_service.renewed_header(user_id)


@app.route('/history', methods=['GET'])
def get_history():
    token = request.headers.get('Authorization')
    user_id = user_service.decrypt_token(token)
    if not user_id:
        return []
    else:
        return task_service.find_task_list_by_user_id(user_id), 200, \
               user_service.renewed_header(user_id)


@app.route('/download/<task_id>', methods=['GET'])
def download_file(task_id):
    token = request.args.get('token')
    user_id = user_service.decrypt_token(token)
    status = task_service.find_task_status_by_task_id(task_id, user_id)
    if status is None:
        return {'message': 'Task not found. Please check your record ID.'}
    elif Status.TO_BE_CONVERTED == status:
        return {'message': 'To be convert. Please try again later.'}
    elif Status.CONVERTING == status:
        return {'message': 'The file is under conversion. Please try again later.'}
    elif Status.COMPRESSING == status:
        return {'message': 'The file is under compressing. Please try again later.'}
    else:
        return send_from_directory(OUTPUT_DIR, task_id + '.zip', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
