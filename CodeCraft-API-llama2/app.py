from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/llama2_api', methods=['POST'])
def generate_code():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'message': 'Missing text or language properties in the request body.'}), 400

    try:
        response = ollama.chat(model='codellama:13b', messages=[{
            'role': 'user',
            'content': text,
            },
        ])
        if response:
            generated_code = response.get('message', {}).get('content', '')
            return jsonify({'message': 'Code generation successful', 'data': generated_code}), 200
        else:
            return jsonify({'message': 'No code available'}), 404
    except Exception as e:
        print("Exception: ", e)
        traceback.print_exc()
        return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)