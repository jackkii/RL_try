# migong_envir.py
# -----------------------------------
# 5*5迷宫环境搭建
# -----------------------------------
# 2019/04/30   Jackkii
# 可render出迷宫窗口，显示障碍和机器人
# -----------------------------------
#

import logging
import numpy
import random
import gym
from gym import spaces


logger = logging.getLogger(__name__)

class MiGong(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 2
    }

    def __init__(self):

        self.states = [1, 2, 3, 4,
                       5, 6, 7, 8,
                       9, 10, 11,
                       12, 13, 14, 15, 16,
                       17, 18]

        self.actions = ['n', 'e', 's', 'w']

        self.x = [140, 220, 300,      460,    # 每个状态点机器人的圆心坐标
                  140, 220, 300,      460,
                            300, 380, 460,
                  140, 220, 300, 380, 460,
                  140, 220                ]
        self.y = [550, 550, 550,      550,
                  450, 450, 450,      450,
                            350, 350, 350,
                  250, 250, 250, 250, 250,
                  150, 150              ]

        self.terminate_states = dict();
        self.terminate_states[15] = 1       # 出口

        self.rewards = dict();          # 回报
        self.rewards['10_s'] = 1.0
        self.rewards['20_n'] = 1.0
        self.rewards['14_e'] = 1.0

        self.t = dict();        # 状态转移
        self.t['1_s'] = 5
        self.t['1_e'] = 2
        self.t['2_s'] = 6
        self.t['2_e'] = 3
        self.t['2_w'] = 1
        self.t['3_s'] = 7
        self.t['3_w'] = 2
        self.t['4_s'] = 8
        self.t['5_n'] = 1
        self.t['5_e'] = 6
        self.t['6_n'] = 2
        self.t['6_w'] = 5
        self.t['6_e'] = 7
        self.t['7_n'] = 3
        self.t['7_w'] = 6
        self.t['7_s'] = 9
        self.t['8_n'] = 4
        self.t['8_s'] = 11
        self.t['9_n'] = 7
        self.t['9_s'] = 14
        self.t['9_e'] = 10
        self.t['10_w'] = 9
        self.t['10_s'] = 15
        self.t['10_e'] = 11
        self.t['12_e'] = 13
        self.t['12_s'] = 17
        self.t['13_w'] = 12
        self.t['13_s'] = 18
        self.t['13_e'] = 14
        self.t['14_e'] = 15
        self.t['14_n'] = 9
        self.t['14_w'] = 13
        self.t['15_e'] = 16
        self.t['15_n'] = 10
        self.t['15_w'] = 14
        self.t['16_w'] = 15
        self.t['16_n'] = 11
        self.t['17_e'] = 18
        self.t['17_n'] = 12
        self.t['18_w'] = 17
        self.t['18_n'] = 13

        self.gamma = 0.8  # 折扣因子
        self.viewer = None  # ？
        self.state = None  # 当前状态

    def getTerminal(self):
        return self.terminate_states

    def getGamma(self):
        return self.gamma

    def getStates(self):
        return self.states

    def getAction(self):
        return self.actions

    def getTerminate_states(self):
        return self.terminate_states

    def setAction(self, s):
        self.state = s

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        # 系统当前状态
        state = self.state
        if state in self.terminate_states:
            return state, 0, True, {}
        key = '%d_%s' % (state, action)     # 状态和动作组成状态动作对

        if key in self.t:
            next_state = self.t[key]
        else:
            next_state = state
        self.state = next_state

        is_terminal = False

        if next_state in self.terminate_states:
            is_terminal = True

        if key not in self.rewards:
            r = 0.0
        else:
            r = self.rewards[key]

        return next_state, r, is_terminal, {}

    def _reset(self):
        self.state = self.states[int(random.random() * len(self.states))]
        return self.state

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewwe.close()
                self.viewer = None
            return
        screen_width = 600
        screen_height = 700

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)

            self.line1 = rendering.Line((100, 600), (500, 600))
            self.line2 = rendering.Line((100, 500), (500, 500))
            self.line3 = rendering.Line((100, 400), (500, 400))
            self.line4 = rendering.Line((100, 300), (500, 300))
            self.line5 = rendering.Line((100, 200), (500, 200))
            self.line6 = rendering.Line((100, 100), (500, 100))
            self.line7 = rendering.Line((100, 600), (100, 100))
            self.line8 = rendering.Line((180, 600), (180, 100))
            self.line9 = rendering.Line((260, 600), (260, 100))
            self.line10 = rendering.Line((340, 600), (340, 100))
            self.line11 = rendering.Line((420, 600), (420, 100))
            self.line12 = rendering.Line((500, 600), (500, 100))

            self.line1.set_color(0, 0, 0)
            self.line2.set_color(0, 0, 0)
            self.line3.set_color(0, 0, 0)
            self.line4.set_color(0, 0, 0)
            self.line5.set_color(0, 0, 0)
            self.line6.set_color(0, 0, 0)
            self.line7.set_color(0, 0, 0)
            self.line8.set_color(0, 0, 0)
            self.line9.set_color(0, 0, 0)
            self.line10.set_color(0, 0, 0)
            self.line11.set_color(0, 0, 0)
            self.line12.set_color(0, 0, 0)

            self.viewer.add_geom(self.line1)  # 将创建的对象添加到几何中
            self.viewer.add_geom(self.line2)
            self.viewer.add_geom(self.line3)
            self.viewer.add_geom(self.line4)
            self.viewer.add_geom(self.line5)
            self.viewer.add_geom(self.line6)
            self.viewer.add_geom(self.line7)
            self.viewer.add_geom(self.line8)
            self.viewer.add_geom(self.line9)
            self.viewer.add_geom(self.line10)
            self.viewer.add_geom(self.line11)
            self.viewer.add_geom(self.line12)

            #创建遮挡区
            self.mukuai1 = rendering.make_circle(40)
            capsule_transform = rendering.Transform(translation=(380, 550))
            self.mukuai1.add_attr(capsule_transform)
            self.mukuai1.set_color(0, 0, 0)
            self.viewer.add_geom(self.mukuai1)

            self.mukuai2 = rendering.make_circle(40)
            capsule_transform = rendering.Transform(translation=(380, 450))
            self.mukuai2.add_attr(capsule_transform)
            self.mukuai2.set_color(0, 0, 0)
            self.viewer.add_geom(self.mukuai2)

            self.mukuai3 = rendering.make_circle(40)
            capsule_transform = rendering.Transform(translation=(140, 350))
            self.mukuai3.add_attr(capsule_transform)
            self.mukuai3.set_color(0, 0, 0)
            self.viewer.add_geom(self.mukuai3)

            self.mukuai4 = rendering.make_circle(40)
            capsule_transform = rendering.Transform(translation=(220, 350))
            self.mukuai4.add_attr(capsule_transform)
            self.mukuai4.set_color(0, 0, 0)
            self.viewer.add_geom(self.mukuai4)

            self.mukuai5 = rendering.make_circle(40)
            capsule_transform = rendering.Transform(translation=(300, 150))
            self.mukuai5.add_attr(capsule_transform)
            self.mukuai5.set_color(0, 0, 0)
            self.viewer.add_geom(self.mukuai5)

            self.mukuai6 = rendering.make_circle(40)
            capsule_transform = rendering.Transform(translation=(380, 150))
            self.mukuai6.add_attr(capsule_transform)
            self.mukuai6.set_color(0, 0, 0)
            self.viewer.add_geom(self.mukuai6)

            self.mukuai7 = rendering.make_circle(40)
            capsule_transform = rendering.Transform(translation=(460, 150))
            self.mukuai7.add_attr(capsule_transform)
            self.mukuai7.set_color(0, 0, 0)
            self.viewer.add_geom(self.mukuai7)

            self.robot = rendering.make_circle(30)
            self.robotrans = rendering.Transform()
            self.robot.add_attr(self.robotrans)
            self.robot.set_color(0.8, 0.6, 0.4)
            self.viewer.add_geom(self.robot)

        if self.state is None:
            return None
        self.robotrans.set_translation(self.x[self.state-1], self.y[self.state-1])

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')
