import sys
import os
import argparse
import bottle
from bottle import route, run, template, request, response, static_file
import json

ROOT_PATH = ''
labels = []
file_lst = []

@route('/upload_label', method='OPTIONS')
def upload_label_options():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Headers', '*')

    return ''

@route('/upload_label', method='POST')
def upload_label():
    data = json.loads(request.body.read())
    path = data['path']
    label_data = data['label_data']
    # path = request.POST.get('path')
    # label_data = request.POST.get('labels')
    response.set_header('Access-Control-Allow-Origin', '*')

    if path.startswith('/'):
        path = path[1:]

    real_path = os.path.join(ROOT_PATH, path)

    if real_path not in file_lst:
        response.status = 400
        return 'Not a valid path'

    label_file_path = os.path.join(ROOT_PATH, path.rsplit('.', 1)[0] + '.txt')
    with open(label_file_path, 'w') as f:
        f.write(label_data)
    
    try:
        file_lst.remove(real_path)
    except ValueError:
        print('Weird, path', path, 'real_path', real_path)

    return label_file_path

@route('/image/<path:path>')
def get_image(path):
    response.set_header('Access-Control-Allow-Origin', '*')
    return static_file(path.replace(ROOT_PATH, ''), root=ROOT_PATH)

@route('/next')
def get_next_image():
    response.set_header('Access-Control-Allow-Origin', '*')
    return file_lst[0].replace(ROOT_PATH, '') if file_lst else ''


@route('/config')
def get_config():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Content-Type', 'application/json')

    return json.dumps({
        'labels': labels,
        'data_path': ROOT_PATH,
        'image_left': len(file_lst)
    }) 


def serve(path):
    global file_lst, ROOT_PATH
    ROOT_PATH = path
    file_lst = ['%s/%s' % (i[0], f) for i in os.walk(path) if i[2] for f in i[2] if f.rsplit('.', 1)[-1].lower() in ('jpg', 'tif', 'jpeg', 'tiff', 'png') and not os.path.exists(('%s/%s' % (i[0], f)).rsplit('.', 1)[0] + '.txt') ]
    run(host='localhost', port=58080)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--labels", help="Labels file, one line for one label", default="labels.txt")
    parser.add_argument("path", help="Data path")
    args = parser.parse_args()

    with open(args.labels, 'r') as f:
        labels = f.read().replace('\r', '').strip().split('\n')

    serve(args.path)

