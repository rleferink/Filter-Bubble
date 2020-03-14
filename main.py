import pandas as pd
import re


def highlight_cells(cellvalue):
    # color = 'red' if len(cellValue) != 10 else ''
    # return ['background-color: red' if len(cellvalue[x][y]) != 10 else '']
    # return ['background-color: red' if len(df.loc[x,y]) != 10 else '']
    return ['background-color: red']

domains = (".nl", ".com", ".org", ".nu", ".be", ".eu", ".info", ".tips", ".net")
accepted_lengths = (9, 10)
total_counter = 0
failed_counter = 0

# data = pd.read_excel (r'C:\Users\Roland\PycharmProjects\scriptie\test.xlsx', sheet_name='Controversieel') #Laptop
# #data = pd.read_excel (r'C:\Users\Roland Leferink\PycharmProjects\scriptie\test.xlsx', sheet_name='Controversieel') #Desktop
# df = pd.DataFrame(data, columns=["Abortus tot hoeveel weken?","Oorzaken klimaatverandering","Zwarte piet of roetveegpiet?","Gevaren vaccinaties","Gevolgen illegale immigratie"])
# df = df.rename(columns={"Abortus tot hoeveel weken?": 1, "Oorzaken klimaatverandering": 2, "Zwarte piet of roetveegpiet?": 3, "Gevaren vaccinaties": 4, "Gevolgen illegale immigratie": 5})
# df.to_excel('ControversialData.xlsx')
# for i in range(len(df)):
#     for x in range(1, 6):
#         str = df.loc[i, x]
#         str = re.sub("[\s\S]*Web results",'', str)
#         str = re.sub("[\s\S]*Webresultaten",'', str)
#         str = re.sub("nl\.", "https://nl.", str)
#         str = re.sub("Adwww.*", '', str)
#         str = re.sub("Advertentiewww.*", '', str)
#         str = re.split("\s", str)
#         for y in range(len(str)):
#             if(str[y].startswith('Adw')):
#                 #print(str[y])
#                 str[y] = re.sub("Adwww.*", '', str[y])
#         #print(str)
#         #r = re.compile("http.*")
#         #r = re.compile("..+\..+")
#         r = re.compile(".*\.nl|.*\.com|.*\.org|.*\.nu|.*\.be|.*\.eu|.*\.info")
#         newlist = list(filter(r.match, str))
#         #print(newlist)
#         df.at[i, x] = newlist
# df.to_excel('ControversialResults.xlsx')

# data = pd.read_excel (r'C:\Users\Roland\PycharmProjects\scriptie\test.xlsx', sheet_name='Niet Controversieel') #Laptop
data = pd.read_excel(r'C:\Users\Roland Leferink\PycharmProjects\scriptie\test.xlsx',
                     sheet_name='Niet Controversieel')  # Desktop
df = pd.DataFrame(data,
                  columns=["Brood bakken recept", "Honden namen", "Wat is het grootste bot in het menselijk lichaam?",
                           "Hoeveel van een komkommer is water?", "Hoeveel mensen wonen er in Nederland?"])
df = df.rename(
    columns={"Brood bakken recept": 1, "Honden namen": 2, "Wat is het grootste bot in het menselijk lichaam?": 3,
             "Hoeveel van een komkommer is water?": 4, "Hoeveel mensen wonen er in Nederland?": 5})
df.to_excel('NonControversialData.xlsx')
for i in range(len(df)):
    for x in range(1, 6):
        str = df.loc[i, x]
        for xx in range(1, 2):
            str = re.sub(r'^.*?{}'.format(re.escape("Web results")), '', str, flags=re.DOTALL).strip()
            str = re.sub(r'^.*?{}'.format(re.escape("Webresultaten")), '', str, flags=re.DOTALL).strip()
        str = re.sub("nl\.", "https://nl.", str)
        # str = re.sub("Adwww.*",'',str)
        # str = re.sub("Advertentiewww.*", '', str)
        str = re.split("\s", str)
        # print(str)
        for y in range(len(str)):
            if str[y].startswith('Adw'):
                # print(str[y])
                str[y] = re.sub("Adwww.*", '', str[y])
                str[y] = re.sub("Advertentiewww.*", '', str[y])
        # print(str)
        # r = re.compile("http.*")
        # r = re.compile("..+\..+")
        for z in range(len(str)):
            if str[z].endswith(domains):
                if "hondennamen.nl" in str[z]:
                    pass
                elif "hondennamen.nu" in str[z]:
                    pass
                elif not str[z + 1] == '›':
                    #print(str[z - 1])
                    str[z] = re.sub(".*", '', str[z])

        r = re.compile(".*\.nl|.*\.com|.*\.org|.*\.nu|.*\.be|.*\.eu|.*\.info|.*\.tips")
        newlist = list(filter(r.match, str))
        total_counter += 1
        print(newlist)
        print(total_counter)
        if len(newlist) not in {9, 10}:
            # print("Er is iets fout gegaan")
            #print(newlist)
            failed_counter += 1
            df.at[i, x] = "handmatig"
        else:
            df.at[i, x] = newlist
        # print(newlist)

print(f'Out of {total_counter} lists {failed_counter} were not correct')

df.to_excel('NonControversialResults.xlsx')
# styled = df.style.applymap(highlight_cells)
# df.style.applymap(highlight_cells).to_excel('NonControversialResults.xlsx', engine='openpyxl')
# styled.to_excel('NonControversialResults.xlsx', engine='openpyxl')
