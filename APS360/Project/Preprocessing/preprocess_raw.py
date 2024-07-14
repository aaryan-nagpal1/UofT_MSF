
import numpy 
import pickle
import pandas as pd
import os
import time
import sqlalchemy
from sqlalchemy import create_engine,text
print(sqlalchemy.__version__)
# game_name = '0021500009.pkl'

# game = pd.read_pickle('/Users/ambroseling/Desktop/raptors/data/'+game_name)
# print(game.keys())
# print(game['events'][0].keys())
# print(game['events'][0]['moments'][0].keys())

data_path = '/Users/ambroseling/Desktop/DeepHoopers/Raptors/data'

dfs = []
frames_with_missing_ball = 0
start = time.time()
for g,dir in enumerate(os.listdir(data_path)):
    game = pd.read_pickle(os.path.join(data_path,dir))
    game_id = game['gameid']
    print(f'Loading game {dir}  progress: {i}/{len(os.listdir(data_path))}')
    for i in range(len(game['events'])):
        home_id = game['events'][i]['home']['teamid']
        visitor_id = game['events'][i]['visitor']['teamid']
        prev_time = game['events'][i]['moments'][0][1]
        prev_off = False
        prev_ball_x = 0
        prev_ball_y = 0
        prev_pos = []
        starting_index = 0
        data_list = []
        for j in range(len(game['events'][i]['moments'])):
            moment = game['events'][i]['moments'][j]
            if len(moment[5])<10:#if ball is off the court
                continue
                
            data =  {
                'Game_ID':game_id,
                'Event_ID':i,
                'Moment_ID':j,
                'Moment_Time':moment[1],
                'Ball_X':moment[5][0][-3],
                'Ball_Y':moment[5][0][-2],
                'Ball_Z':moment[5][0][-1],

            }
            
            prev_ball_x = moment[5][0][-3]
            prev_ball_y = moment[5][0][-2]
            if len(moment[5])==10:
                tracking_data = moment[5]
            else:
                tracking_data =  moment[5][1:]
            
            for k in range(len(moment[5][1:])):
                team_side = 'H' if game['events'][i]['moments'][j][5][k][0]==home_id else 'V'
                data[f'Player_{team_side}_{k%5}_X'] = tracking_data[k][2]
                data[f'Player_{team_side}_{k%5}_Y'] = tracking_data[k][3]

            data_list.append(data)
        df = pd.DataFrame(data_list)
        df['Moment_Time_Diff'] = df['Moment_Time'].diff().fillna(0)
        df['Ball_DXDT'] = df['Ball_X'].diff().div(df['Moment_Time_Diff'], fill_value=0)
        df['Ball_DYDT'] = df['Ball_Y'].diff().div(df['Moment_Time_Diff'], fill_value=0)
        for i in range(10):
            team_side = 'H' if i<5 else 'V'
            df[f'Player_{team_side}_{i%5}_DXDT'] = df[f'Player_{team_side}_{i%5}_X'].diff().div(df['Moment_Time_Diff'], fill_value=0)
            df[f'Player_{team_side}_{i%5}_DYDT'] = df[f'Player_{team_side}_{i%5}_X'].diff().div(df['Moment_Time_Diff'], fill_value=0)
        columns = ['Ball_DXDT','Ball_DYDT','Player_H_0_DXDT','Player_H_1_DXDT','Player_H_2_DXDT','Player_H_3_DXDT','Player_H_4_DXDT','Player_V_0_DXDT','Player_V_1_DXDT','Player_V_2_DXDT','Player_V_3_DXDT','Player_V_4_DXDT','Player_H_0_DYDT','Player_H_1_DYDT','Player_H_2_DYDT','Player_H_3_DYDT','Player_H_4_DYDT','Player_V_0_DYDT','Player_V_1_DYDT','Player_V_2_DYDT','Player_V_3_DYDT','Player_V_4_DYDT']
        df.loc[0, columns] = df.loc[1,columns]
        # print(df.head())
        # has_nan = df.isna().any().any()

        # if has_nan:
        #     print("The DataFrame has NaN values.")
        # else:
        #     print("The DataFrame does not have any NaN values.")
        dfs.append(df)
        




    

stop = time.time()
pd.set_option('display.max_columns', None)
df = pd.concat(dfs)
print(df.head())
print('Time to load 1 game: ',stop-start, '. We have ',len(os.listdir(data_path)) , 'games so it would take ',len(os.listdir(data_path))*(stop-start)/60., ' minutes ',)
print(frames_with_missing_ball)
engine = create_engine("sqlite+pysqlite:///deephoopers-mod.db",echo=True,future=True)
df.to_sql('TrackingDataTable',engine)

# '''
# engine.connect()
# engine.begin()
