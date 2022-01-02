import sys, os, csv, copy, time, random

# flashcardsimple4.py

from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QLineEdit,
    QStackedLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QListWidget,
    QListWidgetItem, 
    QSizePolicy,
    QInputDialog
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from PyQt5 import QtCore, QtGui, QtWidgets

# CONSTANTS 

# FLASHCARD WIDGETS (corresponds to order of addition to stackedwidget)
LIST_OF_FLASHCARDS       = 0
FRONT_TEXT_OF_FLASHCARD  = 1
BACK_TEXT_OF_FLASHCARD   = 2 
FRONT_IMAGE_OF_FLASHCARD = 3  

class FlashcardApp():

    def __init__(self, student_id): 
        super().__init__() 
        self.student_id = student_id
        self.dataio = DataIO(self.student_id) 
        self.fcard_db = self.dataio.load_flashcards() 
        self.session = FlashcardSession(self.student_id, self.dataio, self.fcard_db)
        self.session.fcard_display = FlashcardInit(self.session)
        #self.session.stackedLayout.setCurrentIndex(0) 
        self.session.next_widget_to_view(LIST_OF_FLASHCARDS)
        
# code to add        
#       self.session.next_widget_to_view()
#
#LIST_OF_FLASHCARDS       = 0
#FRONT_TEXT_OF_FLASHCARD  = 1
#BACK_TEXT_OF_FLASHCARD   = 2 
#FRONT_IMAGE_OF_FLASHCARD = 3   

class FlashcardSession():

    def __init__(self, student_id, dataio, fcard_db):
        self.student_id = student_id
        self.dataio     = dataio 
        self.fcard_db   = fcard_db 
        self.current_card = None 
        self.front_text  = None 
        self.front_image = None
        self.back_text   = None
        self.stackedLayout = None
        self.fcarditerator = None
  
    def next_widget_to_view(self, widget):
        self.stackedLayout.setCurrentIndex(widget)
  
    def nextCard(self, new_rating):
        new_card = self.fcarditerator.next_card(new_rating) 
        if new_card:
            (deck, front, back, old_rating) = new_card    
            self.update_card(front, back)            
        else: 
            #self.session.stackedLayout.setCurrentIndex(0) 
            self.next_widget_to_view(LIST_OF_FLASHCARDS) 
       
    def is_image(self,txt):
        return( True if (len(txt.split('.')) > 1) and (txt.split('.')[1] == 'gif') else False ) 
            
    def display_image(self, img, imglbl):
        imglbl.setPixmap(QPixmap(img))
            
    def update_card(self,front_txt,back_txt):  
        # check if current card is text or image
        # then set to new text or image
        self.back_text.b_txt_label.setText(back_txt)  
        if self.is_image(front_txt):
            print('front_txt: ',front_txt)
            print('QtGui.QPixmap(front_txt): ', QtGui.QPixmap(front_txt)) 
            #self.front_image.image_label.setPixmap(QtGui.QPixmap('images/' + front_txt))
            self.display_image('images/' + front_txt, self.front_image.image_label)
            #self.stackedLayout.setCurrentIndex(3)
            self.next_widget_to_view(FRONT_IMAGE_OF_FLASHCARD)
        else:  
            self.front_text.f_txt_label.setText(front_txt)
            #self.stackedLayout.setCurrentIndex(1)
            self.next_widget_to_view(FRONT_TEXT_OF_FLASHCARD)

class DataIO():

    def __init__(self, student_id): 
        self.student_id = student_id 
           
    def record_student_event(self, event, flashcard):
        (name, front_txt, back_txt, rating) = flashcard
        record = [time.ctime(time.time()), self.student_id, event, name, front_txt, back_txt, rating]
        print(record, file=self.student_record_file) # record flashcard event for student  

    def begin_student_record(self):
        # record student deck start time
        self.student_record_file = open('student_event_record.txt', 'at', encoding='utf-8')
        self.record_student_event('flashcard-begin-session', ['','','',''])
        
    def end_student_record(self):
        # record student deck end time
        self.record_student_event('flashcard-end-session', ['','','',''])
        self.student_record_file.close()
        
    def load_flashcards(self):
        # load flashcard database from CSV to dictionary in app 
        # note: problem with loading countries which consist of comma-delimited list of names 
        directory_path = os.getcwd()
        csvfiles = [name for name in os.listdir(directory_path) if name.endswith('.csv')]

        fcard_db = {}
        for f in csvfiles:
            if f.startswith('fcard'):
                (fname,ext) = os.path.splitext(f)
                name = fname[6:].replace('_', ' ')
                fcard_db[name] = []
                filepath = os.path.join(directory_path, f)

                with open(filepath, "r", encoding='utf-8') as csv_f:
                    reader = csv.reader(csv_f)
                    header_labels = next(reader)
                    for row in csv.reader(csv_f):
                        if len(row) > 0:
                            items = [name] + row[0].split('\t')
                            fcard_db[name].append(items)
        self.show_flashcards(fcard_db)
        return fcard_db
        
    def show_flashcards(self, fcard_db):                        
        for key in fcard_db:    
            print('\nkey: ', key, '\n')
            print('fcard_db[key]: ', fcard_db[key])        

class FlashcardIterator():

    def __init__(self, deck, session):  
        super().__init__() 
        session_current = []
        self.deck  = deck  
        self.session = session 
        self.dataio = self.session.dataio 
        self.student_id = self.session.student_id
        self.dataio.begin_student_record()
        for s in self.deck:
            print('s: ', s)
        self.current_round = deck           
        self.next_round = [] 
        self.mastered = [] 
        self.session.current_card = self.current_round[0]        
   
    def first_card(self):  
        self.current_card = self.current_round[0]    
        self.session.current_card = self.current_card
        return self.current_card
       
    def next_card(self, new_rating):
        self.print_all_cards()
        if self.continue_round():
            (deck, front, back, old_rating) = self.current_round.pop(0)    
            next_card = (deck, front, back, new_rating)           
            self.reprioritize_card(new_rating, next_card)
        else:
            next_card = None
        self.session.current_card = next_card     
        return next_card
   
    def reprioritize_card(self, new_rating, new_card):
        # if not mastered (rating < 5) move on to next round, else place in mastered (no more review) 
        return (self.next_round.append(new_card) if new_rating < 5 else self.mastered.append(new_card))

    def mastered_deck(self):
        return (True if len(self.next_round) == 0 else False)   
   
    def finished_current_round(self):
        return (True if len(self.current_round) == 0 else False)       

    def all_cards_mastered(self):
        return (True if len(self.next_round) == 0 else False) 

    def new_round(self):  # begin new round of flashcard review 
        self.current_round = copy.deepcopy(self.next_round) 
        self.next_round = [] 
   
    def continue_round(self):             # after reviewing a card, check if continue  
        if self.finished_current_round(): 
            if self.all_cards_mastered(): # don't continue, all cards mastered (rated 5)       
                return False            
            else:                         # continue, all cards not mastered  
                self.new_round()
                return True
        else:                             # continue current round 
            return True

    def print_all_cards(self):
        print('PRINT ALL CARDS')
        print('RATING COUNT 1,2,3,4,5: ', self.count_ratings()) 
        print('CURRENT ROUND: ', self.current_round)
        print('NEXT ROUND   : ', self.next_round) 
        print('MASTERED     : ', self.mastered) 

    def get_rating(self):
        # get  rating (1-5), (some not int e.g. '' == exit) 
        s = input("rating> ")
        return (int(s) if s.isdigit() else s)        
    
    def count_ratings(self):
        # concatenate current & next, count ratings        
        # to provide rating count mid-session & save away at end-session
        all = self.current_round + self.next_round
        ctr = {} 
        ctr['1'] = [] 
        ctr['2'] = []
        ctr['3'] = [] 
        ctr['4'] = [] 
        ctr['5'] = []        
        for a in all:
            print('a: ', a) 
            #print('str(a[3]): ',str(a[3]), ' a[3]:', a[3])
            ctr[str(a[3])].append(a) 
        print('\n ctr: ', ctr)
        return [len(ctr['1']),len(ctr['2']), len(ctr['3']), len(ctr['4']), len(ctr['5'])]   
        
        #return all_fcards     
        #(1count, 2count, 3count, 4count, 5count) =
        # def combine_current_next_rounds():
        
class FlashcardInit(QWidget):
    
    def __init__(self, session):
        super().__init__()       
        self.session = session 
        self.student_id = self.session.student_id
        self.fcard_db = self.session.fcard_db
        self.dataio = self.session.dataio
        
        self.setWindowTitle("Flashcards")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("""background-color: #d8e9f3""")
        
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
              
        self.front_text     = FrontText(self.session)
        self.front_image    = FrontImage(self.session)
        self.back_text      = BackText(self.session)
        self.session.front_text  = self.front_text 
        self.session.front_image = self.front_image
        self.session.back_text   = self.back_text
        self.flashcardlist = FlashcardList(self.session) 
        self.session.flashcardlist = self.flashcardlist        
        
        # Create the stacked layout
        self.stackedLayout = QStackedLayout()
        self.stackedLayout.addWidget(self.flashcardlist)        
        self.stackedLayout.addWidget(self.front_text)
        self.stackedLayout.addWidget(self.back_text)
        self.stackedLayout.addWidget(self.front_image)
        self.session.stackedLayout = self.stackedLayout

        # Add the stacked layout to the top-level layout
        layout.addLayout(self.stackedLayout)

class FlashcardList(QWidget): 
      
    def __init__(self, session):
        super().__init__() 
        self.session = session        
        self.student_id = self.session.student_id
        self.fcard_db = self.session.fcard_db
        self.dataio = self.session.dataio
        
        # create a top-level layout 
        layout = QVBoxLayout() 
        self.setLayout(layout) 
    
        self.lstwidget = QListWidget()
        self.lstwidget.setAlternatingRowColors(True)
        self.lstwidget.itemDoubleClicked.connect(self.listitemClicked)  # double-click to select
            
        for key in self.fcard_db:                   # create list items for flashcard decks 
            list_item = QListWidgetItem()
            list_item.setText(key)
            list_item.setFont(QFont('Arial', 20))
            self.lstwidget.addItem(list_item)

        # exit button
        self.btn_h_box = QHBoxLayout()
        self.b1=QPushButton("Exit")
        self.b1.clicked.connect(lambda:self.session.fcard_display.close()) 
        self.btn_h_box.addWidget(self.b1)
        
        self.b1.setStyleSheet("""background-color: #b2d3e6;
        color: black;
        border-style: outset;
        border-width: 3px;
        border-radius: 5px;
        font: bold 60px 'Arial'""")
        
        self.left_v_box = QVBoxLayout()
        self.left_v_box.addWidget(self.lstwidget)  
        self.left_v_box.addWidget(self.b1)         
        
        # add the list widget to the top level layout 
        layout.addLayout(self.left_v_box) 
        
    def listitemClicked(self):
        key = self.lstwidget.currentItem().text()
        self.deck = self.fcard_db[key] 
        print('key:',key,'deck:',self.deck)  

        fcarditerator  = FlashcardIterator(self.deck, self.session)       
        fcarditerator.print_all_cards()
        self.current_card = fcarditerator.first_card()
        self.session.fcarditerator = fcarditerator 
        
        (name, front_txt, back_txt, rating) = self.current_card
        print('self.current_card: ', self.current_card)  
        self.session.update_card(front_txt,back_txt)    

class FrontText(QWidget):     
    
    def __init__(self, session):
        super().__init__() 
        self.session = session        
        self.student_id = self.session.student_id
        self.fcard_db = self.session.fcard_db
        self.dataio = self.session.dataio

        # create a top-level layout 
        layout = QVBoxLayout() 
        self.setLayout(layout) 

        initial_txt = ''
        self.cnt_h_box = QHBoxLayout()
        
        self.f_txt_label = QLabel(initial_txt)
        self.f_txt_label.setWordWrap(True) 
        self.f_txt_label.setFont(QFont('Arial', 30))
        self.f_txt_label.setStyleSheet("""qproperty-alignment: AlignCenter""")
                
        self.btn_h_box = QHBoxLayout()
        b1=QPushButton("Reveal Answer")
        b1.clicked.connect(self.revealanswerClicked)
        b2=QPushButton("New Deck")
        b2.clicked.connect(self.newdeckClicked)
        
        self.btn_h_box.addWidget(b1)
        self.btn_h_box.addWidget(b2)
        
        b1.setStyleSheet("""background-color: #b2d3e6;
        color: black;
        border-style: outset;
        border-width: 3px;
        border-radius: 5px;
        font: bold 60px 'Arial'""")
        b2.setStyleSheet("""background-color: #68a7ca;
        color: black;
        border-style: outset;
        border-width: 3px;
        border-radius: 5px;
        font: bold 60px 'Arial'""") 
 
        self.txt_h_box = QHBoxLayout()
        self.txt_h_box.addStretch()
        self.txt_h_box.addWidget(self.f_txt_label)
        self.txt_h_box.addStretch()
        
        self.v_box = QVBoxLayout()
        self.v_box.addStretch(2)
        self.v_box.addLayout(self.txt_h_box)
        self.v_box.addStretch(2)
        self.v_box.addLayout(self.btn_h_box) # button  
        
        # add the list widget to the top level layout 
        layout.addLayout(self.v_box) 
        
    def revealanswerClicked(self):
        #self.session.stackedLayout.setCurrentIndex(2)
        self.session.next_widget_to_view(BACK_TEXT_OF_FLASHCARD) 

    def newdeckClicked(self):
        self.dataio.end_student_record()
        #self.session.stackedLayout.setCurrentIndex(0)  
        self.session.next_widget_to_view(LIST_OF_FLASHCARDS)        

class FrontImage(QWidget):     
    
    def __init__(self, session):
        super().__init__() 
        self.session = session        
        self.student_id = self.session.student_id
        self.fcard_db = self.session.fcard_db
        self.dataio = self.session.dataio        

        # create a top-level layout 
        layout = QVBoxLayout() 
        self.setLayout(layout) 

        initial_img = 'dummy.jpg'
        print('initial_img: ', initial_img)
        self.img_h_box = QHBoxLayout()
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        #self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored) # image can stretch neither horiz nor vert

        self.image = QPixmap(initial_img)
        #self.image_label.setPixmap(self.image.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)) 
        self.image_label.setPixmap(self.image)
            
        self.img_h_box.addWidget(self.image_label)
        
        self.btn_h_box = QHBoxLayout()
        b1=QPushButton("Reveal Answer")
        b1.clicked.connect(self.revealanswerClicked)
        b2=QPushButton("New Deck")
        b2.clicked.connect(self.newdeckClicked)
        
        b1.setStyleSheet("""background-color: #b2d3e6;
        color: black;
        border-style: outset;
        border-width: 3px;
        border-radius: 5px;
        font: bold 60px 'Arial'""")
        b2.setStyleSheet("""background-color: #68a7ca;
        color: black;
        border-style: outset;
        border-width: 3px;
        border-radius: 5px;
        font: bold 60px 'Arial'""") 
 
        self.btn_h_box.addWidget(b1)
        self.btn_h_box.addWidget(b2)
        
        self.v_box = QVBoxLayout()
        self.v_box.addStretch(2)
        self.v_box.addLayout(self.img_h_box)
        self.v_box.addStretch(2)
        self.v_box.addLayout(self.btn_h_box)
        
        # add the list widget to the top level layout 
        layout.addLayout(self.v_box)  

    def revealanswerClicked(self):
        #self.session.stackedLayout.setCurrentIndex(2)
        self.session.next_widget_to_view(BACK_TEXT_OF_FLASHCARD)
       
    def newdeckClicked(self):
        self.dataio.end_student_record()
        #self.session.stackedLayout.setCurrentIndex(0)  
        self.session.next_widget_to_view(LIST_OF_FLASHCARDS)     
    
class BackText(QWidget):     
    
    def __init__(self, session):
        super().__init__() 
        self.session = session        
        self.student_id = self.session.student_id
        self.fcard_db = self.session.fcard_db
        self.dataio = self.session.dataio
    
        # create a top-level layout 
        layout = QVBoxLayout() 
        self.setLayout(layout) 
    
        initial_txt = ''
        txt_h_box = QHBoxLayout()
        self.b_txt_label = QLabel(initial_txt)
        self.b_txt_label.setWordWrap(True) 
        self.b_txt_label.setFont(QFont('Arial', 30))
        self.b_txt_label.setStyleSheet("""qproperty-alignment: AlignCenter""")

        txt_h_box.addStretch()
        txt_h_box.addWidget(self.b_txt_label)
        txt_h_box.addStretch()
        
        btn_h_box = QHBoxLayout()
        b1=QPushButton("1")
        b1.clicked.connect(self.ratingClicked)
        b2=QPushButton("2")
        b2.clicked.connect(self.ratingClicked)
        b3=QPushButton("3")
        b3.clicked.connect(self.ratingClicked)
        b4=QPushButton("4")
        b4.clicked.connect(self.ratingClicked)
        b5=QPushButton("5")
        b5.clicked.connect(self.ratingClicked)
        
        b1.setStyleSheet("""background-color: #d8e9f3;
        color: black;
        border-style: outset;
        border-width: 3px;
        border-radius: 5px;
        font: bold 80px 'Arial'""")
        b2.setStyleSheet("""background-color: #b2d3e6;
        color: black;
        border-style: outset;
        border-width: 3px;
        border-radius: 5px;
        font: bold 80px 'Arial'""") 
        b3.setStyleSheet("""background-color: #8dbdd8;
        color: black;
        border-style: outset;
        border-width: 3px;
        border-radius: 5px;
        font: bold 80px 'Arial'""")      
        b4.setStyleSheet("""background-color: #68a7ca;
        color: black;
        border-style: outset;
        border-width: 3px;
        border-radius: 5px;
        font: bold 80px 'Arial'""")        
        b5.setStyleSheet("""background-color: #4390bc;
        color: black;
        border-style: outset;
        border-width: 3px;
        border-radius: 5px;
        font: bold 80px 'Arial'""")
 
        btn_h_box.addWidget(b1)
        btn_h_box.addWidget(b2)
        btn_h_box.addWidget(b3)
        btn_h_box.addWidget(b4)
        btn_h_box.addWidget(b5)
        
        self.v_box = QVBoxLayout()
        self.v_box.addStretch(2)
        self.v_box.addLayout(txt_h_box)
        self.v_box.addStretch(2)
        self.v_box.addLayout(btn_h_box)
        
        # add the list widget to the top level layout 
        layout.addLayout(self.v_box)         

    def ratingClicked(self):
        sender = self.sender()
        txt = sender.text()
        print(txt + ' changed, type: ', type(txt))
        button_number = int(txt)
        (deck, front, back, old_rating) = self.session.current_card      
        self.current_card = (deck, front, back, button_number)
        self.dataio.record_student_event('flashcard', self.current_card)
        #self.dataio.record_student_event('flashcard', self.current_card, button_number)
        self.session.nextCard(button_number)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    student_id = '001'
    fcard_app = FlashcardApp(student_id)
    fcard_app.session.fcard_display.show()
    sys.exit(app.exec_())
    

    

        
        
        
    
    
    
    