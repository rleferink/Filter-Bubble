import pandas as pd
import textdistance as td
import re

ageSheetNames = ("Controversieel Leeftijd", "Niet Controversieel Leeftijd")
locationSheetNames = ("Controversieel Locatie", "Niet Controversieel Locatie")
partySheetNames = ("Controversieel Partij", "Niet Controversieel Partij")
elementSheetNames = ("Controversieel", "Niet Controversieel")
columnNamesControversial = ("Abortus tot hoeveel weken?","Oorzaken klimaatverandering","Zwarte piet of roetveegpiet?","Gevaren vaccinaties","Gevolgen illegale immigratie")
columnNamesNonControversial = ("Brood bakken recept", "Honden namen", "Wat is het grootste bot in het menselijk lichaam?", "Hoeveel van een komkommer is water?", "Hoeveel mensen wonen er in Nederland?")
smallestWebsiteList = 8
comparisons = 0
rawResults = False
allWebsites = []


#Different groups in the three categories
ageGroups = ['<18', '18 - 24', '25 - 34', '35 - 44', '45 - 54', '>55'] #6 groups
locations = ['Buiten Nederland', 'Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant', 'Noord-Holland', 'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland'] #13 groups
parties = ['CDA', 'ChristenUnie', 'DENK', 'D66', 'FvD', 'GroenLinks', 'Niet', 'PvdA', 'PvdD', 'PVV', 'SGP', 'SP', '50PLUS', 'VVD'] #14 groups
spectrumLeft = ['DENK', 'D66', 'GroenLinks', 'PvdA', 'PvdD', 'SP']
spectrumRight = ['CSA', 'ChristenUnie', 'FvD', 'PVV', 'SGP', '50PLUS', 'VVD']
controversialTopics = ['Abortus', 'Klimaatverandering', 'Zwartepiet', 'Vaccinaties', 'Immigratie']
normalTopics = ['Brood', 'Honden', 'Bot', 'Komkommer', 'Inwoners']
#The different groups in the category of age
#ControversialAgeSimilaritys: CAS
CAS0 = []
CAS1 = []
CAS2 = []
CAS3 = []
CAS4 = []
CAS5 = []
#NormalAgeSimilaritys: NAS
NAS0 = []
NAS1 = []
NAS2 = []
NAS3 = []
NAS4 = []
NAS5 = []
#The different groups in the category of location
#ControversialLocatioNSistances: CLS
CLS0 = []
CLS1 = []
CLS2 = []
CLS3 = []
CLS4 = []
CLS5 = []
CLS6 = []
CLS7 = []
CLS8 = []
CLS9 = []
CLS10 = []
CLS11 = []
CLS12 = []
#NormalLocatioNSistances: NLS
NLS0 = []
NLS1 = []
NLS2 = []
NLS3 = []
NLS4 = []
NLS5 = []
NLS6 = []
NLS7 = []
NLS8 = []
NLS9 = []
NLS10 = []
NLS11 = []
NLS12 = []
#The different groups in the category of political parties
#ControversialPoliticalSimilarity: CPS
CPS0 = []
CPS1 = []
CPS2 = []
CPS3 = []
CPS4 = []
CPS5 = []
CPS6 = []
CPS7 = []
CPS8 = []
CPS9 = []
CPS10 = []
CPS11 = []
CPS12 = []
CPS13 = []
#NormalPoliticalSimilarity: NPS
NPS0 = []
NPS1 = []
NPS2 = []
NPS3 = []
NPS4 = []
NPS5 = []
NPS6 = []
NPS7 = []
NPS8 = []
NPS9 = []
NPS10 = []
NPS11 = []
NPS12 = []
NPS13 = []
#ControversialSpectrumSimilarity: CSS
CSSLeft = []
CSSRight = []
#NormalSpectrumSimilarity: NSS
NSSLeft = []
NSSRight = []
#ControversialSimilarity: CS
CS = []
#NormalSimilarity: NS
NS = []
#ControversialTopicSimilarity: CTS
CTS0 = []
CTS1 = []
CTS2 = []
CTS3 = []
CTS4 = []
#NormalTopicSimilarity: NTS
NTS0 = []
NTS1 = []
NTS2 = []
NTS3 = []
NTS4 = []
#Lists of all groups:
CAS = [CAS0, CAS1, CAS2, CAS3, CAS4, CAS5]
NAS = [NAS0, NAS1, NAS2, NAS3, NAS4, NAS5]
CLS = [CLS0, CLS1, CLS2, CLS3, CLS4, CLS5, CLS6, CLS7, CLS8, CLS9, CLS10, CLS11, CLS12]
NLS = [NLS0, NLS1, NLS2, NLS3, NLS4, NLS5, NLS6, NLS7, NLS8, NLS9, NLS10, NLS11, NLS12]
CPS = [CPS0, CPS1, CPS2, CPS3, CPS4, CPS5, CPS6, CPS7, CPS8, CPS9, CPS10, CPS11, CPS12, CPS13]
NPS = [NPS0, NPS1, NPS2, NPS3, NPS4, NPS5, NPS6, NPS7, NPS8, NPS9, NPS10, NPS11, NPS12, NPS13]
CSS = [CSSLeft, CSSRight]
NSS = [NSSLeft, NSSRight]
CTS = [CTS0, CTS1, CTS2, CTS3, CTS4]
NTS = [NTS0, NTS1, NTS2, NTS3, NTS4]
#Average of the groups
CASAverage = []
NASAverage = []
CLSAverage = []
NLSAverage = []
CPSAverage = []
NPSAverage = []
CSAverage = 0
NSAverage = 0
CSSLeftAverage = 0
CSSRightAverage = 0
NSSLeftAverage = 0
NSSRightAverage = 0
CTSAverage = []
NTSAverage = []

def Average(lst):
    return sum(lst) / len(lst)

def SimilarityCalc(lst1, lst2):
    similarity = 0
    for listElement in lst1:
        if listElement in lst2:
            lst2.remove(listElement)
            similarity += 1
    return similarity

#Only keep first 8 elements of list Niet Controversieel
for i in elementSheetNames:
    data = pd.read_excel("8elementen.xlsx", sheet_name=i)
    if i == "Niet Controversieel":
        df = pd.DataFrame(data, columns=["Timestamp", "Wat is uw leeftijd?", "In welke provincie vult u deze vragenlijst in?", "Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?", "Brood bakken recept", "Honden namen", "Wat is het grootste bot in het menselijk lichaam?", "Hoeveel van een komkommer is water?", "Hoeveel mensen wonen er in Nederland?"])
        df = df.rename(columns={"Timestamp": 1, "Wat is uw leeftijd?": 2, "In welke provincie vult u deze vragenlijst in?": 3, "Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?": 4, "Brood bakken recept": 5, "Honden namen": 6, "Wat is het grootste bot in het menselijk lichaam?": 7, "Hoeveel van een komkommer is water?": 8, "Hoeveel mensen wonen er in Nederland?": 9})
        for x in range(len(df)):
                for y in range(5, 10):
                    stringOfWebsites = df.loc[x, y]
                    websiteList = re.split("\s", stringOfWebsites)
                    websiteList = websiteList[:smallestWebsiteList]
                    df.at[x, y] = websiteList
df.to_excel('Levenshtein8ElementsNonControversial.xlsx')

#Only keep first 8 elements of list Controversieel
for i in elementSheetNames:
    data = pd.read_excel("8elementen.xlsx", sheet_name=i)
    if i == "Controversieel":
        df = pd.DataFrame(data, columns=["Timestamp", "Wat is uw leeftijd?", "In welke provincie vult u deze vragenlijst in?", "Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?", "Abortus tot hoeveel weken?", "Oorzaken klimaatverandering", "Zwarte piet of roetveegpiet?", "Gevaren vaccinaties", "Gevolgen illegale immigratie"])
        df = df.rename(columns={"Timestamp": 1, "Wat is uw leeftijd?": 2, "In welke provincie vult u deze vragenlijst in?": 3, "Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?": 4, "Abortus tot hoeveel weken?": 5, "Oorzaken klimaatverandering": 6, "Zwarte piet of roetveegpiet?": 7, "Gevaren vaccinaties": 8, "Gevolgen illegale immigratie": 9})
        for x in range(len(df)):
                for y in range(5, 10):
                    stringOfWebsites = df.loc[x, y]
                    websiteList = re.split("\s", stringOfWebsites)
                    websiteList = websiteList[:smallestWebsiteList]
                    df.at[x, y] = websiteList
df.to_excel('Levenshtein8ElementsControversial.xlsx')

#Levenshtein similarity based on age
for i in ageSheetNames:
    data = pd.read_excel("LevenshteinData.xlsx", sheet_name=i)
    if i == "Controversieel Leeftijd":
        df = pd.DataFrame(data, columns=["Wat is uw leeftijd?", "Abortus tot hoeveel weken?", "Oorzaken klimaatverandering", "Zwarte piet of roetveegpiet?", "Gevaren vaccinaties", "Gevolgen illegale immigratie"])
        df = df.rename(columns={"Wat is uw leeftijd?": 1, "Abortus tot hoeveel weken?": 2, "Oorzaken klimaatverandering": 3, "Zwarte piet of roetveegpiet?": 4, "Gevaren vaccinaties": 5, "Gevolgen illegale immigratie": 6})
    else:
        df = pd.DataFrame(data, columns=["Wat is uw leeftijd?", "Brood bakken recept", "Honden namen", "Wat is het grootste bot in het menselijk lichaam?", "Hoeveel van een komkommer is water?", "Hoeveel mensen wonen er in Nederland?"])
        df = df.rename(columns={"Wat is uw leeftijd?": 1, "Brood bakken recept": 2, "Honden namen": 3, "Wat is het grootste bot in het menselijk lichaam?": 4, "Hoeveel van een komkommer is water?": 5, "Hoeveel mensen wonen er in Nederland?": 6})
    for x in range(len(df)):
        for y in range(2, 7):
            stringOfWebsites = df.loc[x, y]
            websiteList = re.split("\s", stringOfWebsites)
            websiteList = websiteList[:smallestWebsiteList]
            for xx in range(len(df)):
                if x == xx:
                    pass
                elif x > xx:
                    pass
                elif df.loc[x, 1] == df.loc[xx, 1]:
                    stringOfComparingWebsites = df.loc[xx, y]
                    comparingWebsiteList = re.split("\s", stringOfComparingWebsites)
                    comparingWebsiteList = comparingWebsiteList[:smallestWebsiteList]
                    similarity = SimilarityCalc(websiteList, comparingWebsiteList)
                    if i == "Controversieel Leeftijd":
                        if df.loc[x, 1] == ageGroups[0]:
                            CAS0.append(similarity)
                        elif df.loc[x, 1] == ageGroups[1]:
                            CAS1.append(similarity)
                        elif df.loc[x, 1] == ageGroups[2]:
                            CAS2.append(similarity)
                        elif df.loc[x, 1] == ageGroups[3]:
                            CAS3.append(similarity)
                        elif df.loc[x, 1] == ageGroups[4]:
                            CAS4.append(similarity)
                        elif df.loc[x, 1] == ageGroups[5]:
                            CAS5.append(similarity)
                    else:
                        if df.loc[x, 1] == ageGroups[0]:
                            NAS0.append(similarity)
                        elif df.loc[x, 1] == ageGroups[1]:
                            NAS1.append(similarity)
                        elif df.loc[x, 1] == ageGroups[2]:
                            NAS2.append(similarity)
                        elif df.loc[x, 1] == ageGroups[3]:
                            NAS3.append(similarity)
                        elif df.loc[x, 1] == ageGroups[4]:
                            NAS4.append(similarity)
                        elif df.loc[x, 1] == ageGroups[5]:
                            NAS5.append(similarity)

#Levenshtein Similarity based on location.
for i in locationSheetNames:
    data = pd.read_excel("LevenshteinData.xlsx", sheet_name=i)
    if i == "Controversieel Locatie":
        df = pd.DataFrame(data, columns=["In welke provincie vult u deze vragenlijst in?", "Abortus tot hoeveel weken?", "Oorzaken klimaatverandering", "Zwarte piet of roetveegpiet?", "Gevaren vaccinaties", "Gevolgen illegale immigratie"])
        df = df.rename(columns={"In welke provincie vult u deze vragenlijst in?": 1, "Abortus tot hoeveel weken?": 2, "Oorzaken klimaatverandering": 3, "Zwarte piet of roetveegpiet?": 4, "Gevaren vaccinaties": 5, "Gevolgen illegale immigratie": 6})
    else:
        df = pd.DataFrame(data, columns=["In welke provincie vult u deze vragenlijst in?", "Brood bakken recept", "Honden namen", "Wat is het grootste bot in het menselijk lichaam?", "Hoeveel van een komkommer is water?", "Hoeveel mensen wonen er in Nederland?"])
        df = df.rename(columns={"In welke provincie vult u deze vragenlijst in?": 1, "Brood bakken recept": 2, "Honden namen": 3, "Wat is het grootste bot in het menselijk lichaam?": 4, "Hoeveel van een komkommer is water?": 5, "Hoeveel mensen wonen er in Nederland?": 6})
    for x in range(len(df)):
        for y in range(2, 7):
            stringOfWebsites = df.loc[x, y]
            websiteList = re.split("\s", stringOfWebsites)
            websiteList = websiteList[:smallestWebsiteList]
            for xx in range(len(df)):
                if x == xx:
                    pass
                elif x > xx:
                    pass
                elif df.loc[x, 1] == df.loc[xx, 1]:
                    stringOfComparingWebsites = df.loc[xx, y]
                    comparingWebsiteList = re.split("\s", stringOfComparingWebsites)
                    comparingWebsiteList = comparingWebsiteList[:smallestWebsiteList]
                    similarity = SimilarityCalc(websiteList, comparingWebsiteList)
                    if i == "Controversieel Locatie":
                        if df.loc[x, 1] == locations[0]:
                            CLS0.append(similarity)
                        elif df.loc[x, 1] == locations[1]:
                            CLS1.append(similarity)
                        elif df.loc[x, 1] == locations[2]:
                            CLS2.append(similarity)
                        elif df.loc[x, 1] == locations[3]:
                            CLS3.append(similarity)
                        elif df.loc[x, 1] == locations[4]:
                            CLS4.append(similarity)
                        elif df.loc[x, 1] == locations[5]:
                            CLS5.append(similarity)
                        elif df.loc[x, 1] == locations[6]:
                            CLS6.append(similarity)
                        elif df.loc[x, 1] == locations[7]:
                            CLS7.append(similarity)
                        elif df.loc[x, 1] == locations[8]:
                            CLS8.append(similarity)
                        elif df.loc[x, 1] == locations[9]:
                            CLS9.append(similarity)
                        elif df.loc[x, 1] == locations[10]:
                            CLS10.append(similarity)
                        elif df.loc[x, 1] == locations[11]:
                            CLS11.append(similarity)
                        elif df.loc[x, 1] == locations[12]:
                            CLS12.append(similarity)
                    else:
                        if df.loc[x, 1] == locations[0]:
                            NLS0.append(similarity)
                        elif df.loc[x, 1] == locations[1]:
                            NLS1.append(similarity)
                        elif df.loc[x, 1] == locations[2]:
                            NLS2.append(similarity)
                        elif df.loc[x, 1] == locations[3]:
                            NLS3.append(similarity)
                        elif df.loc[x, 1] == locations[4]:
                            NLS4.append(similarity)
                        elif df.loc[x, 1] == locations[5]:
                            NLS5.append(similarity)
                        elif df.loc[x, 1] == locations[6]:
                            NLS6.append(similarity)
                        elif df.loc[x, 1] == locations[7]:
                            NLS7.append(similarity)
                        elif df.loc[x, 1] == locations[8]:
                            NLS8.append(similarity)
                        elif df.loc[x, 1] == locations[9]:
                            NLS9.append(similarity)
                        elif df.loc[x, 1] == locations[10]:
                            NLS10.append(similarity)
                        elif df.loc[x, 1] == locations[11]:
                            NLS11.append(similarity)
                        elif df.loc[x, 1] == locations[12]:
                            NLS12.append(similarity)


#Levenshtein Similarity based on political affiliation.
for i in partySheetNames:
    data = pd.read_excel("LevenshteinData.xlsx", sheet_name=i)
    if i == "Controversieel Partij":
        df = pd.DataFrame(data, columns=["Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?", "Abortus tot hoeveel weken?", "Oorzaken klimaatverandering", "Zwarte piet of roetveegpiet?", "Gevaren vaccinaties", "Gevolgen illegale immigratie"])
        df = df.rename(columns={"Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?": 1, "Abortus tot hoeveel weken?": 2, "Oorzaken klimaatverandering": 3, "Zwarte piet of roetveegpiet?": 4, "Gevaren vaccinaties": 5, "Gevolgen illegale immigratie": 6})
    else:
        df = pd.DataFrame(data, columns=["Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?", "Brood bakken recept", "Honden namen", "Wat is het grootste bot in het menselijk lichaam?", "Hoeveel van een komkommer is water?", "Hoeveel mensen wonen er in Nederland?"])
        df = df.rename(columns={"Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?": 1, "Brood bakken recept": 2, "Honden namen": 3, "Wat is het grootste bot in het menselijk lichaam?": 4, "Hoeveel van een komkommer is water?": 5, "Hoeveel mensen wonen er in Nederland?": 6})
    for x in range(len(df)):
        for y in range(2, 7):
            stringOfWebsites = df.loc[x, y]
            websiteList = re.split("\s", stringOfWebsites)
            websiteList = websiteList[:smallestWebsiteList]
            for xx in range(len(df)):
                if x == xx:
                    pass
                elif x > xx:
                    pass
                elif df.loc[x, 1] == df.loc[xx, 1]:
                    stringOfComparingWebsites = df.loc[xx, y]
                    comparingWebsiteList = re.split("\s", stringOfComparingWebsites)
                    comparingWebsiteList = comparingWebsiteList[:smallestWebsiteList]
                    similarity = SimilarityCalc(websiteList, comparingWebsiteList)
                    if i == "Controversieel Partij":
                        if df.loc[x, 1] == parties[0]:
                            CPS0.append(similarity)
                        elif df.loc[x, 1] == parties[1]:
                            CPS1.append(similarity)
                        elif df.loc[x, 1] == parties[2]:
                            CPS2.append(similarity)
                        elif df.loc[x, 1] == parties[3]:
                            CPS3.append(similarity)
                        elif df.loc[x, 1] == parties[4]:
                            CPS4.append(similarity)
                        elif df.loc[x, 1] == parties[5]:
                            CPS5.append(similarity)
                        elif df.loc[x, 1] == parties[6]:
                            CPS6.append(similarity)
                        elif df.loc[x, 1] == parties[7]:
                            CPS7.append(similarity)
                        elif df.loc[x, 1] == parties[8]:
                            CPS8.append(similarity)
                        elif df.loc[x, 1] == parties[9]:
                            CPS9.append(similarity)
                        elif df.loc[x, 1] == parties[10]:
                            CPS10.append(similarity)
                        elif df.loc[x, 1] == parties[11]:
                            CPS11.append(similarity)
                        elif df.loc[x, 1] == parties[12]:
                            CPS12.append(similarity)
                        elif df.loc[x, 1] == parties[13]:
                            CPS13.append(similarity)
                    else:
                        if df.loc[x, 1] == parties[0]:
                            NPS0.append(similarity)
                        elif df.loc[x, 1] == parties[1]:
                            NPS1.append(similarity)
                        elif df.loc[x, 1] == parties[2]:
                            NPS2.append(similarity)
                        elif df.loc[x, 1] == parties[3]:
                            NPS3.append(similarity)
                        elif df.loc[x, 1] == parties[4]:
                            NPS4.append(similarity)
                        elif df.loc[x, 1] == parties[5]:
                            NPS5.append(similarity)
                        elif df.loc[x, 1] == parties[6]:
                            NPS6.append(similarity)
                        elif df.loc[x, 1] == parties[7]:
                            NPS7.append(similarity)
                        elif df.loc[x, 1] == parties[8]:
                            NPS8.append(similarity)
                        elif df.loc[x, 1] == parties[9]:
                            NPS9.append(similarity)
                        elif df.loc[x, 1] == parties[10]:
                            NPS10.append(similarity)
                        elif df.loc[x, 1] == parties[11]:
                            NPS11.append(similarity)
                        elif df.loc[x, 1] == parties[12]:
                            NPS12.append(similarity)
                        elif df.loc[x, 1] == parties[13]:
                            NPS13.append(similarity)

#Levenshtein Similarity based on nothing.
for i in ageSheetNames:
    data = pd.read_excel("LevenshteinData.xlsx", sheet_name=i)
    if i == "Controversieel Leeftijd":
        df = pd.DataFrame(data, columns=["Wat is uw leeftijd?", "Abortus tot hoeveel weken?", "Oorzaken klimaatverandering","Zwarte piet of roetveegpiet?", "Gevaren vaccinaties","Gevolgen illegale immigratie"])
        df = df.rename(columns={"Wat is uw leeftijd?": 1, "Abortus tot hoeveel weken?": 2, "Oorzaken klimaatverandering": 3,"Zwarte piet of roetveegpiet?": 4, "Gevaren vaccinaties": 5, "Gevolgen illegale immigratie": 6})
    else:
        df = pd.DataFrame(data, columns=["Wat is uw leeftijd?", "Brood bakken recept", "Honden namen","Wat is het grootste bot in het menselijk lichaam?","Hoeveel van een komkommer is water?","Hoeveel mensen wonen er in Nederland?"])
        df = df.rename(columns={"Wat is uw leeftijd?": 1, "Brood bakken recept": 2, "Honden namen": 3,"Wat is het grootste bot in het menselijk lichaam?": 4,"Hoeveel van een komkommer is water?": 5, "Hoeveel mensen wonen er in Nederland?": 6})
    for x in range(len(df)):
        for y in range(2, 7):
            stringOfWebsites = df.loc[x, y]
            websiteList = re.split("\s", stringOfWebsites)
            websiteList = websiteList[:smallestWebsiteList]
            for z in websiteList:
                if z not in allWebsites:
                    allWebsites.append(z)
            for xx in range(len(df)):
                if x == xx:
                    pass
                elif x > xx:
                    pass
                else:
                    stringOfComparingWebsites = df.loc[xx, y]
                    comparingWebsiteList = re.split("\s", stringOfComparingWebsites)
                    comparingWebsiteList = comparingWebsiteList[:smallestWebsiteList]
                    similarity = SimilarityCalc(websiteList, comparingWebsiteList)
                    if i == "Controversieel Leeftijd":
                        CS.append(similarity)
                    else:
                        NS.append(similarity)

#Levenshtein Similarity based on political left and right.
for i in partySheetNames:
    data = pd.read_excel("LevenshteinData.xlsx", sheet_name=i)
    if i == "Controversieel Partij":
        df = pd.DataFrame(data, columns=["Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?", "Abortus tot hoeveel weken?", "Oorzaken klimaatverandering", "Zwarte piet of roetveegpiet?", "Gevaren vaccinaties", "Gevolgen illegale immigratie"])
        df = df.rename(columns={"Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?": 1, "Abortus tot hoeveel weken?": 2, "Oorzaken klimaatverandering": 3, "Zwarte piet of roetveegpiet?": 4, "Gevaren vaccinaties": 5, "Gevolgen illegale immigratie": 6})
    else:
        df = pd.DataFrame(data, columns=["Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?", "Brood bakken recept", "Honden namen", "Wat is het grootste bot in het menselijk lichaam?", "Hoeveel van een komkommer is water?", "Hoeveel mensen wonen er in Nederland?"])
        df = df.rename(columns={"Op welke politieke partij heeft u bij de laatste tweede-kamer verkiezingen gestemd?": 1, "Brood bakken recept": 2, "Honden namen": 3, "Wat is het grootste bot in het menselijk lichaam?": 4, "Hoeveel van een komkommer is water?": 5, "Hoeveel mensen wonen er in Nederland?": 6})
    for x in range(len(df)):
        for y in range(2, 7):
            stringOfWebsites = df.loc[x, y]
            websiteList = re.split("\s", stringOfWebsites)
            websiteList = websiteList[:smallestWebsiteList]
            for xx in range(len(df)):
                if x == xx:
                    pass
                elif x > xx:
                    pass
                elif df.loc[x, 1] in spectrumLeft and df.loc[xx, 1] in spectrumLeft:
                    stringOfComparingWebsites = df.loc[xx, y]
                    comparingWebsiteList = re.split("\s", stringOfComparingWebsites)
                    comparingWebsiteList = comparingWebsiteList[:smallestWebsiteList]
                    similarity = SimilarityCalc(websiteList, comparingWebsiteList)
                    if i == "Controversieel Partij":
                        CSSLeft.append(similarity)
                    else:
                        NSSLeft.append(similarity)
                elif df.loc[x, 1] in spectrumRight and df.loc[xx, 1] in spectrumRight:
                    stringOfComparingWebsites = df.loc[xx, y]
                    comparingWebsiteList = re.split("\s", stringOfComparingWebsites)
                    comparingWebsiteList = comparingWebsiteList[:smallestWebsiteList]
                    similarity = SimilarityCalc(websiteList, comparingWebsiteList)
                    if i == "Controversieel Partij":
                        CSSRight.append(similarity)
                    else:
                        NSSRight.append(similarity)

#Levenshtein Similarity based on search query.
for i in ageSheetNames:
    data = pd.read_excel("LevenshteinData.xlsx", sheet_name=i)
    if i == "Controversieel Leeftijd":
        df = pd.DataFrame(data, columns=["Wat is uw leeftijd?", "Abortus tot hoeveel weken?", "Oorzaken klimaatverandering","Zwarte piet of roetveegpiet?", "Gevaren vaccinaties","Gevolgen illegale immigratie"])
        df = df.rename(columns={"Wat is uw leeftijd?": 1, "Abortus tot hoeveel weken?": 2, "Oorzaken klimaatverandering": 3,"Zwarte piet of roetveegpiet?": 4, "Gevaren vaccinaties": 5, "Gevolgen illegale immigratie": 6})
    elif i == "Niet Controversieel Leeftijd":
        df = pd.DataFrame(data, columns=["Wat is uw leeftijd?", "Brood bakken recept", "Honden namen","Wat is het grootste bot in het menselijk lichaam?","Hoeveel van een komkommer is water?","Hoeveel mensen wonen er in Nederland?"])
        df = df.rename(columns={"Wat is uw leeftijd?": 1, "Brood bakken recept": 2, "Honden namen": 3,"Wat is het grootste bot in het menselijk lichaam?": 4,"Hoeveel van een komkommer is water?": 5, "Hoeveel mensen wonen er in Nederland?": 6})
    for x in range(len(df)):
        for y in range(2, 7):
            stringOfWebsites = df.loc[x, y]
            websiteList = re.split("\s", stringOfWebsites)
            websiteList = websiteList[:smallestWebsiteList]
            for z in websiteList:
                if z not in allWebsites:
                    allWebsites.append(z)
            for xx in range(len(df)):
                if x == xx:
                    pass
                elif x > xx:
                    pass
                else:
                    stringOfComparingWebsites = df.loc[xx, y]
                    comparingWebsiteList = re.split("\s", stringOfComparingWebsites)
                    comparingWebsiteList = comparingWebsiteList[:smallestWebsiteList]
                    similarity = SimilarityCalc(websiteList, comparingWebsiteList)
                    if i == "Controversieel Leeftijd":
                        if y == 2:
                            CTS0.append(similarity)
                        elif y == 3:
                            CTS1.append(similarity)
                        elif y == 4:
                            CTS2.append(similarity)
                        elif y == 5:
                            CTS3.append(similarity)
                        elif y == 6:
                            CTS4.append(similarity)
                    else:
                        if y == 2:
                            NTS0.append(similarity)
                        elif y == 3:
                            NTS1.append(similarity)
                        elif y == 4:
                            NTS2.append(similarity)
                        elif y == 5:
                            NTS3.append(similarity)
                        elif y == 6:
                            NTS4.append(similarity)

#Make averages of the groups
for x in CAS:
    if x != []:
        y = Average(x)
        CASAverage.append(y)
    else:
        CASAverage.append(0)
for x in NAS:
    if x != []:
        y = Average(x)
        NASAverage.append(y)
    else:
        NASAverage.append(0)
for x in CLS:
    if x != []:
        y = Average(x)
        CLSAverage.append(y)
    else:
        CLSAverage.append(0)
for x in NLS:
    if x != []:
        y = Average(x)
        NLSAverage.append(y)
    else:
        NLSAverage.append(0)
for x in CPS:
    if x != []:
        y = Average(x)
        CPSAverage.append(y)
    else:
        CPSAverage.append(0)
for x in NPS:
    if x != []:
        y = Average(x)
        NPSAverage.append(y)
    else:
        NPSAverage.append(0)
for x in CTS:
    if x != []:
        y = Average(x)
        CTSAverage.append(y)
    else:
        CTSAverage.append(0)
for x in NTS:
    if x != []:
        y = Average(x)
        NTSAverage.append(y)
    else:
        NTSAverage.append(0)
CSAverage = Average(CS)
NSAverage = Average(NS)
CSSLeftAverage = Average(CSSLeft)
CSSRightAverage = Average(CSSRight)
NSSLeftAverage = Average(NSSLeft)
NSSRightAverage = Average(NSSRight)

print("Sorted By Age:")
if rawResults:
    print("Controversial:")
    print(f'Similarities between {ageGroups[0]}: {CAS0}\nSimilarities between {ageGroups[1]}: {CAS1}\nSimilarities between {ageGroups[2]}: {CAS2}\nSimilarities between {ageGroups[3]}: {CAS3}\nSimilarities between {ageGroups[4]}: {CAS4}\nSimilarities between {ageGroups[5]}: {CAS5}\n')
    print("Normal:")
    print(f'Similarities between {ageGroups[0]}: {NAS0}\nSimilarities between {ageGroups[1]}: {NAS1}\nSimilarities between {ageGroups[2]}: {NAS2}\nSimilarities between {ageGroups[3]}: {NAS3}\nSimilarities between {ageGroups[4]}: {NAS4}\nSimilarities between {ageGroups[5]}: {NAS5}\n')
print("Averages of the groups:")
print("Controversial:")
print(f'Average Similarity for {ageGroups[0]}: {CASAverage[0]}\nAverage Similarity for {ageGroups[1]}: {CASAverage[1]}\nAverage Similarity for {ageGroups[2]}: {CASAverage[2]}\nAverage Similarity for {ageGroups[3]}: {CASAverage[3]}\nAverage Similarity for {ageGroups[4]}: {CASAverage[4]}\nAverage Similarity for {ageGroups[5]}: {CASAverage[5]}\n')
print("Normal:")
print(f'Average Similarity for {ageGroups[0]}: {NASAverage[0]}\nAverage Similarity for {ageGroups[1]}: {NASAverage[1]}\nAverage Similarity for {ageGroups[2]}: {NASAverage[2]}\nAverage Similarity for {ageGroups[3]}: {NASAverage[3]}\nAverage Similarity for {ageGroups[4]}: {NASAverage[4]}\nAverage Similarity for {ageGroups[5]}: {NASAverage[5]}\n')

print("Sorted By Location:")
if rawResults:
    print("Controversial:")
    print(f'Similarities between {locations[0]}: {CLS0}\nSimilarities between {locations[1]}: {CLS1}\nSimilarities between {locations[2]}: {CLS2}\nSimilarities between {locations[3]}: {CLS3}\nSimilarities between {locations[4]}: {CLS4}\nSimilarities between {locations[5]}: {CLS5}\nSimilarities between {locations[6]}: {CLS6}\nSimilarities between {locations[7]}: {CLS7}\nSimilarities between {locations[8]}: {CLS8}\nSimilarities between {locations[9]}: {CLS9}\nSimilarities between {locations[10]}: {CLS10}\nSimilarities between {locations[11]}: {CLS11}\nSimilarities between {locations[12]}: {CLS12}\n')
    print("Normal:")
    print(f'Similarities between {locations[0]}: {NLS0}\nSimilarities between {locations[1]}: {NLS1}\nSimilarities between {locations[2]}: {NLS2}\nSimilarities between {locations[3]}: {NLS3}\nSimilarities between {locations[4]}: {NLS4}\nSimilarities between {locations[5]}: {NLS5}\nSimilarities between {locations[6]}: {NLS6}\nSimilarities between {locations[7]}: {NLS7}\nSimilarities between {locations[8]}: {NLS8}\nSimilarities between {locations[9]}: {NLS9}\nSimilarities between {locations[10]}: {NLS10}\nSimilarities between {locations[11]}: {NLS11}\nSimilarities between {locations[12]}: {NLS12}\n')
print("Averages of the groups:")
print("Controversial:")
print(f'Average Similarity for {locations[0]}: {CLSAverage[0]}\nAverage Similarity for {locations[1]}: {CLSAverage[1]}\nAverage Similarity for {locations[2]}: {CLSAverage[2]}\nAverage Similarity for {locations[3]}: {CLSAverage[3]}\nAverage Similarity for {locations[4]}: {CLSAverage[4]}\nAverage Similarity for {locations[5]}: {CLSAverage[5]}\nAverage Similarity for {locations[6]}: {CLSAverage[6]}\nAverage Similarity for {locations[7]}: {CLSAverage[7]}\nAverage Similarity for {locations[8]}: {CLSAverage[8]}\nAverage Similarity for {locations[9]}: {CLSAverage[9]}\nAverage Similarity for {locations[10]}: {CLSAverage[10]}\nAverage Similarity for {locations[11]}: {CLSAverage[11]}\nAverage Similarity for {locations[12]}: {CLSAverage[12]}\n')
print("Normal:")
print(f'Average Similarity for {locations[0]}: {NLSAverage[0]}\nAverage Similarity for {locations[1]}: {NLSAverage[1]}\nAverage Similarity for {locations[2]}: {NLSAverage[2]}\nAverage Similarity for {locations[3]}: {NLSAverage[3]}\nAverage Similarity for {locations[4]}: {NLSAverage[4]}\nAverage Similarity for {locations[5]}: {NLSAverage[5]}\nAverage Similarity for {locations[6]}: {NLSAverage[6]}\nAverage Similarity for {locations[7]}: {NLSAverage[7]}\nAverage Similarity for {locations[8]}: {NLSAverage[8]}\nAverage Similarity for {locations[9]}: {NLSAverage[9]}\nAverage Similarity for {locations[10]}: {NLSAverage[10]}\nAverage Similarity for {locations[11]}: {NLSAverage[11]}\nAverage Similarity for {locations[12]}: {NLSAverage[12]}\n')

print("Sorted By Party:")
if rawResults:
    print("Controversial:")
    print(f'Similarities between {parties[0]}: {CPS0}\nSimilarities between {parties[1]}: {CPS1}\nSimilarities between {parties[2]}: {CPS2}\nSimilarities between {parties[3]}: {CPS3}\nSimilarities between {parties[4]}: {CPS4}\nSimilarities between {parties[5]}: {CPS5}\nSimilarities between {parties[6]}: {CPS6}\nSimilarities between {parties[7]}: {CPS7}\nSimilarities between {parties[8]}: {CPS8}\nSimilarities between {parties[9]}: {CPS9}\nSimilarities between {parties[10]}: {CPS10}\nSimilarities between {parties[11]}: {CPS11}\nSimilarities between {parties[12]}: {CPS12}\nSimilarities between {parties[13]}: {CPS13}\n')
    print("Normal:")
    print(f'Similarities between {parties[0]}: {NPS0}\nSimilarities between {parties[1]}: {NPS1}\nSimilarities between {parties[2]}: {NPS2}\nSimilarities between {parties[3]}: {NPS3}\nSimilarities between {parties[4]}: {NPS4}\nSimilarities between {parties[5]}: {NPS5}\nSimilarities between {parties[6]}: {NPS6}\nSimilarities between {parties[7]}: {NPS7}\nSimilarities between {parties[8]}: {NPS8}\nSimilarities between {parties[9]}: {NPS9}\nSimilarities between {parties[10]}: {NPS10}\nSimilarities between {parties[11]}: {NPS11}\nSimilarities between {parties[12]}: {NPS12}\nSimilarities between {parties[13]}: {CPS13}\n')
print("Averages of the groups:")
print("Controversial:")
print(f'Average Similarity for {parties[0]}: {CPSAverage[0]}\nAverage Similarity for {parties[1]}: {CPSAverage[1]}\nAverage Similarity for {parties[2]}: {CPSAverage[2]}\nAverage Similarity for {parties[3]}: {CPSAverage[3]}\nAverage Similarity for {parties[4]}: {CPSAverage[4]}\nAverage Similarity for {parties[5]}: {CPSAverage[5]}\nAverage Similarity for {parties[6]}: {CPSAverage[6]}\nAverage Similarity for {parties[7]}: {CPSAverage[7]}\nAverage Similarity for {parties[8]}: {CPSAverage[8]}\nAverage Similarity for {parties[9]}: {CPSAverage[9]}\nAverage Similarity for {parties[10]}: {CPSAverage[10]}\nAverage Similarity for {parties[11]}: {CPSAverage[11]}\nAverage Similarity for {parties[12]}: {CPSAverage[12]}\nAverage Similarity for {parties[13]}: {CPSAverage[13]}\n')
print("Normal:")
print(f'Average Similarity for {parties[0]}: {NPSAverage[0]}\nAverage Similarity for {parties[1]}: {NPSAverage[1]}\nAverage Similarity for {parties[2]}: {NPSAverage[2]}\nAverage Similarity for {parties[3]}: {NPSAverage[3]}\nAverage Similarity for {parties[4]}: {NPSAverage[4]}\nAverage Similarity for {parties[5]}: {NPSAverage[5]}\nAverage Similarity for {parties[6]}: {NPSAverage[6]}\nAverage Similarity for {parties[7]}: {NPSAverage[7]}\nAverage Similarity for {parties[8]}: {NPSAverage[8]}\nAverage Similarity for {parties[9]}: {NPSAverage[9]}\nAverage Similarity for {parties[10]}: {NPSAverage[10]}\nAverage Similarity for {parties[11]}: {NPSAverage[11]}\nAverage Similarity for {parties[12]}: {NPSAverage[12]}\nAverage Similarity for {parties[13]}: {NPSAverage[13]}\n')

print("Unsorted:")
print("Average:")
print("Controversial:")
print(f'Average Similarity: {CSAverage}\n')
print("Normal:")
print(f'Average Similarity: {NSAverage}\n')

print("Political Spectrum:")
print("Average:")
print("Controversial:")
print(f'Average Similarity Left: {CSSLeftAverage}\nAverage Similarity Right: {CSSRightAverage}\n')
print("Normal:")
print(f'Average Similarity Left: {NSSLeftAverage}\nAverage Similarity Right: {NSSRightAverage}\n')

print("Sorted By Topic:")
if rawResults:
    print("Controversial:")
    print(f'Similarities between {controversialTopics[0]}: {CTS0}\nSimilarities between {controversialTopics[1]}: {CTS1}\nSimilarities between {controversialTopics[2]}: {CTS2}\nSimilarities between {controversialTopics[3]}: {CTS3}\nSimilarities between {controversialTopics[4]}: {CTS4}\n')
    print("Normal:")
    print(f'Similarities between {normalTopics[0]}: {NTS0}\nSimilarities between {normalTopics[1]}: {NTS1}\nSimilarities between {normalTopics[2]}: {NTS2}\nSimilarities between {normalTopics[3]}: {NTS3}\nSimilarities between {normalTopics[4]}: {NTS4}\n')
print("Averages of the topics:")
print("Controversial:")
print(f'Average Similarity for {controversialTopics[0]}: {CTSAverage[0]}\nAverage Similarity for {controversialTopics[1]}: {CTSAverage[1]}\nAverage Similarity for {controversialTopics[2]}: {CTSAverage[2]}\nAverage Similarity for {controversialTopics[3]}: {CTSAverage[3]}\nAverage Similarity for {controversialTopics[4]}: {CTSAverage[4]}\n')
print("Normal:")
print(f'Average Similarity for {normalTopics[0]}: {NTSAverage[0]}\nAverage Similarity for {normalTopics[1]}: {NTSAverage[1]}\nAverage Similarity for {normalTopics[2]}: {NTSAverage[2]}\nAverage Similarity for {normalTopics[3]}: {NTSAverage[3]}\nAverage Similarity for {normalTopics[4]}: {NTSAverage[4]}\n')


print(allWebsites)