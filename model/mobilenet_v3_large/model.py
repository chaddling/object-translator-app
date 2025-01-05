import torch
import warnings

from torch import Tensor
from torchvision.models.detection.faster_rcnn import FasterRCNN
from torchvision.models.detection.anchor_utils import AnchorGenerator
from torchvision.models import MobileNet_V3_Large_Weights
from torchvision.models.detection.backbone_utils import mobilenet_backbone
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple, Union


class FRCNNMobileNetV3Large(torch.nn.Module):
    """
    Based on:
    https://github.com/pytorch/vision/blob/f7b1cfa8f7e10e0c157da6e55dc6f0237397faec/torchvision/models/detection/faster_rcnn.py#L683

    NOTE that depending on the backbone used, the FasterRCNN class init is done differently.
    """

    def __init__(self, num_classes=91, **kwargs):
        super().__init__()
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

        self.fasterrcnn = FasterRCNN(
            backbone,
            num_classes,
            rpn_anchor_generator=AnchorGenerator(anchor_sizes, aspect_ratios),
            **kwargs
        )


    def forward(self, image: Tensor) -> List[Dict[str, Tensor]]:
        images = [torch.squeeze(image, dim=0)]

        if torch.jit.is_scripting():
            _, detections = self.fasterrcnn(images, None)
        else:
            detections =  self.fasterrcnn(images, None)

        return detections

    # def forward(self, images: Union[Tensor, List[Tensor]], targets: Optional[List[Dict[str, Tensor]]] = None)  -> List[Dict[str, Tensor]]:
    #     if isinstance(images, Tensor):
    #         images = [torch.squeeze(images, dim=0)]
        
    #     if self.training:
    #         if targets is None:
    #             torch._assert(False, "targets should not be none when in training mode")
    #         else:
    #             for target in targets:
    #                 boxes = target["boxes"]
    #                 if isinstance(boxes, torch.Tensor):
    #                     torch._assert(
    #                         len(boxes.shape) == 2 and boxes.shape[-1] == 4,
    #                         f"Expected target boxes to be a tensor of shape [N, 4], got {boxes.shape}.",
    #                     )
    #                 else:
    #                     torch._assert(False, f"Expected target boxes to be of type Tensor, got {type(boxes)}.")

    #     original_image_sizes: List[Tuple[int, int]] = []
    #     for img in images:
    #         val = img.shape[-2:]
    #         torch._assert(
    #             len(val) == 2,
    #             f"expecting the last two dimensions of the Tensor to be H and W instead got {img.shape[-2:]}",
    #         )
    #         original_image_sizes.append((val[0], val[1]))

    #     images, targets = self.transform(images, targets)

    #     # Check for degenerate boxes
    #     # TODO: Move this to a function
    #     if targets is not None:
    #         for target_idx, target in enumerate(targets):
    #             boxes = target["boxes"]
    #             degenerate_boxes = boxes[:, 2:] <= boxes[:, :2]
    #             if degenerate_boxes.any():
    #                 # print the first degenerate box
    #                 bb_idx = torch.where(degenerate_boxes.any(dim=1))[0][0]
    #                 degen_bb: List[float] = boxes[bb_idx].tolist()
    #                 torch._assert(
    #                     False,
    #                     "All bounding boxes should have positive height and width."
    #                     f" Found invalid box {degen_bb} for target at index {target_idx}.",
    #                 )

    #     features = self.backbone(images.tensors)
    #     if isinstance(features, torch.Tensor):
    #         features = OrderedDict([("0", features)])
    #     proposals, proposal_losses = self.rpn(images, features, targets)
    #     detections, detector_losses = self.roi_heads(features, proposals, images.image_sizes, targets)
    #     detections = self.transform.postprocess(detections, images.image_sizes, original_image_sizes)  # type: ignore[operator]

    #     losses = {}
    #     losses.update(detector_losses)
    #     losses.update(proposal_losses)

    #     if torch.jit.is_scripting():
    #         # warnings.warn(f"{detections[0].keys()}")
    #         if not self._has_warned:
    #             warnings.warn("RCNN always returns a (Losses, Detections) tuple in scripting")
    #             self._has_warned = True
    #         return losses, detections # NOTE THIS DOESNT WORK WITH THE EXISTING HANDLER
    #     else:
    #         return self.eager_outputs(losses, detections) # NOTE THIS ONLY RETURNS `detections` in inference