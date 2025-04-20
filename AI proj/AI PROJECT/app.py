from flask import Flask, render_template, request
from cities import cities, find_path, draw_graph
import webbrowser
import threading
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        algo = request.form['algo']
        path = find_path(start, end, algo)
        if path:
            distance = draw_graph(path, start, end)
            result = {
                "path": " → ".join(path),
                "distance": round(distance, 2),
                "image": "route.png"
            }
        else:
            result = {"error": "No path found using the selected algorithm."}
    return render_template("index.html", cities=cities.keys(), result=result)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Only open the browser on the first run (not on reload)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1, open_browser).start()

    app.run(debug=True, use_reloader=True)
