# -*- coding: utf-8 -*-
# __author__ = 'siyuan' & 'jiwen'
import random
WORLD_SIZE = 5
discount = 0.9
# left, up, right, down
actions = ['L', 'U', 'R', 'D']


def construct_MDP(A_POS, A_TO_POS, A_REWARD, B_POS, B_TO_POS, B_REWARD):
    nextState = []
    actionReward = []
    for i in range(0, WORLD_SIZE):
        nextState.append([])
        actionReward.append([])
        for j in range(0, WORLD_SIZE):
            next = dict()
            reward = dict()
            if i == 0:
                next['U'] = [i, j]
                reward['U'] = -1.0
            else:
                next['U'] = [i - 1, j]
                reward['U'] = 0.0

            if i == WORLD_SIZE - 1:
                next['D'] = [i, j]
                reward['D'] = -1.0
            else:
                next['D'] = [i + 1, j]
                reward['D'] = 0.0

            if j == 0:
                next['L'] = [i, j]
                reward['L'] = -1.0
            else:
                next['L'] = [i, j - 1]
                reward['L'] = 0.0

            if j == WORLD_SIZE - 1:
                next['R'] = [i, j]
                reward['R'] = -1.0
            else:
                next['R'] = [i, j + 1]
                reward['R'] = 0.0

            if [i, j] == A_POS:
                next['L'] = next['R'] = next['D'] = next['U'] = A_TO_POS
                reward['L'] = reward['R'] = reward['D'] = reward['U'] = A_REWARD

            if [i, j] == B_POS:
                next['L'] = next['R'] = next['D'] = next['U'] = B_TO_POS
                reward['L'] = reward['R'] = reward['D'] = reward['U'] = B_REWARD

            nextState[i].append(next)
            actionReward[i].append(reward)
    return nextState, actionReward


# value iteration
def value_iteration(nextState, actionReward):
    world = [[0 for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]
    iter_count = 0
    while True:
        # keep iteration until convergence
        difference = 0
        #print(nextState)
        tmp_grid = [[0 for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]
        for i in range(WORLD_SIZE):
            for j in range(WORLD_SIZE):

                state = nextState[i][j]
                val = -float('inf')
                
                for act in actions:
                    x, y = state[act]
                    tmp = actionReward[i][j][act] + discount*world[x][y]
                    if val <= tmp:
                        val =  tmp

                difference += abs(world[i][j]-val)
                tmp_grid[i][j] = val
        iter_count += 1        
        import copy
        world = copy.deepcopy(tmp_grid)             
        # keep iteration until convergence
        if difference < 1e-4:
            print('Value Iteration: {} iters.'.format(iter_count))
            for j in range(WORLD_SIZE):
                print([round(each_v, 1)for each_v in world[j]])
            break


def policy_evaluation(world, policy, nextState, actionReward):
    while True:
        difference = 0
        tmp_grid = [[0 for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]
        for i in range(WORLD_SIZE):
            for j in range(WORLD_SIZE):
                state = nextState[i][j]                
                act = actions[policy[i][j]]
                x, y = state[act]
                val = actionReward[i][j][act] + discount*world[x][y]
                difference += abs(world[i][j]-val)
                tmp_grid[i][j] = val       
        import copy
        world = copy.deepcopy(tmp_grid)             
        if difference < 1e-4:
            break
    return world


# policy iteration
def policy_iteration(nextState, actionReward):
    import copy
    # random initialize state value and policy
    world = [[0 for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)] 
    policy = [[random.randint(0, len(actions)-1) for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]
    iter_count = 0
    while True:
        world = policy_evaluation(world, policy, nextState, actionReward)
        change_flag = True
        iter_count += 1
        
        for i in range(WORLD_SIZE):
            for j in range(WORLD_SIZE):
                state = nextState[i][j]
                Q_val = -float('inf')
                x_p, y_p = state[actions[policy[i][j]]]
                q_p = actionReward[i][j][actions[policy[i][j]]] + discount*world[x_p][y_p]

                for act in actions:
                    x, y = state[act]
                    q = actionReward[i][j][act] + discount*world[x][y]
                    if Q_val < q:
                        Q_val = q
                        act_id = "LURD".find(act) 
                if Q_val > q_p:
                    policy[i][j] = act_id
                    change_flag = False
        if change_flag:
            break
    print('Policy Iteration: {} iters.'.format(iter_count))
    for j in range(WORLD_SIZE):
        print([round(each_v, 1) for each_v in world[j]])


def process_read(x):
    from_state = [int(x[0][1]), int(x[0][-2])]
    to_state = [int(x[1][1]), int(x[1][-2])]
    reward = float(x[-1])
    return from_state, to_state, reward


random.seed(2020)
while True:
    try:
        A_list = input().strip().split()
        B_list = input().strip().split()
        A_POS, A_TO_POS, A_REWARD = process_read(A_list)
        B_POS, B_TO_POS, B_REWARD = process_read(B_list)
        nextState, actionReward = construct_MDP(A_POS, A_TO_POS, A_REWARD, B_POS, B_TO_POS, B_REWARD)
        value_iteration(nextState, actionReward)
        policy_iteration(nextState, actionReward)
    except EOFError:
        break



