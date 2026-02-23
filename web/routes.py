from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def register_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    