import json
from flask import Flask
from tableGenerator import generator
app = Flask(__name__)

@app.route('/')
def hello_world():
    LR2ID = 41955
    with open("userData_41955.json", "r", encoding="utf-8") as fr:
        data = json.load(fr)

    # print(data)
    return generator(data, LR2ID) 
    # return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run()