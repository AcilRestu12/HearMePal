from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
	return render_template("pages/index.html")

@app.route("/chat")
def chat():
	return render_template("pages/chat.html")

if __name__ == '__main__':
	app.run(debug=True)