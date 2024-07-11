import torch
import numpy as np 
import torch.nn as nn
import math
import torch.autograd as Variable

class LSTM(nn.Module):
    def __init__(self,input_size,hidden_size,fc_units,output_size,num_layers,device):
        super().__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.device = device
        self.lstm = nn.LSTM(input_size,hidden_size,num_layers,batch_first =True,device=device) 
        self.linear = [nn.Linear(fc_units[i],fc_units[i+1],bias=True,device=device) for i in range(len(fc_units)-1) ]
        self.relu = nn.ReLU()
    def forward(self,x):
        '''
        '''
        h0 = torch.zeros(self.num_layers,x.size(0),self.hidden_size).to(self.device)
        c0 = torch.zeros(self.num_layers,x.size(0),self.hidden_size).to(self.device)
        x,(h0,c0) = self.lstm(x,(h0,c0))
        for i,l in enumerate(self.linear):
            if i==0:
                out = l(x)
            else:
                out = self.relu(l(out))
        return out




class BiLSTM(nn.Module):
    def __init__(self,input_size,hidden_size,fc_units,output_size,num_layers,device):
        super().__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.device = device
        self.bilstm = nn.LSTM(input_size,hidden_size,num_layers,batch_first =True,bidirectional=True,device=device)
        self.linear = [nn.Linear(fc_units[i],fc_units[i+1],bias=True,device=device) for i in range(len(fc_units)-1) ]
        self.relu = nn.ReLU()
    def forward(self,x):
        '''
        '''
        h0 = torch.zeros(2*self.num_layers,x.size(0),self.hidden_size).to(self.device)
        c0 = torch.zeros(2*self.num_layers,x.size(0),self.hidden_size).to(self.device)
        x,(h0,c0) = self.bilstm(x,(h0,c0))
        for i,l in enumerate(self.linear):
            if i==0:
                out = l(x)
            else:
                out = self.relu(l(out))
        return out


class GRUEncoder(nn.Module):
    def __init__(self,num_layers,hidden_size,input_size,device):
        '''
        '''
        super().__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.input_size = input_size
        self.gru = nn.GRU(input_size,hidden_size,num_layers,batch_first = True,device=device)
        self.device = device
    def forward(self,x):
        '''
        '''
        h0 = torch.zeros(self.num_layers,x.size(0),self.hidden_size).to(self.device)
        out,hn = self.gru(x,h0)
        return out,hn


class GRUDecoder(nn.Module):
    def __init__(self,num_layers,hidden_size,fc_units,input_size,output_size,device):
        '''
        '''
        super().__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.gru = nn.GRU(hidden_size,hidden_size,num_layers,batch_first = True,device=device)
        self.linear = [nn.Linear(fc_units[i],fc_units[i+1],device=device) for i in range(len(fc_units)-1)]
        self.relu = nn.ReLU()
        self.device = device
    def forward(self,x,hn):
        ''' 
        '''

        out, _ = self.gru(x,hn)
        for i,l in enumerate(self.linear):
            if i==0:
                out = self.relu(l(out))
            else:
                out = self.relu(l(out))
        return out
        

class GRUEncoderDecoder(nn.Module):
    def __init__(self,num_layers,input_size,hidden_size,fc_units,output_size,device):
        ''' 
        '''
        super().__init__()
        self.encoder = GRUEncoder(num_layers, hidden_size, input_size,device)
        self.decoder = GRUDecoder(num_layers, hidden_size, fc_units, input_size,output_size,device)
        
    def forward(self,x):
        encoder_output,hn = self.encoder(x)
        decoder_output = self.decoder(encoder_output,hn)
        return decoder_output

# class TCN(nn.Module):
#     def __init__(self,):
#         '''
#         '''
#         self.conv1d
#     def forward(self,x):
#         '''
#         '''


# class TCNBlock(nn.Module):
#     def __init__(self):


# output_lstm = lstm(input_tensor)
# output_bilstm = bilstm(input_tensor)
# output_grued = grued(input_tensor)

# print(output_lstm.shape)
# print(output_bilstm.shape)
# print(output_grued.shape)