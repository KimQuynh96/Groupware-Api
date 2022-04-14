import json
from datetime import date
from os import pardir
from kquynh_function_gw import data,account_one,head_menu,account_two,account_thr,userno,date_time,post,get,notification,msg,delete,create_url
from kquynh_param_gw import project_menu,project_msg
param_msg=json.loads(project_msg())


def project_list(response_mypro):
    # List Project Has No Project #
    if len(response_mypro["rows"]) == 0 :
        return False
    # List Project Has Project #
    else:
        return True

def response_list(param,new_domain):
    # List Project #
    result_list_mypro=param["result_list_mypro"]
    ur_mypro=param["url_get_mypro"]
    pr_mypro=param["pr_get_mypro"]
    response_mypro=post(ur_mypro,pr_mypro,account_one(new_domain))
    if notification(response_mypro) == True :
        result_list_mypro["response_list"]=True
        msg("p",param_msg["pass_list_mypro"])
    else:
        result_list_mypro["response_list"]=False
        msg("f",param_msg["fail_list_mypro"])
    return result_list_mypro

def create_project(param,new_domain,user_no):
    # My Project List #
    ur_mypro=param["url_get_mypro"]
    pr_mypro=param["pr_get_mypro"]

    
    # Create Project #
    check_create=False
    pr_pro=param["pr_create_pro"]
    ur_pro=param["url_create_pro"]
    response_create_pro=post(ur_pro,pr_pro,account_one(new_domain))
    
    if notification(response_create_pro) == True :
        check_create= True
        msg("p",param_msg["pass_create_pro"])
    else:
        msg("f",param_msg["fail_create_pro"])

    # List Project #
    result_my_pro=response_list(param,new_domain)

   
    # Check Created Project #
    if result_my_pro["response_list"] == True :
        if  check_create == True :
            check_displayed_pro=False
            response_list_mypro=post(ur_mypro,pr_mypro,account_one(new_domain))
            list_project=project_list(response_list_mypro)

            # Project List Has Project > Check Created Project Is In The List #
            if list_project == True :
                for project in response_list_mypro["rows"] :
                    if project["subject"] == "Project "+ date_time:
                        id_pro = project["seq_no"]
                        check_displayed_pro=True 
                        break
                if check_displayed_pro== True :
                    msg("p",param_msg["pass_pro_in_list"])
                else:
                    msg("f",param_msg["fail_pro_in_list"])
                
                 # Check Information of Created Project #
                if  check_displayed_pro == True :
                    # Check Leader #
                    check_leader = False
                    ur_detail_pro=param["url_detail_pro"] + id_pro
                    response_detail_pro = get(ur_detail_pro,"",account_one(new_domain))
                    if notification(response_detail_pro) == True :
                        id_leader = str(response_detail_pro["rows"]["ucn"]) + "_" + str(response_detail_pro["rows"]["userno"])
                        if id_leader == user_no["account1"] :
                            check_leader = True
                
                        if  check_leader == True :
                            msg("p",param_msg["pass_leader_pro"])
                        else:
                            msg("f",param_msg["fail_leader_pro"])

                    # Check Participant #
                    check_participant = False
                    ur_modify_pro = param["url_modify_pro"] + id_pro
                    response_modify_pro = get(ur_modify_pro,"",account_one(new_domain))
                    if notification(response_modify_pro) == True :
                        for participant in response_modify_pro["rows"]["part_user"] :
                            id_participant = str(participant["cn"]) + "_" + str(participant["userno"])
                            if id_participant == user_no["account2"] :
                                check_participant = True
                                break
                        if check_participant == True :
                            msg("p",param_msg["pass_par_pro"])
                        else:
                            msg("f",param_msg["fail_par_pro"])

                    if check_participant == True and check_leader == True :
                        msg("p",param_msg["pass_detail_pro"])
                    else:
                        msg("f",param_msg["fail_detail_pro"])

            # Project List Has No Project > The Created Project Not In The List #
            else :
                msg("f",param_msg["fail_pro_in_list"])
               
    # Delete Project #
    ur_mypro=param["url_get_mypro"]
    pr_mypro=param["pr_get_mypro"]
    response_list_mypro_delete=post(ur_mypro,pr_mypro,account_one(new_domain))
    if notification(response_list_mypro_delete) == True :
        list_project = project_list(response_list_mypro_delete)
        total_project_before = len(response_list_mypro_delete["rows"])

        # Project List Has Project > Get Id Of Project #
        if list_project == True :
            for project in response_list_mypro_delete["rows"] :
                project_id_to_delete = project["seq_no"]
                break

            check_delete_pro=False
            pr_delete_pro=param["pr_delete_pro"]
            pr_delete_pro["pseq"]=project_id_to_delete
            url_delete_pro=param["url_delete_pro"]
            response_deletepro=post(url_delete_pro,pr_delete_pro,account_one(new_domain))
            if notification(response_deletepro) == True :
                check_delete_pro= True
                msg("p",param_msg["pass_delete_pro"])

            else :
                msg("f",param_msg["fail_delete_pro"])

            # Check Deleted Project #
            check_removed_pro=True
            if check_delete_pro == True :
                response_mypro=post(ur_mypro,pr_mypro,account_one(new_domain))
                if notification(response_mypro) == True :
                    list_project=project_list(response_mypro)
                if list_project == True:
                    for project in response_mypro["rows"] :
                        if  project["seq_no"]== project_id_to_delete :
                            check_removed_pro = False
                            break 
                    if check_removed_pro == True :
                        msg("p",param_msg["pass_removed_pro"])
                    else:
                        msg("f",param_msg["fail_removed_pro"])
                else:
                    if total_project_before == 1 :
                        msg("p",param_msg["pass_removed_pro"])
                    else:
                        msg("f",param_msg["fail_removed_pro"])


        # Project List Has No Project > No Project to delete #
        else :
            msg("p",param_msg["pass_no_project_dele"])
    

def work(param,new_domain,user_no):
    # List Project #
    ur_mypro=param["url_get_mypro"]
    pr_mypro=param["pr_get_mypro"]
    result_my_pro=response_list(param,new_domain)
    
   
    # Create Work #
    if result_my_pro["response_list"] == True :
        response_mypro_list=post(ur_mypro,pr_mypro,account_one(new_domain))
        list_project=project_list(response_mypro_list)

        # Project List Has Project > Get Project id to create work #
        if list_project == True :
            check_work=False
            id_project=response_mypro_list["rows"][0]["seq_no"]
            pr_create_wk = data["project"]["create_wk"]["param"]
            pr_create_wk["pseq"] =id_project
            ur_create_wk=param["url_create_wk"]  

            response_wk=post(ur_create_wk,pr_create_wk,account_one(new_domain))
            if notification(response_wk) == True :
                check_work=True
                msg("p",param_msg["pass_create_wk"])
            else:
                msg("f",param_msg["fail_create_wk"])

            
            # If Work Has Been Created > Check Created Work #
            if check_work == True :
                ur_list_work=param["url_list_work"]
                pr_list_work=param["pr_list_work"]
                pr_list_work["pseq"]=id_project
                response_listwork=post(ur_list_work,pr_list_work,account_one(new_domain))
                if notification(response_listwork) == True :

                    # If Work List Has Work > Check Created Work Is In The List # 
                    check_displayed_wk = False
                    if len(response_listwork["rows"]) != 0 :
                        for work in response_listwork["rows"]:
                            if work["subject"] == "Work " + date_time :
                                id_pro_to_detail=response_listwork["rows"][0]["seq_no"]
                                id_work_to_detail=response_listwork["rows"][0]["taseq_no"]
                                check_displayed_wk = True
                            
                        if  check_displayed_wk == True :
                            msg("p",param_msg["pass_wk_in_list"])
                        else :
                            msg("f",param_msg["fail_wk_in_list"])

                        # Check Information Of Created Work #
                        if  check_displayed_wk == True :
                            
                            pr_detail_wk = param["pr_detail_wk"]
                            pr_detail_wk["pseq"] = id_pro_to_detail
                            pr_detail_wk["taseq"] = id_work_to_detail
                            url_detail_wk = param["url_detail_wk"]
                            ur_detail_wk = create_url(url_detail_wk,pr_detail_wk)
                            print("ur_detail_wk ",ur_detail_wk)
                            response_detail_wk = get(ur_detail_wk,"",account_one(new_domain))
                            if notification(response_detail_wk) == True :
                                msg("f",param_msg["pass_detail_wk"])
                                info_work=response_detail_wk["rows"]
                                pr_create_wk = param["pr_create_wk"]
                                print(response_detail_wk)

                                # Check Content Work #
                                if info_work["content"] == pr_create_wk["content"] :
                                    msg("p",param_msg["pass_content_wk"])
                                else:
                                    msg("f",param_msg["fail_content_wk"])
                                
                                # Check Subject Work #
                                if info_work["subject"] == pr_create_wk["subject"] :
                                    msg("p",param_msg["pass_subject_wk"])
                                else:
                                    msg("f",param_msg["fail_subject_wk"])

                                # Check Subject Work #
                                if info_work["assignee"] == pr_create_wk["assignee"] :
                                    msg("p",param_msg["pass_assignee_wk"])
                                else:
                                    msg("f",param_msg["fail_assignee_wk"])
                                
                                # Check Subject Work #
                                if info_work["start_date"] == pr_create_wk["start_date"] and info_work["due_date"] == pr_create_wk["due_date"]:
                                    msg("p",param_msg["pass_assignee_wk"])
                                else:
                                    msg("f",param_msg["fail_assignee_wk"])

                            else:
                                msg("f",param_msg["fail_detail_wk"])

                    # If Work List Has No Work > The Created Work Not In The List #  
                    else:
                        msg("f",param_msg["fail_wk_in_list"])
        else:
            msg("p",param_msg["pass_no_project"])
   
    
    # Delete Work #
    if result_my_pro["response_list"] == True :
        response_mypro_delete=post(ur_mypro,pr_mypro,account_one(new_domain))
        list_project_delete=project_list(response_mypro_delete)

        # If Project List Has Project #
        if list_project_delete == True :
            id_project_has_work = 0
            for project in response_mypro_delete["rows"] :
                # Find Project Has Work > Get Project Id To Get Work List Of Project #
                if project["work_count"] !=0 :
                    id_project_has_work=project["seq_no"]
                    break

            # Get Id Of Work #
            if id_project_has_work != 0 :
                ur_list_work=param["url_list_work"]
                pr_list_work=param["pr_list_work"]
                pr_list_work["pseq"]=id_project_has_work
                response_listwork=post(ur_list_work,pr_list_work,account_one(new_domain))
                    
                # Delete work #
                check_delete_work=False
                if notification(response_listwork) == True :
                    pr_delete_wk=param["pr_delete_wk"]
                    url_delete_wk=param["url_delete_wk"]
                    pr_delete_wk["pseq"]=response_listwork["rows"][0]["seq_no"]
                    pr_delete_wk["taseq"]=response_listwork["rows"][0]["taseq_no"]
                    ur_delete_wk=create_url(url_delete_wk,pr_delete_wk)
                    response_deletework=delete(ur_delete_wk,"",account_one(new_domain))
                    if notification(response_deletework) == True :
                        check_delete_work = True
                        msg("p",param_msg["pass_delete_work"])
                    else:
                        msg("f",param_msg["fail_delete_work"])

                    # Check Deleted Work #
                    if check_delete_work == True :
                        check_removed_work = True
                        response_listwork=post(ur_list_work,pr_list_work,account_one(new_domain))
                        if len(response_listwork["rows"]) == 0 :
                            msg("p",param_msg["pass_removed_wk"])
                        else:
                            for work in response_listwork["rows"]:
                                if work["subject"] == "Work "+date_time :
                                    check_removed_work=False
                                    break
                            if  check_removed_work == True :
                                msg("p",param_msg["pass_removed_wk"])
                            else :
                                msg("f",param_msg["fail_removed_wk"])
   
def project(new_domain):
    head_menu("MENU : PROJECT")
    param=json.loads(project_menu(new_domain))
    user_no=userno(new_domain)
    #create_project(param,new_domain,user_no)
    work(param,new_domain,user_no)

   

    




