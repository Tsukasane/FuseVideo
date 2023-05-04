import os
import cv2

file_dir = 'outF/'
ls = []

# manually set the range
for i in range(280): 
    filename = 'poisson_image'+str(i)+'.jpg'
    ls.append(filename)

#print(ls)

video = cv2.VideoWriter('outV.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),30,(1200,900))

for i in range(1,len(ls)):
    img = cv2.imread(file_dir + ls[i-1]) #读取图片

    img = cv2.resize(img,(1200,900)) #将图片转换为1280*720像素大小
    video.write(img) # 写入视频
    
# 释放资源
video.release()
