from flask import Flask
from flask_cors import CORS
import json

from app.query import Query

# from app.services.db import get_db

from flask import request

app = Flask(__name__)
CORS(app)

# with app.app_context():
# 	pass
# 	#get_db()


@app.route("/search")
def search():
	print("HELLLLLLO")
	query = Query()
	q = request.args.get('q')
	return json.dumps(query.get_query_expansion(q))


app.run("0.0.0.0", 8080)
