
%     function [dl] = loss_grad(target,pred)
%         % target is the one hot encoded y_label
%         % pred is the vector of predictions
%         % dl/lp = yi/pi for all i in the length in the vector
%         
%         dl = -1./pred;
%         dl = dl.*target;
%         dl = single(dl);
%     
%     end
%         
% 
%     function [soft_grad] = softmax_gradient(hidden,outputs)
%         % computes the jacobian matrix for the gradient of the softmax
%         % given an input layer 
%         % d_softmax_i/dx_j = output_i(indicator(i,j) - output_j)
%          soft_grad = zeros(length(hidden));
%          
%          for i=1:length(hidden)
%              for j = 1:length(hidden)
%                  
%                  if i == j
%                      soft_grad = outputs(i)*(1-outputs(j));
%                  else
%                      soft_grad = outputs(i)*(-outputs(j));
%                  end
%              end
%          end
%          
%          soft_grad = single(soft_grad);
%     end