
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

max_iter=2;             % maximum number of iterations
iter = 1;
fprintf('Training ...\n');
Loss_Tracker = zeros(1,4);


while iter < max_iter
  fprintf('Iteration %d ...\n', iter);
  % implement gradient descent updates here
  % hint use fullGradient
  [del_Wi,del_Wo,Loss] = fullGradient(Wi,Wo,alpha_i,alpha_o,train_data,train_labels, nclasses);
  Loss_Tracker(iter) = Loss;
  Wi = Wi - eta*del_Wi;
  Wo = Wo - eta*del_Wo;
 
  
  iter = iter + 1;
end

plot(Loss_Tracker)


% Test and print accuracy
fprintf('Testing ...\n');
acc = 0;
N   = length(test_labels);%N=5;
y_pred = zeros(size(test_labels));

for k = 1:N
  yi = [1;train_data(k, :)']; % input
  v1 = Wi*yi; % FC
  yh = [1;relu(v1)]; % hidden layer w/ bias
  
  % output layer
  v2 = Wo*yh; % FC
  yo = softmax(v2); % softmax
  
  [~, i] = max(yo);
  y_pred(k) = i;
  if i == train_labels(k)
    acc = acc + 1;
  end
  if(rem(k, 100)==0)
    fprintf('%d done.\n', k);
  end
end

acc = acc / N;
fprintf('Accuracy is %f\n', acc);

function [y] = softmax(z)
    % Paste your softmax function here
        z_max = max(z);
        z_exp = exp(z-z_max);
        y = single(z_exp/sum(z_exp));

    end
    
    function [y] = relu(x)
    % Paste your relu function here
        x(x<0) = 0;
        y = x;
        y = single(y);
    end
    
    function [d] = onehotenc(nclasses, k)
        %   ONEHOTENC return a onehot vector of class k
        %   vector with zeros and 1 at position k
        d = zeros([nclasses,1]);
        d(k) = 1;
        
end
% 
% function [dWi,dWo] = fullGradient(Wi,Wo,alpha_i,alpha_o, Inputs, Labels, nclasses)
% % Paste your code for calculating gradients here
% 
% end
