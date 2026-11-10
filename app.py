from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, abort
from calculator import calculate_noise_figure

app = Flask(__name__)

GUIDES = [
    {
        "slug": "measure-lna-noise-figure",
        "path": "/guides/measure-lna-noise-figure",
        "template": "guide_measure.html",
        "title": "How to Measure LNA Noise Figure with a Spectrum Analyzer",
        "summary": "A complete walkthrough of a real 3.4 GHz measurement: analyzer settings, calibration, the DUT run, and the final calculation.",
        "description": "Step-by-step Y-factor noise figure measurement of an amplifier at 3.4 GHz using a spectrum analyzer and noise source, with real readings and screenshots.",
    },
    {
        "slug": "second-stage-correction",
        "path": "/guides/second-stage-correction",
        "template": "guide_correction.html",
        "title": "Why Second-Stage Correction Matters in Noise Figure Measurements",
        "summary": "How the spectrum analyzer's own noise inflates your result, the Friis formula that removes it, and when the correction becomes unreliable.",
        "description": "Learn how the Friis cascade formula removes a spectrum analyzer's own noise from a Y-factor noise figure measurement, with a table of the error versus DUT gain.",
    },
    {
        "slug": "y-factor-mistakes",
        "path": "/guides/y-factor-mistakes",
        "template": "guide_mistakes.html",
        "title": "10 Common Y-Factor Noise Figure Measurement Mistakes",
        "summary": "A bench checklist: wrong ENR, wrong detector, compression, mismatch, interference and other causes of bad noise figure readings.",
        "description": "Ten common mistakes in Y-factor noise figure measurements with a spectrum analyzer, and how to avoid each one.",
    },
    {
        "slug": "noise-figure-conversions",
        "path": "/guides/noise-figure-conversions",
        "template": "guide_conversions.html",
        "title": "Noise Figure, Noise Factor and Noise Temperature Conversions",
        "summary": "The formulas and a reference table for converting between dB, linear noise factor and kelvin, with worked examples.",
        "description": "Convert between noise figure (dB), noise factor and noise temperature (K) with formulas, a reference table and worked examples.",
    },
]
GUIDES_BY_SLUG = {g["slug"]: g for g in GUIDES}


@app.before_request
def redirect_www_and_https():
    if request.host.startswith('www.'):
        return redirect(request.url.replace('www.', '', 1).replace('http://', 'https://', 1), code=301)
    if request.url.startswith('http://'):
        return redirect(request.url.replace('http://', 'https://', 1), code=301)


@app.route("/")
def index():
    return render_template("index.html", guides=GUIDES)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/guides")
def guides_index():
    return render_template(
        "guides.html",
        guides=GUIDES,
        path="/guides",
        title="Noise Figure Measurement Guides",
        description="Practical guides to measuring noise figure with a spectrum analyzer and noise source using the Y-factor method.",
    )

@app.route("/guides/<slug>")
def guide(slug):
    g = GUIDES_BY_SLUG.get(slug)
    if g is None:
        abort(404)
    return render_template(
        g["template"],
        guides=GUIDES,
        path=g["path"],
        title=g["title"],
        description=g["description"],
    )

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

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    urls = [("/", "1.0"), ("/guides", "0.8")]
    urls += [(g["path"], "0.8") for g in GUIDES]
    urls += [("/about", "0.6"), ("/privacy", "0.5")]
    body = "\n".join(
        f"  <url><loc>https://noisefigurecalculator.com{p}</loc><priority>{pr}</priority></url>"
        for p, pr in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>"
    )
    return xml, 200, {'Content-Type': 'application/xml'}

if __name__ == "__main__":
    app.run(debug=True)
