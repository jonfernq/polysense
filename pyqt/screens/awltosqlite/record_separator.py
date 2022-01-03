

# record_separator.py: 
# read in screen-scraped AWL data frm 'awl_eng_thai_manual.txt' 
# reformat and write to csv file to upload to SQLite 

# strategy: this AWL file includes the best dataset for English-Thai
# from the SEALANG site including English homonyms and their Thai glosses,
# another AWL file contains the word family or lexical derivatives
# for each AWL lexical item, ultimately for the purposes of the flashcard system
# smaller flashcard files are derived from them as SQL views with three fields,
# a deck name, front card face, back card face, it would be good to automate this process
# of flashcard decks from the raw lexical data, and in fact the text mining of flashcards 
# quiz questions from texts is part of this process as well, the student activity log file 
# is the central repository of student performance data for data mining/machine learning, 
# study next recommender system, recording the time of every interaction that a student
# has with a card or question, front and back, with stimulus/treatment and response/score/rating,
# the stimulus/treatment consists of exactly what was presented to the student,
# this could be the flashcard reformatted into a multiple choice question, 
# or the word and the context presented in a certain fashion (e.g. on flashcard vs. 
# in experimental psychology format) the response could be self-knowledge rating
# e.g. 1-5, yes-no, correct=1, incorrect=0, number correctly matched),
# recommender system consists of different decks being created and recommended to student
# based on an individualized importance for review score calculated for a student
# that takes into account spaced repetition, similar items, what other chose, 
# and other factors based on what has been reviewed in the past and what has not beenreviewed yet
# a dashboard presentation of student progress is presented to help the student make a choice
# from the ranked recommendations    

# record_separator name comes from: 
# parses records in a plain text file 
# grouped in a paragraph delimited by a blank line ('\n\n')
# (idea comes from AWK) 
# https://stackoverflow.com/questions/19600475/how-to-read-records-terminated-by-custom-separator-from-file-in-python
# next step: read AWL raw data file and parse it into CVS file 


# DATA PREPARATION STAGE: 
# read file into string
# run delimited with paragraph record separator 
# producing list of records which represent raw data 
# this raw data is written to CSV file which is loaded into SQLite DB

# basic raw data is collected for all words in the AWL word list 
# this is supplemented by additional extraction of data from corpora using NLP techniques 

# DATA PRESENTATION STAGE: 
# read raw data records from SQLite DB
# construct objects from raw data records 
# (simple reformatting, no ORM and its complications)  
# as students interact with questions,
# student performance is written to a log file in SQLite
# data from log file used by recommendation system using 
# spaced repetition algorithms (collaborative filtering, item similarity,
# knowledge-based)  


data = '''abstract, n.
บทคัดย่อ
ผลการศึกษาดังกล่าวนี้ได้รับรางวัลบทคัดย่อการศึกษาวิจัยยอดเยี่ยม
The research results received an outstanding research abstract award.

accumulate, (intangible)
สั่งสม
นายกรัฐมนตรีกำลังสั่งสมอำนาจโดยไม่มีผู้ใดคอยเหนี่ยวรั้ง
The prime minister is accumulating power without anyone to deter him.

accurate, (on target)
แม่นยำ
คณะผู้วิจัยหวังว่าได้พบวิธีที่ง่ายและแม่นยำเพื่อใช้ตรวจคัดมะเร็งลำไส้ใหญ่แล้ว
The researchers hope they have found a simple and accurate way to screen for colon cancer.

accurate, (correct)
ถูกต้อง
ผู้บัญชาการกล่าวว่าจะให้ข้อมูลที่ถูกต้อง
The commander stated that he will provide accurate data.

achieve
บรรลุ
ขณะนี้ผู้ก่อการร้ายยังไม่บรรลุวัตถุประสงค์
At this time the terrorists have not achieved their objectives.

acknowledge, (accept)
ยอมรับ
พล.ต. สมบัติยอมรับว่า สนใจ(กับ)ข้อเสนอของรัสเซีย
Major General Sombat acknowledged that he is interested in Russia's proposal.'''

# ENGLISH WORD, THAI WORD, THAI SENTENCE, ENGLISH SENTENCE  

import sys, io  


def delimited(file, delimiter='\n', bufsize=4096):
    buf = ''
    while True:
        newbuf = file.read(bufsize)
        if not newbuf:
            yield buf
            return
        buf += newbuf
        lines = buf.split(delimiter)
        for line in lines[:-1]:
            yield line
        buf = lines[-1]
        
def delimited2(file, delimiter='\n'): 
    s = file.read()
    lines = s.split(delimiter)  
    return lines 

if __name__ == "__main__":

    import csv 
    
    # read raw text data reformat paragraph records as line records 
    f = open('awl_eng_thai_manual.txt', 'r', encoding='utf-8')  
    data = f.read() 
    paras = data.split('\n\n')   
    
    # reformat as rows of tuples 
    rows = [] 
    for para in paras:
        #print('para:*', para,'*')    
        tpl = tuple(para.split('\n'))
        print('tpl:*', tpl,'*')                
        # tpl = line.replace('\n','\t') 
        if len(tpl) != 0: 
            rows.append(tpl) 
            # lines2.append(line.replace('\n','\t')) 
    print('rows[51]: ', rows[51])    
    
    # print out AWL csv data to file (to upload to SQLite)
    headers = ['ENGLISH WORD', 'THAI WORD', 'THAI SENTENCE', 'ENGLISH SENTENCE'] 
    with open('awl.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers) 
        writer.writerows(rows)
    
    # print out csv data just stored to check it 
    with open('awl.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print('ROW: ', row)    



    # next import into SQLite DB 
quit()
    
    
#     EXCESS CODE - NOT USED 
#
# below does not work, took working from manual 
# write data out as csv file to load int SQLie DB 
headers = ['ENGLISH WORD', 'THAI WORD', 'THAI SENTENCE', 'ENGLISH SENTENCE'] 
with open('awl.csv','w', encoding='utf-8') as f:     
    f_csv = csv.writer(f, delimiter='\t') 
    f_csv.writerow(headers)
    f_csv.writerows(rows)    
    
    
with open('awl.csv') as f:  
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        print('row: ', row) 
quit() 

s = io.StringIO(data)
d = delimited(s, '\n\n', bufsize=2) 
print(d) 

quit() 


