from flask import Flask, render_template, request, jsonify
import sys
import os

# Ensure the project root is in path (so 'main' and 'src' are importable)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from main import run_pipeline  # ✅ Correct import

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('template/index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        result = run_pipeline(prompt)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)