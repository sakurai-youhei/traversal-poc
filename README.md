# traversal-poc

**server**

```
export DOWNSTREAM=172.xx.xx.xx
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/server.py | sudo -E python3
```

**client**

```
export SERVER=192.xx.xx.xx
export UPSTREAM=192.xx.xx.xx
export DOWNSTREAM=172.xx.xx.xx
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/client.py | sudo -E python3
```

## Diagram

```
UPSTREAM                           DOWNSTREAM
+------+                           +--------+
| 5432 |                           |        |
| 80   |                           |        |
| 22   |                           |  22    |
+--+---+                           +---+----+
   ^                                   ^
   |   +----+    +--------+   +----+   |
   |   |    |    |        |   |    |   |
   +-->+    +<----------------+    +<--+
       |    |    |        |   |    |
       +----+    +--------+   +----+
      (chisel)   NAPT/PROXY  (chisel)
       SERVER                 CLIENT

  [iptables]                 [iptables]
                             15432 <- 5432
                             10080 <- 80
  22 -> 10022                10022 <- 22
```
