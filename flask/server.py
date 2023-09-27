from flask import Flask
from flask_cors import CORS
from app.views.search import search

import nltk

from app.services.neural.model import get_model

app = Flask(__name__)
CORS(app)

# app.config['ENV'] = 'development'
# app.config['DEBUG'] = True

app.register_blueprint(search)

with app.app_context():
	get_model()


def download_nltk_packages():
	nltk.download('wordnet')
	nltk.download('punkt')
	nltk.download('stopwords')
	nltk.download('averaged_perceptron_tagger')


download_nltk_packages()

app.run("0.0.0.0", 80)
