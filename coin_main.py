import coin
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np

v=[0.1,0.5,0.1,0.9,0.1]
env=coin.Cointoss(v)
eps=[0.0,0.1,0.2,0.5,0.8]
game_step=list(range(10,310,10))
result={}

for e in eps:
    agent=coin.EpsilonGreedy(epsilon=e)
    means=[]
    for s in game_step:
        env.max_episode_step=s
        rewards=agent.play(env)
        means.append(np.mean(rewards))
    result["epsilon={}".format(e)]=means
result["coin toss count"]=game_step

result=pd.DataFrame(result)
result.set_index("coin toss count",drop=True,inplace=True)
result.plot.line(figsize=(10,5))
plt.show()
