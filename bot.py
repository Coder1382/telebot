import telebot
import random

help='/help - напечатать справку о программе\n /add - добавить задачу\n /show - показать список задач'
tasks={}
RANDOM=["позавтракать", "пообедать", "поужинать", "погулять", "потренироваться"]
token='insert your telegram bot token here' #here. you is supposed to write your telegram bor token
bot = telebot.TeleBot(token)
flags = {'flagadd': False, 'flagshow': False}
categories={"Работа":[], "Домашние дела":[], "Прочее":[]}
reserve=[]
reserve.append("")

@bot.message_handler(commands=['help', 'HELP', 'Help'])
def helper(message):
    bot.send_message(message.chat.id, help)
    for v in flags:
        flags[v]=False
    reserve[0]=""

@bot.message_handler(commands=['random'])
def rand(message):
    if flags['flagadd']==True:
        date="сегодня"
        task=random.choice(RANDOM)
        if date in tasks:
            tasks[date].append(task)
        else:
            tasks[date]=[]
            tasks[date].append(task)
        bot.send_message(message.chat.id, 'Выберите категорию в нижеследующем списке:\n')
        i=1
        reserve[0]=task
        for category in categories:
            bot.send_message(message.chat.id, category+" - введите \"/"+str(i)+"\", чтобы выбрать")
            i+=1
    else:
        bot.send_message(message.chat.id, "Out of context")
        reserve[0]=""
    for v in flags:
        flags[v]=False

@bot.message_handler(commands=['1', '2', '3'])
def cater(message):
    if reserve[0]!="":
        if message.text=='/1':
            if reserve[0] in categories["Работа"]:
                return
            else:
                categories["Работа"].append(reserve[0])
        elif message.text=='/2':
            if reserve[0] in categories["Домашние дела"]:
                return
            else:
                categories["Домашние дела"].append(reserve[0])
        if message.text=='/3':
            if reserve[0] in categories["Прочее"]:
                return
            else:
                categories["Прочее"].append(reserve[0])
        bot.send_message(message.chat.id, 'Задача добавлена')
        reserve[0]=""
    else:
        bot.send_message(message.chat.id, "Out of context")

@bot.message_handler(commands=['add', 'ADD', 'Add'])
def adder(message):
    flags['flagadd']=True
    flags['flagshow']=False
    bot.send_message(message.chat.id, "Введите через пробел: дату и название задачи, либо команду \"/random\", чтобы добавить случайную задачу")
    reserve[0]=""
    
@bot.message_handler(commands=['show', 'SHOW', 'Show'])
def display(message):
    flags['flagadd']=False
    flags['flagshow']=True
    bot.send_message(message.chat.id, "Введите даты через запятую, либо команду \"/all\", чтобы посмотреть весь список")
    reserve[0]=""
    
@bot.message_handler(commands=['ALL', 'All', 'all'])
def alllist(message):
    if flags['flagshow']==True:
        i=0
        for date in tasks:
            bot.send_message(message.chat.id, "Задачи на "+str(date)+":\n")
            i=0
            for task in tasks[date]:
                i+=1
                respond=task
                for category in categories:
                    if task in categories[category]:
                        respond=respond+" @"+category
                bot.send_message(message.chat.id, str(i)+". "+respond+'\n')
        if i==0:
            bot.send_message(message.chat.id, "Список пуст")
    else:
        bot.send_message(message.chat.id, "Out of context")
    for v in flags:
        flags[v]=False
    reserve[0]=""

@bot.message_handler(content_types=['text'])
def choice(message):
    if flags['flagadd']==True:
        message.text=message.text.lower()
        task=message.text.split(' ', 1)
        if len(task)<2:
            bot.send_message(message.chat.id, "Некорректное значение")
            reserve[0]=""
        elif len(task[1])<3:
            bot.send_message(message.chat.id, "Переформулируйте задачу")
            reserve[0]=""
        elif task[0] in tasks:
            tasks[task[0]].append(task[1])
            bot.send_message(message.chat.id, 'Выберите категорию:\n')
            i=1
            reserve[0]=task[1]
            for category in categories:
                bot.send_message(message.chat.id, category+" - введите \"/"+str(i)+"\", чтобы выбрать")
                i+=1
        else:
            tasks[task[0]]=[]
            tasks[task[0]].append(task[1])
            bot.send_message(message.chat.id, 'Выберите категорию:\n')
            i=1
            reserve[0]=task[1]
            for category in categories:
                bot.send_message(message.chat.id, category+" - введите \"/"+str(i)+"\", чтобы выбрать")
                i+=1
    elif flags['flagshow']==True:
        message.text=message.text.lower()
        dates=message.text.split(', ')
        for date in dates:
            if date in tasks:
                bot.send_message(message.chat.id, "Задачи на "+str(date)+":\n")
                i=0
                for task in tasks[date]:
                    i+=1
                    respond=task
                    for category in categories:
                        if task in categories[category]:
                            respond=respond+" @"+category
                    bot.send_message(message.chat.id, str(i)+". "+respond+'\n')
            else:
                bot.send_message(message.chat.id, "Дата не найдена")
        reserve[0]=""
    else:
        bot.send_message(message.chat.id, "Неизвестная команда\n"+help)
        reserve[0]=""
    for v in flags:
        flags[v]=False

bot.polling(none_stop=True)
