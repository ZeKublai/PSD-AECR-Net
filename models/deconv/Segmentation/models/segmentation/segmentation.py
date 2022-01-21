from torchvision.models._utils import IntermediateLayerGetter
from torchvision.models.utils import load_state_dict_from_url
from .. import resnet,resnetd
from .deeplabv3 import DeepLabHead, DeepLabV3, DeepLabHead_deconv
from .fcn import FCN, FCNHead,FCNHead_deconv


__all__ = ['fcn_resnet50', 'fcn_resnet101', 'deeplabv3_resnet50', 'deeplabv3_resnet101','fcn_resnet50d', 'fcn_resnet101d', 'deeplabv3_resnet50d', 'deeplabv3_resnet101d']


model_urls = {
    'fcn_resnet50_coco': None,
    'fcn_resnet101_coco': 'https://download.pytorch.org/models/fcn_resnet101_coco-7ecb50ca.pth',
    'deeplabv3_resnet50_coco': None,
    'deeplabv3_resnet101_coco': 'https://download.pytorch.org/models/deeplabv3_resnet101_coco-586e9e4e.pth',
}


def _segm_resnet(name, backbone_name, num_classes, aux, pretrained_backbone=True,deconv=False):
    if backbone_name[-1]=='d':
        backbone = resnetd.__dict__[backbone_name](
            pretrained=pretrained_backbone,
            replace_stride_with_dilation=[False, True, True],deconv=deconv,channel_deconv=None)

    else:
        backbone = resnet.__dict__[backbone_name](
            pretrained=pretrained_backbone,
            replace_stride_with_dilation=[False, True, True])

    return_layers = {'layer4': 'out'}
    if aux:
        return_layers['layer3'] = 'aux'
    backbone = IntermediateLayerGetter(backbone, return_layers=return_layers)

    aux_classifier = None
    if aux:
        inplanes = 1024
        if deconv:
            aux_classifier = FCNHead_deconv(inplanes, num_classes,deconv)
        else:        
            aux_classifier = FCNHead(inplanes, num_classes)
    if not deconv:
        print('deconv disabled')
        model_map = {
            'deeplabv3': (DeepLabHead, DeepLabV3),
            'fcn': (FCNHead, FCN),
        }
    else:
        print('deconv enabled')

        model_map = {
            'deeplabv3': (DeepLabHead_deconv, DeepLabV3),
            'fcn': (FCNHead_deconv, FCN),
        }

    inplanes = 2048
    if deconv:
        classifier = model_map[name][0](inplanes, num_classes,deconv)
    else:
        classifier = model_map[name][0](inplanes, num_classes)
    
    base_model = model_map[name][1]

    model = base_model(backbone, classifier, aux_classifier)
    return model


def _load_model(arch_type, backbone, pretrained, progress, num_classes, aux_loss, **kwargs):
    if pretrained:
        aux_loss = True
    model = _segm_resnet(arch_type, backbone, num_classes, aux_loss, **kwargs)
    if pretrained:
        arch = arch_type + '_' + backbone + '_coco'
        model_url = model_urls[arch]
        if model_url is None:
            raise NotImplementedError('pretrained {} is not supported as of now'.format(arch))
        else:
            state_dict = load_state_dict_from_url(model_url, progress=progress)
            model.load_state_dict(state_dict)
    return model


def fcn_resnet50(pretrained=False, progress=True,
                 num_classes=21, aux_loss=None, **kwargs):
    """Constructs a Fully-Convolutional Network model with a ResNet-50 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('fcn', 'resnet50', pretrained, progress, num_classes, aux_loss, **kwargs)


def fcn_resnet101(pretrained=False, progress=True,
                  num_classes=21, aux_loss=None, **kwargs):
    """Constructs a Fully-Convolutional Network model with a ResNet-101 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('fcn', 'resnet101', pretrained, progress, num_classes, aux_loss, **kwargs)


def deeplabv3_resnet50(pretrained=False, progress=True,
                       num_classes=21, aux_loss=None, **kwargs):
    """Constructs a DeepLabV3 model with a ResNet-50 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('deeplabv3', 'resnet50', pretrained, progress, num_classes, aux_loss, **kwargs)


def deeplabv3_resnet101(pretrained=False, progress=True,
                        num_classes=21, aux_loss=None, **kwargs):
    """Constructs a DeepLabV3 model with a ResNet-101 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('deeplabv3', 'resnet101', pretrained, progress, num_classes, aux_loss, **kwargs)


def fcn_resnet50d(pretrained=False, progress=True,
                 num_classes=21, aux_loss=None, **kwargs):
    """Constructs a Fully-Convolutional Network model with a ResNet-50 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('fcn', 'resnet50d', pretrained, progress, num_classes, aux_loss, **kwargs)


def fcn_resnet101d(pretrained=False, progress=True,
                  num_classes=21, aux_loss=None, **kwargs):
    """Constructs a Fully-Convolutional Network model with a ResNet-101 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('fcn', 'resnet101d', pretrained, progress, num_classes, aux_loss, **kwargs)


def deeplabv3_resnet50d(pretrained=False, progress=True,
                       num_classes=21, aux_loss=None, **kwargs):
    """Constructs a DeepLabV3 model with a ResNet-50 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('deeplabv3', 'resnet50d', pretrained, progress, num_classes, aux_loss, **kwargs)


def deeplabv3_resnet101d(pretrained=False, progress=True,
                        num_classes=21, aux_loss=None, **kwargs):
    """Constructs a DeepLabV3 model with a ResNet-101 backbone.

    Args:
        pretrained (bool): If True, returns a model pre-trained on COCO train2017 which
            contains the same classes as Pascal VOC
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _load_model('deeplabv3', 'resnet101d', pretrained, progress, num_classes, aux_loss, **kwargs)
