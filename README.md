# bft-asgd

## Setup
```docker build . -t bftasgd```

Running the container interactively:
```docker run --hostname <host> --name <host> --network <net> --rm -it bftasgd```
 
## Running the container through Jupyter
Included is a script named ```runjupyter.sh```. This is meant to be run after building the docker image. We must modify the imagename in the run command inside ```runjupyter.sh``` to match with the image name that we built with. It has the following usage:
```
./runjupyter.sh <container_name> <port_on_host>
```

So an example would be to run ```./runjupyter.sh container1 8889```. Then we would have a Jupyter Notebook running in the docker's container. We can access the notebook by typing ```localhost:8889``` in a browser (in the host) and copying a token from terminal to access the notebook running in the container.

Run server and worker from inside the Jupyter Notebook of the container. The server must run on "container1". All container names are in Hostfile.
