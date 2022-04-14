import requests,json,random,re,string,time,datetime,testlink,sys,pathlib,os
from datetime import date
from colorama import Fore, Back, Style
from colorama import init, AnsiToWin32
from pathlib import Path
from kquynh_function_gw import data,change,execution_test_link,check_the_saved_data,notification,send_mail,post,post_header,get,cookie_writer,cookie_recipient,msg,next_page,id_user,head_menu,another_user,cookie_user,old_domain


ran=random.randint(1,10000000)
m=0
def board_create_subfolder(name,ran,option_type,folder_no,new_domain):
    a=[]
    subfolder_name=str(name)+ ' ' + str(ran) 
    param_create_subfolder=data["board"]["admin"]["manage_company_folder"]["param_create_subfolder"]
    param_create_subfolder["folder_name"]=subfolder_name
    param_create_subfolder["folder_up"]=folder_no
    param_create_subfolder["bform"]=str(option_type)
    param_create_subfolder["noname"]="true"
    old_url_create_subfolder=data["board"]["admin"]["manage_company_folder"]["api_create_subfolder"]
    url_create_subfolder=change(new_domain,old_url_create_subfolder,old_domain)
    
    if option_type == 1:
        success_create_subfolder=post(url_create_subfolder,param_create_subfolder,cookie_writer(new_domain))
        a.append(notification(success_create_subfolder))
        if notification(success_create_subfolder)== True :
            a.append(success_create_subfolder["rows"]["id_folder_parse"])
    
    elif option_type == 2:
        param_create_subfolder["noname"]="True"
        success_create_subfolder=post(url_create_subfolder,param_create_subfolder,cookie_writer(new_domain))
        a.append(notification(success_create_subfolder))
        if notification(success_create_subfolder)== True :
            a.append(success_create_subfolder["rows"]["id_folder_parse"])
            
    elif option_type == 3 :
        ts1=id_user(new_domain,"ts1")
        ts2=id_user(new_domain,"ts2")
        id_ts1="2_"+ts1[3]+"_"+ts1[1] +":"+"5"
        id_ts2="2_"+ts2[3]+"_"+ts2[1] +":"+"5"
        param_create_subfolder["noname"]="True"
        param_create_subfolder["share_list"]=id_ts1 +"," + id_ts2
        param_create_subfolder["is_share"]="true"
        success_create_subfolder=post(url_create_subfolder,param_create_subfolder,cookie_writer(new_domain))
        a.append(notification(success_create_subfolder))
        if notification(success_create_subfolder)== True :
            a.append(success_create_subfolder["rows"]["id_folder_parse"])
    else :
        ts1=id_user(new_domain,"ts1")
        ts2=id_user(new_domain,"ts2")
        id_ts1="2_"+ts1[3]+"_"+ts1[1] +":"+"5"
        id_ts2="2_"+ts2[3]+"_"+ts2[1] +":"+"5"
        param_create_subfolder["noname"]="True"
        param_create_subfolder["share_list"]=id_ts1 +"," + id_ts2
        param_create_subfolder["is_share"]="false"
        success_create_subfolder=post(url_create_subfolder,param_create_subfolder,cookie_writer(new_domain))
        a.append(notification(success_create_subfolder))
        if notification(success_create_subfolder)== True :
            a.append(success_create_subfolder["rows"]["id_folder_parse"])
    return a

def board_success_folder(folder,id_test_link,folder_name,user,success,folder_no,result,new_domain):
    if folder[0]== True :
        msg("p","  +Create sub folder is " + folder_name  + " => Pass")
        execution_test_link(id_test_link,"p")
        if board_check_folder_created(success,folder_no,folder[1],new_domain)== True :
            folder.append(board_check_folder_created(success,folder_no,folder[1],new_domain)) # True false kết quả kiểm tra folder đã hiển thị
            msg("p","    +" + user +": Sub folder " + folder_name  + " displayed in left menu => Pass")
            execution_test_link(id_test_link,"p")
        else :
            folder.append(board_check_folder_created(success,folder_no,folder[1],new_domain))
            msg("f","    +" + user +": Sub folder " + folder_name  + " displayed in left menu => Fail")
            result.write("<div>"+"[Board]" + user +": Sub folder " + folder_name  + " displayed in left menu => Fail"+"</div>")
            execution_test_link(id_test_link,"f")
    else :
        msg("f","  [Board]Create sub folder is " + folder_name  + " => Fail")
        result.write("<div>"+"[Board]Create sub folder is " + folder_name  + " => Fail"+"</div>")
        execution_test_link(id_test_link,"f")

def board_check_folder_created(success,folder_no,id_subfolder,new_domain):
    i=0
    if new_domain=="global3.hanbiro.com":
        for x in success["rows"]:
            for y in x["children"]:
                if int(y['fldseq']) == int(folder_no):
                    if "children" in y :
                        for z in y['children']:
                            if z['id'] == id_subfolder :
                                i=i+1
                                return True 
                                                   
                    else : 
                        return False
                        
    else :
        for x in success["rows"] :
            if int(x['fldseq']) == int(folder_no):
                if "children" in x :
                    for y in x['children']:
                        if y['id'] == id_subfolder :
                            i=i+1
                            return True 
                                              
                else : 
                    return False
                    
    if i== 0 :
        return False
    
def id_board(success_list_board,board_name):
    id_board=""
    for x in success_list_board["rows"] :
        if x["subject"] == board_name:
            id_board=x["id"]
    return id_board

def view_board(id_folder,id_b,head_url_view_board,param_view_board,cookie):
    param_view_board["folder"]=id_folder
    param_view_board["id"]=id_b
    url_view_board=api(head_url_view_board,param_view_board)
    sucess_view_board=get(url_view_board,"",cookie)
    return sucess_view_board["success"]

def unread_counter(success,rows,viewed):
    if notification(success) == True :
        if success["rows"]["viewed"]== False :
            return False 
        else:
            return True 

def counter(success):
    data["board"]["counter"]["param"]=json.dumps((success["attr"]["count_unread"]))
    data["board"]["counter"]["param"]["conditions"]=json.loads(data["board"]["counter"]["param"]["conditions"])
    print(data["board"]["counter"]["param"])

def board_check_folder_by_name(success,folder_no,title_board,new_domain):

    i=0
    if new_domain=="global3.hanbiro.com":
        for x in success["rows"]:
            for y in x["children"]:
                if int(y['fldseq']) == int(folder_no):
                    if "children" in y :
                        for z in y['children']:
                            if z['text'] == title_board :
                                i=i+1
                                return True 
                                             
                    else : 
                        return False
                        
    else:
        for x in success["rows"] :
            if int(x['fldseq']) == int(folder_no):
                if "children" in x :
                    for y in x['children']:
                        if y['text'] == title_board :
                            i=i+1
                            return True 
                                              
                else : 
                    return False
                    
    if i== 0 :
        return False

def board_notice(result,notice,folder_no,new_domain):
    #0 :success create folder , 1:id_folder , 2:saved folder 
    #TS1#
    head_menu("A .Board Notice ")
    print("*TS1: Write, read , modify , delete all boards*,*TS2 :Read board*")
    board_notice_name ="Notice Board"
    old_url_get_list_folder_left=data["board"]["left_menu"]["api_left"]
    url_get_list_folder_left=change(new_domain,old_url_get_list_folder_left,old_domain)
    param_get_list_folder_left=data["board"]["left_menu"]["param_left"]

    if new_domain=="global3.hanbiro.com":
        url_get_list_folder_left=param["url_get_list_folder_left_gl3"]

    old_head_url_get_list_board=data["board"]["list_board"]["api"]
    head_url_get_list_board=change(new_domain,old_head_url_get_list_board,old_domain)
    param_get_list_board=data["board"]["list_board"]["param"]

    old_head_url_view_board=data["board"]["view_board"]["api"]
    head_url_view_board=change(new_domain,old_head_url_view_board,old_domain)
    param_view_board=data["board"]["view_board"]["param"]

    old_url_delete_board=data["board"]["delete_board"]["api"]
    url_delete_board=change(new_domain,old_url_delete_board,old_domain)
    param_delete_board=data["board"]["delete_board"]["param"]

    old_url_delete_board_by_view=data["board"]["delete_board"]["api_delete_view_board"]
    url_delete_board_by_view=change(new_domain,old_url_delete_board_by_view,old_domain)
    param_delete_board_by_view=data["board"]["delete_board"]["param_delete_view"]
        
    param_write_board=data["board"]["notice_board"]["write_board"]["param_write"]
    param_write_board["folder"]=str(notice[1])
    param_write_board["subject"]=board_name="TS1 Notice board"
    
    old_url_write_board=data["board"]["notice_board"]["write_board"]["api_write"]
    url_write_board=change(new_domain,old_url_write_board,old_domain)
    param_get_list_board["folder"]=str(notice[1])
    url_get_list_board=api(head_url_get_list_board,param_get_list_board) 
    param_delete_board["folder"]= str(notice[1])

    # TS1 #
    #if notice[2] == True :# subfolder display success    
    #get list board #   
    msg("t","[TS1]")
    ts1_success_get_list_board=get(url_get_list_board,"",cookie_writer(new_domain))
    if notification(ts1_success_get_list_board) == True :
        msg("p","  +TS1:Permission access folder => Pass")
        execution_test_link("WAPI-70","p")

        #check permission and write board #
        if ts1_success_get_list_board["attr"]["is_write"]== True :
            msg("p","  +TS1:Permission write board => Pass")
            execution_test_link("WAPI-45","p")


            success_write_board=post(url_write_board,param_write_board,cookie_writer(new_domain))
            if notification(success_write_board)== True :
                msg("p","  +TS1:Write board at folder notice => Pass")
                execution_test_link("WAPI-22","p")
                # check post #
                time.sleep(10)
                ts1_success_get_list_board1=get(url_get_list_board,"",cookie_writer(new_domain))
                if notification(ts1_success_get_list_board1)== True :
                    check_saved_board=check_the_saved_data(url_get_list_board, "",cookie_writer(new_domain),"subject",board_name,get,"rows")
                    if check_saved_board == True :
                        msg("p","    +TS1 :The board has been saved in the folder => Pass")
                        execution_test_link("WAPI-69","p")

                        #TS1 -view board #
                        if ts1_success_get_list_board1["attr"]["is_view"] == True :
                            msg("p","  +TS1 :Permission wiew board => Pass")
                            execution_test_link("WAPI-52","p")
                            
                            id_b=id_board(ts1_success_get_list_board1,board_name)
                            if view_board(notice[1],id_b,head_url_view_board,param_view_board,cookie_writer(new_domain))== True :
                                msg("p","  +TS1 :Click on board => Pass")
                                execution_test_link("WAPI-83","p")
                            else :
                                msg("f","  +TS1 :Click on board => Fail")
                                result.write("<div> [Board]TS1 :Click on board => Fail </div>")
                                execution_test_link("WAPI-83","f")     
                        else :
                            msg("f","  +TS1 :Permission wiew board => Fail")
                            result.write("<div> [Board]TS1 :Permission wiew board => Fail </div>")
                            execution_test_link("WAPI-52","f")

                    else :
                        msg("f","  +TS1 :The board has been saved in the folder => Fail")
                        result.write("<div> [Board]TS1 :The board has been saved in the folder => Fail </div>")
                        execution_test_link("WAPI-69","f")


            else : 
                msg("f","  +TS1:Write board at folder notice => Fail")
                result.write("<div> [Board]TS1:Write board at folder notice => Fail </div>")
                execution_test_link("WAPI-22","f")
        else :
            msg("f","  +TS1:Permission write board => Fail")
            result.write("<div> [Board]TS1:Permission write board => Fail </div>")
            execution_test_link("WAPI-45","f")
        #check counter#
    else :
        msg("f","  +TS1:Permission access folder => Fail")
        result.write("<div> [Board]TS1:Permission access folder => Fail </div>")
        execution_test_link("WAPI-70","f")

    msg("t","[TS2]")
    # TS2 #
    ts2_success_get_list_folder_left=get(url_get_list_folder_left,param_get_list_folder_left,cookie_recipient(new_domain))
    if notification(ts2_success_get_list_folder_left)== True :
        board_success_folder(notice,"WAPI-41",board_notice_name,"TS2",ts2_success_get_list_folder_left,folder_no,result,new_domain)
        if notice[2] == True :# subfolder display  
            ts2_success_get_list_board=get(url_get_list_board,"",cookie_recipient(new_domain))
            if notification(ts2_success_get_list_board) == True :
                msg("p","  +TS2:Permission access folder => Pass")
                execution_test_link("WAPI-70","p")

                #check permission and write board #
                if ts2_success_get_list_board["attr"]["is_write"]== False :
                    msg("p","  +TS2:Does not permission write board => Pass")
                    execution_test_link("WAPI-45","p")
                else :
                    msg("f","  +TS2:Does not permission write board => Fail")
                    result.write("<div> [Board]TS2:Does not permission write board => Fail </div>")
                    execution_test_link("WAPI-45","f")

                #TS2-view board#
                if ts2_success_get_list_board["attr"]["is_view"] == True :
                    msg("p","  +TS2 :Permission view board => Pass")
                    execution_test_link("WAPI-52","p")
                    if notification(success_write_board)== True:
                        board_of_ts1=check_the_saved_data(url_get_list_board, "",cookie_recipient(new_domain),"subject",board_name,get,"rows")
                        if board_of_ts1 == True :
                            msg("p","  +TS2 :View board of Ts1  => Pass")
                            execution_test_link("WAPI-52","p")
                            if view_board(notice[1],id_b,head_url_view_board,param_view_board,cookie_recipient(new_domain))== True :
                                msg("p","  +TS2 :Click on board => Pass")
                                execution_test_link("WAPI-83","p")
                            else :
                                msg("f","  +TS2 :Click on board => Fail")
                                result.write("<div> [Board]TS2 :Click on board => Fail </div>")
                                execution_test_link("WAPI-83","f")
                        else :
                            msg("p","  +TS2 :View board of Ts1  => Pass")
                            execution_test_link("WAPI-52","p")          
                else :
                    msg("f","  +TS2 :Permission view board => Fail")
                    result.write("<div> [Board]TS2 :Permission view board => Fail </div>")
                    execution_test_link("WAPI-52","f")

            else :
                msg("f","  +TS2:Permission access folder => Fail")
                result.write("<div> [Board]TS2:Permission access folder => Fail </div>")
                execution_test_link("WAPI-70","f")

    # add board to delete #
    if notification(success_write_board)== True :
        if check_saved_board == True :
            n=0
            while n < 3 :
                post(url_write_board,param_write_board,cookie_writer(new_domain))
                n +=1 
    
    msg("t","[Delete board by select board]")
    if notification(ts1_success_get_list_board1) == True :
        # TS1 delete board by select board #
        if ts1_success_get_list_board1["attr"]["is_del"]== True :
            msg("p","  +TS1 :Permission delete board by select board => Pass")
            execution_test_link("WAPI-71","p")
            if len(ts1_success_get_list_board1["rows"])==0 :
                msg("p","  +There is no board from board list")
            else :
                i=0
                board_to_delete =ts1_success_get_list_board1["rows"][0]["id"]
                data["board"]["delete_board"]["param"]["menu_head_list"]=ts1_success_get_list_board1["attr"]["menu_head_list"]
                data["board"]["delete_board"]["param"]["ids[0]"]=board_to_delete
                ts1_success_delete_board= post(url_delete_board,param_delete_board,cookie_writer(new_domain))
                if notification(ts1_success_delete_board) == True :
                    msg("p","  +TS1:Delete board => Pass")
                    execution_test_link("WAPI-72","p")
                    ts1_success_get_list_board_after_delete=get(url_get_list_board,"",cookie_writer(new_domain))
                    if notification(ts1_success_get_list_board_after_delete)== True :
                        for x in ts1_success_get_list_board_after_delete["rows"]:
                            if x["id"]== board_to_delete :
                                msg("f","    +TS1:The board deleted has been removed from list board => Fail")
                                result.write("<div> [Board]TS1:The board deleted has been removed from list board => Fail </div>")
                                execution_test_link("WAPI-72","f")
                                i=i+1 
                                break
                        if i==0 :
                            msg("p","    +TS1:The board deleted has been removed from list board => Pass")
                            execution_test_link("WAPI-72","p")

                    
                    # TS2 # 
                    ts2_success_get_list_board_after_delete=get(url_get_list_board,"",cookie_recipient(new_domain))
                    if notification(ts2_success_get_list_board_after_delete) == True : 
                        for x in ts2_success_get_list_board_after_delete["rows"]:
                            if x["id"]== board_to_delete :
                                msg("f","    +TS2:The board of TS1  has been removed from list board => Fail")
                                result.write("<div> [Board]TS2:The board of TS1  has been removed from list board => Fail </div>")
                                execution_test_link("WAPI-72","f")
                                i=i+1 
                                break
                        if i==0 :
                            msg("p","    +TS2:The board of TS1 has been removed from list board => Pass")
                            execution_test_link("WAPI-72","p")
                else:
                    msg("f","    +TS1:Delete board => Fail")
                    result.write("<div> [Board]TS1:Delete board => Fail </div>")
                    execution_test_link("WAPI-72","f")
        else :
            msg("n","  +TS1 :Permission delete board by select board [Note : This function only applies to domain custom ]")
            execution_test_link("WAPI-71","p")
    #TS2#
    ts2_success_get_list_board_1=get(url_get_list_board,"",cookie_recipient(new_domain))
    if notification(ts2_success_get_list_board_1)== True :
        if ts2_success_get_list_board_1["attr"]["is_del"]== False :
            msg("n","  +TS2 :Permission delete board by select board =>Pass")
            execution_test_link("WAPI-72","p")
        else :
            msg("f","  +TS2 :Permission delete board by select board => Fail")
            result.write("<div> [Board]TS2 :Permission delete board by select board => Fail </div>")
            execution_test_link("WAPI-72","f")
    
    # TS1 delete board by view board #
    msg("t","[Delete board by view board]")
    ts1_success_get_list_board_by_view=get(url_get_list_board,"",cookie_writer(new_domain))
    if notification(ts1_success_get_list_board_by_view) == True :
        if len(ts1_success_get_list_board_by_view["rows"])==0 :
            msg("p","  +TS1 :There is no board from board list")
        else :
            param_view_board["folder"]=param_delete_board_by_view["folder"]=notice[1]
            id_board_delete=param_view_board["id"]=param_delete_board_by_view["id"]=ts1_success_get_list_board_by_view["rows"][0]["id"]
            url_view_board=api(head_url_view_board,param_view_board)
            ts1_success_view_board= get(url_view_board,"", cookie_writer(new_domain))
            if notification(ts1_success_view_board)== True :
                if ts1_success_view_board["attr"]["is_del"]== True :
                    msg("p","  +TS1:Permission delete board by view board=> Pass")
                    execution_test_link("WAPI-88","p")
                    success_delete_board_view= post(url_delete_board_by_view,param_delete_board_by_view,cookie_writer(new_domain))
                    if notification(success_delete_board_view)== True :
                        msg("p","  +TS1:Delete board form view board => Pass")
                        execution_test_link("WAPI-89","p")

                        ts1_success_after_delete_by_view_board=get(url_get_list_board,"",cookie_writer(new_domain))
                        if notification(ts1_success_after_delete_by_view_board)== True :
                            i=0
                            if not ts1_success_after_delete_by_view_board :
                                msg("p","    +TS1:Board of TS1 has been removed form list board => Pass")
                                execution_test_link("WAPI-89","p")
                            else :
                                for x in ts1_success_after_delete_by_view_board["rows"]:
                                    if x["id"]== id_board_delete :
                                        msg("f","    +TS1:The board of TS1 has been removed from list board => Fail")
                                        result.write("<div> [Board]TS1:The board of TS1 has been removed from list board => Fail </div>")
                                        execution_test_link("WAPI-89","f")
                                        i=i+1 
                                        break
                                if i==0 :
                                    msg("p","    +TS1:The board of TS1 has been removed from list board => Pass")
                                    execution_test_link("WAPI-89","p")
                        # TS2 # 
                        ts2_get_list_board_after_delete_1=get(url_get_list_board,"",cookie_recipient(new_domain))
                        if notification(ts2_get_list_board_after_delete_1)== True :
                            for x in ts2_get_list_board_after_delete_1["rows"] :
                                if x["id"]== id_board_delete :
                                    msg("f","    +TS2:The board of TS1 has been removed from list board  => Fail")
                                    result.write("<div> [Board]TS2:The board of TS1 has been removed from list board  => Fail </div>")
                                    execution_test_link("WAPI-89","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS2:The board of TS1 has been removed from list board  => Pass")
                                execution_test_link("WAPI-89","p")

                    else :
                        msg("f","  +TS1 :delete board form view board => Fail")
                        result.write("<div> [Board]TS1 :delete board form view board => Fail </div>")
                        execution_test_link("WAPI-89","f")

                else :
                    msg("f","  +TS1:Permission delete board by view board=> Fail")
                    result.write("<div> [Board]TS1:Permission delete board by view board=> Fail </div>")
                    execution_test_link("WAPI-88","f")
        # TS2 #   
        ts2_success_get_list_board_1=get(url_get_list_board,"",cookie_recipient(new_domain))
        if notification(ts2_success_get_list_board_1)== True :
            if not ts2_success_get_list_board_1 :
                msg("p","  +TS2 :There is no board at list board")
            else :
                param_view_board["folder"]=notice[1]
                param_view_board["id"]=ts2_success_get_list_board_1["rows"][0]["id"]
                url_view_board=api(head_url_view_board,param_view_board)
                ts2_success_view_board= get(url_view_board,"", cookie_recipient(new_domain))
                if notification(ts2_success_view_board)== True :
                    if ts2_success_view_board["attr"]["is_del"]== False :
                        msg("p","  +TS2:No permission delete board by view board=> Pass")
                        execution_test_link("WAPI-88","p")
                    else:
                        msg("f","  +TS2:No permission delete board by view board=> Fail")
                        result.write("<div> [Board]TS2:No permission delete board by view board=> Fail </div>")
                        execution_test_link("WAPI-88","f")
            #counter(ts2_success_get_list_board_1)
def board_free(result,free,folder_no,new_domain):   
    #0 :success create folder , 1:id_folder , 2:saved folder 
    head_menu("B .Board Free  ")
    print("*TS1 :Write, read , modify , delete all board at folder*,*TS2 :Write, read ,modify-reply-delete the board of TS2*")
    board_free_name ="Free Board"
    old_url_get_list_folder_left=data["board"]["left_menu"]["api_left"]
    url_get_list_folder_left=change(new_domain,old_url_get_list_folder_left,old_domain)
    param_get_list_folder_left=data["board"]["left_menu"]["param_left"]
    if new_domain=="global3.hanbiro.com":
        url_get_list_folder_left=param["url_get_list_folder_left_gl3"]

    old_head_url_view_board=data["board"]["view_board"]["api"]
    head_url_view_board=change(new_domain,old_head_url_view_board,old_domain)
    param_view_board=data["board"]["view_board"]["param"]

    old_head_url_get_list_board=data["board"]["list_board"]["api"]
    head_url_get_list_board=change(new_domain,old_head_url_get_list_board,old_domain)
    param_get_list_board=data["board"]["list_board"]["param"]

    param_write_board=data["board"]["notice_board"]["write_board"]["param_write"]
    param_write_board["folder"]=str(free[1])
    param_write_board["subject"]=ts1_board_name="TS1 Free board"
    ts2_board_name="TS2 Free board"
    old_url_write_board=data["board"]["notice_board"]["write_board"]["api_write"]
    url_write_board=change(new_domain,old_url_write_board,old_domain)
    
    old_url_delete_board=data["board"]["delete_board"]["api"]
    url_delete_board=change(new_domain,old_url_delete_board,old_domain)
    param_delete_board=data["board"]["delete_board"]["param"]

    old_url_delete_board_by_view=data["board"]["delete_board"]["api_delete_view_board"]
    url_delete_board_by_view=change(new_domain,old_url_delete_board_by_view,old_domain)
    param_delete_board_by_view=data["board"]["delete_board"]["param_delete_view"]

    param_get_list_board["folder"]=str(free[1])
    url_get_list_board=api(head_url_get_list_board,param_get_list_board) 

    # TS1 #
    msg("t","[TS1]")
    ts1_success_get_list_board=get(url_get_list_board,"",cookie_writer(new_domain))
    if notification(ts1_success_get_list_board) == True :
        msg("p","  +TS1:Permission access folder => Pass")
        execution_test_link("WAPI-74","p")

        #check permission and write board #
        if ts1_success_get_list_board["attr"]["is_write"]== True :
            msg("p","  +TS1:Permission write board => Pass")
            execution_test_link("WAPI-47","p")
            success_write_board=post(url_write_board,param_write_board,cookie_writer(new_domain))
            if notification(success_write_board)== True :
                msg("p","  +TS1:Write board at folder free => Pass")
                execution_test_link("WAPI-46","p")

                #check board write #
                time.sleep(10)
                ts1_success_get_list_board1=get(url_get_list_board,"",cookie_writer(new_domain))
                if notification(ts1_success_get_list_board1)== True :
                    check_saved_board=check_the_saved_data(url_get_list_board, "",cookie_writer(new_domain),"subject",ts1_board_name,get,"rows")
                    if check_saved_board == True :
                        msg("p","    +TS1 :The board has been saved to list board => Pass")
                        execution_test_link("WAPI-73","p")
                    else :
                        msg("f","    +TS1 :The board has been saved to list board => Fail")
                        result.write("<div> [Board]TS1 :The board has been saved to list board => Fail </div>")
                        execution_test_link("WAPI-73","f")

                #TS2 view board of TS1 # 
                    
                ts2_view_board_ts1=check_the_saved_data(url_get_list_board, "",cookie_recipient(new_domain),"subject",ts1_board_name,get,"rows")
                if ts2_view_board_ts1 == True :
                    msg("p","    +TS2 :View board of TS1 => Pass")
                    execution_test_link("WAPI-76","p")
                    ts2_success_get_list_board1=get(url_get_list_board,"",cookie_recipient(new_domain))
                    id_b=id_board(ts2_success_get_list_board1,ts1_board_name)
                    if view_board(free[1],id_b,head_url_view_board,param_view_board,cookie_recipient(new_domain))== True :
                        msg("p","    +TS2 :Click on board of TS1 => Pass")
                        execution_test_link("WAPI-90","p")
                    else :
                        msg("f","    +TS2 :Click on board of TS1 => Fail")
                        result.write("<div> [Board]TS2 :Click on board of TS1 => Fail </div>")
                        execution_test_link("WAPI-90","f")
                else :
                    msg("f","    +TS2 :View board of TS1 => Fail")
                    result.write("<div> [Board]TS2 :View board of TS1 => Fail </div>")
                    execution_test_link("WAPI-76","f") 


            else : 
                msg("f","  +TS1:Write board at folder free => Fail")
                result.write("<div> [Board]TS1:Write board at folder free => Fail </div>")
                execution_test_link("WAPI-46","f")
        else :
            msg("f","  +TS1:Permission write board => Fail")
            result.write("<div> [Board]TS1:Permission write board => Fail </div>")
            execution_test_link("WAPI-47","f")

        #check counter#
        
        #view board#
        if ts1_success_get_list_board1["attr"]["is_view"] == True :
            msg("p","  +TS1 :Permission wiew board => Pass")
            execution_test_link("WAPI-76","p")
            if check_saved_board == True :
                id_b=id_board(ts1_success_get_list_board1,ts1_board_name)
                if view_board(free[1],id_b,head_url_view_board,param_view_board,cookie_writer(new_domain))== True :
                    msg("p","  +TS1 :Click on board => Pass")
                    execution_test_link("WAPI-90","p")
                else :
                    msg("f","  +TS1 :Click on board => Fail")
                    result.write("<div> [Board]TS1 :Click on board => Fail </div>")
                    execution_test_link("WAPI-90","f")     
        else :
            msg("f","  +TS1 :Permission wiew board => Fail")
            result.write("<div> [Board]TS1 :Permission wiew board => Fail </div>")
            execution_test_link("WAPI-76","f")
    else :
        msg("f","  +TS1:Permission access folder => Fail")
        result.write("<div> [Board]TS1:Permission access folder => Fail </div>")
        execution_test_link("WAPI-74","f")
    # TS2 #
    msg("t","[TS2]")
    ts2_success_get_list_folder_left=get(url_get_list_folder_left,param_get_list_folder_left,cookie_recipient(new_domain))
    if notification(ts2_success_get_list_folder_left)== True :
        board_success_folder(free,"WAPI-42",board_free_name,"TS2",ts2_success_get_list_folder_left,folder_no,result,new_domain)
        if free[2] == True :
            #get list board #
            #ts2_displayed_folder= True
            ts2_success_get_list_board=get(url_get_list_board,"",cookie_recipient(new_domain))
            if notification(ts2_success_get_list_board) == True :
                msg("p","  +TS2:Permission access folder => Pass")
                execution_test_link("WAPI-74","p")

                #check permission and write board #
                param_write_board["subject"]=ts2_board_name
                if ts2_success_get_list_board["attr"]["is_write"]== True :
                    msg("p","  +TS2:Permission write board => Pass")
                    execution_test_link("WAPI-47","p")
                    ts2_success_write_board=post(url_write_board,param_write_board,cookie_recipient(new_domain))
                    if notification(ts2_success_write_board)== True :
                        msg("p","  +TS2:Write board at folder free => Pass")
                        execution_test_link("WAPI-46","p")

                        #check board write #
                        ts2_success_get_list_board1=get(url_get_list_board,"",cookie_recipient(new_domain))
                        if notification(ts2_success_get_list_board1)== True :
                            ts2_check_saved_board=check_the_saved_data(url_get_list_board, "",cookie_recipient(new_domain),"subject",ts2_board_name,get,"rows")
                            if ts2_check_saved_board == True :
                                msg("p","    +TS2 :The board has been saved to list board => Pass")
                                execution_test_link("WAPI-73","p")

                                #view board#
                                if ts2_success_get_list_board1["attr"]["is_view"] == True :
                                    msg("p","  +TS2 :Permission wiew board => Pass")
                                    execution_test_link("WAPI-76","p")
                                    if ts2_check_saved_board == True :
                                        ts2_id_b=id_board(ts2_success_get_list_board1,ts2_board_name)
                                        if view_board(free[1],ts2_id_b,head_url_view_board,param_view_board,cookie_recipient(new_domain))== True :
                                            msg("p","  +TS2 :Click on board => Pass")
                                            execution_test_link("WAPI-90","p")
                                        else :
                                            msg("f","  +TS2 :Click on board => Fail")
                                            result.write("<div> [Board]TS2 :Click on board => Fail </div>")
                                            execution_test_link("WAPI-90","f")  
                                else :
                                    msg("f","  +TS2 :Permission wiew board => Fail")
                                    result.write("<div> [Board]TS2 :Permission wiew board => Fail </div>")
                                    execution_test_link("WAPI-76","f")
                        #TS1 view board of TS2 #  
                        ts1_view_board_ts2=check_the_saved_data(url_get_list_board, "",cookie_writer(new_domain),"subject",ts2_board_name,get,"rows")
                        if ts1_view_board_ts2 == True :
                            msg("p","  +TS1 :View board of TS2 => Pass")
                            execution_test_link("WAPI-76","p")
                            ts1_success_get_list_board3=get(url_get_list_board,"",cookie_writer(new_domain))
                            id_b_ts1=id_board(ts1_success_get_list_board3,ts2_board_name)
                            if view_board(free[1],id_b_ts1,head_url_view_board,param_view_board,cookie_writer(new_domain))== True :
                                msg("p","  +TS1 :Click on board of TS1 => Pass")
                                execution_test_link("WAPI-90","p")
                            else :
                                msg("f","  +TS1 :Click on board of TS1 => Fail")
                                result.write("<div> [Board]TS1 :Click on board of TS1 => Fail </div>")
                                execution_test_link("WAPI-90","f")
                        else :
                            msg("f","  +TS1 :View board of TS2 => Fail")
                            result.write("<div> [Board]TS1 :View board of TS2 => Fail </div>")
                            execution_test_link("WAPI-76","f")       

                    else : 
                        msg("f","  +TS2:Write board at folder free => Fail")
                        result.write("<div> [Board]TS2:Write board at folder free => Fail </div>")
                        execution_test_link("WAPI-46","f")
                else :
                    msg("f","  +TS2:Permission write board => Fail")
                    result.write("<div> [Board]TS2:Permission write board => Fail </div>")
                    execution_test_link("WAPI-47","f")
            else :
                msg("f","  +TS2:Permission access folder => Fail")
                result.write("<div> [Board]TS2:Permission access folder => Fail </div>")
                execution_test_link("WAPI-74","f")
                
                #check counter#
        

    #TS1 , TS2 add board to delete #
    if notification(success_write_board)== True :
        if check_saved_board == True :
            n=0
            param_write_board["subject"]=ts1_board_name
            while n < 3 :
                post(url_write_board,param_write_board,cookie_writer(new_domain))
                n +=1 
    
    if notification(ts2_success_write_board)== True :
        if ts2_check_saved_board == True :
            n=0
            param_write_board["subject"]=ts2_board_name
            while n < 3 :
                post(url_write_board,param_write_board,cookie_recipient(new_domain))
                n +=1 

    # Delete Board #
    
    #TS1 delete board by select board #
    msg("t","[Delete board by select board]")
    data["board"]["delete_board"]["param"]["folder"]=free[1]
    ts1_get_list_board_to_delete=get(url_get_list_board,"",cookie_writer(new_domain))
    if notification(ts1_get_list_board_to_delete) == True :
        if ts1_get_list_board_to_delete["attr"]["is_del"]== True :
            msg("p","  +TS1 :Permission delete board by select board => Pass")
            execution_test_link("WAPI-75","p")
            if not ts1_get_list_board_to_delete["rows"] :
                msg("p","  +TS1 :There is no board in folder")
            else :
            #TS1 delete board of TS1 #
                board_to_delete=""
                for x in ts1_get_list_board_to_delete["rows"] :
                    if x["name"] == 'TS1' :
                        board_to_delete =x["id"]
                        break 
                if len(board_to_delete)== 0 :
                    msg("p","  +TS1:There is no board of TS1 in folder")
                else :
                    data["board"]["delete_board"]["param"]["menu_head_list"]=ts1_get_list_board_to_delete["attr"]["menu_head_list"]
                    data["board"]["delete_board"]["param"]["ids[0]"]=board_to_delete
                    
                    ts1_success_delete_board_of_ts1= post(url_delete_board,param_delete_board,cookie_writer(new_domain))
                    if notification(ts1_success_delete_board_of_ts1) == True :
                        msg("p","  +TS1:Delete board of TS1 => Pass")
                        execution_test_link("WAPI-91","p")
                        #TS1#
                        time.sleep(10)
                        ts1_success_get_list_board_after_delete=get(url_get_list_board,"",cookie_writer(new_domain))
                        i=0
                        if notification(ts1_success_get_list_board_after_delete)== True :
                            i=0
                            for x in ts1_success_get_list_board_after_delete["rows"]:
                                if x["id"]== board_to_delete :
                                    msg("f","    +TS1:The board of TS1 has been removed from list board => Fail")
                                    result.write("<div> [Board]TS1:The board of TS1 has been removed from list board => Fail </div>")
                                    execution_test_link("WAPI-91","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS1:The board of TS1 has been removed from list board => Pass")
                                execution_test_link("WAPI-91","p")
                        #TS2#
                        ts2_success_get_list_board_after_ts1_delete=get(url_get_list_board,"",cookie_recipient(new_domain))
                        if notification(ts2_success_get_list_board_after_ts1_delete)== True :
                            i=0
                            for x in ts2_success_get_list_board_after_ts1_delete["rows"]:
                                if x["id"]== board_to_delete :
                                    msg("f","    +TS2:The board of TS1 has been removed from list board => Fail")
                                    result.write("<div> [Board]TS2:The board of TS1 has been removed from list board => Fail </div>")
                                    execution_test_link("WAPI-91","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS2:The board of TS1 has been removed from list board => Pass")
                                execution_test_link("WAPI-91","p")
                    else :
                        msg("f","  +TS1:Delete board of TS1 => Fail")
                        result.write("<div> [Board]TS1:Delete board of TS1 => Fail </div>")
                        execution_test_link("WAPI-91","f")

            # TS1 delete board of TS2 #
                board_to_delete_1=""
                for x in ts1_get_list_board_to_delete["rows"] :
                    if x["name"]=="TS2" :
                        board_to_delete_1 =x["id"]
                        break 
                if len(board_to_delete_1)== 0 :
                    msg("p","  +TS1:There is no board of TS2 in folder")
                else :
                    data["board"]["delete_board"]["param"]["menu_head_list"]=ts1_get_list_board_to_delete["attr"]["menu_head_list"]
                    data["board"]["delete_board"]["param"]["ids[0]"]=board_to_delete_1
                    ts1_success_delete_board_of_ts2= post(url_delete_board,param_delete_board,cookie_writer(new_domain))
                    if notification(ts1_success_delete_board_of_ts2) == True :
                        msg("p","  +TS1:Delete board of TS2 => Pass")
                        #TS1#
                        execution_test_link("WAPI-91","p")
                        ts1_success_get_list_board_after_delete_1=get(url_get_list_board,"",cookie_writer(new_domain))
                        if notification(ts1_success_get_list_board_after_delete_1)== True :
                            i=0
                            for x in ts1_success_get_list_board_after_delete_1["rows"]:
                                if x["id"]== board_to_delete_1 :
                                    msg("f","    +TS1:The board of TS2 has been removed from list board => Fail")
                                    result.write("<div> [Board]TS1:The board of TS2 has been removed from list board => Fail </div>")
                                    execution_test_link("WAPI-91","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS1:The board of TS2 has been removed from list board => Pass")
                                execution_test_link("WAPI-91","p")
                        #TS2#
                        ts2_success_get_list_board_after_ts1_delete_1=get(url_get_list_board,"",cookie_recipient(new_domain))
                        if notification(ts2_success_get_list_board_after_ts1_delete_1)== True :
                            i=0
                            for x in ts2_success_get_list_board_after_ts1_delete_1["rows"]:
                                if x["id"]== board_to_delete :
                                    msg("f","    +TS2:The board of TS2 has been removed from list board  => Fail")
                                    result.write("<div> [Board]TS2:The board of TS2 has been removed from list board  => Fail </div>")
                                    execution_test_link("WAPI-91","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS2:The board of TS2 has been removed from list board  => Pass")
                                execution_test_link("WAPI-91","p")
                    else :
                        msg("f","  +TS1:Delete board of TS2 => Fail")
                        result.write("<div> [Board]TS1:Delete board of TS2 => Fail </div>")
                        execution_test_link("WAPI-91","f")
        else :
            msg("n","  +TS1 :Permission delete board by select board [Note : This function only applies to domain custom ]")
            execution_test_link("WAPI-75","p")
    #
    # TS2 delete board by select board #
    ts2_get_list_board_to_delete_3=get(url_get_list_board,"",cookie_recipient(new_domain))
    if notification(ts2_get_list_board_to_delete_3) == True :
        if ts2_get_list_board_to_delete_3["attr"]["is_del"]== False :
            msg("n","  +TS2 :Permission delete board by select board => Pass")
            execution_test_link("WAPI-75","p")
        else :
            msg("f","  +TS2 :Permission delete board by select board => Fail")
            result.write("<div> [Board]TS2 :Permission delete board by select board => Fail </div>")
            execution_test_link("WAPI-75","f")  
    

    # TS1 delete board by view board #
    msg("t","[Delete board by view board]")
    ts1_success_get_list_board_by_view=get(url_get_list_board,"",cookie_writer(new_domain))
    if notification(ts1_success_get_list_board_by_view) == True :
        if not ts1_success_get_list_board_by_view :
            msg("p","  +TS1:There is no board in folder")
        else :
            #TS1 delete board of TS1 #
            board_to_delete_view=""
            for x in ts1_success_get_list_board_by_view["rows"] :
                if x["name"] == 'TS1' :
                    board_to_delete_view =x["id"]
                    break 
            if len(board_to_delete_view)== 0 :
                msg("p","  +TS1:There is no board of TS1 in folder")
            else :
                param_view_board["folder"]=param_delete_board_by_view["folder"]=free[1]
                param_view_board["id"]=param_delete_board_by_view["id"]=board_to_delete_view
                url_view_board=api(head_url_view_board,param_view_board)
                ts1_success_view_board_1= get(url_view_board,"", cookie_writer(new_domain))
                if notification(ts1_success_view_board_1)== True :
                    if ts1_success_view_board_1["attr"]["is_del"]== True :
                        msg("p","  +TS1:Permission delete board of TS1 by view board=> Pass")
                        execution_test_link("WAPI-92","p")
                        ts1_success_delete_board_view_of_ts1= post(url_delete_board_by_view,param_delete_board_by_view,cookie_writer(new_domain))
                        if notification(ts1_success_delete_board_view_of_ts1)== True :
                            msg("p","  +TS1:Delete board of TS1 by view board => Pass")
                            execution_test_link("WAPI-93","p")

                            ts1_success_after_delete_by_view_board=get(url_get_list_board,"",cookie_writer(new_domain))
                            if notification(ts1_success_after_delete_by_view_board)== True :
                                i=0
                                if not ts1_success_after_delete_by_view_board :
                                    msg("p","    +TS1:The board of TS1 has been removed from list board => Pass")
                                    execution_test_link("WAPI-93","p")
                                else :
                                    for x in ts1_success_after_delete_by_view_board["rows"]:
                                        if x["id"]== board_to_delete_view :
                                            msg("f","    +TS1:The board of TS1 has been removed from list board => Fail")
                                            result.write("<div> [Board]TS1:The board of TS1 has been removed from list board => Fail </div>")
                                            execution_test_link("WAPI-93","f")
                                            i=i+1 
                                            break
                                    if i==0 :
                                        msg("p","    +TS1:The board of TS1 has been removed from list board => Pass")
                                        execution_test_link("WAPI-93","p")
                            # TS2 # 
                            ts2_get_list_board_after_delete_view=get(url_get_list_board,"",cookie_recipient(new_domain))
                            if notification(ts2_get_list_board_after_delete_view)== True :
                                for x in ts2_get_list_board_after_delete_view["rows"] :
                                    if x["id"]== board_to_delete_view :
                                        msg("f","    +TS2:The board of TS1 has been removed from list board => Fail")
                                        result.write("<div> [Board]TS2:The board of TS1 has been removed from list board => Fail </div>")
                                        execution_test_link("WAPI-93","f")
                                        i=i+1 
                                        break
                                if i==0 :
                                    msg("p","    +TS2:The board of TS1 has been removed from list board => Pass")
                                    execution_test_link("WAPI-93","p")

                        else :
                            msg("f","  +TS1 :Delete board of TS1 by view board => Fail")
                            result.write("<div> [Board]TS1 :Delete board of TS1 by view board => Fail </div>")
                            execution_test_link("WAPI-93","f")

                    else :
                        msg("f","  +TS1:Permission delete board of TS1 by view board=> Fail")
                        result.write("<div> [Board]TS1:Permission delete board of TS1 by view board=> Fail </div>")
                        execution_test_link("WAPI-92","f")
            #TS1 delete board of TS2 #
            board_to_delete_view_1=""
            for x in ts1_success_get_list_board_by_view["rows"] :
                if x["name"] == 'TS2' :
                    board_to_delete_view_1 =x["id"]
                    break 
            if len(board_to_delete_view_1)== 0 :
                msg("p","  +TS1:There is no board of TS2 in folder")
            else :
                param_view_board["id"]=param_delete_board_by_view["id"]=board_to_delete_view_1
                url_view_board=api(head_url_view_board,param_view_board)
                ts1_success_view_board_2= get(url_view_board,"", cookie_writer(new_domain))
                if notification(ts1_success_view_board_2)== True :
                    if ts1_success_view_board_2["attr"]["is_del"]== True :
                        msg("p","  +TS1:Permission delete board of TS2 by view board=> Pass")
                        execution_test_link("WAPI-92","p")
                        ts1_success_delete_board_view_of_ts2= post(url_delete_board_by_view,param_delete_board_by_view,cookie_writer(new_domain))
                        if notification(ts1_success_delete_board_view_of_ts2)== True :
                            msg("p","  +TS1:Delete board of TS2 by view board => Pass")
                            execution_test_link("WAPI-93","p")

                            ts1_success_after_delete_by_view_board_1=get(url_get_list_board,"",cookie_writer(new_domain))
                            if notification(ts1_success_after_delete_by_view_board_1)== True :
                                i=0
                                if not ts1_success_after_delete_by_view_board_1 :
                                    msg("p","    +TS1:Board of TS2 has been removed removed form list board => Pass")
                                    execution_test_link("WAPI-93","p")
                                else :
                                    for x in ts1_success_after_delete_by_view_board_1["rows"]:
                                        if x["id"]== board_to_delete_view_1 :
                                            msg("f","    +TS1:The board of TS2 has been removed from list board => Fail")
                                            result.write("<div> [Board]TS1:The board of TS2 has been removed from list board => Fail </div>")
                                            execution_test_link("WAPI-93","f")
                                            i=i+1 
                                            break
                                    if i==0 :
                                        msg("p","    +TS1:The board of TS2 has been removed from list board => Pass")
                                        execution_test_link("WAPI-93","p")
                            # TS2 # 
                            ts2_get_list_board_after_delete_view_1=get(url_get_list_board,"",cookie_recipient(new_domain))
                            if notification(ts2_get_list_board_after_delete_view_1)== True :
                                for x in ts2_get_list_board_after_delete_view_1["rows"] :
                                    if x["id"]== board_to_delete_view_1 :
                                        msg("f","    +TS2:The board of TS2 has been removed from list board => Fail")
                                        result.write("<div> [Board]TS2:The board of TS2 has been removed from list board => Fail </div>")
                                        execution_test_link("WAPI-93","f")
                                        i=i+1 
                                        break
                                if i==0 :
                                    msg("p","    +TS2:The board of TS2 has been removed from list board => Pass")
                                    execution_test_link("WAPI-93","p")

                        else :
                            msg("f","  +TS1 :Delete board of TS2 by view board => Fail")
                            result.write("<div> [Board]TS1 :Delete board of TS2 by view board => Fail </div>")
                            execution_test_link("WAPI-93","f")

                    else :
                        msg("f","  +TS1:Permission delete board of TS2 by view board=> Fail")
                        result.write("<div> [Board]TS1:Permission delete board of TS2 by view board=> Fail </div>")
                        execution_test_link("WAPI-92","f")

    # TS2 delete board by view board #
    ts2_success_get_list_board_by_view=get(url_get_list_board,"",cookie_recipient(new_domain))
    if notification(ts2_success_get_list_board_by_view) == True :
        if not ts2_success_get_list_board_by_view :
            msg("p","  +TS2:There is no board in folder")
        else :
            #TS2 delete board of TS2 #
            ts2_board_to_delete_view=""
            for x in ts2_success_get_list_board_by_view["rows"] :
                if x["name"] == 'TS2' :
                    ts2_board_to_delete_view =x["id"]
                    break 
            if len(ts2_board_to_delete_view)== 0 :
                msg("p","  +TS2:There is no board of TS2 in folder")
            else :
                param_view_board["folder"]=param_delete_board_by_view["folder"]=free[1]
                param_view_board["id"]=param_delete_board_by_view["id"]=ts2_board_to_delete_view
                url_view_board=api(head_url_view_board,param_view_board)
                ts2_success_view_board_1= get(url_view_board,"", cookie_recipient(new_domain))
                if notification(ts2_success_view_board_1)== True :
                    if ts2_success_view_board_1["attr"]["is_del"]== True :
                        msg("p","  +TS2:Permission delete board of TS2 by view board=> Pass")
                        execution_test_link("WAPI-92","p")
                        ts2_success_delete_board_view_of_ts2= post(url_delete_board_by_view,param_delete_board_by_view,cookie_recipient(new_domain))
                        if notification(ts2_success_delete_board_view_of_ts2)== True :
                            msg("p","  +TS2:Delete board of TS2 by view board => Pass")
                            execution_test_link("WAPI-93","p")

                            ts2_success_after_delete_by_view_board=get(url_get_list_board,"",cookie_recipient(new_domain))
                            if notification(ts2_success_after_delete_by_view_board)== True :
                                i=0
                                if not ts2_success_after_delete_by_view_board :
                                    msg("p","    +TS2:The Board of TS2 has been removed form list board => Pass")
                                    execution_test_link("WAPI-93","p")
                                else :
                                    for x in ts2_success_after_delete_by_view_board["rows"]:
                                        if x["id"]== ts2_board_to_delete_view :
                                            msg("f","    +TS2:The board of TS2 has been removed form list board => Fail")
                                            result.write("<div> [Board]TS2:The board of TS2 has been removed form list board => Fail </div>")
                                            execution_test_link("WAPI-93","f")
                                            i=i+1 
                                            break
                                    if i==0 :
                                        msg("p","    +TS2:The board of TS2 has been removed form list board => Pass")
                                        execution_test_link("WAPI-93","p")
                            # TS1 # 
                            ts1_get_list_board_after_delete_view=get(url_get_list_board,"",cookie_writer(new_domain))
                            if notification(ts1_get_list_board_after_delete_view)== True :
                                for x in ts1_get_list_board_after_delete_view["rows"] :
                                    if x["id"]== ts2_board_to_delete_view :
                                        msg("f","    +TS1:The board of TS2 has been removed form list board => Fail")
                                        result.write("<div> [Board]TS1:The board of TS2 has been removed form list board => Fail </div>")
                                        execution_test_link("WAPI-93","f")
                                        i=i+1 
                                        break
                                if i==0 :
                                    msg("p","    +TS1:The board of TS1 has been removed form list board => Pass")
                                    execution_test_link("WAPI-93","p")

                        else :
                            msg("f","  +TS2 :Delete board of TS2 by view board => Fail")
                            result.write("<div> [Board]TS2 :Delete board of TS2 by view board => Fail </div>")
                            execution_test_link("WAPI-93","f")

                    else :
                        msg("f","  +TS2:Permission delete board of TS2 by view board=> Fail")
                        result.write("<div> [Board]TS2:Permission delete board of TS2 by view board=> Fail </div>")
                        execution_test_link("WAPI-92","f")
            
            #TS2 delete board of TS1 #
            for x in ts2_success_get_list_board_by_view["rows"] :
                if x["name"] == 'TS1' :
                    ts2_board_to_delete_view_3 =x["id"]
                    break 
            if len(ts2_board_to_delete_view_3)== 0 :
                msg("p","  +TS2:There is no board of TS1 in folder")
            else :
                param_view_board["id"]=param_delete_board_by_view["id"]=ts2_board_to_delete_view_3
                url_view_board=api(head_url_view_board,param_view_board)
                ts2_success_view_board_2= get(url_view_board,"", cookie_recipient(new_domain))
                if notification(ts2_success_view_board_2)== True :
                    if ts2_success_view_board_2["attr"]["is_del"]== False :
                        msg("p","  +TS2:No permission delete board of TS1 by view board=> Pass")
                        execution_test_link("WAPI-92","p")
                    else :
                        msg("f","  +TS2:No permission delete board of TS1 by view board=> Fail")
                        result.write("<div> [Board]TS2:No permission delete board of TS1 by view board=> Fail </div>")
                        execution_test_link("WAPI-92","f")
def board_permit(result,permit,folder_no,new_domain):
    #0 :success create folder , 1:id_folder , 2:saved folder 
    head_menu("C .Board Permit  ")
    print("*TS1,TS2 :Write, read , modify , delete all board at folder* , *TS6 :No permission*")
    old_url_get_list_folder_left=data["board"]["left_menu"]["api_left"]
    url_get_list_folder_left=change(new_domain,old_url_get_list_folder_left,old_domain)
    param_get_list_folder_left=data["board"]["left_menu"]["param_left"]
    if new_domain=="global3.hanbiro.com":
        url_get_list_folder_left=param["url_get_list_folder_left_gl3"]

    old_head_url_get_list_board=data["board"]["list_board"]["api"]
    head_url_get_list_board=change(new_domain,old_head_url_get_list_board,old_domain)
    param_get_list_board=data["board"]["list_board"]["param"]

    old_head_url_view_board=data["board"]["view_board"]["api"]
    head_url_view_board=change(new_domain,old_head_url_view_board,old_domain)
    param_view_board=data["board"]["view_board"]["param"]

    param_write_board=data["board"]["notice_board"]["write_board"]["param_write"]
    param_write_board["folder"]=str(permit[1])
    param_write_board["subject"]=ts1_board_name="TS1 Permit board"
    #ts6_board_name="TS6 Permit board"
    old_url_write_board=data["board"]["notice_board"]["write_board"]["api_write"]
    url_write_board=change(new_domain,old_url_write_board,old_domain)
    
    param_get_list_board["folder"]=str(permit[1])
    url_get_list_board=api(head_url_get_list_board,param_get_list_board)


    # TS1 #
    msg("t","[TS1]")
    ts1_success_get_list_board=get(url_get_list_board,"",cookie_writer(new_domain))
    folder_permit_name =ts1_success_get_list_board["attr"]["folder_data"]["name"]
    if notification(ts1_success_get_list_board) == True :
        msg("p","  +TS1:Permission access folder => Pass")
        execution_test_link("WAPI-77","p")
        # get folder name #
        folder_permit_name =ts1_success_get_list_board["attr"]["folder_data"]["name"]
        #check permission and write board #
        if ts1_success_get_list_board["attr"]["is_write"]== True :
            msg("p","  +TS1:Permission write board => Pass")
            execution_test_link("WAPI-48","p")
            success_write_board=post(url_write_board,param_write_board,cookie_writer(new_domain))
            if notification(success_write_board)== True :
                msg("p","  +TS1:Write board at folder Permit => Pass")
                execution_test_link("WAPI-49","p")

                #check board write #
                ts1_success_get_list_board1=get(url_get_list_board,"",cookie_writer(new_domain))
                if notification(ts1_success_get_list_board1)== True :
                    check_saved_board=check_the_saved_data(url_get_list_board, "",cookie_writer(new_domain),"subject",ts1_board_name,get,"rows")
                    if check_saved_board == True :
                        msg("p","    +TS1 :The board has been saved to list board => Pass")
                        execution_test_link("WAPI-96","p")

                        #view board#
                        if ts1_success_get_list_board1["attr"]["is_view"] == True :
                            msg("p","  +TS1 :Permission wiew board => Pass")
                            execution_test_link("WAPI-54","p")
                            if check_saved_board == True :
                                id_b=id_board(ts1_success_get_list_board1,ts1_board_name)
                                if view_board(permit[1],id_b,head_url_view_board,param_view_board,cookie_writer(new_domain))== True :
                                    msg("p","  +TS1 :Click on board => Pass")
                                    execution_test_link("WAPI-78","p")
                                else :
                                    msg("f","  +TS1 :Click on board => Fail")
                                    result.write("<div> [Board]TS1 :Click on board => Fail </div>")
                                    execution_test_link("WAPI-78","f")     
                        else :
                            msg("f","  +TS1 :Permission wiew board => Fail")
                            result.write("<div> [Board]TS1 :Permission wiew board => Fail </div>")
                            execution_test_link("WAPI-54","f")

                    else :
                        msg("f","    +TS1 :The board has been saved to list board => Fail")
                        result.write("<div> [Board]TS1 :The board has been saved to list board => Fail </div>")
                        execution_test_link("WAPI-96","f")
            else : 
                msg("f","  +TS1:Write board at folder Permit => Fail")
                result.write("<div> [Board]TS1:Write board at folder Permit => Fail </div>")
                execution_test_link("WAPI-49","f")
        else :
            msg("f","  +TS1:Permission write board => Fail")
            result.write("<div> [Board]TS1:Permission write board => Fail </div>")
            execution_test_link("WAPI-48","f")

    else :
        msg("f","  +TS1:Permission access folder => Fail")
        result.write("<div> [Board]TS1:Permission access folder => Fail </div>")
        execution_test_link("WAPI-77","f")
    # TS2 #
    msg("t","[TS2]")
    ts2_success_get_list_folder_left=get(url_get_list_folder_left,param_get_list_folder_left,cookie_recipient(new_domain)) 
    if notification(ts2_success_get_list_folder_left)== True :
        if board_check_folder_by_name(ts2_success_get_list_folder_left,folder_no,folder_permit_name,new_domain) == True :
            msg("p","  +TS2:Permission with folder => Pass")
            execution_test_link("WAPI-43","p")
        else :
            msg("f","  +TS2:Permission with folder => Fail")
            result.write("<div> [Board]TS6:Show created folder => Fail </div>")
            execution_test_link("WAPI-43","f")
    # TS6 #
    msg("t","[TS6]")
    ts6_success_get_list_folder_left=get(url_get_list_folder_left,param_get_list_folder_left,another_user(new_domain))
    if notification(ts6_success_get_list_folder_left)== True :
        if board_check_folder_by_name(ts6_success_get_list_folder_left,folder_no,folder_permit_name,new_domain) == False :
            msg("p","  +TS6: No permission with folder permit => Pass")
            execution_test_link("WAPI-43","p")
        else :
            msg("f","  +TS6:No permission with folder permit => Fail")
            result.write("<div> [Board]TS2:No permission with folder permit => Fail </div>")
            execution_test_link("WAPI-43","f")
def board_1_1(result,board_1,folder_no,new_domain):
    #0 :success create folder , 1:id_folder , 2:saved folder 
    head_menu("D .Board 1:1 ")
    print("*TS1,TS6: Write, read , modify , delete all board *,*TS2:Write, read , modify-reply-delete the board of TS2*")
    board_1_1_name ="1:1 Board"
    old_url_get_list_folder_left=data["board"]["left_menu"]["api_left"]
    url_get_list_folder_left=change(new_domain,old_url_get_list_folder_left,old_domain)
    param_get_list_folder_left=data["board"]["left_menu"]["param_left"]
    if new_domain=="global3.hanbiro.com":
        url_get_list_folder_left=param["url_get_list_folder_left_gl3"]

    old_head_url_get_list_board=data["board"]["list_board"]["api"]
    head_url_get_list_board=change(new_domain,old_head_url_get_list_board,old_domain)
    param_get_list_board=data["board"]["list_board"]["param"]

    old_head_url_view_board=data["board"]["view_board"]["api"]
    head_url_view_board=change(new_domain,old_head_url_view_board,old_domain)
    param_view_board=data["board"]["view_board"]["param"]

    old_url_delete_board=data["board"]["delete_board"]["api"]
    url_delete_board=change(new_domain,old_url_delete_board,old_domain)
    param_delete_board=data["board"]["delete_board"]["param"]

    old_url_delete_board_by_view=data["board"]["delete_board"]["api_delete_view_board"]
    url_delete_board_by_view=change(new_domain,old_url_delete_board_by_view,old_domain)
    param_delete_board_by_view=data["board"]["delete_board"]["param_delete_view"]
    
    param_write_board=data["board"]["notice_board"]["write_board"]["param_write"]
    param_write_board["folder"]=str(board_1[1])
    param_write_board["subject"]=ts1_board_name="TS1 1:1 board"
    ts2_board_name="TS2 1:1 board"
    ts6_board_name="TS6 1:1 board"
    old_url_write_board=data["board"]["notice_board"]["write_board"]["api_write"]
    url_write_board=change(new_domain,old_url_write_board,old_domain)
    
    param_get_list_board["folder"]=str(board_1[1])
    url_get_list_board=api(head_url_get_list_board,param_get_list_board) 

    # TS1 #
    msg("t","[TS1]")
    ts1_success_get_list_board=get(url_get_list_board,"",cookie_writer(new_domain))
    if notification(ts1_success_get_list_board) == True :
        msg("p","  +TS1:Permission access folder => Pass")
        execution_test_link("WAPI-79","p")

        #check permission and write board #
        if ts1_success_get_list_board["attr"]["is_write"]== True :
            msg("p","  +TS1:Permission write board => Pass")
            execution_test_link("WAPI-50","p")
            success_write_board=post(url_write_board,param_write_board,cookie_writer(new_domain))
            if notification(success_write_board)== True :
                msg("p","  +TS1:Write board at folder free => Pass")
                execution_test_link("WAPI-51","p")

                #check board write #
                ts1_success_get_list_board1=get(url_get_list_board,"",cookie_writer(new_domain))
                if notification(ts1_success_get_list_board1)== True :
                    check_saved_board=check_the_saved_data(url_get_list_board, "",cookie_writer(new_domain),"subject",ts1_board_name,get,"rows")
                    if check_saved_board == True :
                        msg("p","    +TS1 :The board has been saved to list board => Pass")
                        execution_test_link("WAPI-53","p")

                        #view board#
                        if ts1_success_get_list_board1["attr"]["is_view"] == True :
                            msg("p","  +TS1 :Permission wiew board => Pass")
                            execution_test_link("WAPI-55","p")
                            id_b=id_board(ts1_success_get_list_board1,ts1_board_name)
                            if view_board(board_1[1],id_b,head_url_view_board,param_view_board,cookie_writer(new_domain))== True :
                                msg("p","  +TS1 :Click on board => Pass")
                                execution_test_link("WAPI-80","p")
                            else :
                                msg("f","  +TS1 :Click on board => Fail")
                                result.write("<div> [Board]TS1 :Click on board => Fail </div>")
                                execution_test_link("WAPI-80","f")     
                        else :
                            msg("f","  +TS1 :Permission wiew board => Fail")
                            result.write("<div> [Board]TS1 :Permission wiew board => Fail </div>")
                            execution_test_link("WAPI-55","f")
                        
                    else :
                        msg("f","    +TS1 :The board has been saved to list board => Fail")
                        result.write("<div> [Board]TS1 :The board has been saved to list board => Fail </div>")
                        execution_test_link("WAPI-53","f")

                # TS2 view board of TS1 #
                ts2_success_get_list_board_view_ts1=get(url_get_list_board,"",cookie_recipient(new_domain))
                if notification(ts2_success_get_list_board_view_ts1) ==  True :
                    ts2_view_board_ts1=check_the_saved_data(url_get_list_board, "",cookie_recipient(new_domain),"subject",ts1_board_name,get,"rows")
                    if ts2_view_board_ts1 == True :
                        msg("p","  +TS2 :View board of TS1 => Pass")
                        execution_test_link("WAPI-55","p")

                        ts2_id_view_ts1=id_board(ts2_success_get_list_board_view_ts1,ts1_board_name)
                        if view_board(board_1[1],ts2_id_view_ts1,head_url_view_board,param_view_board,cookie_recipient(new_domain))== True :
                            msg("p","  +TS2 :Click on board of TS1 => Pass")
                            execution_test_link("WAPI-80","p")
                        else :
                            msg("f","  +TS2 :Click on board of TS1 => Fail")
                            result.write("<div> [Board]TS2 :Click on board of TS1 => Fail </div>")
                            execution_test_link("WAPI-80","f")
                    else :
                        msg("f","  +TS2 :View board of TS1 => Fail")
                        result.write("<div> [Board]TS2 :View board of TS1 => Fail </div>")
                        execution_test_link("WAPI-55","f") 

                # TS6 view board of TS1 #
                ts6_success_get_list_board_view_ts1=get(url_get_list_board,"",another_user(new_domain))
                if notification(ts6_success_get_list_board_view_ts1) ==  True :
                    ts6_view_board_ts1=check_the_saved_data(url_get_list_board, "",another_user(new_domain),"subject",ts1_board_name,get,"rows")
                    if ts6_view_board_ts1 == False :
                        msg("p","  +TS6 :Can not see board of TS1 => Pass")
                        execution_test_link("WAPI-55","p")
                    else :
                        msg("f","  +TS6 :Can not see board of TS1 => Fail")
                        result.write("<div> [Board]TS6 :Can not see board of TS1 => Fail </div>")
                        execution_test_link("WAPI-55","f") 
                
                #check counter#
            else : 
                msg("f","  +TS1:Write board at folder free => Fail")
                result.write("<div> [Board]TS1:Write board at folder free => Fail </div>")
                execution_test_link("WAPI-51","f")
        else :
            msg("f","  +TS1:Permission write board => Fail")
            result.write("<div> [Board]TS1:Permission write board => Fail </div>")
            execution_test_link("WAPI-50","f")
    else :
        msg("f","  +TS1:Permission access folder => Fail")
        result.write("<div> [Board]TS1:Permission access folder => Fail </div>")
        execution_test_link("WAPI-79","f")

    # TS2 #
    msg("t","[TS2]")
    ts2_success_get_list_folder_left=get(url_get_list_folder_left,param_get_list_folder_left,cookie_recipient(new_domain))
    if notification(ts2_success_get_list_folder_left)== True :
        board_success_folder(board_1,"WAPI-42",board_1_1_name,"TS2",ts2_success_get_list_folder_left,folder_no,result,new_domain)
        if board_1[2] == True :
            #get list board #
            #ts2_displayed_folder= True
            ts2_success_get_list_board=get(url_get_list_board,"",cookie_recipient(new_domain))
            if notification(ts2_success_get_list_board) == True :
                msg("p","  +TS2:Permission access folder => Pass")
                execution_test_link("WAPI-79","p")

                #check permission and write board #
                param_write_board["subject"]=ts2_board_name
                if ts2_success_get_list_board["attr"]["is_write"]== True :
                    msg("p","  +TS2:Permission write board => Pass")
                    execution_test_link("WAPI-50","p")
                    ts2_success_write_board=post(url_write_board,param_write_board,cookie_recipient(new_domain))
                    if notification(ts2_success_write_board)== True :
                        msg("p","  +TS2:Write board at folder 1:1 => Pass")
                        execution_test_link("WAPI-51","p")

                        #check board write #
                        ts2_success_get_list_board1=get(url_get_list_board,"",cookie_recipient(new_domain))
                        if notification(ts2_success_get_list_board1)== True :
                            ts2_check_saved_board=check_the_saved_data(url_get_list_board, "",cookie_recipient(new_domain),"subject",ts2_board_name,get,"rows")
                            if ts2_check_saved_board == True :
                                msg("p","    +TS2 :The board has been saved to list board => Pass")
                                execution_test_link("WAPI-53","p")

                                #TS2 view board of TS2#
                                if ts2_success_get_list_board1["attr"]["is_view"] == True :
                                    msg("p","  +TS1 :Permission wiew board => Pass")
                                    execution_test_link("WAPI-55","p")
                                    id_b_1=id_board(ts2_success_get_list_board1,ts2_board_name)
                                    if view_board(board_1[1],id_b_1,head_url_view_board,param_view_board,cookie_recipient(new_domain))== True :
                                        msg("p","  +TS2 :Click on board => Pass")
                                        execution_test_link("WAPI-80","p")
                                    else :
                                        msg("f","  +TS2 :Click on board => Fail")
                                        result.write("<div> [Board]TS2 :Click on board => Fail </div>")
                                        execution_test_link("WAPI-80","f")     
                                else :
                                    msg("f","  +TS1 :Permission wiew board => Fail")
                                    result.write("<div> [Board]TS1 :Permission wiew board => Fail </div>")
                                    execution_test_link("WAPI-55","f")


                            else :
                                msg("f","    +TS2 :The board has been saved to list board => Fail")
                                result.write("<div> [Board]TS2 :The board has been saved to list board => Fail </div>")
                                execution_test_link("WAPI-53","f")
                        #
                        # TS1 view board of TS2 #
                        ts1_success_get_list_board_view_ts2=get(url_get_list_board,"",cookie_writer(new_domain))
                        if notification(ts1_success_get_list_board_view_ts2) ==  True :
                            ts1_view_board_ts2=check_the_saved_data(url_get_list_board, "",cookie_writer(new_domain),"subject",ts2_board_name,get,"rows")
                            if ts1_view_board_ts2 == True :
                                msg("p","  +TS1 :View board of TS2 => Pass")
                                execution_test_link("WAPI-55","p")

                                ts1_id_view_ts2=id_board(ts1_success_get_list_board_view_ts2,ts2_board_name)
                                if view_board(board_1[1],ts1_id_view_ts2,head_url_view_board,param_view_board,cookie_writer(new_domain))== True :
                                    msg("p","  +TS1 :Click on board of TS2 => Pass")
                                    execution_test_link("WAPI-80","p")
                                else :
                                    msg("f","  +TS1 :Click on board of TS2 => Fail")
                                    result.write("<div> [Board]TS1 :Click on board of TS2 => Fail </div>")
                                    execution_test_link("WAPI-80","f")
                            else :
                                msg("f","  +TS1 :View board of TS2 => Fail")
                                result.write("<div> [Board]TS1 :View board of TS2 => Fail </div>")
                                execution_test_link("WAPI-55","f") 

                        # TS6 view board of TS1 #
                        ts6_success_get_list_board_view_ts2=get(url_get_list_board,"",another_user(new_domain))
                        if notification(ts6_success_get_list_board_view_ts2) ==  True :
                            ts6_view_board_ts2=check_the_saved_data(url_get_list_board, "",another_user(new_domain),"subject",ts2_board_name,get,"rows")
                            if ts6_view_board_ts2 == False :
                                msg("p","  +TS6 :Can not see board of TS2 => Pass")
                                execution_test_link("WAPI-55","p")
                            else :
                                msg("f","  +TS6 :Can not see board of TS2 => Fail")
                                result.write("<div> [Board]TS6 :Can not see board of TS2 => Fail </div>")
                                execution_test_link("WAPI-55","f") 
                    else : 
                        msg("f","  +TS2:Write board at folder 1:1 => Fail")
                        result.write("<div> [Board]TS2:Write board at folder 1:1 => Fail </div>")
                        execution_test_link("WAPI-51","f")
                else :
                    msg("f","  +TS2:Permission write board => Fail")
                    result.write("<div> [Board]TS2:Permission write board => Fail </div>")
                    execution_test_link("WAPI-50","f")

                #check counter#
            else :
                msg("f","  +TS2:Permission access folder => Fail")
                result.write("<div> [Board]TS2:Permission access folder => Fail </div>")
                execution_test_link("WAPI-79","f")
    # TS6 #
    msg("t","[TS6]")
    ts6_success_get_list_folder_left=get(url_get_list_folder_left,param_get_list_folder_left,another_user(new_domain))
    if notification(ts6_success_get_list_folder_left)== True :
        board_success_folder(board_1,"WAPI-42",board_1_1_name,"TS6",ts6_success_get_list_folder_left,folder_no,result,new_domain)
        if board_1[2] == True :
            # get list board #
            #ts6_displayed_folder= True
            ts6_success_get_list_board=get(url_get_list_board,"",another_user(new_domain))
            if notification(ts6_success_get_list_board) == True :
                msg("p","  +TS6:Permission access folder => Pass")
                execution_test_link("WAPI-79","p")

                #check permission and write board #
                param_write_board["subject"]=ts6_board_name
                if ts6_success_get_list_board["attr"]["is_write"]== True :
                    msg("p","  +TS6:Permission write board => Pass")
                    execution_test_link("WAPI-50","p")
                    ts6_success_write_board=post(url_write_board,param_write_board,another_user(new_domain))
                    if notification(ts6_success_write_board)== True :
                        msg("p","  +TS6:Write board at folder 1:1 => Pass")
                        execution_test_link("WAPI-51","p")

                        #check board write #
                        ts6_success_get_list_board1=get(url_get_list_board,"",another_user(new_domain))
                        if notification(ts6_success_get_list_board1)== True :
                            ts6_check_saved_board=check_the_saved_data(url_get_list_board, "",cookie_recipient(new_domain),"subject",ts6_board_name,get,"rows")
                            if ts6_check_saved_board == True :
                                msg("p","    +TS6 :The board has been saved to list board => Pass")
                                execution_test_link("WAPI-53","p")

                                #TS6 view board of TS6 #
                                if ts6_success_get_list_board1["attr"]["is_view"] == True :
                                    msg("p","  +TS6 :Permission wiew board of TS6 => Pass")
                                    execution_test_link("WAPI-55","p")
                                    id_b_2=id_board(ts6_success_get_list_board1,ts6_board_name)
                                    if view_board(board_1[1],id_b_2,head_url_view_board,param_view_board,another_user(new_domain))== True :
                                        msg("p","  +TS6 :Click on board of TS6 => Pass")
                                        execution_test_link("WAPI-80","p")
                                    else :
                                        msg("f","  +TS6 :Click on board of TS6=> Fail")
                                        result.write("<div> [Board]TS6 :Click on board of TS6=> Fail </div>")
                                        execution_test_link("WAPI-80","f")     
                                else :
                                    msg("f","  +TS6 :Permission wiew board of TS6=> Fail")
                                    result.write("<div> [Board]TS6 :Permission wiew board of TS6=> Fail </div>")
                                    execution_test_link("WAPI-55","f")

                            else :
                                msg("f","    +TS6 :The board has been saved to list board => Fail")
                                result.write("<div> [Board]TS6 :The board has been saved to list board => Fail </div>")
                                execution_test_link("WAPI-53","f")

                        # TS1 view board of TS6 #
                        ts1_success_get_list_board_view_ts6=get(url_get_list_board,"",cookie_writer(new_domain))
                        if notification(ts1_success_get_list_board_view_ts6) ==  True :
                            ts1_view_board_ts6=check_the_saved_data(url_get_list_board, "",cookie_writer(new_domain),"subject",ts6_board_name,get,"rows")
                            if ts1_view_board_ts6 == True :
                                msg("p","  +TS1 :View board of TS6 => Pass")
                                execution_test_link("WAPI-55","p")

                                ts1_id_view_ts6=id_board(ts1_success_get_list_board_view_ts6,ts6_board_name)
                                if view_board(board_1[1],ts1_id_view_ts6,head_url_view_board,param_view_board,cookie_writer(new_domain))== True :
                                    msg("p","  +TS1 :Click on board of TS6 => Pass")
                                    execution_test_link("WAPI-80","p")
                                else :
                                    msg("f","  +TS1 :Click on board of TS6 => Fail")
                                    result.write("<div> [Board]TS1 :Click on board of TS6 => Fail </div>")
                                    execution_test_link("WAPI-80","f")
                            else :
                                msg("f","  +TS1 :View board of TS6 => Fail")
                                result.write("<div> [Board]TS1 :View board of TS6 => Fail </div>")
                                execution_test_link("WAPI-55","f") 

                        # TS2 view board of TS6 #
                        ts2_success_get_list_board_view_ts6=get(url_get_list_board,"",cookie_recipient(new_domain))
                        if notification(ts2_success_get_list_board_view_ts6) ==  True :
                            ts2_view_board_ts6=check_the_saved_data(url_get_list_board, "",cookie_recipient(new_domain),"subject",ts6_board_name,get,"rows")
                            if ts2_view_board_ts6 == True :
                                msg("p","  +TS2 :View board of TS6 => Pass")
                                execution_test_link("WAPI-55","p")

                                ts2_id_view_ts6=id_board(ts2_success_get_list_board_view_ts6,ts6_board_name)
                                if view_board(board_1[1],ts2_id_view_ts6,head_url_view_board,param_view_board,cookie_recipient(new_domain))== True :
                                    msg("p","  +TS2 :Click on board of TS6 => Pass")
                                    execution_test_link("WAPI-80","p")
                                else :
                                    msg("f","  +TS2 :Click on board of TS6 => Fail")
                                    result.write("<div> [Board]TS2 :Click on board of TS6 => Fail </div>")
                                    execution_test_link("WAPI-80","f")
                            else :
                                msg("f","  +TS2 :View board of TS6 => Fail")
                                result.write("<div> [Board]TS2 :View board of TS6 => Fail </div>")
                                execution_test_link("WAPI-55","f") 
                        #
                    else : 
                        msg("f","  +TS6:Write board at folder 1:1 => Fail")
                        result.write("<div> [Board]TS6:Write board at folder 1:1 => Fail </div>")
                        execution_test_link("WAPI-51","f")
                else :
                    msg("f","  +TS6:Permission write board => Fail")
                    result.write("<div> [Board]TS6:Permission write board => Fail </div>")
                    execution_test_link("WAPI-50","f")

                #check counter#
            else :
                msg("f","  +TS6:Permission access folder => Fail")
                result.write("<div> [Board]TS6:Permission access folder => Fail </div>")
                execution_test_link("WAPI-79","f")
    
    #TS1 , TS2 add board for delete #
    if notification(success_write_board)== True :
        if check_saved_board == True :
            n=0
            param_write_board["subject"]=ts1_board_name
            while n < 3 :
                post(url_write_board,param_write_board,cookie_writer(new_domain))
                n +=1 
    if notification(ts2_success_write_board)== True :
        if ts2_check_saved_board == True :
            n=0
            param_write_board["subject"]=ts2_board_name
            while n < 3 :
                post(url_write_board,param_write_board,cookie_recipient(new_domain))
                n +=1 
    if notification(ts6_success_write_board)== True :
        if ts6_check_saved_board == True :
            n=0
            param_write_board["subject"]=ts6_board_name
            while n < 3 :
                post(url_write_board,param_write_board,another_user(new_domain))
                n +=1 
    
    # Delete Board #
    
    #TS1 delete board by select board #
    msg("t","[Delete board by select board]")
    data["board"]["delete_board"]["param"]["folder"]=board_1[1]
    ts1_get_list_board_to_delete=get(url_get_list_board,"",cookie_writer(new_domain))
    if notification(ts1_get_list_board_to_delete) == True :
        if ts1_get_list_board_to_delete["attr"]["is_del"]== True :
            msg("p","  +TS1 :Permission delete board by select board => Pass")
            execution_test_link("WAPI-97","p")
            if len(ts1_get_list_board_to_delete["rows"])== 0 :
                msg("p","  +TS1 :There is no board in folder")
            else :
            #TS1 delete board of TS1 #
                board_to_delete=""
                for x in ts1_get_list_board_to_delete["rows"] :
                    if x["name"] == 'TS1' :
                        board_to_delete =x["id"]
                        break 
                if len(board_to_delete)== 0 :
                    msg("p","  +TS1:There is no board of TS1 form list board")
                else :
                    data["board"]["delete_board"]["param"]["menu_head_list"]=ts1_get_list_board_to_delete["attr"]["menu_head_list"]
                    data["board"]["delete_board"]["param"]["ids[0]"]=board_to_delete
                    
                    ts1_success_delete_board_of_ts1= post(url_delete_board,param_delete_board,cookie_writer(new_domain))
                    if notification(ts1_success_delete_board_of_ts1) == True :
                        msg("p","  +TS1:Delete board of TS1 => Pass")
                        execution_test_link("WAPI-81","p")
                        #TS1#
                        time.sleep(10)
                        ts1_success_get_list_board_after_delete=get(url_get_list_board,"",cookie_writer(new_domain))
                        if notification(ts1_success_get_list_board_after_delete)== True :
                            i=0
                            for x in ts1_success_get_list_board_after_delete["rows"]:
                                if x["id"]== board_to_delete :
                                    msg("f","    +TS1:The board of TS1 has been removed from list board => Fail")
                                    result.write("<div> [Board]TS1:The board of TS1 has been removed from list board => Fail </div>")
                                    execution_test_link("WAPI-81","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS1:The board of TS1 has been removed from list board => Pass")
                                execution_test_link("WAPI-81","p")
                        #TS2#
                        ts2_success_get_list_board_after_ts1_delete=get(url_get_list_board,"",cookie_recipient(new_domain))
                        if notification(ts2_success_get_list_board_after_ts1_delete)== True :
                            i=0
                            for x in ts2_success_get_list_board_after_ts1_delete["rows"]:
                                if x["id"]== board_to_delete :
                                    msg("f","    +TS2:The board of TS1 has been removed from list board => Fail")
                                    result.write("<div> [Board]TS2:The board of TS1 has been removed from list board => Fail </div>")
                                    execution_test_link("WAPI-81","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS2:The board of TS1 has been removed from list board => Pass")
                                execution_test_link("WAPI-81","p")
                    else :
                        msg("f","  +TS1:Delete board of TS1 => Fail")
                        result.write("<div> [Board]TS1:Delete board of TS1 => Fail </div>")
                        execution_test_link("WAPI-81","f")

            # TS1 delete board of TS2 #
                board_to_delete_1=""
                for x in ts1_get_list_board_to_delete["rows"] :
                    if x["name"]=="TS2" :
                        board_to_delete_1 =x["id"]
                        break 
                if len(board_to_delete_1)== 0 :
                    msg("p","  +TS1:There is no board of TS2 in folder")
                else :
                    data["board"]["delete_board"]["param"]["menu_head_list"]=ts1_get_list_board_to_delete["attr"]["menu_head_list"]
                    data["board"]["delete_board"]["param"]["ids[0]"]=board_to_delete_1
                    ts1_success_delete_board_of_ts2= post(url_delete_board,param_delete_board,cookie_writer(new_domain))
                    if notification(ts1_success_delete_board_of_ts2) == True :
                        msg("p","  +TS1:Delete board of TS2 => Pass")
                        #TS1#
                        execution_test_link("WAPI-97","p")
                        ts1_success_get_list_board_after_delete_1=get(url_get_list_board,"",cookie_writer(new_domain))
                        if notification(ts1_success_get_list_board_after_delete_1)== True :
                            i=0
                            for x in ts1_success_get_list_board_after_delete_1["rows"]:
                                if x["id"]== board_to_delete_1 :
                                    msg("f","    +TS1:The board of TS2 has been removed from list board => Fail")
                                    result.write("<div> [Board]TS1:The board of TS2 has been removed from list board => Fail </div>")
                                    execution_test_link("WAPI-81","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS1:The board of TS2 has been removed from list board => Pass")
                                execution_test_link("WAPI-81","p")
                        #TS2#
                        ts2_success_get_list_board_after_ts1_delete_1=get(url_get_list_board,"",cookie_recipient(new_domain))
                        if notification(ts2_success_get_list_board_after_ts1_delete_1)== True :
                            i=0
                            for x in ts2_success_get_list_board_after_ts1_delete_1["rows"]:
                                if x["id"]== board_to_delete_1 :
                                    msg("f","    +TS2:The board of TS2 has been removed from list board  => Fail")
                                    result.write("<div> [Board]TS2:The board of TS2 has been removed from list board  => Fail </div>")
                                    execution_test_link("WAPI-81","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS2:The board of TS2 has been removed from list board  => Pass")
                                execution_test_link("WAPI-81","p")
                    else :
                        msg("f","  +TS1:Delete board of TS2 => Fail")
                        result.write("<div> [Board]TS1:Delete board of TS2 => Fail </div>")
                        execution_test_link("WAPI-97","f")
            # TS1 delete board of TS6 #
                board_to_delete_2=""
                for x in ts1_get_list_board_to_delete["rows"] :
                    if x["name"]=="TS6" :
                        board_to_delete_2 =x["id"]
                        break 
                if len(board_to_delete_2)== 0 :
                    msg("p","  +TS1:There is no board of TS6 form list board")
                else :
                    data["board"]["delete_board"]["param"]["menu_head_list"]=ts1_get_list_board_to_delete["attr"]["menu_head_list"]
                    data["board"]["delete_board"]["param"]["ids[0]"]=board_to_delete_2
                    ts1_success_delete_board_of_ts6= post(url_delete_board,param_delete_board,cookie_writer(new_domain))
                    if notification(ts1_success_delete_board_of_ts6) == True :
                        msg("p","  +TS1:Delete board of TS6 => Pass")
                        #TS1#
                        execution_test_link("WAPI-97","p")
                        ts1_success_get_list_board_after_delete_2=get(url_get_list_board,"",cookie_writer(new_domain))
                        if notification(ts1_success_get_list_board_after_delete_2)== True :
                            i=0
                            for x in ts1_success_get_list_board_after_delete_2["rows"]:
                                if x["id"]== board_to_delete_2 :
                                    msg("f","    +TS1:The board of TS6 has been removed from list board => Fail")
                                    result.write("<div> [Board]TS1:The board of TS6 has been removed from list board => Fail </div>")
                                    execution_test_link("WAPI-81","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS1:The board of TS6 has been removed from list board => Pass")
                                execution_test_link("WAPI-81","p")
                        #TS6#
                        ts6_success_get_list_board_after_ts1_delete_2=get(url_get_list_board,"",another_user(new_domain))
                        if notification(ts6_success_get_list_board_after_ts1_delete_2)== True :
                            i=0
                            for x in ts6_success_get_list_board_after_ts1_delete_2["rows"]:
                                if x["id"]== board_to_delete_2 :
                                    msg("f","    +TS6:The board of TS6 has been removed from list board  => Fail")
                                    result.write("<div> [Board]TS6:The board of TS6 has been removed from list board  => Fail </div>")
                                    execution_test_link("WAPI-81","f")
                                    i=i+1 
                                    break
                            if i==0 :
                                msg("p","    +TS6:The board of TS6 has been removed from list board  => Pass")
                                execution_test_link("WAPI-81","p")
                    else :
                        msg("f","  +TS1:Delete board of TS6 => Fail")
                        result.write("<div> [Board]TS1:Delete board of TS6 => Fail </div>")
                        execution_test_link("WAPI-97","f")
        else :
            msg("n","  +TS1 :Permission delete board by select board [Note : This function only applies to domain custom ]")
            execution_test_link("WAPI-97","p")
    
    # TS6 delete board by select board #
    ts6_get_list_board_to_delete_3=get(url_get_list_board,"",another_user(new_domain))
    if notification(ts6_get_list_board_to_delete_3) == True :
        if ts6_get_list_board_to_delete_3["attr"]["is_del"]== False :
            msg("n","  +TS6 :Permission delete board by select board ")
            execution_test_link("WAPI-97","p")
        else :
            msg("f","  +TS6 :Permission delete board by select board => Fail")
            result.write("<div> [Board]TS6 :Permission delete board by select board => Fail </div>")
            execution_test_link("WAPI-97","f")  
    

    # TS1 delete board by view board #
    msg("t","[Delete board by view board]")
    ts1_success_get_list_board_by_view=get(url_get_list_board,"",cookie_writer(new_domain))
    if notification(ts1_success_get_list_board_by_view) == True :
        if not ts1_success_get_list_board_by_view :
            msg("p","  +TS1:There is no board in folder")
        else :
            #TS1 delete board of TS1 #
            board_to_delete_view=""
            for x in ts1_success_get_list_board_by_view["rows"] :
                if x["name"] == 'TS1' :
                    board_to_delete_view =x["id"]
                    break 
            if len(board_to_delete_view)== 0 :
                msg("p","  +TS1:There is no board of TS1 in folder")
            else :
                param_view_board["folder"]=param_delete_board_by_view["folder"]=board_1[1]
                param_view_board["id"]=param_delete_board_by_view["id"]=board_to_delete_view
                url_view_board=api(head_url_view_board,param_view_board)
                ts1_success_view_board_1= get(url_view_board,"", cookie_writer(new_domain))
                if notification(ts1_success_view_board_1)== True :
                    if ts1_success_view_board_1["attr"]["is_del"]== True :
                        msg("p","  +TS1:Permission delete board of TS1 by view board=> Pass")
                        execution_test_link("WAPI-98","p")
                        ts1_success_delete_board_view_of_ts1= post(url_delete_board_by_view,param_delete_board_by_view,cookie_writer(new_domain))
                        if notification(ts1_success_delete_board_view_of_ts1)== True :
                            msg("p","  +TS1:Delete board of TS1 by view board => Pass")
                            execution_test_link("WAPI-99","p")

                            ts1_success_after_delete_by_view_board=get(url_get_list_board,"",cookie_writer(new_domain))
                            if notification(ts1_success_after_delete_by_view_board)== True :
                                i=0
                                if len(ts1_success_after_delete_by_view_board["rows"])==0:
                                    msg("p","    +TS1:The board of TS1 has been removed from list board => Pass")
                                    execution_test_link("WAPI-99","p")
                                else :
                                    for x in ts1_success_after_delete_by_view_board["rows"]:
                                        if x["id"]== board_to_delete_view :
                                            msg("f","    +TS1:The board of TS1 has been removed from list board => Fail")
                                            result.write("<div> [Board]TS1:The board of TS1 has been removed from list board => Fail </div>")
                                            execution_test_link("WAPI-99","f")
                                            i=i+1 
                                            break
                                    if i==0 :
                                        msg("p","    +TS1:The board of TS1 has been removed from list board => Pass")
                                        execution_test_link("WAPI-99","p")
                            # TS2 # 
                            ts2_get_list_board_after_delete_view=get(url_get_list_board,"",cookie_recipient(new_domain))
                            if notification(ts2_get_list_board_after_delete_view)== True :
                                for x in ts2_get_list_board_after_delete_view["rows"] :
                                    if x["id"]== board_to_delete_view :
                                        msg("f","    +TS2:The board of TS1 has been removed from list board => Fail")
                                        result.write("<div> [Board]TS2:The board of TS1 has been removed from list board => Fail </div>")
                                        execution_test_link("WAPI-99","f")
                                        i=i+1 
                                        break
                                if i==0 :
                                    msg("p","    +TS2:The board of TS1 has been removed from list board => Pass")
                                    execution_test_link("WAPI-99","p")

                        else :
                            msg("f","  +TS1 :Delete board of TS1 by view board => Fail")
                            result.write("<div> [Board]TS1 :Delete board of TS1 by view board => Fail </div>")
                            execution_test_link("WAPI-99","f")

                    else :
                        msg("f","  +TS1:Permission delete board of TS1 by view board=> Fail")
                        result.write("<div> [Board]TS1:Permission delete board of TS1 by view board=> Fail </div>")
                        execution_test_link("WAPI-98","f")
            #TS1 delete board of TS2 #
            ts1_board_to_delete_view_ts2=""
            for x in ts1_success_get_list_board_by_view["rows"] :
                if x["name"] == 'TS2' :
                    ts1_board_to_delete_view_ts2 =x["id"]
                    break 
            if len(ts1_board_to_delete_view_ts2)== 0 :
                msg("p","  +TS1:There is no board of TS2 in folder")
            else :
                param_view_board["id"]=param_delete_board_by_view["id"]=ts1_board_to_delete_view_ts2
                url_view_board_1=api(head_url_view_board,param_view_board)
                ts1_success_view_board_2= get(url_view_board_1,"", cookie_writer(new_domain))
                if notification(ts1_success_view_board_2)== True :
                    if ts1_success_view_board_2["attr"]["is_del"]== True :
                        msg("p","  +TS1:Permission delete board of TS2 by view board=> Pass")
                        execution_test_link("WAPI-98","p")
                        ts1_success_delete_board_view_of_ts2= post(url_delete_board_by_view,param_delete_board_by_view,cookie_writer(new_domain))
                        if notification(ts1_success_delete_board_view_of_ts2)== True :
                            msg("p","  +TS1:Delete board of TS2 by view board => Pass")
                            execution_test_link("WAPI-99","p")

                            ts1_success_after_delete_by_view_board_1=get(url_get_list_board,"",cookie_writer(new_domain))
                            if notification(ts1_success_after_delete_by_view_board_1)== True :
                                i=0
                                if len(ts1_success_after_delete_by_view_board_1["rows"])==0 :
                                    msg("p","    +TS1:Board of TS2 has been removed form list board => Pass")
                                    execution_test_link("WAPI-99","p")
                                else :
                                    for x in ts1_success_after_delete_by_view_board_1["rows"]:
                                        if x["id"]== ts1_board_to_delete_view_ts2 :
                                            msg("f","    +TS1:The board of TS2 has been removed from list board => Fail")
                                            result.write("<div> [Board]TS1:The board of TS2 has been removed from list board => Fail </div>")
                                            execution_test_link("WAPI-99","f")
                                            i=i+1 
                                            break
                                    if i==0 :
                                        msg("p","    +TS1:The board of TS2 has been removed from list board => Pass")
                                        execution_test_link("WAPI-99","p")
                            # TS2 # 
                            ts2_get_list_board_after_delete_view_1=get(url_get_list_board,"",cookie_recipient(new_domain))
                            if notification(ts2_get_list_board_after_delete_view_1)== True :
                                for x in ts2_get_list_board_after_delete_view_1["rows"] :
                                    if x["id"]== ts1_board_to_delete_view_ts2 :
                                        msg("f","    +TS2:The board of TS2 has been removed from list board => Fail")
                                        result.write("<div> [Board]TS2:The board of TS2 has been removed from list board => Fail </div>")
                                        execution_test_link("WAPI-99","f")
                                        i=i+1 
                                        break
                                if i==0 :
                                    msg("p","    +TS2:The board of TS2 has been removed from list board => Pass")
                                    execution_test_link("WAPI-99","p")

                        else :
                            msg("f","  +TS1 :Delete board of TS2 by view board => Fail")
                            result.write("<div> [Board]TS1 :Delete board of TS2 by view board => Fail </div>")
                            execution_test_link("WAPI-99","f")

                    else :
                        msg("f","  +TS1:Permission delete board of TS2 by view board=> Fail")
                        result.write("<div> [Board]TS1:Permission delete board of TS2 by view board=> Fail </div>")
                        execution_test_link("WAPI-98","f")
            #TS1 delete board of TS6 #
            ts1_board_to_delete_view_ts6=""
            for x in ts1_success_get_list_board_by_view["rows"] :
                if x["name"] == 'TS6' :
                    ts1_board_to_delete_view_ts6 =x["id"]
                    break 
            if len(ts1_board_to_delete_view_ts6)== 0 :
                msg("p","  +TS1:There is no board of TS6 in folder")
            else :
                param_view_board["id"]=param_delete_board_by_view["id"]=ts1_board_to_delete_view_ts6
                url_view_board_1=api(head_url_view_board,param_view_board)
                ts1_success_view_board_3= get(url_view_board_1,"", cookie_writer(new_domain))
                if notification(ts1_success_view_board_3)== True :
                    if ts1_success_view_board_3["attr"]["is_del"]== True :
                        msg("p","  +TS1:Permission delete board of TS6 by view board=> Pass")
                        execution_test_link("WAPI-98","p")
                        ts1_success_delete_board_view_of_ts6= post(url_delete_board_by_view,param_delete_board_by_view,cookie_writer(new_domain))
                        if notification(ts1_success_delete_board_view_of_ts6)== True :
                            msg("p","  +TS1:Delete board of TS6 by view board => Pass")
                            execution_test_link("WAPI-99","p")

                            ts1_success_after_delete_by_view_board_2=get(url_get_list_board,"",cookie_writer(new_domain))
                            if notification(ts1_success_after_delete_by_view_board_2)== True :
                                i=0
                                if len(ts1_success_after_delete_by_view_board_2["rows"])==0 :
                                    msg("p","    +TS1:Board of TS6 has been removed form list board => Pass")
                                    execution_test_link("WAPI-99","p")
                                else :
                                    for x in ts1_success_after_delete_by_view_board_2["rows"]:
                                        if x["id"]== ts1_board_to_delete_view_ts6 :
                                            msg("f","    +TS1:The board of TS6 has been removed from list board => Fail")
                                            result.write("<div> [Board]TS1:The board of TS6 has been removed from list board => Fail </div>")
                                            execution_test_link("WAPI-99","f")
                                            i=i+1 
                                            break
                                    if i==0 :
                                        msg("p","    +TS1:The board of TS6 has been removed from list board => Pass")
                                        execution_test_link("WAPI-99","p")
                            # TS2 # 
                            ts2_get_list_board_after_delete_view_2=get(url_get_list_board,"",cookie_recipient(new_domain))
                            if notification(ts2_get_list_board_after_delete_view_2)== True :
                                for x in ts2_get_list_board_after_delete_view_2["rows"] :
                                    if x["id"]== ts1_board_to_delete_view_ts6 :
                                        msg("f","    +TS2:The board of TS6 has been removed from list board => Fail")
                                        result.write("<div> [Board]TS2:The board of TS6 has been removed from list board => Fail </div>")
                                        execution_test_link("WAPI-99","f")
                                        i=i+1 
                                        break
                                if i==0 :
                                    msg("p","    +TS2:The board of TS6 has been removed from list board => Pass")
                                    execution_test_link("WAPI-99","p")
                                # TS6 # 
                            ts6_get_list_board_after_delete_view_2=get(url_get_list_board,"",another_user(new_domain))
                            if notification(ts6_get_list_board_after_delete_view_2)== True :
                                for x in ts6_get_list_board_after_delete_view_2["rows"] :
                                    if x["id"]== ts1_board_to_delete_view_ts6 :
                                        msg("f","    +TS6:The board of TS6 has been removed from list board => Fail")
                                        result.write("<div> [Board]TS6:The board of TS6 has been removed from list board => Fail </div>")
                                        execution_test_link("WAPI-99","f")
                                        i=i+1 
                                        break
                                if i==0 :
                                    msg("p","    +TS6:The board of TS6 has been removed from list board => Pass")
                                    execution_test_link("WAPI-99","p")

                        else :
                            msg("f","  +TS1 :Delete board of TS2 by view board => Fail")
                            result.write("<div> [Board]TS1 :Delete board of TS2 by view board => Fail </div>")
                            execution_test_link("WAPI-99","f")

                    else :
                        msg("f","-TS1:Permission delete board of TS6 by view board=> Fail")
                        result.write("<div> [Board]TS1:Permission delete board of TS6 by view board=> Fail </div>")
                        execution_test_link("WAPI-98","f")

    # TS6 delete board by view board #
    ts6_success_get_list_board_by_view=get(url_get_list_board,"",another_user(new_domain))
    if notification(ts6_success_get_list_board_by_view) == True :
        if len(ts6_success_get_list_board_by_view["rows"])==0 :
            msg("p","  +TS6:There is no board in folder")
        else :
            #TS6 delete board of TS6 #
            ts6_board_to_delete_view=""
            for x in ts6_success_get_list_board_by_view["rows"] :
                if x["name"] == 'TS6' :
                    ts6_board_to_delete_view =x["id"]
                    break 
            if len(ts6_board_to_delete_view)== 0 :
                msg("p","  +TS6:There is no board of TS6 in folder")
            else :
                param_view_board["folder"]=param_delete_board_by_view["folder"]=board_1[1]
                param_view_board["id"]=param_delete_board_by_view["id"]=ts6_board_to_delete_view
                url_view_board=api(head_url_view_board,param_view_board)
                ts6_success_view_board_1= get(url_view_board,"", another_user(new_domain))
                if notification(ts6_success_view_board_1)== True :
                    if ts6_success_view_board_1["attr"]["is_del"]== True :
                        msg("p","  +TS6:Permission delete board of TS6 by view board=> Pass")
                        execution_test_link("WAPI-98","p")
                        ts6_success_delete_board_view_of_ts6= post(url_delete_board_by_view,param_delete_board_by_view,another_user(new_domain))
                        if notification(ts6_success_delete_board_view_of_ts6)== True :
                            msg("p","  +TS6:Delete board of TS6 by view board => Pass")
                            execution_test_link("WAPI-99","p")

                            ts6_success_after_delete_by_view_board=get(url_get_list_board,"",another_user(new_domain))
                            if notification(ts6_success_after_delete_by_view_board)== True :
                                i=0
                                if len(ts6_success_after_delete_by_view_board["rows"])==0 :
                                    msg("p","    +TS6:The Board of TS6 has been removed form list board => Pass")
                                    execution_test_link("WAPI-99","p")
                                else :
                                    for x in ts6_success_after_delete_by_view_board["rows"]:
                                        if x["id"]== ts6_board_to_delete_view :
                                            msg("f","    +TS6:The board of TS6 has been removed form list board => Fail")
                                            result.write("<div> [Board]TS6:The board of TS6 has been removed form list board => Fail </div>")
                                            execution_test_link("WAPI-99","f")
                                            i=i+1 
                                            break
                                    if i==0 :
                                        msg("p","    +TS6:The board of TS6 has been removed form list board => Pass")
                                        execution_test_link("WAPI-99","p")
                            # TS1 # 
                            ts1_get_list_board_after_delete_view=get(url_get_list_board,"",cookie_writer(new_domain))
                            if notification(ts1_get_list_board_after_delete_view)== True :
                                for x in ts1_get_list_board_after_delete_view["rows"] :
                                    if x["id"]== ts6_board_to_delete_view :
                                        msg("f","    +TS1:The board of TS6 has been removed form list board => Fail")
                                        result.write("<div> [Board]TS1:The board of TS6 has been removed form list board => Fail </div>")
                                        execution_test_link("WAPI-99","f")
                                        i=i+1 
                                        break
                                if i==0 :
                                    msg("p","    +TS1:The board of TS6 has been removed form list board => Pass")
                                    execution_test_link("WAPI-99","p")
                            # TS2 # 
                            ts2_get_list_board_after_delete_view=get(url_get_list_board,"",cookie_recipient(new_domain))
                            if notification(ts2_get_list_board_after_delete_view)== True :
                                for x in ts2_get_list_board_after_delete_view["rows"] :
                                    if x["id"]== ts6_board_to_delete_view :
                                        msg("f","    +TS2:The board of TS6 has been removed form list board => Fail")
                                        result.write("<div> [Board]TS2:The board of TS6 has been removed form list board => Fail </div>")
                                        execution_test_link("WAPI-99","f")
                                        i=i+1 
                                        break
                                if i==0 :
                                    msg("p","    +TS2:The board of TS6 has been removed form list board => Pass")
                                    execution_test_link("WAPI-99","p")

                        else :
                            msg("f","  +TS6 :Delete board of TS6 by view board => Fail")
                            result.write("<div> [Board]TS6 :Delete board of TS6 by view board => Fail </div>")
                            execution_test_link("WAPI-99","f")

                    else :
                        msg("f","  +TS6:Permission delete board of TS6 by view board=> Fail")
                        result.write("<div> [Board]TS6:Permission delete board of TS6 by view board=> Fail </div>")
                        execution_test_link("WAPI-98","f")
      
def board(new_domain,result):
    head_menu("V.BOARD")

    board_notice_name ="Notice Board"
    board_free_name ="Free Board"
    board_permit_name ="Permit Board"
    board_1_1_name ="1:1 Board"

    company_folder=data["board"]["admin"]["manage_company_folder"]
    old_url_get_folder_list=company_folder["get_list_company_folder"]
    url_get_folder_list=change(new_domain,old_url_get_folder_list,old_domain)

    parent_folder_name=company_folder["param_create_folder"]["folder_name"]='Parent Folder' + ' ' +str(ran)
    old_url_create_folder=company_folder["api_create_folder"]
    url_create_folder=change(new_domain,old_url_create_folder,old_domain)
    param_create_folder=company_folder["param_create_folder"]

    old_url_get_list_folder_left=data["board"]["left_menu"]["api_left"]
    url_get_list_folder_left=change(new_domain,old_url_get_list_folder_left,old_domain)
    param_get_list_folder_left=data["board"]["left_menu"]["param_left"]
    if new_domain=="global3.hanbiro.com":
        url_get_list_folder_left=param["url_get_list_folder_left_gl3"]
    #create parent folder #
    success_create_folder_company=post(url_create_folder,param_create_folder,cookie_writer(new_domain))
    if notification(success_create_folder_company)== True :
        folder_no=success_create_folder_company["rows"]["folder_no"] # id parent folder #
        msg("p","-Create parent folder => Pass")
        result.write("<div> [Board]Test Board </div>")
        msg("p","  +Parent folder name :" + parent_folder_name)
        execution_test_link("WAPI-20","p")
    else :
        msg("f","-Create parent folder => Fail")
        result.write("<div> [Board]Create parent folder => Fail </div>")
        execution_test_link("WAPI-20","f")

    #get list company folder#
    success_get_folder_list=get(url_get_folder_list,"", cookie_writer(new_domain))
    if notification(success_get_folder_list)==True :
        msg("p","  +Get folder list => Pass ")
        execution_test_link("WAPI-67","p")

    else :
        msg("f","  +Get folder list  => Fail ")
        result.write("<div> [Board]Get folder list  => Fail </div>")
        execution_test_link("WAPI-67","f")
        msg("f","    +Error information :" + success_get_folder_list["msg"])

    #check created parent folder #
    if notification(success_create_folder_company)== True and notification(success_get_folder_list)==True:
        if check_the_saved_data(url_get_folder_list," " ,cookie_writer(new_domain),"name",parent_folder_name,get,"rows") == True :
            msg("p","  +The Parent Folder is displayed in folder list => Pass")
            execution_test_link("WAPI-20","p")
        else :
            msg("f","  +The Parent Folder is displayed in folder list => Fail")
            result.write("<div> [Board]The Parent Folder is displayed in folder list => Fail </div>")
            execution_test_link("WAPI-20","f")

    #create subfolder #
    #0 :success create folder , 1:id_folder , 2:saved folder 

    notice=board_create_subfolder(board_notice_name,ran,1,folder_no,new_domain)#a[0]
    ts1_success_get_list_folder_left=get(url_get_list_folder_left,param_get_list_folder_left,cookie_writer(new_domain))
    if notification(ts1_success_get_list_folder_left)== True :
        board_success_folder(notice,"WAPI-41",board_notice_name,"TS1",ts1_success_get_list_folder_left,folder_no,result,new_domain)

    free=board_create_subfolder(board_free_name,ran,2,folder_no,new_domain)
    success_get_list_folder_left1=get(url_get_list_folder_left,param_get_list_folder_left,cookie_writer(new_domain))
    if notification(success_get_list_folder_left1)== True :
        board_success_folder(free,"WAPI-42",board_free_name,"TS1",success_get_list_folder_left1,folder_no,result,new_domain) 

    permit=board_create_subfolder(board_permit_name,ran,3,folder_no,new_domain)
    success_get_list_folder_left2=get(url_get_list_folder_left,param_get_list_folder_left,cookie_writer(new_domain))
    if notification(success_get_list_folder_left2)== True :
        board_success_folder(permit,"WAPI-43",board_permit_name,"TS1",success_get_list_folder_left2,folder_no,result,new_domain)

    board_1=board_create_subfolder(board_1_1_name,ran,4,folder_no,new_domain)
    success_get_list_folder_left3=get(url_get_list_folder_left,param_get_list_folder_left,cookie_writer(new_domain))
    if notification(success_get_list_folder_left3)== True :
        board_success_folder(board_1,"WAPI-44",board_1_1_name,"TS1",success_get_list_folder_left3,folder_no,result,new_domain)
    
    if notice[2] == True :
        board_notice(result,notice,folder_no,new_domain)
    if free[2]== True :
        board_free(result,free,folder_no,new_domain) 
    
    if permit[2] == True :
        board_permit(result,permit,folder_no,new_domain)
   
    if board_1[2]== True :
        board_1_1(result,board_1,folder_no,new_domain)
  


