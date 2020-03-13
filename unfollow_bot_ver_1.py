import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, strftime
from random import randint
import pandas as pd

#number of follower in instagram showed in the form of "25,352". this function transform it to integer
def int_followers(str_f):
    comma=str_f.count(',')
    length=len(str_f)-comma
    num=0
    for i in str_f:
        if i==',':
            continue
        num+=int(i)*10**(length-1)
        length-=1
    return num

#introduce firefox to selenium
firefoxdriver_path = 'E:\Tech\Progrmming\python\Instagram bot\Packages\geckodriver-v0.26.0-win64\geckodriver.exe' # Change this to your own firefox path!
webdriver = webdriver.Firefox(executable_path=firefoxdriver_path)
sleep(2)

#Log in to instagram accounts
username='navakco'
password='mja9215'
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)
find_username = webdriver.find_element_by_name(username)
find_username.send_keys(username)
find_password = webdriver.find_element_by_name('password')
find_password.send_keys(password)
button_login = webdriver.find_element_by_css_selector('.L3NKy > div:nth-child(1)')
button_login.click()

#this piece ignore pop up asking about notifications
sleep(10)
notnow = webdriver.find_element_by_css_selector('button.aOOlW:nth-child(2)')
notnow.click() #comment these last 2 lines out, if you don't get a pop up asking about notifications

unfollow_list=[]#users you want to unfollow its followers you followed before
unfollow_exeption=[] #accounts you don't want to be unfollowed at all
for user in unfollow_list:
    followed_dict=pd.read_csv("{}.csv".format(user)).to_dict('list')
    webdriver.get('https://www.instagram.com/'+username+'/')
    number_following=int_followers(webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text)
    following=webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')
    following.click()
    sleep(10)
    for i in range(1,number_following+1):#go to the end of followings list
        if i==1:
            try:
                webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div').click()
                for j in range(int(number_following/3)+1):
                    sleep(2)
                    ActionChains(webdriver).send_keys(Keys.SPACE).perform()
            except:
                pass
                #webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li[2]/div/div[2]/div[2]/div').click()
                #for j in range(int(number_following/3)+1):
                    #sleep(2)
                    #ActionChains(webdriver).send_keys(Keys.SPACE).perform()
        try:
            user_temp=webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a'.format(i)).get_attribute('title')
        except:
            webdriver.get('https://www.instagram.com/gerayeh/')
            following.click()
            webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li[2]/div/div[2]/div[2]/div').click()
            for j in range(int(number_following/3)+1):
                sleep(2)
                ActionChains(webdriver).send_keys(Keys.SPACE).perform()
            user_temp=webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a'.format(i)).get_attribute('title')
        if  user_temp in followed_dict['Users'] and user_temp not in unfollow_exeption:
            webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[2]'.format(i)).click()
            sleep(1)
            webdriver.find_element_by_xpath('/html/body/div[5]/div/div/div[3]/button[1]').click()
            followed_dict['Unfollowed'][followed_dict['Users'].index(user_temp)]=1
            sleep(2)
pd.DataFrame(followed_dict).to_csv('{}.csv'.format(user))
