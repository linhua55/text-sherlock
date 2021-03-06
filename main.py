#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
main.py - Runs the main application.

Created by Christopher Bess (https://github.com/cbess/text-sherlock)
Copyright 2012
"""

from app_args import get_options
from webapp import server
from core.sherlock import indexer, backends, db
from core import FORCE_INDEX_REBUILD, utils, get_version_info, \
    SherlockMeta, SHORT_DATE_FORMAT
import settings
import os
import sys
from datetime import datetime


def show_version():
    pyver = sys.version_info
    print '  Python: v%d.%d.%d' % (pyver[0], pyver[1], pyver[2])
    print 'Sherlock: v' + get_version_info('sherlock')
    print '   Flask: v' + get_version_info('flask')
    print 'Pygments: v' + get_version_info('pygments')
    print '  Whoosh: v' + get_version_info('whoosh')
    print 'CherryPy: v' + get_version_info('cherrypy')


def show_stats():
    # backend stats
    print 'Available indexer backends: %s' % backends.indexer_names()
    print 'Available searcher backends: %s' % backends.searcher_names()
    print 'Current backend: %s' % settings.DEFAULT_SEARCHER
    # indexer stats
    idxr = indexer.get_indexer(rebuild_index=False)
    print 'Total documents indexed: %d' % idxr.doc_count()
    # database stats
    print 'Index Database: %s' % db.DATABASE_PATH


def run_server():
    if settings.LOG_PATH:
        print 'Log path: %s' % settings.LOG_PATH
    print 'Backend: %s' % settings.DEFAULT_SEARCHER
    print 'Server: %s' % settings.SERVER_TYPE
    print 'Listening on: %s:%d' % (settings.SERVER_ADDRESS, settings.SERVER_PORT)
    # launch web server
    server.run()


def reindex():
    path = utils.resolve_path(settings.INDEX_PATH)
    # check path
    if not path.endswith('/'):
        raise Exception('INDEX_PATH must end with a trailing slash. %s' % path)
    if not os.path.exists(path):
        raise Exception('Check INDEX_PATH. Does it exist? %s' % path)
    print 'Indexing path: %s' % path
    if FORCE_INDEX_REBUILD:
        wait_time = 5 # seconds to wait/pause until rebuilding index
        print 'Reindexing everything!'
        print 'Waiting %ss for interrupt...' % wait_time
        import time
        time.sleep(wait_time)
    print 'Indexing started.'
    indexer.index_path(path)
    show_stats()
    print 'Indexing done.'
    # record indexed time
    SherlockMeta.set('last_indexed', datetime.now().strftime(SHORT_DATE_FORMAT))


def run():
    options = get_options()
    # determine app action
    if options.run_tests:
        import tests
        tests.run_all()
    elif options.show_version:
        show_version()
    elif options.show_stats:
        show_stats()
    elif options.run_server:
        run_server()
    elif options.reindex:
        reindex()
    else:
        print 'Use -h to see options.'


if __name__ == '__main__':
    print 'Running sherlock...'
    run()
