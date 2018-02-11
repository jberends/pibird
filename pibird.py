import os
import subprocess

from flask import Flask, render_template

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


@app.route('/')
def hello_world():
    commands = [
        dict(url='/commands/play', name='Play MP3', icon='fa-file-audio-o'),
        dict(url='/commands/testvumeter', name='Test VU meter', icon='fa-flask'),
        dict(url='/commands/volume/0', name='Set volume 0%', icon='fa-volume-off'),
        dict(url='/commands/volume/25', name='Set volume 25%', icon='fa-volume-down'),
        dict(url='/commands/volume/50', name='Set volume 50%', icon='fa-volume-down'),
        dict(url='/commands/volume/75', name='Set volume 75%', icon='fa-volume-down'),
        dict(url='/commands/volume/100', name='Set volume 100%', icon='fa-volume-up'),
    ]

    return render_template('index.t.html', commands=commands)
    # return 'Hello World!'


@app.route('/commands/play')
def command_play_mp3():
    subprocess.run(['mpg321', os.path.join(BASE_DIR, 'static/sounds/Forest-birds-ambience-early-spring.mp3')])
    return 'playing mp3 here'


@app.route('/commands/volume/<int:vol_pct>')
def command_set_volume(vol_pct=None):
    subprocess.run(['amixer', 'sset', 'Master', '{}%'.format(vol_pct)])
    return ('volume set to {}%'.format(vol_pct))


@app.route('/commands/testvumeter')
def command_test_vumeter():
    from test_vumeter import test_vumeter
    test_vumeter()
    return ('testing vu meter')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
