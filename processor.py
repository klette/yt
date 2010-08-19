import psycopg2
import shutil
import os
import time
from youtube import *
from pyroutes import settings

while True:
    db = psycopg2.connect(settings.DB_DSN)
    cursor = db.cursor()
    cursor.execute("SELECT yt_file, url, status FROM yt_file WHERE status = 'Queued' ORDER BY yt_file ASC LIMIT 1")
    if cursor.rowcount:
        (yt_file, url, status) = cursor.fetchone()
        source = get_available_sources(url)
        filename = convert_to_mp3(source, db, yt_file)
        if filename:
            shutil.move(filename + ".mp3", os.path.join(settings.MP3_DIR, '%s.mp3' % yt_file))
            shutil.os.unlink(filename)
    cursor.close()
    db.close()

    time.sleep(1)

