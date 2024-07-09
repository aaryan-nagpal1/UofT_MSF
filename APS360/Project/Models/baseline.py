import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms

class MLP(nn.Module):
  def __init__(self,num_features,device):
    super(MLP, self).__init__()
    self.layer1 = nn.Linear(num_features, 32,device=device)
    self.layer2 = nn.Linear(32, 64,device=device)
    self.layer3 = nn.Linear(64, 128,device=device)
    self.layer4 = nn.Linear(128, 512,device=device)
    self.layer5 = nn.Linear(512, 64,device=device)
    self.layer6 = nn.Linear(64, num_features,device=device)
    self.relu = nn.ReLU()

  def forward(self, x):
    x = self.layer1(x)
    x = self.relu(x)
    x = self.layer2(x)
    x = self.relu(x)
    x = self.layer3(x)
    x = self.relu(x)
    x = self.layer4(x)
    x = self.relu(x)
    x = self.layer5(x)
    x = self.relu(x)
    x = self.layer6(x)
    return x