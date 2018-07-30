import os

"""
    This file contains the different settings depending on the
    application environment.
"""


class Config(object):
    """Settings common to all configurations"""
    SECRETE_KEY = os.urandom(24)
    JWT_SECRET_KEY = "The lord is good."
    DEBUG = False
    TESTING = False
    # DATABASE_URI = 'postgres://admin:admin@localhost:5432/diary_db'
    DATABASE_URI ='postgresql://localhost/diary_db'

class ProductionConfig(Config):
    """Production configurations"""
    DEBUG = False  # should be set to false always


class DevelopmentConfig(Config):
    """Development configurations"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configurations"""
    DEBUG = True
    # DATABASE_URI = 'postgres://admin:admin@localhost:5432/test_db'
    DATABASE_URI ='postgresql://localhost/test_db'


app_config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
