# CREATE A CONVOLUTIONAL MODEL CLASS

# import torch.nn.functional as F
import torch.nn as nn
from torch.nn import init
import torch

class Classifier(nn.Module):

    def __init__(self, n_channel):
        super(Classifier, self).__init__()

        conv_layers = []

        #It will be used every convolution block.
        self.relu = nn.ReLU()

        # 1. Convolution Block
        self.conv1 = nn.Conv2d(n_channel, 8, kernel_size=(5, 5), stride=(2, 2), padding=(2, 2))
        self.bn1 = nn.BatchNorm2d(8)
        init.kaiming_normal_(self.conv1.weight, a=0.1)
        self.conv1.bias.data.zero_()
        conv_layers.extend( [self.conv1, self.relu, self.bn1] )

        # 2. Convolution Block
        self.conv2 = nn.Conv2d(8, 16, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
        self.bn2 = nn.BatchNorm2d(16)
        init.kaiming_normal_(self.conv2.weight, a=0.1)
        self.conv1.bias.data.zero_()
        conv_layers.extend( [self.conv2, self.relu, self.bn2] )


        # 3. Convolution Block
        self.conv3 = nn.Conv2d(16, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
        self.bn3 = nn.BatchNorm2d(32)
        init.kaiming_normal_(self.conv3.weight, a= 0.1)
        self.conv3.bias.data.zero_()
        conv_layers.extend( [self.conv3, self.relu, self.bn3] )

        # 4. Convolution Block
        self.conv4 = nn.Conv2d(32, 64, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
        self.bn4 = nn.BatchNorm2d(64)
        init.kaiming_normal_(self.conv4.weight, a = 0.1)
        self.conv4.bias.data.zero_()
        conv_layers.extend( [self.conv4, self.relu, self.bn4] )

        # Last step for classification
        # Fully Connected Linear Layer

        # Downsizing with pooling
        self.avgPool = nn.AdaptiveAvgPool2d(output_size=1)
        
        #flattening for input to linear layer
        self.flatten = nn.Flatten(1, -1)

        self.linear_layer = nn.Linear(in_features=64, out_features=5)

        conv_layers.extend([self.avgPool, self.flatten, self.linear_layer])

        #The list of conv_layer is unpacked and sent
        self.conv = nn.Sequential(*conv_layers) # nn.Squential() gets *args or OrderedDict

    def forward(self, inputs):
        
        return self.conv(inputs)


# This section is for test and development

if __name__ == "__main__":

    class Classifier(nn.Module):
        def __init__(self, n_channel):
            super(Classifier, self).__init__()
            self.relu = nn.ReLU()
            self.conv1 = nn.Conv2d(n_channel, 8, kernel_size=(5, 5), stride=(2, 2), padding=(2, 2))
            self.bn1 = nn.BatchNorm2d(8)
            init.kaiming_normal_(self.conv1.weight, a=0.1)
            self.conv1.bias.data.zero_()

        def forward(self, x):
            a = self.conv1(x)
            # print(a)
            b = self.relu(a)
            # print(b)
            c = self.bn1(b)
            print(c)
            return c

    test1 = torch.tensor([[ [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1]  ]], dtype=torch.float32)

    #test1.shape:(1, 10, 10)

    classifier = Classifier(1)

    # result = classifier(  torch.stack((test1, test1, test1), 0)    )

    result = classifier (   torch.unsqueeze(test1, 0 )   )
