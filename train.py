import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
from tqdm import tqdm  # 导入 tqdm 库

# 数据集类
class TrafficSignDataset(Dataset):
    def __init__(self, annotation_file, image_dir, transform=None):
        self.image_paths = []
        self.labels = []

        # 读取注释文件
        with open(annotation_file, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                
                # 检查行内的字段数目是否正确
                if len(parts) < 8:  # 必须包含至少 8 个字段
                    print(f"Warning: Skipping invalid line (incorrect number of fields): {line}")
                    continue

                image_path = parts[0]  # 图片路径
                try:
                    label = int(parts[-2])  # 标签位于倒数第二位
                except ValueError:
                    print(f"Warning: Invalid label value (skipping): {line}")
                    continue

                # 收集图片路径和标签
                self.image_paths.append(image_path)
                self.labels.append(label)

        # 打印出一些调试信息
        print(f"Loaded {len(self.image_paths)} samples.")
        if len(self.image_paths) > 0:
            print(f"Example image path: {self.image_paths[0]}")
            print(f"Example label: {self.labels[0]}")

        self.image_dir = image_dir
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = os.path.join(self.image_dir, self.image_paths[idx])
        
        # 检查图像是否存在
        if not os.path.exists(image_path):
            print(f"Warning: Image {image_path} not found!")
            return None, None
        
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
annotation_file = 'C:/Users/user/Desktop/vs.code/python/chinese_traffic/TsignRecgTrain4170Annotation.txt'
image_dir = 'C:/Users/user/Desktop/vs.code/python/chinese_traffic/tsrd-train'

train_dataset = TrafficSignDataset(
    annotation_file=annotation_file,
    image_dir=image_dir,
    transform=transform
)

# 确保数据集加载成功
print(f"Train dataset size: {len(train_dataset)}")

# 如果数据集为空，终止训练
if len(train_dataset) == 0:
    raise ValueError("No data found. Please check the dataset paths and labels.")

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 模型构建（使用预训练的ResNet18模型）
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 58)  # 修改输出类别为58，全连接层58类

# 损失函数和优化器
criterion = nn.CrossEntropyLoss() #损失函数CrossEntropyLoss(),适合多分类问题
optimizer = optim.Adam(model.parameters(), lr=0.001) #优化器Adam，学习率0.001

# 确定设备（使用 GPU 如果可用，否则使用 CPU）
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)  # 将模型移到设备上

# 训练模型
num_epochs = 10 #训练10轮
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    # 使用 tqdm 显示进度条
    with tqdm(train_loader, unit='batch', desc=f"Epoch {epoch+1}/{num_epochs}") as tepoch:
        for images, labels in tepoch:
            # 跳过无效的数据（如果读取时失败）
            if images is None or labels is None:
                continue

            images = images.to(device)  # 将数据移到设备上
            labels = labels.to(device)  # 将标签移到设备上

            optimizer.zero_grad() #清除之前计算的梯度
            outputs = model(images) #前向传播，通过模型得到预测结果
            loss = criterion(outputs, labels) #计算损失
            loss.backward() #反向传播，计算梯度
            optimizer.step() #更新模型参数

            # 累积损失和正确预测的样本数
            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1) # 获取预测的类别标签
            total += labels.size(0) #总样本数
            correct += (predicted == labels).sum().item() # 统计正确预测的数量

            # 更新进度条描述信息
            tepoch.set_postfix(loss=running_loss / (total / 32), accuracy=100 * correct / total)

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}, Accuracy: {100 * correct / total:.2f}%')

# 保存模型
torch.save(model.state_dict(), 'traffic_sign_model.pth')
