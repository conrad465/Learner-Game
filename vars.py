import random
def init():
    global size; size = 700
    global cell_size; cell_size = 10
    global squares; squares = int(size / cell_size)
    global player_speed; player_speed = 7
    global player_scale; player_scale = 4
    global player_size; player_size = player_scale*cell_size
    global block_scale; block_scale = 5
    global bullet_scale; bullet_scale = 1
    global block_size; block_size = block_scale * cell_size
    global bullet_speed; bullet_speed = 20
    global next_gen; next_gen = 7
    global shoot_req; shoot_req = 23
    global gravity; gravity = 2
    global jump_vel; jump_vel = -22
    global gen_dir; gen_dir = 'generations/'
    global mutate_range; mutate_range = .85
    global padding; padding = 0
    global player_num; player_num = 2
    global vision; vision = 2
    global awareness; awareness= (2*(vision+1))* (2*(vision+1))
    global gen_size; gen_size = 15
    global env_timeout; env_timeout = 230
    global inputs; inputs = 14
    global generation_carryover; generation_carryover = 12












