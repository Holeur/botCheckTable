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
    global day1,day2,day3,day4,day5,day6
    if x==1:
        day1 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
    elif x==2:        
        day2 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
    elif x==3:   
        day3 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
    elif x==4:   
        day4 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
    elif x==5:        
        day5 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
    elif x==6:   
        day6 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
    else:
        day1 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
        day2 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
        day3 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
        day4 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
        day5 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]
        day6 = [['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','',''],
                ['','','','','','','']]

day1old = [['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','','']]
        
day2old = [['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','','']]
        
day3old = [['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','','']]
        
day4old = [['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','','']]
        
day5old = [['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','','']]
        
day6old = [['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','','']]
        
#/html/body/div/div[2]/table/tbody/tr[1]/th Первый день недели 
#/html/body/div/div[2]/table/tbody/tr[2]/th[1] Первое название заголовка
#/html/body/div/div[2]/table/tbody/tr[3]/td[1] Первый элемент таблицы
#/html/body/div/div[2]/table/tbody/tr[6]/th Второй день недели
#/html/body/div/div[2]/table/tbody/tr[7]/th[1] Второе название заголовка 

browser = webdriver.Chrome()
browser.get('https://timetable.ptpit.ru/getTimeTable#')
vk = vk_api.VkApi(token=os.getenv("BOT_TOKEN"))

#names = ['holeur',137600777,'kleschevnikovs']
names = ['holeur']
date = ''
olddate = ''

def gettablinfile(filename): #запоминание массивов в фаил
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
        print(e)
        
def loadfile(filename): #Загрзка day*old в фаил. Пока не используется
    global day1old,day2old,day3old,day4old,day5old,day6old
    try:
        file = open(filename,'r')
        numline = 0
        numelem = 0
        num = 1
        for line in file:
            day('day'+str(num)+'old')[numline][numelem] = line[0:len(line)-1]
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
        print(e)
    
def save(): #перевод основных массивов в память
    global day1old,day2old,day3old,day4old,day5old,day6old,olddate,date
    try:
        day1old = day1
        day2old = day2
        day3old = day3
        day4old = day4
        day5old = day5
        day6old = day6
        olddate = date
        zeromas(0)
        print('Массивы сохранены')
        #gettablinfile('bd.txt')
    except Exception as e:
        print(e)

def update(): #открытие страницы
    browser.refresh()
    time.sleep(3)
    try:
        Select(browser.find_element_by_xpath('/html/body/div[1]/div[1]/form/div[2]/select[1]')).select_by_value('81')
        browser.find_element_by_xpath('//*[@id="btnGetTimetable"]').click()
    except:
        print('Опять ошибка с поиском элемента')
        update()
    
def day(nameday): #Выбор массива по названию
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
    global line,browser
    flag1 = 1
    line2 = 2
    elem = 1
    while flag1:
        try:
            day(nday)[line2-2][elem-1] = browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line+line2)+']/td['+str(elem)+']').text
            #print(day(nday)[line2-2][elem-1])
            elem += 1
            if elem > 7:
                elem = 1
                line2 += 1
        except selenium.common.exceptions.NoSuchElementException:
            flag1 = 0

def taketabl(): #Заполнение всех основных массивов по дням недели
    global line,date
    date = browser.find_element_by_xpath("/html/body/div/div[1]/form/div[1]/select").text
    for line in range(1,36):
        try:
            if 'Понедельник' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Понедельник')
                zeromas(1)
                zap('day1')
            elif 'Вторник' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Вторник')
                zeromas(2)
                zap('day2')
            elif 'Среда' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Среда')
                zeromas(3)
                zap('day3')
            elif 'Четверг' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Четверг')
                zeromas(4)
                zap('day4')
            elif 'Пятница' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Пятница')
                zeromas(5)
                zap('day5')
            elif 'Суббота' in browser.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr['+str(line)+']/th').text:
                print('Суббота')
                zeromas(6)
                zap('day6')
        except selenium.common.exceptions.NoSuchElementException:
            print('Не найдена строка под номером',line)
            #print()
    for num in range(1,7):
        print(day('day'+str(num))) #Вывод в консоль собранных массивов

def writetxtall(numday): #Алгоритм создания сообщения
    global txtall,flag1
    txt = ''
    txtall = ''
    numelem = 0
    numline = 0
    for line in day(numday):
        for elem in line:
            if numelem == 0:
                if day(numday)[numline][0] != day(numday+'old')[numline][0]:
                    txt = '*Пара> ' + elem + ' (Было>' + str(day(numday+'old')[numline][0]) + ')\n'
                else:
                    txt = 'Пара> ' + elem + '\n'
            elif numelem == 1:
                if day(numday)[numline][1] != day(numday+'old')[numline][1]:
                    txt = '*Время> ' + elem + ' (Было>' + str(day(numday+'old')[numline][1]) + ')\n'
                else:
                    txt = 'Время> ' + elem + '\n'
            elif numelem == 2:
                if day(numday)[numline][2] != day(numday+'old')[numline][2]:
                    txt = '*Предмет> ' + elem + ' (Было>' + str(day(numday+'old')[numline][2]) + ')\n'
                else:
                    txt = 'Предмет> ' + elem + '\n'
            elif numelem == 3:
                if day(numday)[numline][3] != day(numday+'old')[numline][3]:
                    txt = '*Подгруппа> ' + elem + ' (Было>' + str(day(numday+'old')[numline][3]) + ')\n'
                else:
                    txt = 'Подгруппа> ' + elem + '\n'
            elif numelem == 4:
                # if day(numday)[numline][4] != day(numday+'old')[numline][4]:
                    # txt = '*Группа> ' + elem + ' (Было>' + str(day(numday+'old')[numline][4]) + ')\n'
                # else:
                    # txt = 'Группа> ' + elem + '\n'
                if elem == '':
                    print('Пропускаем пустоту')
                else:
                    print(elem+'пропускаем')
            elif numelem == 5:
                if day(numday)[numline][5] != day(numday+'old')[numline][5]:
                    txt = '*Преподаватель> ' + elem + ' (Было>' + str(day(numday+'old')[numline][5]) + ')\n'
                else:
                    txt = 'Преподаватель> ' + elem + '\n'
            elif numelem == 6:
                if day(numday)[numline][6] != day(numday+'old')[numline][6]:
                    txt = '*Кабинет> ' + elem + ' (Было>' + str(day(numday+'old')[numline][6]) + ')\n'
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
    if numday == 'day1':
        txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nПонедельник изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
    elif numday == 'day2':
        txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nВторник изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
    elif numday == 'day3':
        txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nСреду изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
    elif numday == 'day4':
        txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nЧетверг изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
    elif numday == 'day5':
        txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nПятницу изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
    elif numday == 'day6':
        txtall = '/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\nСубботу изменили\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n'+txtall+'\n'
    if flag1:
        txtall = '{Первый цикл}\n' + txtall

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
            print(e)
            
def eq(): #сравнение таблиц
    global day1old,day2old,day3old,day4old,day5old,day6old,day1,day2,day3,day4,day5,day6,flag1,txtall
    if date == olddate:
        if day1 != day1old:
            print('Понедельник изменили')
            writetxtall('day1')
            if flag1 == 0:
                sendmes(txtall)
            #filewrite(txtall)
        if day2 != day2old:
            print('Вторник изменили')
            writetxtall('day2')
            if flag1 == 0:
                sendmes(txtall)
            #filewrite(txtall)
        if day3 != day3old:
            print('Среду изменили')
            writetxtall('day3')
            if flag1 == 0:
                sendmes(txtall)
            #filewrite(txtall)
        if day4 != day4old:
            print('Четверг изменили')
            writetxtall('day4')
            if flag1 == 0:
                sendmes(txtall)
            #filewrite(txtall)
        if day5 != day5old:
            print('Пятницу изменили')
            writetxtall('day5')
            if flag1 == 0:
                sendmes(txtall)
            #filewrite(txtall)
        if day6 != day6old:
            print('Субботу изменили')
            writetxtall('day6')
            if flag1 == 0:
                sendmes(txtall)
            #filewrite(txtall)
    elif flag1 == 0:
        txtin = "Появилось расписание на следуйщую неделю на: "
        if day1 != day1old:
            txtin += '  Понедельник\n'
        if day2 != day2old:
            txtin += '  Вторник\n'
        if day3 != day3old:
            txtin += '  Среду\n'
        if day4 != day4old:
            txtin += '  Четверг\n'
        if day5 != day5old:
            txtin += '  Пятницу\n'
        if day6 != day6old:
            txtin += '  Субботу\n'
        sendmes(txtin)
    else:
        vk.method("messages.send", {"domain": 'holeur', "message":'Бот включился.', "random_id": random.randint(100, 2147483647)})
        
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

def debug(): #2000000078
    chats = vk.method("messages.getConversations",{"filter":"all","count":200})
    for chat in chats["items"]["conversation"]:
        txtalll = chat["peer"]["id"],chat["chat_settings"]["title"],'\n'
    vk.method("messages.send", {"domain": 'holeur', "message":txtalll, "random_id": random.randint(100, 2147483647)})
        
    

zeromas(0)
#loadfile('bd.txt')
flag1 = 1
debug()
while True:
    try:
        getnames()
        update()
        checkupt()
        if checkflag:
            time.sleep(4)
            taketabl()
            eq()
            flag1 = 0
            save()
            time.sleep(3)
    except Exception as e:
        vk.method("messages.send", {"domain": 'holeur', "message":e, "random_id": random.randint(100, 2147483647)})
