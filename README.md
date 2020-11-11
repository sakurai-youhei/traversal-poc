# traversal-poc

## Version 2

**MANAGER**

```
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/v2/manager.py \
    | sudo env AGENTS=<agent1-ip>[,<agent2-ip>,<agent3-ip>...] python3
```

**AGENT**

```
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/v2/agent.py \
    | sudo env INDEX=<agent-index> MANAGER=<manager-ip> python3
```

_Note: The `agent-index` starts from 1._

**Prerequisites**

- sudo
- iptables
- curl
- Python 2.7 or 3

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

**Configuration notes**

- Source IP of network communication to MANAGER is not AGENT's IP but MANAGER's localhost.
- Source IP of network communication to AGENT is not MANAGER's IP but AGENT's locahost.
