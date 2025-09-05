from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def league():
    return render_template('index.html', active_tab='league')

@app.route('/portfolio')
def portfolio():
    return render_template('index.html', active_tab='portfolio')

@app.route('/market')
def market():
    return render_template('index.html', active_tab='market')

if __name__ == '__main__':
    app.run(debug=True)
