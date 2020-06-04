import requests as r
import json
import pandas as pd

#query = "Please provide all data request"
#query = "Please provide a copy of all intervenor data requests submitted to SoCalGas in this proceeding and SoCalGas’ responses to those requests."
#query = "data warehouse"
#query = "Does SDG&E keep records of the number of small businesses located in California which provide goods or services to SDG&E?"
#query = "please state the current annual right-of-way cost that SoCalGas pays to the Morongo tribe"
#query = "Please provide a table showing SoCalGas's proposed total net revenue requirements for 1998 and 1980, approved revenue requirements for each year from 2014 through 2018, and actual total expenditures for 2014 through 2017. "
#query = "Decarbonizing Pipeline Gas"
#query = "advocacy", "object"

POST_JSON = {
    'input_query': "data warehouse"
}

json_data = r.post('https://dr-prototype-api.herokuapp.com/api', json=POST_JSON).json()

data_dict = {"sim": json_data['sim'], "request": json_data['request'], "url": json_data['url']}
pd.DataFrame(data_dict)
