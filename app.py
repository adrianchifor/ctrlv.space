from flask import Flask, jsonify, request, render_template
from functools import wraps
from redis import StrictRedis
import os, hashlib, uuid

get_hash = lambda: hashlib.md5(uuid.uuid4().bytes).hexdigest()[:12]

app = Flask(__name__)

db = StrictRedis.from_url(os.environ['REDIS_URL'], db=2, decode_responses=True)

def json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return jsonify(f(*args, **kwargs))
    return wrapper

@app.route('/api/v1/create', methods=['POST'])
@json
def api_v1_create():
    if 'ciphertext' not in request.form:
        return {
            'error': 'Bad Request'
        }

    key = get_hash()
    db.set(key, request.form['ciphertext'])

    return {
        'error': None,
        'key': key
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<key>")
def paste(key):
    if not db.exists(key):
        return render_template("404.html")

    ciphertext = db.get(key)
    return render_template("paste.html", ciphertext=ciphertext)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
