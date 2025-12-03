from flask import Flask, send_file
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import datetime
import pytz

app = Flask(__name__)

gandalf_requests = Counter('gcd_gandalf_requests_total', 'Total requests to /gandalf')
colombo_requests = Counter('gcd_colombo_requests_total', 'Total requests to /colombo')

@app.route('/gandalf')
def gandalf():
    gandalf_requests.inc()
    return send_file('gandalf.jpg', mimetype='image/jpeg')

@app.route('/colombo')
def colombo():
    colombo_requests.inc()
    tz = pytz.timezone('Asia/Colombo')
    now = datetime.datetime.now(tz)
    return f"Current time in Colombo: {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)