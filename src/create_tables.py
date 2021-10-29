"""
website_stats table ddl
"""
import psycopg2
from settings import *

conn = psycopg2.connect(POSTGRESQL_URI)


with conn:
    with conn.cursor() as cursor:
        website_stats_sql = "CREATE TABLE IF NOT EXISTS website_stats(" \
                            "id SERIAL PRIMARY KEY," \
                            "website VARCHAR(100) NOT NULL," \
                            "regexp VARCHAR(100) NOT NULL DEFAULT '',"\
                            "status_code INTEGER," \
                            "response_time numeric," \
                            "regexp_exists BOOLEAN DEFAULT FALSE," \
                            "create_datetime timestamptz NOT NULL DEFAULT now(),"\
                            "UNIQUE(website, regexp))"

        cursor.execute(website_stats_sql)

    conn.commit()

conn.close()
