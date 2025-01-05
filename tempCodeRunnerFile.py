import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
from tqdm import tqdm  # 导入 tqdm，用于显示进度条

# 数据集类
class TrafficSignDataset(Dataset):
    def __init__(self, annotation_file, image_dir, transform=None):
        self.image_paths = []
        self.labels = []
        with open(annotation_file, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                image_path = parts[0]
                label = int(parts[1])  # 假设标签是整型
                self.image_paths.append(image_path)
                self.labels.append(label)
        
        self.image_dir = image_dir
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = os.path.join(self.image_dir, self.image_paths[idx])
        image = Image.open(image_path)
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)
        
        return image, label

# 数据预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 创建数据集和数据加载器
train_dataset = TrafficSignDataset(
    annotation_file='C:/Users/user/Desktop/vs.code/python/chinese_traffic/TsignRecgTrain4170Annotation.txt',
    image_dir='C:/Users/user/Desktop/vs.code/python/chinese_traffic/TSRD-train',
    transform=transform
)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 模型构建（使用预训练的ResNet18模型）
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 57)  # 假设有43种交通标志类别

# 损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 确定设备（使用 GPU 如果可用，否则使用 CPU）
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)  # 将模型移到设备上

# 训练模型
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    # 使用 tqdm 显示进度条
    with tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs}', unit='batch') as pbar:
        for images, labels in pbar:
            images = images.to(device)  # 将数据移到设备上
            labels = labels.to(device)  # 将标签移到设备上

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            # 更新进度条显示信息
            pbar.set_postfix(loss=running_loss/len(pbar), accuracy=100 * correct / total)

    # 每个 epoch 结束时打印结果
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}, Accuracy: {100 * correct / total:.2f}%')

# 保存模型
torch.save(model.state_dict(), 'traffic_sign_model.pth')
