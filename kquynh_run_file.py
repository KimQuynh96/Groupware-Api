import os.path,json
from colorama import Fore, Back, Style
from colorama import init, AnsiToWin32
from pathlib import Path
from os import path
from sys import platform
from kquynh_function_gw import msg
from kquynh_param_gw import run
from kquynh_login import domain_list
import kquynh_login,kquynh_whisper,kquynh_mail,kquynh_comanage,kquynh_board,kquynh_project,kquynh_resource,kquynh_asset,kquynh_expense






param=json.loads(run())

# Many domain #
#domain_list=["kimquynh.hanbiro.net"]
print("domain_list :",domain_list)
for domain in domain_list :
    result_load_ui_login=kquynh_login.load_ui(domain)
    if result_load_ui_login == False:
        msg("f",param["load_ui"])
    else:
        result_login=kquynh_login.login_correct(domain)

        if  result_login["login_correct"] == True :
            '''
            kquynh_login.login_wrong(domain)
            kquynh_whisper.whisper(domain)
            kquynh_mail.mail(domain)
            kquynh_comanage.co_manage(domain)
            #kquynh_board.board(domain)
            kquynh_project.project(domain)
            kquynh_resource.resource(domain)
            kquynh_expense.expense(domain)
            '''
            kquynh_asset.asset(domain)
            








   





   
   
   
    
    

    
   




        
