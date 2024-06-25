import pandas as pd
import numpy as np
import collections


ieee = pd.read_csv('IEEE paper results.csv')
acm = pd.read_csv('ACM paper results.csv')
springer = pd.read_csv('springer papers.csv')
included = pd.read_csv('included_papers.csv')
years = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']


ieee['Publication Year'] = ieee['Publication Year'].astype(str)
acm['Publication Year'] = acm['Publication Year'].astype(str)


#checking for year
'''
for year in range(len(acm['Publication Year'])):
    if acm['Publication Year'][year] not in years:
        acm.loc[year, 'excluded_stage1'] = 'True'
        acm.loc[year, 'excluded_stage2'] = 'True'
        acm.loc[year, 'excluded_stage3'] = 'True'
    else:
         acm.loc[year, 'excluded_stage1'] = 'False'

for year in range(len(ieee['Publication Year'])):
    if ieee['Publication Year'][year] not in years:
        ieee.loc[year, 'excluded_stage1'] = 'True'
    else:
         ieee.loc[year, 'excluded_stage1'] = 'False'


for year in range(len(springer['Year'])):
    if springer['Year'][year] not in years:
        springer.loc[year, 'excluded_stage1'] = 'True'
    else:
         springer.loc[year, 'excluded_stage1'] = 'False'

'''

'''
#checking for duplicates

springDOIS = springer['DOI'].tolist()
acmDOIS = acm['DOI'].tolist()
ieeeDOIS = ieee['DOI'].tolist()



for i in range(len(springDOIS)):
    if springDOIS[i] != 'None':
        if springDOIS[i] in acmDOIS and springDOIS[i] not in ieeeDOIS:
            springer.loc[i, 'excluded_stage1'] = 'True'
            springer.loc[i, 'excluded_stage2'] = 'True'
            springer.loc[i, 'excluded_stage3'] = 'True'
        if springDOIS[i] in ieeeDOIS and springDOIS[i] not in acmDOIS:
            springer.loc[i, 'excluded_stage1'] = 'True'
            springer.loc[i, 'excluded_stage2'] = 'True'
            springer.loc[i, 'excluded_stage3'] = 'True'
        if springDOIS[i] in ieeeDOIS and springDOIS[i] in acmDOIS:
            springer.loc[i, 'excluded_stage1'] = 'True'
            springer.loc[i, 'excluded_stage2'] = 'True'
            springer.loc[i, 'excluded_stage3'] = 'True'
            ieee.loc[i, 'excluded_stage1'] = 'True'
            ieee.loc[i, 'excluded_stage2'] = 'True'
            ieee.loc[i, 'excluded_stage3'] = 'True'

for i in range(len(ieeeDOIS)):
    if ieeeDOIS[i] != np.nan:
        if ieeeDOIS[i] in acmDOIS and ieeeDOIS[i] not in springDOIS:
            ieee.loc[i, 'excluded_stage1'] = 'True'
            ieee.loc[i, 'excluded_stage2'] = 'True'
            ieee.loc[i, 'excluded_stage3'] = 'True'


'''
'''
springtitles = springer['Title'].tolist()
acmtitles = acm['Title'].tolist()
ieeetitles = ieee['Document Title'].tolist()
springIEEEDupsTitle = []
springACMDupsTitle = []
ieeeACMDupsTitle = []
allDupsTitle = []
'''
'''
exclusionTypes = ['book', 'reference work', 'reference work entry', 'short paper', 'tool demo', 'review', 'report', 'keynote', 'tutorial summary', 'panel discussion', 'book and reference work']

for type in range(len(acm['Item Type'])):
    if acm['Item Type'][type].lower() in exclusionTypes:
        acm.loc[type, 'excluded_stage3'] = 'True'
        acm.loc[type, 'excluded_stage2'] = 'True'
'''
'''for type in range(len(springer['Content Type'])):
    if springer['Content Type'][type].lower() in exclusionTypes:
        springer.loc[type, 'excluded_stage3'] = 'True'
        springer.loc[type, 'excluded_stage2'] = 'True'

for type in range(len(ieee['excluded_stage1'])):
    if ieee['excluded_stage1'][type] == True:
        ieee.loc[type, 'excluded_stage3'] = 'True'
        ieee.loc[type, 'excluded_stage2'] = 'True' '''

'''
for type in range(len(acm['excluded_stage1'])):
    if acm['excluded_stage1'][type] == 'True':
        acm.loc[type, 'excluded_stage3'] = 'True'
        acm.loc[type, 'excluded_stage2'] = 'True'

for type in range(len(ieee['excluded_stage1'])):
    if ieee['excluded_stage1'][type] == 'True':
        ieee.loc[type, 'excluded_stage3'] = 'True'
        ieee.loc[type, 'excluded_stage2'] = 'True' 
'''

'''

for type in range(len(springer['excluded_stage1'])):
    if springer['excluded_stage1'][type] == True or springer['excluded_stage1'][type] == 'True':
        springer.loc[type, 'excluded_stage3'] = 'True'
        springer.loc[type, 'excluded_stage2'] = 'True' '''

includedDOIs = included['doi'].to_list()
IncludedTitles = included['title'].to_list()
acmtitles = acm['Title'].tolist()
ieeetitles = ieee['Document Title'].tolist()
springerTitle = springer['Title'].tolist()

for paper in range(len(IncludedTitles)):
    print(paper)
    if IncludedTitles[paper] != np.nan:
        '''if includedDOIs[paper] in springDOIS:
            #print(springer.loc[paper, 'DOI'])
            springer.loc[springer['DOI'] == includedDOIs[paper]]['excluded_stage1'] = 'False'
            springer.loc[springer['DOI'] == includedDOIs[paper]]['excluded_stage2'] = 'False'
            springer.loc[springer['DOI'] == includedDOIs[paper]]['excluded_stage3'] = 'False' 
        if includedDOIs[paper] in ieeeDOIS:
            #print(ieee.loc[paper, 'DOI'])
            ieee.loc[ieee['DOI'] == includedDOIs[paper]]['excluded_stage1'] = 'False'
            ieee.loc[ieee['DOI'] == includedDOIs[paper]]['excluded_stage2'] = 'False'
            ieee.loc[ieee['DOI'] == includedDOIs[paper]]['excluded_stage3'] = 'False'
'''
        for title in ieeetitles:
            if title == IncludedTitles[paper]:
                print(title)
                rowIDX = ieee['Document Title'] == IncludedTitles[paper]
                ieee.loc[rowIDX , 'excluded_stage1'] = 'False'
                ieee.loc[rowIDX , 'excluded_stage2'] = 'False'
                ieee.loc[rowIDX , 'excluded_stage3'] = 'False'
                ieee.loc[rowIDX , 'already_analyzed'] = 'True'

'''   for title in acmtitles:
            if title in IncludedTitles[paper]:
                acm.loc[acm['DOI'] == includedDOIs[paper]]['excluded_stage1'] = 'False'
                acm.loc[acm['DOI'] == includedDOIs[paper]]['excluded_stage2'] = 'False'
                acm.loc[acm['DOI'] == includedDOIs[paper]]['excluded_stage3'] = 'False'
          '''      
'''
        if includedDOIs[paper] in acmDOIS:
            #print(acm.loc[paper, 'DOI'])
            acm.loc[acm['DOI'] == includedDOIs[paper]]['excluded_stage1'] = 'False'
            acm.loc[acm['DOI'] == includedDOIs[paper]]['excluded_stage2'] = 'False'
            acm.loc[acm['DOI'] == includedDOIs[paper]]['excluded_stage3'] = 'False' 
'''

            
'''
for title in range(len(acm['Title'])):
    if len(acm['Title'][title].split()) <= 3:
        acm.loc[title, 'excluded_stage2'] = 'True'
        acm.loc[title, 'excluded_stage3'] = 'True'
    if 'survey' in acm['Title'][title].lower() or 'comparative' in acm['Title'][title].lower() or 'comparison' in acm['Title'][title].lower():
        acm.loc[title, 'excluded_stage2'] = 'True'
        acm.loc[title, 'excluded_stage3'] = 'True'

for title in range(len(ieee['Document Title'])):
    if len(ieee['Document Title'][title].split()) <= 3:
        ieee.loc[title, 'excluded_stage2'] = 'True'
        ieee.loc[title, 'excluded_stage3'] = 'True'
    if 'survey' in ieee['Document Title'][title].lower() or 'comparative' in ieee['Document Title'][title].lower() or 'comparison' in ieee['Document Title'][title].lower():
        ieee.loc[title, 'excluded_stage2'] = 'True'
        ieee.loc[title, 'excluded_stage3'] = 'True'

'''

acm.to_csv('ACM paper results.csv', index=False)
ieee.to_csv('IEEE paper results.csv', index=False)
springer.to_csv('springer papers.csv', index=False)