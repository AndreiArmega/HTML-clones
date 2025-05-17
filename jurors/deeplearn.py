import sys
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image


if len(sys.argv) != 3:
    print("Usage: python deeplearn.py <image_path1> <image_path2>")
    sys.exit(1)

img_path1 = sys.argv[1]
img_path2 = sys.argv[2]

model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
model = nn.Sequential(*list(model.children())[:-1])  
model.eval()

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

def load_and_process(path):
    img = Image.open(path).convert("RGB")
    return preprocess(img).unsqueeze(0)  

img1 = load_and_process(img_path1)
img2 = load_and_process(img_path2)

with torch.no_grad():
    feat1 = model(img1)
    feat2 = model(img2)

cos = nn.CosineSimilarity(dim=1, eps=1e-6)
similarity = cos(feat1, feat2).item()

print(f"{similarity:.4f}")
