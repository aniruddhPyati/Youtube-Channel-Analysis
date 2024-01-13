#!/usr/bin/env python
# coding: utf-8

# ## Youtube Channel Analytics

# In[1]:


get_ipython().system('pip install google-api-python-client')


# In[2]:


get_ipython().system('pip install pandas')


# In[3]:


get_ipython().system('pip install seaborn')


# In[4]:


from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns


# In[5]:


channel_ids=['UCMiJRAwDNSNzuYeN2uWa0pA','UCBJycsmduvYEL83R_U4JriQ','UCsTcErHg8oDvUnTzoqsYeNw']
api_key='AIzaSyCKbErZw7NM0Jpdk3lrijCxeSwORFX3Hqg'
api_service_name="youtube"
api_version="v3"
youtube= build(api_service_name,api_version,developerKey=api_key)


# In[6]:


def get_channel_details(youtube, channel_ids):
    final_data=[]
    request=youtube.channels().list(part='snippet,contentDetails,statistics',id=','.join(channel_ids))
    response= request.execute()
    
    for i in range(len(response['items'])):
        
        data= dict(Channel_name = response['items'][i]['snippet']['title'] ,
               Subscribers = response['items'][i]['statistics']['subscriberCount'],
               Views=response['items'][i]['statistics']['viewCount'],
               Total_videos= response['items'][i]['statistics']['videoCount'],
               playlist_id =response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        final_data.append(data)
    return final_data


# In[7]:


channel_stats= get_channel_details(youtube,channel_ids)


# In[8]:


request=youtube.channels().list(part='snippet,contentDetails,statistics',id=','.join(channel_ids))
response= request.execute()
for i in range(len(response['items'])):
        
        data= dict(Channel_name = response['items'][i]['snippet']['title'] ,
               Subscribers = response['items'][i]['statistics']['subscriberCount'],
               Views=response['items'][i]['statistics']['viewCount'],
               Total_videos= response['items'][i]['statistics']['videoCount'],
               playlist_id =response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
data


# In[9]:


channel_df=pd.DataFrame(channel_stats)


# In[10]:


channel_df


# In[11]:


channel_df['Subscribers']=pd.to_numeric(channel_df['Subscribers'])
channel_df['Views']=pd.to_numeric(channel_df['Views'])
channel_df['Total_videos']=pd.to_numeric(channel_df['Total_videos'])


# In[12]:


channel_df.dtypes


# In[13]:


sns.set(rc={'figure.figsize':(10,8)})
ax=sns.barplot(x='Channel_name',y='Subscribers',data=channel_df)


# In[14]:


ax=sns.barplot(x='Channel_name',y='Views',data=channel_df)


# In[15]:


ax=sns.barplot(x='Channel_name',y='Total_videos',data=channel_df)


# In[16]:


channel_df


# In[17]:


playlist_id =channel_df.loc[channel_df['Channel_name']=='Marques Brownlee','playlist_id'].iloc[0]


# In[18]:


def get_video_ids(youtube,playlist_id):
    
    request=youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50)
    response=request.execute()
    
    
    video_ids=[]
    
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
    
    next_page_token=response.get('nextPageToken')
    more_pages=True
    
    while more_pages:
        if next_page_token is None:
            more_pages=False
        else:
            request=youtube.playlistItems().list(
                      part='contentDetails',
                      playlistId=playlist_id,
                      maxResults=50,
                      pageToken=next_page_token)
            response=request.execute()
            
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            next_page_token=response.get('nextPageToken')   
            
    return video_ids
    


# In[35]:


request=youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50)
response=request.execute()
response


# In[37]:


idtuple=[]
for i in response['items']:
    viddict=(i['contentDetails']['videoId'])
    
    idtuple.append(viddict)
idtuple
    


# In[19]:


video_ids=get_video_ids(youtube,playlist_id)
video_ids


# In[20]:


def get_video_details(youtube,video_ids):
    all_video_stats=[]
    
    for i in range(0,len(video_ids),50):
        request=youtube.videos().list(
                part='snippet,statistics',
                id =','.join(video_ids[i:i+50]))
        response=request.execute()
        
        for video in response['items']:
            video_stats=dict(Title=video['snippet']['title'],
                             Views=video['statistics'].get('viewCount'),
                             Likes=video['statistics'].get('likeCount'),
                             Comments=video['statistics'].get('commentCount'))
            
            all_video_stats.append(video_stats)
        
       
    return all_video_stats
    


# In[33]:


for i in range(0,len(video_ids),50):
        request=youtube.videos().list(
                part='snippet,statistics',
                id =','.join(video_ids[i:i+50]))
        response=request.execute()
response


# In[ ]:


get_video_details(youtube,video_ids)


# In[22]:


video_details=get_video_details(youtube,video_ids)
video_data=pd.DataFrame(video_details)
video_data


# In[23]:


video_data['Views']=pd.to_numeric(video_data['Views'])
video_data['Likes']=pd.to_numeric(video_data['Likes'])
video_data['Comments']=pd.to_numeric(video_data['Comments'])


# In[24]:


video_data


# In[25]:


top_10_videos=video_data.sort_values(by='Views',ascending=False).head(10)


# In[26]:


top_10_videos


# In[27]:


ax1=sns.barplot(x='Views',y='Title',data=top_10_videos)
ax1


# In[28]:


top_100_videos=video_data.sort_values(by='Likes',ascending=False).head(100)
top_100_videos


# In[29]:


top_10_videos=video_data.sort_values(by='Likes',ascending=False).head(10)


# In[30]:


top_10_videos


# In[31]:


sns.scatterplot(x=top_10_videos.Views,y=top_10_videos.Likes,s=200)


# In[ ]:




