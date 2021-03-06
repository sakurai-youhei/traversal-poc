#!/usr/bin/env python

from __future__ import print_function

from contextlib import closing
try:
    from gzip import decompress
except ImportError:
    from io import BytesIO
    from gzip import GzipFile

    def decompress(data):
        with GzipFile(fileobj=BytesIO(data)) as f:
            return f.read()
from subprocess import check_call
from os import environ
from tempfile import NamedTemporaryFile
from threading import Timer
from time import sleep
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


def iptables(manager):
    for port in (22, 80, 443, 5432):
        cmd = ("/sbin/iptables -v -w 10 -t nat -A OUTPUT -p tcp --destination "
               "%(manager)s --dport %(port)d -j REDIRECT --to-port 1%(port)04d"
               ) % dict(manager=manager, port=port)
        check_call(cmd.split())

    timer = Timer(10, iptables, args=(manager, ))
    timer.setDaemon(True)
    timer.start()


def main():
    index = int(environ["INDEX"])
    manager = environ["MANAGER"]

    timer = Timer(10, iptables, args=(manager, ))
    timer.setDaemon(True)
    timer.start()

    url = ("https://github.com/jpillora/chisel/releases/download/"
           "v1.7.2/chisel_1.7.2_linux_amd64.gz")
    for _ in range(10):
        try:
            with closing(urlopen(url)) as res, \
                    NamedTemporaryFile("wb", delete=False) as fp:
                fp.write(decompress(res.read()))
        except Exception as e:
            sleep(5)
        else:
            break
    else:
        raise e
    check_call(["chmod", "+x", fp.name])

    while True:
        opts = ("client -v --tls-skip-verify https://%(manager)s:8443 "
                "0.0.0.0:10022:127.0.0.1:22 0.0.0.0:10080:127.0.0.1:80 "
                "0.0.0.0:10443:127.0.0.1:443 0.0.0.0:15432:127.0.0.1:5432 "
                "R:0.0.0.0:1%(port)04d:127.0.0.1:22") % dict(
                    manager=manager, port=22 + index)
        check_call([fp.name] + opts.split())


if __name__ == "__main__":
    main()
