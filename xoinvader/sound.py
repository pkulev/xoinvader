""" Sound files handling. """

#import sys
#import time
import wave
import pyaudio

from xoinvader.common import Settings
p = pyaudio.PyAudio()

class _Mixer(object):
    """ Handle sound files. """
    def __init__(self, settings):
        self._sounds = {k:v for k in settings.path.sound.weapon.keys()
                for v in [wave.open(snd_file, "rb")
                    for snd_file in settings.path.sound.weapon.values()]}
        open(__name__ + "log", "w").write(str(self._sounds))
        self.blaster = self._sounds["Blaster"]

    def _play_sound(self, in_data, frame_count, time_info, status):
        data = self.blaster.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def play(self):
        stream = p.open(format=p.get_format_from_width(self.blaster.getsampwidth()),
                        channels=self.blaster.getnchannels(),
                        rate=self.blaster.getframerate(),
                        output=True,
                        stream_callback=self._play_sound)
        stream.start_stream()
        self.blaster.setpos(0)

Mixer = _Mixer(Settings)
