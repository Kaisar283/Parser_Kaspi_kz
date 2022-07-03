from bs4 import BeautifulSoup

def find_page_count(text: str):
    integ = ''
    for i in text:
        if i.isdigit():
            integ+=i

    return int(integ)

def normalize_short_discription(text: str):
    discription = text.split('-')
    discription.pop(0)
    discription_list = []
    new_discription = []
    rep = ['\n']
    for item in discription:
        for sign in rep:
            if sign in item:
                item = item.replace(sign, '')
        new_discription.append(item)

    for item in new_discription:
        item = item.split(":")
        new_dict = {item[0].strip(): item[1].strip()}

        discription_list.append(new_dict)

    return discription_list
