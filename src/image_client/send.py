#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import socket
import cv2
import struct
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist  # 导入 Twist 消息类型

# 设置默认编码为 UTF-8
reload(sys)
sys.setdefaultencoding('utf-8')

# 设置主机 IP 和端口（需与服务器端匹配）
HOST = '192.168.56.1'  # 主机 IP 地址（根据实际情况修改）
PORT = 12345           # 与服务器端一致的端口号

# 初始化 ROS 节点
rospy.init_node('camera_client_node', anonymous=True)

# 创建 CvBridge 对象
bridge = CvBridge()

# 创建图像发布者
image_pub = rospy.Publisher('/camera/image_raw', Image, queue_size=10)

# 创建套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 尝试连接到服务器
try:
    client_socket.connect((HOST, PORT))
    rospy.loginfo("成功连接到服务器 {}:{}".format(HOST, PORT))
except socket.error as e:
    rospy.logerr("连接服务器失败: {}".format(e))
    exit()

# 打开摄像头
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    rospy.logerr("无法打开摄像头")
    client_socket.close()
    exit()

# 创建 /cmd_vel 话题的发布者
cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

# 持续识别和控制小车运动
while not rospy.is_shutdown():
    # 捕获摄像头图像
    ret, frame = cap.read()
    if not ret:
        rospy.logerr("无法读取摄像头图像")
        break

    # 将图像从 OpenCV 格式转换为 ROS 图像消息
    try:
        ros_image = bridge.cv2_to_imgmsg(frame, "bgr8")
        image_pub.publish(ros_image)  # 发布图像消息
    except CvBridgeError as e:
        rospy.logerr("CvBridge 错误: %s", e)

    # 图像编码为 JPEG 格式
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_data = img_encoded.tobytes()

    # 发送图像大小，4字节
    client_socket.sendall(struct.pack('!I', len(img_data)))  # 发送图像大小
    client_socket.sendall(img_data)  # 发送图像数据

    # 接收服务器返回的预测结果
    try:
        result = client_socket.recv(1024).decode('utf-8')
        rospy.loginfo("Prediction result: {}".format(result))

        # 根据预测结果控制小车
        linear_x = 0.0
        angular_z = 0.0
        if "straight" in result:
            linear_x = 0.2
        elif "left" in result:
            linear_x = 0.1
            angular_z = 0.5
        elif "right" in result:
            linear_x = 0.1
            angular_z = -0.5
        elif "no sign" in result:
            angular_z = 0.1  # 假设没有识别到标识时进行旋转
        else:
            rospy.logwarn("未知的预测结果: %s", result)

        # 发布小车运动命令
        twist = Twist()  # 创建 Twist 消息
        twist.linear.x = linear_x
        twist.angular.z = angular_z

        # 发布到 /cmd_vel 话题
        cmd_vel_pub.publish(twist)

    except socket.error as e:
        rospy.logerr("接收预测结果失败: %s", e)

    # 显示摄像头图像
    cv2.imshow("Camera Feed", frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源并关闭连接
cap.release()
client_socket.close()
cv2.destroyAllWindows()


