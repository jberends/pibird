from pydub import AudioSegment
from pydub.playback import play

if __name__ == '__main__':
    s = AudioSegment.from_mp3("static/sounds/Bird-singing-in-the-forest.mp3")
    sound1 = s[:10*1000]

    fade_louder_for_3_seconds_in_middle = sound1.fade(to_gain=+6.0, start=7500, duration=3000)

    fade_quieter_beteen_2_and_3_seconds = sound1.fade(to_gain=-3.5, start=2000, end=3000)

    # easy way is to use the .fade_in() convenience method. note: -120dB is basically silent.
    fade_in_the_hard_way = sound1.fade(from_gain=-120.0, start=0, duration=6000)
    fade_out_the_hard_way = sound1.fade(to_gain=-120.0, end=0, duration=5000)
