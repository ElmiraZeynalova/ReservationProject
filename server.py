from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book')
def book():
    return render_template('book.html')

if __name__ == '__main__':
    app.run(debug=True)
