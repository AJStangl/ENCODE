__author__ = 'AJ'
import json, csv, os, requests, urllib, time

def test(i,name):
    date = "today"
    name
    return {"exp": i, "name": name}



if __name__ == '__main__':
    data_dict = []
    sub_dir = 'C:\Users\AJ\PycharmProjects\Encode\Testing_Center\jsons'
    file_list = os.listdir('C:\Users\AJ\PycharmProjects\Encode\Testing_Center\jsons')

    while len(file_list) != 0:
        file_list = os.listdir('C:\Users\AJ\PycharmProjects\Encode\Testing_Center\jsons')
        print "Current File List"
        print file_list
        for i in range(len(file_list)):
            data_dict.append((i, file_list[i]))
            os.remove(sub_dir+'/'+file_list[i])
            if len(data_dict) > 3:
                print "Current Data Dict"
                print data_dict
                data_dict = []
                break


