import torch

from mobilenet_v3_large.model import FRCNNMobileNetV3Large

if __name__ == "__main__":
    model = FRCNNMobileNetV3Large()
    model.fasterrcnn.load_state_dict(torch.load("./mobilenet_v3_large/fasterrcnn_mobilenet_v3_large_fpn-fb6a3cc7.pth", weights_only=False))
    jit_model = torch.jit.script(model)

    torch.jit.save(jit_model, "./mobilenet_v3_large/fasterrcnn_mobilenet_v3_large_fpn-fb6a3cc7-jit.pt")