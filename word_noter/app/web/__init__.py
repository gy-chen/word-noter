from word_noter.web.app import create_app

ENV_WEB_CONFIG = 'WORD_NOTER_WEB_CONFIG'

app = create_app('word_noter.web.config', ENV_WEB_CONFIG)
