#!/usr/bin/env python3

from gzip import decompress
from subprocess import check_call
from os import environ
from tempfile import NamedTemporaryFile
from urllib.request import urlopen


agent = environ["AGENT"]

iptables_rule = ("PREROUTING -t nat -p tcp -m tcp --destination "
                 f"{agent} --dport 22 -j REDIRECT --to-ports 10022")
chisel_arguments = ["server", "--reverse", "--port", "443"]
chisel = ("https://github.com/jpillora/chisel/releases/download/"
          "v1.7.2/chisel_1.7.2_linux_amd64.gz")


def main():
    with NamedTemporaryFile("wb", delete=False) as fp, urlopen(chisel) as res:
        fp.write(decompress(res.read()))

    check_call(["chmod", "+x", fp.name])
    check_call("sysctl -w net.ipv4.ip_forward=1".split())
    check_call(["iptables", "-v", "-A"] + iptables_rule.split())
    check_call([fp.name] + chisel_arguments)


if __name__ == "__main__":
    main()
