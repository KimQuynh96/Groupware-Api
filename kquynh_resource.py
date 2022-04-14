import json
from datetime import date
from os import pardir
from kquynh_function_gw import data,account_one,head_menu,account_two,account_thr,userno,date_time,post,get,notification,msg,delete,create_url
from kquynh_param_gw import resource_menu
param_msg=data["resource_msg"]
vehicle_name="Resource Vehicle " + date_time
room_name="Room " + date_time

def check_resource_category(response_list,title,system):
    result={"result":False ,"system":True}
    # Category List Has No Category > The Created Category Not In The List #
    if len(response_list["rows"]) == 0 :
        result["result"] = False

    # Category List Has Category > Check Created Category Is In The List #
    else :
        for category in response_list["rows"] :
            if category["name"] == title and category["ec_is_system"] == system :
                result["result"] = True
                break
            # Check Type of Resource #
            if category["name"] == title and category["ec_is_system"] != system :
                result["result"] = True
                result["system"] = False
                break
    return result

def result_add(response_add,check_add,list_msg):
    if notification(response_add) == True :
        check_add = True
        msg("p",list_msg["msg_pass"])
    else :
        msg("f",list_msg["msg_fail"])
    return check_add

def result_displayed(result,list_msg):
    
    # Category List Has Category #
    if result["result"] == True :
        if result["system"] == True :
            msg("p",list_msg["pass_displayed"])
        else :
            msg("f",list_msg["fail_type"])  
    # Category List Has No Category #
    else:
        msg("f",list_msg["fail_displayed"])

def update_param_to_add_resource(response_list_type,type_resource):
    # Note info_resource["result"] to check Is the resource type on the list? #
    param_add_resource=data["resource"]["info_resource"]
    if len(response_list_type["rows"]) == 0 :
        param_add_resource["result"] = False
    else :
        for type in response_list_type["rows"]:
            if type["ec_is_system"] == type_resource :
                param_add_resource["result"] = True 
                param_add_resource["ec_idx"] = type["id"]
                param_add_resource["category_parent_name"] = type["name"]
                param_add_resource["ec_is_system"] = type["ec_is_system"]
                break
        if type_resource == "C" :
            param_add_resource["et_name"] = room_name
            param_add_resource["is_conference"] = True
        elif type_resource == "V" :
            param_add_resource["is_verhicle"] = True 
            param_add_resource["et_pre_time"] = 0
            param_add_resource["et_return"] = True
            param_add_resource["ec_car_num"] = 123
            param_add_resource["ec_car_vin"] = 50
            param_add_resource["ec_last_value"] = 0
            param_add_resource["et_name"] = vehicle_name
            param_add_resource["is_verhicle"] = True
    return param_add_resource


    
def check_add_resource(response_add_resource,list_msg,check_add):
    if notification(response_add_resource) == True :
        check_add = True
        msg("p",list_msg["pass_add_resource"])
    else:
        msg("p",list_msg["fail_add_resource"])
    return check_add

def result_displayed_resource(response_list,list_msg,resource_name):
    if len(response_list["rows"]) == 0 :
        msg("f",list_msg["fail_displayed"])
        return False
    else:
        for category in response_list["rows"]  :
            if "children" in category :
                if len(category["children"]) != 0 :
                    for resource in category["children"] :
                        if resource["title"] == resource_name :
                            msg("p",list_msg["pass_displayed"])
                            return True
    msg("p",list_msg["fail_displayed"])
    return False



def add_resource(param,new_domain,user_no):
    # URL ADD TYPE #
    ur_add_type = param["url_add_type"]
    # URL ADD RESOURCE #
    ur_add_resource = param["url_add_resource"]

    # GET CATEGORY LIST #
    ur_type_list = param["url_type_list"]
    response_type_list_cm = get(ur_type_list,"",account_one(new_domain))
    if notification(response_type_list_cm) == True :
        msg("p",param_msg["pass_type_list"])
    else :
        msg("f",param_msg["fail_type_list"])

    
    # TYPE IS CONFERENCE #
    check_add_type = False
    pr_add_room = param["pr_add_room"]
    response_add_type = post(ur_add_type,pr_add_room,account_one(new_domain))
    list_msg_type = param["list_msg_type"]
    check_add_type = result_add(response_add_type,check_add_type,list_msg_type)
    # Check Added Type Is Conference #
    if check_add_type == True :
        if notification(response_type_list_cm) == True :
            response_type_list = get(ur_type_list,"",account_one(new_domain))
            result_displayed_room = check_resource_category(response_type_list,pr_add_room["name"],"C")
            list_msg_displayed_room = param["list_msg_displayed_room"]
            result_displayed(result_displayed_room,list_msg_displayed_room)
    

    # TYPE IS VEHICLE # 
    check_add_vehicle = False
    pr_add_vehicle = param["pr_add_vehicle"]
    response_add_vehicle = post(ur_add_type,pr_add_vehicle,account_one(new_domain))
    list_msg_vehicle = param["list_msg_vehicle"]
    check_add_vehicle = result_add(response_add_vehicle,check_add_vehicle,list_msg_vehicle)
    # Check Added Type is Vehicle #
    if check_add_vehicle == True :
        if notification(response_type_list_cm) == True :
            response_type_list = get(ur_type_list,"",account_one(new_domain))
            result_displayed_vehicle = check_resource_category(response_type_list,pr_add_vehicle["name"],"V")
            list_msg_displayed_vehicle = param["list_msg_displayed_vehicle"]
            result_displayed(result_displayed_vehicle,list_msg_displayed_vehicle)


    # TYPE IS NORMAL # 
    check_add_normal = False
    pr_add_normal = param["pr_add_normal"]
    response_add_normal = post(ur_add_type,pr_add_normal,account_one(new_domain))
    list_msg_normal = param["list_msg_normal"]
    check_add_normal = result_add(response_add_normal,check_add_normal,list_msg_normal)
    # Check Added Type is Normal #
    if check_add_normal == True :
        if notification(response_type_list_cm) == True :
            response_type_list = get(ur_type_list,"",account_one(new_domain))
            result_displayed_normal = check_resource_category(response_type_list,pr_add_normal["name"],"N")
            list_msg_displayed_normal = param["list_msg_displayed_normal"]
            result_displayed(result_displayed_normal,list_msg_displayed_normal)
    

    # ADD RESOURCE # 
    if notification(response_type_list_cm) == True :
        # Add resource of type Conference #
        check_resource_n = False
        response_type_list = get(ur_type_list,"",account_one(new_domain))
        param_add_resource = update_param_to_add_resource(response_type_list,"C")
        if param_add_resource["result"] == True :
            pr_add_resource = param["pr_add_resource"]
            pr_add_resource.update(param_add_resource)
            response_add_resource= post(ur_add_resource,pr_add_resource,account_one(new_domain))
            list_msg_resource_n = param["list_msg_resource_n"]
            check_resource_n = check_add_resource(response_add_resource,list_msg_resource_n,check_resource_n)
        else:
            msg("p",param_msg["pass_no_type"])
        # Check added resource #
        if check_resource_n == True :
            response_category_list = get(ur_type_list,"",account_one(new_domain))
            list_msg_room =  param["list_msg_room"]
            result_displayed_resource(response_category_list,list_msg_room,room_name)
        
        # Add resource of type Vehicle #
        check_resource_v = False
        response_type_list = get(ur_type_list,"",account_one(new_domain))
        param_add_resource = update_param_to_add_resource(response_type_list,"V")
        if param_add_resource["result"] == True :
            pr_add_resource = param["pr_add_resource"]
            pr_add_resource.update(param_add_resource)
            response_add_resource= post(ur_add_resource,pr_add_resource,account_one(new_domain))
            list_msg_resource_v = param["list_msg_resource_v"]
            check_resource_v = check_add_resource(response_add_resource,list_msg_resource_v,check_resource_v)
        else:
            msg("p",param_msg["pass_no_type_v"])
        # Check added resource #
        if check_resource_v == True :
            response_category_list = get(ur_type_list,"",account_one(new_domain))
            list_msg_vehicle =  param["list_msg_vehicle"]
            result_displayed_resource(response_category_list,list_msg_vehicle,vehicle_name)
    
    # ADD RESERVE RESOURCE #
    url_left_list= param["url_left_list"]
    response_left_list = get(url_left_list ,"",account_one(new_domain))
    if notification(response_left_list) == True :
        category_list = response_left_list["rows"]["0"]["children"] 
        if len(category_list)  == 0 :
            msg("p",param_msg["pass_no_reserve"])
       




    






def resource(new_domain):
    head_menu("MENU : RESOURCE")
    param=json.loads(resource_menu(new_domain))
    user_no=userno(new_domain)
    add_resource(param,new_domain,user_no)
    
   

    




