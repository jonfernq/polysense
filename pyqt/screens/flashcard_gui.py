# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flashcard_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_flashcard(object):
    def setupUi(self, flashcard):
        flashcard.setObjectName("flashcard")
        flashcard.resize(963, 720)
        self.title = QtWidgets.QLabel(flashcard)
        self.title.setGeometry(QtCore.QRect(20, 20, 821, 31))
        self.title.setObjectName("title")
        self.frame_question = QtWidgets.QFrame(flashcard)
        self.frame_question.setGeometry(QtCore.QRect(20, 70, 821, 161))
        self.frame_question.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_question.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_question.setObjectName("frame_question")
        self.question_content = QtWidgets.QLabel(self.frame_question)
        self.question_content.setGeometry(QtCore.QRect(10, 40, 781, 41))
        self.question_content.setObjectName("question_content")
        self.question_context = QtWidgets.QLabel(self.frame_question)
        self.question_context.setGeometry(QtCore.QRect(10, 90, 781, 31))
        self.question_context.setObjectName("question_context")
        self.label_2 = QtWidgets.QLabel(self.frame_question)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label_2.setObjectName("label_2")
        self.button_next = QtWidgets.QPushButton(flashcard)
        self.button_next.setGeometry(QtCore.QRect(10, 480, 821, 28))
        self.button_next.setObjectName("button_next")
        self.feedback = QtWidgets.QLabel(flashcard)
        self.feedback.setGeometry(QtCore.QRect(20, 430, 821, 41))
        self.feedback.setObjectName("feedback")
        self.frame_answer_2 = QtWidgets.QFrame(flashcard)
        self.frame_answer_2.setGeometry(QtCore.QRect(20, 250, 821, 171))
        self.frame_answer_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_answer_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_answer_2.setObjectName("frame_answer_2")
        self.answer_content = QtWidgets.QLabel(self.frame_answer_2)
        self.answer_content.setGeometry(QtCore.QRect(10, 40, 781, 41))
        self.answer_content.setObjectName("answer_content")
        self.answer_context = QtWidgets.QLabel(self.frame_answer_2)
        self.answer_context.setGeometry(QtCore.QRect(10, 100, 781, 31))
        self.answer_context.setObjectName("answer_context")
        self.label = QtWidgets.QLabel(self.frame_answer_2)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label.setObjectName("label")

        self.retranslateUi(flashcard)
        QtCore.QMetaObject.connectSlotsByName(flashcard)

    def retranslateUi(self, flashcard):
        _translate = QtCore.QCoreApplication.translate
        flashcard.setWindowTitle(_translate("flashcard", "Form"))
        self.title.setText(_translate("flashcard", "title"))
        self.question_content.setText(_translate("flashcard", "Content"))
        self.question_context.setText(_translate("flashcard", "Context"))
        self.label_2.setText(_translate("flashcard", "FRONT"))
        self.button_next.setText(_translate("flashcard", "Next"))
        self.feedback.setText(_translate("flashcard", "feedback"))
        self.answer_content.setText(_translate("flashcard", "Content"))
        self.answer_context.setText(_translate("flashcard", "Context"))
        self.label.setText(_translate("flashcard", "BACK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    flashcard = QtWidgets.QWidget()
    ui = Ui_flashcard()
    ui.setupUi(flashcard)
    flashcard.show()
    sys.exit(app.exec_())
