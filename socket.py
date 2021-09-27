import predictor
import numpy as np
import cv2 as cv
import msvcrt


# 初始化摄像头
cap = cv.VideoCapture(0, cv.CAP_DSHOW)

# 读取图片并识别
def detectImg(imgPath):
    img = cv.imread(imgPath)
    res = predictor.yolo_detect(img)
    return res

# 启动摄像头进行实时检测
def detectVideo():
    while 1:
        ret, frame = cap.read()
        cv.imshow("Camera", predictor.yolo_detect(frame)) # 获取摄像头图像
        key = cv.waitKey(1)
        if key == ord('\x1b'):
            break
    cap.release()
    cv.destroyAllWindows() 

if __name__ == '__main__':
    detectVideo()