import os
from app import create_app

config_name = os.getenv('APP_SETTINGS')
app_ = create_app(config_name)

if __name__ == '__main__':
    app_.run(debug=True)
    