import pandas as pd
import numpy as np
from pathlib import *

#ввод количества студентов в группах с условием
while True:
    try:    
        n = int(input("Введите количество студентов в группах \n"))
        if ((n!=12) and (n!=22)):
            print("Неверное число учеников, исправьте данные!")
            raise Exception()
        break
    except Exception as e:
        print('Количество студентов в группе может быть равно 12 или 22.')
        
#импортиурем входные данные учебного плана, зарплатах, цен на различные расходы и т.д.
university = pd.read_csv(Path.cwd() / 'assets' / 'university.csv')
plan_learn = pd.read_csv(Path.cwd() / 'assets' / 'plan_learning.csv')
offline_un = pd.read_csv(Path.cwd() / 'assets' / 'offline_un.csv')
online_un = pd.read_csv(Path.cwd() / 'assets' / 'online_un.csv')

#вычисление затрат для университета, вне зависимости от формата обучения 
def base_university_costs():
    sum = 0
    #зарплата и ежеквартальные бонусы преподавателям, учитвая начисления на оплату труда + премии
    for i in range(8):
        sum += plan_learn['coach_count'][i] * (university['salary_coach'][0] * 6 * 1.3 + 2 * university['bonus'][0])
    #зарплата бухгалтера, методистов, системного администратора с учетом начислений на оплату труда + премии
    sum += 12 * 4 * (university['salary_accountant'][0] + 2 * university['salary_met'][0] + university['salary_admin'][0]) * 1.3
    sum += 4 * 4 * 3 * university['bonus'][0]
    #оборудование - столы и стулья для сотрудников, компьютеры, канцелярия и прочее
    sum += university['equipment'][0]
    #затраты на интернет
    sum += 12 * 4 * university['internet'][0] 
    #затраты на 1с
    sum += university['1c'][0] 
    return sum

#вычисления дополнительных затрат на оффлайн обучение    
def offline_costs(n):
    sum = 0
    #затраты на аренду всех помещений
    sum += 4 * 12 * offline_un['rent'][0] * offline_un['square'][0]
    #зарплата охраннику, уборщице и гардеробщице с учетом начислений на оплату труда + премии
    sum += 4 * 12 * (offline_un['salary_secur'][0] + offline_un['salary_checkroom'][0] + offline_un['salary_cleaning'][0]) * 1.3 + 4 * 3 * 2 * offline_un['bonus'][0]
    #затраты на столы и стулья для учеников + компьютеры в терминал-классы
    sum += offline_un['chairs_and_tables'][0] * 4 * n / 2 + offline_un['computers'][0] * n
    return sum

#вычисления дополнительных затрат на онлайн обучение 
def online_cost():
    sum = 0
    sum += 4 * 12 * (online_un['zoom'][0])
    return sum

#вычисляем итоговую стомость оффлайн обучения
offline_univer = base_university_costs() + offline_costs(n)

#вычисляем итоговую стоимость онлайн обучения
online_univer = base_university_costs() + online_cost()

#теперь вычислим стоимость обучения для одного студента
#оффлайн:
student_offline = offline_univer / n

#онлайн
student_online = online_univer / n

#округлим данные
student_offline = round(student_offline)
student_online = round(student_online)

#выведим полученные данные для оффлайна
print ("Затраты на оффлайн обучение для одного студента составляют", student_offline)

#выводим полученные данные для онлайна
print ("Затраты на онлайн обучение для одного студента составляют", student_online)

#теперь проанализируем данные
if (student_offline>student_online):
    print("Онлайн обучение обходится дешвле оффлайн обучения")
else:
    print("Оффлайн обучение обходится дешвле онлайн обучения")
    



