import PIL
import numpy
from matplotlib import pyplot as plt
import cv2
import os

#需手動分類字母
def getSimpleNum(dirName="fejwebook" or 'foodsave'):
    for i in range(10):
        classpath="../captchaData/" + dirName + "/classification/"
        if not os.path.exists(classpath+str(i)):
            os.makedirs(classpath+str(i))


    captchaDir = "../captchaData/" + dirName + "/rawPic/"
    numDir = "../captchaData/" + dirName + "/numPic/"

    if not os.path.exists(numDir):
        os.makedirs(numDir)

    for i in os.listdir(captchaDir):
        pil_image = PIL.Image.open(captchaDir+i).convert("RGB")
        open_cv_image = numpy.array(pil_image)
        plt.imshow(open_cv_image)
        imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)  # 箱圖片轉換成灰
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)  # 門檻 色彩不夠pass
        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 找到輪廓(contour)
        cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x: x[1])  # 將輪廓由找到的矩形邊界，以第一個值(表示左邊界)排序
        ary = []
        for (c, _) in cnts:  # 將各邊界篩選不要的(寬度過短 高度過短 最外框都不要)
            (x, y, w, h) = cv2.boundingRect(c)
            # print((x,y,w,h))
            if dirName=='fejwebook':
                if h >= 10 and w != 70 and w>8:
                    ary.append((x, y, w, h))
            elif dirName=="foodsave":
                if w > 11 and h >= 7 and w != 120:
                    if x - 2 > 0:
                        ary.append((x - 2, y - 2, w + 4, h + 4))
                    else:
                        ary.append((x, y, w + 4, h + 4))
            else:
                if h >= 9 and w != 130 and w > 10:
                    ary.append((x, y, w, h))
        n = 0
        for (x, y, w, h) in ary:  # 將各邊界截圖 然後存取
            # fig = plt.figure(figsize=(6.4,4.8),dpi=100)
            fig = plt.figure()
            roi = open_cv_image[y:y + h, x:x + w]
            thresh = roi.copy()
            plt.imshow(thresh)
            plt.savefig(numDir+"{}_{}.png".format(i.split(".")[0],n),dpi=100)
            n+=1
            plt.close()



if __name__=="__main__":
    getSimpleNum('foodsave')