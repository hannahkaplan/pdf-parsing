#!/usr/bin/env python
# coding: utf-8

# # Parsing PDFs Homework
# 
# With the power of pdfminer, pytesseract, Camelot, and Tika, let's analyze some documents!
# 
# > If at any point you think, **"I'm close enough, I'd just edit the rest of it in Excel"**: that's fine! Just make a note of it.
# 
# ## A trick to use again and again
# 
# ### Approach 1
# 
# Before we get started: when you want to take the first row of your data and set it as the header, use this trick.

# In[984]:


df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[ ]:


# Set the first column as the columns
df.columns = df.loc[0]

# Drop the first row
df = df.drop(0)

df


# 🚀 Done!
# 
# ### Approach 2
# 
# Another alternative is to use `.rename` on your columns and just filter out the columns you aren't interested in. This can be useful if the column name shows up multiple times in your data for some reason or another.

# In[ ]:


# Starting with the same-ish data...
df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'fruit name', 'likes' ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[ ]:


df = df.rename(columns={
    0: 'fruit name',
    1: 'likes'
})
df = df[df['fruit name'] != 'fruit name']
df


# In[ ]:





# In[92]:


import requests
import pandas as pd
import tika
from tika import parser
import camelot
import tika
from tika import parser
import matplotlib.pyplot as plt
import numpy as np 


# 🚀 Done!
# 
# ### Useful tips about coordinates
# 
# If you want to grab only a section of the page [Kull](https://jsoma.github.io/kull/#/) might be helpful in finding the coordinates.
# 
# > **Alternatively** run `%matplotlib notebook` in a cell. Afterwards, every time you use something like `camelot.plot(tables[0]).show()` it will get you nice zoomable, hoverable versions that include `x` and `y` coordinates as you move your mouse.
# 
# Coordinates are given as `"left_x,top_y,right_x,bottom_y"` with `(0,0)` being in the bottom left-hand corner.
# 
# Note that all coordinates are strings, for some reason. It won't be `[1, 2, 3, 4]` it will be `['1,2,3,4']`
# 
# # The homework
# 
# This is **mostly Camelot work**, because I don't really have any good image-based PDFs to stretch your wings on tesseract. If you know of any, let me know and I can put together another couple exercises.
# 
# ## Prison Inmates
# 
# Working from [InmateList.pdf](InmateList.pdf), save a CSV file that includes every inmate.
# 
# * Make sure your rows are *all data*, and you don't have any people named "Inmate Name."
# 

# In[217]:


#import pdf
tables = camelot.read_pdf("InmateList.pdf")


# In[367]:


tables


# In[435]:


#adding stream and pages
tables = camelot.read_pdf("InmateList.pdf", flavor='stream', pages= "1 -16")


# In[746]:


#checking to see what i'm working with
tables[1].df


# In[780]:


#looping through and adding all tables/pages
dfs = [table.df for table in tables]


# In[781]:


#renaming it as df.
df = pd.concat(dfs, ignore_index=True)


# In[782]:


df


# In[783]:


#now that all pages have merged, I am going to rename columns
df = df.rename(columns={
    0: 'INC',
    1: 'name',
    2: 'facility',
    3: 'booking'
})
df


# In[784]:


#Dropping the first few rows as they are headers from PDF.
df = df.drop(labels=[0,1,2], axis=0)
df


# In[785]:


#also dropping the last empy column
df = df.drop(labels= df.columns[5], axis=1) 


# In[786]:


df


# In[787]:


#I noticed these words appeared in table, so i removed them
df['name'] = df["name"].str.strip("Inmate Name, Wednesday,July 14,2021, At:").str.strip()


# In[776]:


df


# In[789]:


#filtered the data and renamed variable
filtered_data = df.dropna(axis='rows', how='all')


# In[790]:


filtered_data


# In[791]:


#saved as CSV
filtered_data.name.to_csv("inmates_names.csv")


# In[ ]:





# ## WHO resolutions
# 
# Using [A74_R13-en.pdf](A74_R13-en.pdf), what ten member countries are given the highest assessments?
# 
# * You might need to have two separate queries, and combine the results: that last page is pretty awful!
# * Always rename your columns
# * Double-check that your sorting looks right......
# * You can still get the answer even without perfectly clean data

# In[898]:


#imported WHO pdf.
data = camelot.read_pdf("A74_R13-en.pdf")


# In[899]:


#adding in flavor and pages.
data = camelot.read_pdf("A74_R13-en.pdf", flavor='stream', pages= "1-5")


# In[900]:


data[0].df


# In[901]:


#looping through to make sure all pages are inlcuded
df5 = [data.df for data in data]


# In[902]:


#renaming variable.
merged = pd.concat(df5, ignore_index=True)


# In[514]:


merged


# In[904]:


#renaming columns
merged = merged.rename(columns={
    merged.columns[0]: 'Members',
    merged.columns[1]: 'Scale',
})
merged


# In[905]:


#I am trying to drop these column headers that appear in table. not sure its working..
merged = merged[merged["Members"].str.contains("Members and Associate Members")==False]
merged = merged[merged["Scale"].str.contains("WHO scale for 2022-2023")==False]


# In[863]:


#checking
merged.head(30)


# In[907]:


#triple checking that when i sort a different way, text isn't appearing, but sadly it is :(
merged.sort_values("Scale", ascending=False)


# In[908]:


#split up text differently to remove
mem_remove_list = ['Associate Members','Members and',""]


# In[909]:


scale_remove_list = ["WHO scale","for 2022-2023", "%"]


# In[910]:


#created a new variable
new_merg= merged[~merged['Members'].isin(mem_remove_list)]


# In[911]:


#checking
new_merg


# In[912]:


#to be able to see more rows.
pd.set_option("display.max_rows", None, "display.max_columns", None)


# In[913]:


new_merg


# In[983]:


new_merg.sort_values("Scale",ascending=False).head(10)


# In[914]:


data1 = camelot.read_pdf("A74_R13-en.pdf", flavor='stream', pages= "6")


# In[921]:


df_new = data1[0].df
df_new


# In[885]:


camelot.plot(data1[0], kind='text')
plt.show()


# In[985]:


df_new = pd.DataFrame([
    [ 'Members', 'Scale' ],
    [ 'Zambia', 0.0090 ],
    [ 'Zimbabwe', 0.0050 ],
])
df_new


# In[999]:


df_new = df_new.drop(labels=[0], axis=0)
df_new


# In[1000]:


df_new = df_new.rename(columns={
    df_new.columns[0]: 'Members',
    df_new.columns[1]: 'Scale'
})
df_new


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# AVENGERS - lines from captain america, thor and iron man
# 

# In[453]:


#using pdfminer to look through text pdf 
from pdfminer.high_level import extract_text


# In[454]:


#importing Avengers 
text = extract_text('THE_AVENGERS.pdf')


# In[455]:


print(text)


# In[625]:


#how many lines does Iron man have
text.count("\nIRON MAN\n")


# In[626]:


#how many lines does Thor have
text.count("\nTHOR\n")


# In[627]:


##how many lines does captain america have
text.count("\nCAPTAIN AMERICA\n")


# ## COVID data
# 
# Using [covidweekly2721.pdf](covidweekly2721.pdf), what's the total number of tests performed in Minnesota? Use the Laboratory Test Rates by County of Residence chart.
# 
# * You COULD pull both tables separately OR you could pull them both at once and split them in pandas.
# * Remember you can do things like `df[['name','age']]` to ask for multiple columns

# In[504]:


import numpy as np


# In[811]:


#importing covid data
covid = camelot.read_pdf("covidweekly2721.pdf", flavor='stream', pages= "6" )


# In[812]:


covid


# In[813]:


#there is only one table so saving in new variable
df6 = covid[0].df


# In[814]:


#renaming columns
df6 = df6.rename(columns={
    df6.columns[1]: 'County',
    df6.columns[2]: 'Number of Tests',
    df6.columns[3]: 'Cum Rate',
    df6.columns[4]: 'County1',
    df6.columns[5]: 'Number of Tests1',
    df6.columns[6]: 'Cum Rate1',
   
})
df6


# In[815]:


#cleaning up by dropping column 0
df6 = df6.drop(labels= df6.columns[0], axis=1) 
df6


# In[816]:


#cleaning up a bit more by getting rid of empty rows
df6 = df6.drop(labels=[0,1,2,3,4,6,7,12], axis=0)
df6


# In[545]:


#checking to see what types I'm working with
df6.info()


# In[817]:


#getting rid of commas and adding nan for blank spaces
test= df6["Number of Tests"].apply(lambda x:x.replace(",","")).replace(r'^\s*$', np.nan, regex=True)


# In[818]:


#saving as float
df6['test'] = test.astype(float)


# In[819]:


#sum of first column of tests
df6.test.sum()


# In[820]:


#getting rid of commas and saving as float
test1 = df6["Number of Tests1"].apply(lambda x:x.replace(",","")).replace(r'^\s*$', np.nan, regex=True)
df6['test1'] = test1.astype(float)


# In[821]:


#sum of second column of tests
df6.test1.sum()


# In[822]:


#creating a total column 
df6.assign(total = df6.test + df6.test1)


# In[830]:


#making sure total is the sum of test and test1
df6['total'] = df6.test + df6.test1


# In[832]:


#calulating sum of total column
df6.total.sum()


# In[ ]:





# ## Theme Parks
# 
# Using [2019-Theme-Index-web-1.pdf](2019-Theme-Index-web-1.pdf), save a CSV of the top 10 theme park groups worldwide.
# 
# * You can clean the results or you can restrict the area the table is pulled from, up to you

# In[717]:


#importing park PDF. i tried to use table areas but that ended up cutting off rows i needed, so commented out.
park= camelot.read_pdf("2019-Theme-Index-web-1.pdf", flavor="stream", pages="11") #table_areas =["70,490,380,290"])


# In[718]:


#checking its one table
park


# In[719]:


#saving as variable
themepark = park[0].df
themepark


# In[720]:


#renming columns
themepark = themepark.rename(columns={
    themepark.columns[1]: 'park',
    themepark.columns[2]: 'change',
    themepark.columns[3]: 'attendance19',
    themepark.columns[4]: 'attendance18'
    })
themepark                             


# In[721]:


#dropping unecessary 11th row
themepark = themepark.drop(labels=[11], axis=0)


# In[722]:


#making sure all rows are there
themepark


# In[741]:


#removing messy parts of text in columns
themepark[0] = themepark[0].str.strip("RANK\n")
themepark['park'] = themepark['park'].str.strip("GROUP NAME\n")
themepark['change'] = themepark["change"].str.strip("% CHANGE\n")
themepark['attendance19'] = themepark['attendance19'].str.strip("ATTENDANCE\n, 2019\n")
themepark['attendance18'] = themepark['attendance18'].str.strip("ATTENDANCE\n, 2018\n")


# In[742]:


#checking!
themepark


# In[743]:


#saving as csv.
themepark.to_csv("Themeparks.csv")


# In[ ]:





# ## Hunting licenses
# 
# Using [US_Fish_and_Wildlife_Service_2021.pdf](US_Fish_and_Wildlife_Service_2021.pdf) and [a CSV of state populations](http://goodcsv.com/geography/us-states-territories/), find the states with the highest per-capita hunting license holders.

# In[463]:


import glob
import os


# In[150]:


#bringing in pdf
hunt_data = camelot.read_pdf("US_Fish_and_Wildlife_Service_2021.pdf", flavor='stream')


# In[178]:


#its one table so saving as new variable
df3 = hunt_data[0].df
df3


# In[179]:


#renaming columns
df3 = df3.rename(columns={
    df3.columns[0]: 'State',
    df3.columns[1]: 'Paid License Holder',
    df3.columns[2]: 'Resident License Holder',
    df3.columns[3]: 'Non Resident License Holder',
    df3.columns[4]: 'Total',
    df3.columns[5]: 'Resident Cost',
    df3.columns[6]: 'Non Resident Cost',
    df3.columns[7]: 'Gross Cost'
})
df3


# In[180]:


#dropping unnecessary rows
df3 = df3.drop(labels=[0,1,2,3,4], axis=0)


# In[181]:


df3


# In[166]:


#checking to see total license holders from largest to smallest and which state they belong to
df.sort_values("Total",ascending= False)


# In[282]:


#bringing in population csv file
df_pop = pd.read_csv("us-states-territories.csv")
df_pop


# In[844]:


#renaming columns
df_pop = df_pop.rename(columns={
    df_pop.columns[5]: 'pop',
    df_pop.columns[6]: 'area'
})
df_pop


# In[845]:


#cleaning before i merge
df3["State"]= df3["State"].str.strip()


# In[846]:


#cleaning before i merge
df_pop["Abbreviation"] = df_pop["Abbreviation"].str.strip()


# In[960]:


#merging files
output1 = pd.merge(df3,df_pop, left_on="State", right_on="Abbreviation", how='left')


# In[961]:


output1


# In[957]:


output1.sort_values("Total", ascending = False)


# In[ ]:





# In[973]:


#in order to divide, need to clean numbers in both columns:
total1 = output1["Total"].apply(lambda x:x.replace(",","")).replace(r'^\s*$', np.nan, regex=True)
output1['total1'] = total1.astype(float)


# In[974]:


output1['pop1'] = output1["pop"] = pd.to_numeric(output1["pop"], downcast='float',errors='ignore')


# In[975]:


output1


# In[992]:


#output1["pop1"].apply(lambda x:x.replace(",",""))


# In[979]:


#data_div = output1['Total']/output1['pop1'] 


# In[991]:


type('total1')


# In[993]:


output1['total1'] = output1['total1'].astype(float)


# In[994]:


type("total1")


# In[995]:


output1['total1'] = (output1['total1'].str.split()).apply(lambda x: float(x[0].replace(',', '')))


# In[ ]:


#this will not let me change a str into a float in order to divide total by population to get highest number of hunters
#per capita. would love some guidence on this one!

