# traversal-poc

## Version 1

**server**

```
export AGENT=172.xx.xx.xx
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/v1/server.py | sudo -E python3
```

**client**

```
export SERVER=192.xx.xx.xx
export MANAGER=192.xx.xx.xx
export AGENT=172.xx.xx.xx
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/v1/client.py | sudo -E python3
```

## Diagram

```
  MANAGER                                                   AGENT
  +------+                                                 +-----+
  | 5432 |                                                 |     |
  | 80   |                                                 |     |
+-->22   |                                                 |  22<--+
| |      |                                                 |     | |
| +--+---+                                                 +---+-+ |
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
