import json,datetime,time
from sys import dont_write_bytecode
from kquynh_function_gw import data,check_the_saved_data,notification,send_mail,account_two,account_one,post,post_header,get,cookie_writer,cookie_recipient,msg,next_page,id_user,head_menu,another_user,cookie_user,old_domain
from kquynh_param_gw import mail_menu
msg_mail = data['mail_msg']

def result_msg(result,msg_list):
    if result == True :
        msg("p",msg_list["pass"])
    else :
        msg("f",msg_list["fail"])

def result_view(response,msg_list):
    if len(response["mailview"]) != 0 :
        msg("p",msg_list["pass"])
    else :
        msg("p",msg_list["fail"])

def delete_mail(response,result,msg_list):
    if response["success"] == str(1) :
        result == True
        msg("p",msg_list["pass"])
    else :
        msg("f",msg_list["fail"])
    return result

def mail_removed(total_before,list_after,id,msg_list):
    check_removed =True
    if len(list_after) == 0 :
        if total_before == 1 :
            msg("p",msg_list["pass"])
        else:
            msg("p",msg_list["fail"])
    else :
        for mail in list_after:
            if mail["mid"] == id :
                check_removed == False
                break
        if check_removed == True :
            msg("p",msg_list["pass"])
        else :
            msg("p",msg_list["fail"])

def mail(new_domain):
    head_menu("III.MAIL")
    print("Send Mail")
    param=json.loads(mail_menu(new_domain))
    # Url #
    ur_inbox_list = param["ur_mail_list"]
    ur_sent_list = param["ur_sent_list"]
    title_reply = param["title_reply"]
    
    # Compose mail #
    check_compose = False
    title_mail = param["title_mail"]
    ur_compose = param["url_compose"]
    pr_compose = param["pr_compose"]
    response_compose = post(ur_compose,pr_compose,account_one(new_domain))
    if notification(response_compose) == True :
        check_compose = True
        msg("p",msg_mail["pass_compose"])
    else :
        msg("f",msg_mail["fail_compose"])

    # Check received mail #
    time.sleep(10)
    response_mail_list=get(ur_inbox_list,"",account_two(new_domain))
    if  "maillist" in response_mail_list:
        if check_compose == True :
            result_received = check_the_saved_data(response_mail_list,title_mail,"subject","maillist")
            received_list = param["inbox_received"]
            result_msg(result_received,received_list)
    else :
        msg("f",msg_mail["fail_get_list"])
    
    # Check sent mail #
    response_sent_list=get(ur_sent_list,"",account_one(new_domain))
    if  "maillist" in response_sent_list:
        if check_compose == True :
            result_sent = check_the_saved_data(response_sent_list,title_mail,"subject","maillist")
            sent_list = param["sent_list"]
            result_msg(result_sent,sent_list)
    else :
        msg("f",msg_mail["fail_get_list"])

    # Reply mail #
    check_reply = False 
    if  "maillist" in response_mail_list:
        if len(response_mail_list["maillist"]) == 0 :
            msg("p",msg_mail["pass_no_reply"])
        else :
            id_mail = response_mail_list["maillist"][0]["mid"]
            ur_reply = param["ur_reply"] + id_mail
            pr_reply = param["pr_reply"]
            pr_reply["mailid"] = id_mail 
            response_reply = post(ur_reply,pr_reply,account_two(new_domain))
            if response_reply["msg"] == "mail sent success!!" and notification(response_reply) == True :
                check_reply = True 
                msg("p",msg_mail["pass_reply"])
            else :
                msg("f",msg_mail["fail_reply"])

    # Check reply received #
    if check_reply == True :
        time.sleep(10)
        response_mail_list=get(ur_inbox_list,"",account_one(new_domain))
        if  "maillist" in response_mail_list:
            if check_compose == True :
                result_received = check_the_saved_data(response_mail_list,title_reply,"subject","maillist")
                received_list = param["reply_received"]
                result_msg(result_received,received_list)
        else :
            msg("f",msg_mail["fail_received_reply"])
       
    # Check reply sent #
    if check_reply == True :
        response_sent_list=get(ur_sent_list,"",account_two(new_domain))
        if  "maillist" in response_sent_list:
            if check_compose == True :
                result_sent = check_the_saved_data(response_sent_list,title_reply,"subject","maillist")
                sent_list = param["reply_sent"]
                result_msg(result_sent,sent_list)
        else :
            msg("f",msg_mail["fail_sent_reply"])
    
    msg("t","Submenu Inbox")
    response_inbox_list = get(ur_inbox_list,"",account_two(new_domain))
    if  "maillist" in response_inbox_list:
        total_mail = response_inbox_list["total"]
        if total_mail != 0 :

            # View #
            id_view = response_inbox_list["maillist"][0]["mid"]
            ur_view = param["ur_view"] + id_view
            response_inbox_view = get(ur_view," ",account_two(new_domain))
            view_list = param["inbox_view"]
            result_view(response_inbox_view,view_list)

            # Delete #
            result_delete = False
            ur_delete = param["ur_delete"]
            pr_delete = param["pr_delete"]
            id_delete = response_inbox_list["maillist"][0]['mid']
            pr_delete["mid"] = id_delete
            response_delete = post(ur_delete,pr_delete,account_two(new_domain))
            inbox_delete = param["inbox_delete"]
            result_delete = delete_mail(response_delete,result_delete,inbox_delete)
            
            # Removed #
            if result_delete == True :
                response_inbox_list = get(ur_inbox_list,"",account_two(new_domain))
                mail_list_after = response_inbox_list["maillist"]
                inbox_removed = param["inbox_removed"]
                mail_removed(total_mail,mail_list_after,id_delete,inbox_removed)
        else :
            msg("p",msg_mail["pass_no_mail"])

    msg("t","Submenu Sent")
    response_sent_list = get(ur_sent_list,"",account_one(new_domain))
    if  "maillist" in response_sent_list:
        total_mail = response_inbox_list["total"]
        if total_mail != 0 :

            # View #
            id_view = response_sent_list["maillist"][0]["mid"]
            ur_view_sent = param["ur_view_sent"] + id_view
            response_inbox_view = get(ur_view_sent," ",account_one(new_domain))
            view_list = param["sent_view"]
            result_view(response_inbox_view,view_list)

            # Delete #
            result_delete = False
            ur_delete = param["ur_delete"]
            pr_delete = param["pr_delete"]
            pr_delete["acl"] = "Sent"
            id_delete = response_sent_list["maillist"][0]['mid']
            pr_delete["mid"] = id_delete
            response_delete = post(ur_delete,pr_delete,account_one(new_domain))
            sent_delete = param["sent_delete"]
            result_delete = delete_mail(response_delete,result_delete,sent_delete)
            
            # Removed #
            if result_delete == True :
                response_sent_list = get(ur_inbox_list,"",account_one(new_domain))
                mail_list_after = response_sent_list["maillist"]
                sent_removed = param["sent_removed"]
                mail_removed(total_mail,mail_list_after,id_delete,sent_removed)
        else :
            msg("p",msg_mail["pass_no_mail"])
        
            


            


    