import pandas as pd
import textdistance as td
import re
import statistics
import numpy as np
from scipy import stats

ageSheetNames = ("Controversieel Leeftijd", "Niet Controversieel Leeftijd")
locationSheetNames = ("Controversieel Locatie", "Niet Controversieel Locatie")
partySheetNames = ("Controversieel Partij", "Niet Controversieel Partij")
columnNamesControversial = ("Abortus tot hoeveel weken?","Oorzaken klimaatverandering","Zwarte piet of roetveegpiet?","Gevaren vaccinaties","Gevolgen illegale immigratie")
columnNamesNonControversial = ("Brood bakken recept", "Honden namen", "Wat is het grootste bot in het menselijk lichaam?", "Hoeveel van een komkommer is water?", "Hoeveel mensen wonen er in Nederland?")
smallestWebsiteList = 8
comparisons = 0
rawResults = True
allWebsites = []


#Different groups in the three categories
ageGroups = ['<18', '18 - 24', '25 - 34', '35 - 44', '45 - 54', '>55'] #6 groups
locations = ['Buiten Nederland', 'Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant', 'Noord-Holland', 'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland'] #13 groups
parties = ['CDA', 'ChristenUnie', 'DENK', 'D66', 'FvD', 'GroenLinks', 'Niet', 'PvdA', 'PvdD', 'PVV', 'SGP', 'SP', '50PLUS', 'VVD'] #14 groups
spectrumLeft = ['DENK', 'D66', 'GroenLinks', 'PvdA', 'PvdD', 'SP']
spectrumRight = ['CDA', 'ChristenUnie', 'FvD', 'PVV', 'SGP', '50PLUS', 'VVD']
controversialTopics = ['Abortus', 'Klimaatverandering', 'Zwartepiet', 'Vaccinaties', 'Immigratie']
normalTopics = ['Brood', 'Honden', 'Bot', 'Komkommer', 'Inwoners']
#The different groups in the category of age
#ControversialAgeDistances: CAD
CAD0 = []
CAD1 = []
CAD2 = []
CAD3 = []
CAD4 = []
CAD5 = []
#NormalAgeDistances: NAD
NAD0 = []
NAD1 = []
NAD2 = []
NAD3 = []
NAD4 = []
NAD5 = []
#The different groups in the category of location
#ControversialLocationDistances: CLD
CLD0 = []
CLD1 = []
CLD2 = []
CLD3 = []
CLD4 = []
CLD5 = []
CLD6 = []
CLD7 = []
CLD8 = []
CLD9 = []
CLD10 = []
CLD11 = []
CLD12 = []
#NormalLocationDistances: NLD
NLD0 = []
NLD1 = []
NLD2 = []
NLD3 = []
NLD4 = []
NLD5 = []
NLD6 = []
NLD7 = []
NLD8 = []
NLD9 = []
NLD10 = []
NLD11 = []
NLD12 = []
#The different groups in the category of political parties
#ControversialPoliticalDistance: CPD
CPD0 = []
CPD1 = []
CPD2 = []
CPD3 = []
CPD4 = []
CPD5 = []
CPD6 = []
CPD7 = []
CPD8 = []
CPD9 = []
CPD10 = []
CPD11 = []
CPD12 = []
CPD13 = []
#NormalPoliticalDistance: NPD
NPD0 = []
NPD1 = []
NPD2 = []
NPD3 = []
NPD4 = []
NPD5 = []
NPD6 = []
NPD7 = []
NPD8 = []
NPD9 = []
NPD10 = []
NPD11 = []
NPD12 = []
NPD13 = []
#ControversialSpectrumDistance: CSD
CSDLeft = []
CSDRight = []
#NormalSpectrumDistance: NSD
NSDLeft = []
NSDRight = []
#ControversialDistance: CD
CD = []
#NormalDistance: ND
ND = []
#ControversialTopicDistance: CTD
CTD0 = []
CTD1 = []
CTD2 = []
CTD3 = []
CTD4 = []
#NormalTopicDistance: NTD
NTD0 = []
NTD1 = []
NTD2 = []
NTD3 = []
NTD4 = []
#Lists of all groups:
CAD = [CAD0, CAD1, CAD2, CAD3, CAD4, CAD5]
NAD = [NAD0, NAD1, NAD2, NAD3, NAD4, NAD5]
CLD = [CLD0, CLD1, CLD2, CLD3, CLD4, CLD5, CLD6, CLD7, CLD8, CLD9, CLD10, CLD11, CLD12]
NLD = [NLD0, NLD1, NLD2, NLD3, NLD4, NLD5, NLD6, NLD7, NLD8, NLD9, NLD10, NLD11, NLD12]
CPD = [CPD0, CPD1, CPD2, CPD3, CPD4, CPD5, CPD6, CPD7, CPD8, CPD9, CPD10, CPD11, CPD12, CPD13]
NPD = [NPD0, NPD1, NPD2, NPD3, NPD4, NPD5, NPD6, NPD7, NPD8, NPD9, NPD10, NPD11, NPD12, NPD13]
CSD = [CSDLeft, CSDRight]
NSD = [NSDLeft, NSDRight]
CTD = [CTD0, CTD1, CTD2, CTD3, CTD4]
NTD = [NTD0, NTD1, NTD2, NTD3, NTD4]
#Average of the groups
CADAverage = []
NADAverage = []
CLDAverage = []
NLDAverage = []
CPDAverage = []
NPDAverage = []
CDAverage = 0
NDAverage = 0
CSDLeftAverage = 0
CSDRightAverage = 0
NSDLeftAverage = 0
NSDRightAverage = 0
CTDAverage = []
NTDAverage = []

def Average(lst):
    return sum(lst) / len(lst)

def Similarity(lst1, lst2):
    similarity = 0
    similarElements = []
    for listElement in lst1:
        if listElement in lst2:
            if listElement not in similarElements:
                similarElements.append(listElement)
                similarity += 1
    return similarity


#Levenshtein distance based on age
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
                    distance = td.levenshtein.distance(websiteList, comparingWebsiteList)
                    if i == "Controversieel Leeftijd":
                        if df.loc[x, 1] == ageGroups[0]:
                            CAD0.append(distance)
                        elif df.loc[x, 1] == ageGroups[1]:
                            CAD1.append(distance)
                        elif df.loc[x, 1] == ageGroups[2]:
                            CAD2.append(distance)
                        elif df.loc[x, 1] == ageGroups[3]:
                            CAD3.append(distance)
                        elif df.loc[x, 1] == ageGroups[4]:
                            CAD4.append(distance)
                        elif df.loc[x, 1] == ageGroups[5]:
                            CAD5.append(distance)
                    else:
                        if df.loc[x, 1] == ageGroups[0]:
                            NAD0.append(distance)
                        elif df.loc[x, 1] == ageGroups[1]:
                            NAD1.append(distance)
                        elif df.loc[x, 1] == ageGroups[2]:
                            NAD2.append(distance)
                        elif df.loc[x, 1] == ageGroups[3]:
                            NAD3.append(distance)
                        elif df.loc[x, 1] == ageGroups[4]:
                            NAD4.append(distance)
                        elif df.loc[x, 1] == ageGroups[5]:
                            NAD5.append(distance)

#Levenshtein distance based on location.
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
                    distance = td.levenshtein.distance(websiteList, comparingWebsiteList)
                    if i == "Controversieel Locatie":
                        if df.loc[x, 1] == locations[0]:
                            CLD0.append(distance)
                        elif df.loc[x, 1] == locations[1]:
                            CLD1.append(distance)
                        elif df.loc[x, 1] == locations[2]:
                            CLD2.append(distance)
                        elif df.loc[x, 1] == locations[3]:
                            CLD3.append(distance)
                        elif df.loc[x, 1] == locations[4]:
                            CLD4.append(distance)
                        elif df.loc[x, 1] == locations[5]:
                            CLD5.append(distance)
                        elif df.loc[x, 1] == locations[6]:
                            CLD6.append(distance)
                        elif df.loc[x, 1] == locations[7]:
                            CLD7.append(distance)
                        elif df.loc[x, 1] == locations[8]:
                            CLD8.append(distance)
                        elif df.loc[x, 1] == locations[9]:
                            CLD9.append(distance)
                        elif df.loc[x, 1] == locations[10]:
                            CLD10.append(distance)
                        elif df.loc[x, 1] == locations[11]:
                            CLD11.append(distance)
                        elif df.loc[x, 1] == locations[12]:
                            CLD12.append(distance)
                    else:
                        if df.loc[x, 1] == locations[0]:
                            NLD0.append(distance)
                        elif df.loc[x, 1] == locations[1]:
                            NLD1.append(distance)
                        elif df.loc[x, 1] == locations[2]:
                            NLD2.append(distance)
                        elif df.loc[x, 1] == locations[3]:
                            NLD3.append(distance)
                        elif df.loc[x, 1] == locations[4]:
                            NLD4.append(distance)
                        elif df.loc[x, 1] == locations[5]:
                            NLD5.append(distance)
                        elif df.loc[x, 1] == locations[6]:
                            NLD6.append(distance)
                        elif df.loc[x, 1] == locations[7]:
                            NLD7.append(distance)
                        elif df.loc[x, 1] == locations[8]:
                            NLD8.append(distance)
                        elif df.loc[x, 1] == locations[9]:
                            NLD9.append(distance)
                        elif df.loc[x, 1] == locations[10]:
                            NLD10.append(distance)
                        elif df.loc[x, 1] == locations[11]:
                            NLD11.append(distance)
                        elif df.loc[x, 1] == locations[12]:
                            NLD12.append(distance)


#Levenshtein distance based on political affiliation.
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
                    distance = td.levenshtein.distance(websiteList, comparingWebsiteList)
                    if i == "Controversieel Partij":
                        if df.loc[x, 1] == parties[0]:
                            CPD0.append(distance)
                        elif df.loc[x, 1] == parties[1]:
                            CPD1.append(distance)
                        elif df.loc[x, 1] == parties[2]:
                            CPD2.append(distance)
                        elif df.loc[x, 1] == parties[3]:
                            CPD3.append(distance)
                        elif df.loc[x, 1] == parties[4]:
                            CPD4.append(distance)
                        elif df.loc[x, 1] == parties[5]:
                            CPD5.append(distance)
                        elif df.loc[x, 1] == parties[6]:
                            CPD6.append(distance)
                        elif df.loc[x, 1] == parties[7]:
                            CPD7.append(distance)
                        elif df.loc[x, 1] == parties[8]:
                            CPD8.append(distance)
                        elif df.loc[x, 1] == parties[9]:
                            CPD9.append(distance)
                        elif df.loc[x, 1] == parties[10]:
                            CPD10.append(distance)
                        elif df.loc[x, 1] == parties[11]:
                            CPD11.append(distance)
                        elif df.loc[x, 1] == parties[12]:
                            CPD12.append(distance)
                        elif df.loc[x, 1] == parties[13]:
                            CPD13.append(distance)
                    else:
                        if df.loc[x, 1] == parties[0]:
                            NPD0.append(distance)
                        elif df.loc[x, 1] == parties[1]:
                            NPD1.append(distance)
                        elif df.loc[x, 1] == parties[2]:
                            NPD2.append(distance)
                        elif df.loc[x, 1] == parties[3]:
                            NPD3.append(distance)
                        elif df.loc[x, 1] == parties[4]:
                            NPD4.append(distance)
                        elif df.loc[x, 1] == parties[5]:
                            NPD5.append(distance)
                        elif df.loc[x, 1] == parties[6]:
                            NPD6.append(distance)
                        elif df.loc[x, 1] == parties[7]:
                            NPD7.append(distance)
                        elif df.loc[x, 1] == parties[8]:
                            NPD8.append(distance)
                        elif df.loc[x, 1] == parties[9]:
                            NPD9.append(distance)
                        elif df.loc[x, 1] == parties[10]:
                            NPD10.append(distance)
                        elif df.loc[x, 1] == parties[11]:
                            NPD11.append(distance)
                        elif df.loc[x, 1] == parties[12]:
                            NPD12.append(distance)
                        elif df.loc[x, 1] == parties[13]:
                            NPD13.append(distance)

#Levenshtein distance based on nothing.
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
                    distance = td.levenshtein.distance(websiteList, comparingWebsiteList)
                    if i == "Controversieel Leeftijd":
                        CD.append(distance)
                    else:
                        ND.append(distance)

#Levenshtein distance based on political left and right.
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
                    distance = td.levenshtein.distance(websiteList, comparingWebsiteList)
                    if i == "Controversieel Partij":
                        CSDLeft.append(distance)
                    else:
                        NSDLeft.append(distance)
                elif df.loc[x, 1] in spectrumRight and df.loc[xx, 1] in spectrumRight:
                    stringOfComparingWebsites = df.loc[xx, y]
                    comparingWebsiteList = re.split("\s", stringOfComparingWebsites)
                    comparingWebsiteList = comparingWebsiteList[:smallestWebsiteList]
                    distance = td.levenshtein.distance(websiteList, comparingWebsiteList)
                    if i == "Controversieel Partij":
                        CSDRight.append(distance)
                    else:
                        NSDRight.append(distance)

#Levenshtein distance based on search query.
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
                    distance = td.levenshtein.distance(websiteList, comparingWebsiteList)
                    if i == "Controversieel Leeftijd":
                        if y == 2:
                            CTD0.append(distance)
                        elif y == 3:
                            CTD1.append(distance)
                        elif y == 4:
                            CTD2.append(distance)
                        elif y == 5:
                            CTD3.append(distance)
                        elif y == 6:
                            CTD4.append(distance)
                    else:
                        if y == 2:
                            NTD0.append(distance)
                        elif y == 3:
                            NTD1.append(distance)
                        elif y == 4:
                            NTD2.append(distance)
                        elif y == 5:
                            NTD3.append(distance)
                        elif y == 6:
                            NTD4.append(distance)

#Make averages of the groups
for x in CAD:
    if x != []:
        y = Average(x)
        CADAverage.append(y)
    else:
        CADAverage.append(0)
for x in NAD:
    if x != []:
        y = Average(x)
        NADAverage.append(y)
    else:
        NADAverage.append(0)
for x in CLD:
    if x != []:
        y = Average(x)
        CLDAverage.append(y)
    else:
        CLDAverage.append(0)
for x in NLD:
    if x != []:
        y = Average(x)
        NLDAverage.append(y)
    else:
        NLDAverage.append(0)
for x in CPD:
    if x != []:
        y = Average(x)
        CPDAverage.append(y)
    else:
        CPDAverage.append(0)
for x in NPD:
    if x != []:
        y = Average(x)
        NPDAverage.append(y)
    else:
        NPDAverage.append(0)
for x in CTD:
    if x != []:
        y = Average(x)
        CTDAverage.append(y)
    else:
        CTDAverage.append(0)
for x in NTD:
    if x != []:
        y = Average(x)
        NTDAverage.append(y)
    else:
        NTDAverage.append(0)
CDAverage = Average(CD)
NDAverage = Average(ND)
CSDLeftAverage = Average(CSDLeft)
CSDRightAverage = Average(CSDRight)
NSDLeftAverage = Average(NSDLeft)
NSDRightAverage = Average(NSDRight)
#ControversialStandardDeviation = statistics.stdev(CD)
ControversialStandardDeviation = np.std(CD)
#NormalStandardDeviation = statistics.stdev(ND)
NormalStandardDeviation = np.std(ND)
#ControversialMean = statistics.mean(CD)
ControversialMean = np.mean(CD)
#NormalMean = statistics.mean(ND)
NormalMean = np.mean(ND)
#ControversialVariance = statistics.variance(CD, ControversialMean)
ControversialVariance = np.var(CD)
#NormalVariance = statistics.variance(ND, NormalMean)
NormalVariance = np.var(ND)
ControversialSize = len(CD)
NormalSize = len(ND)
EqualTtest = stats.ttest_ind(ND, CD)
UnEqualTtest = stats.ttest_ind(ND, CD, equal_var= False)

print("Sorted By Age:")
if rawResults:
    print("Controversial:")
    print(f'Distances between {ageGroups[0]}: {CAD0}\nDistances between {ageGroups[1]}: {CAD1}\nDistances between {ageGroups[2]}: {CAD2}\nDistances between {ageGroups[3]}: {CAD3}\nDistances between {ageGroups[4]}: {CAD4}\nDistances between {ageGroups[5]}: {CAD5}\n')
    print("Normal:")
    print(f'Distances between {ageGroups[0]}: {NAD0}\nDistances between {ageGroups[1]}: {NAD1}\nDistances between {ageGroups[2]}: {NAD2}\nDistances between {ageGroups[3]}: {NAD3}\nDistances between {ageGroups[4]}: {NAD4}\nDistances between {ageGroups[5]}: {NAD5}\n')
print("Averages of the groups:")
print("Controversial:")
print(f'Average distance for {ageGroups[0]}: {CADAverage[0]}\nAverage distance for {ageGroups[1]}: {CADAverage[1]}\nAverage distance for {ageGroups[2]}: {CADAverage[2]}\nAverage distance for {ageGroups[3]}: {CADAverage[3]}\nAverage distance for {ageGroups[4]}: {CADAverage[4]}\nAverage distance for {ageGroups[5]}: {CADAverage[5]}\n')
print("Normal:")
print(f'Average distance for {ageGroups[0]}: {NADAverage[0]}\nAverage distance for {ageGroups[1]}: {NADAverage[1]}\nAverage distance for {ageGroups[2]}: {NADAverage[2]}\nAverage distance for {ageGroups[3]}: {NADAverage[3]}\nAverage distance for {ageGroups[4]}: {NADAverage[4]}\nAverage distance for {ageGroups[5]}: {NADAverage[5]}\n')

print("Sorted By Location:")
if rawResults:
    print("Controversial:")
    print(f'Distances between {locations[0]}: {CLD0}\nDistances between {locations[1]}: {CLD1}\nDistances between {locations[2]}: {CLD2}\nDistances between {locations[3]}: {CLD3}\nDistances between {locations[4]}: {CLD4}\nDistances between {locations[5]}: {CLD5}\nDistances between {locations[6]}: {CLD6}\nDistances between {locations[7]}: {CLD7}\nDistances between {locations[8]}: {CLD8}\nDistances between {locations[9]}: {CLD9}\nDistances between {locations[10]}: {CLD10}\nDistances between {locations[11]}: {CLD11}\nDistances between {locations[12]}: {CLD12}\n')
    print("Normal:")
    print(f'Distances between {locations[0]}: {NLD0}\nDistances between {locations[1]}: {NLD1}\nDistances between {locations[2]}: {NLD2}\nDistances between {locations[3]}: {NLD3}\nDistances between {locations[4]}: {NLD4}\nDistances between {locations[5]}: {NLD5}\nDistances between {locations[6]}: {NLD6}\nDistances between {locations[7]}: {NLD7}\nDistances between {locations[8]}: {NLD8}\nDistances between {locations[9]}: {NLD9}\nDistances between {locations[10]}: {NLD10}\nDistances between {locations[11]}: {NLD11}\nDistances between {locations[12]}: {NLD12}\n')
print("Averages of the groups:")
print("Controversial:")
print(f'Average distance for {locations[0]}: {CLDAverage[0]}\nAverage distance for {locations[1]}: {CLDAverage[1]}\nAverage distance for {locations[2]}: {CLDAverage[2]}\nAverage distance for {locations[3]}: {CLDAverage[3]}\nAverage distance for {locations[4]}: {CLDAverage[4]}\nAverage distance for {locations[5]}: {CLDAverage[5]}\nAverage distance for {locations[6]}: {CLDAverage[6]}\nAverage distance for {locations[7]}: {CLDAverage[7]}\nAverage distance for {locations[8]}: {CLDAverage[8]}\nAverage distance for {locations[9]}: {CLDAverage[9]}\nAverage distance for {locations[10]}: {CLDAverage[10]}\nAverage distance for {locations[11]}: {CLDAverage[11]}\nAverage distance for {locations[12]}: {CLDAverage[12]}\n')
print("Normal:")
print(f'Average distance for {locations[0]}: {NLDAverage[0]}\nAverage distance for {locations[1]}: {NLDAverage[1]}\nAverage distance for {locations[2]}: {NLDAverage[2]}\nAverage distance for {locations[3]}: {NLDAverage[3]}\nAverage distance for {locations[4]}: {NLDAverage[4]}\nAverage distance for {locations[5]}: {NLDAverage[5]}\nAverage distance for {locations[6]}: {NLDAverage[6]}\nAverage distance for {locations[7]}: {NLDAverage[7]}\nAverage distance for {locations[8]}: {NLDAverage[8]}\nAverage distance for {locations[9]}: {NLDAverage[9]}\nAverage distance for {locations[10]}: {NLDAverage[10]}\nAverage distance for {locations[11]}: {NLDAverage[11]}\nAverage distance for {locations[12]}: {NLDAverage[12]}\n')

print("Sorted By Party:")
if rawResults:
    print("Controversial:")
    print(f'Distances between {parties[0]}: {CPD0}\nDistances between {parties[1]}: {CPD1}\nDistances between {parties[2]}: {CPD2}\nDistances between {parties[3]}: {CPD3}\nDistances between {parties[4]}: {CPD4}\nDistances between {parties[5]}: {CPD5}\nDistances between {parties[6]}: {CPD6}\nDistances between {parties[7]}: {CPD7}\nDistances between {parties[8]}: {CPD8}\nDistances between {parties[9]}: {CPD9}\nDistances between {parties[10]}: {CPD10}\nDistances between {parties[11]}: {CPD11}\nDistances between {parties[12]}: {CPD12}\nDistances between {parties[13]}: {CPD13}\n')
    print("Normal:")
    print(f'Distances between {parties[0]}: {NPD0}\nDistances between {parties[1]}: {NPD1}\nDistances between {parties[2]}: {NPD2}\nDistances between {parties[3]}: {NPD3}\nDistances between {parties[4]}: {NPD4}\nDistances between {parties[5]}: {NPD5}\nDistances between {parties[6]}: {NPD6}\nDistances between {parties[7]}: {NPD7}\nDistances between {parties[8]}: {NPD8}\nDistances between {parties[9]}: {NPD9}\nDistances between {parties[10]}: {NPD10}\nDistances between {parties[11]}: {NPD11}\nDistances between {parties[12]}: {NPD12}\nDistances between {parties[13]}: {CPD13}\n')
print("Averages of the groups:")
print("Controversial:")
print(f'Average distance for {parties[0]}: {CPDAverage[0]}\nAverage distance for {parties[1]}: {CPDAverage[1]}\nAverage distance for {parties[2]}: {CPDAverage[2]}\nAverage distance for {parties[3]}: {CPDAverage[3]}\nAverage distance for {parties[4]}: {CPDAverage[4]}\nAverage distance for {parties[5]}: {CPDAverage[5]}\nAverage distance for {parties[6]}: {CPDAverage[6]}\nAverage distance for {parties[7]}: {CPDAverage[7]}\nAverage distance for {parties[8]}: {CPDAverage[8]}\nAverage distance for {parties[9]}: {CPDAverage[9]}\nAverage distance for {parties[10]}: {CPDAverage[10]}\nAverage distance for {parties[11]}: {CPDAverage[11]}\nAverage distance for {parties[12]}: {CPDAverage[12]}\nAverage distance for {parties[13]}: {CPDAverage[13]}\n')
print("Normal:")
print(f'Average distance for {parties[0]}: {NPDAverage[0]}\nAverage distance for {parties[1]}: {NPDAverage[1]}\nAverage distance for {parties[2]}: {NPDAverage[2]}\nAverage distance for {parties[3]}: {NPDAverage[3]}\nAverage distance for {parties[4]}: {NPDAverage[4]}\nAverage distance for {parties[5]}: {NPDAverage[5]}\nAverage distance for {parties[6]}: {NPDAverage[6]}\nAverage distance for {parties[7]}: {NPDAverage[7]}\nAverage distance for {parties[8]}: {NPDAverage[8]}\nAverage distance for {parties[9]}: {NPDAverage[9]}\nAverage distance for {parties[10]}: {NPDAverage[10]}\nAverage distance for {parties[11]}: {NPDAverage[11]}\nAverage distance for {parties[12]}: {NPDAverage[12]}\nAverage distance for {parties[13]}: {NPDAverage[13]}\n')

print("Unsorted:")
print("Average:")
print("Controversial:")

if rawResults:
    print(f'Controversial size: {ControversialSize}')
    print(f'Average distance: {CDAverage}')
    print(f'Distances between Controversial: {CD}')
    print(f'Controversial mean: {ControversialMean}')
    print(f'Controversial variance: {ControversialVariance}')
    print(f'Controversial standard deviation: {ControversialStandardDeviation}\n')
    print("Normal:")
    print(f'Normal size: {NormalSize}')
    print(f'Average distance: {NDAverage}')
    print(f'Distances between Normal: {ND}')
    print(f'Normal mean: {NormalMean}')
    print(f'Normal variance: {NormalVariance}')
    print(f'Normal standard deviation: {NormalStandardDeviation}\n')
else:
    print(f'Average distance: {CDAverage}\n')
    print("Normal:")
    print(f'Average distance: {NDAverage}\n')

print("Political Spectrum:")
print("Average:")
print("Controversial:")
print(f'Average distance Left: {CSDLeftAverage}\nAverage distance Right: {CSDRightAverage}\n')
print("Normal:")
print(f'Average distance Left: {NSDLeftAverage}\nAverage distance Right: {NSDRightAverage}\n')

print("Sorted By Topic:")
if rawResults:
    print("Controversial:")
    print(f'Distances between {controversialTopics[0]}: {CTD0}\nDistances between {controversialTopics[1]}: {CTD1}\nDistances between {controversialTopics[2]}: {CTD2}\nDistances between {controversialTopics[3]}: {CTD3}\nDistances between {controversialTopics[4]}: {CTD4}\n')
    print("Normal:")
    print(f'Distances between {normalTopics[0]}: {NTD0}\nDistances between {normalTopics[1]}: {NTD1}\nDistances between {normalTopics[2]}: {NTD2}\nDistances between {normalTopics[3]}: {NTD3}\nDistances between {normalTopics[4]}: {NTD4}\n')
print("Averages of the topics:")
print("Controversial:")
print(f'Average distance for {controversialTopics[0]}: {CTDAverage[0]}\nAverage distance for {controversialTopics[1]}: {CTDAverage[1]}\nAverage distance for {controversialTopics[2]}: {CTDAverage[2]}\nAverage distance for {controversialTopics[3]}: {CTDAverage[3]}\nAverage distance for {controversialTopics[4]}: {CTDAverage[4]}\n')
print("Normal:")
print(f'Average distance for {normalTopics[0]}: {NTDAverage[0]}\nAverage distance for {normalTopics[1]}: {NTDAverage[1]}\nAverage distance for {normalTopics[2]}: {NTDAverage[2]}\nAverage distance for {normalTopics[3]}: {NTDAverage[3]}\nAverage distance for {normalTopics[4]}: {NTDAverage[4]}\n')

print(f'T-test Equal variance: {EqualTtest}')
print(f'T-test Unequal variance: {UnEqualTtest}')

print(allWebsites)