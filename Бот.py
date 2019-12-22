# -*- coding: utf-8 -*-
import selenium
import vk_api
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

def zeromas(group,day):
    global globalday
    try:
        globalday[group][day] = [['','','','','','','']]
    except Exception as e:
        print('zeromas err:',e,globalday)
    
def groupzeromas(group):
    global globalday
    globalday[group] = [[['','','','','','','']],
                  [['','','','','','','']],
                  [['','','','','','','']],
                  [['','','','','','','']],
                  [['','','','','','','']],
                  [['','','','','','','']]]
def fullzeromas(): 
    global globaday
    globalday = [[[['','','','','','','']],
                  [['','','','','','','']],
                  [['','','','','','','']],
                  [['','','','','','','']],
                  [['','','','','','','']],
                  [['','','','','','','']]]]

globalday = [[[['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']]]]
              
globaldayold = [[[['','','','','','','']],
                [['','','','','','','']],
                [['','','','','','','']],
                [['','','','','','','']],
                [['','','','','','','']],
                [['','','','','','','']]]]
#empty = globalday

#Структура массива - [индекс группы][индекс дня недели][индекс пары][индекс элемента пары]
#Индексы элементов пары - Пара:0 Время:1 Предмет:2 Подгруппа:3 Группа:4 Преподователь:5 Кабинет:6

#/html/body/div/div[2]/table/tbody/tr[1]/th Первый день недели 
#/html/body/div/div[2]/table/tbody/tr[2]/th[1] Первое название заголовка
#/html/body/div/div[2]/table/tbody/tr[3]/td[1] Первый элемент таблицы
#/html/body/div/div[2]/table/tbody/tr[6]/th Второй день недели
#/html/body/div/div[2]/table/tbody/tr[7]/th[1] Второе название заголовка 

browser = webdriver.Chrome()
browser.get('https://timetable.ptpit.ru/getTimeTable#')
vk = vk_api.VkApi(token=os.getenv("BOT_TOKEN"))

names = [['holeur']]
groups = ['17СПИ3']
date = ''
olddate = ''
sendingerrflag = 1
kastilflag = 1
kastilcheck = 0

def globalgroupappend(): #Добавление место под группу в массиве.
    global globalday
    globalday.append([[['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']]])
    globaldayold.append([[['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']],
              [['','','','','','','']]])
    
def gettablinfile(filename): #запоминание массивов в фаил. Пока не используется.
    try:
        file = open(filename,'w')
        numline = 0
        numelem = 0
        for num in range(1,7):
            for line in day('day'+str(num)+'old'):
                for elem in line:
                    #print('Попытка загрузить элемент',num,numline,numelem)
                    file.write(day('day'+str(num)+'old')[numline][numelem]+'\n')
                    numelem += 1
                numline += 1
                numelem = 0
            numline = 0
        file.close()
        print('Сохраненые массивы скопированны в фаил')
    except Exception as e:
        print('gettablinfile err:',e)
        
def loadfile(filename): #Загрзка dayold в фаил. Пока не используется.
    global globaldayold,globalday
    try:
        file = open(filename,'r')
        numline = 0
        numelem = 0
        num = 1
        for line in file:
            globalday[0][num-1][numline][numelem] = line[0:len(line)-1]
            numelem += 1
            if numelem >= 7:
                numelem = 0
                numline += 1
            if numline >= 7:
                numelem = 0
                numline = 0
                num += 1
            if num > 6:
                break
        file.close()
        print('Массивы загружены из файла')
    except Exception as e:
        print('loadfile err:',e)
        
def save(group): #Перевод основных массивов в память.
    global globaldayold,globalday
    try:
        for num in range(6): #day1old = day1...
            try:
                globaldayold[group][num] = globalday[group][num]
            except IndexError:
                globaldayold[group].append([])
                globaldayold[group][num] = globalday[group][num]
        #print(globaldayold)
        print('Массивы сохранены')
        #gettablinfile('bd.txt')
    except Exception as e:
        print('save err:',e,globalday,globaldayold)

def update(group): #Открытие страницы определенной группы.
    global groups
    browser.refresh()
    time.sleep(4)
    try:
        Select(browser.find_element_by_xpath('/html/body/div[1]/div[1]/form/div[2]/select[1]')).select_by_visible_text(groups[group])
        browser.find_element_by_xpath('//*[@id="btnGetTimetable"]').click()
    except:
        print('Опять ошибка с поиском элемента')
        update(group)
    
def day(nameday): #Выбор массива по названию. Не используется. Лежит в память о старом алгоритме.
    if nameday == 'day1':
        return day1
    elif nameday == 'day2':
        return day2
    elif nameday == 'day3':
        return day3
    elif nameday == 'day4':
        return day4
    elif nameday == 'day5':
        return day5
    elif nameday == 'day6':
        return day6
    elif nameday == 'day1old':
        return day1old
    elif nameday == 'day2old':
        return day2old
    elif nameday == 'day3old':
        return day3old
    elif nameday == 'day4old':
        return day4old
    elif nameday == 'day5old':
        return day5old
    elif nameday == 'day6old':
        return day6old

def zap(groupnum,nday): #Заполнение выбранного дня в массиве.
    global line,browser,globalday
    try:
        flag1 = 1
        line2 = 2
        elem = 1
        while flag1:
            try:
                globalday[groupnum][nday][line2-2][elem-1] = browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line+line2)+']/td['+str(elem)+']').text
                #print(globalday[groupnum][nday][line2-2][elem-1])
                elem += 1
                if elem > 7:
                    elem = 1
                    line2 += 1
                    globalday[groupnum][nday].append(['','','','','','',''])
            except selenium.common.exceptions.NoSuchElementException:
                flag1 = 0
                del globalday[groupnum][nday][-1]
    except Exception as e:
        print("zap err:",e)

def checkdate(pos):
    global date,olddate
    if pos == 1:
        date = browser.find_element_by_xpath("/html/body/div/div[1]/form/div[1]/select").text
    elif pos == 2:
        olddate = date
        
def taketabl(groupnum): #Заполнение массива по дням недели.
    global line,globalday
    for line in range(1,48):
        try:
            if 'Понедельник' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Понедельник')
                zeromas(groupnum,0)
                zap(groupnum,0)
            elif 'Вторник' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Вторник')
                zeromas(groupnum,1)
                zap(groupnum,1)
            elif 'Среда' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Среда')
                zeromas(groupnum,2)
                zap(groupnum,2)
            elif 'Четверг' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Четверг')
                zeromas(groupnum,3)
                zap(groupnum,3)
            elif 'Пятница' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Пятница')
                zeromas(groupnum,4)
                zap(groupnum,4)
            elif 'Суббота' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Суббота')
                zeromas(groupnum,5)
                zap(groupnum,5)
        except selenium.common.exceptions.NoSuchElementException:
            print('Не найдена строка под номером',line)
            #print()
        except Exception as e:
            print('taketabl err:',e) 
    print(globalday) #Вывод в консоль собранных массивов

def writetxtall(group,numday): #Алгоритм создания сообщения.
    global globalday,globaldayold,groups,txtall,flag1,groups
    try:
        txt = ''
        txtall = ''
        numelem = 0
        numline = 0
        for line in globalday[group][numday-1]:
            for elem in line:
                if numelem == 0:
                    try:
                        if globalday[group][numday-1][numline][0] != globaldayold[group][numday-1][numline][0]:
                            txt = '*Пара> ' + elem + '\n'
                        else:
                            txt = 'Пара> ' + elem + '\n'
                    except IndexError:
                        if globalday[group][numday-1][numline][0] != '':
                            txt = '*Пара> ' + elem + '\n'
                        else:
                            txt = 'Пара> ' + elem + '\n'
                elif numelem == 1:
                    try:
                        if globalday[group][numday-1][numline][1] != globaldayold[group][numday-1][numline][1]:
                            txt = '*Время> ' + elem + '\n'
                        else:
                            txt = 'Время> ' + elem + '\n'
                    except IndexError:
                        if globalday[group][numday-1][numline][1] != '':
                            txt = '*Время> ' + elem + '\n'
                        else:
                            txt = 'Время> ' + elem + '\n'
                elif numelem == 2:
                    try:
                        if globalday[group][numday-1][numline][2] != globaldayold[group][numday-1][numline][2]:
                            txt = '*Предмет> ' + elem + '\n'
                        else:
                            txt = 'Предмет> ' + elem + '\n'
                    except IndexError:
                        if globalday[group][numday-1][numline][2] != '':
                            txt = '*Предмет> ' + elem + '\n'
                        else:
                            txt = 'Предмет> ' + elem + '\n'
                elif numelem == 3:
                    try:
                        if globalday[group][numday-1][numline][3] != globaldayold[group][numday-1][numline][3]:
                            txt = '*Подгруппа> ' + elem + '\n'
                        else:
                            txt = 'Подгруппа> ' + elem + '\n'
                    except IndexError:
                        if globalday[group][numday-1][numline][3] != '':
                            txt = '*Подгруппа> ' + elem + '\n'
                        else:
                            txt = 'Подгруппа> ' + elem + '\n'
                elif numelem == 4:
                    # try:
                        # if globalday[group][numday-1][numline][4] != globaldayold[group][numday-1][numline][4]:
                            # txt = '*Группа> ' + elem + '\n'
                        # else:
                            # txt = 'Группа> ' + elem + '\n'
                    # except IndexError:
                        # if globalday[group][numday-1][numline][4] != '':
                            # txt = '*Группа> ' + elem + '\n'
                        # else:
                            # txt = 'Группа> ' + elem + '\n'
                    if elem == '':
                        print('Пропускаем пустоту')
                    else:
                        print(elem,'пропускаем')
                elif numelem == 5:
                    try:
                        if globalday[group][numday-1][numline][5] != globaldayold[group][numday-1][numline][5]:
                            txt = '*Преподаватель> ' + elem + '\n'
                        else:
                            txt = 'Преподаватель> ' + elem + '\n'
                    except IndexError:
                        if globalday[group][numday-1][numline][5] != '':
                            txt = '*Преподаватель> ' + elem + '\n'
                        else:
                            txt = 'Преподаватель> ' + elem + '\n'
                elif numelem == 6:
                    try:
                        if globalday[group][numday-1][numline][6] != globaldayold[group][numday-1][numline][6]:
                            txt = '*Кабинет> ' + elem + '\n'
                        else:
                            txt = 'Кабинет> ' + elem + '\n'
                    except IndexError:
                        if globalday[group][numday-1][numline][6] != '':
                            txt = '*Кабинет> ' + elem + '\n'
                        else:
                            txt = 'Кабинет> ' + elem + '\n'
                else:
                    print('Что-то пропущено...')
                txtall += txt
                txt = ''
                numelem += 1
            numline += 1
            numelem = 0
            txtall += '---------------------------\n'
        if numday == 1:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nПонедельник изменили у группы '+str(groups[group])+'\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        elif numday == 2:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nВторник изменили у группы '+str(groups[group])+'\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        elif numday == 3:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nСреду изменили у группы '+str(groups[group])+'\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        elif numday == 4:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nЧетверг изменили у группы '+str(groups[group])+'\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        elif numday == 5:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nПятницу изменили у группы '+str(groups[group])+'\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        elif numday == 6:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nСубботу изменили у группы '+str(groups[group])+'\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        if flag1:
            txtall = '{Первый цикл}\n' + txtall
    except Exception as e:
        print('writetextall err:',e)
    
def filewrite(text): #Запись полученного текста в фаил. Пока не используется.
    file = open('logs.txt','a')
    file.write(text)
    file.close()
    
def sendmes(group,text): #Отправление сообщения нескольким людям.
    global names,sendingerrflag
    for elem in names[group]:
        try:
            if isinstance(elem,int):
                vk.method("messages.send", {"user_id": elem, "message":text, "random_id": random.randint(100, 2147483647), "group_id":"181204528"})
            else:
                vk.method("messages.send", {"domain": elem, "message":text, "random_id": random.randint(100, 2147483647), "group_id":"181204528"})
        except Exception as e:
            print('sendmes',elem,'err:',e)
            if sendingerrflag:
                vk.method("messages.send", {"domain": 'holeur', "message":'err:'+str(e)+str(elem), "random_id": random.randint(100, 2147483647)})

def eq(group): #Сравнение таблиц.
    global sendingerrflag,globaldayold,globalday,flag1,txtall,groups,date,olddate
    try:
        if date == olddate:
            if globalday[group][0] != globaldayold[group][0]:
                print('Понедельник изменили')
                writetxtall(group,1)
                if flag1 == 0:
                    sendmes(group,txtall)
                #filewrite(txtall)
            if globalday[group][1] != globaldayold[group][1]:
                print('Вторник изменили')
                writetxtall(group,2)
                if flag1 == 0:
                    sendmes(group,txtall)
                #filewrite(txtall)
            if globalday[group][2] != globaldayold[group][2]:
                print('Среду изменили')
                writetxtall(group,3)
                if flag1 == 0:
                    sendmes(group,txtall)
                #filewrite(txtall)
            if globalday[group][3] != globaldayold[group][3]:
                print('Четверг изменили')
                writetxtall(group,4)
                if flag1 == 0:
                    sendmes(group,txtall)
                #filewrite(txtall)
            if globalday[group][4] != globaldayold[group][4]:
                print('Пятницу изменили')
                writetxtall(group,5)
                if flag1 == 0:
                    sendmes(group,txtall)
                #filewrite(txtall)
            if globalday[group][5] != globaldayold[group][5]:
                print('Субботу изменили')
                writetxtall(group,6)
                if flag1 == 0:
                    sendmes(group,txtall)
                #filewrite(txtall)
        else:
            print('Новая неделя')
            if flag1 == 0:
                groupzeromas(group)
            if globalday[group][0] != globaldayold[group][0]:
                print('Понедельник изменили')
                writetxtall(group,1)
                if flag1 == 0:
                    sendmes(group,txtall)
                #filewrite(txtall)
    except Exception as e:
        print('eq err:',e)
        if sendingerrflag:
            vk.method("messages.send", {"domain": 'holeur', "message":'eq err:'+str(e), "random_id": random.randint(100, 2147483647)})
        
def checkupt(): #Проверка на случай не загрузки сайта.
    global checkflag,tabledate
    try:
        tabledate = browser.find_element_by_xpath('/html/body/div/div[1]/form/div[1]/select').text
        checkflag = 1
    except:
        checkflag = 0

def getnames(): #Использовал личку сообщества как бд с именами участников. XD
    try:    
        global names,groups
        oldnames = names
        names = [['holeur']]
        messages = vk.method("messages.search",{"q":"+add","peer_id":"125524519","group_id":"181204528"})
        print(messages["count"]+1)
        for mes in messages["items"]:
            if '+add' == mes["text"][:4]: #+add:4563456:17СПИ3
                name = mes["text"][5:mes["text"].rfind(':'):]
                try:
                    namegroup = mes["text"][mes["text"].rfind(':')+1:]
                    if namegroup == '':
                        namegroup = '17СПИ3'
                    elif namegroup not in groups:
                        print('Группы не существует')
                except Exception as e:
                    print('getnames namegroup err:',e)
                try:
                    if int(name) not in names[groups.index(namegroup)]:
                        names[groups.index(namegroup)].append(int(name))
                    if int(name) not in oldnames:
                        print('Добавлен в массив имен',name,'в группу',namegroup)
                except ValueError:
                    if name not in names[groups.index(namegroup)]:
                        names[groups.index(namegroup)].append(name)
                    if name not in oldnames:
                        print('Добавлен в массив имен',name,'в группу',namegroup)
        print(names)
    except Exception as e:
        print('getnames err:',e)

def getgroups(): #Скопированный алгоритм getnames. Только с группами.
    global groups,names
    oldgroups = groups
    groups = ['17СПИ3']
    messages = vk.method("messages.search",{"q":"+addgr","peer_id":"125524519","group_id":"181204528"})
    print(messages["count"]+1)
    for mes in messages["items"]:
        if '+addgr' == mes["text"][:6]:
            group = mes["text"][7:]
            if group not in groups:
                groups.append(group)
            if group not in oldgroups:
                print('Добавлен в массив групп',group)
                names.append(['holeur'])
                globalgroupappend()
                flag1 = 1
    print(groups)
    
def delerr(): #Функция удаления всех ошибок.
    ids = []
    messages = vk.method("messages.search",{"q":"err:","peer_id":"125524519","group_id":"181204528","count":"99"})
    for message in messages["items"]:
        ids.append(message["id"])
    for id in ids:
        try:
            vk.method("messages.delete",{"message_ids":id,"delete_for_all":"1","group_id":"181204528"})
        except Exception as e:
            print("Error",id,"can not be deleted:",e)
            vk.method("messages.delete",{"message_ids":id,"delete_for_all":"0","group_id":"181204528"})
            
def checklist(): #Список участников.
    global names
    txtall = ''
    for num in range(len(names)):
        txtall += '------------------------'+'\n'+'Группа: '+str(groups[num])+'\n'
        for name in names[num]:
            txt = str(name)+': '+str(vk.method("users.get",{"user_ids":name})[0]["first_name"])+' '+str(vk.method("users.get",{"user_ids":name})[0]["last_name"])+'\n'
            txtall += txt
    vk.method("messages.send", {"domain": 'holeur', "message":txtall, "random_id": random.randint(100, 2147483647)})

def checkgroups(): #Список групп.
    global groups
    txtall = ''
    for group in groups:
        txt = group+'\n'
        txtall += txt
    vk.method("messages.send", {"domain": 'holeur', "message":txtall, "random_id": random.randint(100, 2147483647)})

def testperm(): #Попытка в проверку доступа к участнику со стороны сообщества. Не работает ибо в вк работают твари. https://vk.com/holeur?z=photo125524519_457246955%2Falbum125524519_00%2Frev
    global names
    txtall = ''
    for name in names[0]:
        try:
            if vk.method("messages.isMessagesFromGroupAllowed",{"group_id":"181204528","user_id":name}):
                txt = name,'красавчик.'
            else:
                txt = name,'не читает закреп.'
            txtall += txt+'\n'
        except Exception as e:
            print('testperm err:',e,name)

def checkmassive(x4,x3,x2,x1): #Получение элемента из массива. Пока что не работает.
    global globalday,sendingerrflag
    try:
        print(globalday[x4][x3][x2][x1])
        vk.method("messages.send", {"domain": 'holeur', "message":'Элемент:'+str(globalday[x4][x3][x2][x1]), "random_id": random.randint(100, 2147483647)})
    except IndexError:
        print('Индекса не существует.')
        if sendingerrflag:
            vk.method("messages.send", {"domain": 'holeur', "message":'Индекса не существует.', "random_id": random.randint(100, 2147483647)})

def deletemes(text):
    messages = vk.method("messages.search",{"q":text,"peer_id":"125524519","group_id":"181204528","count":"99"})
    for message in messages["items"]:
        vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})    
        print('Удалено со стороны бота:',message["text"])
        
def help(id): #Получение помощи по командам. Сделано пока кастыльно, но работает.
    txt = '-/|\-\ncom:delerr - Удаление недавних ошибок\ncom:getelem: - неработающая хрень\ncom:list - список участников\ncom:erroff - включение/выключение ошибок\ncom:send - рассылка сообщения всем участникам\ncom:grouplist - список всех групп участников\n+add:* - добавление участника\n+addgr:* добавление группы'
    vk.method("messages.send", {"domain": id, "message":txt, "random_id": random.randint(100, 2147483647)})
    
def detectcomm(): #Обработчик комманд
    global sendingerrflag,globalday
    messages = vk.method("messages.search",{"q":"com:","peer_id":"125524519","group_id":"181204528","count":"99"})
    for message in messages["items"]:
        if '-/|\-' in message:
            continue
        if message["text"] == "com:delerr":
            delerr()
            vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})
        elif message["text"][:11] == 'com:delmes:':
            deletemes(message["text"][12:])
        elif message["text"][:12] == "com:getelem:": #com:getelem:2:2:2:2
            checkmassive(int(message["text"][12]),int(message["text"][14]),int(message["text"][16]),int(message["text"][18]))
            vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})
        elif message["text"] == "com:list":
            checklist()
            vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})    
        elif message["text"] == "com:erroff":
            if sendingerrflag:
                sendingerrflag = 0
                print('errsend:',sendingerrflag)
                vk.method("messages.send", {"domain": 'holeur', "message":'Вывод ошибок выключен.', "random_id": random.randint(100, 2147483647)})
                vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})    
            else:
                sendingerrflag = 1
                print('errsend:',sendingerrflag)
                vk.method("messages.send", {"domain": 'holeur', "message":'Вывод ошибок включен.', "random_id": random.randint(100, 2147483647)})
                vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})    
        elif message["text"][:9] == "com:send:":
            sendmes(message["text"][9:])
            vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})    
        elif message["text"] == "com:help":
            help('holeur')
            vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})    
        elif message["text"] == "com:groupslist":
            checkgroups()
            vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})   
        else:
            vk.method("messages.send", {"domain": 'holeur', "message":'Команда не опознана.', "random_id": random.randint(100, 2147483647)})
            vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})

def checkbug(): #Если опять будет err:Опять наебнулись массивы. - дофиксить и вписать в цикл
    global kastilcheck,globalday,kastilflag
    if globalday[0] == empty and kastilcheck <= 0:
        kastilcheck = 10
    if kastilcheck > 0:
        if globalday[0] == empty:
            vk.method("messages.send", {"domain": 'holeur', "message":'err:Опять наебнулись массивы.', "random_id": random.randint(100, 2147483647)})
            kastilflag = 0
        kastilcheck -= 1
            
#
# Основная часть кода где обьявляются все функции.
#
flag1 = 1
flag2 = 0
while True:
    try:
        #fullzeromas()
        detectcomm()
        getgroups()
        getnames()
        for numgroup in range(len(groups)):
            print('Обработка расписания группы:',groups[numgroup])
            update(numgroup)
            checkupt()
            checkdate(1)
            if checkflag:
                time.sleep(4)
                taketabl(numgroup)
                eq(numgroup)
                save(numgroup)
            checkdate(2)
        flag1 = 0
        if flag1:
            vk.method("messages.send", {"domain": 'holeur', "message":'Бот включился.', "random_id": random.randint(100, 2147483647)})
    except Exception as e:
        if sendingerrflag:
            vk.method("messages.send", {"domain": 'holeur', "message":'err:'+str(e), "random_id": random.randint(100, 2147483647)})