import communicator
import sys
import torch

PORT = 1232
HOSTADDR = "container1"
myid = sys.argv[1]
print(f"My id: {myid}")

if myid == '0':
	print("I am server. Waiting for msg...")
	serv = communicator.Server(PORT)
	result = serv.recv()
	print(f"Received obj of type {str(type(result))} and content:\n{str(result)}")


if myid == '1':
	print("I am client. Sending msg...")
	loc = (HOSTADDR, PORT)
	sender = communicator.Client()
	testobj = torch.randn(4, 10)
	sender.send(loc, testobj)
	print(f"Sent {str(testobj)}")
