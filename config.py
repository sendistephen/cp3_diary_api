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


class ProductionConfig(Config):
    """Production configurations"""
    DEBUG = False  # should be set to false always


class DevelopmentConfig(Config):
    """Development configurations"""
    DEBUG = True
    DATABASE_URI = 'postgresql://localhost/test_db'


class TestingConfig(Config):
    """Testing configurations"""
    TESTING = True
    DEBUG = True

    DATABASE_URI = 'postgresql://localhost/test_db'


app_config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
