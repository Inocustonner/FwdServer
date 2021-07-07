# Example usage
```sh
python main.py localhost:5555 localhost:6666
```

# What is this
This will link `localhost:5555` <---> `localhost:6666`

So any socket that will connect to `localhost:5555` can be considered to be connected to `localhost:6666`, because any data sent to `localhost:5555` will be forwarded to `localhost:6666` and the other way around. Same with `recv`