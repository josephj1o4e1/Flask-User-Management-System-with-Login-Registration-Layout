from flask import Flask, render_template

app = Flask(__name__)

# set route. use a decorator to join a url to a function. (see flasknotes)
# a decorator: when url '/' is requested by client, it triggers home()
@app.route('/')
def home():
    return "Hello World!"

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

if __name__ == "__main__":
    app.run(debug=True) # `debug=True` gives us a fancier flask debugger in the browser
