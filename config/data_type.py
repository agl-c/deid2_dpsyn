"""this file read the DATA_TYPE json file to generate a dict COLS,
which describes the coloumn attributes' data type

"""
import json 
from config.path import DATA_TYPE


with open(DATA_TYPE,'r') as f:
    content = json.load(f)
COLS = content['dtype']

# one example is given below
# COLS = {
#     "PUMA": "str",
#     "YEAR": "uint32",
#     "HHWT": "float",
#     "GQ": "uint8",
#     "PERWT": "float",
#     "SEX": "uint8",
#     "AGE": "uint8",
#     "MARST": "uint8",
#     "RACE": "uint8",
#     "HISPAN": "uint8",
#     "CITIZEN": "uint8",
#     "SPEAKENG": "uint8",
#     "HCOVANY": "uint8",
#     "HCOVPRIV": "uint8",
#     "HINSEMP": "uint8",
#     "HINSCAID": "uint8",
#     "HINSCARE": "uint8",
#     "EDUC": "uint8",
#     "EMPSTAT": "uint8",
#     "EMPSTATD": "uint8",
#     "LABFORCE": "uint8",
#     "WRKLSTWK": "uint8",
#     "ABSENT": "uint8",
#     "LOOKING": "uint8",
#     "AVAILBLE": "uint8",
#     "WRKRECAL": "uint8",
#     "WORKEDYR": "uint8",
#     "INCTOT": "int32",
#     "INCWAGE": "int32",
#     "INCWELFR": "int32",
#     "INCINVST": "int32",
#     "INCEARN": "int32",
#     "POVERTY": "uint32",
#     "DEPARTS": "uint32",
#     "ARRIVES": "uint32",
# }

# we delete the complex column data type in simple test 
#"Date": {
    #   "dtype": "date",
    #   "kind": "date",
    #   "min": "2012-01-01 00:00:00",
    #   "max": "2020-12-31 00:00:00"
    # },
    # "Date Type": {
    #   "dtype": "str",
    #   "kind": "categorical",
    #   "values": [
    #     "DATEOFDEATH",
    #     "DATEREPORTED"
    #   ],
    #   "codes": [
    #     1,
    #     2
    #   ]
    # },
# just a test

# another example is given below 
# COLS = {
#    "Date": "date",
#    "Date Type": "str",
#     "Age": "uint8",
#     "Sex": "str",
#     "Race": "str",
#     "Residence State": "str",
#     "Death County": "str",
#     "Location": "str",
#     "Location if Other": "str",
#     "Injury County": "str",
#     "Injury State": "str",
#     "Heroin": "str",
#     "Cocaine": "str",
#     "Fentanyl": "str",
#     "Fentanyl Analogue": "str",
#     "Oxycodone": "str",
#     "Oxymorphone": "str",
#     "Ethanol": "str",
#     "Hydrocodone": "str",
#     "Benzodiazepine": "str",
#     "Methadone": "str",
#     "Amphet": "str",
#     "Tramad": "str",
#     "Morphine (Not Heroin)": "str",
#     "Hydromorphone": "str",
#     "Xylazine": "str",
#     "Opiate NOS": "str",
#     "Any Opioid": "str",
#     "CardioCondition": "str",
#     "RespiratoryCondition": "str",
#     "ObesityCondition": "str",
#     "DiabetesCondition": "str"
# }