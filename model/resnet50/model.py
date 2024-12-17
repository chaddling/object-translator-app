from torchvision.models.detection.faster_rcnn import FasterRCNN
from torchvision.models.detection.backbone_utils import resnet_fpn_backbone


class FRCNNResnet50(FasterRCNN):
    """
    Taken from:
    https://github.com/pytorch/serve/blob/master/examples/object_detector/fast-rcnn/model.py

    Simplest example of FasterRCNN initialization.
    """

    def __init__(self, num_classes=91, **kwargs):
        backbone = resnet_fpn_backbone("resnet50", True)
        super(FRCNNResnet50, self).__init__(backbone, num_classes, **kwargs)
