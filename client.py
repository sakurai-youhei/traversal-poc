#!/usr/bin/env python3

from gzip import decompress
from subprocess import check_call
from subprocess import Popen
from os import environ
from tempfile import NamedTemporaryFile
from urllib.request import urlopen


server = environ["SERVER"]
upstream = environ["UPSTREAM"]
downstream = environ["DOWNSTREAM"]

iptables_rules = [f"PREROUTING -t nat -p tcp -m tcp --destination {upstream} "
                  f"--dport {port} -j REDIRECT --to-ports 1{port:0>4}"
                  for port in (22, 80, 5432)]
chisel_arguments = ["client",
                    f"http://{server}",
                    f"0.0.0.0:10022:{upstream}:22",
                    f"0.0.0.0:10080:{upstream}:80",
                    f"0.0.0.0:15432:{upstream}:5432",
                    f"R:0.0.0.0:10022:{downstream}:22"]
chisel = ("https://github.com/jpillora/chisel/releases/download/"
          "v1.7.2/chisel_1.7.2_linux_amd64.gz")


def main():
    with NamedTemporaryFile("wb", delete=False) as fp, urlopen(chisel) as res:
        fp.write(decompress(res.read()))

    check_call(["chmod", "+x", fp.name])
    check_call("sysctl -w net.ipv4.ip_forward=1".split())
    for rule in iptables_rules:
        check_call(["iptables", "-A"] + rule.split())
    with Popen([fp.name] + chisel_arguments) as proc:
        proc.wait()


if __name__ == "__main__":
    main()