from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.rout('/commands/play')
def command_play_mp3():
    return 'playing mp3 here'


if __name__ == '__main__':
    app.run()
