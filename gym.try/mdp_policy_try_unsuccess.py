# 尝试使用策略迭代和值迭代算法
# 算法代码并未运行过，不全
# 从190行开始

import logging
import numpy
import random
from gym import spaces
import gym

logger = logging.getLogger(__name__)


class GridEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],  #？
        'video.frames_per_second': 2
    }

    def __init__(self):

        self.states = [1, 2, 3, 4, 5, 6, 7, 8]      # 状态空间
        self.actions = ['n', 'e', 's', 'w']         # 动作空间
        self.x=[140,220,300,380,460,140,300,460]        # 每个状态点机器人位置的中心坐标
        self.y=[250,250,250,250,250,150,150,150]

        self.terminate_states = dict()  # 终止状态为字典格式
        self.terminate_states[6] = 1    # 死亡
        self.terminate_states[7] = 1    # 金币
        self.terminate_states[8] = 1    # 死亡

        self.rewards = dict();        # 回报的数据结构为字典
        self.rewards['1_s'] = -1.0    # 死亡 （状态1向南移动即死亡）
        self.rewards['3_s'] = 1.0     # 金币
        self.rewards['5_s'] = -1.0    # 死亡

        self.t = dict();             # 状态转移的数据格式为字典，此为状态转移概率P
        self.t['1_s'] = 6            # 列举出所有可能状态转移
        self.t['1_e'] = 2
        self.t['2_w'] = 1
        self.t['2_e'] = 3
        self.t['3_s'] = 7
        self.t['3_w'] = 2
        self.t['3_e'] = 4
        self.t['4_w'] = 3
        self.t['4_e'] = 5
        self.t['5_s'] = 8
        self.t['5_w'] = 4

        self.gamma = 0.8         # 折扣因子
        self.viewer = None       # ？
        self.state = None        # 当前状态

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

    def _step(self, action):        # 输入动作，输出下一时刻动作，回报，是否终止，调试信息
        # 系统当前状态
        state = self.state
        if state in self.terminate_states:  # 判断系统是否终止
            return state, 0, True, {}
        key = "%d_%s" % (state, action)   # 将状态和动作组成字典的键值

        # 状态转移
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

    def _reset(self):       # 随机初始化机器人状态
        self.state = self.states[int(random.random() * len(self.states))]
        return self.state

    def _render(self, mode='human', close=False):       # 重绘环境的一帧，默认弹出一个窗口
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        screen_width = 600
        screen_height = 400

        if self.viewer is None:
            from gym.envs.classic_control import rendering      # 导入rendering模块中的画图函数进行绘制
            self.viewer = rendering.Viewer(screen_width, screen_height)     # 绘制600*400的窗口
            # 创建网格世界
            self.line1 = rendering.Line((100,300),(500,300))
            self.line2 = rendering.Line((100, 200), (500, 200))
            self.line3 = rendering.Line((100, 300), (100, 100))
            self.line4 = rendering.Line((180, 300), (180, 100))
            self.line5 = rendering.Line((260, 300), (260, 100))
            self.line6 = rendering.Line((340, 300), (340, 100))
            self.line7 = rendering.Line((420, 300), (420, 100))
            self.line8 = rendering.Line((500, 300), (500, 100))
            self.line9 = rendering.Line((100, 100), (180, 100))
            self.line10 = rendering.Line((260, 100), (340, 100))
            self.line11 = rendering.Line((420, 100), (500, 100))
            # 创建第一个骷髅
            self.kulo1 = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(140, 150))
            self.kulo1.add_attr(self.circletrans)
            self.kulo1.set_color(0, 0, 0)
            # 创建第二个骷髅
            self.kulo2 = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(460, 150))
            self.kulo2.add_attr(self.circletrans)
            self.kulo2.set_color(0, 0, 0)
            # 创建金币
            self.gold = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(300, 150))
            self.gold.add_attr(self.circletrans)
            self.gold.set_color(1, 0.9, 0)
            # 创建机器人
            self.robot= rendering.make_circle(30)
            self.robotrans = rendering.Transform()
            self.robot.add_attr(self.robotrans)
            self.robot.set_color(0.8, 0.6, 0.4)

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

            self.viewer.add_geom(self.line1)        # 将创建的对象添加到几何中
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
            self.viewer.add_geom(self.kulo1)
            self.viewer.add_geom(self.kulo2)
            self.viewer.add_geom(self.gold)
            self.viewer.add_geom(self.robot)

        if self.state is None:
            return None
        self.robotrans.set_translation(self.x[self.state-1], self.y[self.state-1])   # 设置机器人当前圆心坐标

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')






    def policy_iterate(self, grid_mdp):         # 策略迭代算法
        for i in range(100):
            self.policy_evaluate(grid_mdp);
            self.policy_impove(grid_mdp);

    def policy_evaluate(self, grid_mdp):        # 策略评估算法
        for i in range(1000):                   # 保证值函数收敛到该策略所对应的真实值函数
            delta = 0.0
            for state in grid_mdp.states:       # 整个状态空间的扫描，保证状态空间每一点的值函数都得到估计
                if state in grid_mdp.terminal_states:
                    continue
                action = self.pi[state]
                t, r, s = grid_mdp.transform(state, action)
                new_v = r + grid_mdp.gamma *self.v[s]    # 由于模型已知，可以仅利用模型就可以预测下一个状态，无需实际采取动作
                delta += abs(self.v[s] - new_v)
                self.v[state] = new_v
            if delta < 1e-6:
                break

    def policy_impove(self, grid_mdp):          # 策略改善算法（贪婪策略,求max)
        for state in grid_mdp.states:           # 遍历整个状态空间
            if state in grid_mdp.terminal_states:
                continue
            al = grid_mdp.actions[0]
            t, s, r = grid_mdp.transform(state, al)
            vl = r + grid_mdp.gamma * self.v[s]
            for action in grid_mdp.actions:         # 对每个状态对应的动作空间进行遍历
                t, s, r = grid_mdp.transform(state, action)
                if vl < r + grid_mdp.gamma * self.v[s]:
                    al = action
                    vl = r +grid_mdp.gamma *self.v[s]
            self.pi[state] = al

    def value_iteration(self, grid_mdp):        # 值迭代算法（需三重循环）
        for i in range(1000):                   # 第一重循环保证值函数收敛
            delta = 0.0
            for state in grid_mdp.states:       # 第二重循环遍历整个状态空间
                if state in grid_mdp.terminal_states:
                    continue
                al = grid_mdp.actions[0]
                t, s, r =grid_mdp.transfoem(state, al)
                vl = r + grid_mdp.gamma * self.v[s]

                for action in grid_mdp.actions:     # 第三重循环遍历整个动作空间选取最优动作
                    t, s, r = grid_mdp.transfoem(state, action)
                    if vl < r +grid_mdp.gamma *self.v[s]:
                        al = action
                        vl = r + grid_mdp.gamma * self.v[s]
                delta += abs(vl - self.v[state])
                self.pi[state] = al
                self.v[state] = vl
            if delta < 1e-6:
                break
                
    def gen_randompi_sample(self, num):             # 产生样本的采样过程
        state_sample = []
        action_sample = []
        reward_sample = []
        for i in range(num):                        # 采样多个样本序列，每个样本序列包括状态序列，动作序列和回报序列
            s_tmp = []
            a_tmp = []
            r_tmp = []
            s = self.states[int(random.random() * len(self.states))]
            t = False
            while t is False:   # 产生一个具体的状态序列, 每个样本序列的初始状态是随机的
                a = self.actions[int(random.random() * len(self.actions))]  # 评估随机均匀分布的策略，所以采样时动作随机产生
                t, s1, r = self.transform(s, a)
                s_tmp.append(s)
                r_tmp.append(r)
                a_tmp.append(a)
                s = s1
            state_sample.append(s_tmp)      # 该样本包含多个状态序列
            reward_sample.append(r_tmp)
            action_sample.append(a_tmp)
        return state_sample, action_sample, reward_sample

    def mc(self, gamma, state_sample, action_sample, reward_sample):        # 蒙特卡洛评估
        vfunc = dict()
        nfunc = dict()
        for s in self.states:
            vfunc[s] = 0.0
            nfunc[s] = 0.0
            for iter1 in range(len(state_sample)):
                G = 0.0
                for step in range(len(state_sample[iter1])-1, -1, -1):  # 逆向计算初始状态的累积回报, step递减
                    G *= gamma                                          # Gt=R_(t+1)+gm*G_(t+1)
                    G += reward_sample[iter1][step]                     # 先计算出初始状态G才可计算整个状态序列的回报
                for step in range(len(state_sample[iter1])):                # 正向计算每个状态处的累积回报
                    s = state_sample[iter1][step]                           # G_(t+1)=(Gt-R_(t+1))/gm
                    vfunc[s] += G
                    nfunc[s] += 1.0
                    G -= reward_sample[iter1][step]
                    G /= gamma

            for s in self.states:           # 每个状态处求经验平均
                if nfunc[s] > 0.000001:     # 每次访问蒙特卡罗方法
                    vfunc[s] /= nfunc[s]
            print('mc')
            print(vfunc)
            return(vfunc)

    def MC_complete(self, num_iter1, epsilon):              # 完整版蒙特卡罗方法，不懂
        x = []
        y = []
        n = dict()
        qfunc = dict()
        for s in self.states:
            for a in self.actions:
                qfunc['%d_%s' %(s, a)] = 0.0
                n['%d_%s' %(s, a)] = 0.001
        for iter1 in range(num_iter1):
            x.append(iter1)
            y.append(compute_error(qfunc))
            s_sample = []
            a_sample = []
            r_sample = []
            s = self.states[int(random.random()*len(self.states))]
            t = False
            count = 0
            while t is False and count < 100:
                a = epsilon_greedy(qfunc, s, epsilon)
                t, s1, r = self.tranform(s, a)
                s_sample.append(s)
                a_sample.append(a)
                r_sample.append(r)
                s = s1
                count += 1 
                g = 0.0

                for i in range(len(s_sample)-1, -1, -1):
                    g *= self.gamma
                    g += r_sample[r]
                for i in range(len(s_sample)):
                    key = '%d_%s' %(s_sample[i], a_sample[i])
                    n[key] += 1.0
                    qfunc[key] =(qfunc[key]*(n[key]-1)+g)/n[key]    # 取平均
                    g -= r_sample[i]
                    g /= self.gamma
            return qfunc










