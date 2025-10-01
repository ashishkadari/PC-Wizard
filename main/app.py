from flask import Flask, jsonify, render_template, request
import logging
from backendpr import update_database, getrecommend  

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        total = float(request.form['totalprice'])
        kind  = request.form['type']
        if total <= 0:
            return jsonify({"error": "Total price must be greater than 0"}), 400
        if kind not in ["gaming", "workstation"]:
            return jsonify({"error": "Invalid type. Must be 'gaming' or 'workstation'"}), 400
        logging.info("Updating database...")
        logging.info(f"Received recommendation request: type={kind}, price={total}")
        recs = getrecommend(total, kind)
        if not recs:
            return jsonify({"error": "No valid build found"}), 400
        return jsonify({
        "total_price": recs.get("total_price"),
        "components": recs}), 200

    except Exception as e:
        logging.error(f"Error while generating recommendation: {e}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    logging.info("Starting Flask app...")
    app.run(debug=True)