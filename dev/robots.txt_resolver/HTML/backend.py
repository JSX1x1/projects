from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/get-robots', methods=['GET'])
def get_robots():
    url = request.args.get('url')
    
    if not url:
        return jsonify({'status': 'error', 'message': 'No URL provided.'}), 400

    robots_url = url.rstrip('/') + '/robots.txt'
    
    try:
        response = requests.get(robots_url)

        if response.status_code == 200:
            return jsonify({'status': 'success', 'robots_txt': response.text})
        else:
            return jsonify({'status': 'error', 'message': f'robots.txt not found (Status code {response.status_code}).'}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Error fetching robots.txt: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
