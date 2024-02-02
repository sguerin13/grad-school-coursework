'''
Handles all of the data preprocessing for the train.py script

makes use of data utils to load files and prepare it for loading into the model

- load data
- standardize the data
- load it into batches for the model
- convert it into a torch data loader file

'''

import torch
import numpy as np
from sklearn.preprocessing import StandardScaler as STD
import Utils.data_utils as du
import os

def build_scalers(path):

    '''
    - provide the path to the simulation directory

    - saves scalars built on the dataset in the file directory

    '''

    list_of_files = os.listdir(path = path+'.')
    # sim_scaled,vscaler,rho_scaler = du.normalize_sim_data(sim,std=True)
    # sdf_scaled,sdf_scaler = du.normalize_data(sdf,SDF=True)

    velo_scaler  = STD()
    rho_scaler   = STD()
    sdf_scaler   = STD()
    # param_scaler = STD()
    Re_scaler    = STD()

    for i in range(len(list_of_files)):
        # print(i)
        sim,sdf,param_vec      = du.load_array_with_sdf_and_params(path + list_of_files[i])
        velo_scaler,rho_scaler = du.partially_fit_sim_scaler(velo_scaler,rho_scaler,sim)
        sdf_scaler             = du.partially_fit_data_scaler(sdf_scaler,sdf,SDF=True)
        # param_scaler           = du.partially_fit_data_scaler(param_scaler,param_vec,SDF=False)
        Re_scaler              = du.partially_fit_data_scaler(param_scaler,param_vec,SDF=False)
        

    # save the scalers
    du.save_std_scaler(velo_scaler,'./Data/scalers/velo_scaler_circles_5-10-20.pkl')
    du.save_std_scaler(rho_scaler,'./Data/scalers/rho_scaler_circles_5-10-20.pkl')
    du.save_std_scaler(sdf_scaler,'./Data/scalers/sdf_scaler_circles_5-10-20.pkl')
    # du.save_std_scaler(param_scaler,'./Data/scalers/param_scaler_circles_5-10-20.pkl')
    du.save_std_scaler(Re_scaler,'./Data/scalers/Re_scaler_circles_5-10-20.pkl')
    
    return


def scale_data(data,scaler_1,scaler_2=None,data_type = 'sim'):

    '''
    scales a given array using provided scalers

    '''
    
    if data_type == 'sim':
        # scaler_1 = velo_scaler
        # scaler_2 = rho_scaler
        scaled_data = du.normalize_sim_w_scaler(data,scaler_1,scaler_2)
    
    elif data_type == 'SDF':
        scaled_data = du.normalize_data_w_scaler(data,scaler_1,SDF=True)

    # elif data_type == 'params': 
    #     # parameter vector
    #     scaled_data = du.normalize_data_w_scaler(data,scaler_1,SDF=False)

    elif data_type == 'Re': 
        # parameter vector
        scaled_data = du.normalize_data_w_scaler(data,scaler_1,SDF=False)
    
    else:
        print('please provide a data type')
        return

    return scaled_data

def build_scaled_dataset(path,velo_scaler,rho_scaler,sdf_scaler,Re_scaler,mode = 'x to y',num_scenes='max'):

    if num_scenes is not 'max':   
        list_of_files = os.listdir(path = path+'.')
        assert len(list_of_files) >= num_scenes, 'not enough scenes in the directory'
    else:
        list_of_files = os.listdir(path = path+'.')
        num_scenes = len(list_of_files)
    
    for i in range(num_scenes):
        # load the data from the file
        sim,sdf,mask,Re = du.load_array_with_sdf_mask_Re(path + list_of_files[i])
        # scale the data
        sim_scaled = scale_data(data=sim,scaler_1 = velo_scaler,scaler_2 = rho_scaler,data_type='sim')
        sdf_scaled = scale_data(data=sdf,scaler_1 = sdf_scaler,data_type = 'SDF')
        param_vec = param_vec.reshape(1,-1) # need to turn it into row vec
        param_scaled = scale_data(data=param_vec,scaler_1 = param_scaler,data_type = 'params')
        # print('param_scaled shape',param_scaled.shape)

        # create multiple copies of the SDF and params so that they stack with the sim data
        sdf_scaled = np.repeat(sdf_scaled,sim_scaled.shape[0],axis=0)  # now shape is (num_time_steps,y,x)
        sdf_scaled = np.expand_dims(sdf_scaled,axis = 1)               # now shape is (num_time_steps,1,y,x) - now we can stack
        
        # create multiple copies of the param data
        param_scaled = np.repeat(param_scaled,sim_scaled.shape[0],axis=0) # shape: (num_time_steps,1,num_params)
        
        # stack the sdf and the sim
        stacked_sim = np.concatenate((sim_scaled,sdf_scaled),axis = 1) # input to conv_encoder
        
        if mode == 'x to y':

            # split into x and y
            x_data,y_data = du.sim_to_x_y(stacked_sim)
            # remove the sdf from the y_data
            y_data = y_data[:,:-1,:,:]
            # shorten the parameter vector
            param_scaled = du.param_to_x_y(param_scaled)
        
            if i == 0:
                list_out = [x_data,param_scaled,y_data] # create the list
            else:
                list_out[0] = np.concatenate((list_out[0],x_data),axis=0) # start stacking scenes
                list_out[1] = np.concatenate((list_out[1],param_scaled),axis=0)
                list_out[2] = np.concatenate((list_out[2],y_data),axis = 0)


        else:
            print('add more here ')
            return

    return list_out

