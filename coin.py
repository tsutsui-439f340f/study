import numpy as np
import random

class Cointoss():
    def __init__(self,head_prob,max_episode_step=30):
        self.head_prob=head_prob
        self.max_episode_step=max_episode_step
        self.toss_count=0
    
    def __len__(self):
        return len(self.head_prob)
    
    def reset(self):
        self.toss_count=0
    def step(self,action):
        final=self.max_episode_step-1
        if self.toss_count>final:
            raise Exception("End")
        else:
            done=True if self.toss_count==final else False
        
        if action>=len(self.head_prob):
            raise Exception("Error")
        else:
            head_prob=self.head_prob[action]
            if random.random()<head_prob:
                reward=1.0#確率的にコインを選び確率的に表が出ないと報酬に加算されない
            else:
                reward=0.0
            
            self.toss_count+=1
            return reward,done

class EpsilonGreedy():
    def __init__(self,epsilon):
        self.epsilon=epsilon
        self.V=[]

    def policy(self):
        #期待値が大きいほうが報酬が増える可能性がある。
        #ランダムに選ばれたものよりいいはずである。
        #探索の場合ランダムピック、活用の場合期待値最大のコインをピックする。
        coin=range(len(self.V))
        if random.random()<self.epsilon:
            return random.choice(coin)
        else:
            return np.argmax(self.V)
    
    def play(self,env):
        N=[0]*len(env)
        #Vは期待値初期は0
        self.V=[0]*len(env)
        env.reset()
        done=False
        rewards=[]

        while not done:
            #まずコインを期待値にしたがって選ぶ
            selected_coin=self.policy()
            #選んだコインを使って試行実験
            reward,done=env.step(selected_coin)
            #1回の試行実験の報酬を記録
            rewards.append(reward)
            #選んだコインの今まで出た回数n
            n=N[selected_coin]
            #選んだコインの今までの期待値
            coin_average=self.V[selected_coin]
            #新しい期待値をrewardを加味して計算
            new_average=(coin_average*n+reward)/(n+1)
            #選んだコインの出た回数を+1
            N[selected_coin]+=1
            #新しく期待値を更新
            self.V[selected_coin]=new_average

          
        return rewards



