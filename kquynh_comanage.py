import json,random
from random import choice,randint
from kquynh_function_gw import data,result,execution_test_link,check_the_saved_data,notification,send_mail,post,post_header,get,account_two,account_one,msg,next_page,id_user,head_menu,account_thr,cookie_user,old_domain,msg_execution_test_link
from kquynh_param_gw import comanage_menu,username
msg_coma = data['comanage_msg']

def id_project(sucess,title_comanage):
    for x in sucess["rows"]:
        if title_comanage == x["subject"] :
            return x["pseqno"]

def check_work_type(sucess,subject,work_name,color_name,icon_name):
    #1 :color,2:icon,0:check display 
    a=[] 
    i=0
    for x in sucess["rows"] :
        if x[subject]==work_name :
            a.append(True) 
            if x["color"]==color_name :
                a.append("yes_color")
            else :
                a.append("no_color")
            if x["icon"]== icon_name :
                a.append("yes_icon")
            else :
                a.append("no_icon") 
            break
        else: 
            a.append(False) 
    return a

def check_list_member(success,member_type,list_member):
    a=[]
    b=[]
    if len(success["rows"][member_type])==0 :
        return False 
    else:
        i=0
        for x in success["rows"][member_type] :
            a.append(x["id"])

        if len(a) != len(list_member) :
            return False
        else :
            for x in a:
                for y in list_member :
                    if x == y :
                        i=i+1
                if i== 0 :
                    b.append(False)
                    i=0
                else:
                    b.append(True)
                    i=0
            j=0
            length=len(b)
            for x in b :
                if x == False:
                    break
                else :
                    j=j+1 
            if j< length:
                return False
            else:
                return True

def check_list_data(a,b):
    c=[]
    if len(a) != len(b) :
        return False
    else :
        i=0
        for x in a:
            for y in b :
                if x == y :
                    i=i+1
            if i== 0 :
                c.append(False)
                i=0
            else:
                c.append(True)
                i=0
        j=0
        length=len(c)
        for x in c :
            if x == False:
                break
            else :
                j=j+1 
        if j< length:
            return False
        else:
            return True

def work_type_list(success,a_type):
    a=[]
    b=["Epic","Story","Sub Task"]
    if a_type=="rows" :
        for x in success["rows"]:
            if x["subject"] not in b:
                a.append(x["subject"])
    else :
        for x in success["rows"][a_type]:
            if x["subject"] not in b:
                a.append(x["subject"])
    return a

def work_type_no_defa(success):
    a=[]
    for x in success["rows"]["types"]:
        if x["is_default"] == "0":
            a.append(x["subject"])
    return a

def status_no_base(success):
    a=[]
    for x in success["rows"]["status"]:
        if x["is_base"] == "0":
            a.append(x["name"])
    return a

def status_list(success,a_type):
    a=[]
    if a_type=="rows" :
        for x in success["rows"]:
            a.append(x["name"])
    else :
        for x in success["rows"][a_type]:
            a.append(x["name"])
    return a

def type_at_work(success,type_pro):
    a=[]
    if type_pro == "kanban":
        for x in success["rows"]["types"]:
            if x["type"]== "0" :
                a.append(x["ttseq"])
    if type_pro == "sub_task":
        for x in success["rows"]["types"]:
            if x["type"]== "3" :
                a.append(x["ttseq"])
    if type_pro =="scrum":
        for x in success["rows"]["types"]:
            if x["type"]== "1" or x["type"]== "2" :
                a.append(x["ttseq"])
    return a

def no_status_at_column(success):
    a=[]
    for x in success["rows"]["columns"]:
        a.append(x["defined_status"])
    return a

def text(user_name,pass_access_pj):
    text = str("-") + str(user_name) + " : " + str(pass_access_pj)
    return text

def result_add(response,msg_list):
    result = False
    if notification(response) == True :
        result = True
        msg("p",msg_list["pass"])
    else :
        msg("f",msg_list["fail"])
    return result



def result_wt_displayed(type,response,msg_list,subject,param):
    if type == "save":
        check = False
        if len(response["rows"]) == 0 :
            msg("f",msg_list["fail"])
        else :
            for work in response["rows"]:
                if work["subject"] == subject :
                    check = True
                    msg("p",msg_list["pass"])
                    # Check detail #
                    if work["color"] == param["color"] :
                        msg("p",msg_list["pass_color"])
                    else :
                        msg("p",msg_list["fail_color"])

                    if work["icon"]== param["icon"] :
                        msg("p",msg_list["pass_icon"]) 
                    else:
                        msg("f",msg_list["fail_icon"]) 

                    break
            if  check == False :
                msg("f",msg_list["fail"])
def result_st_displayed(type,response,msg_list,subject,param):
    if type == "save":
        check = False
        if len(response["rows"]) == 0 :
            msg("f",msg_list["fail"])
        else :
            for status in response["rows"]:
                if status["name"] == subject :
                    check = True
                    msg("p",msg_list["pass"])

                    # Check detail #
                    if status["description"]== param["description"] :
                        msg("p",msg_list["pass_description"])
                    else:
                        msg("f",msg_list["fail_description"])
                        
                    if status["category"]== param["category"] :
                        msg("p",msg_list["pass_category"])
                    else:
                        msg("f",msg_list["fail_category"])
                        
                    if status["is_base"]== param["is_base"] :
                        msg("p",msg_list["pass_base"])

                    else:
                        msg("f",msg_list["fail_base"])
                    break
            if  check == False :
                msg("f",msg_list["fail"])

def result_pj_displayed(type,response,msg_list,subject):
    if type == "save":
        check = False
        id_pro = ""
        if len(response["rows"]) == 0 :
            msg("f",msg_list["fail"])
        else :
            for project in response["rows"] :
                if project["subject"] == subject :
                    check = True
                    id_pro = project["pseqno"]
                    break
            if  check == True :
                msg("p",msg_list["pass"])
            else :
                msg("f",msg_list["fail"])
        return id_pro

def co_manage(new_domain):
    param=json.loads(comanage_menu(new_domain))
    user_name=username(new_domain)
    '''
    # ADMIN > MANAGER WORK TYPE #
    param=json.loads(comanage_menu(new_domain))
    head_menu("CO MANAGE") 
    msg("n","I.ADMIN")
    msg("n","Manage Work Type")
    

    # Add Work Type #
    result_add_wt = False 
    ur_work_type = param["ur_work_type"]
    pr_work_type = param["pr_work_type"]
    title_wt =  pr_work_type["subject"]
    response_add_work_type = post(ur_work_type,pr_work_type,account_one(new_domain))
    wt_list = param["wt_list"]
    result_add_wt = result_add(response_add_work_type,wt_list)
      
    
    # Work Type is displayed #
    if result_add_wt == True :
        response_wt_list = get(param["ur_ad_wt_list"],"",account_one(new_domain))
        wt_displayed = param["wt_displayed"]
        if notification(response_wt_list) == True :
            result_wt_displayed("save",response_wt_list,wt_displayed,title_wt,pr_work_type)
        else :
            msg("f",msg_coma["fail_wt_list"])
   

    # ADMIN > MANAGE STATUS #
    msg("n","Manager Status")
    result_add_st = False
    ur_add_status = param["ur_add_status"]
    pr_add_status = param["pr_add_status"]
    title_st =  pr_add_status["name"]
    response_add_status = post(ur_add_status,pr_add_status,account_one(new_domain))
    st_list = param["st_list"]
    result_add_st = result_add(response_add_status,st_list) 

    # Status is displayed #
    if result_add_st == True :
        response_st_list = get(param["ur_ad_st_list"],"",account_one(new_domain))
        st_displayed = param["st_displayed"]
        if notification(response_st_list) == True :
            result_st_displayed("save",response_st_list,st_displayed,title_st,pr_add_status)
        else :
            msg("f",msg_coma["fail_st_list"])
    '''
    # PROJECT #
    msg("n","II.PROJECT LIST")
    msg("n","Creator : TS1 , Leader : TS3 , (TS7,TS8) , CC : TS5  , (TS7,TS8) , Participant :TS2 , (TS7,TS8) , Not right :TS6 ")

    # Add Project #
    result_project = False 
    title_pj = param["project_name"]
    ur_project = param["ur_project"]
    pr_project = param['pr_project']
    response_project = post(ur_project,pr_project,account_one(new_domain))
    add_project = param["add_project"]
    result_project = result_add(response_project,add_project)

    # Project is displayed #
    id_pj = ""
    if result_project == True :
        response_project_list = get(param["ur_pro_list"],"",account_one(new_domain))
        add_pj = param["add_pj"]
        if notification(response_project_list) == True :
            id_pj = result_pj_displayed("save",response_project_list,add_pj,title_pj)

            # Access Project #
            ur_access_pro = param["ur_access_pro"] + id_pj
            response_access = get(ur_access_pro,"",account_one(new_domain))
            if notification(response_access) == True :
                msg("p",text(user_name["name1"],msg_coma["pass_access_pj"]))
            else :
                msg("f",text(user_name["name1"],msg_coma["fail_access_pj"]))


        else :
            msg("f",msg_coma["fail_pj_list"])

    # PROJECT > SETTINGS PROJECT   #
   
    
    ur_add_member = param["ur_add_member"]
    pr_add_member = param["pr_add_member"]
    pr_add_leader = param["pr_add_leader"]
    
    if id_pj != "" :
        # add member #
        pr_add_member["pseqno"] = id_pj
        pr_add_member["user_list"] = json.dumps(pr_add_member["user_list"])
        response_add_member = post(ur_add_member,pr_add_member,account_one(new_domain))
        member_list = param["member_list"]
        result(response_add_member,member_list)

        
        # add leader #
        pr_add_leader["pseqno"] = id_pj
        pr_add_leader["user_list"] = json.dumps(pr_add_leader["user_list"])
        response_add_leader = post(ur_add_member,pr_add_leader,account_one(new_domain))
        leader_list = param["leader_list"]
        result(response_add_leader,leader_list)

        
        # add  #


        
        '''         
        # PROJECT > SETTINGS PROJECT   #
        id_pro = ""
        list_member=[]
        msg("n","  <Project Settings>")
        param["param_add_member"]["pseqno"]=id_pro
        ts7=id_user(new_domain,"ts7")
        ts8=id_user(new_domain,"ts8")
        list_member.append("ts7")
        list_member.append("ts8")
        param["param_get_list_member"]["pseqno"]=param["param_get_list_member"]["pseqno"]=id_pro
        param["param_add_wt_to_work"]["pseqno"]=param["param_add_st_to_work"]["pseqno"]=id_pro
        url_get_list_member=api(param["url_head_get_list_member"],param["param_get_list_member"])
        
        

        # add multiple leader #
        param["param_add_member"]["user_list"]=json.dumps([{"ucn":ts7[0],"no":ts7[1],"type":1},{"ucn":ts8[0],"no":ts8[1],"type":1}])
        success_add_leader=post(param["url_add_member"],param["param_add_member"],account_one(new_domain))
        if notification(success_add_leader)== True :
            msg_execution_test_link("p","WAPI-102","  +TS1:Add multiple leader")
            
            success_get_list_member=get(url_get_list_member,param["param_get_list_member"],account_one(new_domain))
            if notification(success_get_list_member)== True :
                check_member=check_list_member(success_get_list_member,"leaders",list_member)
                if check_member== True :
                    msg_execution_test_link("p","WAPI-102","    +TS1:Leader list updated is Correct")
                    
                else :
                    msg_execution_test_link("f","WAPI-102","    +TS1:Leader list updated is Correct")
                   
                    
            else :
                msg("f","  +TS1 :Get list member => Fail")
               
        else:
            msg_execution_test_link("f","WAPI-102","  +TS1:Add multiple leader")
           

        # add leader #
        leader=[]
        leader.append("ts3")
        ts3=id_user(new_domain,"ts3")
        param["param_add_member"]["user_list"]=json.dumps([{"ucn":ts3[0],"no":ts3[1],"type":1}])
        success_add_leader=post(param["url_add_member"],param["param_add_member"],account_one(new_domain))
        if notification(success_add_leader)== True :
            msg_execution_test_link("p","WAPI-102","  +TS1:Add leader")
            
            success_get_list_member_1=get(url_get_list_member,param["param_get_list_member"],account_one(new_domain))
            if notification(success_get_list_member_1)== True :
                check_member=check_list_member(success_get_list_member_1,"leaders",leader)
                if check_member== True :
                    msg_execution_test_link("p","WAPI-102","    +TS1:Leader list updated is Correct")
                    
                else :
                    msg_execution_test_link("f","WAPI-102","    +TS1:Leader list updated is Correct")
                  
                    
            else :
                msg("f","  +TS1 :Get list member => Fail")
                

        else:
            msg_execution_test_link("f","WAPI-102","  +TS1:Add leader")
            
            

        # add multiple particpant #
        param["param_add_member"]["user_list"]=json.dumps([{"ucn":ts7[0],"no":ts7[1],"type":2},{"ucn":ts8[0],"no":ts8[1],"type":2}])
        success_add_leader=post(param["url_add_member"],param["param_add_member"],account_one(new_domain))
        if notification(success_add_leader)== True :
            msg_execution_test_link("p","WAPI-104","  +TS1:Add multiple participant")
            
            success_get_list_member_3=get(url_get_list_member,param["param_get_list_member"],account_one(new_domain))
            if notification(success_get_list_member_3)== True :
                check_member=check_list_member(success_get_list_member_3,"participants",list_member)
                if check_member== True :
                    msg_execution_test_link("p","WAPI-104","    +TS1:Participants list updated is Correct")
                    
                else :
                    msg_execution_test_link("f","WAPI-104","    +TS1:Participants list updated is Correct")
                     
            else :
                msg("f","  +TS1 :Get list member => Fail")
               
        else:
            msg_execution_test_link("f","WAPI-104","  +TS1:Add multiple participant")
           
            

        # add particpant #
        participants=[]
        participants.append("ts2")
        ts2=id_user(new_domain,"ts2")
        param["param_add_member"]["user_list"]=json.dumps([{"ucn":ts2[0],"no":ts2[1],"type":2}])
        success_add_leader=post(param["url_add_member"],param["param_add_member"],account_one(new_domain))
        if notification(success_add_leader)== True :
            msg_execution_test_link("p","WAPI-104","  +TS1:Add participant")
            
            success_get_list_member_4=get(url_get_list_member,param["param_get_list_member"],account_one(new_domain))
            if notification(success_get_list_member_4)== True :
                check_member=check_list_member(success_get_list_member_4,"participants",participants)
                if check_member== True :
                    msg_execution_test_link("p","WAPI-104","    +TS1:Participants list updated is Correct")
                    
                else :
                    msg_execution_test_link("f","WAPI-104","    +TS1:Participants list updated is Correct")
                   
                    
            else :
                msg("f","  +TS1 :Get list member => Fail")
                

        else:
            msg_execution_test_link("f","WAPI-104","  +TS1:Add participant")
            
            

        # add multiple cc #
        param["param_add_member"]["user_list"]=json.dumps([{"ucn":ts7[0],"no":ts7[1],"type":3},{"ucn":ts8[0],"no":ts8[1],"type":3}])
        success_add_leader=post(param["url_add_member"],param["param_add_member"],account_one(new_domain))
        if notification(success_add_leader)== True :
            msg_execution_test_link("p","WAPI-103","  +TS1:Add multiple cc")
            
            success_get_list_member_5=get(url_get_list_member,param["param_get_list_member"],account_one(new_domain))
            if notification(success_get_list_member_5)== True :
                check_member=check_list_member(success_get_list_member_5,"cc",list_member)
                if check_member== True :
                    msg_execution_test_link("p","WAPI-103","    +TS1:CC list updated is Correct")
                    
                else :
                    msg_execution_test_link("f","WAPI-103","    +TS1:CC list updated is Correct")
                    
                    
            else :
                msg("f","  +TS1 :Get list member => Fail")
               
        else:
            msg_execution_test_link("f","WAPI-103","  +TS1:Add multiple cc")
            
            

        # add cc #
        cc=[]
        cc.append("ts5")
        ts5=id_user(new_domain,"ts5")
        param["param_add_member"]["user_list"]=json.dumps([{"ucn":ts5[0],"no":ts5[1],"type":3}])
        success_add_leader=post(param["url_add_member"],param["param_add_member"],account_one(new_domain))
        if notification(success_add_leader)== True :
            msg_execution_test_link("p","WAPI-103","  +TS1:Add cc")
        
            success_get_list_member_6=get(url_get_list_member,param["param_get_list_member"],account_one(new_domain))
            if notification(success_get_list_member_6)== True :
                check_member=check_list_member(success_get_list_member_6,"cc",cc)
                if check_member== True :
                    msg_execution_test_link("p","WAPI-103","    +TS1:CC list updated is Correct")
                    
                else :
                    msg_execution_test_link("f","WAPI-103","    +TS1:CC list updated is Correct")
                   
                    
            else :
                msg("f","  +TS1 :Get list member => Fail")
               
        else:
            msg_execution_test_link("f","WAPI-103","  +TS1:Add cc")
           
            
        
        #Check work type list from manage work type of admin  to manage work type of project #
        ad_list_work=[]
        pro_list_work=[]
        ad_success_get_list_work_type_1=get(param["admin_url_get_list_work_type"],"",account_one(new_domain))
        if notification(ad_success_get_list_work_type_1)== True :
            ad_list_work=work_type_list(ad_success_get_list_work_type_1,"rows")
            success_init_work_type=get(param["url_init_work_type"],"",account_one(new_domain))
            if notification(success_init_work_type)== True :
                pro_list_work=work_type_list(success_init_work_type,"types")
            
                if check_list_data(ad_list_work,pro_list_work)== True :
                    msg_execution_test_link("p","WAPI-112","  +Updated Work type list from admin to project settings")
                    
                else :
                    msg_execution_test_link("f","WAPI-112","  +Updated Work type list from admin to project settings")
                   
                    

                # Add work type to use for created work #
                ttseq_work_type= "{"
                for x in success_init_work_type["rows"]["types"]:
                    ttseq_work_type +='"' + x["subject"]+ '"' + ":"+ '"' + x["ttseq"]+ '"' + ","
                data["comanage"]["basic_information"]["list_id_init_work_type"]= json.loads(ttseq_work_type[None:len(ttseq_work_type)-1] +"}")
                id_list_init_work_type=data["comanage"]["basic_information"]["list_id_init_work_type"]

                if len(work_type_no_defa(success_init_work_type)) !=0 :
                    add_wt_name= random.choice(work_type_no_defa(success_init_work_type))
                    param["param_add_wt_to_work"]["ttseq"]=id_list_init_work_type[add_wt_name]
                    success_add_wt_to_work=post(param["url_add_wt_to_work"],param["param_add_wt_to_work"],account_one(new_domain))
                    if notification(success_add_wt_to_work)== True:
                        msg_execution_test_link("p","WAPI-111","  +Add work type to work")
                        
                        # Check added work type at create work #
                        old_load_pro=data["comanage"]["load_project"]+id_pro
                        load_pro=change(new_domain,old_load_pro,old_domain)
                        success_load_pro=get(load_pro,"", account_one(new_domain))
    
                        if notification(success_load_pro)== True :
                            list_wt_at_work=work_type_list(success_load_pro,"types")
                            if add_wt_name in list_wt_at_work :
                                msg_execution_test_link("p","WAPI-111","    +Work type has been added to the work")
                                
                            else :
                                msg_execution_test_link("f","WAPI-111","    +Work type has been added to the work")
                               
                                
                    else :
                        msg_execution_test_link("f","WAPI-111","  +Add work type to work")
                       
                        
                

                

        #Check status list from manage status of admin to manage status of project #  
        ad_list_status=[]
        pro_list_status=[]
        ad_success_get_list_status_1=get(param["ad_url_get_list_status"],"",account_one(new_domain))
        if notification(ad_success_get_list_status_1)== True :
            ad_list_status=status_list(ad_success_get_list_status_1,"rows")
            success_init_status=get(param["url_init_work_type"],"",account_one(new_domain))
            if notification(success_init_status)== True :
                pro_list_status_1=status_list(success_init_status,"status")
                if check_list_data(ad_list_status,pro_list_status_1)== True :
                    msg_execution_test_link("p","WAPI-113","  +Updated status list from admin to project settings")
                    
                else :
                    msg_execution_test_link("f","WAPI-113","  +Updated status list from admin to project settings")
                    
                    
                # Add sattus to use for cteare work #
                sseq_work_type= "{"
                for x in success_init_status["rows"]["status"]:
                    sseq_work_type +='"' + x["name"]+ '"' + ":"+ '"' + x["sseq"]+ '"' + ","
                data["comanage"]["basic_information"]["list_id_init_status"]= json.loads(sseq_work_type[None:len(sseq_work_type)-1] +"}")
                id_list_init_status=data["comanage"]["basic_information"]["list_id_init_status"]
                if len(work_type_no_defa(success_init_status)) !=0 :
                    add_st_name= random.choice(status_no_base(success_init_status))
                    param["param_add_st_to_work"]["sseq"]=id_list_init_status[add_st_name]
                    success_add_st_to_work=post(param["url_add_st_to_work"],param["param_add_st_to_work"],account_one(new_domain))
                    if notification(success_add_st_to_work)== True :
                        msg_execution_test_link("p","WAPI-114","  +Add status to work")
                        
                        # Check status is added at create work #
                        old_load_pro_1=data["comanage"]["load_project"]+id_pro
                        load_pro_1=change(new_domain,old_load_pro_1,old_domain)
                        success_load_pro1=get(load_pro_1,"", account_one(new_domain))
    
                        if notification(success_load_pro1)== True :
                            list_st_at_work=status_list(success_load_pro1,"status")
                            if add_st_name in list_st_at_work :
                                msg_execution_test_link("p","WAPI-114","    +Status has been added to the work")
                                
                            else :
                                msg_execution_test_link("f","WAPI-114","    +Status type has been added to the work")
                                
                                
                    else :
                        msg_execution_test_link("f","WAPI-114","  +Add status to work")
                        
                                              
        else :
            msg("f","-Get list project => Fail")
            
        # PERMISSION OF MEMBER #
        maxpage= ""
        param["param_b_url_cretae_work"]["pseqno"]=id_pro
        old_detail_pro=data["comanage"]["detail_project"]+id_pro
        detail_pro=change(new_domain,old_detail_pro,old_domain)
        success_detail_pro=get(detail_pro,"",account_one(new_domain))
        
        old_load_pro_2=data["comanage"]["load_project"]+id_pro
        load_pro_2=change(new_domain,old_load_pro_2,old_domain)
        success_load_pro2=get(load_pro_2,"", account_one(new_domain))
        
        if notification(success_load_pro2)== True :
            #Leader#
            list_leader=[]
            for x in success_load_pro2["rows"]["members"]["leaders"]:
                list_leader.append(x["id"])
            if len(list_leader) == 0:
                msg("p","-There is no leader")
            else :
                i=0
                id_leader= random.choice(list_leader)
                url_id_leader=" "
                for x in data["login"]:
                    if x == id_leader :
                        url_id_leader= data["login"][x]
                        break
                if len(url_id_leader) != 0 :
                    
                    msg("n","[Leader name : " + id_leader.upper() +"]")
                    cookie_ld=cookie_user(new_domain,id_leader)
                    leader_list_project=next_page(maxpage,param["url_head_get_project"],param["param_add_member"],cookie_ld,"subject")
                    
                    for x in leader_list_project :
                        if x== param["project_name"] :
                            i=i+1
                    if i==0 :
                        msg_execution_test_link("f","WAPI-115","-"+id_leader.upper()+":"+":Project is not seen")
                       
                        
                    else :
                        # access project #
                        ld_old_url_access_pro=data["comanage"]["load_project"] + id_pro
                        ld_url_access_pro=change(new_domain,ld_old_url_access_pro,old_domain)
                        success_access_pro=get(ld_url_access_pro,"",cookie_ld)
                        if notification(success_access_pro)== True :
                            msg_execution_test_link("p","WAPI-115","  +" + id_leader.upper()+":"+"Acesss project")
                            
                        else :
                            msg_execution_test_link("f","WAPI-115","  +" + id_leader.upper()+":"+"Acesss project")
                            
                else :
                    msg("p","-There is no user id of leader")


            #Participant#  
            list_participants=[]
            for x in success_load_pro2["rows"]["members"]["participants"]:
                list_participants.append(x["id"])
            if len(list_participants) == 0:
                msg("p","-There is no Participant")
            else :
                i=0
                id_participant= random.choice(list_participants)
                url_id_participant=" "
                for x in data["login"]:
                    if x == id_participant :
                        url_id_participant= data["login"][x]
                        break
                if len(url_id_participant) != 0 :
                    msg("n","[Participant name : " + id_participant.upper() +"]")
                    cookie_ld_p=cookie_user(new_domain,id_participant)
                    participant_list_project=next_page(maxpage,param["url_head_get_project"],param["param_get_project"],cookie_ld_p,"subject")
                    for x in participant_list_project :
                        if x== param["project_name"] :
                            i=i+1
                    if i==0 :
                        msg_execution_test_link("f","WAPI-115","-"+id_participant.upper()+":"+"Project is not seen")
                        result.write("<div>"+"[Co-manage]"+id_participant.upper()+":"+"Project is not seen => Fail "+"</div>")
                       
                    else :
                        # permission access project #
                        ld_old_url_access_pro=data["comanage"]["load_project"] + id_pro
                        ld_url_access_pro=change(new_domain,ld_old_url_access_pro,old_domain)
                        success_access_pro=get(ld_url_access_pro,"",cookie_ld_p)
                        if notification(success_access_pro)== True :
                            msg_execution_test_link("p","WAPI-115","  +"+ id_participant.upper()+ ":-Acesss project")
                            
                            # create work #
                            success_p_detail_pro=get(detail_pro,"",cookie_ld_p)
                            if notification(success_p_detail_pro)== True :
                                if success_p_detail_pro["attrs"]["access"]["is_create"]== True :
                                    p_load_pro=get(load_pro_2,"",cookie_ld_p)
                                    if notification(p_load_pro)== True:
                                        #p_list_wt_at_work=type_at_work(p_load_pro,"kanban")
                                        param["param_b_url_cretae_work"]["params[type]"]=random.choice(type_at_work(p_load_pro,"kanban"))
                                        sseq_status= "{"
                                        for x in p_load_pro["rows"]["status"]:
                                            sseq_status +='"' + x["name"]+ '"' + ":"+ '"' + x["sseq"]+ '"' + ","
                                        data["comanage"]["basic_information"]["list_id_pro_status"]= json.loads(sseq_status[None:len(sseq_status)-1] +"}")
                                        param["param_b_url_cretae_work"]["params[status]"]=id_status=random.choice(no_status_at_column(p_load_pro))
                                        param["param_b_url_cretae_work"]["params[assignee]"]=id_user(new_domain,id_participant)[2]
                                        param["param_b_url_cretae_work"]["params[priority]"]= randint(0,4)
                                        success_p_create_work=post(param["b_url_cretae_work"],param["param_b_url_cretae_work"],cookie_ld_p)
                                        if notification(success_p_create_work)== True:
                                            msg_execution_test_link("p","WAPI-116","-"+id_participant.upper() +":" +"-Create work")
                                            
                                        else:
                                            msg_execution_test_link("f","WAPI-116","-"+id_participant.upper() +":" +"-Create work")
                                            
                                            
                                else :
                                    msg("f","  +Permission to create work => fail")
                                   
                                

                        else :
                            msg_execution_test_link("f","WAPI-115","  +"+ id_participant.upper()+ ":Acesss project")
                           
                else :
                    msg("p","-There is no user id of participant")


            #CC#  
            list_cc=[]
            for x in success_load_pro2["rows"]["members"]["cc"]:
                list_cc.append(x["id"])
            if len(list_cc) == 0:
                msg("p","-There is no CC")
            else :
                i=0
                id_cc= random.choice(list_cc)
                url_id_cc=" "
                for x in data["login"]:
                    if x == id_cc :
                        url_id_cc= data["login"][x]
                        break
                if len(url_id_cc) != 0 :
                    msg("n","[CC name : " + id_cc.upper() +"]")
                    cookie_ld_c=cookie_user(new_domain,id_cc)
                    cc_list_project=next_page(maxpage,param["url_head_get_project"],param["param_get_project"],cookie_ld_c,"subject")
                    
                    for x in cc_list_project :
                        if x== param["project_name"] :
                            i=i+1
                    if i==0 :
                        msg_execution_test_link("f","WAPI-115","-"+id_cc.upper()+":"+"Project is not seen")
                      
                        
                    else :
                        # access project #
                        ld_old_url_access_pro=data["comanage"]["load_project"] + id_pro
                        ld_url_access_pro=change(new_domain,ld_old_url_access_pro,old_domain)
                        success_access_pro=get(ld_url_access_pro,"",cookie_ld_c)
                        if notification(success_access_pro)== True :
                            msg_execution_test_link("p","WAPI-115","  +"+ id_cc.upper()+ ":Acesss project")
                            
                        else :
                            msg_execution_test_link("f","WAPI-115","  +"+ id_cc.upper()+ ":Acesss project")
                            
                else :
                    msg("p","-There is no user id of cc")
    '''


    else :
        msg_execution_test_link("f","WAPI-38","-Create project")
       
        

   



    



    
