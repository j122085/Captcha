from sklearn.externals import joblib
from matplotlib import pyplot as plt
import os
import PIL
import requests
import numpy
import cv2
import time
from sklearn.preprocessing import StandardScaler #數值標準化

def test(dirName="fejwebook" or 'foodsave',url="https://ftracebook.fda.gov.tw/ImageCode.aspx"):
    modelDir=r"../captchaData/"+dirName+"/model/"
    mlp=joblib.load(modelDir+'captcha.pkl')
    fig =plt.figure(figsize=(20,20))
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1,hspace=0.05,wspace=0.05)
    testDir=r"../captchaData/"+dirName+"/test/"
    if not os.path.exists(testDir):
        os.makedirs(testDir)
    N=0
    while N!=4:
        res=requests.get(url)
        with open(testDir+"test.png",'wb') as f:
            f.write(res.content)

        pil_image = PIL.Image.open(testDir+"test.png").convert("RGB")
        open_cv_image = numpy.array(pil_image)
        plt.imshow(open_cv_image)
        imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x: x[1])
        ary = []
        for (c, _) in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            #         print((x,y,w,h))
            if dirName=='fejwebook':
                if h >= 10 and w != 70 and w>8:
                    ary.append((x, y, w, h))
            elif dirName=="foodsave":
                if w > 11 and h >= 7 and w != 120:
                    if x - 2 > 0:
                        ary.append((x - 2, y - 2, w + 4, h + 4))
                    else:
                        ary.append((x, y, w + 4, h + 4))

        N=len(ary)
        print(N)

    n = 0

    testNumDir=testDir+"numPic/"
    if not os.path.exists(testNumDir):
        os.makedirs(testNumDir)

    for i in os.listdir(testNumDir):
        os.remove(testNumDir + i)

    for (x, y, w, h) in ary:
        fig = plt.figure()
        roi = open_cv_image[y:y + h, x:x + w]
        thresh = roi.copy()
        #     ax=fig.add
        plt.imshow(thresh)
        plt.savefig(testNumDir+"test_{}.png".format(n), dpi=100)
        n += 1

    data = []
    basewidth = 50
    fig = plt.figure(figsize=(20, 20))
    cnt = 0
    for idx, img in enumerate(os.listdir(testNumDir)):
        pil_image = PIL.Image.open(testNumDir+"{}".format(img)).convert('1')
        wpercent = (basewidth / float(pil_image.size[0]))
        hsize = int((float(pil_image.size[1]) * float(wpercent)))
        img = pil_image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        data.append([pixel for pixel in iter(img.getdata())])

    scaler = StandardScaler()
    scaler.fit(data)
    data_scaled = scaler.transform(data)

    print(mlp.predict(data_scaled))

    result="".join(mlp.predict(data_scaled)).replace("xx", "")
    print(result)

    with open(testDir + "{}.png".format(result), 'wb') as f:
        f.write(res.content)

if __name__=="__main__":
    for i in range(10):
        test("fejwebook")
    # test('foodsave','https://waste.epa.gov.tw/export/include/CAPTCHA/CAPTCHA_image.asp?8987')