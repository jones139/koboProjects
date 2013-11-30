## gmail_test.py -- A command line util to check GMail -*- Python -*-

# ======================================================================
# Copyright (C) 2006 Baishampayan Ghose <b.ghose@ubuntu.com>
#               2013 Graham Jones <grahamjones139@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# ======================================================================

import urllib2             # For BasicHTTPAuthentication
import feedparser        # For parsing the feed
from textwrap import wrap # For pretty printing assistance

_URL = "https://mail.google.com/gmail/feed/atom/kobo"

def auth():
    '''The method to do HTTPBasicAuthentication
    created based on http://docs.python.org/2/howto/urllib2.html'''

    # create a password manager
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    # If we knew the realm, we could use it instead of None.
    top_level_url = "https://mail.google.com"
    username = "<username>@gmail.com"
    password = "<password>"
    password_mgr.add_password(None, top_level_url, username, password)

    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    opener = urllib2.build_opener(handler)

    # use the opener to fetch a URL
    f = opener.open(_URL)
    feed = f.read()
    return feed

def fill(text, width):
    '''A custom method to assist in pretty printing'''
    if len(text) < width:
        return text + ' '*(width-len(text))
    else:
        return text

def readmail(feed):
    '''Parse the Atom feed and print a summary'''
    atom = feedparser.parse(feed)
    print ""
    print atom.feed.title
    print "You have %s new mails" % len(atom.entries)
    # Mostly pretty printing magic
    print "+"+("-"*84)+"+"
    print "| Sl.|"+" Subject"+' '*48+"|"+" Author"+' '*15+"|"
    print "+"+("-"*84)+"+"
    for i in xrange(len(atom.entries)):
        print "| %s| %s| %s|" % (
            fill(str(i), 3),
            fill(wrap(atom.entries[i].title, 50)[0]+"[...]", 55),
            fill(wrap(atom.entries[i].author, 15)[0]+"[...]", 21))
    print "+"+("-"*84)+"+"

if __name__ == "__main__":
    f = auth()  # Do auth and then get the feed
    readmail(f) # Let the feed be chewed by feedparser
