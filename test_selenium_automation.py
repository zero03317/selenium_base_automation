from seleniumbase import BaseCase
import subprocess
from time import sleep
import re
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import spur
from hurry.filesize import size
import ftplib
import socket
import easywebdav
import shutil
import os
from deepdiff import DeepDiff
import pytest

nasip="xxx"
computerip="xxxx"

def dict_compare(d1, d2):
    result=DeepDiff(d1,d2)
    if result=={}:
        print "Nic mapping pass"
        return True
    else:
        print"Nic mapping false"
        print result
        return False

def string_compare(fwdate, system_time):
    if fwdate == system_time:
        return True
    else:
        return False
def samba_check_function(service_name,source,destination):
    try:
        shutil.copy(source, destination) # complete target filename given
        print str(service_name)+" copy final"
    except IOError,e:
        print str(service_name)+" can't connact"
    statinfo = os.stat(destination)
    filesize=statinfo.st_size
    kb_to_gb=size(filesize)
    if kb_to_gb=="1G":
        print "check file size="+kb_to_gb
        return True
    else:
        print "check file false~"
        return False

def uploadFile(dir_ftp, filename_ftp, filepath_local, host, port, username, password):

    if not os.path.exists(filepath_local):
        print 'can not find the source file'
        return False
    # connect
    try:
        f = ftplib.FTP()
        f.connect(host=host, port=port)
    except (socket.error, socket.gaierror), e:
        print '----ERROR:cannot reach ' + host
        print e
        return False
    # login
    try:
        f.login(user=username, passwd=password)
    except ftplib.error_perm, e:
        print '----ERROR:cannot login to server ' + host
        print e
        f.quit()
        return False
    print '****Logged in as ' + username + ' to server ' + host
    # change folder
    try:
        f.cwd(dir_ftp)
    except ftplib.error_perm, e:
        print '----ERROR:cannot CD to %s on %s' % (dir_ftp, host)
        print e
        f.quit()
        return False
    print '**** changed to %s folder on %s' % (dir_ftp, host)
    # upload file
    try:
        f.storbinary('STOR ' + filename_ftp, open(filepath_local, 'rb'))
    except ftplib.error_perm, e:
        print '----ERROR:cannot write %s on %s' % (filename_ftp, host)
        print e
        return False
    else:
        print '****Uploaded ' + filepath_local + ' to ' + host + ' as ' \
              + os.path.join(dir_ftp, filename_ftp)
        f.quit()
        return True

def getServerFile(dir_ftp, filename, host, port, username, password):
    if os.path.exists(filename):
        print '****the file ' + filename + ' has already exist! The file will be over writed'
    # connect
    try:
        f = ftplib.FTP()
        f.connect(host=host, port=port)
    except (socket.error, socket.gaierror), e:
        print '----ERROR:cannot reach ' + host
        print e
        return False
    # login
    try:
        f.login(user=username, passwd=password)
    except ftplib.error_perm, e:
        print '----ERROR:cannot login to server ' + host
        print e
        f.quit()
        return False
    print '****Logged in as ' + username + ' to server ' + host
    # change folder
    try:
        f.cwd(dir_ftp)
    except ftplib.error_perm, e:
        print '----ERROR:cannot CD to %s on %s' % (dir_ftp, host)
        print e
        f.quit()
        return False
    print '**** changed to %s folder on %s' % (dir_ftp, host)
    # get file
    try:
        f.retrbinary('RETR %s' % filename, open(filename, 'wb').write)
    except ftplib.error_perm, e:
        print '----ERROR:cannot read file %s on %s' % (filename, host)
        print e
        os.unlink(filename)
        return False
    else:
        print '****Downloaded ' + filename + ' from ' + host + ' to ' + os.getcwd()
        f.quit()
        return True

def get_ip_address():
    # ip adjustment
    for i in range(1, 10):
        proc = subprocess.Popen(
            'c:\Users\N269-01\Desktop\slp\slptool.exe findsrvs service:raid.xxxx ("mac=xxxxx")',
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        tmp = proc.stdout.read()
        if tmp == "":
            print "slp can't fond ip"
            sleep(30)
            continue
        else:
            ipresult = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', tmp).group()
            print "slp find ip address = " + str(ipresult)
            break
    return ipresult

def ping_host(ip):
    hostname = ip
    output = subprocess.Popen(["ping.exe", hostname], stdout=subprocess.PIPE).communicate()[0]

    print(output)

    if ('unreachable' in output):
        print("host Offline")
        return False
    else:
        print "host alive"
        return True

def webdav_tranfer():
    webdav = easywebdav.connect(
        host=nasip,
        username='admin',
        port=50000,
        protocol="http",
        password='1234')
    try:
        print "Webdav start uploadn & download......"
        web_cd = webdav.cd("/f0")
        # print webdav._get_url("")
        # print webdav.ls()
        # print webdav.exists("/dav/test.py")
        # print webdav.exists("ECS.zip")
        # print webdav.download(_file, "./"+_file)
        webdav_upload_status = webdav.upload("E:/service/webdav.txt", "webdav.txt")
        if webdav_upload_status == None:
            print "webdav upload success"
        else:
            print "webdav upload fail!!"
        webdav_download_status = webdav.download('/f0/webdav.txt',
                                                 'C:/Users/N269-01/Desktop/service_download/webdav.txt')
        if webdav_download_status == None:
            print "webdav download success"

        else:
            print "webdav download fail!!"
        return True
    except Exception as error:
        print error
        return False

def dict_compare(d1, d2):
    result = DeepDiff(d1, d2)
    if result == {}:
        print "Nic mapping pass"
        return True
    else:
        print"Nic mapping false"
        print result
        return False

#-----------------------------------------function part-----------------------
class MyTestClass(BaseCase):

    def element_clickable(self,message, path):
        for i in range(1, 10):
            try:
                start_time = time.time()
                element=self.wait_for_element_present(path,timeout=10)
                sleep(2)
                self.highlight(element)
                element.click()
                end_time = time.time()
                waste_time = end_time - start_time
                print message + " " + "time=" + str(waste_time) + "second."
                return True
                break  # it will break from the loop once the specific element will be present.
            except TimeoutException:
                print "Loading took too much time!-Try again"
                continue
        return False

    def wait_element(self,message, path):
        for i in range(1, 5):
            try:
                start_time = time.time()
                element = self.wait_for_element_visible(path,timeout=10)
                self.highlight(element)
                print message
                return True
                break  # it will break from the loop once the specific element will be present.
            except Exception:
                print "Loading took too much time! "
                sleep(5)
                continue
        return False

    def wait_element_click(self,message, path):
        for i in range(1, 10):
            try:
                start_time = time.time()
                element = self.wait_for_element_present(path,timeout=10)
                self.highlight(element)
                element.click()
                end_time = time.time()
                waste_time = end_time - start_time
                print message + " " + "time=" + str(waste_time) + "second."
                return True
                break  # it will break from the loop once the specific element will be present.
            except TimeoutException:
                print "Loading took too much time!-Try again"
        return False

    def wait_element_send(self,message, word, path):
        for i in range(1, 10):
            try:
                start_time = time.time()
                element = self.wait_for_element_visible(path,timeout=10)
                self.highlight(element)
                element.send_keys(word)
                end_time = time.time()
                waste_time = end_time - start_time
                print message + " " + "time=" + str(waste_time) + "second."
                break  # it will break from the loop once the specific element will be present.
            except TimeoutException:
                print "Loading took too much time!-Try again"
                continue

    def wait_element_send_clear(self,message, word, path):
        for i in range(1, 10):
            try:
                start_time = time.time()
                element = self.wait_for_element_visible(path,timeout=10)
                self.highlight(element)
                element.clear()
                element.send_keys(word)
                end_time = time.time()
                waste_time = end_time - start_time
                print message + " " + "time=" + str(waste_time) + "second."
                break  # it will break from the loop once the specific element will be present.
            except TimeoutException:
                print message + "Loading took too much time!-Try again"
                continue

    def login_page_frist_time(self):
        for i in range(1, 10):
            try:
                ip = get_ip_address()
                start_time = time.time()
                self.open("http://" + str(ip) + ":13080")
                element = self.wait_for_element_present("//input[@id='username']", timeout=10)
                self.highlight(element)
                element.send_keys("admin")

                element1 = self.wait_for_element_present("//input[@id='password']", timeout=10)
                self.highlight(element1)
                element1.send_keys("1234")

                element2 = self.wait_for_element_present("//button[@id='loginbtn']", timeout=10)
                self.highlight(element2)
                element2.click()
                # element3=WebDriverWait(driver, 10).until(
                #    EC.visibility_of_element_located((By.XPATH, "//button[@id='loginbtn']"))
                # )
                # element3.click()
                # wait_tutorials
                self.element_clickable("tutorials start", "//div[2]/div/div/div/div/div[2]/div/div/a/span/span/span[2]")
                self.element_clickable("tutorials next button", "//div[2]/a[2]/span/span/span[2]")
                self.element_clickable("tutorials next button", "//div[2]/a[2]/span/span/span[2]")
                self.element_clickable("tutorials next button", "//div[2]/a[2]/span/span")
                self.element_clickable("tutorials next button", "//div[2]/a[2]/span/span/span[2]")
                self.element_clickable("tutorials next button", "//div[2]/a[2]/span/span/span[2]")
                self.element_clickable("tutorials next button", "//div[2]/a[2]/span/span")
                tutorials_final = self.element_clickable("tutorials final button",
                                                    "//div[2]/div/div/div/div/div[3]/div/div/a/span/span/span[2]")
                if tutorials_final == True:
                    end_time = time.time()
                    waste_time = end_time - start_time
                    print "Loading login page success!!!" + str(waste_time) + "second."
                    return True
                    break  # it will break from the loop once the specific element will be present.
            except TimeoutException:
                print "Loading........."
                sleep(10)
                continue
        return False

    def css_sele_clickable(self,message, css):
        for i in range(1, 10):
            try:
                start_time = time.time()
                element = self.wait_for_element_visible(css,timeout=10)
                self.highlight(element)
                sleep(3)
                element.click()
                end_time = time.time()
                waste_time = end_time - start_time
                print message + " " + "time=" + str(waste_time) + "second."
                return True
                break  # it will break from the loop once the specific element will be present.
            except TimeoutException:
                print "Loading took too much time!-Try again"
                continue
        return False

    def highlight(self,element):
        """Highlights (blinks) a Selenium Webdriver element"""
        self = element._parent

        def apply_style(s):
            self.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                  element, s)

        original_style = element.get_attribute('style')
        apply_style("background: yellow; border: 2px solid red;")
        time.sleep(.3)
        apply_style(original_style)

    def login_admin(self):
        for i in range(1, 10):
            try:
                ip = get_ip_address()
                start_time = time.time()
                self.open("http://" + str(ip) + ":13080")
                element=self.wait_for_element_present("//input[@id='username']",timeout=10)
                self.highlight(element)
                element.send_keys("admin")

                element1=self.wait_for_element_present("//input[@id='password']",timeout=10)
                self.highlight(element1)
                element1.send_keys("1234")

                element2=self.wait_for_element_present("//button[@id='loginbtn']",timeout=10)
                self.highlight(element2)
                element2.click()
                for i in range(1, 10):
                    try:
                        element3 = self.wait_for_element_visible("//span[@id='button-ControlPanel-btnInnerEl']/div/div/img",timeout=10)
                        self.highlight(element3)
                        sleep(3)
                        boelement3 = bool(element3)
                        element3.click()
                        if boelement3 == True:
                            print "Login webUI success!!"
                            return True
                            break
                    except TimeoutException:
                        print "Find control panel again!"
                        sleep(5)
                        continue
                break
            except TimeoutException:
                print "Login webui again"
                sleep(5)
                continue

    def login_second(self):
        for i in range(1, 10):
            try:
                ip = get_ip_address()
                start_time = time.time()
                self.open("http://" + str(ip) + ":13080")
                for i in range(1, 10):
                    try:
                        element3=self.wait_for_element_visible("//span[@id='button-ControlPanel-btnInnerEl']/div/div/img",timeout=10)
                        sleep(3)
                        boelement3 = bool(element3)
                        element3.click()
                        if boelement3 == True:
                            print "Login webUI success!!"
                            return True
                            break
                    except TimeoutException:
                        print "Find control panel again!"
                        sleep(5)
                        continue
                break
            except TimeoutException:
                print "Login webui again"
                sleep(5)
                continue

    def comptext_volume(self,name, xpath):
        for i in range(1, 10):
            try:
                namea = str(name)
                text1 = self.find_element(xpath,timeout=10).text
                print "xpath text =" + text1
                settext = str(text1)
                print settext
                if namea == settext:
                    print "Create" + " " + settext + " " + "sucess!!"
                    print "-----------------------------------------"
                    return True
                    break
                else:
                    print "Create" + " " + settext + " " + "Fail!!" + "refer now!!"
                    elemtn1 = WebDriverWait(driver, 30, 0.5).until \
                        (EC.presence_of_element_located((By.XPATH, "//div[4]/div/div/a[5]/span/span/span"))
                         )
                    elemtn1.click()
                    sleep(10)
                    print "-----------------------------------------"
                    return False
            except:
                sleep(5)
            continue

    def textcomp(self,name, numberi):
        for i in range(1, 10):
            try:
                namea = str(name)
                print namea
                if namea == "f0":
                    textname = "//div[4]/div[2]/div/div/table/tbody/tr/td/div"
                    print textname
                    text = self.find_element(textname).text
                    print text
                    settext = str(text)
                    if namea == settext:
                        print "Create" + " " + settext + " " + "sucess!!"
                        print "-----------------------------------------"
                        return True
                        break
                    else:
                        print "Create" + " " + settext + " " + "Fail!!" + "refer now!!"
                        elemtn1=self.wait_for_element_visible("//div[4]/div/div/a[5]/span/span/span",timeout=30)
                        elemtn1.click()
                        sleep(10)
                        print "-----------------------------------------"
                        return False
                else:
                    textname = "//div[4]/div[2]/div/div/table" + "[" + str(numberi) + "]" + "/tbody/tr/td/div"
                    print textname
                    text = self.find_element(textname).text
                    settext = str(text)
                    print settext
                    if namea == settext:
                        print "Create" + " " + settext + " " + "sucess!!"
                        print "-----------------------------------------"
                        return True
                        break
                    else:
                        print "Create" + " " + settext + " " + "Fail!!" + "refer now!!"
                        elemtn1=self.wait_for_element_visible("//div[4]/div/div/a[5]/span/span/span",timeout=30)
                        elemtn1.click()
                        sleep(10)
                        print "-----------------------------------------"
                        return False
            except:
                sleep(5)
                continue
#-------------------------------------------------------------start test ------------------------------------------------------------------
    def test_0_fw_upgrade_status(self):
        ip = get_ip_address()
        shell = spur.SshShell(hostname=ip, username="root", password="1234", port=2222,
                              missing_host_key=spur.ssh.MissingHostKey.accept)
        result = shell.run(["/bin/uname", "-a"])
        result_string = result.output
        date = result_string[40:48]
        print "FW date =" + date
        systime = time.strftime("%Y%m%d")
        print systime
        compare_result = string_compare(date, systime)
        if compare_result == True:
            print "FW upgrade success"

        else:
            print "FW upgrade fail"
            pytest.exit("close the program")

        self.assertTrue(compare_result==True)

    def test_1_reset_reinitialize(self):
        try:
            self.login_admin()
            self.element_clickable("click maintain button",
                              "//div[2]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/img")
            self.element_clickable("choose system recovery", "//div[2]/div/a[2]/span/span/span[2]")
            self.element_clickable("choose radio reset_to_default", "//div[6]/div/div/div/div/div/span")
            self.element_clickable("click reset device button", "//div[7]/div/div/a/span/span/span[2]")
            sleep(3)
            self.element_clickable("click confirm button", "//div[3]/div/div/a[5]/span/span/span[2]")
            sleep(40)
            # check nas reboot status,give nas 3min reboot
            for i in range(1, 10):
                ping_status = ping_host(nasip)
                if ping_status == False:
                    print "NAS reinitialize success!!"
                    break
                else:
                    print "NAS is alive,ping time =" + str(i)
                    sleep(10)
                    continue
            print "-----------------------------------------------------------------------------------------"
            print "after reset checking nas ip........"
            for i in range(1, 10):
                reset_after_ip = get_ip_address()
                print "reset_after_ip =" + str(reset_after_ip)
                reboot_ping = ping_host(reset_after_ip)
                if reboot_ping == True:
                    print "NAS reset success!!"
                    break
                else:
                    print "NAS is restarting...."
                    sleep(10)
                    continue
            shell = spur.SshShell(hostname=reset_after_ip, username="root", password="1234", port=2222,
                                  missing_host_key=spur.ssh.MissingHostKey.accept)
            result = shell.run(["/usr/local/sbin/zpool", "list"])
            result_string = result.output
            if len(result_string) == 19:
                reinit_status = True
                print "reset success!!"
            else:
                reinit_status = False
                print "reset fail"
        except Exception as error:
            print error

            self.assertTrue(reinit_status==True,msg="Test success!!")

    def test_2_Quick_install(self):
        ip = get_ip_address()
        try:
            self.open("http://" + str(ip))
            wait_result = self.wait_element("button fond", "//a[2]/span/span/span[2]")
            if wait_result == True:
                print "Quick install loading Success!"
            else:
                print "Quick install Loading Fail"

            # enter Quick install settings
            self.wait_element_click("click Customized setup button success", "//a[2]/span/span/span[2]")
            self.wait_element_click("click network button", "//div[3]/div/div/div/div[2]/div/div/input")
            self.wait_element_click("choose static ip ratio", "//div[5]/div/div/span")
            self.wait_element_send_clear("send static ip to text", nasip,
                                    "//div[6]/div/div/div/div/div/div[2]/div/div/div/input")
            self.wait_element_click("click next button in network page", "//div[4]/div/div/a[2]/span/span/span[2]")
            self.wait_element_click("cancel select all disk ratio", "//div[11]/div/div/div/div/div/div/div/div")
            self.wait_element_click("choose one disk", "//td/div/div")
            self.wait_element_click("click next button in storage page", "//div[4]/div/div/a[2]/span/span/span[2]")
            self.wait_element_click("click apply button in finish page", "//div[4]/div/div/a[3]/span/span/span[2]")
            sleep(50)
            self.wait_element("wait login page", "//input[@id='username']")
            # start slp service
            shell = spur.SshShell(hostname=nasip, username="root", password="1234", port=2222,
                                  missing_host_key=spur.ssh.MissingHostKey.accept)
            result = shell.run(["/etc/init.d/slpd", "start"])
            result_string = result.output
            print result_string

            # skip tutorial
            loginresult = self.login_page_frist_time()

        except Exception as error:
            print error

            self.assertTrue(loginresult==True)

    #nic_mapping_check
    def nic_mapping(self):
        shell = spur.SshShell(hostname=nasip, username="root", password="1234", port=2222,
                              missing_host_key=spur.ssh.MissingHostKey.accept)
        result = shell.run(["/bin/sh", "-c", "/sbin/ifconfig | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"])
        result_string = result.output
        print result_string
        # auto gen index by line to dictionary
        mydict = dict(enumerate(line.strip() for line in result_string.split('\n')))
        print mydict
        for x in mydict.keys():
            if mydict[x] == "":
                del mydict[x]
            elif mydict[x] == "127.0.0.1":
                del mydict[x]
        self.login_admin()
        self.element_clickable("click control panel network","//div/div/div/div/div/div/div/div[2]/div/div/img")
        html = self.execute_script("return document.getElementsByClassName('x-grid-cell-inner').length;")
        if html == 28:
            list1 = []
            ip1 = self.execute_script(
                "return document.getElementsByClassName('x-grid-cell-inner')[16].textContent;").encode("utf-8")
            print "ip1 = " + str(ip1)
            ip2 = self.execute_script(
                "return document.getElementsByClassName('x-grid-cell-inner')[24].textContent;").encode("utf-8")
            print "lan port 2=" + str(ip2)
            ip3 = ip1 + "\n" + ip2
            mydict2 = dict(enumerate(line.strip() for line in ip3.split('\n')))
            print mydict2
        if html == 44:
            list1 = []
            ip1 = self.execute_script(
                "return document.getElementsByClassName('x-grid-cell-inner')[16].textContent;").encode(
                "utf-8")
            print "ip1 = " + str(ip1)
            ip2 = self.execute_script(
                "return document.getElementsByClassName('x-grid-cell-inner')[24].textContent;").encode(
                "utf-8")
            ip3 = self.execute_script(
                "return document.getElementsByClassName('x-grid-cell-inner')[32].textContent;").encode(
                "utf-8")
            ip4 = self.execute_script(
                "return document.getElementsByClassName('x-grid-cell-inner')[40].textContent;").encode(
                "utf-8")
            print "lan port 2=" + str(ip2)
            ip3 = ip1 + "\n" + ip2 + "\n" + ip3 + "\n" + ip4
            mydict2 = dict(enumerate(line.strip() for line in ip3.split('\n')))
            print mydict2

            result_nic = dict_compare(mydict, mydict2)
            self.assertTrue(result_nic==True)

    def test_3_create_pool(self):
        self.login_admin()
        self.element_clickable("click control panel pool", "//div[2]/div/div/div/div[3]/div/div/img")
        self.element_clickable("click create pool button", "//div/div/div/div/div/div/div/div/div/div/a/span/span/span[2]")
        self.element_clickable("click create pool page 1 --->Next button", "//div[5]/div[3]/div/div/a[4]/span/span/span[2]")
        self.element_clickable("click create pool page 2 --->Next button", "//div[5]/div[3]/div/div/a[4]/span/span/span[2]")
        self.element_clickable("click create pool page 3 --->Next button", "//div[5]/div[3]/div/div/a[4]/span/span/span[2]")
        self.wait_element_send("input pool name", "pool2", "//div[4]/div/div/div/div[2]/div/div/div/div/div/div/input")
        self.element_clickable("click create pool page 4 --->Next button", "//div[5]/div[3]/div/div/a[4]/span/span/span[2]")
        self.element_clickable("trigged tering type", "//div[5]/div/div/div/div[2]/div/div/div/div/div/div[2]")
        sleep(3)
        self.css_sele_clickable("choose tering type to HDD", "ul > li:nth-child(4)")
        self.element_clickable("choose disk", "//div[4]/div[2]/div/div[2]/table/tbody/tr/td/div/div")
        self.element_clickable("click Create pool page 5", "//div[5]/div[3]/div/div/a[4]/span/span/span[2]")
        self.element_clickable("click create pool confirm button", "//div[5]/div[3]/div/div/a[3]/span/span/span[2]")
        pool_success = self.comptext_volume("pool2", "//table[2]/tbody/tr/td/div/div/div/div/div/div")
        if pool_success == True:
            print "create pool2 success"
        else:
            print "create pool fail"

        assert pool_success == True

    def test_4_create_volume(self):
        self.login_admin()
        self.element_clickable("click control panel volume button", "//div[2]/div/div/div/div[4]/div/div/img")
        self.element_clickable("click create volume button","//div/div/div/div/div/div/div/div/div/div/a/span/span/span[2]")
        self.wait_element_send("input volume name", "v1", "//div[2]/div/div/div/div/div/div/input")
        self.wait_element_send("input volume capacity", "100", "//div[4]/div/div/div/div/div/div/input")
        self.element_clickable("click next button", "//div[3]/div/div/a[3]/span/span/span[2]")
        self.element_clickable("click confirm button", "//div[3]/div/div/a[4]/span/span/span[2]")
        volume_create_success = self.comptext_volume("v1", "//div[3]/div[2]/div/div/table[3]/tbody/tr/td/div")
        if volume_create_success == True:
            print "voulme create success"

        else:
            print "Volume create fail"

        assert volume_create_success == True

    def test_5_create_share_folder(self):
        self.login_admin()
        self.wait_element_click("click control panel share folder", "//div[3]/div/div/div/div[4]/div/div/img")
        sleep(5)
        self.wait_element_click("click share folder  ", "//div[2]/div/a[2]/span/span/span[2]")
        sleep(5)
        for i in range(0, 1):
            for a in range(1, 10):
                try:
                    createbutton=self.wait_for_element_visible("//div[2]/div/div/div/div/div[2]/div/a/span/span/span[2]",timeout=10)
                    tfcreatebutton = bool(createbutton)
                    if tfcreatebutton == True:
                        sleep(10)
                        createbutton.click()
                        break
                    else:
                        continue
                except:
                    continue
            folder = "f" + str(i)
            foldername=self.wait_for_element_visible("//div[2]/div/div/div/div/div/div/div[3]/div/div/div/div/div/div/input",timeout=10)
            foldername.send_keys(folder)
            sleep(2)
            self.find_element("//div[5]/div[3]/div/div/a[2]/span/span/span[2]").click()
            for s in range(1, 50):
                sleep(3)
                textcompatf = self.textcomp(folder, i)
                if textcompatf == True:
                    break
                else:
                    print textcompatf
                    sleep(1)
                    continue

            assert textcompatf == True

    def test_6_set_nfs_host(self):
        self.login_admin()
        print "start set nfs host......"
        self.wait_element_click("click control panel share folder", "//div[3]/div/div/div/div[4]/div/div/img")
        sleep(5)
        self.wait_element_click("click NFS host", "//div[2]/div/a[3]/span/span/span[2]")
        sleep(5)
        self.wait_element_click("click add nfs button", "//div[2]/div/div/div/div[2]/div/div/a/span/span/span")
        self.wait_element_send("input ip", computerip,
                          "//div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/input")
        self.element_clickable("trigged read/write checkbox",
                          "//div[5]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[2]")
        sleep(2)
        self.execute_script("document.querySelector('ul > li:nth-child(2)').click()")
        self.wait_element_click("click confirm button in nfs host list", "//div[3]/div/div/a[2]/span/span/span[2]")

    def test_7_create_iscsi_target_Lun(self):
        self.login_admin()
        self.element_clickable("click control panel ISCSI button", "//div[2]/div/div/div/div[6]/div/div/img")
        self.element_clickable("click ISCSI setup button", "//div[2]/div/a[2]/span/span/span[2]")
        self.element_clickable("click create ISCSI", "//div[2]/div/div/div/div/div[2]/div/a/span/span/span[2]")
        self.element_clickable("click create target & lun", "//div[3]/div/div/a[5]/span/span/span[2]")
        self.wait_element_send("input target name=Lun1", "lun1",
                          "//div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/input")
        self.element_clickable("click next button in Create Wizard page", "//div[3]/div/div/a[7]/span/span/span[2]")
        self.wait_element_send("input lun name=Lun1", "lun1",
                          "//div[2]/div/div/div/div/div/div[2]/div/div/div/div/div/div/input")
        self.wait_element_send("input capacity 100GB", "100", "//div[5]/div/div/div/div/div/div/input")
        self.element_clickable("click next button in Create a LUN page", "//div[3]/div/div/a[7]/span/span/span[2]")
        self.element_clickable("click confirm button", "//div[3]/div/div/a[8]/span/span/span[2]")
        print "wait pop up ok message"
        sleep(15)
        self.execute_script(
            "document.getElementsByClassName('x-btn x-unselectable x-box-item x-toolbar-item x-btn-default-small q-btn-primary')[6].click()")
        self.wait_element_click("click iscsi list", "//div[2]/div[2]/div/div/table/tbody/tr/td/div/img")
        iscis_sucess = self.comptext_volume("lun1", "//div[2]/div[2]/div/div/table[2]/tbody/tr/td/div")
        self.execute_script(
            "document.getElementsByClassName('x-form-field x-form-checkbox x-form-checkbox-default x-form-cb x-form-cb-default')[4].click()")
        if iscis_sucess == True:
            print "ISCSI create success!!"
        else:
            print "ISCSI create fail!!!"

        self.assertTrue(iscis_sucess==True)

        for i in range(1, 5):
            sleep(1)
            print "wait ISCSI ready " + str(i) + "second"

    def test_8_iscsi_transfer(self):
        print "ISCSI tranfer start........"
        p = subprocess.Popen("C:\\Users\\N269-01\\Desktop\\quicktest\\iscsi.bat", stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        result = p.communicate()[0]
        print result

        sleep(10)
        c = subprocess.Popen("C:\\ISCSI_auto\\iscsi_test.bat", stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        result1 = c.communicate()[0]
        print result1

        iscsi_upload_status = samba_check_function("ISCSI upload ", r'E:\service\iscsi.txt', r'I:\iscsi.txt')
        print "ISCSI tranfer status = " + str(iscsi_upload_status)
        if iscsi_upload_status == True:
            print "ISCSI upload success!!"
        else:
            print "ISCSI upload fail!!"
        iscsi_download_status = samba_check_function("ISCSI download", r'I:\iscsi.txt',
                                                     r'C:\Users\N269-01\Desktop\service_download\iscsi.txt')
        if iscsi_download_status == True:
            print "ISCSI download success!!"
        else:
            print "ISCSI download fail!!"

        self.assertTrue(iscsi_upload_status==True and iscsi_download_status==True)

    def test_9_test_samba_transfer(self):
        print "samba tranfer start........E:---->Y:"
        samaba_upload_status = samba_check_function("samba upload ", r'E:\service\samba.txt', r'Y:\samba.txt')
        if samaba_upload_status == True:
            print "samba upload file success!!"
        else:
            print "samba upload file  fail!!"
        samba_download_status = samba_check_function("samba download", r'Y:\samba.txt',
                                                     r'C:\Users\N269-01\Desktop\service_download\samba.txt')
        if samba_download_status == True:
            print "samba download success!!"
        else:
            print "samba download fail!!!"

        self.assertTrue(samaba_upload_status==True and samba_download_status==True)

    def test_10_ftp_transfer(self):

        ftp_upload = uploadFile("/f0", "ftp.txt", "E:/service/ftp.txt", nasip, 21, "admin", "1234")
        print ftp_upload
        ftp_download = getServerFile("/f0", "ftp.txt", nasip, 21, "admin", "1234")
        print ftp_download
        print "done.."
        assert ftp_upload == True and ftp_upload == True

    def test_11_nfs_tranfer(self):

        print "nfs tranfer start........E:---->z:"
        nfs_upload_status = samba_check_function("nfs upload ", r'E:\service\nfs.txt', r'Z:\nfs.txt')
        if nfs_upload_status == True:
            print "nfs upload file success!!"
        else:
            print "nfs upload file  fail!!"
        nfs_download_status = samba_check_function("nfs download", r'Z:\nfs.txt',
                                                   r'C:\Users\N269-01\Desktop\service_download\nfs.txt')
        if nfs_download_status == True:
            print "nfs download success!!"
        else:
            print "nfs download fail!!!"

        assert nfs_upload_status == True and nfs_download_status == True

    def test_12_webdav_tranfer(self):
        print "webdav tranfer start....."
        webdav_status = webdav_tranfer()
        print webdav_status
        assert webdav_status == True