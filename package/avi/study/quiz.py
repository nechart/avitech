import ipywidgets as widgets
import sys
from IPython.display import display
from IPython.display import clear_output

results = {}

def create_multipleChoice_widget(quiz, description, options, correct_answer):
    if correct_answer not in options:
        options.append(correct_answer)
    
    correct_answer_index = options.index(correct_answer)
    
    radio_options = [(words, i) for i, words in enumerate(options)]
    alternativ = widgets.RadioButtons(
        options = radio_options,
        description = '',
        disabled = False
    )
    
    description_out = widgets.Output()
    with description_out:
        print(description)
        
    feedback_out = widgets.Output()

    def check_selection(b):
        global results
        nonlocal quiz
        correct = False
        a = int(alternativ.value)
        if a==correct_answer_index:
            s = '\x1b[6;30;42m' + "правильно" + '\x1b[0m' +"\n" #green color
            correct = True
        else:
            s = '\x1b[5;30;41m' + "ошибка" + '\x1b[0m' +"\n" #red color
        if not quiz in results:
            results[quiz] = correct
        with feedback_out:
            clear_output()
            print(s)
        return
    
    check = widgets.Button(description="ответить")
    check.on_click(check_selection)
    
    return widgets.VBox([description_out, alternativ, check, feedback_out])

def launch(quiz = '2020'):
    from IPython.display import display

    print('*'*30)
    print('Переменные. Типы данных. Вывод на экран.')
    display(create_multipleChoice_widget('var_1', 'В переменную какого типа python запишет число 1.56? ',
                                        ['int', 'str', 'float','boolean'],'float'))
    display(create_multipleChoice_widget('var_2', 'Что напечатает следующий код: print(1, "*"*3, 3 == 2+1)',
                                        ['1*3 == 2+1','1 *** True','1"*"*3True'],'1 *** True'))
    display(create_multipleChoice_widget('var_3', 'Выбери правильный тип type(1==3)',
                                        ['int', 'str', 'float','boolean'],'boolean'))
    display(create_multipleChoice_widget('var_4', 'Как правильно прочитать от пользователя целое число?',
                                        ['i1=int(input())', 'i1=input(int)', 'i1=input()'],'i1=int(input())'))
    print('*'*30)
    print('Условные операторы')
    display(create_multipleChoice_widget('cond_1', 'Какой оператор не относится к условным?',
                                        ['if', 'elif', 'for','and', 'else'],'for'))
    display(create_multipleChoice_widget('cond_2', 'Чему будет равна переменная res, если a = 5: if (a > 6): res = 10 else: res = 15',
                                        ['10','15','5'],'15'))
    display(create_multipleChoice_widget('cond_3', 'Как правильно записать условие a больше b и a не больше с:',
                                        ['a>b and a<c', 'a>b or a<=c', 'a>b and not a>c'],'a>b and not a>c'))
    display(create_multipleChoice_widget('cond_4', 'Какой символ используется в тернарном операторе:',
                                        ['?', '*', ':','.'],'?'))
    print('*'*30)
    print('Циклы')
    display(create_multipleChoice_widget('cycle_1', 'Чем отличаются цикл while от цикла for?',
                                        ['ничем - оба создают циклы', 'while работает по условию, for - по множеству', 'while работает по множеству, for - по условию','while - это пока, а for - для'],
                                        'while работает по условию, for - по множеству'))
    display(create_multipleChoice_widget('cycle_2', 'Чем отличаются инструкции continue и break?',
                                        ['continue прерывает цикл, а break итерацию','continue прерывает итерацию, а break - цикл','обе инструкции прерывают цикл'],
                                        'continue прерывает итерацию, а break - цикл'))
    display(create_multipleChoice_widget('cycle_3', 'Сколько раз выполнится цикл: for i in range(1, 10)?',
                                        ['1', '9', '10', '11'],'9'))
    display(create_multipleChoice_widget('cycle_4', 'Сколько раз выполнится цикл: while 5 > 4:',
                                        ['4', '5', 'бесконечное число','ни разу'],'бесконечное число'))
    print('*'*30)
    print('Списки. Кортежи. Словари')
    display(create_multipleChoice_widget('list_1', 'Какое число выведится на экран list1 = [1, 2, 3, 4] print(list1[-1])?',
                                        ['1', '2', '3','4'],
                                        '4'))
    display(create_multipleChoice_widget('list_2', 'Каким будет список list2 = [1, 2, 3] после команды list2.insert(1, 4)?',
                                        ['[1, 4, 2, 3]', '[1, 2, 3, 4]', '[4, 1, 2, 3]'],
                                        '[1, 4, 2, 3]'))
    display(create_multipleChoice_widget('list_3', 'Каким будет список list3 = [3, 4, 5, 2] после команды list3.remove(2)?',
                                        ['[3, 4, 5]', '[3, 4, 2]', '[3, 4, 5, 2, 2]'],
                                        '[3, 4, 5]'))
    display(create_multipleChoice_widget('list_4', 'Каким будет список list4 = [3, 4, 5, 2] после команды list4.sort(reverse=True)?',
                                        ['[3, 4, 5, 2]', '[2, 3, 4, 5]', '[5, 4, 3, 2]'],
                                        '[5, 4, 3, 2]'))
    display(create_multipleChoice_widget('list_5', "Чему равен список ключей словаря {1:'a', 2:'b', 3:'c'}",
                                        ["['a', 'b', 'c']", "[1, 2, 3, 'a', 'b', 'c']", '[1, 2, 3]'],
                                        '[1, 2, 3]'))
    print('*'*30)
    print('Встроенные функции')
    display(create_multipleChoice_widget('build_1', 'Что вернет функция len(list1) для списка list1 = [1, 2, 3, 4]?',
                                        ['1', '4', '10'],
                                        '4'))
    display(create_multipleChoice_widget('build_2', 'Что вернет выражение max(list1)-min(list1) для списка list1 = [1, 2, 3, 4]?',
                                        ['1', '4', '3'],
                                        '3'))
    display(create_multipleChoice_widget('build_3', 'Выбери правильный ответ, как узнать модуль числа -4?',
                                        ['round(-4)', 'abs(-4)', 'pow(-4, 2)'],
                                        'abs(-4)'))
    display(create_multipleChoice_widget('build_4', 'Чему равно выражение 7 // 3 + 7 % 3 ?',
                                        ['2', '3', '4'],
                                        '3'))
    print('*'*30)
    print('Функции. Модули')
    display(create_multipleChoice_widget('func_1', 'Как объявить функцию func с двумя аргументами, второй аргумент по умолчанию 1?',
                                        ['def func(a, b):', 'def func(a=0, b):', 'def func(a, b=0):'],
                                        'def func(a, b=0):'))
    display(create_multipleChoice_widget('func_2', 'Как скопировать в функции изменяемый объект obj?',
                                        ['copy(obj)', 'obj2 = obj', 'obj.copy()'],
                                        'obj.copy()'))
    display(create_multipleChoice_widget('func_3', 'Что дает выражение в функции: global x ?',
                                        ['для чтения глобальной переменной х', 'для записи глобальной переменной х', 'объявление глобальной переменной х'],
                                        'для записи глобальной переменной х'))
    display(create_multipleChoice_widget('func_4', 'Как импортировать модуль работы со случайными числами?',
                                        ['import random', 'import math', 'random.randint(5, 9)'],
                                        'import random'))
    print('*'*30)
    print('Файлы')
    display(create_multipleChoice_widget('file_1', 'Как открыть файл file1.txt, чтоб он автоматически закрылся?',
                                        ["with open('file1.txt') as file:", "open('file1.txt')", "with file = 'file1.txt'"],
                                        "with open('file1.txt') as file:"))
    display(create_multipleChoice_widget('file_2', 'Что прочитает функцию file.readline()',
                                        ['все содержимое файла', 'первую строку файла', 'текущую строку файла'],
                                        'текущую строку файла'))
    display(create_multipleChoice_widget('file_3', 'Как записать список строк в файл?',
                                        ['file.writelines()', 'file.readlines()', 'file.writeline()'],
                                        'file.writelines()'))

def rate(quiz = '2020'):
    import pandas as pd
    res_df = pd.Series(results).to_frame(name="value")

    topics = {'var':'Переменные. Типы данных. Вывод на экран.',
            'cond':'Условные операторы',
            'cycle':'Циклы',
            'list':'Списки. Словари',          
            'build':'Встроенные функции',          
            'func':'Функции',
            'file':'Файлы'
            }

    print('Результат:')
    for topic, name in topics.items():
        print('\n')
        topic_df = res_df[res_df.index.str.startswith(topic)]
        rate = topic_df.value.sum()/topic_df.value.count()
        print('{0}: {1}%'.format(name, round(rate*100)))
    print('\n')    
    print('Всего: {0} баллов из 100'.format(round(sum(results.values())/len(results.values())*100)))