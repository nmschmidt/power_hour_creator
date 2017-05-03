import os
import glob

from PyQt5.QtSql import QSqlQuery

import power_hour_creator.config
from power_hour_creator import power_hour_creator, config, boot
from PyQt5.QtTest import QTest

SUPPORT_PATH = os.path.join(config.ROOT_DIR, "../tests/support")

def before_all(context):
    config.phc_env = 'test'
    delete_database()


def after_step(context, step):
    QTest.qWait(5)


def before_scenario(context, scenario):
    config.phc_env = 'test'
    launch_app(context)
    context.support_path = SUPPORT_PATH
    context.num_tracks = 0
    context.prhr_length = 0
    QTest.qWaitForWindowActive(context.main_window)


def after_scenario(context, scenario):
    close_app(context)
    delete_export_files(context)
    clean_database()


def launch_app(context):
    app = power_hour_creator.launch_app()
    context.main_window = app.main_window
    context.tracklist = context.main_window.tracklist
    context.app = app


def close_app(context):
    del context.app


def delete_export_files(context):
    for ext in ['m4a', 'mp4']:
        export_files = glob.glob(os.path.join(context.support_path, "exports/*.{}".format(ext)))
        for f in export_files:
            os.remove(f)


def clean_database():
    try:
        db = boot.connect_to_db()
        query = QSqlQuery()
        query.exec_("DELETE FROM tracks")
        query.exec_("DELETE FROM power_hours")
        query.exec_("DELETE FROM migrations")
    finally:
        db.close()


def delete_database():
    if 'test' in config.db_path():
        os.remove(config.db_path())


