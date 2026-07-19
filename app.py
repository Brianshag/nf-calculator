from flask import Flask, request, jsonify, render_template
from calculator import calculate_noise_figure

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route('/ads.txt')
def ads_txt():
    return "google.com, pub-4436507227492177, DIRECT, f08c47fec0942fa0", 200, {'Content-Type': 'text/plain'}

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    required = ["ns_off", "ns_on", "dut_off", "dut_on", "enr"]
    missing = [k for k in required if k not in data or data[k] is None]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        ns_off  = float(data["ns_off"])
        ns_on   = float(data["ns_on"])
        dut_off = float(data["dut_off"])
        dut_on  = float(data["dut_on"])
        enr     = float(data["enr"])
    except (ValueError, TypeError):
        return jsonify({"error": "All inputs must be valid numbers."}), 400

    try:
        result = calculate_noise_figure(ns_off, ns_on, dut_off, dut_on, enr)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 422


if __name__ == "__main__":
    app.run(debug=True)
