#!/usr/bin/env python
# coding: utf-8

# # Lesson 1: Simple ReAct Agent from Scratch

# In[1]:


# based on https://til.simonwillison.net/llms/python-react-pattern


# In[2]:


import openai
import re
import httpx
import os
from dotenv import load_dotenv

_ = load_dotenv()
from openai import OpenAI


# In[3]:


client = OpenAI()


# In[4]:


chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello world"}]
)


# In[5]:


chat_completion.choices[0].message.content


# In[6]:


class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.chat.completions.create(
                        model="gpt-4o", 
                        temperature=0,
                        messages=self.messages)
        return completion.choices[0].message.content
    


# In[7]:


prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:

Answer: A bulldog weights 51 lbs
""".strip()


# In[8]:


def calculate(what):
    return eval(what)

def average_dog_weight(name):
    if name in "Scottish Terrier": 
        return("Scottish Terriers average 20 lbs")
    elif name in "Border Collie":
        return("a Border Collies average weight is 37 lbs")
    elif name in "Toy Poodle":
        return("a toy poodles average weight is 7 lbs")
    else:
        return("An average dog weights 50 lbs")

known_actions = {
    "calculate": calculate,
    "average_dog_weight": average_dog_weight
}


# In[9]:


abot = Agent(prompt)


# In[10]:


result = abot("How much does a toy poodle weigh?")
print(result)


# In[11]:


result = average_dog_weight("Toy Poodle")


# In[12]:


result


# In[13]:


next_prompt = "Observation: {}".format(result)


# In[14]:


next_prompt


# In[ ]:


abot(next_prompt)


# In[18]:


abot.messages


# In[19]:


abot = Agent(prompt)


# In[27]:


abot.messages


# In[21]:


question = """I have 2 dogs, a border collie and a scottish terrier. \
What is their combined weight"""
abot(question)


# In[23]:


next_prompt = "Observation: {}".format(average_dog_weight("Border Collie"))
print(next_prompt)


# In[24]:


abot(next_prompt)


# In[25]:


next_prompt = "Observation: {}".format(average_dog_weight("Scottish Terrier"))
print(next_prompt)


# In[26]:


abot(next_prompt)


# In[28]:


next_prompt = "Observation: {}".format(eval("37 + 20"))
print(next_prompt)


# In[29]:


abot(next_prompt)


# In[30]:


abot.messages


# 

# In[ ]:





# ### Add loop 

# In[16]:


action_re = re.compile('^Action: (\w+): (.*)$')   # python regular expression to selection action


# In[17]:


def query(question, max_turns=5):
    i = 0
    bot = Agent(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [
            action_re.match(a) 
            for a in result.split('\n') 
            if action_re.match(a)
        ]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return


# In[18]:


question = """I have 2 dogs, a border collie and a scottish terrier. \
What is their combined weight"""
query(question)


# In[ ]:





# In[ ]:




