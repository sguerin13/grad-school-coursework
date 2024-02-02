%% Assessment 2
clear
rng('default');

%% loading data
load mnist.mat

% rename label 0 to 10
train_labels(train_labels == 0) = 10;
test_labels(test_labels == 0)   = 10;
labels = unique(train_labels);

%% Neural Network

% Fixed parameters
d = size(train_data, 2); % MNIST digit size 
nclasses = length(labels); % total number of classes
Ni = d; % Number of external inputs
Nh = 200; % Number of hidden units
No = nclasses; % Number of output units
alpha_i = 0.0; % Input weight decay
alpha_o = 0.0; % Output weight decay
range = 0.1; % Initial weight range                
eta=0.001; % gradient descent parameter

% Initialize network weights
Wi = range * randn(Nh,Ni+1);
Wo = range * randn(No,Nh+1);

[dWi,dWo,total_Loss] =  fullGradient(Wi,Wo,alpha_i,alpha_o,train_data,train_labels, nclasses);
