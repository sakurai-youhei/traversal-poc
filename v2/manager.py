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
from textwrap import dedent
from threading import Timer
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


def iptables(agents):
    for index, agent in enumerate(filter(None, agents), start=1):
        cmd = ("/sbin/iptables -v -t nat -A OUTPUT -p tcp --destination "
               "%(agent)s --dport 22 -j REDIRECT --to-port 1%(port)04d"
               ) % dict(agent=agent, port=22 + index)
        check_call(cmd.split())

    timer = Timer(10, iptables, args=(agents, ))
    timer.setDaemon(True)
    timer.start()


def main():
    agents = environ["AGENTS"].split(",")

    url = ("https://github.com/jpillora/chisel/releases/download/"
           "v1.7.2/chisel_1.7.2_linux_amd64.gz")
    with closing(urlopen(url)) as res, \
            NamedTemporaryFile("wb", delete=False) as fp:
        fp.write(decompress(res.read()))
    check_call(["chmod", "+x", fp.name])

    timer = Timer(10, iptables, args=(agents, ))
    timer.setDaemon(True)
    timer.start()

    with NamedTemporaryFile("w", delete=False) as crt, \
            NamedTemporaryFile("w", delete=False) as key:
        print(dedent("""\
            # DO NEVER EVER USE THIS FOR PRODUCTION PURPOSE
            -----BEGIN CERTIFICATE-----
            MIIC/DCCAeSgAwIBAgIJALfSv+K8yCwDMA0GCSqGSIb3DQEBBQUAMCcxJTAjBgNV
            BAMTHHRyYXZlcnNhbC1wb2Muc2FrdXJhaS15b3VoZWkwHhcNMjAxMTEwMDQ0NzU1
            WhcNMzAxMTA4MDQ0NzU1WjAnMSUwIwYDVQQDExx0cmF2ZXJzYWwtcG9jLnNha3Vy
            YWkteW91aGVpMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnRVU1dji
            jvM6pMOskinE9UGvpqr4uulkJnrohGfagyH9k3e31cMeeYJyZ1MR7umDS6DWK0M3
            TJ8KbYs9jDKneiMOsld4hmsvPoIHINeJ2pMSyMVHkHh4e7p6eba+s4HtulIgdXej
            crZ5EF2NlJg7Kk2ri0bZumejklo/R1Jy0EBJaSPGtBack4ZMQW02GucUAh3e7dtN
            4c/XQsLpAj3Wu2zExI8yqyzm9bqdLhkQ1Cg/Ac/QYiryaMWb5h85z/yUDz83KfOU
            kWyzfZQHwv93y68L1QdR3Hr/sA0dsgtEBJVgL22cNaEy1sil4Oxf3i7vvWY6qmOv
            /U6Y3IsfUCnKtQIDAQABoyswKTAnBgNVHREEIDAeghx0cmF2ZXJzYWwtcG9jLnNh
            a3VyYWkteW91aGVpMA0GCSqGSIb3DQEBBQUAA4IBAQAhPMq8ua1eTb8dkNwg4plJ
            dRRGmfHOKkpaaXE3FSDtS/NVeRrK1nFZeYdXKXygAzqkongWB6dhAR4SLrydrL0w
            /jIxBdksX1wul0w2Y6onEdR2/zN2G5xjETOenBsBuJBjUODs/KtQWKCexCcpp15p
            59fUS/bebcIk2E910L6U+tWXqXwPxqXsy86b6FFfMzBy1RDGLrbTGlRHsOv0wT3Z
            K7PsKVhSGF7vjL1V9gnBPhGkiQDGEj83ny0a59E1LJ0PP5v8rxPCnqiqiiLpg3c8
            3AF6C3wZ2SbJHDmM9u17WdiiYaAggLUC3KLBcCr+0rcGxfMP0scUV/iYYUNiXDrO
            -----END CERTIFICATE-----
        """), file=crt)
        print(dedent("""\
            # DO NEVER EVER USE THIS FOR PRODUCTION PURPOSE
            -----BEGIN RSA PRIVATE KEY-----
            MIIEpAIBAAKCAQEAnRVU1djijvM6pMOskinE9UGvpqr4uulkJnrohGfagyH9k3e3
            1cMeeYJyZ1MR7umDS6DWK0M3TJ8KbYs9jDKneiMOsld4hmsvPoIHINeJ2pMSyMVH
            kHh4e7p6eba+s4HtulIgdXejcrZ5EF2NlJg7Kk2ri0bZumejklo/R1Jy0EBJaSPG
            tBack4ZMQW02GucUAh3e7dtN4c/XQsLpAj3Wu2zExI8yqyzm9bqdLhkQ1Cg/Ac/Q
            YiryaMWb5h85z/yUDz83KfOUkWyzfZQHwv93y68L1QdR3Hr/sA0dsgtEBJVgL22c
            NaEy1sil4Oxf3i7vvWY6qmOv/U6Y3IsfUCnKtQIDAQABAoIBAQCFhHEkh4IjEXkC
            PVP8tMY11QxRNTfP37uBvazPhlrEZWrdIsA+UOghThCh5Ij0ssUnzmDcSvjBBtnd
            PKIm/ZM/DHdcfV7zmj2A+xLGBo6lG6e2wYDPuqZmPJ4HwJ4dhE2ltlLipbtnMNR8
            ZZiG+lIn5fbunl1IxPjS2CS7Ich3Wyg/b00CnBLF2YuRhOpQkoUUekkzTNaxxMiw
            80KSJ/XiJtSaICY5jO0+OPidNwKDV++Bi5ag+9+e3CORSsOZGm9xlOt89QCNK6aU
            Brtyxm9KJ8Pvw/b9qRUQFWOmEXWISFKTxo1Rr2fdyQhaxGPFivNp5VvG0+2gOWvE
            SO0ASLyNAoGBAM5rvk9NND4ywMSKBX+o2XC4PxwSvEe7WYg/Vr9DHsK+WPKQoV9e
            3WTEFqxj3VwHeLxTiI5nChlVX4mh0ueU5f3/iWFVCGN7Id69zAHhsspflRDdsl3m
            C54MRnppZSjF/3BL40aIi4DmerZeNKIArBWW4MKBf0N4G1SotaOaboW/AoGBAMLP
            9O5VMymuIOYQh9wkK/h8sjxJ00iJOYwv52bikKsUL4P7DyM2h/ni+KXr7PKMrOx/
            aov9t8siQxnnGzQbZYSxwo9uhDcHSDLretZJCr+EZfuJxIgWG540dCbml1s0Adfh
            efEMhzkh3T/5/6pe8tRkkXAbeXCh+SxJwti729SLAoGAaTy89akirWMqrAjB7Oek
            k7cbVbCnlNqLNs8z5qbNk/N/XYsm+nxe2vStqo3vWO/mOf1MbW1S1L+VyZFa+P4M
            k4YoABtd/3nTNsAEtiDfChXY5ZRhT0XtPlJ7zATXsgXfyNynrloG5Vyby0YUB1PY
            Z9lYFVH4E+mz5WFt2U7ucfkCgYBUW67JQbWc990hIsliB3vO51hbCPDn+RwlW10N
            zVAt9Ni6gw3EBsoM6D8ZwjbhtQ7wfiBKLHzZBqYd4liCUNa+Biek6otwNMQL4LJZ
            dlmkIxXyPW8QKtqcwEQH0FR8VuHxdJ7URcOMduCS4pPWV7U5Sa8853jH0CvRBMPO
            DFMeDwKBgQCi92xFdpT3d5vxYk4ejflfGVjp/nD8igm1bTwEWQqMp+EVYFrsWekN
            jF9LB8q6EEFLXBn1B7dXKGWlEJYjM9Vfbice7Vszjf/E9uEWMT3Sq41Sqs7E9iRf
            FO5l6w5JIv86uG8iHyELpNP2Kp8xUMWdtaTq8BhGx1gNb1uwSdTCXw==
            -----END RSA PRIVATE KEY-----
        """), file=key)

    while True:
        check_call([fp.name, "server", "-v", "--reverse", "--port", "8443",
                    "--tls-cert", crt.name, "--tls-key", key.name])


if __name__ == "__main__":
    main()
