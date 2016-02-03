# -*- coding: utf-8 -*-
#/usr/bin/env python2

import sqlite3
import sys


try:
    from PyQt4 import QtCore, QtGui,uic
except:
    print u"PyQt modülü yüklü değil.\nPyQt 4.5 veya üzeri bir sürüm yükledikten tekrar deneyin."
    sys.exit()



from ui_sozluk import Ui_MainWindow
app = QtGui.QApplication(sys.argv)
class Sozlux(QtGui.QMainWindow, Ui_MainWindow):

    category=""


    def __init__(self):

        QtGui.QMainWindow.__init__(self)

        self.setupUi(self)
        QtGui.QMainWindow.setWindowTitle(self,"sozlux")

        self.connectToDB()

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.showTrayIcon()

        self.searchBox.textChanged.connect(self.printRelatives)

        self._windowIcon=QtGui.QIcon("sozlux.png")
        self.setWindowIcon(self._windowIcon)

        self._exitIcon=QtGui.QIcon("cikis.png")
        self.pushButton.setIcon(self._exitIcon)

        self. _clearIcon =QtGui.QIcon("clear.png")
        self.clearButton.setIcon(self._clearIcon)

        self. _pasteIcon =QtGui.QIcon("paste.png")
        self.pushButton_3.setIcon(self._pasteIcon)
        #print  list(QtGui.QStyleFactory.keys() )

        self.actionCleanlooks.triggered.connect(lambda: self.setAppearance('Cleanlooks'))
        self.actionPlastique.triggered.connect(lambda: self.setAppearance('Plastique'))
        self.actionPlastique.triggered.connect(lambda: self.setAppearance('GTK+'))
        self.actionBespin.triggered.connect(lambda: self.setAppearance('Bespin'))
        self.actionCDE.triggered.connect(lambda: self.setAppearance('CDE'))
        self.actionMotif.triggered.connect(lambda: self.setAppearance('Motif'))
        self.actionOxygen.triggered.connect(lambda: self.setAppearance('Oxygen'))
        self.actionQtcurve.triggered.connect(lambda: self.setAppearance('QtCurve'))
        self.actionWindows.triggered.connect(lambda: self.setAppearance('Windows'))



        # self.trayIcon.activated(self.trayIcon.Trigger).connect(lambda:self.trayIconEventHandle("Trigger"))
        # self.trayIcon.activated(self.trayIcon.Context).connect(lambda:self.trayIconEventHandle("Context"))
        # self.trayIcon.activated(self.trayIcon.MiddleClick).connect(lambda:self.trayIconEventHandle("MiddleClick"))
        # self.trayIcon.activated(self.trayIcon.DoubleClick).connect(lambda:self.trayIconEventHandle("DoubleClick"))
        self.connect(self.trayIcon,QtCore.SIGNAL( "activated(QSystemTrayIcon::ActivationReason)"),self.trayIconEventHandle)



        self.categoryButtonsGroup=QtGui.QButtonGroup()
        self.categoryButtonsGroup.setExclusive(True)

        self.categoryButtonsGroup.addButton(self.pushButtonBilgisayarTerimleri)
        self.categoryButtonsGroup.addButton(self.pushButtonBilisimTerimleri)
        self.categoryButtonsGroup.addButton(self.pushButtonElektronikTerimleri)
        self.categoryButtonsGroup.addButton(self.pushButtonIngilizceTurkce)
        self.categoryButtonsGroup.addButton(self.pushButtonTipTerimleri)
        self.categoryButtonsGroup.addButton(self.pushButtonTurkceIngilizce)
        self.categoryButtonsGroup.addButton(self.pushButtonTeknikTerimler)


        self.categoryButtonsGroup.buttonClicked.connect(self.setCategory)
        self.categoryButtonsGroup.buttonClicked.connect(self.printRelatives)
        self.setCategory()
        self.searchBox.setFocus()
        self.opacitySlider.valueChanged.connect(lambda: QtGui.QMainWindow.setWindowOpacity(self,self.opacitySlider.value()/100.0))

        self.relatedList.setSortingEnabled(True)

        self.trayContextMenu=QtGui.QMenu()
        #actions specified in ui file using designer
        self.trayContextMenu.addAction(self.actionExit)
        self.actionExit.triggered.connect(self.closeApplication)
        self.trayContextMenu.addAction(self.actionShow)
        self.actionShow.triggered.connect(lambda : self.trayIconEventHandle("Show"))
        self.trayContextMenu.addAction(self.actionHide)
        self.actionHide.triggered.connect(lambda: self.trayIconEventHandle("Hide"))
        self.trayIcon.setContextMenu(self.trayContextMenu)



    def trayIconEventHandle(self,Reason=None):
        
        #print Reason
        if Reason==self.trayIcon.Trigger:
            if self.isHidden():
                self.show()
            elif not self.isHidden():
                self.hide()
            else:
                pass
        elif Reason==self.trayIcon.Context:
            self.trayContextMenu.show()

        elif Reason==self.trayIcon.MiddleClick:
            #print "MiddleClick"
            pass
        elif Reason==self.trayIcon.DoubleClick:
            #print "DoubleClick"
            pass
        elif Reason=="Show":
            if self.isHidden():
                self.show()
        elif Reason=="Hide":
            if not self.isHidden():
                self.hide()
        elif Reason=="Exit":
            self.closeApplication()

    def setAppearance(self, appearance_choice):
        """
        sets appereance (eg: qtcurve , bespin)
        """
        if appearance_choice == None:
            appearance_choice = "Cleanlooks"

        self.setStyle(QtGui.QStyleFactory.create(appearance_choice))
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(appearance_choice))

    def showTrayIcon(self):
        """
        shows a tray icon
        """
        self.trayIcon.setIcon(QtGui.QIcon("sozlux.png"))#TODO path should be specified correctly

        if self.trayIcon.isVisible():
            pass
        else:
            self.trayIcon.show()
    def setCategory(self):#sets current category


        if self.pushButtonBilgisayarTerimleri.isChecked():
            self.category="BilgisayarTerimleriTablosu"
        elif self.pushButtonBilisimTerimleri.isChecked():
            self.category="BilisimTerimleriTablosu"
        elif self.pushButtonElektronikTerimleri.isChecked():
            self.category="ElektronikTerimleriTablosu"
        elif self.pushButtonIngilizceTurkce.isChecked():
            self.category="IngilizceTurkceTablosu"
        elif self.pushButtonTipTerimleri.isChecked():
            self.category="TipTerimleriTablosu"
        elif self.pushButtonTurkceIngilizce.isChecked():
            self.category="TurkceIngilizceTablosu"
        elif self.pushButtonTeknikTerimler.isChecked():
            self.category="TeknikTerimlerTablosu"
    def printResult(self, result):#takes a something and prints to resultbox
        self.resultsBox.setText((result))
    def connectToDB(self):#tries to connect to db. creates connection object
        try:
            self.conn = sqlite3.connect('new.db')

        except Exception as e:
            print(e)






    def printRelatives(self):
        self.resultsBox.clear()
        searchText=str(QtCore.QString.toUtf8 (self.searchBox.text()))
        if len(searchText) <= 0:
            pass
        else:
            query1=query2=("Select `SozcukAdi` from {} Where `SozcukAdi` LIKE '{}%' ".format(self.category,searchText))#qyery for similars
            query2=("Select `SozcukAdi` from {} Where `SozcukAdi` LIKE '%{}%' ".format(self.category,searchText))#qyery for similars
            cursor = self.conn.cursor()
            if self.findIncludings.isChecked():
                cursor.execute(query2)
            elif not self.findIncludings.isChecked():
                cursor.execute(query1)

            self.relatedList.clear()


            try:#tries to fetch if there is any similar (that includes searchtext) words to row
                row = cursor.fetchall()
            except Exception as e:
                self.resultsBox.clear()
                #print "no similar"
                print(e)

            if len(row)>0:
                    #!=[]: #TODO length ile kontrol
             #if there is any similar word

                for element in row:# for any similar word
                    self.relatedList.addItem(element[0]) # add similar to related list

                    if QtCore.QString.fromUtf8(element[0])==self.searchBox.text(): #if not just similar but exactly same
                        self.printResult( self.getMeaning(  str(QtCore.QString.toUtf8 ( self.searchBox.text())))) #get and print the meaning to resultbox

                try:#makes sure the string that startswith typed one is in related list , visible without scroll and changes its bg color to gray
                    match=self.relatedList.findItems(QtCore.QString.fromUtf8(searchText),QtCore.Qt.MatchStartsWith)
                    self.relatedList.scrollTo(self.relatedList.indexFromItem(match[0]),self.relatedList.EnsureVisible)
                    match[0].setBackgroundColor(QtCore.Qt.lightGray)

                except:
                    self.resultsBox.clear()
                    #print "problem in startswith painting ,showing"



                try:#changes bg color if matching string is found
                    matchexact=self.relatedList.findItems(QtCore.QString.fromUtf8(searchText),QtCore.Qt.MatchExactly)


                    if len(matchexact)>0:
                        matchexact[0].setBackgroundColor(QtCore.Qt.cyan)
                        matchingText=str(QtCore.QString.toUtf8 ((matchexact[0]).text()))

                        self.printResult( self.getMeaning(matchingText))

                    else:
                        self.resultsBox.setText("")

                except Exception as e:
                    print "problem in exact "
                    print(e)



            else :
                pass
            #print self.relatedList.count()



    def getMeaning(self,text):
        query=("select `SozcukAnlami` from {} where `SozcukAdi`='{}' ".format(self.category,text))
        #print query
        cursor = self.conn.cursor()
        cursor.execute(query)

        try:
            row = cursor.fetchall()
            if row:
                return row[0][0]
            else:
                return ""
        except Exception as e:
            print(e)
            return ""










    def relatedSelected(self):
        #self.searchBox.setText()#changes whole content
        #queryit and result# changes only result
        selectedText=self.relatedList.itemFromIndex(self.relatedList.currentIndex()).text()

        query=("select `SozcukAnlami` from {} where `SozcukAdi`='{}' ".format(self.category,unicode(selectedText).encode('utf-8')))
        #print query
        cursor = self.conn.cursor()
        cursor.execute(query)

        try:
            row = cursor.fetchall()
            if row:
                self.printResult(row[0][0])
            else:
                self.resultsBox.setText("")

        except Exception as e:
            print(e)

        finally:
            pass
            # cursor.close()
            # self.conn.close()



    #
    # def searchMatch(self):
    #     currentText=unicode( self.searchBox.text())
    #     if currentText==None or currentText=="" or currentText.startswith(" ") or currentText.startswith("\t"):
    #         self.resultsBox.setText("")
    #         self.relatedList.clear()
    #     else:
    #
    #
    #         pass
    #         # query=("select `SozcukAnlami` from {} where `SozcukAdi`='{}' ".format(self.category,currentText.encode('utf-8')))
    #         # #print query
    #         # cursor = self.conn.cursor()
    #         # cursor.execute(query)
    #         #
    #         # try:
    #         #     row = cursor.fetchall()
    #         #     if row:
    #         #
    #         #         self.printResult(row[0][0])
    #         #     else:
    #         #         self.resultsBox.setText("")
    #         #
    #         # except Error as e:
    #         #     print(e)
    #         #
    #         # finally:
    #         #     pass
    #         #     # cursor.close()
    #         #     # self.conn.close()
    #         self.printRelatives(currentText)

    def closeApplication(self):
        self.conn.close()
        sys.exit(0)
if __name__ == "__main__":
    app.setApplicationName("sozlux") #necessary for phonon module.
    program = Sozlux()
    program.show()
    sys.exit(app.exec_())