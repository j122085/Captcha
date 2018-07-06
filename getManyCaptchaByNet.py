import concurrent.futures
import requests
import os

def getCaptchaPic(i,url="https://ftracebook.fda.gov.tw/ImageCode.aspx",dirName="fejwebook" or 'foodsave'):
    res = requests.get(url)
    mydir=r"../captchaData/"+dirName+"/rawPic/"
    if not os.path.exists(mydir):
        os.makedirs(mydir)
    with open(mydir + str(i) + ".png", 'wb') as f:
        f.write(res.content)

def highSpeedGet(n=500,url="https://ftracebook.fda.gov.tw/ImageCode.aspx",dirName="default",maxWorker=20):
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorker) as executor:
        graph = [executor.submit(getCaptchaPic, i,url,dirName) for i in range(n)]




if __name__=="__main__":
    highSpeedGet(50, "https://ftraceadmin.fda.gov.tw/captcha.ashx?w=130&h=33&0.19502310285632518", "foodsave")

