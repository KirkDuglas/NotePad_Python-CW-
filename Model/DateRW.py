

import csv
from Model.note import *
from Model.noteitem import *


class FileCSV:

    _fileName: str

    def __init__(self, fileName: str):
        self._fileName = fileName

    
    def load(self) -> Note:
        res = Note()
        with open(self._fileName, 'r', encoding='cp866') as f:
            reader = csv.DictReader(f, delimiter=';')
            for elem in reader:
                rec = NoteItem()
                if rec.setData(elem):
                    res.add(rec)
                else:
                    print(f'- Error: bad line: {elem}')
            return res
    
    
    def save(self, note: Note):
        with open(self._fileName, 'w', encoding='cp866') as f:
            writer = csv.DictWriter(f, fieldnames=list(note.get(0).getData().keys()), quoting=csv.QUOTE_ALL, delimiter=';', lineterminator="\n")
            writer.writeheader()
            for elem in note:
                rec = elem.getData()
                rec['date'] = elem.dateToStr()
                writer.writerow(rec)

# headers = ['header1','header5','header6','header7']

# with open('write.csv','w',newline='') as csvWriter,open('read.csv',newline='') as csvfile:
#     writer = csv.DictWriter(csvWriter,fieldnames=headers,extrasaction='ignore')
#     readCSV = csv.DictReader(csvfile)
#     writer.writeheader()
#     for row in readCSV:
#         writer.writerow(row)