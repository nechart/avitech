#############################################
# Multyplayer

mlevel_empty =\
[[1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
] 

mlevel_4cubes =\
[[1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,0,0,1,1,0,0,1,1],
 [1,1,0,0,1,1,0,0,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,0,0,1,1,0,0,1,1],
 [1,1,0,0,1,1,0,0,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
] 

mlevel_crest =\
[[1,1,1,1,0,1,1,1,1,1],
 [1,1,1,1,0,1,1,1,1,1],
 [1,1,1,1,0,1,1,1,1,1],
 [1,1,1,1,0,1,1,1,1,1],
 [0,0,1,1,1,1,1,0,0,0],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,0,1,1,1,1,1],
 [1,1,1,1,0,1,1,1,1,1],
 [1,1,1,1,0,1,1,1,1,1],
 [1,1,1,1,0,1,1,1,1,1],
] 

mlevel_diag =\
[[0,1,1,1,1,1,1,1,1,0],
 [1,0,1,1,1,1,1,1,0,1],
 [1,1,0,1,1,1,1,0,1,1],
 [1,1,1,0,1,1,0,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1,1,1,1],
 [1,1,1,0,1,1,0,1,1,1],
 [1,1,0,1,1,1,1,0,1,1],
 [1,0,1,1,1,1,1,1,0,1],
 [0,1,1,1,1,1,1,1,1,0],
] 

mlevel_closely =\
[[1,1,1,1,1,1],
 [1,1,1,1,1,1], 
 [1,1,1,1,1,1], 
 [1,1,1,1,1,1], 
 [1,1,1,1,1,1], 
 [1,1,1,1,1,1],     
] 

mlevel_survival_empty =[[1]*20 for i in range(10)]

# карта двух лагерей
mlevel_camp2 = mlevel_survival_empty.copy()
mlevel_camp2[5][1] = 6
mlevel_camp2[5][18] = 6
for i in range(0, 10, 4):
    mlevel_camp2[i][10] = 0
for i in range(2, 10, 4):
    mlevel_camp2[i][9] = 0

levels = {'empty':{'map': mlevel_empty, 'guards':6, 'chests':10},
          '4cubes':{'map': mlevel_4cubes, 'guards':3, 'chests':5},
          'crest':{'map': mlevel_crest, 'guards':10, 'chests':5},
          'close':{'map': mlevel_closely, 'guards':6, 'chests':3},
          'diag':{'map': mlevel_diag, 'guards':6, 'chests':3},
          'survival':{'map': mlevel_survival_empty, 'guards':8, 'chests':8},
          'camp':{'map': mlevel_camp2, 'guards':8, 'chests':8, 
            'teams':[{'color':'blue', 'location':(5,1), 'cols':(0,9)},
                     {'color':'yellow', 'location':(5,18), 'cols':(10,19)}]
                }
        }