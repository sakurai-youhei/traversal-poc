#!/usr/bin/env python

from __future__ import print_function

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
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


def main():
    index = int(environ["INDEX"])
    manager = environ["MANAGER"]

    for port in (22, 80, 443, 5432):
        cmd = ("iptables -v -t nat -A OUTPUT -p tcp --destination %(manager)s "
               "--dport %(port)d -j REDIRECT --to-port 1%(port)04d") % dict(
                   manager=manager, port=port)
        check_call(cmd.split())

    url = ("https://github.com/jpillora/chisel/releases/download/"
           "v1.7.2/chisel_1.7.2_linux_amd64.gz")
    with urlopen(url) as res, NamedTemporaryFile("wb", delete=False) as fp:
        fp.write(decompress(res.read()))
    check_call(["chmod", "+x", fp.name])

    while True:
        opts = ("client -v --tls-skip-verify https://%(manager)s:8443 "
                "0.0.0.0:10022:%(manager)s:22 0.0.0.0:10080:%(manager)s:80 "
                "0.0.0.0:10443:%(manager)s:443 0.0.0.0:15432:%(manager)s:5432 "
                "R:0.0.0.0:1%(port)04d:127.0.0.1:22") % dict(
                    manager=manager, port=22 + index)
        check_call([fp.name] + opts.split())


if __name__ == "__main__":
    main()
