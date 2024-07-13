import numpy 
import pickle
import pandas as pd
import os
import time
import math
import itertools
import sqlalchemy
from sqlalchemy import create_engine,text
import numpy as np
import tqdm
from torch.utils.data import Dataset,DataLoader,Subset
import torch_geometric
from torch_geometric.data import Data,Batch
import torch
import sklearn
from sklearn.preprocessing import StandardScaler

#need to cd inot preprocessing to run main.py
def query_data():
    engine = create_engine("sqlite+pysqlite:///deephoopers-mod.db",echo=True,future=True)
    with engine.connect() as conn:
        data = conn.execute(text('SELECT Event_ID,Moment_Time,Ball_X,Ball_Y,Ball_DXDT,Ball_DYDT,Player_H_0_X,Player_H_1_X,Player_H_2_X,Player_H_3_X,Player_H_4_X,Player_V_0_X,Player_V_1_X,Player_V_2_X,Player_V_3_X,Player_V_4_X, Player_H_0_Y,Player_H_1_Y,Player_H_2_Y,Player_H_3_Y,Player_H_4_Y,Player_V_0_Y,Player_V_1_Y,Player_V_2_Y,Player_V_3_Y,Player_V_4_Y ,Player_H_0_DXDT,Player_H_1_DXDT,Player_H_2_DXDT,Player_H_3_DXDT,Player_H_4_DXDT,Player_V_0_DXDT,Player_V_1_DXDT,Player_V_2_DXDT,Player_V_3_DXDT,Player_V_4_DXDT, Player_H_0_DYDT,Player_H_1_DYDT,Player_H_2_DYDT,Player_H_3_DYDT,Player_H_4_DYDT,Player_V_0_DYDT,Player_V_1_DYDT,Player_V_2_DYDT,Player_V_3_DYDT,Player_V_4_DYDT FROM TrackingDataTable'))
        start = time.time()
        data = [list(t) for t in data]
        t_data = np.array(data,dtype=float)
        engine.dispose()
        return t_data

class TrackingDataDataset(Dataset):
    def __init__(self,size=None,scale=True,freq = 25,velocity=True,graph=False,data =None, scaler=None):
        self.dataset_len = len(data)
        self.scaler = scaler
        self.data = data
        self.freq = freq
        print(len(set(self.data[:,0])))
        self.scale = scale
        self.velocity = velocity
        self.graph = graph
        self.windowed = None
        self.graph_data = None
        self.edge_index_list = None
        if size == None:
            self.seq_len = 10
            self.target_len = 10
            self.pred_len = 5
        else:
            self.seq_len = size[0]
            self.target_len = size[1]
            self.pred_len = size[2]
        self.__read_data__()

    def construct_edges(self,row):
        edge_index = [[],[]]
        for i in range(int(len(row)/2.0)):
            for j in range(int(len(row)/2.0)):
                if i == j:
                    continue
                else:
                    #if math.sqrt(((row[j][0]-row[i][0])*100.0)**2 + ((row[j][1]-row[i][1])*50.0)**2)<5.0:
                    edge_index[0].append(i)
                    edge_index[1].append(j)
        return edge_index


    def __read_data__(self):
        '''
        data split need to be split by games or by events, rn 
        '''
        #self.data = self.data[index]
        mask = np.isnan(self.data ) | (self.data  == None)
        self.data = self.data[~mask.any(axis=1)]
        self.data = self.data[::int((25/self.freq))]
        if self.scale:
            # self.data[:,list(range(2,46))]=self.scaler.fit_transform(self.data[:,list(range(2,46))])

            self.data[:, [2] + [4] +list(range(6, 16)) + list(range(26, 36))] = self.data[:, [2] + [4] +list(range(6, 16)) + list(range(26, 36))] / 100.
            self.data[:, [3] + [5] + list(range(16,26)) + list(range(36, 46))] = self.data[:, [3] + [5] + list(range(16,26)) + list(range(36, 46))] / 50.

        self.data_x = self.data[:,[4]+[5]+list(range(26,46))]*1000 if self.velocity else self.data[:,[6]+[7]+[16]+[17]]
        self.data_y = self.data[:,[4]+[5]+list(range(26,46))]*1000 if self.velocity else self.data[:,[6]+[7]+[16]+[17]]
        x_coord = self.data_x[:,list(range(0,2))]
        y_coord = self.data_y[:,list(range(2,4))]
        self.graph_data = np.stack((x_coord,y_coord),axis=-1)

        edge_index = []
        for i in range(len(self.graph_data)):
            e_i = self.construct_edges(self.graph_data[i])
            edge_index.append(e_i)
        self.edge_index_list = edge_index
        print("Transformed data shape: ",self.graph_data.shape)
        print("Edge_index: ",len(edge_index[0]))




    #         [              seq_len           ]     
    #                          [  target_len   ][   pred_len   ]
    #------------------------------------------------------------------
    #         |                |                |               |
    #        seq_start     target_start      seq_end        target_end
     
     #Regular getter
    def __getitem__(self,index):
        seq_begin = index
        seq_end = index + self.seq_len
        target_start = seq_end - self.target_len
        target_end = seq_end + self.pred_len
        if self.graph:
            graph_data_list = []
            for i in range(seq_begin,seq_end):
                d = Data(x = torch.tensor(self.graph_data[i]),edge_index=torch.tensor(self.edge_index_list[i]),y=torch.tensor(self.data_y[i-seq_begin+target_start]))
                #print(type(d))
                graph_data_list.append(d)
            batch = Batch.from_data_list(graph_data_list)
            return batch
        else:
            seq_x = self.data_x[seq_begin:seq_end]
            seq_y = self.data_y[target_start:target_end]
        return seq_x,seq_y
    
    def __len__(self):
        return len(self.data)

    # def get_window_indices(self):
    #     indices = []
    #     index = 0
    #     train_index = 0
    #     train_index_found = False
    #     val_test_index = 0
    #     val_test_index_found = False
    #     print(self.data.shape[-1])
    #     for i in range(len(self.data)-self.pred_len-self.seq_len):
    #         if self.data[i,0] != self.data[i+self.pred_len+self.seq_len-1,0]: #if you are transitioning from one event to another
    #             if not train_index_found and i >= int((len(self.data)-self.pred_len-self.seq_len)*0.6):
    #                 train_index = i
    #                 indices.append(i)
    #                 train_index_found = True
    #             elif not val_test_index_found and i >= int((len(self.data)-self.pred_len-self.seq_len)*0.8):
    #                 val_test_index_found = True
    #                 indices.append(i)
    #                 val_test_index = i
    #             continue
    #         else:
    #             indices.append(i)
    #     return train_index,val_test_index,indices
        
    def get_test_game(self,val_test_index):
        min_event_id = self.data[val_test_index,0]
        max_event_id = self.data[-1,0]
        print("Min event id: ",min_event_id)
        print("Max event id: ",max_event_id)
        random_event = np.random.randint(min_event_id,max_event_id)
        mask = self.data[:,0] == random_event
        test_data = self.data[mask]
        return test_data


#THIS CODE IS JUST FOR TESTING OUT THE DATASET AND DATALOADER, SO FAR IT WORKS:)
def data_provider(size = (10,7,3),scale=True,velocity=True,freq = 25 ,graph=False, scaler=None):
    data = query_data()
    dataset = TrackingDataDataset(size,scale,freq,velocity,graph,data,scaler)
    # train_index,val_test_index,indices = dataset.get_window_indices()
    # #indices = indices[0:int(len(indices)*0.6)]
    train_index = int(len(dataset)*0.6)
    val_test_index = int(len(dataset)*0.8)
    train_indices = list(range(0,train_index))
    val_indices = list(range(train_index,val_test_index))
    test_indices = list(range(val_test_index,len(dataset)-size[0]-size[2]+1))

    train_dataset = Subset(dataset,train_indices)
    val_dataset = Subset(dataset,val_indices)
    test_dataset = Subset(dataset,test_indices)

    if graph:
        train_dataloader = torch_geometric.loader.DataLoader(train_dataset,batch_size=32,shuffle=False,drop_last=True)
        val_dataloader = torch_geometric.loader.DataLoader(val_dataset,batch_size=32,shuffle=False,drop_last=True)
        test_dataloader = torch_geometric.loader.DataLoader(test_dataset,batch_size=32,shuffle=False,drop_last=True)
    else:
        train_dataloader = DataLoader(train_dataset,batch_size = 32,shuffle=None,num_workers=0,drop_last = True)
        val_dataloader = DataLoader(val_dataset,batch_size = 32,shuffle=None,num_workers=0,drop_last = True)
        test_dataloader = DataLoader(test_dataset,batch_size = 32,shuffle=None,num_workers=0,drop_last = True)
    test_data = dataset.get_test_game(val_test_index)

    # What our data loaders for the graph model look like: 
    # 1 batch has 32 of these --> DataBatch(x=[550, 2], edge_index=[2, 286], y=[1100], batch=[550], ptr=[51])
    #                             This DataBatch object has 50 graphs stacked together
    #                             batch is a vector indicating which node belongs to which graph
    #                             ptr tells us the cummulative number of nodes in the batch up to each graph
    # Each sample is a DataBatch


    return train_dataloader,val_dataloader,test_dataloader,test_data

