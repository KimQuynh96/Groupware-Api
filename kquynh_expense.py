import json
from datetime import date
from os import pardir
from kquynh_function_gw import data,account_one,head_menu,account_two,account_thr,userno,date_time,post,get,notification,msg,delete,create_url,result_add
from kquynh_param_gw import expense_menu
param_msg=data["expense_msg"]
vehicle_name="Resource Vehicle " + date_time
room_name="Room " + date_time



def add_expense(param,new_domain):
    # Add folder #
    title_folder = param["title_folder"]
    check_add = False
    ur_add_folder = param["ur_add_folder"]
    pr_add_folder = param["pr_add_folder"]
    add_msg = param["add_msg"]
    
    response_add_folder = post(ur_add_folder,pr_add_folder,account_one(new_domain))
    check_add = result_add(response_add_folder,check_add,add_msg)
    
    # Check added folder #
    category_id =""
    result_displayed = False
    if check_add == True :
        response_folder_list = get(param["ur_list_folder"],"",account_one(new_domain))

        if notification(response_folder_list) == True :
            if len(response_folder_list["rows"]) == 0 :
                msg("p",param_msg["fail_folder_displayed"])
            else :
                for folder in response_folder_list["rows"] :
                    if folder["text"] == title_folder :
                        category_id = folder["id"]
                        result_displayed = True
                        break
                if  result_displayed == True :
                    msg("p",param_msg["pass_folder_displayed"])
                else :
                    msg("p",param_msg["fail_folder_displayed"])
        else :
            msg("p",param_msg["fail_folder_list"])

    # Add expense #
    id_expense = "" 
    check_expense = False 
    expense_msg = param["expense_msg"]
    ur_add_expense = param["ur_add_expense"]
    pr_add_expense = param["pr_add_expense"]

    if category_id != "":
        pr_add_expense["category_id"] = category_id
        response_add_expense = post(ur_add_expense,pr_add_expense,account_one(new_domain))
        check_expense = result_add(response_add_expense,expense_msg,add_msg)

    else :
        response_folder_list = get(param["ur_list_folder"],"",account_one(new_domain))
        if notification(response_folder_list) == True :
            if len(response_folder_list["rows"]) == 0 :
                category_id = ""
            else :
                category_id = response_folder_list["rows"][0]["id"]


    if check_expense == True :
        title_expense = param["title_expense"]
        result_displayed = False
        pr_expense_list = param["pr_expense_list"]
        ur_expense_list = param["ur_expense_list"]
        pr_expense_list["category"] = category_id
        response_expense_list = post(ur_expense_list ,pr_expense_list, account_one(new_domain))
        if notification(response_expense_list) == True :
            if len(response_expense_list["rows"]) == 0 :
                msg("p",param_msg["fail_expense_displayed"])
            else :
                for expesnse in response_expense_list["rows"] :
                    if expesnse["title"] == title_expense :
                        id_expense = expesnse["id"]
                        result_displayed = True
                        break

                if  result_displayed == True :
                    msg("p",param_msg["pass_expense_displayed"])
                else :
                    msg("p",param_msg["fail_expense_displayed"])

    # Delete expense #
    ur_delete_expense = param["ur_delete_expense"]
    pr_delete_expense = param["pr_delete_expense"]
    if id_expense != 0 :
        pr_delete_expense["id[0]"] = id_expense
        response_delete = post(ur_delete_expense,pr_delete_expense,account_one(new_domain))
        if response_delete == True :
            msg("p",param_msg["pass_delete_expense"])
        else :
            msg("f",param_msg["fail_delete_expense"])

    





        
        
    

def expense(new_domain):
    head_menu("MENU : EXPENSE")
    param = json.loads(expense_menu(new_domain))
    user_no = userno(new_domain)
    add_expense(param,new_domain)