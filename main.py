import pandas as pd
import re

#data = pd.read_excel (r'C:\Users\Roland\PycharmProjects\scriptie\test.xlsx', sheet_name='Sheet1') #Laptop
data = pd.read_excel (r'C:\Users\Roland Leferink\PycharmProjects\scriptie\test.xlsx', sheet_name='Controversieel') #Desktop
df = pd.DataFrame(data, columns=["Abortus tot hoeveel weken?","Oorzaken klimaatverandering","Zwarte piet of roetveegpiet?","Gevaren vaccinaties","Gevolgen illegale immigratie"])
df = df.rename(columns={"Abortus tot hoeveel weken?": 1, "Oorzaken klimaatverandering": 2, "Zwarte piet of roetveegpiet?": 3, "Gevaren vaccinaties": 4, "Gevolgen illegale immigratie": 5})
df.to_excel('ControversialData.xlsx')
for i in range(len(df)):
    for x in range(1, 6):
        str = df.loc[i, x]
        str = re.sub(".*Search results",'', str)
        str = re.sub(".*Zoekresultaten",'', str)
        str = re.sub("nl\.", "https://nl.", str)
        #str = re.sub("Adwww.*", '', str)
        str = re.split("\s", str)
        for y in range(len(str)):
            if(str[y].startswith('Adw')):
                #print(str[y])
                str[y] = re.sub("Adwww.*", '', str[y])
        #print(str)
        #r = re.compile("http.*")
        #r = re.compile("..+\..+")
        r = re.compile(".*\.nl|.*\.com|.*\.org|.*\.nu|.*\.be|.*\.eu|.*\.info")
        newlist = list(filter(r.match, str))
        print(newlist)
        df.at[i, x] = newlist
df.to_excel('ControversialResults.xlsx')

data = pd.read_excel (r'C:\Users\Roland Leferink\PycharmProjects\scriptie\test.xlsx', sheet_name='Niet Controversieel') #Desktop
df = pd.DataFrame(data, columns=["Brood bakken recept","Honden namen","Wat is het grootste bot in het menselijk lichaam?","Hoeveel van een komkommer is water?","Hoeveel mensen wonen er in Nederland?"])
df = df.rename(columns={"Brood bakken recept": 1, "Honden namen": 2, "Wat is het grootste bot in het menselijk lichaam?": 3, "Hoeveel van een komkommer is water?": 4, "Hoeveel mensen wonen er in Nederland?": 5})
df.to_excel('NonControversialData.xlsx')
for i in range(len(df)):
    for x in range(1, 6):
        str = df.loc[i, x]
        str = re.sub(".*Search results",'', str)
        str = re.sub(".*Zoekresultaten",'', str)
        str = re.sub("nl\.", "https://nl.", str)
        #str = re.sub("Adwww.*",'',str)
        str = re.split("\s", str)
        for y in range(len(str)):
            if (str[y].startswith('Adw')):
                #print(str[y])
                str[y] = re.sub("Adwww.*", '', str[y])
        #print(str)
        #r = re.compile("http.*")
        #r = re.compile("..+\..+")
        r = re.compile(".*\.nl|.*\.com|.*\.org|.*\.nu|.*\.be|.*\.eu|.*\.info")
        newlist = list(filter(r.match, str))
        print(newlist)
        df.at[i, x] = newlist
df.to_excel('NonControversialResults.xlsx')