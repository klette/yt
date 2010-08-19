import sys
import os
import psycopg2
sys.path.append('/home/klette/dev/pyroutes')
sys.path.append('/var/www/yt.klette.us')

from pyroutes import application
from pyroutes import route, settings
from pyroutes.http.response import Response
from pyroutes.template import TemplateRenderer

from youtube import *

tr = TemplateRenderer('base.html')

@route('/')
def index(request):
    return Response(tr.render('index.html',{}))

@route('/process')
def process(request):
    link = request.POST.get('url', None)
    if not link:
        return Response('FAIL')

    try:
        source = get_available_sources(link)
    except:
        return Response('No sources found.. sorry.')
    db = psycopg2.connect(settings.DB_DSN)
    cursor = db.cursor()
    cursor.execute("SELECT yt_file FROM yt_file WHERE url = %s AND status NOT ILIKE '%%fail%%'", (link,))
    if not cursor.rowcount:
        cursor.execute('INSERT INTO yt_file (url) values (%s) RETURNING yt_file', (link,))
    (yt_file) = cursor.fetchone()
    cursor.close()
    db.commit()
    db.close()
    return Response(tr.render('process.html', {'#yt_file/id': 'id_%s' % yt_file}))

@route('/report')
def report(request, yt_file):
    try:
        yt_file = int(yt_file)
    except:
        return Response('Fail')
    db = psycopg2.connect(settings.DB_DSN)
    cursor = db.cursor()
    cursor.execute('SELECT status FROM yt_file WHERE yt_file = %s', (yt_file,))
    res = cursor.fetchone()
    if res:
        (status,) = res
    else:
        status = 'none'
    return Response(str(status))
