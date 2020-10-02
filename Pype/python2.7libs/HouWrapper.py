#!/usr/bin/python
# -*- coding: utf-8 -*-   
##################################################
# ver 0.4
# author : Junyoung Kim
# houWrapper_nonGUI.py
##################################################
# 메소드 이름 수정
# 클래스 부분 통합 및 축약
##################################################

import os, sys, time, subprocess, PypeCore, platform
from PypeCore import Completer



class setDB():
    """It checks required environments, then collects all of the HOU versions, parses normal and arnold installed versions into the dict type DB."""
    
    def __init__(self):
        if platform.system() == "Windows":
            #TODO: SESI환경변수가 없으면 0으로 리턴이 되니, 예외처리를 해주든가, 경고메세지를 띄우는게 좋을거야
            self.sesi_path = os.getenv("SESI")
            self.htoa_path = os.getenv("HTOA")

            self.checkEnv()
            
            self.versions = self.getVersions(self.sesi_path)

            self.hou_db = self.getHOU(self.versions)
            self.htoa_db = self.getHTOA(self.htoa_path, self.hou_db)

    
    def checkEnv(self):
        try:
            sesi_path = os.environ["SESI"]
        except KeyError:
            print "{}{}".format("Env variable ", "'SESI' is not defined")
              
        try:
            htoa_path = os.environ["HTOA"]
        except KeyError:
            print "{}{}".format("Env variable ", "'HTOA' is not defined")

    
    def getVersions(self, sesi_path):
        dirs = os.listdir(sesi_path)
        versions = []
        for x in dirs:
            versions.append(x.split(" ")[-1])
        return versions

    
    def getHOU(self, versions):
        majors = []
        dic = {}

        for x in versions:
            if x[:4] not in majors:
                majors.append(x[:4])

        for x in majors:
            minors = []
            for y in versions:
                if x in y:
                    minors.append(y.split(".")[2])
            dic[x] = minors
        return dic

    
    def getHTOA(self, htoa_path, hou_db):
        htoa_versions = os.listdir(htoa_path)
        htoa_dic = {}

        dirname = htoa_versions[-1]
        versionTemp = dirname.split("-")[2]
        majorTemp = versionTemp[:4]
        htoa_dic[majorTemp] = [hou_db[majorTemp][-1]]

        return htoa_dic



if __name__ == "__main__":
    #shorten 'class(argument)' form
    setDB = setDB()

    #declare default DB variable
    DB = setDB.hou_db
    
    
    #asking htoa option
    htoa_input = None
    while htoa_input != "y" and htoa_input != "n":

        htoa_input = raw_input("Include arnold? [y/n]: ")

        if htoa_input == "y":
            DB = setDB.htoa_db
        elif htoa_input == "n":
            pass


    # select major version #
    #declare empty key number variable
    major_key_num = None

    while major_key_num not in range(len(DB.keys())):

        majorTemp = {}

        for count, x in enumerate(DB.keys()):
            print '\n{}. {}'.format(count, x)
            majorTemp[count] = x

        major_input = raw_input("\ninput the number of major ver : ")
        major_key_num = int(major_input)

        if major_key_num in range(len(DB.keys())):
            chosenMaj = majorTemp[major_key_num]

    
    # select minor version #
    #declare empty value number variable
    minor_val_num = None

    while minor_val_num not in range(len(DB[chosenMaj])):

        for count, x in enumerate(DB[chosenMaj]):
            print '\n{}. {}'.format(count, x)

        minor_input = raw_input("\ninput the number of minor ver : ")
        minor_val_num = int(minor_input)

        if minor_val_num in range(len(DB[chosenMaj])):
            chosenMin = DB[chosenMaj][minor_val_num]
            runpath = '{}{}{}{}{}\{}'.format(os.getenv('SESI'), "\Houdini ", chosenMaj, ".", chosenMin, "bin\houdinifx.exe")
            print runpath
            subprocess.Popen(runpath)
            exit(0)
