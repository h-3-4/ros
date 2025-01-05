import socket
import torch
from torchvision import models, transforms
import torch.nn.functional as F
from PIL import Image
import io

# 定义标签（与训练时的标签一致）
labels = [
    "限速5公里每时","限速15公里每时","限速30公里每时","限速40公里每时","限速50公里每时",
    "限速60公里每时","限速70公里每时","限速80公里每时","禁止直行和左转","禁止直行和右转",
    "禁止直行","禁止左转","禁止左转和右转","禁止右转","禁止超车",
    "禁止掉头","禁止机动车行驶","禁止鸣笛","解除40公里每小时限速","解除50公里每小时限速",
    "允许直行和左转","straight","left","允许左转和右转","right",
    "靠左行驶","靠右行驶","环岛","机动车道","允许鸣笛",
    "非机动车道","允许掉头","左右绕行","注意信号灯","注意危险",
    "注意行人","注意非机动车","前方学校","向右急转弯","向左急转弯",
    "下陡坡","上陡坡","减速慢行","T字路口","T字路口",
    "村庄","反向弯路","无人看守铁道路口","前方施工","连续弯路",
    "有人看守铁道路口","注意安全","停车让行","禁止通行","禁止停车",
    "禁止驶入","减速让行","停车检查"
]

# 图像预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # 调整图像大小为 224x224（ResNet 输入大小）
    transforms.ToTensor(),  # 转换为 Tensor 格式
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 归一化
])

# 加载训练好的模型
model = models.resnet18(pretrained=True)
model.fc = torch.nn.Linear(model.fc.in_features, 58)  # 修改输出类别为58（你的标签数量）
model.load_state_dict(torch.load('C:/Users/user/Desktop/vs.code/python/chinese_traffic/traffic_sign_model.pth'))
model.eval()  # 设置为评估模式

# 设置主机 IP 和端口（需与客户端匹配）
HOST = '0.0.0.0'  # 监听所有接口
PORT = 12345      # 与客户端一致的端口号

# 创建服务器套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server is listening on {HOST}:{PORT}...")

while True:
    # 接受客户端连接
    client_socket, client_address = server_socket.accept()
    print(f"Connected by {client_address}")

    while True:
        # 接收图像数据大小
        img_size = int.from_bytes(client_socket.recv(4), byteorder='big')
        img_data = b''
        while len(img_data) < img_size:
            img_data += client_socket.recv(4096)

        # 将图像数据转换为PIL图像
        image = Image.open(io.BytesIO(img_data))

        # 对图像进行预处理
        img_tensor = transform(image)
        img_tensor = img_tensor.unsqueeze(0)  # 增加批次维度

        # 使用模型进行预测
        with torch.no_grad():
            outputs = model(img_tensor)

        # 使用 softmax 转换为概率
        probabilities = F.softmax(outputs, dim=1)

        # 获取最大概率的类别
        max_prob, predicted = torch.max(probabilities, 1)
        predicted_label = labels[predicted[0]]  # 映射到标签名称

        # 检查最大置信度是否低于 0.6
        if max_prob.item() < 0.6:
            result = "no sign"
        else:
            result = f"{predicted_label} - Confidence: {max_prob.item():.4f}"

        # 发送预测结果回客户端
        client_socket.sendall(result.encode('utf-8'))

    client_socket.close()
