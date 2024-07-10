import torch
import matplotlib.pyplt as plt
import numpy as np 
import torch.nn as nn
import math
import torch.autograd as Variable

#ODE solver

def euler_solver(z0,t0,t1,f):
    '''
    Simplest Euler ODE initial solver
    '''
    h_max = 0.05
    n_steps = math.ceil((abs(t1-t0)/hmax).max().item())
    h = (t1-t0)/n_steps
    t = t0
    for i in range(n_steps):
        z = z + h*f(z,t)
        t = t + h
    return z


class ODEF(nn.Module):
    def forward_with_grad():