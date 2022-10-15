#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
from bs4 import BeautifulSoup as bts
import pandas as pd


# In[3]:


URL = "https://www.bgr.in/gadgets/mobile-phones/search/"
res=[]  ##save the final result 
no_of_pages=15


# In[4]:


for _ in range(no_of_pages):
    r = requests.get(URL)        ##request is used to  call url and get the content of html page
    ##use the beautifull soup to parse the html page
    soup = bts(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    a=soup.findAll("li",class_='mobile-listing')       ## get all the link of mobile specs  : in fig 1
    #travers over the mobile spec links to scrap the specs     
    for k in a:
        data={}  #save the spec of mobile in it
        ## open the mobile spec link
        url_tmp=k.find('a')['href']
        mob=requests.get(url_tmp)
        mob = bts(mob.content, 'html5lib')   ## parse the html page of mobile spec  : fig 2
        # print(mob)
        info=mob.find_all('span',class_='col-xs-12 col-sm-5 spec-lbl')           ## get the col 1 from spec table
        desc=mob.find_all('span',class_='col-xs-12 col-sm-7 spec-val')           ## get the col 2 from spec table
        name=mob.find('h1',{'itemprop':'name'})                                  
        data['name']=name.get_text()                                             ## get the name of mobile phone
        price=mob.find("span",class_='rsm').get_text()                           ## get the price of that mobile
        
        for k,v in zip(info,desc):
            data[k.get_text()]=v.get_text()
        data['price']=price    
        res.append(data)                             # store the result into list 
    URL=soup.find('a',class_='next pagination')['href']            ## get the url for moving to page 2


# In[8]:


df = pd.DataFrame(res)


# In[9]:


df.info()


# In[10]:


df.fillna('none',inplace=True)


# In[11]:


df


# In[13]:


df.shape


# In[15]:


df['Display Resolution'].unique()


# In[ ]:




