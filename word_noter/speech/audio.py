"""Provide audio related functions

- Listen sounds in background, record sounds when detect large sound

"""
import audioop
import asyncio
import contextlib
import collections
import enum
import math
import logging
import queue
import wave
import pyaudio

recorded_sounds = queue.Queue()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

LARGE_SOUND_THRESHOLD = 1000


@contextlib.contextmanager
def get_input_stream(chunk=CHUNK, format=FORMAT, channels=CHANNELS, rate=RATE):
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    try:
        yield stream
    finally:
        stream.stop_stream()
        p.terminate()


def get_record_seconds(rate, data_size):
    if data_size <= 0:
        return 0
    return data_size / rate


def is_sound_large(data):
    logging.debug(math.sqrt(abs(audioop.avg(data, 4))))
    return math.sqrt(abs(audioop.avg(data, 4))) > LARGE_SOUND_THRESHOLD


def save_record(data, file="output.wav", channels=CHANNELS, format=FORMAT, rate=RATE):
    if type(data) is not bytes and isinstance(data, collections.Iterable):
        data = b''.join(data)
    wf = wave.open(file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(data)
    wf.close()


class StopRecordException(Exception):
    pass


class RecordStatus(enum.Enum):
    WAIT = 1
    RECORDING = 2
    IDLE = 3
    STOP = 4


class LargeSoundActivateRecorder:
    """Start record when detect large sound and stop recording when no large sound detected for specific seconds
    """

    def __init__(self, channels=CHANNELS, chunk=CHUNK, rate=RATE, stop_record_seconds=2):
        self._channels = channels
        self._chunk = chunk
        self._rate = rate
        self._stop_record_seconds = stop_record_seconds
        self._out_queue = recorded_sounds
        self._reset()

    def record(self):
        with get_input_stream(channels=self._channels, chunk=self._chunk, rate=self._rate) as stream:
            try:
                while True:
                    data = stream.read(self._chunk)
                    if is_sound_large(data):
                        self._on_sound_large(data)
                    else:
                        self._on_sound_not_large(data)
            except StopRecordException:
                recorded = self._recorded_sounds
                logging.debug("done recording")
                logging.debug("recorded %s seconds" % get_record_seconds(self._rate, len(recorded) * self._chunk))
                self._reset()
                return recorded

    def _on_sound_large(self, data):
        logging.debug('on_sound_large')
        if self._status == RecordStatus.WAIT:
            self._status = RecordStatus.RECORDING
            self._recorded_sounds.append(data)
        elif self._status == RecordStatus.IDLE:
            self._status = RecordStatus.RECORDING
            self._recorded_sounds.extend(self._idle_sounds)
            self._recorded_sounds.append(data)
            self._idle_sounds = []

    def _on_sound_not_large(self, data):
        logging.debug('on_sound_not_large')
        if self._status == RecordStatus.RECORDING:
            self._status = RecordStatus.IDLE
            self._on_idle(data)
        elif self._status == RecordStatus.IDLE:
            self._on_idle(data)

    def _on_idle(self, data):
        logging.debug('on_idle')
        self._idle_sounds.append(data)
        idle_seconds = get_record_seconds(self._rate, len(self._idle_sounds) * self._chunk)
        logging.debug('idle %s seconds' % idle_seconds)
        if idle_seconds >= self._stop_record_seconds:
            self._status = RecordStatus.STOP
            self._recorded_sounds.extend(self._idle_sounds)
            raise StopRecordException()

    def _reset(self):
        self._status = RecordStatus.WAIT
        self._recorded_sounds = []
        self._idle_sounds = []


async def active_record_large_sound(out_queue=recorded_sounds, **kargs):
    """Keep listen sound in background, and record sound when detect large sounds

    :param out_queue: the queue to put the recorded sounds
    """
    # TODO use threading to do this, or the event loop will be blocked here
    recorder = LargeSoundActivateRecorder(**kargs)
    while True:
        recorded_sound = recorder.record()
        try:
            out_queue.put(recorded_sound)
        except queue.Empty:
            pass
        finally:
            await asyncio.sleep(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    recorder = LargeSoundActivateRecorder(channels=1)
    data = recorder.record()
    save_record(data, 'output.wav', channels=1)
