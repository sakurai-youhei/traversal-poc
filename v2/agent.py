#!/usr/bin/env python3

from gzip import decompress
from subprocess import check_call
from os import environ
from tempfile import NamedTemporaryFile
from urllib.request import urlopen


def main():
    index = int(environ["INDEX"])
    manager = environ["MANAGER"]

    for port in (22, 80, 443, 5432):
        cmd = (f"iptables -v -t nat -A OUTPUT -p tcp --destination {manager} "
               f"--dport {port} -j REDIRECT --to-port 1{port:0>4}")
        check_call(cmd.split())

    url = ("https://github.com/jpillora/chisel/releases/download/"
           "v1.7.2/chisel_1.7.2_linux_amd64.gz")
    with urlopen(url) as res, NamedTemporaryFile("wb", delete=False) as fp:
        fp.write(decompress(res.read()))
    check_call(["chmod", "+x", fp.name])

    while True:
        check_call([fp.name, "client", "-v", "--tls-skip-verify",
                    f"https://{manager}:8443"
                    f"0.0.0.0:10022:{manager}:22",
                    f"0.0.0.0:10080:{manager}:80",
                    f"0.0.0.0:10443:{manager}:443",
                    f"0.0.0.0:15432:{manager}:5432",
                    f"R:0.0.0.0:{(10022 + index)}:127.0.0.1:22"])


if __name__ == "__main__":
    main()
