from flask import Flask, request, send_from_directory
import os.path

def run(messagebus):
    app = Flask(__name__)
    @app.route('/', methods=['GET', 'POST'])
    def root():
        if request.method == 'POST':
            print("Clicked:", request.form.get('program'))
            messagebus.put(request.form.get('program'))

        return app.send_static_file('index.html')

    app.run()
