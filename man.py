import os
import json as jsond  # json
import time  # sleep before exit
import binascii  # hex encoding
from uuid import uuid4  # gen random guid
import platform  # check platform
import subprocess  # needed for mac device
import hmac # signature checksum
import hashlib # signature checksum
import requests as r, json
import time
from colorama import Fore, Back, init, Style
import keyboard

try:

    if os.name == 'nt':

        import win32security  # get sid (WIN only)

    import requests  # https requests

except ModuleNotFoundError:

    print("Exception when importing modules")

    print("Installing necessary modules....")

    if os.path.isfile("requirements.txt"):

        os.system("pip install -r requirements.txt")

    else:

        if os.name == 'nt':

            os.system("pip install pywin32")

        os.system("pip install requests")

    print("Modules installed!")

    time.sleep(1.5)

    os._exit(1)





class api:



    name = ownerid = secret = version = hash_to_check = ""



    def __init__(self, name, ownerid, secret, version, hash_to_check):

        if len(ownerid) != 10 and len(secret) != 64:

            print("Go to Manage Applications on dashboard, copy python code, and replace code in main.py with that")

            time.sleep(3)

            os._exit(1)

    

        self.name = name



        self.ownerid = ownerid



        self.secret = secret



        self.version = version

        self.hash_to_check = hash_to_check

        self.init()



    sessionid = enckey = ""

    initialized = False



    def init(self):

        if self.sessionid != "":

            print("You've already initialized!")

            time.sleep(3)

            os._exit(1)



        sent_key = str(uuid4())[:16]

        

        self.enckey = sent_key + "-" + self.secret

        

        post_data = {

            "type": "init",

            "ver": self.version,

            "hash": self.hash_to_check,

            "enckey": sent_key,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        if response == "KeyAuth_Invalid":

            print("The application doesn't exist")

            time.sleep(3)

            os._exit(1)



        json = jsond.loads(response)



        if json["message"] == "invalidver":

            if json["download"] != "":

                print("New Version Available")

                download_link = json["download"]

                os.system(f"start {download_link}")

                time.sleep(3)

                os._exit(1)

            else:

                print("Invalid Version, Contact owner to add download link to latest app version")

                time.sleep(3)

                os._exit(1)



        if not json["success"]:

            print(json["message"])

            time.sleep(3)

            os._exit(1)



        self.sessionid = json["sessionid"]

        self.initialized = True

        

        if json["newSession"]:

            time.sleep(0.1)



    def register(self, user, password, license, hwid=None):

        self.checkinit()

        if hwid is None:

            hwid = others.get_hwid()



        post_data = {

            "type": "register",

            "username": user,

            "pass": password,

            "key": license,

            "hwid": hwid,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            print(json["message"])

            self.__load_user_data(json["info"])

        else:

            print(json["message"])

            time.sleep(3)

            os._exit(1)



    def upgrade(self, user, license):

        self.checkinit()



        post_data = {

            "type": "upgrade",

            "username": user,

            "key": license,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            print(json["message"])

            print("Please restart program and login")

            time.sleep(3)

            os._exit(1)

        else:

            print(json["message"])

            time.sleep(3)

            os._exit(1)



    def login(self, user, password, hwid=None):

        self.checkinit()

        if hwid is None:

            hwid = others.get_hwid()



        post_data = {

            "type": "login",

            "username": user,

            "pass": password,

            "hwid": hwid,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            self.__load_user_data(json["info"])

            print(json["message"])

        else:

            print(json["message"])

            time.sleep(3)

            os._exit(1)



    def license(self, key, hwid=None):

        self.checkinit()

        if hwid is None:

            hwid = others.get_hwid()



        post_data = {

            "type": "license",

            "key": key,

            "hwid": hwid,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            self.__load_user_data(json["info"])

            print(json["message"])

        else:

            print(json["message"])

            time.sleep(3)

            os._exit(1)



    def var(self, name):

        self.checkinit()



        post_data = {

            "type": "var",

            "varid": name,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            return json["message"]

        else:

            print(json["message"])

            time.sleep(3)

            os._exit(1)



    def getvar(self, var_name):

        self.checkinit()



        post_data = {

            "type": "getvar",

            "var": var_name,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }

        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            return json["response"]

        else:

            print(f"NOTE: This is commonly misunderstood. This is for user variables, not the normal variables.\nUse keyauthapp.var(\"{var_name}\") for normal variables");

            print(json["message"])

            time.sleep(3)

            os._exit(1)



    def setvar(self, var_name, var_data):

        self.checkinit()



        post_data = {

            "type": "setvar",

            "var": var_name,

            "data": var_data,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }

        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            return True

        else:

            print(json["message"])

            time.sleep(3)

            os._exit(1)



    def ban(self):

        self.checkinit()



        post_data = {

            "type": "ban",

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }

        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            return True

        else:

            print(json["message"])

            time.sleep(3)

            os._exit(1)



    def file(self, fileid):

        self.checkinit()



        post_data = {

            "type": "file",

            "fileid": fileid,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if not json["success"]:

            print(json["message"])

            time.sleep(3)

            os._exit(1)

        return binascii.unhexlify(json["contents"])



    def webhook(self, webid, param, body = "", conttype = ""):

        self.checkinit()



        post_data = {

            "type": "webhook",

            "webid": webid,

            "params": param,

            "body": body,

            "conttype": conttype,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            return json["message"]

        else:

            print(json["message"])

            time.sleep(3)

            os._exit(1)



    def check(self):

        self.checkinit()



        post_data = {

            "type": "check",

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }

        response = self.__do_request(post_data)



        json = jsond.loads(response)

        if json["success"]:

            return True

        else:

            return False



    def checkblacklist(self):

        self.checkinit()

        hwid = others.get_hwid()



        post_data = {

            "type": "checkblacklist",

            "hwid": hwid,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }

        response = self.__do_request(post_data)



        json = jsond.loads(response)

        if json["success"]:

            return True

        else:

            return False



    def log(self, message):

        self.checkinit()



        post_data = {

            "type": "log",

            "pcuser": os.getenv('username'),

            "message": message,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        self.__do_request(post_data)



    def fetchOnline(self):

        self.checkinit()



        post_data = {

            "type": "fetchOnline",

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            if len(json["users"]) == 0:

                return None

            else:

                return json["users"]

        else:

            return None

            

    def fetchStats(self):

        self.checkinit()



        post_data = {

            "type": "fetchStats",

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            self.__load_app_data(json["appinfo"])

            

    def chatGet(self, channel):

        self.checkinit()



        post_data = {

            "type": "chatget",

            "channel": channel,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            return json["messages"]

        else:

            return None



    def chatSend(self, message, channel):

        self.checkinit()



        post_data = {

            "type": "chatsend",

            "message": message,

            "channel": channel,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            return True

        else:

            return False



    def checkinit(self):

        if not self.initialized:

            print("Initialize first, in order to use the functions")

            time.sleep(3)

            os._exit(1)



    def changeUsername(self, username):

        self.checkinit()



        post_data = {

            "type": "changeUsername",

            "newUsername": username,

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            print("Successfully changed username")

        else:

            print(json["message"])

            time.sleep(3)

            os._exit(1)  



    def logout(self):

        self.checkinit()



        post_data = {

            "type": "logout",

            "sessionid": self.sessionid,

            "name": self.name,

            "ownerid": self.ownerid

        }



        response = self.__do_request(post_data)



        json = jsond.loads(response)



        if json["success"]:

            print("Successfully logged out")

            time.sleep(3)

            os._exit(1)

        else:

            print(json["message"])

            time.sleep(3)

            os._exit(1)         

            

    def __do_request(self, post_data):

        try:

            response = requests.post(

                "https://keyauth.win/api/1.2/", data=post_data, timeout=10

            )

            

            key = self.secret if post_data["type"] == "init" else self.enckey

            if post_data["type"] == "log": return response.text

                        

            client_computed = hmac.new(key.encode('utf-8'), response.text.encode('utf-8'), hashlib.sha256).hexdigest()

            

            signature = response.headers["signature"]

            

            if not hmac.compare_digest(client_computed, signature):

                print("Signature checksum failed. Request was tampered with or session ended most likely.")

                print("Response: " + response.text)

                time.sleep(3)

                os._exit(1) 

            

            return response.text

        except requests.exceptions.Timeout:

            print("Request timed out. Server is probably down/slow at the moment")



    class application_data_class:

        numUsers = numKeys = app_ver = customer_panel = onlineUsers = ""



    class user_data_class:

        username = ip = hwid = expires = createdate = lastlogin = subscription = subscriptions = ""



    user_data = user_data_class()

    app_data = application_data_class()



    def __load_app_data(self, data):

        self.app_data.numUsers = data["numUsers"]

        self.app_data.numKeys = data["numKeys"]

        self.app_data.app_ver = data["version"]

        self.app_data.customer_panel = data["customerPanelLink"]

        self.app_data.onlineUsers = data["numOnlineUsers"]



    def __load_user_data(self, data):

        self.user_data.username = data["username"]

        self.user_data.ip = data["ip"]

        self.user_data.hwid = data["hwid"] or "N/A"

        self.user_data.expires = data["subscriptions"][0]["expiry"]

        self.user_data.createdate = data["createdate"]

        self.user_data.lastlogin = data["lastlogin"]

        self.user_data.subscription = data["subscriptions"][0]["subscription"]

        self.user_data.subscriptions = data["subscriptions"]





class others:

    @staticmethod

    def get_hwid():

        if platform.system() == "Linux":

            with open("/etc/machine-id") as f:

                hwid = f.read()

                return hwid

        elif platform.system() == 'Windows':

            winuser = os.getlogin()

            sid = win32security.LookupAccountName(None, winuser)[0]  # You can also use WMIC (better than SID, some users had problems with WMIC)

            hwid = win32security.ConvertSidToStringSid(sid)

            return hwid

            '''

            cmd = subprocess.Popen(

                "wmic useraccount where name='%username%' get sid",

                stdout=subprocess.PIPE,

                shell=True,

            )



            (suppost_sid, error) = cmd.communicate()



            suppost_sid = suppost_sid.split(b"\n")[1].strip()



            return suppost_sid.decode()



            ^^ HOW TO DO IT USING WMIC

            '''

        elif platform.system() == 'Darwin':

            output = subprocess.Popen("ioreg -l | grep IOPlatformSerialNumber", stdout=subprocess.PIPE, shell=True).communicate()[0]

            serial = output.decode().split('=', 1)[1].replace(' ', '')

            hwid = serial[1:-2]

            return hwid


init(convert=True)

merah = Back.RED
hijau = Back.GREEN
reset = Style.RESET_ALL

class SmsHub:
    def __init__(self):
        self.api_key = '185941U2bdd29d10161b5d813cce82165c2d1bb'
        self.api = r.Session()

    def send(self, data):
        return self.api.post('https://smshub.org/stubs/handler_api.php', data=data)

    def get_number(self):
        data = {
            'api_key': self.api_key,
            'action': 'getNumber',
            'service': 'alj',
            'operator': 'wom',
            'country': '151',
            'maxPrice': '5'
        }
        return self.send(data)

    def get_code(self, rn1):
        data = {
            'api_key': self.api_key,
            'action': 'getStatus',
            'id': rn1
        }
        return self.send(data)
    
    def get_balance(self):
        data = {
            'api_key': self.api_key,
            'action': 'getBalance',
        }
        return self.send(data)

    def set_status(self, rn1):
        data = {
            'api_key': self.api_key,
            'action': 'setStatus',
            'id': rn1,
            'status': '3'
        }
        return self.send(data)
    
    def batal(self, rn1):
        data = {
            'api_key': self.api_key,
            'action': 'setStatus',
            'id': rn1,
            'status': '8'
        }
        return self.send(data)

class Smsman:
    def __init__(self):
        self.api_key = 'U3f6SZCzf2_96ylpSuzrm0x_4jDqCvhL'
        self.api = r.Session()

    def send(self, data):
        return self.api.post('https://api.sms-man.com/stubs/handler_api.php', data=data)

    def get_number(self, serv, cont):
        data = {
            'api_key': self.api_key,
            'action': 'getNumber',
            'service': serv,
            'country': cont
        }
        return self.send(data)

    def get_code(self, rn1):
        data = {
            'api_key': self.api_key,
            'action': 'getStatus',
            'id': rn1
        }
        return self.send(data)
    
    def get_balance(self):
        data = {
            'api_key': self.api_key,
            'action': 'getBalance',
        }
        return self.send(data)

    def set_status(self, rn1):
        data = {
            'api_key': self.api_key,
            'action': 'setStatus',
            'id': rn1,
            'status': '3'
        }
        return self.send(data)
    
    def batal(self, rn1):
        data = {
            'api_key': self.api_key,
            'action': 'setStatus',
            'id': rn1,
            'status': '8'
        }
        return self.send(data)
    
    def get_services(self):
        data = {
            'api_key': self.api_key,
            'action': 'getServices'
        }
        return self.send(data)
    
    def get_countries(self):
        data = {
            'api_key': self.api_key,
            'action': 'getCountries'
        }
        return self.send(data)

license = input('Masukan License: ')

keyauthapp = api(
    name = "SMSBOT",
    ownerid = "sfwiIb0X5o",
    secret = "f036d0190025ac0795ed0ba5b75d554015c32dc456e47a35122ca133ded367d2",
    version = "1.0",
    hash_to_check = getchecksum()
)

KeyAuthApp.license(license)

    
print('-- SMS NIGGA BOT --')
provider = input('> 1. SMSHUB, 2. SMS_MAN \n> Pilih Provider: ')

if provider == '1':
    sms_hub = SmsHub()

    # Order a number
    gb = sms_hub.get_balance()
    gbv = gb.text.split(':')[1]
    gv = float(float(gbv))
    print("> Saldo SMS_HUB:",gv)

    while True:
        try:
            y = input('> Order Number? (y/c/b): ')

            if y == 'y':
                result_number = sms_hub.get_number()
                rn1 = result_number.text.split(':')[1]
                rn2 = result_number.text.split(':')[2]  
                print(f"{hijau}> Number: {rn2}{reset}")
                print(f'{hijau}> ID Pesanan: {rn1}{reset}')

                while True:
                    # Call getcode method with the rn1 as a parameter
                    result_code = sms_hub.get_code(rn1)
                    rc = result_code.text

                    if 'STATUS_OK' in rc:
                        print("> OTP: ", rc)

                    # Check if the code is successfully retrieved
                    if rc != '0':
                        # If the code is successfully retrieved, proceed to call the set_status method
                        sms_hub.set_status(rn1)

                    # Wait for a while before checking again
                    time.sleep(15) # wait for 60 seconds

            elif y == 'c':
                rn1 = input('> ID Pesanan: ')
                while True:
                    result_code = sms_hub.get_code(rn1)
                    rc = result_code.text

                    if 'STATUS_OK' in rc:
                        print("> OTP: ", rc)

                    if rc != '0':
                        sms_hub.set_status(rn1)

                    time.sleep(15)

            elif y == 'b':
                rn1 = input('> ID Pesanan: ')
                batal = sms_hub.batal(rn1)
                bt = batal.text
                print('Nomor telah di cancel.', bt)
            else:
                print('Go Fuck Yourself.')
                break

        except KeyboardInterrupt:
            print('Proses Terganggu.')  

if provider == '2':
    sms_man = Smsman()

    # Order a number
    gb = sms_man.get_balance()
    gbv = gb.text.split(':')[1]
    gv = float(float(gbv))
    print("> Saldo SMS_NAN:", gv)

    while True:
        try:
            y = input('> Wut? (y/c/b/o): ')

            if y == 'y':
                print('--- Order Number ---')
                serv = input('> Service: ')
                cont = input('> Country: ')
                num = sms_man.get_number(serv, cont)
                rn1 = num.text.split(':')[1]
                rn2 = num.text.split(':')[2]
                print(f'> Number:  {hijau}{rn2}{reset}')
                print(f'> ID Pesanan:  {hijau}{rn1}{reset}')

                while True:
                    # Call getcode method with the rn1 as a parameter
                    result_code = sms_man.get_code(rn1)
                    rc = result_code.text

                    if 'STATUS_OK' in rc:
                        print("> OTP: ", rc)

                    # Check if the code is successfully retrieved
                    if rc != '0':
                        # If the code is successfully retrieved, proceed to call the set_status method
                        sms_man.set_status(rn1)

                    # Wait for a while before checking again
                    time.sleep(15) # wait for 60 seconds

            elif y == 'c':
                rn1 = input('> ID Pesanan: ')
                while True:
                    result_code = sms_man.get_code(rn1)
                    rc = result_code.text

                    if 'STATUS_OK' in rc:
                        print("> OTP: ", rc)

                    if rc != '0':
                        sms_man.set_status(rn1)

                    time.sleep(15)

            elif y == 'b':
                rn1 = input('> ID Pesanan: ')
                batal = sms_man.batal(rn1)
                bt = batal.text
                if 'ACCESS_CANCEL' in bt:
                    print(f'{merah}Nomor Dibatalkan.{reset}')

            elif y == 'o':
                s = sms_man.get_services()
                if s.status_code == 200:
                    sr = sorted(s.json(), key=lambda x: x.get('id', ''))
                    print(f"> Services: ")
                    for service in sr:
                        print(f"{'> '}{service['id']} - {service['title']}")

                # Mendapatkan data dari getCountries
                cc = sms_man.get_countries()
                if cc.status_code == 200:
                        cc_dict = json.loads(cc.text)
                        sorted_countries = sorted(cc_dict.values(), key=lambda x: int(x['id']))
                        print("\n> Countries:")
                        for country_info in sorted_countries:
                            print(f"{'> '}{country_info['id']} - {country_info['name_en']}")

            else:
                print('Go Fuck Yourself.')
                break

        except KeyboardInterrupt:
            print(f'{merah}Proses Terganggu.{reset}')
