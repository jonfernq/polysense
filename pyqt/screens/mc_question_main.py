import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from mc_question_gui import Ui_mc_question 
        

class MCQuestionGUI(QtWidgets.QWidget):
    def __init__(self, mc_deck): 
        super(MCQuestionGUI, self).__init__()
        self.mc_deck = mc_deck 
        
        self.ui = Ui_mc_question()  
        self.ui.setupUi(self)
        self.initializeUI()
        
    def initializeUI(self):        
        ####### Button Signal/slot Connections #######
        self.ui.button_answer_1.clicked.connect(lambda: self.answerClicked(self.ui.button_answer_1.text()))
        self.ui.button_answer_2.clicked.connect(lambda: self.answerClicked(self.ui.button_answer_2.text()))
        self.ui.button_answer_3.clicked.connect(lambda: self.answerClicked(self.ui.button_answer_3.text()))
        self.ui.button_answer_4.clicked.connect(lambda: self.answerClicked(self.ui.button_answer_4.text()))

        self.ui.button_next.clicked.connect(lambda: self.nextMCQuestion(self.ui.button_next.text()))

    def show_gui(self):  
        self.show()       

    def answerClicked(self, button_text):
        # When answer button with letter pressed, send to logic layer for processing. Update feedback. 
        letters = ['A','B','C','D']
        (correct_tf, correct_answer) = self.mc_deck.check_answer(button_text) 
        if correct_tf:
            fdbck = 'Correct' 
        else:
            fdbck = 'Not Correct, Right Answer: ' + letters[correct_answer]   
        print('correct_tf, correct_answer: ', correct_tf, correct_answer)  
        self.ui.feedback.setText(fdbck)  
        
    def nextMCQuestion(self, button_text):
        # When next button pressed, send to logic layer for processing.
        
        # (title, question_content, question_context, answer_content, answer_context, feedback) = self.mc_deck.get_next_flashcard()   
        # self.set_flashcard(title, question_content, question_context, answer_content, answer_context, '') 
        next_question = self.mc_deck.get_next_mcquestion()
        if next_question: 
            (deck_name, mc_number, question, answer_1, answer_2, answer_3, answer_4, correct_answer, context_english, context_thai) = next_question 
            self.set_mc_question(deck_name, mc_number, question, answer_1, answer_2, answer_3, answer_4, correct_answer, context_english, context_thai)
        else: 
            s = 'Select Answer (before moving to next question)'
            self.ui.feedback.setText(s)

    def set_mc_question(self, deck_name, mc_number, question, answer_1, answer_2, answer_3, answer_4, correct_answer, context_english, context_thai):    
        # def set_next_flashcard(self, flashcard): 
        # initialize gui before show 
        # title, question_content, question_context, answer_content, answer_context, feedback
        
        self.ui.title.setText(str(deck_name) + ': ' + str(mc_number))      
 
        self.ui.context.setText(context_english)   
        self.ui.question.setText(question)  
         
        self.ui.answer_1.setText(answer_1) 
        self.ui.answer_2.setText(answer_2)         
        self.ui.answer_5.setText(answer_3) 
        self.ui.answer_4.setText(answer_4)  

        self.ui.feedback.setText('')       


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Keypad = MCQuestionGUI()
    sys.exit(app.exec_())
    
    