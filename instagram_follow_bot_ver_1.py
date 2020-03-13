import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # This module import for sending data to input boxes
from selenium.webdriver.common.action_chains import ActionChains #This module import for using space button for scroll down
from time import sleep, strftime
from random import randint
import pandas as pd

#number of follower is in the form of for example "27,356" this function transform it to int value
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
username='your_username'
password='your_password'
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

find_username = webdriver.find_element_by_name('username')
find_username.send_keys(username)
find_password = webdriver.find_element_by_name('password')
find_password.send_keys(password)

button_login = webdriver.find_element_by_css_selector('.L3NKy > div:nth-child(1)')
button_login.click()

#this piece ignore pop up asking about notifications
sleep(10)
notnow = webdriver.find_element_by_css_selector('button.aOOlW:nth-child(2)')
notnow.click() #comment these last 2 lines out, if you don't get a pop up asking about notifications

#Follow
follow_list = [] #follow the follower of users existed in the list
i_want_follow=int(20/len(follow_list)) #specify total number of account you want to follow
for user in follow_list:
     follow_dict={'Users':[],'Followed':[],'Unfollowed':[],'Follow me?':[]}
     followed_list=pd.read_csv('{}.csv'.format(user)).to_dict('list')['Users']
     webdriver.get('https://www.instagram.com/'+ user + '/')
     sleep(10)
     number_followers=int_followers(webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').get_attribute("title"))
     followers=webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
     followers.click()
     sleep(10)
     i=1
     while i<i_want_follow:#i use while because of its ability to handle decrease of i (in order to put people already followed in loop)
         if i==1
         #this piece scroll down follower windows
             try:
                 webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li[2]/div/div[2]/div[1]/div/div').click()#click on name of account then send space
                 for j in range(int(i_want_follow/3)+1):
                     sleep(2)
                     ActionChains(webdriver).send_keys(Keys.SPACE).perform()
             except:#if name doesnot existed click on second account's name
                 webdriver.get('https://www.instagram.com/'+ user + '/followers/')
                 webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li[2]/div/div[2]/div[1]/div/div').click()
                 for j in range(int(i_want_follow/3)+1):
                     sleep(2)
                     ActionChains(webdriver).send_keys(Keys.SPACE).perform()

         follow_temp=webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a'.format(i)).text #user name of account
         follow_button=webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[2]/button'.format(i))
         if follow_button.text=="Following" and follow_temp not in followed_list:
             follow_dict['Users'].append(follow_temp)
             follow_dict['Followed'].append(1)
             follow_dict['Unfollowed'].append(0)
             follow_dict['Follow me?'].append(0)
             i_want_follow+=1
             i+=1
             continue
         elif follow_temp not in followed_list :
             follow_dict['Users'].append(follow_temp)
             follow_button.click()
             follow_dict['Followed'].append(1)
             follow_dict['Unfollowed'].append(0)
             follow_dict['Follow me?'].append(0)
             i+=1
             sleep(randint(18,25))
         elif follow_temp in followed_list:
             i+=1
             i_want_follow+=1
             continue
     temp_frame=pd.DataFrame(follow_dict)
     file_name='{}_{}.csv'.format(strftime("%Y%m%d-%H%M%S"),user) #creat csv file with name and date
     with open ("name_of_following_csv.txt","a") as file: #insert files name to txt file in order to combine them later
         file.write(file_name+'\n')
     pass
     temp_frame.to_csv(file_name)
