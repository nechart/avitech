from avi.mine.data.base import connect as connect
import avi.study.init as data_init

import avi.study.quiz as data_quiz

"""
con = connect()
data_init.drop_tables(con)
data_init.create_tables(con)
con.close()
"""
"""
data_quiz.insert_quiz('2020', 'test', 'asd', 12.3)
data_quiz.insert_quiz('2020', 'test', 'asd2', 13.4)
"""
print(data_quiz.find_quizzes('2020'))

# data_quiz.delete_quiz_user(quizname='2020', username='test')

"""
data_quiz.results = {'var_1': True,
                    'var_2': True,
                    'var_3': False,
                    'cycle_1': False,
                    'cond_4': False}

data_quiz.rate('2020')
"""