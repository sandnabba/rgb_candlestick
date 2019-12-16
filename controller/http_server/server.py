from flask import Flask, request
import os.path

def run(messagebus):
    app = Flask(__name__)

    @app.route('/api', methods=['GET', 'POST'])
    def root():
        if request.method == 'POST':
            print(request.get_json())
            messagebus.put(request.get_json())
            # data = request.get_json()
            # if 'speed' in data:
            #     messagebus.put({'speed': data['speed']})
            # if 'program' in data:
            #     messagebus.put({'program': data['program']})

        return "", 204

    @app.route('/api/color', methods=['POST'])
    def color():
        if request.method == 'POST':
            # print(request.get_json())
            messagebus.put(request.get_json())

        return "Hello", 204

    app.run()
