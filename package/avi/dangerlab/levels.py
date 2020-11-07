level1_map =\
[[1,1,1,1,3],
 [1,0,1,0,1],
 [2,1,1,1,1],
 [1,0,1,0,3],
 [1,1,3,1,1]] 

level2_map =\
[[0,0,3,0,0],
 [0,0,1,0,0],
 [2,1,1,1,3],
 [0,0,1,0,0],
 [0,0,3,0,0]] 

level3_map =\
[[1,1,1,1,3],
 [1,0,1,0,1],
 [2,1,3,1,1],
 [1,0,1,0,3],
 [1,1,3,1,1]] 

level4_map =\
[[1,1,1,0,3],
 [1,0,1,0,1],
 [2,0,1,1,1],
 [1,0,0,0,1],
 [1,3,0,3,1]] 

levels = {1: [level1_map, 1], 2: [level2_map, 1], 3: [level3_map, 3], 4: [level4_map, 2]}      

level_search_border_map =\
[[2,1,1,1,1],
 [1,0,0,0,1],
 [1,0,0,0,1],
 [1,0,0,0,3],
 [1,1,3,1,1]] 

level_search_empty_map =\
[[2,1,1,1,1],
 [1,1,3,1,1],
 [1,1,1,1,1],
 [1,1,1,1,3],
 [1,1,3,1,1]] 

level_search_diag_map =\
[[2,1,0,0,0],
 [1,1,1,0,0],
 [0,0,1,1,0],
 [0,0,0,1,1],
 [0,0,0,1,3]] 

level_search_grid_map =\
[[2,1,1,1,1],
 [1,0,1,0,3],
 [1,1,1,1,1],
 [1,0,1,0,1],
 [1,1,1,3,3]] 

level_search_krest_map =\
[[2,1,0,1,3],
 [1,1,1,1,1],
 [1,0,0,1,0],
 [1,1,0,1,1],
 [1,3,1,3,1]] 

level_search_empty_enemy_map =\
[[2,1,1,1,1],
 [1,1,3,1,1],
 [3,1,1,1,1],
 [1,1,1,1,3],
 [1,1,3,1,1]] 

levels_task = { 'search_border':[level_search_border_map, 0],
                'search_empty':[level_search_empty_map, 0],
                'search_diag':[level_search_diag_map, 0],
                'search_grid':[level_search_grid_map, 0],
                'search_krest':[level_search_krest_map, 0],
                'search_empty_enemy1':[level_search_empty_enemy_map, 1],
                'search_empty_enemy2':[level_search_empty_enemy_map, 2],
                'search_empty_enemy3':[level_search_empty_enemy_map, 3],
                'level1':[level1_map, 1],
                'level2':[level2_map, 1],
                'level3':[level3_map, 3],
                'level4':[level4_map, 2]
    }

