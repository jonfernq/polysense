 

# flashcard.py

# working prototype of flashcard and multiple choice cards and decks 

import random, csv, copy  
from io import StringIO 

import sqlite3
from sqlite3 import Error

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from flashcard_gui import Ui_flashcard 
import flashcard_main, flashcard_gui, mc_question_main, mc_question_gui


# CLASS DEFINITIONS 

class AWL_word():

    def __init__(self, word_eng, word_thai, sentence_thai, sentence_eng):
        super().__init__()
        self.word_eng      = word_eng
        self.word_thai     = word_thai
        self.sentence_thai = sentence_thai
        self.sentence_eng  = sentence_eng

    def __repr__(self):
        return "AWL({0.word_eng}, {0.word_thai}, {0.sentence_thai}, {0.sentence_eng})".format(self) 
        
    def __str__(self):
        return "({0.word_eng}, {0.word_thai}, {0.sentence_thai}, {0.sentence_eng})".format(self)


class Face():

    def __init__(self, side, card_number, content, context): 
        super().__init__() 
        self.side        = side
        self.card_number = card_number
        self.content     = content
        self.context     = context        
        
    def __repr__(self):
        return "Face({0.side}, {0.card_number}, {0.content}, {0.context})".format(self) 
        
    def __str__(self):
        return "({0.side}, {0.card_number}, {0.content}, {0.context})".format(self) 
   
      
class Flashcard():

    def __init__(self, deck, number, front, back):
        super().__init__()
        self.deck    = deck
        self.number  = number
        self.front   = front
        self.back    = back
      
    def __repr__(self):
        return "Flashcard({0.deck}, {0.number}, {0.front}, {0.back})".format(self)  
        
    def __str__(self):
        return "({0.deck}, {0.number}, {0.front}, {0.back})".format(self)

      
class Deck():

    def __init__(self, name, description, questions, treatment, keywords):  
        super().__init__()
        self.name        = name
        self.description = description 
        self.questions   = questions     # items (better descriptor) 
        self.treatment   = treatment     # iterator object 
        self.keywords    = keywords      # keyword list 
        self.current_card_number = 0         
        self.current_side        = 'front' 

    def add(self, question):   
        self.questions.append(question) 

    def get_next_card_number(self): 
        n = self.current_card_number + 1
        if n > len(self.questions) - 1: 
            return 0
        else:
            return n        

    def get_next_side(self):     
        if self.current_side == 'front':
            return 'back' 
        else:
            return 'front'   
        
    def get_next_flashcard(self):
        self.current_side        = self.get_next_side() 
        self.current_card_number = self.get_next_card_number() 
        if self.current_side == 'front':
            title = self.name  
            question_content = self.questions[self.current_card_number].front.content
            question_context = self.questions[self.current_card_number].front.context
            answer_content = ''
            answer_context = '' 
            feedback = '' 
        else: #  back
            title = self.name   
            question_content = self.questions[self.current_card_number].front.content
            question_context = self.questions[self.current_card_number].front.context
            answer_content = self.questions[self.current_card_number].back.content
            answer_context = self.questions[self.current_card_number].back.context 
            feedback = '' 
        return title, question_content, question_context, answer_content, answer_context, feedback
            
    def __repr__(self):
        return "Deck({0.name}, {0.questions})".format(self)  
        
    def __str__(self):
        return "({0.name}, {0.questions})".format(self)

    def __len__(self):
        return len(self.questions)           

    
      
class MCQuestion():

    def __init__(self, deck, mc_number, question, answer_1, answer_2, answer_3, answer_4, correct_answer, context_english, context_thai):  
        super().__init__()
        self.deck            = deck 
        self.mc_number       = mc_number
        self.question        = question    
        self.answer_1        = answer_1 
        self.answer_2        = answer_2
        self.answer_3        = answer_3
        self.answer_4        = answer_4
        self.correct_answer  = correct_answer   # given by letter selected
        self.context_english = context_english  
        self.context_thai    = context_thai         
        
    def __repr__(self):
        return "Flashcard({0.deck}, {0.mc_number}, {0.question}, {0.answer_1}, {0.answer_2}, {0.answer_3}, {0.answer_4}, {0.correct_answer}, {0.context_english}, {0.context_thai})".format(self)   
        
    def __str__(self):
        return "({0.deck}, {0.mc_number}, {0.question}, {0.answer_1}, {0.answer_2}, {0.answer_3}, {0.answer_4}, {0.correct_answer}, {0.context_english}, {0.context_thai})".format(self)
        
class MCQuestionDeck(Deck):

    def __init__(self, flashcard_deck):  
        #def __init__(self, name, description, questions, treatment, keywords):  
        # super().__init__()
        self.name        = flashcard_deck.name
        self.description = flashcard_deck.description 
        self.questions   = make_mcquestions_from_flashcards(flashcard_deck)      # items (better descriptor) 
        self.treatment   = flashcard_deck.treatment     # iterator object 
        self.keywords    = flashcard_deck.keywords      # keyword list 
        self.current_card_number = 0  
        self.card_answer_selected = False         

    def check_answer(self, answer):
        self.card_answer_selected = True 
        correct_answer = self.questions[self.current_card_number].correct_answer
        answer_idx = ord(answer) - ord('A')
        if answer_idx == correct_answer:  
            return True, correct_answer
        else:
            return False, correct_answer  

    def get_next_card_number(self): 
        n = self.current_card_number + 1
        if n > len(self.questions) - 1: 
            return 0
        else:
            return n

    def get_next_mcquestion(self):
        if self.card_answer_selected:
            self.current_card_number = self.get_next_card_number() 
            mc = self.questions[self.current_card_number]
            self.card_answer_selected = False  
            return mc.deck, mc.mc_number, mc.question, mc.answer_1, mc.answer_2, mc.answer_3, mc.answer_4, mc.correct_answer, mc.context_english, mc.context_thai 
        else: 
            return None 


# PERFORMANCE LAYER DATA LAYER 

class StudentActivityLog():

    def __init__(self, student_id): 
        self.student_id = student_id 
       
    def record_student_event(self, question_type, event_type, stimulus, response):       
        # def record_student_event(self, event_type, flashcard):
        #(name, front_txt, back_txt, rating) = flashcard
        record = [time.ctime(time.time()), self.student_id, question_type, event_type, stimulus, response] 
        print(record, file=self.student_record_file) # record flashcard event for student  

    def begin_student_record(self):
        # record student deck start time
        self.student_record_file = open('student_event_record.txt', 'at', encoding='utf-8')
        self.record_student_event('flashcard-receptive-rating-1-5', 'begin-session', '', '')
        
    def end_student_record(self):
        # record student deck end time
        self.record_student_event('flashcard-receptive-rating-1-5', 'flashcard-end-session', '', '') 
        self.student_record_file.close()
                     
    def sqlite_write_logfile():
        pass 


# AWL DATA LAYER  
    
def sqlite_table_to_list(database, table):
    conn = None
    try:
        conn = sqlite3.connect(database) 
    except Error as e:
        print('ERROR: ', e)
        quit() 

    cur = conn.cursor()
    query = "SELECT * FROM {}".format(table) 
    cur.execute(query) 
    rows = cur.fetchall()
    return rows  

def sqlite_table_to_awl_objects(database, table):
    conn = None
    try:
        conn = sqlite3.connect(database) 
    except Error as e:
        print('ERROR: ', e)
        quit() 

    cur = conn.cursor()
    query = "SELECT * FROM {}".format(table) 
    cur.execute(query) 
    rows = cur.fetchall()
    #return rows   

    awl_words = []
    for line in rows:
        (word_eng, word_thai, sentence_thai, sentence_eng) = line 
        awl_words.append(AWL_word(word_eng, word_thai, sentence_thai, sentence_eng))
    return awl_words        

 
# FLASHCARD DATA LAYER 

def make_fcard_deck_from_AWL(awl_words):
    # create deck of flashcards
    # iterate through AWL creating flashcards
    ctr = 0
    fcard_lst = []
    deck = Deck('AWL', None, [], None, [])   
    for w in awl_words:
        fcard = Flashcard('AWL', ctr, Face('front', ctr, w.word_eng, w.sentence_eng), Face('back', ctr, w.word_thai, w.sentence_thai)) 
        deck.add(fcard)      
        ctr = ctr + 1 
    flashcard_deck = deck     
    return flashcard_deck 

def chunk_deck(seq, step):    
    chunked_by_n = [seq[i:i+step] for i in range(0,len(seq),step)] 
    return chunked_by_n 


# MC QUESTION DATA LAYER 

def extract_txts_from_face(faces):
    return list(map(lambda x: x.content, faces)) 
                                                          
def make_mcquestions_from_flashcards(flashcard_deck):
    chunked_by_4   = chunk_deck(flashcard_deck.questions, 4)   
    print('chunked_by_4: ', chunked_by_4)    
    # quit() 
    mc_questions   = [] 
    answers        = [] 
    correct_answer = ''      
    ctr            = 1     
    for l in chunked_by_4:
        for f in l:        # f is flashcard
            answer_ctr = 0
            answers    = []             
            for g in l: 
                answers.append(g.back.content) 
                if g.back.card_number == f.front.card_number: 
                    correct_answer = answer_ctr                
                    answer_ctr = answer_ctr + 1                      
                else:                
                    answer_ctr = answer_ctr + 1
            mc = MCQuestion('AWL', ctr, f.front.content, answers[0], answers[1], answers[2], answers[3], correct_answer, f.front.context, g.back.context)    
            mc_questions.append(mc) 
            distractors = []            
            ctr = ctr + 1                
    return mc_questions 
    

def make_mc_deck_from_flashcards(flashcard_deck, chunk): 

    # deepcopy of flashcard object that it is derived from
    mc_deck = copy.deepcopy(flashcard_deck) 
    
    # deepcopy replacement of questions with mc questions
    mc_questions = make_mcquestions_from_flashcards(flashcard_deck)  
    mc_deck.questions = copy.deepcopy(mc_questions) 
    
    # change deck identity to mc
    mc_deck.keywords.append('#mc_question')      

    return mc_deck 
    

    # LOGIC AND PRESENTATION LAYER OF PROGRAM 

    # FLASHCARD PRESENTATION LAYER 
def ui_display_front(content): 
    print("\nFRONT: ", content)
    print("<Return for Back of Card>")
    choice = str(input(""))

def ui_display_back(content):  
    print("BACK: ", content)
    print("Rate word mastery 1-5")
    rating = str(input(">>> ")) 
    return rating 

    # FLASHCARD LOGIC LAYER 
def do_fcard_deck_oneround(flashcards):  
    print('\n' + 'FLASHCARD DECK: ' + flashcards.name)  
    qctr = 0
    for fc in flashcards.questions:      
        ui_display_front(fc.front.content)     
        rating = ui_display_back(fc.back.content)      
        if rating == '':   # end deck review 
            break      
        
    # MC QUESTION PRESENTATION LAYER       
        
def ui_display_mc_question(deck_name, question, answers):    
    print('\n' + deck_name)             # print deck name            
    print("\n", question.content, "\n") # print question 
    print("\n".join(map(lambda x, y: x + y.content, ["a : ","b : ","c : ","d : "], answers)))
    print("\nWhat's your answer?") # get answer choice 
    choice = str(input(">>> "))
    return choice 

def ui_display_feedback_for_mc_question(correct_flag, choice, correct_option_content):  
    # provide feedback on correctness of response         
    if correct_flag:
        print('Right answer') 
    else:
        print('Wrong answer:', choice.upper(),', correct_answer: ', correct_option_content)             
    choice = str(input("<Press Return to Continue>"))

def ui_end_of_deck_report(correct_count, question_count):
    print('\n', correct_count, ' out of ', question_count)
    choice = str(input("<Press Return to Continue>"))     


    # MC QUESTION LOGIC LAYER   

def do_mc_deck_oneround(deck_name, mc_questions): 
    # deck, mc_number, stem, key, distractors    
    correct_count = 0
    question_count = 0
    for mc_question in mc_questions:
        correct_option = mc_question.key
        question = mc_question.stem
        
        # get all answers & shuffle 
        answers = mc_question.distractors        
        answers.append(mc_question.key)            
        random.shuffle(answers)  
        
        choice = ui_display_mc_question(deck_name, question, answers)
        
        if choice == '': break   # end deck review, break command entered  
                           
        # PROVIDE FEEDBACK, RECORD RESPONSE 
        # is chosen option correct option?  
        chosen_option = answers[ord(choice.upper()) - ord("A")]             
        if chosen_option.card_number == correct_option.card_number:
            correct_count = correct_count + 1
            correct_flag = True 
        else:
            correct_flag = False  

        ui_display_feedback_for_mc_question(correct_flag, choice, correct_option.content)  
            
        question_count = question_count + 1
    ui_end_of_deck_report(correct_count, question_count)      
            
            
def do_fcard_deck_pyqt(flashcard_deck):  
    print('\n' + 'FLASHCARD DECK: ' + flashcard_deck.name) 
    app = QtWidgets.QApplication(sys.argv)
    flashcard_gui = flashcard_main.FlashcardGUI(flashcard_deck) 
    flashcard = flashcard_deck.questions[0] 
    flashcard_gui.set_flashcard(flashcard_deck.name, flashcard.front.content, flashcard.front.context, flashcard.back.content, flashcard.back.context, '')     
    flashcard_gui.show_gui()    
    sys.exit(app.exec_())  
    
def get_flashcard_deck_sample(flashcard_deck, sample_size): 
    # get sample_size random sample from flashcard_deck.questions 
    deck_questions_sample = random.sample(flashcard_deck.questions, sample_size)     
    # deepcopy previous deck into new deck, change one attribute, namely questions 
    deck_sample = copy.deepcopy(flashcard_deck) 
    deck_sample.questions = copy.deepcopy(deck_questions_sample) 
    return deck_sample
    
def make_mc_question(mc_question):    
    #correct_option = mc_question.key
    question = mc_question.stem
    
    # get all answers & shuffle 
    answers = mc_question.distractors        
    answers.append(mc_question.key)            
    random.shuffle(answers)
    return mc_question.context, question, answers[0], answers[1], answers[2], answers[3]       
    
def do_mc_deck_pyqt(mc_deck):
    # title, context, question, answer_1, answer_2, answer_3, answer_4, feedback    
    print('\n' + 'MULTIPLE CHOICE DECK: ' + mc_deck.name)  
    app = QtWidgets.QApplication(sys.argv)
    mc_gui = mc_question_main.MCQuestionGUI(mc_deck) 
    mc = mc_deck.questions[0]  
    #(context, question, answer_1, answer_2, answer_3, answer_4) = make_mc_question(mc_question) 
    print('mc_correct_answer: ', mc.correct_answer)
    mc_gui.set_mc_question(mc_deck.name, mc.mc_number, mc.question, mc.answer_1, mc.answer_2, mc.answer_3, mc.answer_4, mc.correct_answer, mc.context_english, mc.context_thai) 
    mc_gui.show_gui() 
    sys.exit(app.exec_())      
    
def do_mc_deck_pyqt_old(mc_deck):
    # title, context, question, answer_1, answer_2, answer_3, answer_4, feedback    
    print('\n' + 'MULTIPLE CHOICE DECK: ' + mc_deck.name)  
    app = QtWidgets.QApplication(sys.argv)
    mc_gui = mc_question_main.MCQuestionGUI(mc_deck) 
    mc_question = mc_deck.questions[0]  
    #mc = make_mc_question(mc_question)
    #print('mc: ', mc)    
    (context, question, answer_1, answer_2, answer_3, answer_4) = make_mc_question(mc_question) 
    mc_gui.set_mc_question(mc_deck.name, context, question, answer_1, answer_2, answer_3, answer_4, '') 
    #quit()     
    mc_gui.show_gui() 
    sys.exit(app.exec_())  
   

if __name__ == "__main__":  

    awl_words = sqlite_table_to_awl_objects('awl.db', 'awl_eng_thai')
    flashcard_deck = make_fcard_deck_from_AWL(awl_words)
    deck = flashcard_deck   
    flashcard_deck_sample = get_flashcard_deck_sample(flashcard_deck, 12) 
    
    # run flashcard screen
    do_fcard_deck_pyqt(flashcard_deck_sample)     
    quit() 
  
    # run multiple choice question screen  
    mc_deck = MCQuestionDeck(flashcard_deck_sample) 
    print('mc_deck: ', mc_deck) 
    do_mc_deck_pyqt(mc_deck)
    quit()
    
    