from flask import Flask, jsonify
from pymongo import MongoClient
import json
import utils
from bson.json_util import dumps
import sys
sys.path.append('../dnstwist')
import phase2

app = Flask(__name__)

@app.route("/")
def landing():
    return "<h1 style='color:blue'>Domain Squatting!</h1>"

@app.route('/squatting/api/v1.0/registered', methods=['GET'])
def get_registered_domains():
  db = utils.connect_mongo()
  rs = db.registered_domain.find({}, {"_id":0})
  out = list()
  for doc in rs:
    out.append(dumps(doc))
  return jsonify(out)

#example: curl -i -H "Content-Type: application/json" -X PUT http://10.2.4.231:5000/squatting/api/v1.0/registered/qatarliving.com
#this registers qatarliving.com if it is not already registered
@app.route('/squatting/api/v1.0/registered/<string:domain_name>', methods=['PUT'])
def register_domains(domain_name):
  msg = phase2.register_domain(domain_name)
  return jsonify("{'msg':" + msg + "}")

@app.route('/squatting/api/v1.0/twisted/<string:domain_name>', methods=['GET'])
def get_twisted_domains(domain_name):
	db = utils.connect_mongo()
	collectionName = "domain_" + domain_name
	rs = db[collectionName].find({}, {"_id":0})
	out = list()
	for doc in rs:
		out.append(dumps(doc))
	return jsonify(out)

if __name__ == "__main__":
    app.run(host='10.2.4.231')
