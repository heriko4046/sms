import requests as r, json
import time
from colorama import Fore, Back, init, Style
import keyboard

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
