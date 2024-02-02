import torch
import torch.nn as nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
import numpy as np
from BaseTransformer import AttentionEncoder
from PositionalEncoding import PositionalEncoding
from SimpleLSTM import SimpleLSTM
from ConvEncoderDecoder import AutoEncoder
from Utils.data_utils import sim_to_seqx_y,sim_to_auto_enc_data
import math

class ATTN2DLSTM(nn.Module):

    def __init__(self,seq_length=5,embedding_dim = 512,model_dropout = .1):
        super(ATTN2DLSTM,self).__init__()

        # constant definitions
        self.seq_len = seq_length
        self.embed_dim = embedding_dim
        self.dout = model_dropout

        # define the convolutional encoder and decoder
        self.enc_dec = AutoEncoder()
        self.encoder = self.enc_dec.encoder
        self.decoder = self.enc_dec.decoder

        # define the attention encoder
        self.attn = AttentionEncoder()

        # define the LSTM Module
        self.lstm = SimpleLSTM()


    def forward(self,x):
        # a mini-batch of data of the form:
        # batch_size,sequence_size,input_dims will be passed to the
        # encoder, after passing it through, we will reshape it for passing 
        # into the attention mechanism


        # process each element in the sequence, turn it into its own tensor
        x_sec = torch.zeros((self.seq_len,x.shape[2],x.shape[3],x.shape[4]))
        for i in range(x.shape[1]):
            x_sec[i,:,:,:] = x[0,i,:,:,:]
            
        x_enc = self.encoder(x_sec)
        # reshape the sequence
        x_enc = x_enc.view(1,self.seq_len,-1)

        # LOOK AT VECTORIZING
        x_enc = x_enc[:,:,:512]
        x_attn = self.attn(x_enc)
        x_lstm, (_,_) = self.lstm(x_attn)
        # out = self.decoder(x_lstm)
        return x_lstm


    




