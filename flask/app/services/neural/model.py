import os

from flask import g
from werkzeug.local import LocalProxy
from sentence_transformers import SentenceTransformer


def get_model():
	"""
	Configuration method to return db instance
	"""
	model = getattr(g, "_model", None)

	if not model:
		model = g._model = SentenceTransformer('bert-base-nli-mean-tokens')
		print("ONE ONCE")

	return model


# Use LocalProxy to read the global db instance with just `db`
model = LocalProxy(get_model)
