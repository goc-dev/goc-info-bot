from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Bot is running!'

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'goc-info-bot'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)