import requests,json
import base64 
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5
from Crypto.PublicKey import RSA
from kquynh_function_gw import data,notification,post,msg,head_menu
from kquynh_param_gw import login,account_login
account=data["account"]
domain_list=[]

def load_ui(new_domain):
    # Check the login interface is displayed #
    param=json.loads(login(new_domain))
    try:
        url_load_ui=param["url_load_ui"]
        respon = requests.get(url_load_ui, data = "",cookies="")
        return True
    except Exception as e:
        return False
    
def login_correct(new_domain):
    head_menu("LOGIN")
    param=json.loads(login(new_domain))
    result_login=param["result_login"]
    sucess_login=post(param["url_login"],param["param_login_ri"],"")
    try :
        if sucess_login == False :
            result_login["no_ui"] = True
        elif notification(sucess_login) == True :
            msg("p",param["id_pass"])
            result_login["login_correct"] = True
        else :
            if sucess_login["msg"]==param["pass_changed"]:
                result_login["pass_changed"]=True

            elif sucess_login["msg"]==param["id_exist"]:
                result_login["id"]=True
    except :
        result_login["no_response"]=True
    
    return result_login  

def login_wrong(new_domain):
    try :
        param=json.loads(login(new_domain))
        url_login=param["url_login"]


        # login is wrong #
        sucess_login=post(url_login,param["param_login_pw"],"")
        if notification(sucess_login) == False:
            msg("p",param["pass_pass"])
        else :
            msg("f",param["fail_pass"])


        # login is wrong #
        sucess_login=post(url_login,param["param_login_iw"],"")
        if notification(sucess_login) == False:
            msg("p",param["pass_id"])
        else :
            msg("f",param["fail_id"])
    except :
        pass


def enter_account():
    param=json.loads(account_login())
    domain_list=[]
    pubkey = '''-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDlOJu6TyygqxfWT7eLtGDwajtN
    FOb9I5XRb6khyfD1Yt3YiCgQWMNW649887VGJiGr/L5i2osbl8C9+WJTeucF+S76
    xFxdU6jE0NQ+Z+zEdhUTooNRaY5nZiu5PgDB0ED/ZKBUSLKL7eibMxZtMlUDHjm4
    gwQco1KRMDSmXSMkDwIDAQAB
    -----END PUBLIC KEY-----'''
    rsa_key = RSA.importKey(pubkey)
    cipher = PKCS1_v1_5.new(rsa_key)

    msg("n",param["note"])
    # Enter domain #
    i=1
    total_domain=input(param["total_domain"])
    while i <= int(total_domain) :
        domain_name=input(param["domain"]+str(i)+" : ")
        domain_list.append(domain_name)
        i=i+1
    msg("t",param["range"])


    # Enter Account #
    j=1
    total_account=3
    while j<=int(total_account) :
        id=input(param["enter_id"]+str(j)+" : ")
        password=input(param["enter_pw"]+str(j)+" : ")
        if j== 1:
            account["id_us_one"]=base64.b64encode(cipher.encrypt(str.encode(id))).decode()
            account["pw_us_one"]=base64.b64encode(cipher.encrypt(str.encode(password))).decode()
            msg("t",param["range"])
        elif j==2 :
            account["id_us_two"]=base64.b64encode(cipher.encrypt(str.encode(id))).decode()
            account["pw_us_two"]=base64.b64encode(cipher.encrypt(str.encode(password))).decode()
            msg("t",param["range"])
        else:
            account["id_us_thr"]=base64.b64encode(cipher.encrypt(str.encode(id))).decode()
            account["pw_us_thr"]=base64.b64encode(cipher.encrypt(str.encode(password))).decode()
            msg("t",param["range"])
        j=j+1
    return domain_list

domain_list=enter_account()

