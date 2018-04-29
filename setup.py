from setuptools import setup, find_packages

setup(
    name="web-noter",
    description="Help note unrecognized words while reading",
    packages=find_packages(),
    scripts=[
        'word_noter/script/start-word-noter-web',
        'word_noter/script/start-word-noter-socketio'
    ],
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
        'aiohttp',
        'flask-migrate',
        'flask-sqlalchemy'
    ]
)
