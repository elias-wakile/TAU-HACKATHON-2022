import searchHeuristic
import requests
import json
import datetime
from dateutil import parser
from datetime import *
from datetime import  timedelta
from monday import MondayClient
import numpy as np
import numpy
apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE2MDMwNDMxMSwidWlkIjoyOTk1NzUwOCwiaWFkIjoiMjAyMi0wNS0xMlQxOTo1MToxNS4wMTJaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTE4NzU5MjIsInJnbiI6InVzZTEifQ.kc5XsEklOx116dzWk_RajsxSgVObTxc3HQn9L4z4USw"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}

monday = MondayClient('eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE2MDMwNDMxMSwidWlkIjoyOTk1NzUwOCwiaWFkIjoiMjAyMi0wNS0xMlQxOTo1MToxNS4wMTJaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTE4NzU5MjIsInJnbiI6InVzZTEifQ.kc5XsEklOx116dzWk_RajsxSgVObTxc3HQn9L4z4USw')
#data = {'query' : query}

# r = requests.post(url=apiUrl, json=data, headers=headers) # make request
# print(r.json())
# query2 = '{boards { name id items { name column_values{title id text } } } }'
# data1 = {'query' : query2}
# r = requests.post(url=apiUrl, json=data1, headers=headers)
# print(r.json())
# query3 = 'mutation{ create_item (board_id:2660130381, item_name:"WHAT IS UP MY FRIENDS!") { id } }'
# data = {'query' : query3}
#
# r1 = requests.post(url=apiUrl, json=data, headers=headers) # make request
# print(r1.json())
task_b_id = 2666261828
calender_b_id = 2666371707
query_task_id = 'query($taskBoardID: Int!) {boards(ids: [$taskBoardID]) {groups { title id  }  } }'
vars1 = {'taskBoardID' : task_b_id}
data_t1_id = {'query' : query_task_id, 'variables' : vars1}
r_task_id = requests.post(url=apiUrl, json=data_t1_id, headers=headers)
query_task = 'query($taskBoardID: Int!) {boards(ids: [$taskBoardID]) { name  items { name id column_values{title text } } }}'
data_t1 = {'query' : query_task, 'variables' : vars1}
r_task = requests.post(url=apiUrl, json=data_t1, headers=headers)
query_task = 'query($calBoardID: Int!) {boards(ids: [$calBoardID]) { name id items { name column_values{title id text } } } }'
vars2 = {'calBoardID' : calender_b_id}
data_t2 = {'query' : query_task, 'variables' : vars2}
r_cal = requests.post(url=apiUrl, json=data_t2, headers=headers)
print((r_task_id.json()))
print(r_task.json())
print(r_cal.json())
items = r_cal.json()['data']['boards'][0].get('items')
groups = r_task_id.json()['data']['boards'][0]['groups']
items_val = r_task.json()['data']['boards'][0]['items']
task_lst=[]
#print(groups)
for i in range(len(groups)):
    curr_dict={}
    curr_dict1={}
    course_items = monday.groups.get_items_by_group(task_b_id, groups[i].get('id'))
    cur_items = course_items['data']['boards'][0]['groups'][0].get('items')
    curr_dict['course name'] = course_items['data']['boards'][0]['groups'][0].get('title')
    curr_dict['course id'] = groups[i].get('id')
    #print(cur_items)
    curr_dict['items'] = cur_items
    # for j in range(len(items_val)):
    #     #print(items_val[j]['column_values'])
    #     for k in range(len(cur_items)):
    #         if items_val[j]['id'] == cur_items[k]['id']:
    #             #for w in range(len(items_val[j]['column_values'])):
    #                 curr_dict1[cur_items[k].get('name')+' '+items_val[j]['column_values'][k]['title']] = items_val[j]['column_values'][k]['text']
    #                 curr_dict['items'].append(curr_dict1)
    task_lst.append(curr_dict)
#print(task_lst)
item_lst =[]
for i in range(len(task_lst)):
    lst = []
    curr_course_name = task_lst[i]['course name']
    lst.append(curr_course_name)
    for k in range(len(task_lst[i]['items'])):
        curr_task_name = task_lst[i]['items'][k]['name']
        curr_task_id =  task_lst[i]['items'][k]['id']
        lst.append(curr_task_name)
        for w in range(len(items_val)):
            if curr_task_id == items_val[w]['id']:
                curr_col_value = items_val[w]['column_values']
                lst.append(curr_col_value)
    item_lst.append(lst)
print(item_lst)
course_list = []
dict123={}
for item in item_lst:

    for i in range(1,len(item)):
        if type(item[i])==list:
            dict123[item[i-1]+'.'+item[0]] = (int(item[i][0]['text']),int(item[i][1]['text'][1]))
            #course_list.append(dict1)  'task1.course 2': ('3', '3') --> (difficulty, time)
print(dict123)
items_lst = []
for i in range(len(items)) :
    cur_item_name = items[i].get('name')
    list_cul_value = items[i].get('column_values')
    if cur_item_name == 'enter you limit hour':
        for j in range(len(list_cul_value)):
            if list_cul_value[j].get('title') == 'finish hour' or list_cul_value[j].get('title')=='start hour':
                dict1={}
                dict1['item name'] = 'limit_of_day'
                str = list_cul_value[j].get('title')
                str2 = list_cul_value[j].get('text')
                dict1[str] = str2
        items_lst.append(dict1)

    elif cur_item_name != 'stop':
        curr_dict={}
        curr_dict['item name'] = cur_item_name

        for w in range(len(list_cul_value)):
            if list_cul_value[w].get('title')=='Date':
                curr_dict[list_cul_value[w].get('title')] = list_cul_value[w].get('text')
            elif list_cul_value[w].get('title')=='start hour':
                curr_dict[list_cul_value[w].get('title')] = list_cul_value[w].get('text')
            elif list_cul_value[w].get('title')=='finish hour':
                curr_dict[list_cul_value[w].get('title')] = list_cul_value[w].get('text')
        items_lst.append(curr_dict)

today = datetime.now().strftime("%Y-%m-%d")
print(items_lst)
fixed_item_lst = []
for item in range(len(items_lst)):
    curr_dict1={}
    curr_dict1['item name'] = items_lst[item].get('item name')
    if items_lst[item].get('item name') !='limit_of_day':
        day_dist = parser.parse(items_lst[item].get('Date')) - parser.parse(today)
        curr_dict1['Dist'] = int(day_dist.days)
        m2 = datetime.strptime(items_lst[item].get('start hour'), '%I:%M %p')
        m1 = datetime.strptime(items_lst[item].get('finish hour'), '%I:%M %p')

        start = m2.strftime("%H:%M:%S")
        finish = m1.strftime("%H:%M:%S")
        start_lst = start.split(':')
        finish_lst = finish.split(':')
        start_float = float(start_lst[0])+float(start_lst[1])/60
        finish_float = float(finish_lst[0]) + float(finish_lst[1])/60
        curr_dict1['start_hour'] = start_float
        curr_dict1['finish_hour'] = finish_float
        fixed_item_lst.append(curr_dict1)


#print(fixed_item_lst)
l = datetime.strptime(items_lst[0].get('finish hour'), '%I:%M %p')
lim = l.strftime("%H:%M:%S").split(':')
limitf = float(lim[0])+float(lim[1])/60
limits = 8.0
time_in_day = (limitf-limits)
newlist = sorted(fixed_item_lst, key=lambda d: d['Dist'])
#print(newlist)
array= numpy.zeros((int(time_in_day),7))
for i in range(int(time_in_day)):
    for j in range(7):
        for k in range(len(fixed_item_lst)):
            inti = newlist[k]['Dist']
            if int(inti) == j+1:
                if (i >= int(newlist[k]['start_hour'])-int(limits)) and (i <= int(newlist[k]['finish_hour'])-int(limits)):
                    array[i][j] = 1

#print(array)
time_count = 0
for task in dict123:
    time_count= time_count + int(dict123[task][1])
avg_time = time_count/len(dict123)
print (avg_time)
array_aranged1 = array
print(dict123)
counter9=0
dict1234={}
for i in dict123:
    if counter9%5==0 :
        dict1234[i]=dict123[i]
    counter9+=1
print(dict1234)
array_aranged = searchHeuristic.depth_first_search(searchHeuristic.SearchProblem(array_aranged1, dict1234)).schedule
# for task in dict123:
#     counter = 0
#     for row in range(int(time_in_day)):
#         row_count = 0
#         one_count = 0
#         for col in range(7):
#             if row_count<=int(avg_time)+1:
#                 if array_aranged[row][col]==0:
#                     row_count = row_count + 1
#                     if int(counter)!=int(dict123[task][1]):
#                         num = task.split('.')
#                         task_num = float(num[0][-1]+'.'+num[1][-1])
#                         array_aranged[row][col] = task_num
#                         counter = counter + 1
#
#                 else:
#                     one_count+=1
#             else:
#                 break
print(array_aranged)

query_task1 = 'query($calBoardID: Int!) {boards(ids: [$calBoardID]) {groups { title id  }  } }'

data_t3 = {'query' : query_task1, 'variables' : vars2}
r_cal1 = requests.post(url=apiUrl, json=data_t3, headers=headers)
print(r_cal1.json())
#cal_group_id = r_cal1.json()['data']['boards'][0]['groups'][1]['id']
cal_group_id = 'topics'
item_val_dict = {}
for col in range(7):
    for row in range(int(time_in_day)):
        if array_aranged[row][col]!=0 and array_aranged[row][col]!=1.0:
            task_num = (int(array_aranged[row][col]))
            course_num = (int(((array_aranged[row][col]+0.01)-int(array_aranged[row][col]))*10))
           # print(course_num)
            namet = 'task %d'%task_num +' course %d'%course_num
            if namet not in item_val_dict.keys():
                item_val_dict[namet] = [(row,col)]
            else:
                item_val_dict[namet].append((row,col))
print(item_val_dict)
send_dict={}
lstd =[]
for item in item_val_dict:
    curr_day = 0
    for i in range(len(item_val_dict[item])):
        curr_dict1 ={}
        if i==0 and len(item_val_dict[item])!=1:
            curr_day = item_val_dict[item][i][1]
            start = item_val_dict[item][i][0]
        elif curr_day==item_val_dict[item][i][1]:
            continue
        elif curr_day!=item_val_dict[item][i][1] and i!=len(item_val_dict[item]):
            curr_dict1['name']= item
            curr_dict1['Date'] = curr_day
            curr_dict1['start_hour']=start
            curr_dict1['finish hour']=item_val_dict[item][i-1][0]
            lstd.append(curr_dict1)
            curr_day = item_val_dict[item][i][1]
        elif len(item_val_dict[item])==1:
            curr_dict1['name'] = item
            curr_dict1['Date'] = curr_day
            curr_dict1['start_hour'] = item_val_dict[item][i][0]
            curr_dict1['finish hour'] = item_val_dict[item][i][0]
            lstd.append(curr_dict1)
        elif i==len(item_val_dict[item]):
            if item_val_dict[item][i]!=item_val_dict[i-1]:
                curr_dict1['name'] = item
                curr_dict1['start_hour'] = item_val_dict[i][0]
                curr_dict1['Date'] = curr_day
                curr_dict1['finish hour'] = item_val_dict[i][0]
                lstd.append(curr_dict1)
            else:
                curr_dict1['name'] = item
                curr_dict1['start_hour'] = start
                curr_dict1['Date'] = curr_day
                curr_dict1['finish hour'] = item_val_dict[i][0]
                lstd.append(curr_dict1)

final_list =[]
for item in item_val_dict:
    for i in range(7):
        day_dic = {}
        list = item_val_dict[item]
        arr = []
        for j in list:
            if j[1] == i:
                arr.append(j[0])
        if arr != []:
            day_dic["name"]=item
            day_dic["Date"] = i
            day_dic["start_hour"]=np.array(arr).min()
            day_dic["final_hour"]=np.array(arr).max()
            final_list.append(day_dic)
print(final_list)
        # if len(item_val_dict[item])>1:
        #     if item_val_dict[item][i][1]==item_val_dict[item][i+1][1]:
        #         curr_day =  item_val_dict[item][i][1]+1
        #         start = item_val_dict[item][i][0]
        #     elif curr_day != item_val_dict[item][i-1][1]+1 and i!=len(item_val_dict[item]):
        #         finish = item_val_dict[item][i-1][0]
        #         curr_dict1[item]= [curr_day,start,finish]
        #         lstd.append(curr_dict1)
   #monday.items.create_item(calender_b_id, cal_group_id, item_name, column_values=None, create_labels_if_missing=False)
send_list=[]
def hour24_to_ampm(hour):
    ampm = "AM" if hour < 12 else "PM"
    new_hour = (hour - 1) % 12 + 1
    r ='%s'% new_hour
    if new_hour<10:
        return "0"+r+":00 "+ampm
    return r+":00 "+ampm
for item in final_list:
    curr_dict={}
    start_hour_int = int(limits+item['start_hour'])
    final_hour_int = int(limits+item['final_hour'])+1
    curr_dict['name'] = item['name']
    curr_dict['column_values'] = []
    #if start_hour_int<10:
    start_hour = hour24_to_ampm( start_hour_int)
    # else:
    #     start_hour = '%d:00'%start_hour_int
    finish_hour = hour24_to_ampm(final_hour_int)
    end_date = datetime.now() + timedelta(days=int(item['Date']+1))
    curr_dict['column_values'].append({'title': 'Date', 'text': end_date.strftime("%Y-%m-%d")})
    curr_dict['column_values'].append({'title': 'start hour', 'text': start_hour})
    curr_dict['column_values'].append({'title': 'finish hour', 'text': finish_hour})

    send_list.append(curr_dict)
print(send_list)
for item in (send_list):
    name = item['name']
   # print('in')
    #monday.items.create_item(calender_b_id, cal_group_id, item['name'], column_values=item['column_values'], create_labels_if_missing=True)
    curr_qury = 'mutation($name: String!,$col: JSON!) {create_item (board_id: 2666371707, group_id: topics, item_name: $name,column_values:$col) {id}}'
    date1 = item['column_values'][0]['text']
    start1 = item['column_values'][1]['text']
    finish1 = item['column_values'][2]['text']
   # print(start1)
    vars_send = {'name':name,'col':json.dumps({'date4':date1,'start_hour':start1,'finish_hour':finish1})}
    datase = {'query': curr_qury, 'variables': vars_send}

    r_send = requests.post(url=apiUrl, json=datase, headers=headers)
    print(r_send.json())
#
