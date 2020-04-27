import requests
import json
import csv
from bs4 import BeautifulSoup

def read_json(filename):
    with open(filename, "r", encoding='utf-8') as fr:
        data = json.load(fr)

    return data

def getNumOfPlayersFromURL(url):
    get_url_info = requests.get(url)
    res = get_url_info.text
    soup = BeautifulSoup(res, 'html.parser')

    playCountTable = soup.find_all("table")[1]
    table_tr = playCountTable.find_all("tr")[2]
    num_players = table_tr.find_all("td")[0].get_text()
    print(playCountTable)

    return num_players

def main():
    url_data = read_json("./URLLinks.json")
    for music in url_data:
        print(music)

if __name__ == "__main__":
    main()

"""
example of playCountTable (Armais u7): 

<table border="0">
<tr><th width="15%"></th><th width="28%"><U+0083>v<U+0083><U+008C><U+0083>C</th><th width="28%"><U+0083>N<U+0083><U+008A><U+0083>A</th><th width="29%"><U+0083>N<U+0083><U+008A>
<U+0083>A<U+0083><U+008C><U+0081>[<U+0083>g</th></tr>
<tr><th><U+0089>ñ<U+0090><U+0094></th><td>198645</td><td>65413</td><td>32.92%</td></tr>
<tr><th><U+0090>l<U+0090><U+0094></th><td>18339</td><td>15057</td><td>82.1%</td></tr>
</table>
"""