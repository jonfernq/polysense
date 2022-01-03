import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from flashcard_gui import Ui_flashcard 
#import card3_pyqt  
import flashcard


class FlashcardGUI(QtWidgets.QWidget):
    def __init__(self, flashcard_deck):
        super(FlashcardGUI, self).__init__()
        self.flashcard_deck = flashcard_deck
        #awl_words2 = read_in_test_data_string()
        #print(awl_words)  
        
        self.ui = Ui_flashcard()   
        self.ui.setupUi(self)
        self.initializeUI()              
        
    def show_gui(self):  
        self.show()        
        
    def initializeUI(self):        
        ####### Button Signal/slot Connections #######
        self.ui.button_next.clicked.connect(lambda: self.nextSide(self.ui.button_next.text())) 
        
    def nextSide(self, button_text):
        # When next button pressed, send to logic layer for processing.
        (title, question_content, question_context, answer_content, answer_context, feedback) = self.flashcard_deck.get_next_flashcard()   
        self.set_flashcard(title, question_content, question_context, answer_content, answer_context, '')             
        #s = 'Next Button Pressed: ' + button_text
        #self.ui.feedback.setText(s)

    def set_flashcard(self, title, question_content, question_context, answer_content, answer_context, feedback):  
    # def set_next_flashcard(self, flashcard): 
        # initialize gui before show 
        # title, question_content, question_context, answer_content, answer_context, feedback
        
        self.ui.title.setText(str(title))   
        self.ui.question_content.setText(question_content)    
        self.ui.question_context.setText(question_context)  
        self.ui.answer_content.setText(answer_content)   
        self.ui.answer_context.setText(answer_context)    
        self.ui.feedback.setText(feedback)         
        
        #self.ui.title.setText(str(flashcard.front.card_number))   
        #self.ui.question_content.setText(flashcard.front.content)    
        #self.ui.question_context.setText(str(flashcard.front.card_number))  
        #self.ui.answer_content.setText(flashcard.back.content)   
        #self.ui.answer_context.setText(str(flashcard.back.card_number))   
        #self.ui.feedback.setText(flashcard.front.content)  

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Keypad = FlashcardGUI() 
    sys.exit(app.exec_())
    
    