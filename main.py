import pandas as pd
import re




domains = (".nl", ".com", ".org", ".nu", ".be", ".eu", ".info", ".tips", ".net")
accepted_lengths = (9, 10)
total_counter = 0
failed_counter = 0
ten_result_pages = 0
nine_result_pages = 0
controversial_counter = 0
noncontroversial_counter = 0


data = pd.read_excel(r'..\PycharmProjects\scriptie\test.xlsx', sheet_name='Controversieel')
df = pd.DataFrame(data, columns=["Abortus tot hoeveel weken?","Oorzaken klimaatverandering","Zwarte piet of roetveegpiet?","Gevaren vaccinaties","Gevolgen illegale immigratie"])
df = df.rename(columns={"Abortus tot hoeveel weken?": 1, "Oorzaken klimaatverandering": 2, "Zwarte piet of roetveegpiet?": 3, "Gevaren vaccinaties": 4, "Gevolgen illegale immigratie": 5})
df.to_excel('ControversialData.xlsx')
for i in range(len(df)):
    for x in range(1, 6):
        str = df.loc[i, x]
        #removes all text before the first occurance Web results, Webresultaten and Search Results.
        str = re.sub(r'^.*?{}'.format(re.escape("Web results")), '', str, flags=re.DOTALL).strip()
        str = re.sub(r'^.*?{}'.format(re.escape("Webresultaten")), '', str, flags=re.DOTALL).strip()
        str = re.sub(r'^.*?{}'.format(re.escape("Search Results")), '', str, flags=re.DOTALL).strip()
        str = re.sub("Advertentie.*$", '', str)
        str = re.sub("Ads.*$", '', str)
        str = re.split("\s", str)
        for z in range(len(str)):
            if str[z].endswith('/'):
                str[z] = str[z][:-1]
            if str[z].endswith(domains):
                if "stichtingvaccinvrij.nl" in str[z]:
                    pass
                elif not str[z + 1] == '›':
                    str[z] = re.sub(".*", '', str[z])

        r = re.compile(".*\.nl|.*\.com|.*\.org|.*\.nu|.*\.be|.*\.eu|.*\.info|.*\.tips|.*\.net")
        website_list = list(filter(r.match, str))
        total_counter += 1
        controversial_counter += 1
        if len(website_list) not in {9, 10}:
            failed_counter += 1
            df.at[i, x] = website_list
        else:
            if len(website_list) == 9:
                nine_result_pages += 1
                #df.at[i, x] = website_list
            else:
                ten_result_pages += 1
                #df.at[i, x] = ""
            df.at[i, x] = ''

df.to_excel('ControversialResults.xlsx')


data = pd.read_excel(r'..\PycharmProjects\scriptie\test.xlsx', sheet_name='Niet Controversieel')
df = pd.DataFrame(data, columns=["Brood bakken recept", "Honden namen", "Wat is het grootste bot in het menselijk lichaam?", "Hoeveel van een komkommer is water?", "Hoeveel mensen wonen er in Nederland?"])
df = df.rename(columns={"Brood bakken recept": 1, "Honden namen": 2, "Wat is het grootste bot in het menselijk lichaam?": 3, "Hoeveel van een komkommer is water?": 4, "Hoeveel mensen wonen er in Nederland?": 5})
df.to_excel('NonControversialData.xlsx')
for i in range(len(df)):
    for x in range(1, 6):
        str = df.loc[i, x]
        str = re.sub(r'^.*?{}'.format(re.escape("Web results")), '', str, flags=re.DOTALL).strip()
        str = re.sub(r'^.*?{}'.format(re.escape("Webresultaten")), '', str, flags=re.DOTALL).strip()
        str = re.sub("Advertentie.*$", '', str)
        str = re.sub("Ad.*$", '', str)
        str = re.split("\s", str)
        for z in range(len(str)):
            if str[z].endswith('/'):
                str[z] = str[z][:-1]
            if str[z].endswith(domains):
                if "hondennamen.nl" in str[z]:
                    pass
                elif "hondennamen.nu" in str[z]:
                    pass
                elif not str[z + 1] == '›':
                    str[z] = re.sub(".*", '', str[z])

        r = re.compile(".*\.nl|.*\.com|.*\.org|.*\.nu|.*\.be|.*\.eu|.*\.info|.*\.tips|.*\.net")
        website_list = list(filter(r.match, str))
        total_counter += 1
        noncontroversial_counter += 1
        if len(website_list) not in {9, 10}:
            failed_counter += 1
            df.at[i, x] = website_list
        else:
            if len(website_list) == 9:
                nine_result_pages += 1
            else:
                ten_result_pages += 1
            df.at[i, x] = website_list

print(f'Out of {total_counter} lists {failed_counter} were not correct')
print(f'There are {nine_result_pages} pages with 9 results')
print(f'There are {ten_result_pages} pages with 10 results')
print(f'There are {controversial_counter} Controversial lists and {noncontroversial_counter} non controversial lists')

df.to_excel('NonControversialResults.xlsx')