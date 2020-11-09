#!/usr/bin/env python3

from gzip import decompress
from subprocess import check_call
from subprocess import Popen
from os import environ
from tempfile import NamedTemporaryFile
from urllib.request import urlopen


downstream = environ["DOWNSTREAM"]

iptables_rule = ("PREROUTING -t nat -p tcp -m tcp --destination "
                 f"{downstream} --dport 22 -j REDIRECT --to-ports 10022")
chisel_arguments = ["server", "--reverse"]
chisel = ("https://github.com/jpillora/chisel/releases/download/"
          "v1.7.2/chisel_1.7.2_linux_amd64.gz")


def main():
    with NamedTemporaryFile("wb", delete=False) as fp, urlopen(chisel) as res:
        fp.write(decompress(res.read()))

    check_call(["chmod", "+x", fp.name])
    check_call("sysctl -w net.ipv4.ip_forward=1".split())
    check_call(["iptables", "-A"] + iptables_rule.split())
    with Popen([fp.name] + chisel_arguments) as proc:
        proc.wait()


if __name__ == "__main__":
    main()
