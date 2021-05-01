import os
import subprocess
import time

from flask import Flask, render_template
from pydub import AudioSegment
from pydub.playback import play
from rq import Queue
from rq.job import Job, cancel_job

from worker import conn

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])

q = Queue(connection=conn)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


@app.route('/')
def hello_world():
    commands = [
        dict(url='/commands/play', name='Play MP3', icon='fa-file-audio-o'),
        dict(url='/mp3s', name='List MP3s', icon='fa-file-audio'),
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


@app.route('/commands/playasync/<mp3>')
def command_play_async_mp3(mp3):
    mp3_path = os.path.join(BASE_DIR, 'static', 'sounds', mp3)
    if os.path.exists(mp3_path):
        job = q.enqueue_call(
            func=play_async_audio, args=(mp3_path,), ttl=600, result_ttl=0
        )
    return render_template('jobs.t.html', jobid=job.get_id())


def play_async_audio(audiofile):
    fadein = 6 * 1000  # ms
    fadeout = 6 * 1000  # ms

    audio_root, audio_ext = os.path.splitext(audiofile)

    if audio_ext == '.mp3':
        rawsound = AudioSegment.from_mp3(audiofile)
    elif audio_ext =='.wav':
        rawsound = AudioSegment.from_wav(audiofile)

    #sound = rawsound.fade(from_gain=-120.0, start=0, duration=fadein).fade(to_gain=-120.0, end=0, duration=fadeout)
    print('--- Playing async Audio {}'.format(audiofile))
    play(rawsound)
    print('--- Done playing async Audio {}'.format(audiofile))


@app.route('/commands/volume/<int:vol_pct>')
def command_set_volume(vol_pct=None):
    subprocess.run(['amixer', 'sset', 'Master', '{}%'.format(vol_pct)])
    return ('volume set to {}%'.format(vol_pct))


@app.route('/commands/testvumeter')
def command_test_vumeter():
    from test_vumeter import test_vumeter
    test_vumeter()
    return ('testing vu meter')


@app.route('/mp3s')
def get_mp3_list():
    mp3s = os.listdir('static/sounds')

    return render_template('mp3s.t.html', mp3s=mp3s)


@app.route('/asynctest/<int:seconds>')
def aynctest(seconds=None):
    job = q.enqueue_call(
        func=background_processing, args=(seconds,), result_ttl=30
    )
    return render_template('jobs.t.html', jobid=job.get_id())


@app.route('/results/<jobid>')
def get_results(jobid=None):
    job = Job.fetch(jobid, connection=conn)
    if job.is_finished:
        return str(job.result), 200
    else:
        return 'status: {}'.format(job.status), 202


@app.route('/cancel/<jobid>')
def kill_jon(jobid):
    cancel_job(jobid, connection=conn)
    return 'jon cancelled {}'.format(jobid)


def background_processing(s = 5):
    print('halt .....')
    time.sleep(s)
    print('and go >>')
    return 'waited {} seconds'.format(s)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
