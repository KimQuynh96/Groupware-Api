
import testlink,requests,json,datetime,sys,os
from datetime import date
from colorama import Fore, Back, Style
from colorama import init, AnsiToWin32
from pathlib import Path
from requests.auth import HTTPBasicAuth
from sys import platform




old_domain="qa.hanbiro.net"
init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream
testlink_url='http://qa1.hanbiro.net/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
testlink_devkey='45deb0ba8978e83d78a81d0b80a7df0c'
tls=testlink.TestLinkHelper(testlink_url,testlink_devkey).connect(testlink.TestlinkAPIClient)
json_file=os.path.dirname(Path(__file__).absolute())+"\\kquynh_file_data.json"
date_time=str(date.today())+"-"+ str(datetime.datetime.now().time())[None:str(datetime.datetime.now().time()).rfind(".")].replace(":","-")
today = str(date.today())

if platform == "linux" or platform == "linux2":
    json_file=json_file.replace("\\","/")
with open(json_file) as json_file:
	data = json.load(json_file)

def change(new_domain,url,old_domain):
    if len(new_domain)==0 :
        return url 
    else :
        return url.replace(old_domain,new_domain)

def execution_test_link(id_testcase,sta):
    if sta=="p" :
        tls.reportTCResult(testcaseexternalid=id_testcase,testplanid=8963,buildname="V3.8.41",status='p')
    if sta=="f" :
        tls.reportTCResult(testcaseexternalid=id_testcase,testplanid=8963,buildname="V3.8.41",status='f')

def check_the_saved_data(response,title,memo,array):
    if len(response[array]) == 0:
        return False
    else:
        for x in response[array] :
            if (x[memo])== title :
                return True
        return False
                
def notification(success):
    if "success" in success :
        if success["success"]== True :
            return True    
        elif success["success"]== "null" :
            return 0
        else : 
            return False
    else :
        return False

def result_add(response_add,check_add,list_msg):
    if notification(response_add) == True :
        check_add = True
        msg("p",list_msg["pass"])
    else :
        msg("f",list_msg["fail"])
    return check_add

def send_mail(title_mail,receiver,content_mail):
    param_compose=data["mail"]["compose_mail"]["param_write"]
    param_compose["toaddr"]=receiver
    param_compose["subject"]=title_mail
    param_compose["contents"]=content_mail
    url_compose=data["mail"]["compose_mail"]["api_write"]
    success_send_mail=post(url_compose,param_compose,cookie_recipient("qa.hanbiro.net"))
    return success_send_mail

'''
def url_file(menu,local_file,file_name):
    def api_file():
        def random_id(num):
            ranchar=''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(num))
            return ranchar
        uuiarr=[]
        uuiarr.append(random_id(8))
        uuiarr.append(random_id(4))
        uuiarr.append('4'+ random_id(3))
        uuiarr.append(random_id(4))
        uuiarr.append(random_id(12))
        uuid="-".join(uuiarr)
        return uuid
    a=[]
    a.append(menu +"_" + api_file())
    api=data["attach_file"]["api"]
    api=api + menu +"_" + api_file()

    param=data["attach_file"]["param"]
    param["name"]=file_name
   
    #local_file_1=os.path.dirname(Path(__file__).absolute())+"\\cuncon.png" 
    f = open(local_file, 'rb')
    files = param["file"]= {"file": (local_file, f)}
    
    success=requests.post(api,files=files,data=param)
    success_upload_file=json.loads(success.text)
    print(success_upload_file)
   
    if success_upload_file["success"]== True :
        a.append(True)
    else :
        a.append(False)
    return a
'''
    
'''
def post(url,param,cookies):
    respon = requests.post(url, data = param,cookies=cookies)
    success = json.loads(respon.text)
    return success

'''
def post(url,param,cookies):
    respon = requests.post(url, data = param,cookies=cookies)
    if "<html>" in respon.text:
        response=respon.text
        n=response[response.rfind(">{"):None][1:None]
        success=data["success"]=json.loads(n)
        msg("f","-UI is not returned <Fail>")
        return False

    else :
        success = json.loads(respon.text)
    return success

def post_header(url,param,header,cookies):
    respon = requests.post(url, data = param,headers= header,cookies=cookies)
    success = json.loads(respon.text)
    return success

def get(url,param,cookies):
    respon = requests.get(url, data = param,cookies=cookies)
    success = json.loads(respon.text)
    return success

def delete(url,param,cookies):
    respon = requests.delete(url, data = param,cookies=cookies)
    success = json.loads(respon.text)
    return success

def cookie_writer(new_domain):
    url=data["login"]["api_login"]
    url_login=change(new_domain,url,old_domain)
    param_login = {'gw_id': data["login"]["id_user"],'gw_pass': data["login"]["passwword_user"]}
    success=post(url_login,param_login,cookies="")
    return {"HANBIRO_GW":success["session"],"hmail_key":success["hmail_key"]}

def cookie_recipient(new_domain):
    url=data["login"]["api_login"]
    url_login=change(new_domain,url,old_domain)
    param_login = {'gw_id': data["login"]["id_recipient"],'gw_pass': data["login"]["password_recipient"]}
    success=post(url_login,param_login,cookies="")
    return {"HANBIRO_GW":success["session"],"hmail_key":success["hmail_key"]}

def account_one(new_domain):
    url=data["login"]["api_login"]
    url_login=change(new_domain,url,old_domain)
    param_login ={'gw_id': data["account"]["id_us_one"],'gw_pass': data["account"]["pw_us_one"]}
    success=post(url_login,param_login,cookies="")
    return {"HANBIRO_GW":success["session"],"hmail_key":success["hmail_key"]}

def account_two(new_domain):
    url=data["login"]["api_login"]
    url_login=change(new_domain,url,old_domain)
    param_login ={'gw_id': data["account"]["id_us_two"],'gw_pass': data["account"]["pw_us_two"]}
    success=post(url_login,param_login,cookies="")
    return {"HANBIRO_GW":success["session"],"hmail_key":success["hmail_key"]}

def account_thr(new_domain):
    url=data["login"]["api_login"]
    url_login=change(new_domain,url,old_domain)
    param_login ={'gw_id': data["account"]["id_us_thr"],'gw_pass': data["account"]["pw_us_thr"]}
    success=post(url_login,param_login,cookies="")
    return {"HANBIRO_GW":success["session"],"hmail_key":success["hmail_key"]}


def msg(t,text):
    if t=="p":
        print("\033[32m"+text+"\033[39m")
    elif t=="n":
        print("\033[33m"+text+"\033[39m")
    elif t=="t":
        print("\033[37m"+text+"\033[39m")
    else :
        print("\033[31m"+text+"\033[39m")

def url(url_head,param):
    api=""
    for x in param :
        api= api + x +"=" +param[x] +'&' 
    url= url_head + api
    url = url[:-1]
    return url 

def create_url(url_head,param):
    url_content=""
    for x in param :
        url_content= url_content + x +"/" +param[x] +'/' 
    url= url_head + url_content
    url = url[:-1]
    return url 

def next_page(maxpage,url,param,cookie,subject):
    i=1 
    list_data=[]
    while i<=maxpage :
        param["page"]=str(i)
        url=api(url,param)
        sucess_get_list=get(url,"",cookie)
        for x in sucess_get_list["rows"] :
            list_data.append(x[subject]) 
        i=i+1
    return list_data

def id_user(new_domain,user_id):
    old_url_get_list_left_folder=data["contact"]["get_list_left_menu"]
    url_get_list_left_folder=change(new_domain,old_url_get_list_left_folder,old_domain)
    success_get_list_left_folder=get(url_get_list_left_folder,"",cookie_writer(new_domain))
    i=0
    user=[]
    if notification(success_get_list_left_folder)== True :
        for x in success_get_list_left_folder["rows"]:
            if "children" in x:
                for z in x["children"] :
                    if z["title"]=="Kim Quynh" :
                        data["contact"]["get_list_user"]["param"]["id"]=z["id"] # id folder #
                        i=i+1
                        break
            else :
                for z in success_get_list_left_folder["rows"] :
                    if z["title"]=="Kim Quynh" :
                        data["contact"]["get_list_user"]["param"]["id"]=z["id"] # id folder #
                        i=i+1
                        break
        # get list user #
        if i != 0 :
            old_url_get_list_user=data["contact"]["get_list_user"]["url"]
            url_get_list_user=change(new_domain,old_url_get_list_user,old_domain)
            param_get_list_user=data["contact"]["get_list_user"]["param"]
            json_list_data=data["contact"]["list_user"]
            success_get_list_user=post( url_get_list_user,param_get_list_user,cookie_writer(new_domain))
            if notification(success_get_list_user)== True :
                for x in success_get_list_user["rows"]:
                    for y in json_list_data:
                        if x["id"]== y :
                            json_list_data[x["id"]]["ucn"]=x["ucn"]
                            json_list_data[x["id"]]["userno"]=x["userno"]
                            json_list_data[x["id"]]["seqno"]=x["seqno"]
                            json_list_data[x["id"]]["cn"]=x["cn"]
                for x in json_list_data :
                    if x== user_id :
                        user.append(json_list_data[user_id]["ucn"])
                        user.append(json_list_data[user_id]["userno"])
                        user.append(json_list_data[user_id]["seqno"])
                        user.append(json_list_data[user_id]["cn"])
                        break
                return user

def user_data(data):
    userno=str(data["rows"]["user_config"]["user_data"]["ucn"]) + "_" +str(data["rows"]["user_config"]["user_data"]["userno"])
    return userno

def userno(new_domain):
    account=data["account"]["account"]
    old_userno=data["account"]["config"]
    url_userno=change(new_domain,old_userno,old_domain)

    info_userno=get(url_userno,"",account_one(new_domain))
    account["account1"]=user_data(info_userno)

    info_userno=get(url_userno,"",account_two(new_domain))
    account["account2"]=user_data(info_userno)

    info_userno=get(url_userno,"",account_thr(new_domain))
    account["account3"]=user_data(info_userno)

    return account

def user_id(data):
    userid=str(data["rows"]["user_config"]["user_data"]["id"])
    return userid

def userid(new_domain):
    account=data["account"]["account"]
    old_userno=data["account"]["config"]
    url_userno=change(new_domain,old_userno,old_domain)

    info_userno=get(url_userno,"",account_one(new_domain))
    account["account1"]=user_id(info_userno)

    info_userno=get(url_userno,"",account_two(new_domain))
    account["account2"]=user_id(info_userno)

    info_userno=get(url_userno,"",account_thr(new_domain))
    account["account3"]=user_id(info_userno)

    return account


def user_name(data):
    username=str(data["rows"]["user_config"]["user_data"]["name"])
    return username

def username(new_domain):
    account=data["account"]["account"]
    old_userno=data["account"]["config"]
    url_userno=change(new_domain,old_userno,old_domain)

    info_userno=get(url_userno,"",account_one(new_domain))
    account["name1"]=user_name(info_userno)

    info_userno=get(url_userno,"",account_two(new_domain))
    account["name2"]=user_name(info_userno)

    info_userno=get(url_userno,"",account_thr(new_domain))
    account["name3"]=user_name(info_userno)

    return account
def depart_name(data):
    username=str(data["rows"]["user_config"]["user_data"]["baseno"])
    return username + "_0"

def depart(new_domain):
    account=data["account"]["account"]
    old_userno=data["account"]["config"]
    url_userno=change(new_domain,old_userno,old_domain)

    info_userno=get(url_userno,"",account_one(new_domain))
    account["depart1"]=depart_name(info_userno)

    info_userno=get(url_userno,"",account_two(new_domain))
    account["depart2"]=depart_name(info_userno)

    info_userno=get(url_userno,"",account_thr(new_domain))
    account["depart3"]=depart_name(info_userno)

    return account

# Note pahir xóa #
def api(api_head,param):
    api=""
    for x in param :
        api= api + x +"=" +param[x] +'&' 
    url= api_head + api
    url = url[:-1]
    return url 

def head_menu(menu) :
    print(" ")
    print(menu)

def another_user(new_domain):
    url=data["login"]["api_login"]
    url_login=change(new_domain,url,old_domain)
    param_login = {'gw_id': data["login"]["id_ts6"],'gw_pass':data["login"]["pw_ts6"]}
    success=post(url_login,param_login,cookies="")
    return {"HANBIRO_GW":success["session"],"hmail_key":success["hmail_key"]}

def cookie_user(new_domain,id_user):
    url=data["login"]["api_login"]
    url_login=change(new_domain,url,old_domain)
    param_login = {'gw_id': data["login"][id_user],'gw_pass':data["login"]["common_pass"]}
    success=post(url_login,param_login,cookies="")
    return {"HANBIRO_GW":success["session"],"hmail_key":success["hmail_key"]}

def msg_execution_test_link(status,id,text):
    #msg("p","-Create work type => Pass")
    #execution_test_link("WAPI-105","p")
    if status == "p":
        msg(status, text +" => Pass")
        execution_test_link(id,status)
    else :
        msg(status, text +" => Fail")
        execution_test_link(id,status)

def result(response,msg_list):
    if notification(response) == True :
        msg("p",msg_list["pass"])
    else :
        msg("f",msg_list["fail"])
   