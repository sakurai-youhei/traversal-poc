# traversal-poc

## Version 1

**SERVER**

```
export AGENT=172.xx.xx.xx
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/v1/server.py | sudo -E python3
```

**CLIENT**

```
export SERVER=192.xx.xx.xx
export MANAGER=192.xx.xx.xx
export AGENT=172.xx.xx.xx
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/v1/client.py | sudo -E python3
```

**Prerequisites**

- sudo
- iptables
- curl
- Python 3.7 or later

**Diagram**

```
   MANAGER                                                  AGENT
  +-------+                                                +-----+
  | 5432  |                                                |     |
  | 443   |                                                |     |
  | 80    |                                                |     |
+-->22    |                                                |  22<--+
| |       |                                                |     | |
| +--+----+                                                +---+-+ |
|    |       SERVER          NA(P)T/PROXY         CLIENT       |   |
|    |   +-------------+    +------------+   +---------------+ |   |
|    |   |[iptables]   |    |            |   |     [iptables]| |   |
|    +-----+           |    |            |   |           +-----+   |
|        | |           |    |            |   |           |   |     |
|        | |           |    |            |   |           v   |     |
|        | |           |    |            |   | 15432 <- 5432 |     |
|        | |           |    | WebSocket  |   | 10443 <- 443  |     |
|        | v           |    |   over     |   | 10080 <- 80   |     |
|        | 22 -> 10022 |    |    SSL/TLS |   | 10022 <- 22   |     |
+--------------[chisel]<----------------------[chisel]-------------+
         |             |    |  (443/tcp) |   |               |
         +-------------+    +------------+   +---------------+
```

**Configuration notes**

- Gateway on MANAGER should be pointed to SERVER's IP, which allows port redirection of network communication to AGENT on SERVER.
- Gateway on AGENT should be pointed to CLIENT's IP, which allows port redirection of network communication to MANAGER on CLIENT.
- Source IP of network communication to MANAGER is not AGENT's but SERVER's, which affects firewall rule/s on MANAGER.
- Source IP of network communication to AGENT is not MANAGER's but CLIENT's, which affects firewall rule/s on AGENT.
