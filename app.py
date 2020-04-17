from flask import Flask, request, current_app, redirect, send_file
import scraper as sc
app = Flask(__name__)

@app.route('/')
def index():
    sc.saveG()
    return send_file('graph.png', mimetype='image/png')

if __name__ == '__main__':
    app.run()



