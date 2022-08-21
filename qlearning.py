from pyqlearning.qlearning.greedy_q_learning import GreedyQLearning
import numpy as np


class BirdQLearner(GreedyQLearning):
    POLICY_LEN = 60

    def __init__(self):
        self.states = ['ru_lu', 'ru_li', 'ru_ld', 'ri_lu', 'ri_li', 'ri_ld', 'rd_lu', 'rd_li', 'rd_ld']
        self.actions = ['ru_lu', 'ru_li', 'ru_ld', 'ri_lu', 'ri_li', 'ri_ld', 'rd_lu', 'rd_li', 'rd_ld']
        self.rewards = {('ru_lu', 'ru_lu'): -1000,
                        ('ru_lu', 'ru_li'): -1100,
                        ('ru_lu', 'ru_ld'): 16000,
                        ('ru_lu', 'ri_lu'): -1100,
                        ('ru_lu', 'ri_li'): -1000,
                        ('ru_lu', 'ri_ld'): 15900,
                        ('ru_lu', 'rd_lu'): 16000,
                        ('ru_lu', 'rd_li'): 15900,
                        ('ru_lu', 'rd_ld'): 32000,
                        ('ru_li', 'ru_lu'): -1000,
                        ('ru_li', 'ru_li'): -1100,
                        ('ru_li', 'ru_ld'): 16000,
                        ('ru_li', 'ri_lu'): -1100,
                        ('ru_li', 'ri_li'): -1000,
                        ('ru_li', 'ri_ld'): 15900,
                        ('ru_li', 'rd_lu'): 16000,
                        ('ru_li', 'rd_li'): 15900,
                        ('ru_li', 'rd_ld'): 32000,
                        ('ru_ld', 'ru_lu'): -1000,
                        ('ru_ld', 'ru_li'): -1100,
                        ('ru_ld', 'ru_ld'): -1000,
                        ('ru_ld', 'ri_lu'): -1100,
                        ('ru_ld', 'ri_li'): -1000,
                        ('ru_ld', 'ri_ld'): -1100,
                        ('ru_ld', 'rd_lu'): 16000,
                        ('ru_ld', 'rd_li'): 15900,
                        ('ru_ld', 'rd_ld'): 16000,
                        ('ri_lu', 'ru_lu'): -1000,
                        ('ri_lu', 'ru_li'): -1100,
                        ('ri_lu', 'ru_ld'): 16000,
                        ('ri_lu', 'ri_lu'): -1100,
                        ('ri_lu', 'ri_li'): -1000,
                        ('ri_lu', 'ri_ld'): 15900,
                        ('ri_lu', 'rd_lu'): 16000,
                        ('ri_lu', 'rd_li'): 15900,
                        ('ri_lu', 'rd_ld'): 32000,
                        ('ri_li', 'ru_lu'): -1000,
                        ('ri_li', 'ru_li'): -1100,
                        ('ri_li', 'ru_ld'): 16000,
                        ('ri_li', 'ri_lu'): -1100,
                        ('ri_li', 'ri_li'): -1000,
                        ('ri_li', 'ri_ld'): 15900,
                        ('ri_li', 'rd_lu'): 16000,
                        ('ri_li', 'rd_li'): 15900,
                        ('ri_li', 'rd_ld'): 32000,
                        ('ri_ld', 'ru_lu'): -1000,
                        ('ri_ld', 'ru_li'): -1100,
                        ('ri_ld', 'ru_ld'): -1000,
                        ('ri_ld', 'ri_lu'): -1100,
                        ('ri_ld', 'ri_li'): -1000,
                        ('ri_ld', 'ri_ld'): -1100,
                        ('ri_ld', 'rd_lu'): 16000,
                        ('ri_ld', 'rd_li'): 15900,
                        ('ri_ld', 'rd_ld'): 32000,
                        ('rd_lu', 'ru_lu'): -1000,
                        ('rd_lu', 'ru_li'): -1100,
                        ('rd_lu', 'ru_ld'): 16000,
                        ('rd_lu', 'ri_lu'): -1100,
                        ('rd_lu', 'ri_li'): -1000,
                        ('rd_lu', 'ri_ld'): 15900,
                        ('rd_lu', 'rd_lu'): -1000,
                        ('rd_lu', 'rd_li'): -1100,
                        ('rd_lu', 'rd_ld'): 16000,
                        ('rd_li', 'ru_lu'): 0,
                        ('rd_li', 'ru_li'): -100,
                        ('rd_li', 'ru_ld'): 0,
                        ('rd_li', 'ri_lu'): -100,
                        ('rd_li', 'ri_li'): -1000,
                        ('rd_li', 'ri_ld'): 15900,
                        ('rd_li', 'rd_lu'): -100,
                        ('rd_li', 'rd_li'): -1100,
                        ('rd_li', 'rd_ld'): 16000,
                        ('rd_ld', 'ru_lu'): 1000,
                        ('rd_ld', 'ru_li'): 400,
                        ('rd_ld', 'ru_ld'): 500,
                        ('rd_ld', 'ri_lu'): 400,
                        ('rd_ld', 'ri_li'): -200,
                        ('rd_ld', 'ri_ld'): -100,
                        ('rd_ld', 'rd_lu'): 500,
                        ('rd_ld', 'rd_li'): -200,
                        ('rd_ld', 'rd_ld'): -100}

    @staticmethod
    def wing_gain(w_pos_t, w_pos_t_1):
        if w_pos_t == 0 and w_pos_t_1 == 1:
            return 1000
        elif w_pos_t == 0 and w_pos_t_1 == 0:
            return -100
        elif w_pos_t == 0 and w_pos_t_1 == -1:
            return 1000
        elif w_pos_t == 1 and w_pos_t_1 == 1:
            return -100
        elif w_pos_t == 1 and w_pos_t_1 == 0:
            return -500
        elif w_pos_t == 1 and w_pos_t_1 == -1:
            return 1000
        elif w_pos_t == -1 and w_pos_t_1 == 1:
            return 1000
        elif w_pos_t == -1 and w_pos_t_1 == 0:
            return -500
        elif w_pos_t == -1 and w_pos_t_1 == -1:
            return -100

    @staticmethod
    def get_reward(state, action):
        rt, rt_1 = 0, 0
        lt, lt_1 = 0, 0
        if state[1] == 'u':
            rt = 1
        elif state[1] == 'd':
            rt = -1
        if action[1] == 'u':
            rt_1 = 1
        elif action[1] == 'd':
            rt_1 = -1
        if state[4] == 'u':
            rt = 1
        elif state[4] == 'd':
            rt = -1
        if action[4] == 'u':
            rt_1 = 1
        elif action[4] == 'd':
            rt_1 = -1
        return BirdQLearner.wing_gain(rt, rt_1) + BirdQLearner.wing_gain(lt, lt_1)

    def extract_possible_actions(self, state_key):
        return self.actions

    def observe_reward_value(self, state_key, action_key):
        return self.get_reward(state_key, action_key)

    def visualize_learning_result(self, state_key):
        policy = []
        for i in range(BirdQLearner.POLICY_LEN):
            actions = self.extract_possible_actions(state_key)
            action = self.select_action(state_key, actions)
            rw, lw = 0, 0
            if action[1] == 'u':
                rw = 1
            elif action[1] == 'd':
                rw = -1
            if action[4] == 'u':
                lw = 1
            elif action[4] == 'd':
                lw = -1
            policy.extend([rw, lw])
            state_key = self.update_state(state_key, action)
        return np.array(policy)


if __name__ == '__main__':
    bird_learner = BirdQLearner()
    bird_learner.learn('rd_ld', 10000)
    policy = bird_learner.visualize_learning_result('rd_ld')
    np.save('out/ql.npy', policy)
