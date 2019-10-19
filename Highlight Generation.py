#!/usr/bin/env python
# coding: utf-8

# In[1]:


import librosa 


# In[2]:


filename='powerplay.wav' 


# In[3]:


x, sr = librosa.load(filename,sr=16000)


# In[4]:


int(librosa.get_duration(x, sr)/60)


# In[5]:


max_slice = 5
window_length = max_slice * sr


# In[7]:


import IPython.display as ipd
a = x[21*window_length:22*window_length]
ipd.Audio(a,rate = sr)


# In[8]:


energy = sum(abs(a**2))
print(energy)


# In[12]:


import matplotlib.pyplot as plt
fig = plt.figure(figsize=(14,8))
ax1 = fig.add_subplot(211)
ax1.set_xlabel('time')
ax1.set_ylabel('Amplitude')
ax1.plot(a)


# In[10]:


import numpy as np
energy = np.array([sum(abs(x[i:i+window_length]**2)) for i in range(0, len(x), window_length)])


# In[11]:


plt.hist(energy)
plt.show()


# In[14]:


import pandas as pd
df= pd.DataFrame(columns=['energy','start','end'])
thres = 12000
row_index = 0
for i in range(len(energy)):
    value = energy[i]
    if(value>=thres):
        i=np.where(energy==value)[0]
        df.loc[row_index, 'energy']=value
        df.loc[row_index, 'start'] = i[0]*5
        df.loc[row_index, 'end'] =(i[0]+1)*5
        row_index=row_index+1
        


# In[15]:


temp=[]
i=0
j=0
n=len(df) - 2
m=len(df) - 1
while(i<=n):
  j=i+1
  while(j<=m):
    if(df['end'][i] == df['start'][j]):
      df.loc[i,'end'] = df.loc[j,'end']
      temp.append(j)
      j=j+1
    else:
      i=j
      break  
df.drop(temp,axis=0,inplace=True)


# In[24]:


from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
path =r'C:\Users\rohan\test'


# In[25]:


start=np.array(df['start'])
end=np.array(df['end'])
for i in range(len(df)):
    if(i!=0):
        start_lim = start[i] - 5
    else:
        start_lim = start[i] 
    end_lim   = end[i]   
    filename=r"C:\Users\rohan\test\highlight" + str(i+1) + ".mp4"
    ffmpeg_extract_subclip(path+"\\powerplay.mp4",start_lim,end_lim,targetname=filename)


# In[ ]:




