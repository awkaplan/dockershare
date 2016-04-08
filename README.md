# DockerShare
## Description
Use Docker Hub to store and retrieve files!  Be warned, this is some disgusting, lazy Python.

## Usage
```
python dockershare.py --help
usage: dockershare.py [-h] [--debug] [--socket SOCKET | --machine]
                      {put,get} ...

Store and retrieve files on Docker Hub!

positional arguments:
  {put,get}

optional arguments:
  -h, --help            show this help message and exit
  --debug               Debugging output
  --socket SOCKET, -s SOCKET
                        Path to Docker socket
  --machine, -m         Use Docker machine?
```

## Notes
If you're using boot2docker / docker-machine, do the following before running DockerShare with the --machine flag:
```
$ eval "$(docker-machine env name_of_machine)"
```