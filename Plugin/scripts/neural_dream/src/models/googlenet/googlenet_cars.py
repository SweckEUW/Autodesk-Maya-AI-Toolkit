import torch
import torch.nn as nn
import torch.nn.functional as F
import neural_dream.src.helper_layers as helper_layers


class GOOGLENET_CARS(nn.Module):

    def __init__(self):
        super(GOOGLENET_CARS, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=(7, 7), stride=(2, 2), groups=1, bias=True)
        self.conv2_1x1 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.conv2_3x3 = nn.Conv2d(in_channels=64, out_channels=192, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.inception_3a_5x5_reduce = nn.Conv2d(in_channels=192, out_channels=16, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_3a_3x3_reduce = nn.Conv2d(in_channels=192, out_channels=96, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_3a_1x1 = nn.Conv2d(in_channels=192, out_channels=64, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_3a_pool_proj = nn.Conv2d(in_channels=192, out_channels=32, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_3a_5x5 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(5, 5), stride=(1, 1), groups=1, bias=True)
        self.inception_3a_3x3 = nn.Conv2d(in_channels=96, out_channels=128, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.inception_3b_1x1 = nn.Conv2d(in_channels=256, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_3b_3x3_reduce = nn.Conv2d(in_channels=256, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_3b_5x5_reduce = nn.Conv2d(in_channels=256, out_channels=32, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_3b_pool_proj = nn.Conv2d(in_channels=256, out_channels=64, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_3b_3x3 = nn.Conv2d(in_channels=128, out_channels=192, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.inception_3b_5x5 = nn.Conv2d(in_channels=32, out_channels=96, kernel_size=(5, 5), stride=(1, 1), groups=1, bias=True)
        self.inception_4a_3x3_reduce = nn.Conv2d(in_channels=480, out_channels=96, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4a_5x5_reduce = nn.Conv2d(in_channels=480, out_channels=16, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4a_1x1 = nn.Conv2d(in_channels=480, out_channels=192, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4a_pool_proj = nn.Conv2d(in_channels=480, out_channels=64, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4a_3x3 = nn.Conv2d(in_channels=96, out_channels=208, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.inception_4a_5x5 = nn.Conv2d(in_channels=16, out_channels=48, kernel_size=(5, 5), stride=(1, 1), groups=1, bias=True)
        self.inception_4b_3x3_reduce = nn.Conv2d(in_channels=512, out_channels=112, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4b_1x1 = nn.Conv2d(in_channels=512, out_channels=160, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4b_5x5_reduce = nn.Conv2d(in_channels=512, out_channels=24, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.loss1_conv = nn.Conv2d(in_channels=512, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4b_pool_proj = nn.Conv2d(in_channels=512, out_channels=64, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4b_3x3 = nn.Conv2d(in_channels=112, out_channels=224, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.inception_4b_5x5 = nn.Conv2d(in_channels=24, out_channels=64, kernel_size=(5, 5), stride=(1, 1), groups=1, bias=True)
        self.loss1_fc_1 = nn.Linear(in_features = 2048, out_features = 1024, bias = True)
        self.inception_4c_1x1 = nn.Conv2d(in_channels=512, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4c_5x5_reduce = nn.Conv2d(in_channels=512, out_channels=24, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4c_3x3_reduce = nn.Conv2d(in_channels=512, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4c_pool_proj = nn.Conv2d(in_channels=512, out_channels=64, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4c_5x5 = nn.Conv2d(in_channels=24, out_channels=64, kernel_size=(5, 5), stride=(1, 1), groups=1, bias=True)
        self.inception_4c_3x3 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.loss1_classifier_model_1 = nn.Linear(in_features = 1024, out_features = 431, bias = True)
        self.inception_4d_1x1 = nn.Conv2d(in_channels=512, out_channels=112, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4d_3x3_reduce = nn.Conv2d(in_channels=512, out_channels=144, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4d_5x5_reduce = nn.Conv2d(in_channels=512, out_channels=32, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4d_pool_proj = nn.Conv2d(in_channels=512, out_channels=64, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4d_3x3 = nn.Conv2d(in_channels=144, out_channels=288, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.inception_4d_5x5 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(5, 5), stride=(1, 1), groups=1, bias=True)
        self.inception_4e_1x1 = nn.Conv2d(in_channels=528, out_channels=256, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4e_3x3_reduce = nn.Conv2d(in_channels=528, out_channels=160, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4e_5x5_reduce = nn.Conv2d(in_channels=528, out_channels=32, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.loss2_conv = nn.Conv2d(in_channels=528, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4e_pool_proj = nn.Conv2d(in_channels=528, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_4e_3x3 = nn.Conv2d(in_channels=160, out_channels=320, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.inception_4e_5x5 = nn.Conv2d(in_channels=32, out_channels=128, kernel_size=(5, 5), stride=(1, 1), groups=1, bias=True)
        self.loss2_fc_1 = nn.Linear(in_features = 2048, out_features = 1024, bias = True)
        self.inception_5a_5x5_reduce = nn.Conv2d(in_channels=832, out_channels=32, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_5a_3x3_reduce = nn.Conv2d(in_channels=832, out_channels=160, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_5a_1x1 = nn.Conv2d(in_channels=832, out_channels=256, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_5a_pool_proj = nn.Conv2d(in_channels=832, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.loss2_classifier_model_1 = nn.Linear(in_features = 1024, out_features = 431, bias = True)
        self.inception_5a_5x5 = nn.Conv2d(in_channels=32, out_channels=128, kernel_size=(5, 5), stride=(1, 1), groups=1, bias=True)
        self.inception_5a_3x3 = nn.Conv2d(in_channels=160, out_channels=320, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.inception_5b_3x3_reduce = nn.Conv2d(in_channels=832, out_channels=192, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_5b_1x1 = nn.Conv2d(in_channels=832, out_channels=384, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_5b_5x5_reduce = nn.Conv2d(in_channels=832, out_channels=48, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_5b_pool_proj = nn.Conv2d(in_channels=832, out_channels=128, kernel_size=(1, 1), stride=(1, 1), groups=1, bias=True)
        self.inception_5b_3x3 = nn.Conv2d(in_channels=192, out_channels=384, kernel_size=(3, 3), stride=(1, 1), groups=1, bias=True)
        self.inception_5b_5x5 = nn.Conv2d(in_channels=48, out_channels=128, kernel_size=(5, 5), stride=(1, 1), groups=1, bias=True)


    def add_layers(self):	
        self.relu1 = helper_layers.ReluLayer()
        self.relu_conv2_1x1 = helper_layers.ReluLayer()
        self.relu2_3x3 = helper_layers.ReluLayer()
        self.relu_inception_3a_5x5_reduce = helper_layers.ReluLayer()
        self.reulu_inception_3a_3x3_reduce = helper_layers.ReluLayer()
        self.relu_inception_3a_1x1 = helper_layers.ReluLayer()
        self.relu_inception_3a_pool_proj = helper_layers.ReluLayer()
        self.relu_inception_3a_5x5 = helper_layers.ReluLayer()
        self.relu_inception_3a_3x3 = helper_layers.ReluLayer()
        self.relu_inception_3b_1x1 = helper_layers.ReluLayer()
        self.relu_inception_3b_3x3_reduce = helper_layers.ReluLayer()
        self.relu_inception_3b_5x5_reduce = helper_layers.ReluLayer()
        self.relu_inception_3b_pool_proj = helper_layers.ReluLayer()
        self.relu_inception_3b_3x3 = helper_layers.ReluLayer()
        self.relu_inception_3b_5x5 = helper_layers.ReluLayer()
        self.relu_inception_4a_3x3_reduce = helper_layers.ReluLayer()
        self.relu_inception_4a_5x5_reduce = helper_layers.ReluLayer()
        self.relu_inception_4a_1x1 = helper_layers.ReluLayer()
        self.relu_inception_4a_pool_proj = helper_layers.ReluLayer()
        self.relu_inception_4a_3x3 = helper_layers.ReluLayer()
        self.relu_inception_4a_5x5 = helper_layers.ReluLayer()
        self.inception_4b_relu_3x3_reduce = helper_layers.ReluLayer()
        self.inception_4b_relu_1x1 = helper_layers.ReluLayer()
        self.inception_4b_relu_5x5_reduce = helper_layers.ReluLayer()
        self.inception_4b_relu_pool_proj = helper_layers.ReluLayer()
        self.inception_4b_relu_3x3 = helper_layers.ReluLayer()
        self.inception_4b_relu_5x5 = helper_layers.ReluLayer()
        self.inception_4c_relu_1x1 = helper_layers.ReluLayer()
        self.inception_4c_relu_5x5_reduce = helper_layers.ReluLayer()
        self.inception_4c_relu_3x3_reduce = helper_layers.ReluLayer()
        self.inception_4c_relu_pool_proj = helper_layers.ReluLayer()
        self.inception_4c_relu_5x5 = helper_layers.ReluLayer()
        self.inception_4c_relu_3x3 = helper_layers.ReluLayer()
        self.inception_4d_relu_1x1 = helper_layers.ReluLayer()
        self.inception_4d_relu_3x3_reduce = helper_layers.ReluLayer()
        self.inception_4d_relu_5x5_reduce = helper_layers.ReluLayer()
        self.inception_4d_relu_pool_proj = helper_layers.ReluLayer()
        self.inception_4d_relu_3x3 = helper_layers.ReluLayer()
        self.inception_4d_relu_5x5 = helper_layers.ReluLayer()
        self.inception_4e_relu_1x1 = helper_layers.ReluLayer()
        self.inception_4e_relu_3x3_reduce = helper_layers.ReluLayer()
        self.inception_4e_relu_5x5_reduce = helper_layers.ReluLayer()
        self.inception_4e_relu_pool_proj = helper_layers.ReluLayer()
        self.inception_4e_relu_3x3 = helper_layers.ReluLayer()
        self.inception_4e_relu_5x5 = helper_layers.ReluLayer()
        self.inception_5a_relu_5x5_reduce = helper_layers.ReluLayer()
        self.inception_5a_relu_3x3_reduce = helper_layers.ReluLayer()
        self.inception_5a_relu_1x1 = helper_layers.ReluLayer()
        self.inception_5a_relu_pool_proj = helper_layers.ReluLayer()
        self.inception_5a_relu_5x5 = helper_layers.ReluLayer()
        self.inception_5a_relu_3x3 = helper_layers.ReluLayer()
        self.inception_5b_relu_3x3_reduce = helper_layers.ReluLayer()
        self.inception_5b_relu_1x1 = helper_layers.ReluLayer()
        self.inception_5b_relu_5x5_reduce = helper_layers.ReluLayer()
        self.inception_5b_relu_pool_proj = helper_layers.ReluLayer()
        self.inception_5b_relu_3x3 = helper_layers.ReluLayer()
        self.inception_5b_relu_5x5 = helper_layers.ReluLayer()

        self.pool1 = helper_layers.MaxPool2dLayer()
        self.pool2 = helper_layers.MaxPool2dLayer()
        self.inception_3a_pool = helper_layers.MaxPool2dLayer()
        self.inception_3b_pool = helper_layers.MaxPool2dLayer()
        self.pool3 = helper_layers.MaxPool2dLayer()
        self.inception_4a_pool = helper_layers.MaxPool2dLayer()
        self.inception_4b_pool = helper_layers.MaxPool2dLayer()
        self.inception_4c_pool = helper_layers.MaxPool2dLayer()
        self.inception_4d_pool = helper_layers.MaxPool2dLayer()
        self.inception_4e_pool = helper_layers.MaxPool2dLayer()
        self.pool4 = helper_layers.MaxPool2dLayer()
        self.inception_5a_pool = helper_layers.MaxPool2dLayer()
        self.inception_5b_pool = helper_layers.MaxPool2dLayer()
		
        self.inception_3a_output = helper_layers.CatLayer()
        self.inception_3b_output = helper_layers.CatLayer()
        self.inception_4a_output = helper_layers.CatLayer()
        self.inception_4b_output = helper_layers.CatLayer()
        self.inception_4c_output = helper_layers.CatLayer()
        self.inception_4d_output = helper_layers.CatLayer()
        self.inception_4e_output = helper_layers.CatLayer()
        self.inception_5a_output = helper_layers.CatLayer()
        self.inception_5b_output = helper_layers.CatLayer()
		
        self.pool5_drop = helper_layers.DropoutLayer()


    def forward(self, x):
        conv1_pad       = F.pad(x, (3, 3, 3, 3))
        conv1           = self.conv1(conv1_pad)
        relu1           = self.relu1(conv1)
        pool1_pad       = F.pad(relu1, (0, 1, 0, 1), value=float('-inf'))
        pool1           = self.pool1(pool1_pad, kernel_size=(3, 3), stride=(2, 2), padding=0, ceil_mode=False)
        norm1           = F.local_response_norm(pool1, size=5, alpha=9.999999747378752e-05, beta=0.75, k=1.0)
        conv2_1x1       = self.conv2_1x1(norm1)
        relu_conv2_1x1  = self.relu_conv2_1x1(conv2_1x1)
        conv2_3x3_pad   = F.pad(relu_conv2_1x1, (1, 1, 1, 1))
        conv2_3x3       = self.conv2_3x3(conv2_3x3_pad)
        relu2_3x3       = self.relu2_3x3(conv2_3x3)
        norm2           = F.local_response_norm(relu2_3x3, size=5, alpha=9.999999747378752e-05, beta=0.75, k=1.0)
        pool2_pad       = F.pad(norm2, (0, 1, 0, 1), value=float('-inf'))
        pool2           = self.pool2(pool2_pad, kernel_size=(3, 3), stride=(2, 2), padding=0, ceil_mode=False)
        inception_3a_5x5_reduce = self.inception_3a_5x5_reduce(pool2)
        inception_3a_3x3_reduce = self.inception_3a_3x3_reduce(pool2)
        inception_3a_1x1 = self.inception_3a_1x1(pool2)
        inception_3a_pool_pad = F.pad(pool2, (1, 1, 1, 1), value=float('-inf'))
        inception_3a_pool = self.inception_3a_pool(inception_3a_pool_pad, kernel_size=(3, 3), stride=(1, 1), padding=0, ceil_mode=False)
        relu_inception_3a_5x5_reduce = self.relu_inception_3a_5x5_reduce(inception_3a_5x5_reduce)
        reulu_inception_3a_3x3_reduce = self.reulu_inception_3a_3x3_reduce(inception_3a_3x3_reduce)
        relu_inception_3a_1x1 = self.relu_inception_3a_1x1(inception_3a_1x1)
        inception_3a_pool_proj = self.inception_3a_pool_proj(inception_3a_pool)
        inception_3a_5x5_pad = F.pad(relu_inception_3a_5x5_reduce, (2, 2, 2, 2))
        inception_3a_5x5 = self.inception_3a_5x5(inception_3a_5x5_pad)
        inception_3a_3x3_pad = F.pad(reulu_inception_3a_3x3_reduce, (1, 1, 1, 1))
        inception_3a_3x3 = self.inception_3a_3x3(inception_3a_3x3_pad)
        relu_inception_3a_pool_proj = self.relu_inception_3a_pool_proj(inception_3a_pool_proj)
        relu_inception_3a_5x5 = self.relu_inception_3a_5x5(inception_3a_5x5)
        relu_inception_3a_3x3 = self.relu_inception_3a_3x3(inception_3a_3x3)
        inception_3a_output = self.inception_3a_output((relu_inception_3a_1x1, relu_inception_3a_3x3, relu_inception_3a_5x5, relu_inception_3a_pool_proj), 1)
        inception_3b_1x1 = self.inception_3b_1x1(inception_3a_output)
        inception_3b_3x3_reduce = self.inception_3b_3x3_reduce(inception_3a_output)
        inception_3b_5x5_reduce = self.inception_3b_5x5_reduce(inception_3a_output)
        inception_3b_pool_pad = F.pad(inception_3a_output, (1, 1, 1, 1), value=float('-inf'))
        inception_3b_pool = self.inception_3b_pool(inception_3b_pool_pad, kernel_size=(3, 3), stride=(1, 1), padding=0, ceil_mode=False)
        relu_inception_3b_1x1 = self.relu_inception_3b_1x1(inception_3b_1x1)
        relu_inception_3b_3x3_reduce = self.relu_inception_3b_3x3_reduce(inception_3b_3x3_reduce)
        relu_inception_3b_5x5_reduce = self.relu_inception_3b_5x5_reduce(inception_3b_5x5_reduce)
        inception_3b_pool_proj = self.inception_3b_pool_proj(inception_3b_pool)
        inception_3b_3x3_pad = F.pad(relu_inception_3b_3x3_reduce, (1, 1, 1, 1))
        inception_3b_3x3 = self.inception_3b_3x3(inception_3b_3x3_pad)
        inception_3b_5x5_pad = F.pad(relu_inception_3b_5x5_reduce, (2, 2, 2, 2))
        inception_3b_5x5 = self.inception_3b_5x5(inception_3b_5x5_pad)
        relu_inception_3b_pool_proj = self.relu_inception_3b_pool_proj(inception_3b_pool_proj)
        relu_inception_3b_3x3 = self.relu_inception_3b_3x3(inception_3b_3x3)
        relu_inception_3b_5x5 = self.relu_inception_3b_5x5(inception_3b_5x5)
        inception_3b_output = self.inception_3b_output((relu_inception_3b_1x1, relu_inception_3b_3x3, relu_inception_3b_5x5, relu_inception_3b_pool_proj), 1)
        pool3_pad       = F.pad(inception_3b_output, (0, 1, 0, 1), value=float('-inf'))
        pool3           = self.pool3(pool3_pad, kernel_size=(3, 3), stride=(2, 2), padding=0, ceil_mode=False)
        inception_4a_pool_pad = F.pad(pool3, (1, 1, 1, 1), value=float('-inf'))
        inception_4a_pool = self.inception_4a_pool(inception_4a_pool_pad, kernel_size=(3, 3), stride=(1, 1), padding=0, ceil_mode=False)
        inception_4a_3x3_reduce = self.inception_4a_3x3_reduce(pool3)
        inception_4a_5x5_reduce = self.inception_4a_5x5_reduce(pool3)
        inception_4a_1x1 = self.inception_4a_1x1(pool3)
        inception_4a_pool_proj = self.inception_4a_pool_proj(inception_4a_pool)
        relu_inception_4a_3x3_reduce = self.relu_inception_4a_3x3_reduce(inception_4a_3x3_reduce)
        relu_inception_4a_5x5_reduce = self.relu_inception_4a_5x5_reduce(inception_4a_5x5_reduce)
        relu_inception_4a_1x1 = self.relu_inception_4a_1x1(inception_4a_1x1)
        relu_inception_4a_pool_proj = self.relu_inception_4a_pool_proj(inception_4a_pool_proj)
        inception_4a_3x3_pad = F.pad(relu_inception_4a_3x3_reduce, (1, 1, 1, 1))
        inception_4a_3x3 = self.inception_4a_3x3(inception_4a_3x3_pad)
        inception_4a_5x5_pad = F.pad(relu_inception_4a_5x5_reduce, (2, 2, 2, 2))
        inception_4a_5x5 = self.inception_4a_5x5(inception_4a_5x5_pad)
        relu_inception_4a_3x3 = self.relu_inception_4a_3x3(inception_4a_3x3)
        relu_inception_4a_5x5 = self.relu_inception_4a_5x5(inception_4a_5x5)
        inception_4a_output = self.inception_4a_output((relu_inception_4a_1x1, relu_inception_4a_3x3, relu_inception_4a_5x5, relu_inception_4a_pool_proj), 1)
        #loss1_ave_pool  = F.avg_pool2d(inception_4a_output, kernel_size=(5, 5), stride=(3, 3), padding=(0,), ceil_mode=True, count_include_pad=False)
        inception_4b_3x3_reduce = self.inception_4b_3x3_reduce(inception_4a_output)
        inception_4b_1x1 = self.inception_4b_1x1(inception_4a_output)
        inception_4b_pool_pad = F.pad(inception_4a_output, (1, 1, 1, 1), value=float('-inf'))
        inception_4b_pool = self.inception_4b_pool(inception_4b_pool_pad, kernel_size=(3, 3), stride=(1, 1), padding=0, ceil_mode=False)
        inception_4b_5x5_reduce = self.inception_4b_5x5_reduce(inception_4a_output)
        #loss1_conv      = self.loss1_conv(loss1_ave_pool)
        inception_4b_relu_3x3_reduce = self.inception_4b_relu_3x3_reduce(inception_4b_3x3_reduce)
        inception_4b_relu_1x1 = self.inception_4b_relu_1x1(inception_4b_1x1)
        inception_4b_pool_proj = self.inception_4b_pool_proj(inception_4b_pool)
        inception_4b_relu_5x5_reduce = self.inception_4b_relu_5x5_reduce(inception_4b_5x5_reduce)
        #loss1_relu_conv = F.relu(loss1_conv)
        inception_4b_3x3_pad = F.pad(inception_4b_relu_3x3_reduce, (1, 1, 1, 1))
        inception_4b_3x3 = self.inception_4b_3x3(inception_4b_3x3_pad)
        inception_4b_relu_pool_proj = self.inception_4b_relu_pool_proj(inception_4b_pool_proj)
        inception_4b_5x5_pad = F.pad(inception_4b_relu_5x5_reduce, (2, 2, 2, 2))
        inception_4b_5x5 = self.inception_4b_5x5(inception_4b_5x5_pad)
        #loss1_fc_0      = loss1_relu_conv.view(loss1_relu_conv.size(0), -1)
        inception_4b_relu_3x3 = self.inception_4b_relu_3x3(inception_4b_3x3)
        inception_4b_relu_5x5 = self.inception_4b_relu_5x5(inception_4b_5x5)
        #loss1_fc_1      = self.loss1_fc_1(loss1_fc_0)
        inception_4b_output = self.inception_4b_output((inception_4b_relu_1x1, inception_4b_relu_3x3, inception_4b_relu_5x5, inception_4b_relu_pool_proj), 1)
        #loss1_relu_fc   = F.relu(loss1_fc_1)
        inception_4c_pool_pad = F.pad(inception_4b_output, (1, 1, 1, 1), value=float('-inf'))
        inception_4c_pool = self.inception_4c_pool(inception_4c_pool_pad, kernel_size=(3, 3), stride=(1, 1), padding=0, ceil_mode=False)
        inception_4c_1x1 = self.inception_4c_1x1(inception_4b_output)
        inception_4c_5x5_reduce = self.inception_4c_5x5_reduce(inception_4b_output)
        inception_4c_3x3_reduce = self.inception_4c_3x3_reduce(inception_4b_output)
        #loss1_drop_fc   = F.dropout(input = loss1_relu_fc, p = 0.699999988079071, training = self.training, inplace = True)
        inception_4c_pool_proj = self.inception_4c_pool_proj(inception_4c_pool)
        inception_4c_relu_1x1 = self.inception_4c_relu_1x1(inception_4c_1x1)
        inception_4c_relu_5x5_reduce = self.inception_4c_relu_5x5_reduce(inception_4c_5x5_reduce)
        inception_4c_relu_3x3_reduce = self.inception_4c_relu_3x3_reduce(inception_4c_3x3_reduce)
        #loss1_classifier_model_0 = loss1_drop_fc.view(loss1_drop_fc.size(0), -1)
        inception_4c_relu_pool_proj = self.inception_4c_relu_pool_proj(inception_4c_pool_proj)
        inception_4c_5x5_pad = F.pad(inception_4c_relu_5x5_reduce, (2, 2, 2, 2))
        inception_4c_5x5 = self.inception_4c_5x5(inception_4c_5x5_pad)
        inception_4c_3x3_pad = F.pad(inception_4c_relu_3x3_reduce, (1, 1, 1, 1))
        inception_4c_3x3 = self.inception_4c_3x3(inception_4c_3x3_pad)
        #loss1_classifier_model_1 = self.loss1_classifier_model_1(loss1_classifier_model_0)
        inception_4c_relu_5x5 = self.inception_4c_relu_5x5(inception_4c_5x5)
        inception_4c_relu_3x3 = self.inception_4c_relu_3x3(inception_4c_3x3)
        inception_4c_output = self.inception_4c_output((inception_4c_relu_1x1, inception_4c_relu_3x3, inception_4c_relu_5x5, inception_4c_relu_pool_proj), 1)
        inception_4d_1x1 = self.inception_4d_1x1(inception_4c_output)
        inception_4d_3x3_reduce = self.inception_4d_3x3_reduce(inception_4c_output)
        inception_4d_5x5_reduce = self.inception_4d_5x5_reduce(inception_4c_output)
        inception_4d_pool_pad = F.pad(inception_4c_output, (1, 1, 1, 1), value=float('-inf'))
        inception_4d_pool = self.inception_4d_pool(inception_4d_pool_pad, kernel_size=(3, 3), stride=(1, 1), padding=0, ceil_mode=False)
        inception_4d_relu_1x1 = self.inception_4d_relu_1x1(inception_4d_1x1)
        inception_4d_relu_3x3_reduce = self.inception_4d_relu_3x3_reduce(inception_4d_3x3_reduce)
        inception_4d_relu_5x5_reduce = self.inception_4d_relu_5x5_reduce(inception_4d_5x5_reduce)
        inception_4d_pool_proj = self.inception_4d_pool_proj(inception_4d_pool)
        inception_4d_3x3_pad = F.pad(inception_4d_relu_3x3_reduce, (1, 1, 1, 1))
        inception_4d_3x3 = self.inception_4d_3x3(inception_4d_3x3_pad)
        inception_4d_5x5_pad = F.pad(inception_4d_relu_5x5_reduce, (2, 2, 2, 2))
        inception_4d_5x5 = self.inception_4d_5x5(inception_4d_5x5_pad)
        inception_4d_relu_pool_proj = self.inception_4d_relu_pool_proj(inception_4d_pool_proj)
        inception_4d_relu_3x3 = self.inception_4d_relu_3x3(inception_4d_3x3)
        inception_4d_relu_5x5 = self.inception_4d_relu_5x5(inception_4d_5x5)
        inception_4d_output = self.inception_4d_output((inception_4d_relu_1x1, inception_4d_relu_3x3, inception_4d_relu_5x5, inception_4d_relu_pool_proj), 1)
        #loss2_ave_pool  = F.avg_pool2d(inception_4d_output, kernel_size=(5, 5), stride=(3, 3), padding=(0,), ceil_mode=True, count_include_pad=False)
        inception_4e_pool_pad = F.pad(inception_4d_output, (1, 1, 1, 1), value=float('-inf'))
        inception_4e_pool = self.inception_4e_pool(inception_4e_pool_pad, kernel_size=(3, 3), stride=(1, 1), padding=0, ceil_mode=False)
        inception_4e_1x1 = self.inception_4e_1x1(inception_4d_output)
        inception_4e_3x3_reduce = self.inception_4e_3x3_reduce(inception_4d_output)
        inception_4e_5x5_reduce = self.inception_4e_5x5_reduce(inception_4d_output)
        #loss2_conv      = self.loss2_conv(loss2_ave_pool)
        inception_4e_pool_proj = self.inception_4e_pool_proj(inception_4e_pool)
        inception_4e_relu_1x1 = self.inception_4e_relu_1x1(inception_4e_1x1)
        inception_4e_relu_3x3_reduce = self.inception_4e_relu_3x3_reduce(inception_4e_3x3_reduce)
        inception_4e_relu_5x5_reduce = self.inception_4e_relu_5x5_reduce(inception_4e_5x5_reduce)
        #loss2_relu_conv = F.relu(loss2_conv)
        inception_4e_relu_pool_proj = self.inception_4e_relu_pool_proj(inception_4e_pool_proj)
        inception_4e_3x3_pad = F.pad(inception_4e_relu_3x3_reduce, (1, 1, 1, 1))
        inception_4e_3x3 = self.inception_4e_3x3(inception_4e_3x3_pad)
        inception_4e_5x5_pad = F.pad(inception_4e_relu_5x5_reduce, (2, 2, 2, 2))
        inception_4e_5x5 = self.inception_4e_5x5(inception_4e_5x5_pad)
        #loss2_fc_0      = loss2_relu_conv.view(loss2_relu_conv.size(0), -1)
        inception_4e_relu_3x3 = self.inception_4e_relu_3x3(inception_4e_3x3)
        inception_4e_relu_5x5 = self.inception_4e_relu_5x5(inception_4e_5x5)
        #loss2_fc_1      = self.loss2_fc_1(loss2_fc_0)
        inception_4e_output = self.inception_4e_output((inception_4e_relu_1x1, inception_4e_relu_3x3, inception_4e_relu_5x5, inception_4e_relu_pool_proj), 1)
        #loss2_relu_fc   = F.relu(loss2_fc_1)
        pool4_pad       = F.pad(inception_4e_output, (0, 1, 0, 1), value=float('-inf'))
        pool4           = self.pool4(pool4_pad, kernel_size=(3, 3), stride=(2, 2), padding=0, ceil_mode=False)
        #loss2_drop_fc   = F.dropout(input = loss2_relu_fc, p = 0.699999988079071, training = self.training, inplace = True)
        inception_5a_pool_pad = F.pad(pool4, (1, 1, 1, 1), value=float('-inf'))
        inception_5a_pool = self.inception_5a_pool(inception_5a_pool_pad, kernel_size=(3, 3), stride=(1, 1), padding=0, ceil_mode=False)
        inception_5a_5x5_reduce = self.inception_5a_5x5_reduce(pool4)
        inception_5a_3x3_reduce = self.inception_5a_3x3_reduce(pool4)
        inception_5a_1x1 = self.inception_5a_1x1(pool4)
        #loss2_classifier_model_0 = loss2_drop_fc.view(loss2_drop_fc.size(0), -1)
        inception_5a_pool_proj = self.inception_5a_pool_proj(inception_5a_pool)
        inception_5a_relu_5x5_reduce = self.inception_5a_relu_5x5_reduce(inception_5a_5x5_reduce)
        inception_5a_relu_3x3_reduce = self.inception_5a_relu_3x3_reduce(inception_5a_3x3_reduce)
        inception_5a_relu_1x1 = self.inception_5a_relu_1x1(inception_5a_1x1)
        #loss2_classifier_model_1 = self.loss2_classifier_model_1(loss2_classifier_model_0)
        inception_5a_relu_pool_proj = self.inception_5a_relu_pool_proj(inception_5a_pool_proj)
        inception_5a_5x5_pad = F.pad(inception_5a_relu_5x5_reduce, (2, 2, 2, 2))
        inception_5a_5x5 = self.inception_5a_5x5(inception_5a_5x5_pad)
        inception_5a_3x3_pad = F.pad(inception_5a_relu_3x3_reduce, (1, 1, 1, 1))
        inception_5a_3x3 = self.inception_5a_3x3(inception_5a_3x3_pad)
        inception_5a_relu_5x5 = self.inception_5a_relu_5x5(inception_5a_5x5)
        inception_5a_relu_3x3 = self.inception_5a_relu_3x3(inception_5a_3x3)
        inception_5a_output = self.inception_5a_output((inception_5a_relu_1x1, inception_5a_relu_3x3, inception_5a_relu_5x5, inception_5a_relu_pool_proj), 1)
        inception_5b_3x3_reduce = self.inception_5b_3x3_reduce(inception_5a_output)
        inception_5b_1x1 = self.inception_5b_1x1(inception_5a_output)
        inception_5b_5x5_reduce = self.inception_5b_5x5_reduce(inception_5a_output)
        inception_5b_pool_pad = F.pad(inception_5a_output, (1, 1, 1, 1), value=float('-inf'))
        inception_5b_pool = self.inception_5b_pool(inception_5b_pool_pad, kernel_size=(3, 3), stride=(1, 1), padding=0, ceil_mode=False)
        inception_5b_relu_3x3_reduce = self.inception_5b_relu_3x3_reduce(inception_5b_3x3_reduce)
        inception_5b_relu_1x1 = self.inception_5b_relu_1x1(inception_5b_1x1)
        inception_5b_relu_5x5_reduce = self.inception_5b_relu_5x5_reduce(inception_5b_5x5_reduce)
        inception_5b_pool_proj = self.inception_5b_pool_proj(inception_5b_pool)
        inception_5b_3x3_pad = F.pad(inception_5b_relu_3x3_reduce, (1, 1, 1, 1))
        inception_5b_3x3 = self.inception_5b_3x3(inception_5b_3x3_pad)
        inception_5b_5x5_pad = F.pad(inception_5b_relu_5x5_reduce, (2, 2, 2, 2))
        inception_5b_5x5 = self.inception_5b_5x5(inception_5b_5x5_pad)
        inception_5b_relu_pool_proj = self.inception_5b_relu_pool_proj(inception_5b_pool_proj)
        inception_5b_relu_3x3 = self.inception_5b_relu_3x3(inception_5b_3x3)
        inception_5b_relu_5x5 = self.inception_5b_relu_5x5(inception_5b_5x5)
        inception_5b_output = self.inception_5b_output((inception_5b_relu_1x1, inception_5b_relu_3x3, inception_5b_relu_5x5, inception_5b_relu_pool_proj), 1)
        pool5           = F.avg_pool2d(inception_5b_output, kernel_size=(7, 7), stride=(1, 1), padding=(0,), ceil_mode=False, count_include_pad=False)
        pool5_drop      = self.pool5_drop(input = pool5, p = 0.4000000059604645, training = self.training, inplace = True)
        return pool5_drop