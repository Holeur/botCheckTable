# -*- coding: utf-8 -*-
import selenium
import vk_api
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

def zeromas(x):
    global day1,day2,day3,day4,day5,day6,globalday
    if x==1:
        day1 = [['','','','','','','']]
        globalday[0] = [['','','','','','','']]
    elif x==2:
        day2 = [['','','','','','','']]
        globalday[1] = [['','','','','','','']]
    elif x==3:
        day3 = [['','','','','','','']]
        globalday[2] = [['','','','','','','']]
    elif x==4:
        day4 = [['','','','','','','']]
        globalday[3] = [['','','','','','','']]
    elif x==5:
        day5 = [['','','','','','','']]
        globalday[4] = [['','','','','','','']]
    elif x==6:
        day6 = [['','','','','','','']]
        globalday[5] = [['','','','','','','']]
    else:
        day1 = [['','','','','','','']]
        day2 = [['','','','','','','']]
        day3 = [['','','','','','','']]
        day4 = [['','','','','','','']]
        day5 = [['','','','','','','']]
        day6 = [['','','','','','','']]
        globalday = [[['','','','','','','']]]

day1old = []
day2old = []
day3old = []
day4old = []
day5old = []
day6old = []

globaldayold = [[['','','','','','','']]]

#/html/body/div/div[2]/table/tbody/tr[1]/th Первый день недели 
#/html/body/div/div[2]/table/tbody/tr[2]/th[1] Первое название заголовка
#/html/body/div/div[2]/table/tbody/tr[3]/td[1] Первый элемент таблицы
#/html/body/div/div[2]/table/tbody/tr[6]/th Второй день недели
#/html/body/div/div[2]/table/tbody/tr[7]/th[1] Второе название заголовка 

browser = webdriver.Chrome()
browser.get('https://timetable.ptpit.ru/getTimeTable#')
vk = vk_api.VkApi(token=os.getenv("BOT_TOKEN"))

names = ['holeur']
groups = ['17СПИ3']
date = ''
olddate = ''
sendingerrflag = 1

def gettablinfile(filename): #запоминание массивов в фаил. Пока не используется
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
        
def loadfile(filename): #Загрзка day*old в фаил. Пока не используется
    global globaldayold,globalday
    try:
        file = open(filename,'r')
        numline = 0
        numelem = 0
        num = 1
        for line in file:
            globalday[num-1][numline][numelem] = line[0:len(line)-1]
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
        
def save(): #перевод основных массивов в память
    global globaldayold,globalday,olddate,date
    try:
        for num in range(6): #day1old = day1...
            try:
                globaldayold[num] = globalday[num]
            except IndexError:
                globaldayold.append([])
                globaldayold[num] = globalday[num]
        #print(globaldayold)
        olddate = date
        zeromas(0)
        print('Массивы сохранены')
        #gettablinfile('bd.txt')
    except Exception as e:
        print('save err:',e)

def update(group): #открытие страницы
    browser.refresh()
    time.sleep(3)
    try:
        Select(browser.find_element_by_xpath('/html/body/div[1]/div[1]/form/div[2]/select[1]')).select_by_visible_text(group)
        browser.find_element_by_xpath('//*[@id="btnGetTimetable"]').click()
    except:
        print('Опять ошибка с поиском элемента')
        update(group)
    
def day(nameday): #Выбор массива по названию. Не используется. Лежит в память о старом алгоритме
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

def zap(nday): #Заполнение выбранного массива
    global line,browser,globalday
    flag1 = 1
    line2 = 2
    elem = 1
    while flag1:
        try:
            globalday[nday-1][line2-2][elem-1] = browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line+line2)+']/td['+str(elem)+']').text
            #print(globalday[nday-1][line2-2][elem-1])
            elem += 1
            if elem > 7:
                elem = 1
                line2 += 1
                globalday[nday-1].append(['','','','','','',''])
        except selenium.common.exceptions.NoSuchElementException:
            flag1 = 0
            del globalday[nday-1][line2-2]

def taketabl(): #Заполнение всех основных массивов по дням недели
    global line,date,globalday
    date = browser.find_element_by_xpath("/html/body/div/div[1]/form/div[1]/select").text
    for line in range(1,36):
        try:
            if 'Понедельник' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Понедельник')
                zeromas(1)
                zap(1)
            elif 'Вторник' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Вторник')
                zeromas(2)
                zap(2)
            elif 'Среда' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Среда')
                zeromas(3)
                zap(3)
            elif 'Четверг' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Четверг')
                zeromas(4)
                zap(4)
            elif 'Пятница' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Пятница')
                zeromas(5)
                zap(5)
            elif 'Суббота' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Суббота')
                zeromas(6)
                zap(6)
        except selenium.common.exceptions.NoSuchElementException:
            print('Не найдена строка под номером',line)
            #print()
    for num in range(1,7):
        print(globalday) #Вывод в консоль собранных массивов

def writetxtall(numday): #Алгоритм создания сообщения
    global globalday
    try:
        global txtall,flag1
        txt = ''
        txtall = ''
        numelem = 0
        numline = 0
        for line in globalday[numday-1]:
            for elem in line:
                if numelem == 0:
                    if globalday[numday-1][numline][0] != globaldayold[numday-1][numline][0]: #day(numday+'old')[numline][0]:
                        txt = '*Пара> ' + elem + '\n'
                    else:
                        txt = 'Пара> ' + elem + '\n'
                elif numelem == 1:
                    if globalday[numday-1][numline][1] != globaldayold[numday-1][numline][1]:
                        txt = '*Время> ' + elem + '\n'
                    else:
                        txt = 'Время> ' + elem + '\n'
                elif numelem == 2:
                    if globalday[numday-1][numline][2] != globaldayold[numday-1][numline][2]:
                        txt = '*Предмет> ' + elem + '\n'
                    else:
                        txt = 'Предмет> ' + elem + '\n'
                elif numelem == 3:
                    if globalday[numday-1][numline][3] != globaldayold[numday-1][numline][3]:
                        txt = '*Подгруппа> ' + elem + '\n'
                    else:
                        txt = 'Подгруппа> ' + elem + '\n'
                elif numelem == 4:
                    # if globalday[numday-1][numline][4] != globaldayold[numday-1][numline][4]:
                        # txt = '*Группа> ' + elem + '\n'
                    # else:
                        # txt = 'Группа> ' + elem + '\n'
                    if elem == '':
                        print('Пропускаем пустоту')
                    else:
                        print(elem+'пропускаем')
                elif numelem == 5:
                    if globalday[numday-1][numline][5] != globaldayold[numday-1][numline][5]:
                        txt = '*Преподаватель> ' + elem + '\n'
                    else:
                        txt = 'Преподаватель> ' + elem + '\n'
                elif numelem == 6:
                    if globalday[numday-1][numline][6] != globaldayold[numday-1][numline][6]:
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
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nПонедельник изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        elif numday == 2:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nВторник изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        elif numday == 3:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nСреду изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        elif numday == 4:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nЧетверг изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        elif numday == 5:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nПятницу изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        elif numday == 6:
            txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nСубботу изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
        if flag1:
            txtall = '{Первый цикл}\n' + txtall
    except Exception as e:
        print('writetextall err:',e)
    
def filewrite(text): #Запись полученного текста в фаил
    file = open('logs.txt','a')
    file.write(text)
    file.close()
    
def sendmes(text): #Скидывание оповещений нескольким людям
    global names
    for elem in names:
        try:
            if isinstance(elem,int):
                vk.method("messages.send", {"user_id": elem, "message":text, "random_id": random.randint(100, 2147483647)})
            else:
                vk.method("messages.send", {"domain": elem, "message":text, "random_id": random.randint(100, 2147483647)})
        except Exception as e:
            print('sendmes err:',e)
            
def eq(): #сравнение таблиц
    global sendingerrflag,globaldayold,globalday,flag1,txtall
    try:
        if date == olddate:
            if globalday[0] != globaldayold[0]: #day1old
                print('Понедельник изменили')
                writetxtall(1)
                if flag1 == 0:
                    sendmes(txtall)
                #filewrite(txtall)
            if globalday[1] != globaldayold[1]:
                print('Вторник изменили')
                writetxtall(2)
                if flag1 == 0:
                    sendmes(txtall)
                #filewrite(txtall)
            if globalday[2] != globaldayold[2]:
                print('Среду изменили')
                writetxtall(3)
                if flag1 == 0:
                    sendmes(txtall)
                #filewrite(txtall)
            if globalday[3] != globaldayold[3]:
                print('Четверг изменили')
                writetxtall(4)
                if flag1 == 0:
                    sendmes(txtall)
                #filewrite(txtall)
            if globalday[4] != globaldayold[4]:
                print('Пятницу изменили')
                writetxtall(5)
                if flag1 == 0:
                    sendmes(txtall)
                #filewrite(txtall)
            if globalday[5] != globaldayold[5]:
                print('Субботу изменили')
                writetxtall(6)
                if flag1 == 0:
                    sendmes(txtall)
                #filewrite(txtall)
        elif flag1 == 0:
            txtin = "Появилось расписание на следуйщую неделю на: "
            if globalday[0] == globaldayold[0]: #day1old
                txtin += '  Понедельник\n'
            if globalday[1] == globaldayold[1]:
                txtin += '  Вторник\n'
            if globalday[2] == globaldayold[2]:
                txtin += '  Среду\n'
            if globalday[3] == globaldayold[3]:
                txtin += '  Четверг\n'
            if globalday[4] == globaldayold[4]:
                txtin += '  Пятницу\n'
            if globalday[5] == globaldayold[5]:
                txtin += '  Субботу\n'
            sendmes(txtin)
        else:
            vk.method("messages.send", {"domain": 'holeur', "message":'Бот включился.', "random_id": random.randint(100, 2147483647)})
    except Exception as e:
        print('eq err:',e)
        if sendingerrflag:
            vk.method("messages.send", {"domain": 'holeur', "message":'err:'+str(e), "random_id": random.randint(100, 2147483647)})
        
def checkupt():
    global checkflag,tabledate
    try:
        tabledate = browser.find_element_by_xpath('/html/body/div/div[1]/form/div[1]/select').text
        checkflag = 1
    except:
        checkflag = 0

def getnames():
    global names
    oldnames = names
    names = ['holeur']
    number = 0
    messages = vk.method("messages.search",{"q":"+add","peer_id":"125524519","group_id":"181204528"})
    print(messages["count"])
    for mes in messages["items"]:
        if '+add' == mes["text"][:4]:
            name = mes["text"][5:]
            try:
                if int(name) not in names:
                    names.append(int(name))
                if int(name) not in oldnames:
                    print('Добавлен в массив',name)
            except ValueError:
                if name not in names:
                    names.append(name)
                if name not in oldnames:
                    print('Добавлен в массив',name)
        number += 1
    print(names)

def delerr(): #Функция удаления всех ошибок
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
            
def checklist(): #Список участников в боте
    global names
    txtall = ''
    for name in names:
        txt = str(name)+': '+str(vk.method("users.get",{"user_ids":name})[0]["first_name"])+' '+str(vk.method("users.get",{"user_ids":name})[0]["last_name"])+'\n'
        txtall += txt
    vk.method("messages.send", {"domain": 'holeur', "message":txtall, "random_id": random.randint(100, 2147483647)})

def detectcomm(): #Обработка комманд
    global sendingerrflag
    messages = vk.method("messages.search",{"q":"com:","peer_id":"125524519","group_id":"181204528","count":"99"})
    for message in messages["items"]:
        if message["text"] == "com:del":
            delerr()
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
        else:
            vk.method("messages.send", {"domain": 'holeur', "message":'Команда не опознана.', "random_id": random.randint(100, 2147483647)})
            vk.method("messages.delete",{"message_ids":message["id"],"delete_for_all":"0","group_id":"181204528"})

zeromas(0) #Для того, чтобы обьявить массивы
#loadfile('bd.txt')
flag1 = 1
while True:
    try:
        detectcomm()
        getnames()
        index = 0
        for group in groups:
            update(group)
            checkupt()
            if checkflag:
                time.sleep(4)
                taketabl()
                eq()
                flag1 = 0
                save()
            index += 1
    except Exception as e:
        if sendingerrflag:
            vk.method("messages.send", {"domain": 'holeur', "message":'err:'+str(e), "random_id": random.randint(100, 2147483647)})