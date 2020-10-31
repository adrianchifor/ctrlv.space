from flask import Flask, jsonify, request, render_template, make_response
from redis import StrictRedis
from redis.exceptions import ConnectionError
import os, hashlib, uuid, logging
from datetime import timedelta

get_hash = lambda: hashlib.md5(uuid.uuid4().bytes).hexdigest()[:12]

app = Flask(__name__)

db = StrictRedis.from_url(os.environ.get('REDIS_URL', "redis://localhost:6379"), db=2, decode_responses=True)

try:
    db.ping()
except (ConnectionError):
    print("Cannot connect to Redis. Make sure it's running at REDIS_URL or localhost:6379")
    quit()

@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


@app.route('/api/v1/create', methods=['POST'])
def api_v1_create():
    if 'ciphertext' not in request.form:
        return make_response(jsonify(error='Bad Request'), 400)

    maxLength = int(os.environ.get('MAX_LENGTH', 5000))

    ciphertext = request.form['ciphertext']

    if (not isinstance(ciphertext, str)) or (len(ciphertext) > maxLength) or (len(ciphertext) == 0):
        return make_response(jsonify(error='Bad Request'), 400)

    key = get_hash()
    db.set(key, ciphertext)

    if ('token' in request.form) and ('encryptedToken' in request.form):
        db.set(key + "_encryptedToken", request.form['encryptedToken'])
        db.set(key + "_" + request.form['token'], 'true')

    if 'destructOption' in request.form:
        destructOption = request.form['destructOption']

        if destructOption == "1h":
            db.expire(key, timedelta(hours=1))
        elif destructOption == "1d":
            db.expire(key, timedelta(days=1))
        elif destructOption == "1w":
            db.expire(key, timedelta(weeks=1))

    return make_response(jsonify(error=None, key=key), 200)


@app.route('/api/v1/destruct', methods=['POST'])
def api_v1_destruct():
    if ('key' not in request.form) or ('token' not in request.form):
        return make_response(jsonify(error='Bad Request'), 400)

    key = request.form['key']
    token = request.form['token']

    if (not len(key) == 12) or (not len(token) == 64):
        return make_response(jsonify(error='Bad Request'), 400)

    if db.exists(key + "_" + token):
        db.delete(key, key + "_encryptedToken", key + "_" + token)
        return make_response(jsonify(error=None, success="true"), 200)
    else:
        return make_response(jsonify(error=None, success="false"), 200)


@app.route('/health')
def health_check():
    return make_response("", 200)


@app.route("/")
def index():
    selfDestructMandatory = os.environ.get('SELF_DESTRUCT_MANDATORY', "false")
    maxLength = int(os.environ.get('MAX_LENGTH', 5000))
    googleAnalyticsId = os.environ.get('GOOGLE_ANALYTICS_ID', "")

    return render_template("index.html", selfDestructMandatory=selfDestructMandatory,
        maxLength=maxLength, analyticsId=googleAnalyticsId)


@app.route("/<key>")
def paste(key):
    if not db.exists(key):
        return render_template("404.html", key=key), 404

    ciphertext = db.get(key)

    encryptedToken = ""
    if db.exists(key + "_encryptedToken"):
        encryptedToken = db.get(key + "_encryptedToken")

    googleAnalyticsId = os.environ.get('GOOGLE_ANALYTICS_ID', "")

    return render_template("paste.html", ciphertext=str(ciphertext),
        encryptedToken=str(encryptedToken), key=key, analyticsId=googleAnalyticsId)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
