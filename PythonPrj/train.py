#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

import os
import numpy as np

import parl
from parl import layers
from paddle import fluid
from parl.utils import logger
from parl.utils import action_mapping  # 将神经网络输出映射到对应的 实际动作取值范围内
from parl.utils import ReplayMemory  # 经验回放
import Logger
from HFSS_Gym import HFSS_env  # 创建HFSS环境
from HFSS_model import HFSS_Model
from HFSS_agent import HFSS_Agent
from parl.algorithms import DDPG

fmt = '%(asctime)s - %(levelname)s: %(message)s'
#log = Logger.Logger('recordings.log',level='info',fmt=fmt)

os.environ['CUDA_VISIBLE_DEVICES']=''

GAMMA = 0.99  # reward 的衰减因子，一般取 0.9 到 0.999 不等
TAU = 0.001  # target_model 跟 model 同步参数 的 软更新参数
ACTOR_LR = 0.0002  # Actor网络更新的 learning rate
CRITIC_LR = 0.001  # Critic网络更新的 learning rate
MEMORY_SIZE = 1e6  # replay memory的大小，越大越占用内存
MEMORY_WARMUP_SIZE = 1e3  # replay_memory 里需要预存一些经验数据，再从里面sample一个batch的经验让agent去learn
REWARD_SCALE = 0.1  # reward 的缩放因子
BATCH_SIZE = 256  # 每次给agent learn的数据数量，从replay memory随机里sample一批数据出来
TRAIN_TOTAL_STEPS = 1e5  # 总训练步数
TEST_EVERY_STEPS = 500  # 每个N步评估一下算法效果，每次评估5个episode求平均reward
NOISE=0.05 # 随机噪声标准差
WAVE_LENGTH=689.66 # 435MHz真空波长

def run_episode(env, agent, rpm):
    obs = env.reset()
    total_reward, steps = 0, 0
    while True:
        steps += 1
        batch_obs = np.expand_dims(obs, axis=0)
        action = agent.predict(batch_obs.astype('float32'))
        action = np.squeeze(action)

        # Add exploration noise, and clip to [-1.0, 1.0]
        action = np.random.normal(action, NOISE)
        #action = action_mapping(action, env.action_space.low[0],
        #                        env.action_space.high[0])
        if steps>50: #尺寸更新了50轮，开始仿真
            next_obs, reward, done = env.step(action,en_sim=True)
        else:
            next_obs, reward, done = env.step(action, en_sim=False)

        rpm.append(obs, action, REWARD_SCALE * reward, next_obs, done)

        if rpm.size() > MEMORY_WARMUP_SIZE:
            batch_obs, batch_action, batch_reward, batch_next_obs, \
                    batch_terminal = rpm.sample_batch(BATCH_SIZE)
            critic_cost = agent.learn(batch_obs, batch_action, batch_reward,
                                      batch_next_obs, batch_terminal)
        obs = next_obs
        total_reward += reward

        if done:
            break

    return total_reward, steps


# 评估 agent, 跑 1 个episode，总reward求平均
def evaluate(env, agent, render=True):
    #log.logger.info('evaluating')
    eval_reward = []
    for i in range(1):
        obs = env.reset()
        total_reward, steps = 0, 0
        while True:
            steps += 1
            batch_obs = np.expand_dims(obs, axis=0)
            action = agent.predict(batch_obs.astype('float32'))
            action = np.squeeze(action)
            #action = np.clip(action, -1.0, 1.0)  ## special
            #action = action_mapping(action, env.action_space.low[0],
            #                        env.action_space.high[0])
            # action = np.clip(action, -1.0, 1.0) ## special

            if steps > 50:  # 尺寸更新了50轮，开始仿真
                next_obs, reward, done = env.step(action, en_sim=True)
            else:
                next_obs, reward, done = env.step(action, en_sim=False)
            obs = next_obs
            total_reward += reward

            if render:
                env.render()

            if done:
                break
        eval_reward.append(total_reward)
    return np.mean(eval_reward)


# 创建HFSS模型环境
env = HFSS_env()
env.reset()
obs_dim = len(env.state)
act_dim = len(env.ofst_rtos)

# 使用parl框架搭建Agent：HFSS_Model, DDPG, HFSS_Agent三者嵌套
model = HFSS_Model(act_dim)
algorithm = DDPG(
    model, gamma=GAMMA, tau=TAU, actor_lr=ACTOR_LR, critic_lr=CRITIC_LR)
agent = HFSS_Agent(algorithm, obs_dim, act_dim)

# parl库也为DDPG算法内置了ReplayMemory，可直接从 parl.utils 引入使用
rpm = ReplayMemory(int(MEMORY_SIZE), obs_dim, act_dim)

test_flag = 0
total_steps = 0
while total_steps < TRAIN_TOTAL_STEPS:
    train_reward, steps = run_episode(env, agent, rpm)
    total_steps += steps
    #logger.info('Steps: {} Reward: {}'.format(total_steps, train_reward))
    env.render()
    if total_steps // TEST_EVERY_STEPS >= test_flag:
        while total_steps // TEST_EVERY_STEPS >= test_flag:
            test_flag += 1

        evaluate_reward = evaluate(env, agent)
        logger.info('Steps {}, Test reward: {}'.format(total_steps,
                                                       evaluate_reward))

        # 保存模型
        ckpt = 'steps_{}.ckpt'.format(total_steps)
        agent.save(ckpt)
