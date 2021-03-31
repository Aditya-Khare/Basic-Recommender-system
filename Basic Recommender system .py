#!/usr/bin/env python
# coding: utf-8

# In[1]:


# In this study I will analyse MIT and Harvard Online Courses data set 
# and create a basic recommendation system based on course category.
# By choosing from the four main course category, system will recommend top 5 rated and popular courses in that category.

# LOADING NECESSARY LIBRARIES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from warnings import filterwarnings
filterwarnings('ignore')

# READING THE DATA SET

data = pd.read_csv('appendix.csv')
df = data.copy()
pd.options.display.max_columns = 23


# In[2]:


# ELIMINATING UNNECESSARY COLUMNS

df = df.drop(columns=['Launch Date', 'Year', 'Honor Code Certificates', '% Certified of > 50% Course Content Accessed',
                      '% Played Video', '% Grade Higher Than Zero', 'Total Course Hours (Thousands)',
                      'Median Hours for Certification'])
df.head()


# In[3]:


# IS THERE ANY NAN VALUE IN THE DATA SET?

df.isnull().sum()


# In[4]:


# DEALING THE NAN DATA

df['Instructors'] = df['Instructors'].fillna('-')


# In[5]:


# ANALYSING THE DATA TYPES

df.info()


# In[6]:


# COURSE SUPPLIERS

sns.countplot(x='Institution', data=df);
df['Institution'].value_counts()


# In[7]:


# AGE DISTRIBUTION FOR ALL OF THE COURSES

df['Median Age'].hist()
plt.title('Age Distribution For All the Courses')
plt.xlabel('Student Ages');


# In[8]:


# ANALYSING THE COURSE CATEGORIES

print(df['Course Subject'].value_counts())
df['Course Subject'].value_counts().plot(kind='barh')
plt.title('Nu of Courses in the Subject Category');


# In[9]:


# INITIAL STATISTICS OF THE COLUMNS

df.describe().T


# In[10]:


# Demographic Recommendation
#1. By Course Weight (Rating)
#Course Weight = ((Nu of Students of the Course/Nu of All Students)*0.60)+(Forum Posts*0.30)+(Aquiered Certifications x 0.10)

# CREATING COURSE WEIGHT COLUMN

df['Weight Avg'] = ((df['Participants (Course Content Accessed)'] / df['Participants (Course Content Accessed)'].sum())*0.60) 
+ (df['% Posted in Forum']*0.30)+(df['% Certified']*0.10)


# ERASING THE DUPLICATED COURSES

df_new = df.drop_duplicates(subset=['Course Number', 'Course Title'], keep=False)


# TOP 10 COURSES BY RATING

df_present1 = df_new[['Course Title', 'Course Subject', 'Participants (Course Content Accessed)', '% Audited', '% Certified', 
                      '% Posted in Forum', 'Weight Avg']].sort_values(by=['Weight Avg'], ascending=False).head(10)


# In[11]:


# 2. By Number of Students
# TOP 1O COURSES BY PARTICIPANTS

df_present2 = df_new[['Course Title', 'Course Subject', 'Participants (Course Content Accessed)', '% Audited', '% Certified', 
                      '% Posted in Forum', 'Weight Avg']].sort_values(by=['Participants (Course Content Accessed)'], 
                                                                      ascending=False).head(10)


# In[12]:


# COMPARISON OF TOP 10 COURSES BY RATING AND POPULARITY

plt.figure(figsize=(8,12))
plt.subplot(2,1,1)
plt.barh(df_present1['Course Title'].head(10), df_present1['Weight Avg'].head(10), color='orange')
plt.gca().invert_yaxis()
plt.title('Top 10 Courses by Rating')
plt.xlabel('Course Rating')

plt.subplot(2,1,2)
plt.barh(df_present2['Course Title'].head(10), df_present2['Participants (Course Content Accessed)'].head(10), color='purple')
plt.gca().invert_yaxis()
plt.title('Top 10 Courses by Number of Students')
plt.xlabel('Number of Students');


# In[13]:


# Category Base Recommendation
# COURSE CATEGORIES

subject_list = list(df_new['Course Subject'].unique())
subject_dict = {'a': subject_list[0], 'b': subject_list[1], 'c': subject_list[2], 'd': subject_list[3]}
# CREATING FUNCTION TO RECOMMEND TOP 5 COURSES BY CATEGORY SELECTION 

print('Course categories: \n')
print('a) ', subject_dict['a'])
print('b) ', subject_dict['b'])
print('c) ', subject_dict['c'])
print('d) ', subject_dict['d'])

def recommend(course_subject):
    
    filter_subject = df_new['Course Subject'] == course_subject
    
    print('\n Top 5 Rated Courses in %a \n' % course_subject)
    df_rated = df_new[filter_subject].sort_values(by=['Weight Avg'], ascending=False).head()
    print(df_rated[['Course Number', 'Course Title']])
    
    print('\nTop 5 Popular Courses in %a \n' % course_subject)
    df_popular = df_new[filter_subject].sort_values(by=['Participants (Course Content Accessed)'], ascending=False).head()
    print(df_popular[['Course Number', 'Course Title']])


# In[14]:


# GOVERNMENT, HEALTH, AND SOCIAL SCIENCE CATEGORY COURSE RECOMMENDATIONS:

recommend(subject_dict['a'])


# In[15]:


# SCIENCE, TECHNOLOGY, ENGINEERING, AND MATHEMATICS CATEGORY COURSE RECOMMENDATIONS:

recommend(subject_dict['b'])


# In[16]:


# HUMANITIES, HISTORY, DESIGN, RELIGION, AND EDUCATION CATEGORY COURSE RECOMMENDATIONS:

recommend(subject_dict['c'])


# In[17]:


# COMPUTER SCIENCE CATEGORY COURSE RECOMMENDATIONS:

recommend(subject_dict['d'])


# In[19]:


# FOR AN INTERACTIVE VERSION WITH USER INPUT USE THE CODE BELOW:

def recommend():
    print('a) ', subject_dict['a'])
    print('b) ', subject_dict['b'])
    print('c) ', subject_dict['c'])
    print('d) ', subject_dict['d'])
    
    print('\nChoose the subject you want to learn: \n')
    user_input = input()
    
    course_subject = subject_dict[user_input]
    
    filter_subject = df_new['Course Subject'] == course_subject
    
    print('\n Top 5 Rated Courses in %a \n' % subject_dict[user_input])
    df_rated = df_new[filter_subject].sort_values(by=['Weight Avg'], ascending=False).head()
    print(df_rated[['Course Number', 'Course Title']])
    
    print('\nTop 5 Popular Courses in %a \n' % subject_dict[user_input])
    df_popular = df_new[filter_subject].sort_values(by=['Participants (Course Content Accessed)'], ascending=False).head()
    print(df_popular[['Course Number', 'Course Title']])
    
    print('\nWould you like to look for a different subject? (y/n)\n')
    restart = input()
    
    if restart == 'y' or restart == 'yes':
        recommend()
    elif restart == 'n' or restart == 'no':
        print('\nGood bye!')
    else:
        print('\nWrong input.')
    return


recommend()


# In[ ]:




