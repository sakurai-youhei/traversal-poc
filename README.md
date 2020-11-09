# traversal-poc

**client**

```
export SERVER=192.xx.xx.xx
export UPSTREAM=192.xx.xx.xx
export DOWNSTREAM=172.xx.xx.xx
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/client.py | sudo -E python3
```

**server**

```
export DOWNSTREAM=172.xx.xx.xx
curl -sSL https://github.com/sakurai-youhei/traversal-poc/raw/main/server.py | sudo -E python3
```
