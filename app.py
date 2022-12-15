from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "TopPage"

@app.route("/<page_id>")
def page(page_id):
    return page_id

if __name__ == '__main__':
    app.run(port=80)