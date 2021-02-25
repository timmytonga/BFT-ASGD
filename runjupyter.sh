#!/bin/bash

if [ -z ${1+x} ] || [ -z ${2+x} ]; then 
	echo "usage: $0 <container_name> <local_port_for_notebook>"; 
	exit 1;
fi

DOCKERIMAGENAME=bftasgd

docker build . -t $DOCKERIMAGENAME
docker rm -f $1
# replace bftasgd with whatever you name your docker build image with
docker run --name $1 --hostname $1 --network mynetwork -it -p $2:8888 $DOCKERIMAGENAME /bin/bash -c "/opt/conda/bin/jupyter notebook --ip 0.0.0.0 --port=8888 --allow-root --no-browser";
echo "Now type localhost:8888 into a browser (from host) to access the notebook from this container"
