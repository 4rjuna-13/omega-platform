from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return "Flask works on 8081!"
if __name__ == '__main__':
    print("Testing port 8081...")
    app.run(port=8081, debug=False)
