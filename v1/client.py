#!/usr/bin/env python3

from gzip import decompress
from subprocess import check_call
from os import environ
from tempfile import NamedTemporaryFile
from urllib.request import urlopen


server = environ["SERVER"]
manager = environ["MANAGER"]
agent = environ["AGENT"]

iptables_rules = [f"PREROUTING -t nat -p tcp -m tcp --destination {manager} "
                  f"--dport {port} -j REDIRECT --to-ports 1{port:0>4}"
                  for port in (22, 80, 5432)]
chisel_arguments = ["client",
                    f"https://{server}",
                    f"0.0.0.0:10022:{manager}:22",
                    f"0.0.0.0:10080:{manager}:80",
                    f"0.0.0.0:15432:{manager}:5432",
                    f"R:0.0.0.0:10022:{agent}:22"]
chisel = ("https://github.com/jpillora/chisel/releases/download/"
          "v1.7.2/chisel_1.7.2_linux_amd64.gz")


def main():
    with NamedTemporaryFile("wb", delete=False) as fp, urlopen(chisel) as res:
        fp.write(decompress(res.read()))

    check_call(["chmod", "+x", fp.name])
    check_call("sysctl -w net.ipv4.ip_forward=1".split())
    for rule in iptables_rules:
        check_call(["iptables", "-v", "-A"] + rule.split())
    check_call([fp.name] + chisel_arguments)


if __name__ == "__main__":
    main()
