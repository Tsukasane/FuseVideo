import cv2
import os

def suofang(im, target_height, target_width):
    height, width = im.shape[:2]  # 取彩色图片的长、宽。
    ratio_h = height / target_height
    ration_w = width / target_width
    ratio = max(ratio_h, ration_w)

    # 缩小图像  resize(...,size)--size(width，height)
    size = (int(width / ratio), int(height / ratio))
    shrink = cv2.resize(im, size, interpolation=cv2.INTER_AREA)  # 双线性插值
    WHITE = [255, 255, 255]  # 修改该值可以将放大部分填成任意颜色

    a = 700
    b = 470

    # 原图主体放到右下角
    constant = cv2.copyMakeBorder(shrink, int(b), 0, int(a), 0, cv2.BORDER_CONSTANT, value=WHITE)
    constant = cv2.resize(constant, (target_width, target_height), interpolation=cv2.INTER_AREA)

    return constant

def transparence2white(img):  
    sp = img.shape  # 获取图片维度
    width = sp[0]  # 宽度
    height = sp[1]  # 高度
    for yh in range(height):
        for xw in range(width):
            color_d = img[xw, yh]  # 遍历图像每一个点，获取到每个点4通道的颜色数据
            if (color_d[3] == 0):  # 最后一个通道为透明度，如果其值为0，即图像是透明
                img[xw, yh] = [255, 255, 255, 255]  # 则将当前点的颜色设置为白色，且图像设置为不透明
    return img

def Transform(base_path):
    #hyperparameter
    targetSize = [270, 390]

    base_path = 'test/'
    images = os.listdir(base_path)

    for i_path in images:
        filename = base_path+i_path
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)  # 按原通道数读取图片
        if img.shape[2] == 4:  # RGBA, 需要转为RGB，并填充白色
            img = cv2.imread(filename, -1)
            img = transparence2white(img)  # 此时图片背景已经是白色
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        img = suofang(img, targetSize[0], targetSize[1])
        cv2.imwrite(filename, img)
