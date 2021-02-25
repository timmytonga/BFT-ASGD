from nlknguyen/alpine-mpich
from continuumio/anaconda3

RUN conda install -y --quiet pytorch torchvision cpuonly -c pytorch
RUN conda install jupyter -y --quiet

ADD ./Hostfile /app/
ADD ./*.py /app/
ADD ./*.sh /app/
ADD ./*.ipynb /app/
#ADD ./*.csv /app/
ADD ./*.data /app/
ADD ./*.txt /app/

WORKDIR /app/
