from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r"/api/*")  # Enable CORS for all routes with '/api/' prefix

# Import the routes module to register the routes with the Flask app
from . import routes
