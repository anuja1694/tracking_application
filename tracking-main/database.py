from flask import g
import sqlite3


def connect_to_database():
    sql = sqlite3.connect('tracking.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_database():
    if not hasattr(g, 'tracking_db'):
        g.tracking_db = connect_to_database()
    return g.tracking_db


