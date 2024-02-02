function [dWi,dWo,Total_Loss] = fullGradient(Wi,Wo,alpha_i,alpha_o, Inputs, Labels, nclasses)
%
% Calculate the partial derivatives of the quadratic cost function
% wrt. the weights. Derivatives of quadratic weight decay are included.
%
% Input:
%        Wi      :  Matrix with input-to-hidden weights
%        Wo      :  Matrix with hidden-to-outputs weights
%        alpha_i :  Weight decay parameter for input weights
%        alpha_o :  Weight decay parameter for output weights
%        Inputs  :  Matrix with examples as rows
%        Targets :  Matrix with target values as rows
% Output:
%        dWi     :  Matrix with gradient for input weights
%        dWo     :  Matrix with gradient for output weights

% Determine the number of examples

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

    function [soft_grad] = softmax_grad(y_target,y_pred)
        % combines the dL/dp*dp/a_2(a2) in a single function to prevent any
        % overflow/underflow errors
        
        soft_grad = y_pred - y_target;
        soft_grad = single(soft_grad);
        
    end

    
    function [relu_grad] = relu_grad(x)
        relu_grad = x;
        relu_grad(relu_grad<=0) = 0;
        relu_grad(relu_grad>0) = 1;
        relu_grad = single(relu_grad);
    end
     
[ndata, inp_dim] = size(Inputs);

dWi = single(zeros(size(Wi)));
dWo = single(zeros(size(Wo)));
Total_Loss = 0;
% compute the derivatives for each data point separately.


for k=1:ndata
  %%%%%%%%%%%%%%%%%%%%
  %%% FORWARD PASS %%%
  %%%%%%%%%%%%%%%%%%%%
  %
  % Propagate kth example forward through network
  % calculating all hidden- and output unit outputs

  input = Inputs(k,:);
  a_1 = Wi*[1,input]';
%   disp(size(a_1))
  h_1 = relu(a_1);
%   disp(size(h_1));
  a_2 = Wo*[[1];[h_1]];
  probs = softmax(a_2);
  % Calculate hidden unit outputs for every example
  

  %%%%%%%%%%%%%%%%%%%%%
  %%% BACKWARD PASS %%%
  %%%%%%%%%%%%%%%%%%%%%

  
  y_target = Labels(k); % gt class label
  y_t_one_hot = onehotenc(10,y_target);
  pred_label = find(probs==max(probs));
%   disp(a_2)
%   disp(probs)
%   disp(y_target)
  log_loss = -log(probs(y_target));% loss
%   disp(log_loss)
  if log_loss == Inf
      log_loss = 100;
  end
      
  Total_Loss = Total_Loss + log_loss;
  delta_a2 = softmax_grad(y_t_one_hot,probs); % error propagated back to the inputs of softmax
%   disp(delta_a2);  
  % weight updates 
  dW_2 = delta_a2*h_1';
  dB_2 = delta_a2;
  
  % propagate error back up the chain
  delta_h1 = Wo(:,2:end)'*delta_a2; % post relu error accumulation
  delta_a1 = delta_h1.*relu_grad(a_1); % pre relu error accumulation
  
  % weight updates
  dW_1 = delta_a1*input;
  dB_1 = delta_a1;
  
  
  temp_dWo = [dB_2,dW_2]; % aggregate the biases and the weight gradients
  temp_dWi = [dB_1,dW_1]; 
  
  dWi = dWi + single(temp_dWi);
  dWo = dWo + single(temp_dWo);


end


% Add derivatives of the weight decay term
dWi = dWi/ndata;
dWi = dWi+alpha_i*dWi;

dWo = dWo/ndata;
dWo = dWo+alpha_o*dWo;


end