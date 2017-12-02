from flask import Flask, request, send_from_directory
import os.path

def run(messagebus):
    app = Flask(__name__)
    @app.route('/', methods=['GET', 'POST'])
    def root():
        if request.method == 'POST':
            if request.form.get('program') != None:
                print("Clicked:", request.form.get('program'))
                messagebus.put({'program': request.form.get('program')})
            if request.form.get('speed') != None:
                print("Clicked:", request.form.get('speed'))
                messagebus.put({'speed': request.form.get('speed')})
        return app.send_static_file('index.html')

    app.run()
