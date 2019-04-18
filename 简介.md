## 强化学习
应用：非线性控制，下棋，机器人，视频游戏，人机对话，无人驾驶，机器翻译，文本序列预测等  
解决序贯决策问题：需要连续不断做出决策以实现最终目标的问题  

分类：  
1.(1)基于模型的强化学习算法：利用与环境交互得到的数据学习系统或环境模型，再基于模型进行序贯决策  
  (2)无模型强化学习：直接利用与环境交互得到的数据改善自身的行为  
2.(1)基于值函数的强化学习算法：学习值函数，最终策略依据值函数贪婪得到  
  (2)基于直接策略搜索的强化学习算法：将策略参数化，学习实现目标的最优参数  
  (3)基于AC方法：联合使用值函数和直接策略搜索  
3.(1)正向强化学习：回报函数已知  
  (2)逆向强化学习：回报函数未知  

问题难度提升：  
1.若状态<a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_T" title="S_T" /></a>有限，但数量巨大，如何降低动态规划算法计算成本  
2.若状态<a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_T" title="S_T" /></a>无限，动态规划算法失效，如何改进算法  
3.若状态<a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_T" title="S_T" /></a>无限，且取值连续，如何改进算法  
4.若状态<a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_T" title="S_T" /></a>只能被部分观察到，剩余部分被遮挡或缺失，如何改进算法  
5.若状态<a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_T" title="S_T" /></a>完全不能被观察到，只能通过其他现象猜测潜在状态，如何改进算法  
