from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Welcome to My Flask Project!"

if __name__ == "__main__":
    print("Starting Flask App...")
    app.run(debug=True)