from mnist_models import Classifier, init_weights, accuracy, validate
from communicator import Server 
import torch
from torchvision.datasets import MNIST
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from torch.utils.data import random_split, DataLoader, Subset
import torch.nn as nn
import torch.nn.functional as F
import threading
import sys

argc = len(sys.argv)
if argc < 2 or argc > 3:
    print(f"Usage: python {sys.argv[0]} <worker_id> [-m]\n\t -m: worker is malicious")
    sys.exit(1)

torch.manual_seed(0)  # for reproducibility
dataset_size = 60000


################################################
#               META INFO                      #
################################################
WORKER_ID = int(sys.argv[1])  # id from 0 to 4
MALICIOUS = False
if argc == 3:
    MALICIOUS = True
SLEEPTIME = 2

perm_idxs = torch.randperm(dataset_size)
worker_idxs = perm_idxs[WORKER_ID*10000:(WORKER_ID+1)*10000]

################################################
#               Get Datasets                   #
################################################
# MNIST dataset (images and labels)
dataset = MNIST(root='data/', download=True, train=True, transform=transforms.ToTensor())
test_dataset = MNIST(root='data/', train=False, transform=transforms.ToTensor())

batch_size = 128
train_ds = Subset(dataset, worker_idxs)
train_data = dataset.data[worker_idxs]
train_target = dataset.targets[worker_idxs]

train_loader = DataLoader(train_ds, batch_size, shuffle=True)
# val_loader = DataLoader(val_ds, batch_size)

################################################
#            Get Models and Initialize         #
################################################
model = Classifier(hidden_1=0)
model.apply(init_weights)

lr = 0.001
lossfn = F.cross_entropy
opt = torch.optim.SGD(model.parameters(), lr)

################################################
#    Networking Stuff (only run this once!)    #
################################################
PORT = 1232
PORT2 = 1233
HOSTADDR = "container1"
serv = Server(PORT)
loc_model = (HOSTADDR, PORT)
loc_server = (HOSTADDR, PORT2)

import time

dataloader_iterator = iter(train_loader)

grad_scale = 1
if MALICIOUS:
    grad_scale = -10 

while True:
#     enter = input('Hit ENTER to send update:')
#     while enter != '':
#         enter = input('Hit ENTER to send update:')
    # send request to server for model w
    msg = "Req"
    serv.send(loc_model, msg)
#     print(f"Sent {str(msg)}")

    # wait for model
    server_state_dict = serv.recv()
    # get model and load
    model.load_state_dict(server_state_dict)

    # now compute gradient and send state_dict
    # first get a sample
    try:
        data, target = next(dataloader_iterator)
    except StopIteration:
        dataloader_iterator = iter(train_loader)
        data, target = next(dataloader_iterator)
    # zero out grad
    opt.zero_grad()
    # get prediction from current (latest) model
    pred = model(data)
    loss = lossfn(pred, target)
    loss.backward()
    # now the gradients are stored inside the state_dict. We send grad_dict
    grad_dict = {k:v.grad*grad_scale for k, v in zip(model.state_dict(), model.parameters())}
#     print(grad_dict)
    serv.send(loc_server, grad_dict)
    time.sleep(SLEEPTIME)
