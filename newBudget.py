# Import Session ---------------------------------------------------------------
import sqlite3
import wx
import wx.grid as gridlib
import time
import datetime

# Global Variables -------------------------------------------------------------
conn = sqlite3.connect("budget.db")
cursor = conn.cursor()

## First 3 parameters are mandatory for wx.Frame
##wx.Frame(wx.Window parent, int id=-1, string title='', wx.Point pos = wx.DefaultPosition,
##wx.Size size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE, string name = "frame")

# MainFrame Session ------------------------------------------------------------
class newFrame(wx.Frame):
    def __init__(self, parent, id):
        style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX
        self.total = 0
        wx.Frame.__init__(self, parent, id, title='Budget!', size=(608,700), style=style)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        ## Init main UI
        self.InitUI()

        ## Get data and return total amount
        self.setMonthField(0)
        self.setYearField(0)
        self.GetData((False,False,False,False))
        self.setDefaultSkin()
        self.Center()

    def OnClose(self, event):
        if self.changeUp:
            changeFrame.Destroy(self.frame2)
        if self.addUp:
            AddFrame.Destroy(self.addRecord)
        if self.updateUp:
            UpdateFrame.Destroy(self.updateRecord)
        if self.deleteUp:
            DeleteFrame.Destroy(self.deleteRecord)
        self.Destroy()
    ## InitUI ------------------------------------------------------------------
    def InitUI(self):

        self.changeUp = False
        self.addUp = False
        self.updateUp = False
        self.deleteUp = False
        ## Mainbox contains 2 Panels
        mainBox = wx.BoxSizer(wx.VERTICAL)
        topPanel = wx.Panel(self, -1)
        self.midPanel = wx.Panel(self, -1)
        innerPanel = wx.Panel(self, -1)
        botPanel = wx.Panel(self, -1)

        mainBox.Add(topPanel, 1, wx.EXPAND)
        mainBox.Add(self.midPanel, 1, wx.EXPAND)
        mainBox.Add(innerPanel, 0, wx.EXPAND)
        mainBox.Add(botPanel, 1, wx.EXPAND)

        self.SetSizer(mainBox)

        self.img = wx.StaticBitmap(topPanel)
        self.innerImg = wx.StaticBitmap(innerPanel)

        ## topPanel
        ## topPanel.Buttons
        skinList  = ['Alien','Sparta','eve_gaya']
        self.mainSkin = ['alien.jpg','sparta.jpg','eve_gaya.jpg']
        self.tableSkin = [
                'alien_table_name.jpg',
                'sparta_table_name.jpg',
                'eve_gaya_table_name.jpg']
        self.chooseSkin = wx.ComboBox(self.img, -1, value = 'Alien', pos = (0,0), choices = skinList, style = wx.CB_READONLY)

        self.Bind(wx.EVT_COMBOBOX, self.OnChooseSkin)
        self.change = wx.Button(self.img, -1, "Change", (85,0))
        self.Bind(wx.EVT_BUTTON, self.OnChange, self.change)
        self.add = wx.Button(self.img, -1, "Add", (165,0))
        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.add)
        self.update = wx.Button(self.img, -1, "Update", (245,0))
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.update)
        self.delete = wx.Button(self.img, -1, "Delete", (325,0))
        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.delete)

        ## topPanel.Fields
        self.yearField = wx.StaticText(self.img, -1, "", (110,75))
        self.monthField = wx.StaticText(self.img, -1, "", (110,100))
        self.totalDebitField = wx.StaticText(self.img, -1, "", (110,125))
        self.totalCreditField = wx.StaticText(self.img, -1, "", (110,149))


        ## midPanel contains midBox
        midBox = wx.BoxSizer(wx.VERTICAL)
        self.debitGrid = DebitGrid(self.midPanel)
        ## midBox contains DebitGrid
        midBox.Add(self.debitGrid, 1, wx.EXPAND)
        self.midPanel.SetSizer(midBox)

        ## innerPanel
##        wx.StaticText(innerPanel, -1, "Credit", (0,0))
        ## botPanel contains botBox
        botBox = wx.BoxSizer(wx.VERTICAL)
        self.creditGrid = CreditGrid(botPanel)

        ## botBox contains CreditGrid
        botBox.Add(self.creditGrid, 1, wx.EXPAND)
        botPanel.SetSizer(botBox)

        self.debitGrid.SetMargins(0-wx.SystemSettings_GetMetric(wx.SYS_VSCROLL_X),0)
        self.creditGrid.SetMargins(0-wx.SystemSettings_GetMetric(wx.SYS_VSCROLL_X),0)
        self.debitGrid.ForceRefresh()

    def setDefaultSkin(self):
        skin = self.chooseSkin.GetSelection()
        self.change.Refresh()
        self.add.Refresh()
        self.update.Refresh()
        self.delete.Refresh()
        self.img.SetBitmap(wx.Bitmap(self.chooseSkin.GetValue()+"/"+self.mainSkin[skin]))
        self.innerImg.SetBitmap(wx.Bitmap(self.chooseSkin.GetValue()+"/"+self.tableSkin[skin]))
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        if self.chooseSkin.GetValue() == 'Alien':
            self.yearField.SetBackgroundColour("black")
            self.yearField.SetForegroundColour("white")

            self.yearField.SetFont(font)
            self.monthField.SetBackgroundColour("black")
            self.monthField.SetForegroundColour("white")
            self.monthField.SetFont(font)

            self.totalDebitField.SetBackgroundColour("black")
            self.totalDebitField.SetForegroundColour("white")
            self.totalDebitField.SetFont(font)

            self.totalCreditField.SetBackgroundColour("black")
            self.totalCreditField.SetForegroundColour("white")
            self.totalCreditField.SetFont(font)

            self.debitGrid.setAlienSkin()
            self.creditGrid.setAlienSkin()
        if self.chooseSkin.GetValue() == 'Sparta':
            self.debitGrid.setSpartaSkin()
            self.creditGrid.setSpartaSkin()
        if self.chooseSkin.GetValue() == 'eve_gaya':
            self.yearField.SetBackgroundColour(wx.Colour(73,121,93))
            self.yearField.SetForegroundColour("white")

            self.yearField.SetFont(font)
            self.monthField.SetBackgroundColour(wx.Colour(73,121,93))
            self.monthField.SetForegroundColour("white")
            self.monthField.SetFont(font)

            self.totalDebitField.SetBackgroundColour(wx.Colour(73,121,93))
            self.totalDebitField.SetForegroundColour("white")
            self.totalDebitField.SetFont(font)

            self.totalCreditField.SetBackgroundColour(wx.Colour(73,121,93))
            self.totalCreditField.SetForegroundColour("white")
            self.totalCreditField.SetFont(font)

            self.debitGrid.setEveGayaSkin()
            self.creditGrid.setEveGayaSkin()

    def OnChooseSkin(self, event):
        self.setDefaultSkin()

##        skin = event.GetSelection()
##        self.change.Refresh()
##        self.add.Refresh()
##        self.update.Refresh()
##        self.delete.Refresh()
##        self.img.SetBitmap(wx.Bitmap(self.chooseSkin.GetValue()+"/"+self.mainSkin[skin]))
##        self.innerImg.SetBitmap(wx.Bitmap(self.chooseSkin.GetValue()+"/"+self.tableSkin[skin]))
##        if self.chooseSkin.GetValue() == 'Alien':
##            self.debitGrid.setAlienSkin()
##            self.creditGrid.setAlienSkin()
##            self.debitGrid.ForceRefresh()
##            self.creditGrid.ForceRefresh()
##        if self.chooseSkin.GetValue() == 'Sparta':
##            self.debitGrid.SetLabelBackgroundColour("white")
##            self.debitGrid.SetLabelTextColour("black")

    def getCurrentSkin(self):
        return self.chooseSkin.GetValue()

    def getCurrentSkinPos(self):
        return self.chooseSkin.GetSelection()

    ## GetData -----------------------------------------------------------------
    def GetData(self, yesno):
        ## Get data from DB
        debitCurrentRow = 0
        creditCurrentRow = 0

        ## Debit Query
        sqlDebit = self.getQuery("Debit", yesno)

        ## Credit Query
        sqlCredit = self.getQuery("Credit", yesno)

        with conn:
            self.debitTotal = 0
            self.creditTotal = 0


            ## Execute Debit Query
            cursor.execute(sqlDebit)
            while True:
                debitRow = cursor.fetchone()
                if debitRow is None:
                    break
                self.debitGrid.AppendRows(1)
                self.debitGrid.SetCellValue(debitCurrentRow, 0, str(debitRow[1]))
                self.debitGrid.SetCellValue(debitCurrentRow, 1, str(debitRow[2]))
                self.debitGrid.SetCellValue(debitCurrentRow, 2, str(debitRow[3]))
                self.debitGrid.SetCellValue(debitCurrentRow, 3, str(debitRow[4]))
                self.debitGrid.SetCellValue(debitCurrentRow, 4, str(debitRow[5]))
                debitCurrentRow = debitCurrentRow + 1
                names = list(map(lambda x: x[0], cursor.description))
                ## Get total amount
                for i in range(len(names)):
                    if names[i] == 'Amnt':
                        self.debitTotal = self.debitTotal + debitRow[i]

            ## Execute Credit Query
            cursor.execute(sqlCredit)
            while True:
                creditRow = cursor.fetchone()
                if creditRow is None:
                    break
                self.creditGrid.AppendRows(1)
                self.creditGrid.SetCellValue(creditCurrentRow, 0, str(creditRow[1]))
                self.creditGrid.SetCellValue(creditCurrentRow, 1, str(creditRow[2]))
                self.creditGrid.SetCellValue(creditCurrentRow, 2, str(creditRow[3]))
                self.creditGrid.SetCellValue(creditCurrentRow, 3, str(creditRow[4]))
                self.creditGrid.SetCellValue(creditCurrentRow, 4, str(creditRow[5]))
                creditCurrentRow = creditCurrentRow + 1
                names = list(map(lambda x: x[0], cursor.description))
                ## Get total amount
                for i in range(len(names)):
                    if names[i] == 'Amnt':
                        self.creditTotal = self.creditTotal + creditRow[i]
            self.FillData()
            self.setDefaultSkin()
##            self.debitGrid.setAlienSkin()
##            self.creditGrid.setAlienSkin()

    def getGrid(self, grid):
        if grid == 'Debit':
            return self.debitGrid
        if grid == 'Credit':
            return self.creditGrid

    def FillData(self):
        self.totalDebitField.SetLabel(str(self.debitTotal))
        self.totalCreditField.SetLabel(str(self.creditTotal))

    def setChangeUp(self, yesno):
        self.changeUp = yesno

    def setAddUp(self, yesno):
        self.addUp = yesno

    def setUpdateUp(self, yesno):
        self.updateUp = yesno

    def setDeleteUp(self, yesno):
        self.deleteUp = yesno

    def OnChange(self, event):
        if not self.changeUp:
            self.frame2 = changeFrame(None, -1)
            self.frame2.Show()
            self.changeUp = True
        else:
            changeFrame.Destroy(self.frame2)
            self.changeUp = False

    def OnAdd(self, event):
        if not self.addUp:
            self.addRecord = AddFrame(None, -1)
            self.addRecord.Show()
            self.addUp = True
        else:
            AddFrame.Destroy(self.addRecord)
            self.addUp = False

    def OnUpdate(self, event):
        if not self.updateUp:
            self.updateRecord = UpdateFrame(None, -1)
            self.updateRecord.Show()
            self.updateUp = True
        else:
            UpdateFrame.Destroy(self.updateRecord)
            self.updateUp = False

    def OnDelete(self, event):
        if not self.deleteUp:
            self.deleteRecord = DeleteFrame(None, -1)
            self.deleteRecord.Show()
            self.deleteUp = True
        else:
            DeleteFrame.Destroy(self.deleteRecord)
            self.deleteUp = False

    ## Getters and Setters
    def setDebitTotal(self, newTotalField):
        self.totalDebitField.SetLabel(str(newTotalField))

    def setCreditTotal(self, newTotalField):
        self.totalCreditField.SetLabel(str(newTotalField))

    def setYearField(self, newYearField):
        if newYearField == 0:
            self.yearField.SetLabel(str(time.strftime("%Y")))
        else:
            self.yearField.SetLabel(str(newYearField))

    def getYearField(self):
        return self.yearField.GetLabel()

    def setMonthField(self, newMonthField):
        if newMonthField == 0:
            self.monthField.SetLabel(time.strftime("%B"))
        else:
            self.monthField.SetLabel(str(newMonthField))

    def getMonthField(self):
        return self.monthField.GetLabel()

    def getQuery(self, table, yesno):
        types = ('Food','Car','Games','ACP','Misc')
        whereInserted = False
        descInserted = False
        readMonthInput = self.getMonthField()
        if readMonthInput == "All":
            sqlWhereMonth = ""
            if str(self.getYearField()) == "All":
                sqlWhereYear = ""
            else:
                sqlWhereYear = " WHERE Year = " + str(self.getYearField())
                whereInserted = True
        else:
            sqlWhereMonth = " WHERE Month = " + "'" + self.getMonthField() + "'"
            whereInserted = True
            if str(self.getYearField()) == "All":
                sqlWhereYear = ""
            else:
                sqlWhereYear = " AND Year = " + str(self.getYearField())
        for i in range(len(yesno)):
            if yesno[i]:
                if whereInserted:
                    if descInserted:
                        sqlWhereYear = sqlWhereYear + " OR Desc = " + "'" + types[i] + "'"
                    else:
                        descInserted = True
                        sqlWhereYear = sqlWhereYear + " AND (Desc = " + "'" + types[i] + "'"
                else:
                    sqlWhereYear = sqlWhereYear + " WHERE (Desc = " + "'" + types[i] + "'"
                    whereInserted = True
                    descInserted = True
        if descInserted:
            sqlWhereYear += ")"
##        orderBy = " ORDER BY Year, Month, Day"
        orderBy = " ORDER BY Year, Day ASC, Month DESC"
        sqlSelect = "SELECT * FROM " + table
        sql = sqlSelect + sqlWhereMonth + sqlWhereYear + orderBy
        whereInserted = False
        descInserted = False
        return sql

## Change Screen
class changeFrame(wx.Frame):
    def __init__(self, parent, id):
        style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, parent, id, title='Frame Name', pos = wx.Point(450,170), size=(205,325), style=style)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        ## Init UI
        self.InitUI()

    def OnClose(self, event):
        newFrame.setChangeUp(frame, False)
        self.Destroy()

    def InitUI(self):
        mainPanel = wx.Panel(self, -1)
        self.img = wx.StaticBitmap(mainPanel)
        months = ['All','January','February','March','April','May','June',
                  'July','August','September','October','November','December']
        self.years = ['All']
        self.changeSkin = [
                'alien_change.jpg',
                'sparta_change.jpg',
                'eve_gaya_change.jpg']
        ## Set Years
        self.setYear()

        ## Fields
        self.chooseYear = wx.ComboBox(self.img, -1, value = str(newFrame.getYearField(frame)), pos = (85,63), choices = self.years, style = wx.CB_READONLY)
        self.chooseMonth = wx.ComboBox(self.img, -1, value = str(newFrame.getMonthField(frame)), pos = (85,93), choices = months, style = wx.CB_READONLY)
        self.yesnoFood = wx.CheckBox(self.img, -1, "", (75, 137))
        self.yesnoCar = wx.CheckBox(self.img, -1, "", (75, 162))
        self.yesnoMisc = wx.CheckBox(self.img, -1, "", (75, 185))
        self.yesnoGames = wx.CheckBox(self.img, -1, "", (75, 208))
        self.yesnoACP = wx.CheckBox(self.img, -1, "", (145, 137))

        ## Buttons
        changeButton = wx.Button(self.img, -1, "Change!", (60, 250))
        self.Bind(wx.EVT_BUTTON, self.OnChange, changeButton)

        self.setSkin()
    def getYesnoFields(self):
        return self.yesnoFood.GetValue(), self.yesnoCar.GetValue(), self.yesnoGames.GetValue(), self.yesnoACP.GetValue(), self.yesnoMisc.GetValue()

    def setSkin(self):
        skin = newFrame.getCurrentSkin(frame)
        skinPos = newFrame.getCurrentSkinPos(frame)
        self.img.SetBitmap(wx.Bitmap(skin+"/"+self.changeSkin[skinPos]))

    def setYear(self):
        ## Year Query
        sqlDebitYear = "SELECT Year FROM Debit ORDER BY Year"
        sqlCreditYear = "SELECT Year FROM Credit ORDER BY Year"

        ## Execute Debit Year Query
        cursor.execute(sqlDebitYear)
        while True:
            debitYearRow = cursor.fetchone()
            if debitYearRow is None:
                break
            if self.years.count(str(debitYearRow[0])) == 0:
                self.years = self.years + [str(debitYearRow[0])]

        ## Execute Credit Year Query
        cursor.execute(sqlCreditYear)
        while True:
            creditYearRow = cursor.fetchone()
            if creditYearRow is None:
                break
            if self.years.count(str(creditYearRow[0])) == 0:
                self.years = self.years + [str(creditYearRow[0])]

    def OnChange(self, event):
        DebitGrid.ClearData(frame.debitGrid)
        CreditGrid.ClearData(frame.creditGrid)
        newFrame.setYearField(frame, self.chooseYear.GetValue())
        newFrame.setMonthField(frame, self.chooseMonth.GetValue())
        yesno = self.getYesnoFields()
        newFrame.GetData(frame, yesno)

##    def OnSelect(self, event):

class AddFrame(wx.Frame):
    def __init__(self, parent, id):
        style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, parent, id, title='Add Record', pos = wx.Point(355,170), size=(300,300), style=style)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.InitUI()

    def OnClose(self, event):
        newFrame.setAddUp(frame, False)
        self.Destroy()

    def InitUI(self):
        mainPanel = wx.Panel(self, -1)
        descs = ['Food','Car','Games','ACP','Misc']
        types = ['Debit','Credit']
        self.addSkin = [
                'alien_add.jpg',
                'sparta_add.jpg',
                'eve_gaya_add.jpg']
        self.img = wx.StaticBitmap(mainPanel)
        ## Buttons
        addButton = wx.Button(self.img, -1, "Add!", (100,225))
        self.Bind(wx.EVT_BUTTON, self.OnAdd, addButton)

        ## Input fields
        self.inputDay = wx.DatePickerCtrl(self.img, -1, pos = (110,62), style = wx.DP_DROPDOWN)
        self.inputAmount = wx.TextCtrl(self.img, -1, "", (110,91))
        self.chooseDesc = wx.ComboBox(self.img, -1, value = 'Food', pos = (110,120), choices = descs, style = wx.CB_READONLY)
        self.inputNote = wx.TextCtrl(self.img, -1, "", (110,149), size=(150,-1))
        self.chooseType = wx.ComboBox(self.img, -1, value = 'Debit', pos = (110,177), choices = types, style = wx.CB_READONLY)

        self.setSkin()

    def setSkin(self):
        skin = newFrame.getCurrentSkin(frame)
        skinPos = newFrame.getCurrentSkinPos(frame)
        self.img.SetBitmap(wx.Bitmap(skin+"/"+self.addSkin[skinPos]))

    def OnAdd(self, event):
        oDay = 0
        oMonth = ""
        oYear = 0
        oAmount = 0
        oDesc = 0
        oNote = ""
        oType = ""

        ## Get Date
        date = self.inputDay.GetValue()
        oMonth = date.GetMonthName(date.GetMonth())
        oYear = date.GetYear()
        oDate = date.Format("%d/%m/%Y")

        ## Get Amount
        oAmount = self.checkAmount()

        ## Get Description
        oDesc = self.chooseDesc.GetValue()

        ## Get Note
        oNote = self.inputNote.GetValue()

        ## Get Type
        oType = self.chooseType.GetValue()

        insertBudget = (str(oYear),oMonth,str(oDate),oAmount,oDesc,oNote)

        if oAmount == "" or oNote == "":
            errorMessage = wx.MessageDialog(None, 'Blank field!','Oops!',wx.OK)
            errorMessage.ShowModal()
            errorMessage.Destroy()
        else:
            with conn:
                if oType == "Debit":
                    cursor.execute("INSERT INTO Debit VALUES(?,?,?,?,?,?)", insertBudget)
                if oType == "Credit":
                    cursor.execute("INSERT INTO Credit VALUES(?,?,?,?,?,?)", insertBudget)

            self.inputAmount.SetValue("")
            self.inputNote.SetValue("")
            DebitGrid.ClearData(frame.debitGrid)
            CreditGrid.ClearData(frame.creditGrid)
            newFrame.GetData(frame, (False,False,False,False))

    def checkAmount(self):
        oAmount = ""
        for i in self.inputAmount.GetValue():
            if i == ",":
                oAmount += "."
            else:
                oAmount += i
        return oAmount

class UpdateFrame(wx.Frame):
    def __init__(self, parent, id):
        style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, parent, id, title='Update Record', pos = wx.Point(75,170), size=(580,350), style=style)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.InitUI()

    def OnClose(self, event):
        newFrame.setUpdateUp(frame, False)
        self.Destroy()

    def InitUI(self):
        mainPanel = wx.Panel(self, -1)
        self.img = wx.StaticBitmap(mainPanel)
        descs = ['Food','Car','Games','Misc']
        types = ['Debit','Credit']
        self.updateSkin = [
                'alien_update.jpg',
                'sparta_update.jpg',
                'eve_gaya_update.jpg']

        ## Buttons
        fetchButton = wx.Button(self.img, -1, "Fetch!",(30,274))
        updateButton = wx.Button(self.img, -1, "Update!", (110,274))
        self.Bind(wx.EVT_BUTTON, self.OnFetch, fetchButton)
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, updateButton)

        ##
        self.chooseTable = wx.ComboBox(self.img, -1, value = 'Debit', pos = (75,53), choices = types, style = wx.CB_READONLY)
        self.inputRow = wx.TextCtrl(self.img, -1, "", (75,78), size=(30,-1))

        ## Display fields FROM
        self.displayDay = wx.DatePickerCtrl(self.img, -1, pos = (110,120), style = wx.DP_DROPDOWN)
        self.displayAmount = wx.TextCtrl(self.img, -1, "", (110,146))
        self.displayDesc = wx.ComboBox(self.img, -1, value = 'Food', pos = (110,172), choices = descs, style = wx.CB_READONLY)
        self.displayNote = wx.TextCtrl(self.img, -1, "", (110,198), size=(150,-1))
        self.displayType = wx.ComboBox(self.img, -1, value = 'Debit', pos = (110,223), choices = types, style = wx.CB_READONLY)

        self.displayDay.Disable()
        self.displayAmount.Disable()
        self.displayDesc.Disable()
        self.displayNote.Disable()
        self.displayType.Disable()

        ## Input fields TO
        self.inputDay = wx.DatePickerCtrl(self.img, -1, pos = (384,120), style = wx.DP_DROPDOWN)
        self.inputAmount = wx.TextCtrl(self.img, -1, "", (384,146))
        self.chooseDesc = wx.ComboBox(self.img, -1, value = 'Food', pos = (384,172), choices = descs, style = wx.CB_READONLY)
        self.inputNote = wx.TextCtrl(self.img, -1, "", (384,198), size=(150,-1))
        self.chooseType = wx.ComboBox(self.img, -1, value = 'Debit', pos = (384,223), choices = types, style = wx.CB_READONLY)

        self.setSkin()

    def setSkin(self):
        skin = newFrame.getCurrentSkin(frame)
        skinPos = newFrame.getCurrentSkinPos(frame)
        self.img.SetBitmap(wx.Bitmap(skin+"/"+self.updateSkin[skinPos]))

    def OnFetch(self, event):
        grid = newFrame.getGrid(frame, str(self.chooseTable.GetValue()))
        fetchRow = int(self.inputRow.GetValue())-1
        if fetchRow <> "":
            iday,imonth,iyear = str(grid.GetCellValue(fetchRow,1)).split('/')
            itime = wx.DateTimeFromDMY(int(iday),int(imonth)-1,int(iyear))
            self.displayDay.SetValue(itime)

            self.displayAmount.SetValue(str(grid.GetCellValue(fetchRow,2)))
            self.displayDesc.SetValue(str(grid.GetCellValue(fetchRow,3)))
            self.displayNote.SetValue(str(grid.GetCellValue(fetchRow,4)))
            self.displayType.SetValue(str(self.chooseTable.GetValue()))

            self.inputDay.SetValue(self.displayDay.GetValue())
            self.inputAmount.SetValue(self.displayAmount.GetValue())
            self.chooseDesc.SetValue(self.displayDesc.GetValue())
            self.inputNote.SetValue(self.displayNote.GetValue())
            self.chooseType.SetValue(self.displayType.GetValue())

    def OnUpdate(self, event):
        if self.inputAmount.GetValue() == "" or self.inputNote.GetValue() == "":
            errorMessage = wx.MessageDialog(None, 'Blank field!','Oops!',wx.OK)
            errorMessage.ShowModal()
            errorMessage.Destroy()
        else:
            fetchDate = self.displayDay.GetValue()
            iYear = fetchDate.GetYear()
            iMonth = fetchDate.GetMonthName(fetchDate.GetMonth())
            iDate = fetchDate.Format("%d/%m/%Y")
            iAmount = self.displayAmount.GetValue()
            iDesc = self.displayDesc.GetValue()
            iNote = self.displayNote.GetValue()
            iType = self.displayType.GetValue()

            date = self.inputDay.GetValue()
            oMonth = date.GetMonthName(date.GetMonth())
            oYear = date.GetYear()
            oDate = date.Format("%d/%m/%Y")

            ## Get Amount
            oAmount = self.checkAmount()

            ## Get Description
            oDesc = self.chooseDesc.GetValue()

            ## Get Note
            oNote = self.inputNote.GetValue()

            ## Get Type
            oType = self.chooseType.GetValue()

            with conn:
                if oType == "Debit":
                    updateDebit = (
                         "UPDATE Debit "
                        +"SET Year =" + str(oYear)
                        +", Month =" + "'" + oMonth + "'"
                        +",Day =" + "'" + str(oDate) + "'"
                        +",Amnt =" + str(oAmount)
                        +",Desc =" + "'" + str(oDesc) + "'"
                        +",Note =" + "'" + str(oNote) + "'"
                        +" WHERE Year =" + str(iYear)
                        +" AND Month =" + "'" + str(iMonth) + "'"
                        +" AND Day =" + "'" + str(iDate) + "'"
                        +" AND Amnt =" + str(iAmount)
                        +" AND Desc =" + "'" + str(iDesc) + "'"
                        +" AND Note =" + "'" + str(iNote) + "'"
                        )
                    testsql = "UPDATE Debit SET Amnt=30 WHERE Day=" + "'" + str(iDate) + "'"
                    cursor.execute(updateDebit)
                if oType == "Credit":
                    updateCredit = (
                         "UPDATE Credit "
                        +"SET Year =" + str(oYear)
                        +",Month =" + str(oMonth)
                        +",Day =" + str(oDate)
                        +",Amnt =" + str(oAmount)
                        +",Desc =" + oType
                        +",Note =" + oNote
                        +" WHERE Year =" + str(iYear)
                        +" AND Month =" + str(iMonth)
                        +" AND Day =" + str(iDate)
                        +" AND Amount =" + str(iAmount)
                        +" AND Desc =" + str(iDesc)
                        +" AND Note =" + str(iNote)
                        )
                    cursor.execute(updateSQL)

            self.inputAmount.SetValue("")
            self.inputNote.SetValue("")
            DebitGrid.ClearData(frame.debitGrid)
            CreditGrid.ClearData(frame.creditGrid)
            newFrame.GetData(frame,(False,False,False,False))

    def checkAmount(self):
        self.Amount = ""
        for i in self.inputAmount.GetValue():
            if i == ",":
                self.Amount += "."
            else:
                self.Amount += i
        return self.Amount

class DeleteFrame(wx.Frame):
    def __init__(self, parent, id):
        style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, parent, id, title='Update Record', pos = wx.Point(465,170), size=(190,200), style=style)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.InitUI()

    def OnClose(self, event):
        newFrame.setDeleteUp(frame, False)
        self.Destroy()

    def InitUI(self):
        mainPanel = wx.Panel(self, -1)
        self.img = wx.StaticBitmap(mainPanel)
        types = ['Debit','Credit']
        self.deleteSkin = [
                'alien_delete.jpg',
                'sparta_delete.jpg',
                'eve_gaya_delete.jpg']

        ## Buttons
        deleteButton = wx.Button(self.img, -1, "Delete!", (50, 130))
        self.Bind(wx.EVT_BUTTON, self.OnDelete, deleteButton)

        ## Fields
        self.chooseTable = wx.ComboBox(self.img, -1, value = 'Debit', pos = (75,58), choices = types, style = wx.CB_READONLY)
        self.inputRow = wx.TextCtrl(self.img, -1, "", (75,84), size=(30,-1))

        self.setSkin()

    def setSkin(self):
        skin = newFrame.getCurrentSkin(frame)
        skinPos = newFrame.getCurrentSkinPos(frame)
        self.img.SetBitmap(wx.Bitmap(skin+"/"+self.deleteSkin[skinPos]))

    def OnDelete(self, event):
        grid = newFrame.getGrid(frame, str(self.chooseTable.GetValue()))
        readRow = int(self.inputRow.GetValue())-1
        if readRow <> "":
            readDate = grid.GetCellValue(readRow,1)
            readAmountRow = (str(grid.GetCellValue(readRow,2)))
            readDescRow = (str(grid.GetCellValue(readRow,3)))
            readNoteRow = (str(grid.GetCellValue(readRow,4)))
            readType = (str(self.chooseTable.GetValue()))

            with conn:
                deleteSQL = (
                            "DELETE FROM " + readType
                            + " WHERE Day =" + "'" + readDate + "'"
                            + " AND Amnt =" + readAmountRow
                            + " AND Desc =" + "'" + readDescRow + "'"
                            + " AND Note =" + "'" + readNoteRow + "'"
                            )
                cursor.execute(deleteSQL)

            self.inputRow.SetValue("")
            DebitGrid.ClearData(frame.debitGrid)
            CreditGrid.ClearData(frame.creditGrid)
            newFrame.GetData(frame, (False,False,False,False))

## Debit grid
class DebitGrid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.CreateGrid(0,5)
        self.SetColLabelValue(0, "Month")
        self.SetColLabelValue(1, "Day")
        self.SetColLabelValue(2, "Amount")
        self.SetColLabelValue(3, "Type")
        self.SetColLabelValue(4, "Note")
        self.SetColSize(4, 200)

##        self.setAlienSkin()

    def ClearData(self):
        self.ClearGrid()
        if self.GetNumberRows() <> 0:
            self.DeleteRows(numRows = self.GetNumberRows())

    def setAlienSkin(self):
        self.SetLabelBackgroundColour("black")
        self.SetLabelTextColour("white")
        attr = gridlib.GridCellAttr()
        attr.SetBackgroundColour("black")
        for i in range(self.GetNumberRows()):
            self.SetRowAttr(i, attr)
            for t in range(self.GetNumberCols()):
                self.SetCellTextColour(i,t,"white")
        self.SetDefaultCellBackgroundColour("black")
        self.ForceRefresh()

    def setSpartaSkin(self):
        self.SetLabelBackgroundColour("white")
        self.SetLabelTextColour("black")
        attr = gridlib.GridCellAttr()
        attr.SetBackgroundColour("white")
        for i in range(self.GetNumberRows()):
            self.SetRowAttr(i, attr)
            for t in range(self.GetNumberCols()):
                self.SetCellTextColour(i,t,"black")
        self.SetDefaultCellBackgroundColour("white")
        self.ForceRefresh()

    def setEveGayaSkin(self):
        self.SetLabelBackgroundColour("white")
        self.SetLabelTextColour("black")
        attr = gridlib.GridCellAttr()
        attr.SetBackgroundColour("white")
        for i in range(self.GetNumberRows()):
            self.SetRowAttr(i, attr)
            for t in range(self.GetNumberCols()):
                self.SetCellTextColour(i,t,"black")
        self.SetDefaultCellBackgroundColour("white")
        self.ForceRefresh()


## Credit Grid
class CreditGrid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.CreateGrid(0,5)
        self.SetColLabelValue(0, "Month")
        self.SetColLabelValue(1, "Day")
        self.SetColLabelValue(2, "Amount")
        self.SetColLabelValue(3, "Type")
        self.SetColLabelValue(4, "Note")
        self.SetColSize(4, 200)

##        self.setAlienSkin()

    def ClearData(self):
        self.ClearGrid()
        if self.GetNumberRows() <> 0:
            self.DeleteRows(numRows = self.GetNumberRows())

    def setAlienSkin(self):
        self.SetLabelBackgroundColour("black")
        self.SetLabelTextColour("white")
        attr = gridlib.GridCellAttr()
        attr.SetBackgroundColour("black")
        for i in range(self.GetNumberRows()):
            self.SetRowAttr(i, attr)
            for t in range(self.GetNumberCols()):
                self.SetCellTextColour(i,t,"white")
        self.SetDefaultCellBackgroundColour("black")
        self.ForceRefresh()

    def setSpartaSkin(self):
        self.SetLabelBackgroundColour("white")
        self.SetLabelTextColour("black")
        attr = gridlib.GridCellAttr()
        attr.SetBackgroundColour("white")
        for i in range(self.GetNumberRows()):
            self.SetRowAttr(i, attr)
            for t in range(self.GetNumberCols()):
                self.SetCellTextColour(i,t,"black")
        self.SetDefaultCellBackgroundColour("white")
        self.ForceRefresh()

    def setEveGayaSkin(self):
        self.SetLabelBackgroundColour("white")
        self.SetLabelTextColour("black")
        attr = gridlib.GridCellAttr()
        attr.SetBackgroundColour("white")
        for i in range(self.GetNumberRows()):
            self.SetRowAttr(i, attr)
            for t in range(self.GetNumberCols()):
                self.SetCellTextColour(i,t,"black")
        self.SetDefaultCellBackgroundColour("white")
        self.ForceRefresh()

if __name__=='__main__':
    app = wx.App()
    frame = newFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()

if conn:
    conn.close()