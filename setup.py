from setuptools import setup, find_packages

setup(
    name="word-noter",
    description="Help note unrecognized words while reading",
    packages=find_packages(),
    install_requires=[
        'pyocr',
        'pynput',
        'websockets',
        'opencv-python',
        'pyaudio',
        'google-cloud-speech',
        'pocketsphinx',
        'google-cloud-vision',
        'websockets',
        'Faker',
        'sqlalchemy',
        'flask',
        'flask-restful',
        'cerberus',
        'flask-cors',
        'python-socketio',
        'eventlet'
    ]
)
