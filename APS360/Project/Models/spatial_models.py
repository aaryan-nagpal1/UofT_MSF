import torch
import numpy as np 
import torch.nn as nn
from torch_geometric.nn import aggr
from torch_geometric.nn.conv import GATConv,GCNConv
from models.discrete_seq_models import GRUEncoderDecoder, LSTM, BiLSTM



class GNN(nn.Module):
    def __init__(self, batch_size=32,seq_len = 50,num_layers=5, input_heads=4, hidden_size=[64,128], activation = "elu",aggr_type = "mean",gnn="gat",device="cpu"):
      super().__init__()
      self.input_heads = input_heads
      self.hidden_size = hidden_size
      self.batch_size = batch_size
      self.device = device
      self.seq_len = seq_len
      if gnn == "gat":
        self.conv1 = GATConv(2, hidden_size[0], heads=input_heads,concat=False, dropout=0.5,device=self.device).to("cuda")
        self.conv2 = GATConv(hidden_size[0], hidden_size[1], heads=input_heads,concat=False, dropout=0.5,device=self.device).to("cuda")
      elif gnn == "gcn":
        self.conv1 = GCNConv(2, hidden_size[0],improved=True,cached=True,device=self.device).to("cuda")
        self.conv2 = GCNConv(hidden_size[0], hidden_size[1],improved=True,cached=True,device=self.device).to("cuda")
      if activation == "elu":
        self.activation = nn.ELU(alpha=1.0)
      elif activation == "relu":
        self.activation = nn.ReLU()
      elif activation == "leakyrelu":
        self.activaiton = nn.LeakyReLU()
      self.dropout = nn.Dropout(p=0.5)
      if aggr_type == "mean":
        self.aggr = aggr.MeanAggregation()
      elif aggr_type == "max":
        self.aggr = aggr.MedianAggregation()


    def forward(self, data):
      data=data.to(self.device)
      x = data.x.float().to(self.device)
      edge_index = data.edge_index.type(torch.int32)
      x = self.conv1(x, edge_index)
      x = self.dropout(x)
      x = self.activation(x)
      x = self.conv2(x, edge_index)
      x = self.dropout(x)
      x = self.activation(x)
      x = self.aggr(x,index=data.batch)
      x = torch.reshape(x,(self.batch_size,self.seq_len,self.hidden_size[-1]))
      return x

class GNNLSTM(nn.Module):
    def __init__(self,batch_size=32,seq_len = 50, lstm_layers = 3,gat_layers=5, input_heads=4,output_size=22, hidden_size=[64,128],fc_units = [64,32,22], activation = "elu",device="cuda",aggr = "mean",gnn="gat"):
        super().__init__()
        self.graph_module = GNN(batch_size=batch_size,seq_len = seq_len,num_layers=gat_layers, input_heads=input_heads, hidden_size=hidden_size, activation = activation,aggr_type = aggr,gnn=gnn,device=device)
        self.sequence_module = LSTM(input_size=hidden_size[-1],hidden_size=fc_units[0],fc_units=fc_units,output_size=output_size,num_layers=lstm_layers,device=device)
    def forward(self,x):
        x = self.graph_module(x)
        x = self.sequence_module(x)
        return x


class GNNBiLSTM(nn.Module):
    def __init__(self,batch_size=32,seq_len = 50, bilstm_layers = 3,gat_layers=5, input_heads=4,output_size=22, hidden_size=[64,128],fc_units =  [512,64,22], activation = "elu",device="cpu",aggr = "mean",gnn="gat"):
        super().__init__()
        self.graph_module = GNN(batch_size=batch_size,seq_len = seq_len,num_layers=gat_layers, input_heads=input_heads, hidden_size=hidden_size, activation = activation,aggr_type = aggr,gnn=gnn,device=device)
        self.sequence_module = BiLSTM(input_size=hidden_size[-1],hidden_size=hidden_size[-1]*2,fc_units=fc_units,output_size=fc_units[-1],num_layers=bilstm_layers,device=device)
    def forward(self,x):
        x = self.graph_module(x)
        x = self.sequence_module(x)
        return x


class GNNGRUED(nn.Module):
    def __init__(self,batch_size=32,seq_len = 50, gru_layers = 3,gat_layers=5, input_heads=4,output_size=22, hidden_size=[64,128],fc_units = [64,32,22], activation = "elu",device="cpu",aggr = "mean",gnn="gat"):
        super().__init__()
        self.graph_module = GNN(batch_size=batch_size,seq_len = seq_len,num_layers=gat_layers, input_heads=input_heads, hidden_size=hidden_size, activation = activation,aggr_type = aggr,gnn=gnn,device=device)
        self.sequence_module = GRUEncoderDecoder(num_layers=gru_layers, input_size=hidden_size[-1], hidden_size=fc_units[0], fc_units=fc_units, output_size=fc_units[-1],device=device)
    def forward(self,x):
        x = self.graph_module(x)
        x = self.sequence_module(x)
        return x



# if __name__ == "__main__":
    





