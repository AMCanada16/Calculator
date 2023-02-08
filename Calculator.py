#!/usr/bin/env python
#Andrew Mainella
import re
import tkinter as tk

window = tk.Tk()
window.title("Calculator")
window.geometry('200x200')
MainString = ""
decimalplaced = False
def AddString(Input):
    global MainString
    global decimalplaced
    if type(Input) == str:
        if Input == "0":
            if MainString == "":
                return
        if Input == ".":
            if decimalplaced:
                return
            if decimalplaced == False:
                decimalplaced = True
        if Input == "":
            MainString = ""
            MainLabel.config(text=MainString)
            return
        if len(MainString) == 0:
            if Input == "+" or Input == "/" or Input == "*":
                return
        if len(MainString) >= 1:
            LastStringUsed = MainString[-1]
            if LastStringUsed == "+" or LastStringUsed == "*" or LastStringUsed == "-" or LastStringUsed == "/":
                if Input == "+" or Input == "*" or Input == "/":
                    update = MainString[:-1]
                    MainString = update + Input
                    LastStringUsed = Input
                    MainLabel.config(text=MainString)
                    return
                elif Input == "-":
                    if LastStringUsed == "-" or LastStringUsed == "+":
                        update = MainString[:-1]
                        MainString = update + Input
                        LastStringUsed = Input
                        MainLabel.config(text=MainString)
                        return
        update = MainString + Input
        MainString = update
        MainLabel.config(text=MainString)
def RemoveString():
    global MainString
    MainString = MainString[:-1]
    MainLabel.config(text=MainString)
MainStringNew: str = ""
def Calculate():
    def CreateOperations():
        global result
        global operations
        ArrayofResults = [*MainStringNew]
        operationNumber = -1
        operations = []
        result = []
        resultIndex = 0
        NegativeForNext: bool = True
        for i in ArrayofResults:
            if NegativeForNext == False:
                if i == "/" or i == "*" or i == "-" or i == "+":
                    resultIndex = resultIndex + 1
                    NegativeForNext = True
                    continue
            if len(result) <= resultIndex:
                result.append("")
            result[resultIndex] = result[resultIndex] + i
            NegativeForNext = False
        OperationNumberIdx = -1
        for idx,i in enumerate(ArrayofResults):
            if OperationNumberIdx == idx - 1 or idx == 0:
                continue
            if OperationNumberIdx != idx - 1:
                if i == "+" or i == "-" or i == "/" or i == "*":
                    operationNumber = operationNumber + 1
                    if i == "/":
                        operations.append({"Operation":f"{i}", "Index": operationNumber, "ID":1, "SecondIndex":0})
                        OperationNumberIdx = idx
                    if i == "*":
                        operations.append({"Operation":f"{i}", "Index": operationNumber, "ID":2, "SecondIndex":0})
                        OperationNumberIdx = idx
                    if i == "-":
                        operations.append({"Operation":f"{i}", "Index": operationNumber, "ID":3, "SecondIndex":0})
                        OperationNumberIdx = idx
                    if i == "+":
                        operations.append({"Operation":f"{i}", "Index": operationNumber, "ID":4, "SecondIndex":0})
                        OperationNumberIdx = idx
        operations = sorted(operations, key=lambda d:d['ID'])
        for idx,value in enumerate(operations):
            value["SecondIndex"] = idx
        return
    def Operation(Input, op):
        Index = op["Index"]
        NewIndex = Index + 1
        NumberOne = float(result[Index])
        NumberTwo = float(result[NewIndex])
        if Input == 0:
            NewResult = NumberOne/NumberTwo
        if Input == 1:
            NewResult = NumberOne*NumberTwo
        if Input == 2:
            NewResult = NumberOne+NumberTwo
        if Input == 3:
            NewResult = NumberOne-NumberTwo
        result.pop(Index + 1)
        result.pop(Index)
        operations.pop(0)
        return NewResult
    def ReturnString(Input, op):
        global MainString
        global operations
        global MainStringNew
        operations = sorted(operations, key=lambda d:d['Index'])
        result.insert(op["Index"], str(Input))
        for OperationValue in reversed(operations):
            NewIndex = OperationValue["Index"]
            Index = op["Index"]
            if NewIndex <= Index:
                NewIndex = NewIndex + 1
            result.insert(NewIndex, OperationValue["Operation"])
        MainStringNew = "".join(result)
        operations = []
        return
    def OperationRunning():
        global MainString
        global operations
        global MainStringNew
        if len(operations) == 0:
            MainString = MainString + MainStringNew
            return 1
        op = operations[0]
        if op["Operation"] == "/":
            OperationResult = Operation(0, op=op)
            ReturnString(OperationResult, op=op)
            return 0
        if op["Operation"] == "*":
            OperationResult = Operation(1, op=op)
            ReturnString(OperationResult, op=op)
            return 0 
        if op["Operation"] == "+":
            OperationResult = Operation(2, op=op)
            ReturnString(OperationResult, op=op)
            return 0
        if op["Operation"] == "-":
            OperationResult = Operation(3, op=op)
            ReturnString(OperationResult, op=op)
            return 0
    def Main():
        #Start
        global MainStringNew
        global MainString
        Split = re.split("=", MainString)
        spiltresult = Split[-2]
        MainStringNew = spiltresult
        CreateOperations()
        while True:
            code = OperationRunning()
            if code == 1:
                ResultSplit = re.split("=", MainString)
                ResultSplitLast = ResultSplit[-1]
                ResultSplit1 = [*ResultSplitLast]
                ResultSplitLast1 = ResultSplit1[-1]
                ResultSplitLast2 = ResultSplit1[-2]
                if ResultSplitLast1 == "0" and ResultSplitLast2 == ".":
                    Number = float(ResultSplitLast)
                    NewNumber = int(Number)
                    ResultSplit[-1] = f"{NewNumber}"
                    MainString = "=".join(ResultSplit)
                    MainLabel.config(text=MainString)
                else:
                    MainLabel.config(text=MainString)
                return
            CreateOperations()
    Main()
def Equal():
    if MainString != "":
        AddString("=")
        Calculate()
MainLabel = tk.Label(text=MainString)
MainLabel.grid(row = 0, pady = 2, columnspan=4)
ClearButton = tk.Button(text="AC", command=lambda: AddString(""))
ClearButton.grid(row = 1, column = 0, sticky="w", pady = 2)
BackButton = tk.Button(text="<-", command=lambda: RemoveString())
BackButton.grid(row = 1, column = 1, pady= 2)
DevideButton = tk.Button(text="/", command=lambda: AddString("/"))
DevideButton.grid(row = 1, column = 3, sticky="w", pady = 2)
OneButton = tk.Button(text="1", command=lambda: AddString("1"))
OneButton.grid(row = 2, column = 0, sticky="w", pady = 2)
TwoButton = tk.Button(text="2", command=lambda:  AddString("2"))
TwoButton.grid(row = 2, column = 1, sticky="w", pady = 2)
ThreeButton = tk.Button(text="3", command=lambda: AddString("3"))
ThreeButton.grid(row = 2, column = 2, sticky="w", pady = 2)
AddButton = tk.Button(text="+", command=lambda: AddString("+"))
AddButton.grid(row = 2, column = 3, sticky="w", pady = 2)
FourButton = tk.Button(text="4", command=lambda: AddString("4"))
FourButton.grid(row = 3, column = 0, sticky="w", pady = 2)
FiveButton = tk.Button(text="5", command=lambda: AddString("5"))
FiveButton.grid(row = 3, column = 1, sticky="w", pady = 2)
SixButton = tk.Button(text="6", command=lambda: AddString("6"))
SixButton.grid(row = 3, column = 2, sticky="w", pady = 2)
SubtractButton = tk.Button(text="-", command=lambda: AddString("-"))
SubtractButton.grid(row = 3, column = 3, sticky="w", pady = 2)
SevenButton = tk.Button(text="7", command=lambda: AddString("7"))
SevenButton.grid(row = 4, column = 0, sticky="w", pady = 2)
EightButton = tk.Button(text="8", command=lambda: AddString("8"))
EightButton.grid(row = 4, column = 1, sticky="w", pady = 2)
NineButton = tk.Button(text="9", command=lambda: AddString("9"))
NineButton.grid(row = 4, column = 2, sticky="w", pady = 2)
MultiplyButton = tk.Button(text="*", command=lambda: AddString("*"))
MultiplyButton.grid(row = 4, column = 3, sticky="w", pady = 2)
ZeroButton = tk.Button(text="0", command=lambda: AddString("0"))
ZeroButton.grid(row = 5, column = 0, sticky="w", columnspan=2, pady = 2)
DecimalButton = tk.Button(text=".", command=lambda: AddString("."))
DecimalButton.grid(row = 5, column = 2, sticky="w", pady = 2)
EqualButton = tk.Button(text="=", command=lambda: Equal())
EqualButton.grid(row = 5, column = 3, sticky="w", pady = 2)
window.bind('1', lambda event:AddString("1"))
window.bind('2', lambda event:AddString("2"))
window.bind('3', lambda event:AddString("3"))
window.bind('4', lambda event:AddString("4"))
window.bind('5', lambda event:AddString("5"))
window.bind('6', lambda event:AddString("6"))
window.bind('7', lambda event:AddString("7"))
window.bind('8', lambda event:AddString("8"))
window.bind('9', lambda event:AddString("9"))
window.bind('0', lambda event:AddString("0"))
window.bind('=', lambda event:AddString("+"))
window.bind('+', lambda event:AddString("+"))
window.bind('-', lambda event:AddString("-"))
window.bind('/', lambda event:AddString("/"))
window.bind('<Return>', lambda event:Equal())
window.mainloop()