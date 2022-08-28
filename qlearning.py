from pyqlearning.qlearning.greedy_q_learning import GreedyQLearning
import numpy as np
import argparse
import simulator
OUT_PATH = 'out/ql_'


class BirdQLearner(GreedyQLearning):
    POLICY_LEN = 60
    START_STATE = 'rd_ld'
    ALPHA = 0.01

    def __init__(self, gui, save_process, num_iterations, to_visualize):
        self.states = ['ru_lu',
                       'ru_li',
                       'ru_ld',
                       'ri_lu',
                       'ri_li',
                       'ri_ld',
                       'rd_lu',
                       'rd_li',
                       'rd_ld']
        self.actions = ['ru_lu',
                        'ru_li',
                        'ru_ld',
                        'ri_lu',
                        'ri_li',
                        'ri_ld',
                        'rd_lu',
                        'rd_li',
                        'rd_ld']
        self._gui = gui
        self._save_process = save_process
        self._num_iterations = num_iterations
        self._to_visualize = to_visualize

    @staticmethod
    def get_reward(state, action):
        if action[1] != action[4]:
            return -1
        if state[1] == action[1]:
            return -1
        if action[1] == 'i':
            return -1
        return 2

    def extract_possible_actions(self, state_key):
        return self.actions

    def observe_reward_value(self, state_key, action_key):
        return self.get_reward(state_key, action_key)

    def get_policy(self, state_key):
        policy = []
        for i in range(BirdQLearner.POLICY_LEN):
            actions = self.extract_possible_actions(state_key)
            action = self.predict_next_action(state_key, actions)
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

    def visualize_learning_result(self, state_key):
        if self.t % self._to_visualize == 0:
            policy = self.get_policy(self.START_STATE)
            if self._save_process:
                np.save(f'{OUT_PATH}{self.t}.npy', policy)
            if self._gui:
                bird_sim = simulator.BirdSim()
                bird_sim.run_simulation_offline(policy,gui=True)

    def run_bird_learner(self, alpha=0.005):
        self.alpha_value = alpha
        self.learn(self.START_STATE, self._num_iterations)


def parse_args():
    parser = argparse.ArgumentParser(description='Run QLearning and teach Birdy to fly')
    parser.add_argument('--gui', dest='gui', action='store_true', default=False,
                        help='activate gui')
    parser.add_argument('--save_proc', dest='save_proc', action='store_true', default=False,
                        help='save process')
    parser.add_argument('--num_iterations', metavar='-n', type=int, nargs='?', default=2000,
                        help='how many iteration the QLearner should run')
    parser.add_argument('--to_visualize', metavar='-v', type=int, nargs='?', default=10,
                        help='visualize current policy evey v iterations')
    return parser


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()
    bird_learner = BirdQLearner(args.gui, args.save_proc, args.num_iterations, args.to_visualize)
    bird_learner.run_bird_learner()


