import pandas as pd
import re

data = pd.read_excel (r'C:\Users\Roland\PycharmProjects\scriptie\test.xlsx', sheet_name='Sheet1') #Laptop
#data = pd.read_excel (r'C:\Users\Roland Leferink\PycharmProjects\scriptie\test.xlsx', sheet_name='Sheet1') #Desktop
df = pd.DataFrame(data, columns=["Abortus tot hoeveel weken?","Oorzaken klimaatverandering","Zwarte piet of roetveegpiet?","Gevaren vaccinaties","Gevolgen illegale immigratie"])
df = df.rename(columns={"Abortus tot hoeveel weken?": 1, "Oorzaken klimaatverandering": 2, "Zwarte piet of roetveegpiet?": 3, "Gevaren vaccinaties": 4, "Gevolgen illegale immigratie": 5})
#print(df)
df.to_excel('data.xlsx')
for i in range(len(df)):
    for x in range(1, 6):
        str = df.loc[i, x]
        str = re.sub(".*Web results",'', str)
        str = re.sub(".*Webresultaten",'', str)
        str = re.split("\s", str)
        #print(str)
        #r = re.compile("http.*")
        r = re.compile("..+\..+")
        newlist = list(filter(r.match, str))
        print(newlist)
        df.at[i, x] = newlist
df.to_excel('result.xlsx')

#df.to_csv(r'C:\Users\Roland Leferink\PycharmProjects\scriptie\output.txt', header=None, index=None, mode='a', sep=' ')
#dato = pd.read_csv('output.txt', header = None)
#print(dato)
#dato.to_excel('dato.xlsx', header=None)


#data = pd.read_csv (r'C:\Users\Roland\PycharmProjects\scriptie\test.csv') #Laptop
#data = pd.read_csv (r'C:\Users\Roland Leferink\PycharmProjects\scriptie\test.csv') #Desktop
#df = pd.DataFrame(data, columns=['Wat is uw leeftijd?','Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?'])
#print(df)