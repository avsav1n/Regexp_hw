'''
Скрипт рефакторинга адресной книги
'''

import csv
import re

result = {}
pattern = re.compile(
    r'(?:\+7|8)\s*\(?(\d{3})\)?[\s-]?(\d{3})-?(\d{2})-?(\d{2})\s?(?:\(?доб\. (\d{4})\)?)?',
    flags=re.IGNORECASE
    )

with open('phonebook_raw.csv', encoding='utf-8', newline='') as fr:
    data = list(csv.reader(fr))
    fieldnames = data[0]
    convert = dict(enumerate(fieldnames))
    for line in data[1:]:
        name = ' '.join(line[:3]).split()
        lname, fname, sname = name if len(name) == 3 else name + ['']
        person = (lname, fname)
        if person not in result:
            result[person] = dict.fromkeys(fieldnames, '')
            result[person]['lastname'] = lname
            result[person]['firstname'] = fname
        if not result[person].get('surname'):
            result[person]['surname'] = sname
        for index, info in enumerate(line[3:], 3):
            if not info:
                continue
            if convert[index] == 'phone':
                number = pattern.sub(r'+7(\1)\2-\3-\4', info)
                if not info.isascii():
                    number = number + pattern.sub(r' доб.\5', info)
                info = number
            result[person][convert[index]] = info

with open('phonebook.csv', 'w', encoding='utf-8', newline='') as fw:
    data_writer = csv.DictWriter(fw, delimiter=',', fieldnames=fieldnames)
    data_writer.writeheader()
    data_writer.writerows(list(result.values()))
