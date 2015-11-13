__author__ = 'AJ'
import json, csv, os, requests, urllib, time

def test(i,v):
    date = "today"
    name = "aj"
    return {"date": i, "name": v}



if __name__ == '__main__':
    data_dict = []
    tester = ['a', 'b', 'c', 'd', 'e', 'f', 'g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v'
        ,'w','x','y','z']


    i = 0
    while i < len(tester):
        data_dict.append(test(i,tester[i]))
        i = i + 1
        if len(data_dict) > 3:
           break

    print tester
    print data_dict

