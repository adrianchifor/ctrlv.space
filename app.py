from flask import Flask, jsonify, request, render_template, make_response
from redis import StrictRedis
import os, hashlib, uuid, logging

get_hash = lambda: hashlib.md5(uuid.uuid4().bytes).hexdigest()[:12]

app = Flask(__name__)

db = StrictRedis.from_url(os.environ['REDIS_URL'], db=2, decode_responses=True)

@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


@app.route('/api/v1/create', methods=['POST'])
def api_v1_create():
    if 'ciphertext' not in request.form:
        return make_response(jsonify(error='Bad Request'), 400)

    ciphertext = request.form['ciphertext']

    if (not isinstance(ciphertext, str)) or (len(ciphertext) > 5100) or (len(ciphertext) == 0):
        return make_response(jsonify(error='Bad Request'), 400)

    key = get_hash()
    db.set(key, ciphertext)

    if 'destroy' in request.form:
        if request.form['destroy'] == "true":
            db.set(key + "_destroy", True)

    return make_response(jsonify(error=None, key=key), 200)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<key>")
def paste(key):
    if not db.exists(key):
        return render_template("404.html"), 404

    ciphertext = db.get(key)

    destroy_key = key + "_destroy"
    if db.exists(destroy_key):
        db.delete(key, destroy_key)

    return render_template("paste.html", ciphertext=str(ciphertext))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
