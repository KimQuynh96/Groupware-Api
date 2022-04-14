import json,random,datetime
from datetime import date
from sys import platform
from random import choice,randint
from kquynh_function_gw import change,data,old_domain,username,userno,date_time,userid,create_url,url,api,depart,today

def login(new_domain):
    par= {
    "url_login":"http://"+new_domain+"/ngw/sign/auth",
    "url_load_ui":"http://"+new_domain+"/ngw/app/",
    "param_login_ri":{'gw_id': data["account"]["id_us_one"],'gw_pass': data["account"]["pw_us_one"]},
    "param_login_pw":{'gw_id': data["login"]["id_user"],'gw_pass': data["login"]["pw_wrong"]},
    "param_login_iw":{'gw_id': data["login"]["id_wrong"],'gw_pass': data["login"]["passwword_user"]},
    "result_login": {"login_correct":"","pass_changed":"","no_response":"","id":"" ,"no_ui":""},
    "account":{"id":"","pass":""},
    "id_pass":"-Id correct & Password correct <Pass>",
    "pass_changed":"The ID or password you entered is incorrect.(2)",
    "id_exist":"You do not have permission to access.",
    "fail_pass":"-Id correct & Password wrong <Fail>",
    "pass_pass":"-Id correct & Password wrong <Pass>",
    "pass_id":"-Id wrong & Password correct <Pass>",
    "fail_id":"-Id wrong & Password correct <Fail>",
    }
    return json.dumps(par)

def account_login():
  
    par= {
    "account_one":{'gw_id': data["account"]["id_us_one"],'gw_pass': data["account"]["pw_us_one"]},
    "account_two":{'gw_id': data["account"]["id_us_two"],'gw_pass': data["account"]["pw_us_two"]},
    "account_thr":{'gw_id': data["account"]["id_us_thr"],'gw_pass': data["account"]["pw_us_thr"]},
    "account":{"account1":"","account2":"","account3":""},
    "domain":"Enter domain name " ,
    "total_domain":"Enter total domain : ",
    "total_account":"Plesae enter 3 account :",
    "enter_id":"Enter Id ",
    "enter_pw":"Enter PassWord  ",
    "note":"Domain : Run on all domains you will enter \nAccount :Enter 3 registered accounts for the domains that will enter \n",
    "range":" "
    }
    return json.dumps(par)

def run():
    par= {
    "load_ui":"-Load UI to login <Fail>",
    "pass_changed":"-Pass has changed ",
    "id_exist":"-Id does not exist",
    "no_response":"-No response <Fail> ",
    "fail_ui":"-UI is not returned <Fail>"
    }
    return json.dumps(par)

def whiper_menu(new_domain):
    user_no=userno(new_domain)
    user_name=username(new_domain)
    param_send={"to": user_no["account2"],"receivers": user_name["name2"],"upload_id":"","memo":"whisper " +date_time}
    par= {
    "url_send":"http://"+new_domain+"/ngw/whisper/main/insert",
    "param_send":param_send,
    "url_list_inbox":"http://"+new_domain+"/ngw/whisper/main/list",
    "param_list_inbox":data["whisper"]["list_inbox"]["param_list"],
    "param_list_send":data["whisper"]["list_send_box"]["param_list"],
    "url_view_whisper":"http://"+new_domain+"/ngw/whisper/main/view",
    "param_view_whisper":{"type":"inbox","param":" ","format": "html"},
    "url_delete_whisper":"http://"+new_domain+"/ngw/whisper/main/deletemultiwhisper",
    "pr_delete_whisper": data["whisper"]["delete"]["param_delete"],
    "list_inbox_view":{"pass_view":data["whisper_msg"]["pass_inbox_view"],"fail_view":data["whisper_msg"]["fail_inbox_view"]},
    "list_sent_view" :{"pass_view":data["whisper_msg"]["pass_sent_view"],"fail_view":data["whisper_msg"]["fail_sent_view"]},
    "inbox_delete":{"pass_delete":data["whisper_msg"]["pass_inbox_delete"],"fail_delete":data["whisper_msg"]["fail_inbox_delete"]},
    "sent_delete":{"pass_delete":data["whisper_msg"]["pass_sent_delete"],"fail_delete":data["whisper_msg"]["fail_sent_delete"]},
    "inbox_removed":{"pass_removed":data["whisper_msg"]["pass_inbox_removed"],"fail_removed":data["whisper_msg"]["fail_inbox_removed"]},
    "sent_removed":{"pass_removed":data["whisper_msg"]["pass_sent_removed"],"fail_removed":data["whisper_msg"]["fail_sent_removed"]},


    }
    return json.dumps(par)

def mail_menu(new_domain):
    user_id=userid(new_domain)
    ur_list="http://"+new_domain+"/email/list?"
    pr_list=data["mail"]["get_list_mail"]["param_list"]
    pr_sent_list=data["mail"]["get_list_sent"]["param_list"]
    title_mail = "Mail " + date_time
    title_reply = "Re " + date_time
    pr_compose = data["mail"]["compose_mail"]["param_write"]
    pr_compose["toaddr"] = user_id["account2"] + "@" +new_domain
    pr_compose["fromaddr"] = user_id["account1"] + "@" +new_domain
    pr_compose["subject"] = title_mail
    pr_reply = data["mail"]["reply_mail"]["param_write"]
    pr_reply["subject"] = title_reply
    pr_reply["fromaddr"] = user_id["account2"] + "@" +new_domain
    pr_reply["toaddr"] = user_id["account1"] + "@" +new_domain
    
    par={
        "title_mail" : title_mail,
        "title_reply" : title_reply,
        "pr_compose":pr_compose,
        "url_compose":"http://"+new_domain+"/email/write/Maildir",
        "ur_reply":"http://"+new_domain+"/email/write/Maildir/",
        "ur_mail_list":url(ur_list,pr_list),
        "ur_sent_list":url(ur_list,pr_sent_list),
        "pr_reply":pr_reply,
        "url_mail_reply":data["mail"]["reply_mail"]["api_write"],
        "ur_delete":"https://"+new_domain+"/cgi-bin/NEW/mailTohtml5.do?removemail=1",
        "pr_delete":data["mail"]["delete_mail"]["param_list"],
        "id":data["mail"]["delete_mail"]["param_list"]["mid"],
        "ur_view":"http://"+new_domain+"/email/Maildir/",
        "ur_view_sent":" http://"+new_domain+"/email/Sent/",
        "inbox_received":{"pass":data["mail_msg"]["pass_received"],"fail":data["mail_msg"]["fail_received"]},
        "sent_list" : {"pass":data["mail_msg"]["pass_sent"],"fail":data["mail_msg"]["fail_sent"]},
        "reply_received" : {"pass":data["mail_msg"]["pass_received_reply"],"fail":data["mail_msg"]["fail_received_reply"]},
        "reply_sent" : {"pass":data["mail_msg"]["pass_sent_reply"],"fail":data["mail_msg"]["fail_sent_reply"]},
        "inbox_view" : {"pass":data["mail_msg"]["pass_inbox_view"],"fail":data["mail_msg"]["fail_inbox_view"]},
        "inbox_delete":  {"pass":data["mail_msg"]["pass_inbox_delete"],"fail":data["mail_msg"]["fail_inbox_delete"]},
        "inbox_removed" : {"pass":data["mail_msg"]["pass_inbox_removed"],"fail":data["mail_msg"]["fail_inbox_removed"]},
        "sent_view" : {"pass":data["mail_msg"]["pass_sent_view"],"fail":data["mail_msg"]["fail_sent_view"]},
        "sent_delete":  {"pass":data["mail_msg"]["pass_sent_delete"],"fail":data["mail_msg"]["fail_sent_delete"]},
        "sent_removed" : {"pass":data["mail_msg"]["pass_sent_removed"],"fail":data["mail_msg"]["fail_sent_removed"]}
    }
    return json.dumps(par)

def comanage_menu(new_domain):
    
    number = str(random.randint(0,10000))
    color=data["comanage"]["admin"]["color"].split(',')
    color_random=random.choice(color)
    icon=data["comanage"]["admin"]["icon"].split(',')

    # param work type #
    pr_work_type = data["comanage"]["admin"]["manage_work_type"]["add_work_type"]["param"]
    pr_work_type["subject"]="Work Type " + number
    pr_work_type["color"]=color_random
    pr_work_type["icon"]=random.choice(icon)
    
    # param add status #
    pr_add_status = data["comanage"]["admin"]["manage_status"]["param"]
    pr_add_status["color"] = color_random
    pr_add_status["name"]="Status" + number
    pr_add_status["is_base"]="0"
    category_list=["To-Do","In Progress","Done"]
    category_name=choice(category_list)
    pr_add_status["category"]=data["comanage"]["admin"]["status_category"][category_name]
    
    
    # param project #
    pr_project=data["comanage"]["create_project"]["param"]
    project_name="Project" + " " + str(random.randint(0,10000))
    status_name="Status "+ str(random.randint(0,10000))
    pr_project["subject"]=pr_project["comment"]=project_name

    # param project list #
    url_pro_list = "http://"+new_domain+"/ngw/projectnew/project/list?"
    pr_pro_list = data["comanage"]["get_list_project_left"]["param"]
    pr_pro_list["page"]="1"

    # param add member #
    user_no=userno(new_domain)
    pr_add_member = data["comanage"]["basic_information"]["add_member"]["param"]
    user2 = user_no["account2"][int(user_no["account2"].rfind("_"))+1:None]
    user_list = [{"ucn":"0","no":user2,"type":2}]
    data["comanage"]["basic_information"]["add_member"]["param"]["user_list"] = user_list
    
    # param add leader #
    pr_add_leader = data["comanage"]["basic_information"]["add_leader"]["param"]
    user1 = user_no["account1"][int(user_no["account1"].rfind("_"))+1:None]
    leader = [{"ucn":"0","no":user1,"type":1}]
    pr_add_leader["user_list"] = leader

    
    old_url_head_get_project=data["comanage"]["get_list_project_left"]["url"]
   
    param_get_project=data["comanage"]["get_list_project_left"]["param"]
    param_get_project["page"]="1"
    


    old_url_head_get_list_member=data["comanage"]["basic_information"]["get_list_member"]["url"]
    url_head_get_list_member=change(new_domain,old_url_head_get_list_member,old_domain)
    old_url_init_work_type=data["comanage"]["basic_information"]["get_list_init_work_type"]
    old_url_add_wt_to_work=data["comanage"]["basic_information"]["add_work_type_to_work"]["url"]
    old_url_add_st_to_work=data["comanage"]["basic_information"]["add_work_status_work"]["url"]
    old_b_url_cretae_work=data["comanage"]["create_work"]["url"]
    old_ad_url_get_list_status= data["comanage"]["admin"]["get_list_status"]
    data["comanage"]["admin"]["manage_status"]["param"]["name"]=status_name
    data["comanage"]["admin"]["manage_status"]["param"]["description"]=status_name
    data["comanage"]["create_work"]["param"]["params[content]"]="Content work"
    data["comanage"]["create_work"]["param"]["params[subject]"]="Work " + str(datetime.datetime.now())
    data["comanage"]["create_work"]["param"]["params[start_date]"]=start_date=str(datetime.date.today()).replace("-","/")
    data["comanage"]["create_work"]["param"]["params[due_date]"]=due_date=str(datetime.date.today()).replace("-","/")
    
    par={
        #"color":data["comanage"]["admin"]["color"].split(','),
        #"icon":data["comanage"]["admin"]["icon"].split(','),
        "ur_access_pro":"http://"+new_domain+"/ngw/projectnew/project/project_setting?pseqno=",
        "ur_ad_st_list":"http://"+new_domain+"/ngw/projectnew/project/status_list_all",
        "pr_work_type":data["comanage"]["admin"]["manage_work_type"]["add_work_type"]["param"],
        "ur_work_type":"http://"+new_domain+"/ngw/projectnew/work_type/save",
        "ur_ad_wt_list":"http://"+new_domain+"/ngw/projectnew/work_type/list",
        "ur_add_status":"http://"+new_domain+"/ngw/projectnew/project/status_save",
        "pr_add_status":pr_add_status,
        "wt_name":data["comanage"]["admin"]["manage_work_type"]["add_work_type"]["param"]["subject"],
        "color":data["comanage"]["admin"]["manage_work_type"]["add_work_type"]["param"]["color"],
        "icon":data["comanage"]["admin"]["manage_work_type"]["add_work_type"]["param"]["icon"],
        "is_base":data["comanage"]["admin"]["manage_status"]["param"]["is_base"],
        "category":data["comanage"]["admin"]["manage_status"]["param"]["category"],
        "pr_project":pr_project,
        "ur_project":"http://"+new_domain+"/ngw/projectnew/project/save",
        "ur_pro_list":url(url_pro_list,pr_pro_list),
        "param_get_project":data["comanage"]["get_list_project_left"]["param"],
        "pr_add_member":pr_add_member,
        "pr_add_leader" : pr_add_leader,
        "ur_add_member":"https://"+new_domain+"/ngw/projectnew/project/add_member",
        "url_init_work_type":change(new_domain,old_url_init_work_type,old_domain),
        "param_get_list_member":data["comanage"]["basic_information"]["get_list_member"]["param"],
        "param_add_wt_to_work":data["comanage"]["basic_information"]["add_work_type_to_work"]["param"],
        "url_add_wt_to_work":change(new_domain,old_url_add_wt_to_work,old_domain),
        "url_add_st_to_work":change(new_domain,old_url_add_st_to_work,old_domain),
        "param_add_st_to_work":data["comanage"]["basic_information"]["add_work_status_work"]["param"],
        "project_name":project_name,
        "url_head_get_list_member":change(new_domain,old_url_head_get_list_member,old_domain),
        "param_b_url_cretae_work":data["comanage"]["create_work"]["param"],
        "b_url_cretae_work":change(new_domain,old_b_url_cretae_work,old_domain),
        "wt_list" : {"pass":data["comanage_msg"]["pass_wt_add"],"fail":data["comanage_msg"]["fail_wt_add"]},
        "wt_displayed" : {"pass":data["comanage_msg"]["pass_wt_displayed"],
                        "fail":data["comanage_msg"]["fail_wt_displayed"],
                        "pass_color":data["comanage_msg"]["pass_wt_color"],
                        "fail_color":data["comanage_msg"]["fail_wt_color"],
                        "pass_icon":data["comanage_msg"]["pass_wt_icon"],
                        "fail_icon":data["comanage_msg"]["fail_wt_icon"],
                        },
        "st_list" : {"pass":data["comanage_msg"]["pass_st_add"],"fail":data["comanage_msg"]["fail_st_add"]},
        "st_displayed" : {"pass":data["comanage_msg"]["pass_st_displayed"],
                        "fail":data["comanage_msg"]["fail_st_displayed"],
                        "pass_description":data["comanage_msg"]["pass_st_description"],
                        "fail_description":data["comanage_msg"]["fail_st_description"],
                        "pass_category":data["comanage_msg"]["pass_st_category"],
                        "fail_category":data["comanage_msg"]["fail_st_category"],
                        "pass_base":data["comanage_msg"]["pass_st_base"],
                        "pass_base":data["comanage_msg"]["fail_st_base"],
                        },
        "add_project" : {"pass":data["comanage_msg"]["pass_pj_add"],"fail":data["comanage_msg"]["fail_pj_add"]},
        "add_pj" : {"pass":data["comanage_msg"]["pass_pj_displayed"],"fail":data["comanage_msg"]["fail_pj_displayed"]},
        "member_list" : {"pass":data["comanage_msg"]["pass_add_member"],"fail":data["comanage_msg"]["fail_add_member"]},
        "leader_list" : {"pass":data["comanage_msg"]["pass_add_leader"],"fail":data["comanage_msg"]["pass_add_leader"]},
    }
    return json.dumps(par)

def project_menu(new_domain):
    to_day=str(date.today()).replace("-","/")
    # Create project #
    user_no=userno(new_domain)
    pr_create_pro=data["project"]["create_pro"]["param"]
    param_create_pro={"subject": "Project "+date_time,"charge": user_no["account1"],"part": user_no["account2"]}
    pr_create_pro.update(param_create_pro)
    # Create work #
    pr_create_wk=data["project"]["create_wk"]["param"]
    param_create_wk={"subject": "Work "+date_time,"content": "Content Work","start_date": to_day,"due_date":to_day,"assignee":user_no["account1"]}
    pr_create_wk.update(param_create_wk)
    pr_list_work={"page": 1,"limit": "30","pseq": ""}
    

    
    par={
        "url_create_pro":"http://"+new_domain+"/ngw/project/project/save",
        "pr_create_pro":pr_create_pro,
        "url_get_mypro":"https://"+new_domain+"/ngw/project/project/list/",
        "url_create_wk":"http://"+new_domain+"/ngw/project/task/save",
        "pr_get_mypro":data["project"]["my_pro"]["param"],
        "pr_create_wk":data["project"]["create_wk"]["param"],
        "pr_add_pseq":{"pseq":""},
        "result_list_mypro":{"response_list":False},
        "url_list_work":"http://"+new_domain+"/ngw/project/task/new_list2",
        "pr_list_work":pr_list_work,
        "url_delete_wk":"http://"+new_domain+"/ngw/project/task/delete/",
        "pr_delete_wk":{"pseq": "","taseq": ""},
        "url_delete_pro":"http://"+new_domain+"/ngw/project/project/delete",
        "pr_delete_pro":{"pseq":"","password":"matkhau1!"},
        "url_detail_pro":"http://"+new_domain+"/ngw/project/project/view/pseq/",
        "url_modify_pro":"http://"+new_domain+"/ngw/project/project/write/mode/edit/pseq/",
        "url_detail_wk":"http://"+new_domain+"/ngw/project/task/view/",
        "pr_detail_wk":{"pseq": "","taseq": ""},
        
        
    }
    return json.dumps(par)

def project_msg():
    par={
      
       "pass_create_pro":"-Create Project <Pass>",
       "fail_create_pro":"-Create Project <Fail>",
       "pass_list_mypro":"-Get List My Project <Pass>",
       "fail_list_mypro":"-Get List My Project <Fail>",
       "pass_pro_in_list":"-The Created Project Is In The List <Pass>",
       "fail_pro_in_list":"-The Created Project Is in The List <Fail>",
       "pass_create_wk":"-Create Work <Pass>",
        "fail_create_wk":"-Create Work <Fail>",
        "pass_wk_in_list":"-The Created Work Is In The List <Pass>",
        "fail_wk_in_list":"-The Created Work Is In The List <Fail>",
        "pass_delete_work":"-Delete Work <Pass>",
        "fail_delete_work":"-Delete Work <Fail>",
        "pass_no_project":"-No Project To Add Work <Pass>",
        "pass_removed_wk":"-Work Has Removed From The List <Pass>",
        "faid_removed_wk":"-Work Has Removed From The List <Fail>",
        "pass_delete_pro":"-Delete Project <Pass>",
        "fail_delete_pro":"-Delete Project <Fail>",
        "pass_no_project_dele":"-No Project To Add Work <Pass>",
        "pass_removed_pro":"-Project Has Removed From The List <Pass>",
        "faid_removed_pro":"-Project Has Removed From The List <Fail>",
        "pass_leader_pro":"-Leader Updated Correctly <Pass>",
        "fail_leader_pro":"-Leader Updated Correctly <Fail>",
        "pass_par_pro":"-Participant Updated Correctly <Pass>",
        "fail_par_pro":"-Participant Updated Correctly <Fail>",
        "pass_detail_pro":"-View Detail Project <Pass>",
        "fail_detail_pro":"-View Detail Project <Fail>",
        "fail_detail_wk":"-View Detail Work <Fail>",
        "pass_detail_wk":"-View Detail Work <Pass>",
        "pass_content_wk":"-Content Updated Correctly <Pass>",
        "fail_content_wk":"-Content Updated Correctly <Fail>",
        "pass_subject_wk":"-Subject Updated Correctly <Pass>",
        "fail_subject_wk":"-Subject Updated Correctly <Fail>",
        "pass_assignee_wk":"-Assignee Updated Correctly <Pass>",
        "fail_assignee_wk":"-Assignee Updated Correctly <Fail>",
        "pass_date_wk":"-Date Updated Correctly <Pass>",
        "fail_date_wk":"-Date Updated Correctly <Fail>",




    }
    return json.dumps(par)

def resource_menu(new_domain):
    # Create work #
    pr_add_room={"mode": "add","fid":"-1","name": "Conference Room "+date_time ,"ec_is_system":"C","view_type": "0","frm_memo":"" ,"chk_frm_regis":"" }
    pr_add_vehicle={"mode": "add","fid":"-1","name": "Vehicle "+date_time ,"ec_is_system":"V","view_type": "0","frm_memo":"" ,"chk_frm_regis":"" }
    pr_add_normal={"mode": "add","fid":"-1","name": "Normal "+date_time ,"ec_is_system":"N","view_type": "0","frm_memo":"" ,"chk_frm_regis":"" }
    pr_add_resource=data["resource"]["create_res"]["param"]
    par={
        "url_left_list":"https://"+new_domain+"/ngw/resource/main/category/type/all/fid/RS_0/reverse/1",
        "pr_add_vehicle":pr_add_vehicle,
        "pr_add_room":pr_add_room,
        "pr_add_normal":pr_add_normal,
        "url_add_resource":"https://"+new_domain+"/ngw/resource/manage/add_equip/",
        "url_add_type":"https://"+new_domain+"/ngw/resource/manage/category_add/",
        "url_type_list":"https://"+new_domain+"/ngw/resource/main/optimize_resource/all/1/iscate/0/",
        "list_msg_type":{"msg_pass":data["resource_msg"]["pass_add_type"],"msg_fail":data["resource_msg"]["fail_add_type"]},
        "list_msg_displayed_room":{"pass_displayed":data["resource_msg"]["pass_room_displayed"],"fail_displayed":data["resource_msg"]["fail_room_displayed"],"fail_type":data["resource_msg"]["fail_room_type"]},
        "list_msg_vehicle":{"msg_pass":data["resource_msg"]["pass_add_vehicle"],"msg_fail":data["resource_msg"]["fail_add_vehicle"]},
        "list_msg_displayed_vehicle" :{"pass_displayed":data["resource_msg"]["pass_vehicle_displayed"],"fail_displayed":data["resource_msg"]["fail_vehicle_displayed"],"fail_type":data["resource_msg"]["fail_vehicle_type"]},
        "list_msg_normal":{"msg_pass":data["resource_msg"]["pass_add_normal"],"msg_fail":data["resource_msg"]["fail_add_normal"]},
        "list_msg_displayed_normal" :{"pass_displayed":data["resource_msg"]["pass_normal_displayed"],"fail_displayed":data["resource_msg"]["fail_normal_displayed"],"fail_type":data["resource_msg"]["fail_normal_type"]},
        "pr_add_resource":pr_add_resource,
        "list_msg_resource_n":{"pass_add_resource":data["resource_msg"]["pass_add_resource"],"fail_add_resource":data["resource_msg"]["fail_add_resource"]},
        "list_msg_resource_v":{"pass_add_resource":data["resource_msg"]["pass_add_resource_v"],"fail_add_resource":data["resource_msg"]["fail_add_resource_v"]},
        "list_msg_room":{"pass_displayed":data["resource_msg"]["pass_resource_displayed_r"],"fail_displayed":data["resource_msg"]["fail_resource_displayed_r"]},
        "list_msg_vehicle":{"pass_displayed":data["resource_msg"]["pass_resource_displayed_v"],"fail_displayed":data["resource_msg"]["fail_resource_displayed_v"]},
   
   }
    return json.dumps(par)

def expense_menu(new_domain):
    # Add Folder #
    title_folder = "Folder " + date_time
    pr_add_folder = data["expense"]["add_folder"]
    pr_add_folder["title"] = title_folder
    # Add Expense #
    title_expense = "Expense " + date_time
    id_depart = depart(new_domain)
    pr_add_expense = data["expense"]["add_expense"]
    pr_add_expense["dept"] = id_depart["depart1"]
    pr_add_expense["title"] = title_expense
    pr_add_expense["category_id"] = "",
    pr_add_expense["carbons_copy"] ="",
    pr_add_expense["start_date"] = today.replace("-","/"),
    pr_add_expense["end_date"] = today.replace("-","/")

    # Expense List #
    pr_expense_list = data["expense"]["expsense_list"]

    par={
        "ur_add_folder":"http://"+new_domain+"/ngw/expense/expense/save_folder",
        "pr_add_folder":pr_add_folder,
        "add_msg" :{"pass":data["expense_msg"]["pass_add_folder"],"fail":data["expense_msg"]["fail_add_folder"]},
        "ur_list_folder":"http://"+new_domain+"/ngw/expense/expense/tree/id/all/reverse/1",
        "title_folder":title_folder,
        "ur_add_expense" :"http://"+new_domain+"/ngw/expense/expense/write",
        "pr_add_expense" :pr_add_expense,
        "expense_msg" :{"pass":data["expense_msg"]["pass_add_expense"],"fail" :data["expense_msg"]["fail_add_expense"]},
        "ur_expense_list":"http://"+new_domain+"/ngw/expense/expense",
        "pr_expense_list" :pr_expense_list,
        "title_expense" :title_expense,
        "ur_delete_expense":"http://"+new_domain+"/ngw/expense/expense/expenses_delete",
        "pr_delete_expense":data["expense"]["delete_expsense"]
   }
    return json.dumps(par)

def asset_menu(new_domain):
    # Add categories #
    category_name = "Category " + str(random.randint(0,10000))
    pr_add_category = data["asset"]["add_category"]
    pr_add_category["category_name"] = category_name

    par={
        "pr_add_category" : pr_add_category ,
        "ur_add_category":"https://"+new_domain+"/ngw/asset/category/save"
   }
    return json.dumps(par)


    