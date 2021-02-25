import torch
import torchvision
import torch.nn as nn

input_size = 28*28
num_classes = 10
# first make our classifier... just basic 2 hidden layer feedforward
class Classifier(nn.Module):
    def __init__(self, input_size=28*28, num_classes=10, hidden_1=0):
        assert hidden_1 >= 0
        super().__init__()
        if hidden_1 == 0:
            self.layer = nn.Sequential(
                nn.Linear(input_size, num_classes),
                nn.Softmax(dim=1)
            ) 
        else:
            self.layer = nn.Sequential(
                nn.Linear(input_size, hidden_1),
                nn.Sigmoid(),
                nn.Linear(hidden_1, num_classes),
                nn.Softmax(dim=1)
            ) 
        
    def forward(self, xb):
        xb = xb.reshape(-1, 784)
        out = self.layer(xb)
        return out


def init_weights(m):
    if type(m) == nn.Linear:
        torch.nn.init.xavier_uniform_(m.weight)
        m.bias.data.fill_(0.01)


def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))


def validate(model, val_loader, lossfn):
    # validation step
    val_loss_temp = []
    val_acc_temp = []
    for val, val_label in val_loader:
        val_pred = model(val)
        val_loss = lossfn(val_pred, val_label)
        val_acc = accuracy(val_pred, val_label)
        val_loss_temp += [val_loss]
        val_acc_temp += [val_acc]
    epoch_val_loss = torch.stack(val_loss_temp).mean()
    epoch_val_acc = torch.stack(val_acc_temp).mean()
    return epoch_val_loss, epoch_val_acc
