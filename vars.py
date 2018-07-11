def init():
    global size
    global squares
    global cell_size
    global player_speed
    global player_scale
    global block_scale
    global bullet_scale
    global bullet_speed
    global shoot_req
    global gravity
    global jump_vel
    global gen_dir; gen_dir = 'generations/'
    global mutate_range; mutate_range = .4
    global padding; padding = 4
    global vision; vision = 2
    global awareness; awareness= (2*(vision+1))* (2*(vision+1))
    global gen_size; gen_size = 30
    global env_timeout; env_timeout = 130
    size = 700
    cell_size = 10
    player_scale = 4
    bullet_scale = 1
    block_scale = 5
    gravity = 2;
    size = 700
    cell_size = 10
    squares = int(size / cell_size)
    bullet_speed = 20
    player_speed = 7
    shoot_req = 14
    jump_vel = -22
