from torchvision.models.detection.faster_rcnn import FasterRCNN
from torchvision.models.detection.anchor_utils import AnchorGenerator
from torchvision.models import MobileNet_V3_Large_Weights
from torchvision.models.detection.backbone_utils import mobilenet_backbone


class FRCNNMobileNetV3Large(FasterRCNN):
    """
    Based on: 
    https://github.com/pytorch/vision/blob/f7b1cfa8f7e10e0c157da6e55dc6f0237397faec/torchvision/models/detection/faster_rcnn.py#L683
    
    NOTE that depending on the backbone used, the FasterRCNN class init is done differently.
    """

    def __init__(self, num_classes=91, **kwargs):
        backbone = mobilenet_backbone(
            backbone_name="mobilenet_v3_large",
            fpn=True,
            weights=MobileNet_V3_Large_Weights.IMAGENET1K_V2,
        )

        anchor_sizes = (
            (
                32,
                64,
                128,
                256,
                512,
            ),
        ) * 3
        aspect_ratios = ((0.5, 1.0, 2.0),) * len(anchor_sizes)

        super(FRCNNMobileNetV3Large, self).__init__(
            backbone,
            num_classes,
            rpn_anchor_generator=AnchorGenerator(anchor_sizes, aspect_ratios),
            **kwargs
        )
