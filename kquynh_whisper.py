import json
from math import e
from kquynh_function_gw import account_two, data,check_the_saved_data,notification,post,msg,head_menu,account_one
from kquynh_param_gw import whiper_menu,date_time
msg_wh=data["whisper_msg"]

def all_list_inbox(url,param,cookies,value):
    array=[]
    j=1
    success_list_inbox=post(url,param,cookies)
    if notification(success_list_inbox)== True :
        maxpage=int(success_list_inbox["attr"]["maxPage"])
        while j<=maxpage :
            param['page']=j
            success_list_inbox1=post(url,param,cookies)
            if len(success_list_inbox1["rows"])==0 :
                return array
                
            else :
                for x in success_list_inbox1["rows"] :
                    array.append(x[value]) 
            j=j+1
        return array
    else :
        return False

def search(content,value,search_by_sender,url_list_inbox,param_list_inbox,cookie_recipient,url_list_search,param_list_search):
    list_inbox=all_list_inbox(url_list_inbox,param_list_inbox,cookie_recipient(),value)
    def result_list():
        i=0
        if len(list_inbox)==0 :
            return False
        else:
            for x in list_inbox :
                if x == search_by_sender :
                    i=i+1 
            return i
    list_search=all_list_inbox(url_list_search,param_list_search,cookie_recipient(),value)
    def result_search():
        j=0
        for x in list_search :
            if x == search_by_sender :
                j=j+1 
            else :
                return False
        return j

    if result_list()== False :
        if len(list_search)== 0 :
            result="-"+ content + " in Inbox => Pass 1"
            msg("p",result)
            
        else:
            result="-"+ content + " in Inbox => Fail 1"
            msg("f",result)
            
    else :
        if len(list_search)== 0 :
            result="-"+ content + " in Inbox => Fail 2"
            msg("f",result)
            
        else :
            if result_search() == False :
                result="-"+ content + " in Inbox(The search contained false results) => Fail 3"
                msg("f",result)
                
            else :
                if result_list() == result_search() :
                    result="-"+ content + " in Inbox => Pass 1"
                    msg("p",result)

def view_whisper(response_view,msg_list):
    
    if notification(response_view)== True :
        msg("p",msg_list["pass_view"])
        
    else :
        msg("p",msg_list["fail_view"])

def delete_whisper(response,result,msg_list):
    if notification(response) == True :
        result == True
        msg("p",msg_list["pass_delete"])
    else :
        msg("f",msg_list["fail_delete"])
    return result

def whisper_removed(total_before,list_after,id,msg_list):
    check_removed =True
    if len(list_after) == 0 :
        if total_before == 1 :
            msg("p",msg_list["pass_removed"])
        else:
            msg("p",msg_list["fail_removed"])
    else :
        for whisper in list_after:
            if whisper["unique_id"] == id :
                check_removed == False
                break
        if check_removed == True :
            msg("p",msg_list["pass_removed"])
        else :
            msg("p",msg_list["fail_removed"])

def whisper(new_domain):
    head_menu("WHISPER")
    msg("t","Send Whisper")
    param = json.loads(whiper_menu(new_domain))

    # Url #
    ur_inbox_list = param["url_list_inbox"]
    pr_sent_list = param["param_list_send"]
    ur_view_whisper = param["url_view_whisper"]
    pr_view_whisper = param["param_view_whisper"]
    ur_delete_whisper =  param["url_delete_whisper"]
    pr_delete_whisper = param["pr_delete_whisper"]

    # Send Whiper #
    check_send = False
    ur_send = param["url_send"]
    pr_send = param["param_send"]
    response_send = post(ur_send,pr_send,account_one(new_domain))
    if notification(response_send) == True:
        check_send = True 
        msg("p",msg_wh["pass_send"])
    else :
        msg("f",msg_wh["fail_send"])

    # Check Received Whisper #
    if check_send == True :
        title = "whisper " +date_time
        pr_inbox_list = param["param_list_inbox"]
        response_received_list = post(ur_inbox_list,pr_inbox_list,account_two(new_domain))
        if notification(response_received_list) == True :
            result_received_whisper = check_the_saved_data(response_received_list,title,"memo","rows")
            if result_received_whisper == True :
                msg("p",msg_wh["pass_received_whisper"])
            else :
                msg("f",msg_wh["fail_received_whisper"]) 
        else:
            msg("f",msg_wh["fail_inbox_list"])

    # Check Whisper Sent #
        response_sent_list = post(ur_inbox_list,pr_sent_list,account_one(new_domain))
        if notification(response_sent_list) == True :
            result_sent_whisper = check_the_saved_data(response_sent_list,title,"memo","rows")
            if result_sent_whisper == True :
                msg("p",msg_wh["pass_sent_whisper"])
            else :
                msg("f",msg_wh["fail_sent_whisper"]) 
        else:
            msg("f",msg_wh["fail_sent_list"])

    
    msg("t","Submenu Inbox")
    response_list_inbox =  post(ur_inbox_list,pr_inbox_list,account_two(new_domain))
    if notification(response_list_inbox) == True :
        total_whisper_before = len(response_list_inbox["rows"])

        if total_whisper_before != 0:
            # View Whisper #
            pr_view_whisper["param"] = response_list_inbox["rows"][0]["unique_id"]
            response_view = post(ur_view_whisper,pr_view_whisper,account_two(new_domain))
            msg_view = param["list_inbox_view"]
            view_whisper(response_view,msg_view)
            
            # Delete whisper #
            result_delete = False
            id_whisper_delete = response_list_inbox["rows"][0]["unique_id"] 
            pr_delete_whisper["list_id"] = id_whisper_delete
            response_delete = post(ur_delete_whisper,pr_delete_whisper,account_two(new_domain))
            msg_delete = param["inbox_delete"]
            result_delete = delete_whisper(response_delete,result_delete,msg_delete)

            # Whisper is removed #
            if result_delete == True :
                response_list_inbox_after =  post(ur_inbox_list,pr_inbox_list,account_two(new_domain))
                list_after = response_list_inbox_after["rows"]
                msg_removed = param["inbox_removed"]
                whisper_removed(total_whisper_before,list_after,id_whisper_delete,msg_removed)

               

    msg("t","submenu sentbox ")
    response_sent_list = post(ur_inbox_list,pr_sent_list,account_one(new_domain))
    if notification(response_sent_list) == True :
        total_whisper_before = len(response_sent_list["rows"])
        if total_whisper_before != 0:

            # View Whisper #
            pr_view_whisper["type"] = "sentbox"
            pr_view_whisper["param"] = response_sent_list["rows"][0]["unique_id"]
            response_view = post(ur_view_whisper,pr_view_whisper,account_one(new_domain))
            msg_view = param["list_sent_view"]
            view_whisper(response_view,msg_view)
        
            # Delete whisper #
            result_delete = False
            id_whisper_delete = response_sent_list["rows"][0]["unique_id"] 
            pr_delete_whisper["type"] = "sentbox"
            pr_delete_whisper["list_id"] = id_whisper_delete
            response_delete = post(ur_delete_whisper,pr_delete_whisper,account_one(new_domain))
            msg_delete = param["inbox_delete"]
            result_delete = delete_whisper(response_delete,result_delete,msg_delete)
            
            # Whisper is removed #
            if result_delete == True :
                response_list_sent_after =  post(ur_inbox_list,pr_sent_list,account_two(new_domain))
                list_after = response_list_sent_after["rows"]
                msg_removed = param["sent_removed"]
                whisper_removed(total_whisper_before,list_after,id_whisper_delete,msg_removed)
    
           

    
    



