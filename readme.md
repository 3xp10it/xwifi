## xwifi

### Disclaimer


[!] legal disclaimer: Usage of xwifi.py for attacking targets without prior mutual consent is illegal.It is the end user's responsibility to obey all applicable local, state and federal laws.Developers assume no liability and are not responsible for any misuse or damage caused by this program.


### Usage

```
python3 xwifi.py
```

### Requirement


+ 1.macOS[test with:macOS sierra 10.12.3/5]

+ 2.need airport
    macOS sierra系统自带

+ 3.need aircrack-ng
    brew install aircrack-ng

+ 4.need ack
    brew install ack


### About


由于macOS下有2个缺陷:
+ a.aircrack-ng官网说airodump-ng和aireplay-ng在macOS不支持
+ b.新版本的macOS还没找到可利用的wifi破解工具(https://github.com/IGRSoft/KisMac2支持老mac系统)

于是有了本工具,本工具可在新版本macOS上自动破解wifi,适用物理机装mac系统,理论上支持所有版本苹果系统

支持两种破解方法
+ a)aircrack-ng基于字典的破解
+ b)reaver基于wps的破解

可同时运行两个python3 xwifi.py实例,一个选aircrack-ng破解方式,一个选reaver破解方式


### Attention


+ 1.由于macOS下没有找到aireplay-ng的替代品,因此无法主动攻击,本工具采用的是不断sniff并自动检测是否抓到握手包并自动
破解

+ 2.抓到握手包后有两种破解方式:
  + a)aircrack-ng破解
      eg.aircrack-ng -w ......./pass.txt -b 50:bd:5f:6e:3f:44 /tmp/*.cap
      本工具中用这种方式破解
  + b)hashcat破解
      要将cap文件转成hashcat支持的格式再用hashcat破解
      + 1>将https://github.com/hashcat/hashcat-utils/releases里面的cap2hccapx.bin放到kali64(vm)下运行得到hccapx
      + 2>然后再运行eg.hashcat -a 3 -m 2500 output.hccapx ?d?d?d?d?d?d?d?d

+ 3.代码里有个关键操作是主进程里开2个子进程,如果用成2个子线程则无法工作,应该是因为2个不同的分支要执行不同的系统命令,
  系统命令(os.system)要想多分支执行不同的系统命令最好用多进程不能多线程,因为如果某个分支中要执行的系统命令是阻塞式
  的如ping www.baidu.com而不是简单的自行终止的如echo 1,这样的阻塞式的系统命令用多线程来执行会无法达到目的,改成多进程
  就可以了,更多详情如下link中


<a href="https://stackoverflow.com/questions/44402158/how-to-execute-different-system-commands-in-differrent-threads-with-python3">更多详情link</a>
