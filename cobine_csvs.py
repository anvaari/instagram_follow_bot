#this code combine csv files which contain name of account and date them generated into one 1 file with name of accounts
import pandas as pd
def file_l (fname):
    with open(fname) as f:
        count=0
        for line in f:
            count+=1
    pass
    return count

def find_user(name):#function find name of account in name of file which contain name and date created
    start=name.find('_')
    end=name.rfind('.')
    return name[start+1:end]

final_dframe=pd.DataFrame({'Users':[],'Followed':[],'Unfollowed':[],'Follow me?':[]})
with open("name_of_following_csv.txt","r") as file:
    number_of_file=file_len('name_of_following_csv.txt')
    for i in range(number_of_file):
        name=file.readline().rstrip('\n')
        temp_dframe=pd.read_csv(name,usecols=['Users','Followed','Unfollowed','Follow me?'])
        for j in range(len(temp_dframe['Users'])):
            if temp_dframe['Users'][j] not in final_dframe['Users']:
                final_dframe=final_dframe.append(temp_dframe.loc[j],ignore_index=True)
        final_dframe.to_csv("{}.csv".format(find_user(name)))
pass
