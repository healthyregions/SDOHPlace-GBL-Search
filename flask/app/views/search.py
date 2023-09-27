import json

from flask import Blueprint, request
from flask_cors import CORS

from app.query import Query

search = Blueprint('search', __name__)
CORS(search)


@search.route("/search", methods=["GET"])
def semantic_search():
	query = Query()
	q = request.args.get('q')
	return json.dumps(query.get_query_expansion(q))
