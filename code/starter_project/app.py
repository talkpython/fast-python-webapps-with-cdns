import datetime
import sys

import flask
import jinja_partials
from flask import Response

from db import db_init
from services import json_video_service

app = flask.Flask("app")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(datetime.timedelta(days=31).total_seconds())


def configure():
    print("Configuring Flask app:")

    register_template_ops()
    print("Registered template helpers")

    register_blueprints()
    print("Registered blueprints")

    setup_db()
    print("DB setup completed.")
    print("", flush=True)


def register_template_ops():
    jinja_partials.register_extensions(app)
    helpers = {
        'len': len,
        'isinstance': isinstance,
        'str': str,
        'type': type
    }
    app.jinja_env.globals.update(**helpers)


def register_blueprints():
    from views import home
    from views import videos
    from views import feed

    app.register_blueprint(home.blueprint)
    app.register_blueprint(videos.blueprint)
    app.register_blueprint(feed.blueprint)


def setup_db():
    json_video_service.load_data()
    db_init.init()
    db_init.ensure_data()


@app.after_request
def add_caching_header(response: Response):
    # print(f"REQUEST FROM: {response.}")
    # response.cache_control.max_age = 300
    return response


if __name__ == '__main__':
    configure()
    being_debugged = sys.gettrace() is not None
    app.run(host="127.0.0.1", port=10001, debug=being_debugged)
else:
    configure()
