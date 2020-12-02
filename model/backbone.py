from torchsummary import summary
from torchvision.models.detection import MaskRCNN
import torch
import timm
import torchvision
import torchvision.models as models
import torchvision.models.detection.backbone_utils as backbone_utils
from collections import OrderedDict
from torch import nn
from torchvision.ops.feature_pyramid_network import FeaturePyramidNetwork, LastLevelMaxPool
#from timm.models.attFPN import AttFeaturePyramidNetwork, LastLevelMaxPool
from torchvision.models.detection.backbone_utils import resnet_fpn_backbone

# TODO: Fix the pretrain--> can be used in non strict --> easy


class TimmToVisionFPN(nn.Module):
    def __init__(self, backbone):
        super(TimmToVisionFPN, self).__init__()
        self.backbone = backbone
        self.out_channels = 256
        self.in_channels_list = [128, 256, 512, 1024]
        self.fpn = FeaturePyramidNetwork(
            in_channels_list=self.in_channels_list,
            out_channels=self.out_channels,
            extra_blocks=LastLevelMaxPool(),
        )

    def forward(self, x):
        x = self.backbone(x)
        out = OrderedDict()
        for i in range(len(x)-1):
            out[str(i)] = x[i+1]
        out = self.fpn(out)
        return out


class TimmToVision(nn.Module):
    def __init__(self, backbone, out_channels):
        super(TimmToVision, self).__init__()
        self.backbone = backbone
        self.out_channels = out_channels

    def forward(self, x):
        x = self.backbone(x)
        return x


def resnet50_fpn():
    backbone = backbone_utils.resnet_fpn_backbone('resnet50', True)
    return backbone


def calculate_param(model):
    pytorch_total_params = sum(p.numel() for p in model.parameters())
    return pytorch_total_params


def test():

    input = torch.Tensor(2, 3, 832, 928)

    #n = timm.create_model('cspresnet50', features_only=True, pretrained=True)
    #n = timm.create_model('resnet50', features_only=True, pretrained=True)

    # print(m.state_dict().keys())

    m = timm.create_model('LAcspresnet50', features_only=True, pretrained=True, pretrained_strict=False)
    backbone = TimmToVisionFPN(m)
    m = MaskRCNN(backbone, 91)
    print(calculate_param(m))
    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #m = n.to(device)

    #summary(m, input_size=(3, 64, 64))

    # print(n.state_dict().keys())
    # m = TimmToVisionFPN(m)
    # o = m(input)
    # print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGg")
    # for (k, v) in o.items():
    #     print(k, v.shape)

    # m = resnet50_fpn()

    # o = m(input)
    # for (k, v) in o.items():
    #     print(k, v.shape)

    # m = torchvision.models.resnet50(pretrained=False)
    # m = TimmToVisionFPN(m)
    # o = m(input)

    # for (k, v) in o.items():
    #     print(k, v.shape)
    '''
    resnet = torchvision.models.resnet50(pretrained=False)
    in_channels_stage2 = resnet.inplanes // 8
    # print(in_channels_stage2)
    in_channels_list = [
        in_channels_stage2,
        in_channels_stage2 * 2,
        in_channels_stage2 * 4,
        in_channels_stage2 * 8,
    ]
    print(in_channels_list)
    out_channels = 256
    fpn = FeaturePyramidNetwork(
        in_channels_list=in_channels_list,
        out_channels=out_channels,
        extra_blocks=LastLevelMaxPool(),
    )
    return_layers = {'layer1': '0', 'layer2': '1', 'layer3': '2', 'layer4': '3'}
    resnet = torchvision.models.resnet50(pretrained=False)
    resnet = torchvision.models._utils.IntermediateLayerGetter(resnet, return_layers)
    resnet_out = resnet(input)
    for k, v in resnet_out.items():
        print(k, v.shape)

    fpn_out = fpn(resnet_out)
    for k, v in fpn_out.items():
        print(k, v.shape)
    '''
