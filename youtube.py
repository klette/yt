
import urllib
import sys
import os
import tempfile

class HTMLFetchException(Exception):
    pass

class ParseError(Exception):
    pass

def check_key_val(val):
    if '=' in val:
        return val

def get_available_sources(link):
    try:
        raw_html = urllib.urlopen(link).read()
    except Exception, e:
        print e
        raise HTMLFetchException()

    try:
        raw_dict = map(check_key_val, map(urllib.unquote, raw_html.split('&')))
        raw_dict = filter(bool, raw_dict)

        sources = dict(map(lambda x: (x[:x.index('=')],x[x.index('=')+1:]), raw_dict))['fmt_stream_map']
        sources = dict(map(lambda x: x.split('|')[:2], sources.split(',')))
        qualities = map(int, sources.keys())
        qualities.sort()
        best = qualities[-1]
        best_source = sources[str(best)]
        return best_source
    except Exception, e:
        print e
        raise ParseError()



def convert_to_mp3(link, db, yt_file):
    filename = tempfile.mktemp(suffix='.flv')
    def report_progress(count, block_size, total_size):
        percent = int(count*block_size*100/total_size)
        cursor = db.cursor()
        cursor.execute("UPDATE yt_file SET status = %s WHERE yt_file = %s", ("Downloading %d%% complete" % percent, yt_file))
        cursor.close()
        db.commit()

    urllib.urlretrieve(link, filename, report_progress)
    cursor = db.cursor()
    cursor.execute("UPDATE yt_file SET status = %s WHERE yt_file = %s", ("Transcoding", yt_file))
    cursor.close()
    db.commit()
    ret = os.system('ffmpeg -i %s  -ab 192k %s.mp3' % (filename, filename))
    cursor = db.cursor()
    if ret:
        cursor.execute("UPDATE yt_file SET status = %s WHERE yt_file = %s", ("Transcoding failed.. bummer dude.", yt_file))
    else:
        cursor.execute("UPDATE yt_file SET status = %s WHERE yt_file = %s", ("Done", yt_file))
    cursor.close()
    db.commit()
    if not ret:
        return filename
    else:
        return False
