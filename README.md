# traversal-poc

## Version 2

**MANAGER**

Run this

```
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/v2/manager.py \
    | sudo env AGENTS=<agent1-ip>[,<agent2-ip>,<agent3-ip>...] python
```

Or add this cron rule through `sudo crontab -e`.

```
@reboot /usr/bin/sh -c '/usr/bin/curl --retry 60 --retry-delay 10 -vsSL https://github.com/sakurai-youhei/traversal-poc/raw/main/v2/manager.py | /usr/bin/env AGENTS=<agent1-ip>[,<agent2-ip>,<agent3-ip>...] /usr/bin/python' >> /var/log/traversal-poc.log 2>&1 &
```

**AGENT**

Run this (_Note: The `agent-index` starts from 1._)

```
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/v2/agent.py \
    | sudo env INDEX=<agent-index> MANAGER=<manager-ip> python
```

Or add this cron rule through `sudo crontab -e`.

```
@reboot /usr/bin/sh -c '/usr/bin/curl --retry 60 --retry-delay 10 -vsSL https://github.com/sakurai-youhei/traversal-poc/raw/main/v2/agent.py | /usr/bin/env INDEX=<agent-index> MANAGER=<manager-ip> /usr/bin/python' >> /var/log/traversal-poc.log 2>&1 &
```

**Prerequisites**

- sudo or cron
- iptables
- curl
- Python 2.7 or 3
- [jpillora/chisel](https://github.com/jpillora/chisel) (to be downloaded automatically)

**Diagram**

```
   MANAGER                 NA(P)T/PROXY     AGENT
  +------------------+    +------------+   +--------------------+
  | 5432<-------+    |    |            |   |                    |
  | 443<--------+    |    |            |   |                    |
  | 80<---------+    |    | WebSocket  |   |                    |
  | 22<---------+    |    |   over     |   |   +------------>22 |
  |             |    |    |    SSL/TLS |   |   |                |
  | *        [chisel]<----------------------[chisel]          * |
  | |   +(22)->10023 |    | (8443/tcp) |   | 15432<-(5432)+   | |
  | |   |      10024 |    |            |   | 10443<-(443)-+   | |
  | |   |      10025 |    |            |   | 10080<-(80)--+   | |
  | |   |        ... |    |            |   | 10022<-(22)--+   | |
  | |   |            |    |            |   |              |   | |
  | +---+            |    |            |   |              +---+ |
  |[iptables]        |    |            |   |          [iptables]|
  +------------------+    +------------+   +--------------------+
```

- chisel established bi-directional communication tunnel over wss:// (WebSocket over SSL/TLS) through 8443/tcp.
- When AGENT opens channels to 5432/tcp, 443/tcp, 80/tcp and 22/tcp on MAANGER, iptables on AGENT redirects the communication to local 15432/tcp, 10443/tcp, 10080/tcp and 10022/tcp which ports will be tunneled to MAANGER's remote 5432/tcp, 443/tcp, 80/tcp and 22/tcp by chisel.
- When MANAGER  opens channels to 22/tcp on AGENT, iptables on MANAGER redirects the communication to local 1002x/tcp which port will be tunneled to AGENT's remote 22/tcp by chisel.

**Configuration notes**

- Source IP of network communication to MANAGER is not AGENT's IP but MANAGER's 127.0.0.1.
- Source IP of network communication to AGENT is not MANAGER's IP but AGENT's 127.0.0.1.
