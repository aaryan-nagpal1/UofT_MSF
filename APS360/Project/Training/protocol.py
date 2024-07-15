import torch
import numpy as np 
import torch.nn as nn
import math
from IPython import display
from preprocessing.data_factory import data_provider
from models.discrete_seq_models import GRUEncoderDecoder, LSTM, BiLSTM
from models.spatial_models import GNNLSTM, GNNBiLSTM,GNNGRUED
from models.baseline import MLP
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation

class Protocol():
    def __init__(self,model,epoch,learning_rate,batch_size,num_features,seq_len,pred_len,target_len,scale,velocity,freq,graph,device,scaler):
        super(Protocol,self).__init__()
        #model
        self.scaler = scaler
        self.model_name = ""
        if isinstance(model, GRUEncoderDecoder):
            self.model_name = 'GRUED'
        elif isinstance(model, LSTM):
            self.model_name = 'LSTM'
        elif isinstance(model, BiLSTM):
            self.model_name = 'BiLSTM'
        elif isinstance(model,MLP):
            self.model_name = 'MLP'
        elif isinstance(model, GNNLSTM):
            self.model_name = "GNNLSTM"
        elif isinstance(model, GNNBiLSTM):
            self.model_name = "GNNBiLSTM"
        elif isinstance(model, GNNGRUED):
            self.model_name = "GNNGRUED"

        self.model_size = 0
        self.device = device
        #hyper param
        self.epoch = epoch
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        #data parameters
        self.num_features = num_features
        self.seq_len = seq_len
        self.target_len = target_len
        self.pred_len = pred_len
        self.scale = scale
        self.velocity = velocity
        self.freq = freq
        self.graph = graph
        #loaders
        self.train_loader = None
        self.val_loader = None
        self.test_loader = None
        self.test_data = None

        #training metrics
        self.training_loss = []
        self.val_loss = []
        self.avg_train_loss = 0.0
        self.avg_val_loss = 0.0
        self.avg_test_loss = 0.0

        self.best_val_loss = 100
        self.best_epoch = 0
        self.best_path = ""

        #other metrics 
        self.training_time = 0.0
        self.avg_inference_time = 0.0
        self.avg_time_per_epoch = 0.0

        #loss fn & optimizer
        self.loss_fn = nn.MSELoss()
        self.optimizer = None

        self.court_path = "C:/Users/DIC/Desktop/DEEP/DeepHoopers/assets/nba_court_T.png"

    def load_data(self):
        self.train_loader,self.val_loader,self.test_loader,self.test_data = data_provider(size = (self.seq_len,self.target_len,self.pred_len),scale=self.scale,velocity=self.velocity,graph=self.graph,freq = self.freq, scaler=self.scaler)
        print("\n")
        print("###############DATA LOADING SUCCESS###############")
        print("Data paremters: ")
        print("Seq len: ",self.seq_len)
        print("Target len: ",self.target_len)
        print("Pred len: ",self.pred_len)
        print("Normalization: ",self.scale)
        print("Using velocity as features: ",self.velocity)
        print("Sampling Frequency: ",self.freq)
        print("\n")

    def train(self, model):
        self.optimizer = torch.optim.Adam(model.parameters(),lr=self.learning_rate)
        print("###############STARTING TRAINING###############")
        model.train()
        model.to(self.device)
        train_start = time.time()
        if not self.graph:
            for epoch in range(self.epoch):
                epoch_start = time.time()
                self.avg_train_loss = 0.0
                self.avg_val_loss = 0.0
                for batch_x,batch_y in tqdm(self.train_loader):
                    batch_x, batch_y = batch_x.float().to(self.device), batch_y.float().to(self.device)
                    inf_start = time.time()
                    output = model(batch_x).to(self.device)
                    inf_end = time.time()
                    self.avg_inference_time += inf_end-inf_start
                    loss = self.loss_fn(output,batch_y)
                    self.avg_train_loss +=loss.item()
                    loss.backward()
                    self.optimizer.step()
                    self.optimizer.zero_grad()
                self.avg_train_loss /= len(self.train_loader)
                self.training_loss.append(self.avg_train_loss )
                self.avg_inference_time /= len(self.train_loader)
                with torch.no_grad():
                    for batch_x,batch_y in tqdm(self.val_loader):
                        batch_x, batch_y = batch_x.float().to(self.device), batch_y.float().to(self.device)
                        output = model(batch_x).to(self.device)
                        loss = self.loss_fn(output,batch_y)
                        self.avg_val_loss += loss.item()
                    self.avg_val_loss /= len(self.val_loader)
                    self.val_loss.append(self.avg_val_loss) 
                    if self.avg_val_loss < self.best_val_loss:
                        self.best_val_loss = self.avg_val_loss
                        self.best_epoch = epoch
                        self.best_path = f'../checkpoints/{self.model_name}_bs{self.batch_size}_lr{self.learning_rate}_win{self.seq_len}-{self.target_len}-{self.pred_len}_v{self.velocity}_sc{self.scale}_ep{epoch}.pth'
                epoch_end = time.time()
                epoch_time = epoch_end-epoch_start
                self.save(epoch,model,self.avg_val_loss)
                self.avg_time_per_epoch += epoch_time/self.epoch
                print(f'===Epoch: {epoch} | Training Loss: {self.avg_train_loss} | Validation Loss: {self.avg_val_loss} | Avg inference time: {self.avg_inference_time} | Time per epoch: {epoch_time}')
        else:
            for epoch in range(self.epoch):
                epoch_start = time.time()
                self.avg_train_loss = 0.0
                self.avg_val_loss = 0.0
                for batch in tqdm(self.train_loader):
                    batch_y = torch.reshape(batch.y.float(),(self.batch_size,self.seq_len,self.num_features)).to(self.device)
                    inf_start = time.time()
                    output = model(batch).to(self.device)
                    inf_end = time.time()
                    self.avg_inference_time += inf_end-inf_start
                    loss = self.loss_fn(output,batch_y)
                    self.avg_train_loss +=loss.item()
                    loss.backward()
                    self.optimizer.step()
                    self.optimizer.zero_grad()
                self.avg_train_loss /= len(self.train_loader)
                self.training_loss.append(self.avg_train_loss )
                self.avg_inference_time /= len(self.train_loader)
                with torch.no_grad():
                    for batch in tqdm(self.val_loader):
                        batch_y = torch.reshape(batch.y.float(),(self.batch_size,self.seq_len,self.num_features)).to(self.device)
                        output = model(batch).to(self.device)
                        loss = self.loss_fn(output,batch_y)
                        self.avg_val_loss += loss.item()
                    self.avg_val_loss /= len(self.val_loader)
                    self.val_loss.append(self.avg_val_loss) 
                    if self.avg_val_loss < self.best_val_loss:
                        self.best_val_loss = self.avg_val_loss
                        self.best_epoch = epoch
                        self.best_path = f'../checkpoints/{self.model_name}_bs{self.batch_size}_lr{self.learning_rate}_win{self.seq_len}-{self.target_len}-{self.pred_len}_v{self.velocity}_sc{self.scale}_ep{epoch}.pth'
                epoch_end = time.time()
                epoch_time = epoch_end-epoch_start
                self.save(epoch,model,self.avg_val_loss)
                self.avg_time_per_epoch += epoch_time/self.epoch
                print(f'===Epoch: {epoch} | Training Loss: {self.avg_train_loss} | Validation Loss: {self.avg_val_loss} | Avg inference time: {self.avg_inference_time} | Time per epoch: {epoch_time}')
                

        train_end = time.time()
        self.training_time = train_end-train_start
        print("###############TRAINING COMPLETE###############")
        print("Training metrics: ")
        print("Final training loss: ",self.avg_train_loss)
        print("Final validation loss: ",self.avg_val_loss)
        print("Best validation loss: ",self.best_val_loss)
        print("Best epoch: ",self.best_epoch)
        print("Avg training inference time: ",self.avg_inference_time)
        print("Total training time: ",self.training_time)
        print(f"Model size: {self.find_model_size(model)} MB")
        self.plot_training_curve()
        return

    def find_model_size(self,model):
        param_size = 0
        for param in model.parameters():
            param_size += param.nelement() * param.element_size()
        buffer_size = 0
        for buffer in model.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()

        size_all_mb = (param_size + buffer_size) / 1024**2
        return size_all_mb

    def eval(self, model):
        model.eval()
        if not self.graph:
            with torch.no_grad():
                for batch_x,batch_y in self.test_loader:
                    output = model(batch_x.float().to(self.device))
                    loss = self.loss_fn(output,batch_y.float().to(self.device))
                    self.avg_test_loss+=loss.item()
                self.avg_test_loss /= len(self.test_loader)
            print("Test Loss: ",self.avg_test_loss)
        else:
            with torch.no_grad():
                for batch in self.test_loader:
                    batch_y = torch.reshape(batch.y.float(),(self.batch_size,self.seq_len,self.num_features))
                    output = model(batch)
                    loss = self.loss_fn(output,batch_y.float().to(self.device))
                    self.avg_test_loss+=loss.item()
                self.avg_test_loss /= len(self.test_loader)
            print("Test Loss: ",self.avg_test_loss)
        return 

    def save(self,epoch,model,loss):
        torch.save({
            'epoch':epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'loss': loss,
            }, f'../checkpoints/{self.model_name}_bs{self.batch_size}_lr{self.learning_rate}_win{self.seq_len}-{self.target_len}-{self.pred_len}_v{self.velocity}_sc{self.scale}_ep{epoch}.pth')
        return
    def plot_training_curve(self):
        n = len(self.training_loss) # number of epochs
        fig = plt.figure()
        plt.title("Train vs Validation Loss")
        plt.plot(range(1,n+1), self.training_loss, label="Train")
        plt.plot(range(1,n+1), self.val_loss, label="Validation")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend(loc='best')
        plt.savefig(f"../training_curves/{self.model_name}_bs{self.batch_size}_lr{self.learning_rate}_win{self.seq_len}-{self.target_len}-{self.pred_len}_v{self.velocity}_sc{self.scale}.png")

    def generate_predictions(self,model):
        #print(self.test_data.shape)
        pred_data = self.test_data[:,[2]+[3]+[6]+[7]+[16]+[17]]
        prediction = self.test_data[0:self.seq_len,[2]+[3]+[6]+[7]+[16]+[17]]
        # print("Largest values : ")
        # print(np.max(self.test_data[:,2]))
        # print(np.max(self.test_data[:,3]))
        # print(np.max(self.test_data[:,6]))
        # print(np.max(self.test_data[:,7]))
        # pred_data = torch.unsqueeze(torch.tensor(pred_data),dim=0)
        for i in range(len(self.test_data) - self.seq_len):
            #print("RUNNING PRED DATA: ",pred_data[i:i+self.seq_len:,:].shape)
            input_tensor = torch.unsqueeze(torch.tensor(pred_data[i:i+self.seq_len,:]),dim=0).float().to(self.device)
            # input_tensor = input_tensor[:,:,[2]+[3]+list(range(6, 26))]
            with torch.no_grad():
                #print("INPUT TENSOR: ")
                #print(input_tensor.shape)
                output = model(input_tensor)
                # print("OUTPUT: ")
                # print(output)
                # print(output.shape)
            # if i==0:
                output = np.squeeze(output[:,self.target_len:,:].cpu().numpy(),axis=0)
            # else:
            #     output = np.squeeze(output[:,-1,:].cpu().numpy(),axis=0)


            #print("OUTPUT SHAPE: ",output.shape)
            # last_output = output[:, -1,:].cpu().numpy()
            # print("LAST OUTPUT: ",last_output.shape)
            #predictions.append(last_output)
            prediction = np.vstack([prediction, output])
        #predictions = np.vstack(predictions)
        return prediction

    def plot_test_data(self,model):
        #model = model.load_state_dict(torch.load(ckpt_path))
        self.pred_data = self.generate_predictions(model)
        print("Legnth of test data: ",len(self.test_data))
        fig = plt.figure()
        ax = plt.gca()
        img = mpimg.imread(self.court_path)  # read image. I got this image from gmf05's github.
        plt.imshow(img, extent=[0,94,0,50], zorder=0)  # show the image.
        plt.xlim([0,94])
        plt.ylim([0,50])
        plt.tight_layout(pad=0, w_pad=0.5, h_pad=0)

        home_color = '#E13A3E'
        away_color = '#008348'

        pred_home_color = '#F09C9E'
        pred_away_color = '#7FC1A3'

        ball_color = '#E65C00'
        pred_ball_color = '#FFA500'

       
        rescale_x = 100.0
        rescale_y = 50.0

        length = int(len(self.test_data)*0.07)   
        ball_x = self.test_data[:,2]*rescale_x #4,5 ball x,y 6-
        ball_y = self.test_data[:,3]*rescale_y

        pred_ball_x = self.pred_data[:,0]*rescale_x #4,5 ball x,y 6-
        pred_ball_y = self.pred_data[:,1]*rescale_y

        player_x = self.test_data[:,[6]+[7]]*rescale_x
        player_y = self.test_data[:,[16]+[17]]*rescale_y

        # print("PRED BALL X MAX: ")
        # print(np.max(pred_ball_x))
        # print("PRED BALL Y MAX: ")
        # print(np.max(pred_ball_y))

        pred_player_x = self.pred_data[:,[2]+[3]]*rescale_x
        pred_player_y = self.pred_data[:,[4]+[5]]*rescale_y

        # print("PRED PLAYER X MAX: ")
        # print(np.max(pred_player_x[:,0]))
        # print("PRED PLAYER Y MAX: ")
        # print(np.max(pred_player_y[:,1]))
        # print("PRED PLAYER X MIN: ")
        # print(np.mean(pred_player_x[:,0]))
        # print("PRED PLAYER Y MIN: ")
        # print(np.mean(pred_player_y[:,1]))

        # -------- PLOT TRAJECTORIES VAR ---------
        p_player_h_1, = ax.plot([], [], pred_home_color)
        # p_player_h_2, = ax.plot([], [], pred_home_color)
        # p_player_h_3, = ax.plot([], [], pred_home_color)
        # p_player_h_4, = ax.plot([], [], pred_home_color)
        # p_player_h_5, = ax.plot([], [], pred_home_color)

        p_player_a_1, = ax.plot([], [], pred_away_color)
        # p_player_a_2, = ax.plot([], [], pred_away_color)
        # p_player_a_3, = ax.plot([], [], pred_away_color)
        # p_player_a_4, = ax.plot([], [], pred_away_color)
        # p_player_a_5, = ax.plot([], [], pred_away_color)

        player_h_1, = ax.plot([], [], home_color)
        # player_h_2, = ax.plot([], [], home_color)
        # player_h_3, = ax.plot([], [], home_color)
        # player_h_4, = ax.plot([], [], home_color)
        # player_h_5, = ax.plot([], [], home_color)

        player_a_1, = ax.plot([], [], away_color)
        # player_a_2, = ax.plot([], [], away_color)
        # player_a_3, = ax.plot([], [], away_color)
        # player_a_4, = ax.plot([], [], away_color)
        # player_a_5, = ax.plot([], [], away_color)

        # ------- PLOT POSITIONS VAR ---------
        #player_h_1 = ax.scatter([], [], home_color)
        # player_h_2 = ax.scatter([], [], home_color)
        # player_h_3 = ax.scatter([], [], home_color)
        # player_h_4 = ax.scatter([], [], home_color)
        # player_h_5 = ax.scatter([], [], home_color)

        #player_a_1 = ax.scatter([], [], away_color)
        # player_a_2 = ax.scatter([], [], away_color)
        # player_a_3 = ax.scatter([], [], away_color)
        # player_a_4 = ax.scatter([], [], away_color)
        # player_a_5 = ax.scatter([], [], away_color)

        #p_player_h_1 = ax.scatter([], [], pred_home_color)
        # p_player_h_2 = ax.scatter([], [], pred_home_color)
        # p_player_h_3 = ax.scatter([], [], pred_home_color)
        # p_player_h_4 = ax.scatter([], [], pred_home_color)
        # p_player_h_5 = ax.scatter([], [], pred_home_color)

        #p_player_a_1 = ax.scatter([], [], pred_away_color)
        # p_player_a_2 = ax.scatter([], [], pred_away_color)
        # p_player_a_3 = ax.scatter([], [], pred_away_color)
        # p_player_a_4 = ax.scatter([], [], pred_away_color)
        # p_player_a_5 = ax.scatter([], [], pred_away_color)

        def update_traj(frame):

             p_player_h_1.set_data(pred_player_x[:frame + 1,0], pred_player_y[:frame + 1,0])
        #     p_player_h_2.set_data(pred_player_x[:frame + 1,1], pred_player_y[:frame + 1,1])
        #     p_player_h_3.set_data(pred_player_x[:frame + 1,2], pred_player_y[:frame + 1,2])
        #     p_player_h_4.set_data(pred_player_x[:frame + 1,3], pred_player_y[:frame + 1,3])
        #     p_player_h_5.set_data(pred_player_x[:frame + 1,4], pred_player_y[:frame + 1,4])

             p_player_a_1.set_data(pred_player_x[:frame + 1,1], pred_player_y[:frame + 1,1])
        #     p_player_a_2.set_data(pred_player_x[:frame + 1,6], pred_player_y[:frame + 1,6])
        #     p_player_a_3.set_data(pred_player_x[:frame + 1,7], pred_player_y[:frame + 1,7])
        #     p_player_a_4.set_data(pred_player_x[:frame + 1,8], pred_player_y[:frame + 1,8])
        #     p_player_a_5.set_data(pred_player_x[:frame + 1,9], pred_player_y[:frame + 1,9])
    
             player_h_1.set_data(player_x[:frame + 1,0], player_y[:frame + 1,0])
        #     player_h_2.set_data(player_x[:frame + 1,1], player_y[:frame + 1,1])
        #     player_h_3.set_data(player_x[:frame + 1,2], player_y[:frame + 1,2])
        #     player_h_4.set_data(player_x[:frame + 1,3], player_y[:frame + 1,3])
        #     player_h_5.set_data(player_x[:frame + 1,4], player_y[:frame + 1,4])

             player_a_1.set_data(player_x[:frame + 1,1], player_y[:frame + 1,1])
        #     player_a_2.set_data(player_x[:frame + 1,6], player_y[:frame + 1,6])
        #     player_a_3.set_data(player_x[:frame + 1,7], player_y[:frame + 1,7])
        #     player_a_4.set_data(player_x[:frame + 1,8], player_y[:frame + 1,8])
        #     player_a_5.set_data(player_x[:frame + 1,9], player_y[:frame + 1,9])

             return p_player_h_1,p_player_a_1,player_h_1,player_a_1
             #return player_h_1, player_h_2, player_h_3,player_h_4,player_h_5,player_a_1,player_a_2,player_a_3,player_a_4,player_a_5,p_player_h_1,p_player_h_2,p_player_h_3,p_player_h_4,p_player_h_5,p_player_a_1,p_player_a_2,p_player_a_3,p_player_a_4,p_player_a_5
        

        # def update_pos(frame):
        #     player_h_1.set_offsets([player_x[frame,0], player_y[frame,0]])
        #     # player_h_2.set_offsets([player_x[frame,1], player_y[frame,1]])
        #     # player_h_3.set_offsets([player_x[frame,2], player_y[frame,2]])
        #     # player_h_4.set_offsets([player_x[frame,3], player_y[frame,3]])
        #     # player_h_5.set_offsets([player_x[frame,4], player_y[frame,4]])

        #     player_a_1.set_offsets([player_x[frame,5], player_y[frame,5]])
        #     # player_a_2.set_offsets([player_x[frame,6], player_y[frame,6]])
        #     # player_a_3.set_offsets([player_x[frame,7], player_y[frame,7]])
        #     # player_a_4.set_offsets([player_x[frame,8], player_y[frame,8]])
        #     # player_a_5.set_offsets([player_x[frame,9], player_y[frame,9]])

        #     p_player_h_1.set_offsets([pred_player_x[frame,0], pred_player_y[frame,0]])
        #     # p_player_h_2.set_offsets([pred_player_x[frame,1], pred_player_y[frame,1]])
        #     # p_player_h_3.set_offsets([pred_player_x[frame,2], pred_player_y[frame,2]])
        #     # p_player_h_4.set_offsets([pred_player_x[frame,3], pred_player_y[frame,3]])
        #     # p_player_h_5.set_offsets([pred_player_x[frame,4], pred_player_y[frame,4]])

        #     p_player_a_1.set_offsets([pred_player_x[frame,5], pred_player_y[frame,5]])
        #     # p_player_a_2.set_offsets([pred_player_x[frame,6], pred_player_y[frame,6]])
        #     # p_player_a_3.set_offsets([pred_player_x[frame,7], pred_player_y[frame,7]])
        #     # p_player_a_4.set_offsets([pred_player_x[frame,8], pred_player_y[frame,8]])
        #     # p_player_a_5.set_offsets([pred_player_x[frame,9], pred_player_y[frame,9]])
        #     #return player_h_1, player_h_2, player_h_3,player_h_4,player_h_5,player_a_1,player_a_2,player_a_3,player_a_4,player_a_5,p_player_h_1,p_player_h_2,p_player_h_3,p_player_h_4,p_player_h_5,p_player_a_1,p_player_a_2,p_player_a_3,p_player_a_4,p_player_a_5
        #     return player_h_1,player_a_1,p_player_h_1,p_player_a_1
        
        
        
        # PLOTS STILL TRAJECTORY 
        # plot_length = int(len(self.test_data)*0.04)
        # plt.plot(ball_x[:plot_length],ball_y[:plot_length],color=ball_color,label=f'Ball')
        # plt.plot(pred_ball_x[:plot_length],pred_ball_y[:plot_length],color=pred_ball_color,label=f'Ball Pred')
        # plt.arrow(ball_x[plot_length-2], ball_y[plot_length-2], ball_x[plot_length-1]-ball_x[plot_length-2], ball_y[plot_length-1]-ball_y[plot_length-2], color=ball_color)
        # plt.arrow(pred_ball_x[plot_length-2], pred_ball_y[plot_length-2], pred_ball_x[plot_length-1]-pred_ball_x[plot_length-2], pred_ball_y[plot_length-1]-pred_ball_y[plot_length-2], color=ball_color)
        # for i in range(10):
        #     if i<5:
        #         plt.plot(player_x[:plot_length,i],player_y[:plot_length,i],color=home_color,label=f'Home Player {i}')
        #         plt.plot(pred_player_x[:plot_length,i],pred_player_y[:plot_length,i],color=pred_home_color,label=f'Pred Home Player {i}')

        #         plt.arrow(player_x[plot_length-2,i], player_y[plot_length-2,i], player_x[plot_length-1,i]-player_x[plot_length-2,i], player_y[plot_length-1,i]-player_y[plot_length-2,i], color=home_color )
        #         plt.arrow(pred_player_x[plot_length-2,i], pred_player_y[plot_length-2,i], pred_player_x[plot_length-1,i]-pred_player_x[plot_length-2,i], pred_player_y[plot_length-1,i]- pred_player_y[plot_length-2,i], color=pred_home_color)
        #     else:
        #         plt.plot(player_x[:plot_length,i],player_y[:plot_length,i],color=away_color,label=f'Away Player {i}')
        #         plt.plot(pred_player_x[:plot_length,i],pred_player_y[:plot_length,i],color=pred_away_color,label=f'Pred Away Player {i}')
        #         plt.arrow(player_x[plot_length-2,i], player_y[plot_length-2,i], player_x[plot_length-1,i]-player_x[plot_length-2,i], player_y[plot_length-1,i]-player_y[plot_length-2,i], color=away_color )
        #         plt.arrow(pred_player_x[plot_length-2,i], pred_player_y[plot_length-2,i], pred_player_x[plot_length-1,i]-pred_player_x[plot_length-2,i], pred_player_y[plot_length-1,i]- pred_player_y[plot_length-2,i], color=pred_away_color)

        ani = FuncAnimation(fig, update_traj, frames=length, interval=200)
        video = ani.to_html5_video() 


        html = display.HTML(video) 
        #ani = FuncAnimation(fig, update_pos, frames=length, interval=200)
        plt.show()


        # PLOTS ONE FRAME
        # for t in range():
        #     pred_ball_circ = plt.Circle((pred_ball_x[t], pred_ball_y[t]), 0, color=[1, 0.4, 0])  # create circle object for bal
        #     ball_circ = plt.Circle((ball_x[t], ball_y[t]), 0, color=[1, 0.4, 0])  # create circle object for bal
        #     ax.add_artist(pred_ball_circ)
        #     ax.add_artist(ball_circ)
        #     l = [1] #[0,1,2,3,4,5,6,7,8,9]
        #     for a in l:
        #         if a<5: #home x & y
        #             color = home_color
        #             pred_color = pred_home_color
        #         else:
        #             color = away_color
        #             pred_color = pred_away_color
        #         p_x = player_x[t,a]
        #         p_y =player_y[t,a]
        #         pred_p_x = pred_player_x[t,a]
        #         pred_p_y =pred_player_y[t,a]

        #         # player_circ = plt.Circle((p_x,p_y), 0.3,
        #         #     facecolor=color,edgecolor='k')
        #         pred_player_circ = plt.Circle((pred_p_x,pred_p_y), 0.3,
        #             facecolor=pred_color,edgecolor='k')
        #         #ax.add_artist(player_circ)
        #         ax.add_artist(pred_player_circ)
        #         plt.show()