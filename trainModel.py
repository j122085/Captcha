import os
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPClassifier
import numpy
import PIL
from sklearn.preprocessing import StandardScaler #數值標準化
from sklearn.externals import joblib


def trainModel(dirName="fejwebook" or 'foodsave'):
    digits=[]
    labels=[]
    basewidth=50 #寬度全變50
    fig=plt.figure(figsize=(20,20))
    cnt=0
    #畫圖用
    # fig.subplots_adjust(left=0,right=1,bottom=0,top=1,hspace=0.05,wspace=0.05)
    for i in os.listdir("../captchaData/" + dirName + "/classification"):
        if os.path.isdir("../captchaData/" + dirName + "/classification/"+i):
            for img in os.listdir("../captchaData/" + dirName + "/classification/{}/".format(i)):
                pil_image=PIL.Image.open("../captchaData/" + dirName + "/classification/{}/{}".format(i,img)).convert('1')
                wpercent=(basewidth/float(pil_image.size[0])) #寬度全變50 找到寬度跟原本的比例
                hsize=int((float(pil_image.size[1])*float(wpercent))) #找到高度比例
                img=pil_image.resize((basewidth,hsize),PIL.Image.ANTIALIAS) #將高度也變成一樣比例
                #畫圖用
                try:
                    ax=fig.add_subplot(10,12,cnt+1,xticks=[],yticks=[])
                    ax.imshow(img,cmap=plt.cm.binary,interpolation='nearest')
                    ax.text(0,7,str(i),color='red',fontsize=20)
                except:
                    pass
                cnt+=1
                digits.append([pixel for pixel in iter(img.getdata())])#將資料變成一為矩陣 變成data
                labels.append(i) #資料夾名稱變成label
    digit_ary=numpy.array(digits)
    #數值標準化
    scaler =StandardScaler()
    scaler.fit(digit_ary)
    X_scaled=scaler.transform(digit_ary)
    #訓練開始
    mlp=MLPClassifier(hidden_layer_sizes=(80,80,80),activation="logistic",max_iter=3000)
    mlp.fit(X_scaled,labels)
    #存取model
    if not os.path.exists("../captchaData/" + dirName + "/model/"):
        os.makedirs("../captchaData/" + dirName + "/model/")
    joblib.dump(mlp,"../captchaData/" + dirName + "/model/captcha.pkl")

if __name__=="__main__":
    trainModel("fejwebook")
    # trainModel('foodsave')
    print("finish")