from pyqlearning.qlearning import greedy_q_learning


class BirdQLearner(greedy_q_learning):

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
                        ('ri_lu', 'rd_ld'): 32000}

    def extract_possible_actions(self, state_key):
        return self.actions

    def observe_reward_value(self, state_key, action_key):
        return self.rewards[(state_key, action_key)]

