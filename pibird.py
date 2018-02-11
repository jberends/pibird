from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    commands = [
        dict(url='/commands/play', name='Play MP3'),
        dict(url='/commands/testvumeter', name='Test VU meter')
    ]

    return render_template('index.t.html', commands=commands)
    # return 'Hello World!'

@app.route('/commands/play')
def command_play_mp3():
    return 'playing mp3 here'

@app.route('/commands/testvumeter')
def command_test_vumeter():
    from test_vumeter import test_vumeter
    test_vumeter()
    return('testing vu meter')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
