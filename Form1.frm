VERSION 5.00
Begin VB.Form Form1 
   BackColor       =   &H80000001&
   BorderStyle     =   1  'Fixed Single
   Caption         =   $"Form1.frx":0000
   ClientHeight    =   8880
   ClientLeft      =   0
   ClientTop       =   0
   ClientWidth     =   15345
   DrawStyle       =   -9510  'Solid
   DrawWidth       =   10
   FillStyle       =   9  'Solid
   BeginProperty Font 
      Name            =   "Arial"
      Size            =   8.25
      Charset         =   0
      Weight          =   400
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   Icon            =   "Form1.frx":0009
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   8880
   ScaleWidth      =   15345
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Dim appVisio As Visio.Application
Dim docVisio As Visio.Document
Dim pagesVisio As Visio.Pages
Dim pageVisio As Visio.Page
Dim shapesVisio As Visio.Shapes
Dim shapeVisio As Visio.Shape
Dim shapeTo As Visio.Shape
Dim shapeFrom As Visio.Shape
Dim shapeCur As Visio.Shape
Dim charactersVisio As Visio.Characters
Dim cellColorVisio As Visio.Cell
Dim cellStyleVisio As Visio.Cell
Dim connects As Visio.connects
Dim connect As Visio.connect

Dim outputFilename As String
Dim outputFile
Dim FSO
Dim ts


Private Function CharacterFormatEnd(visShape As Visio.Shape, iBegin As Integer) As Integer
   Dim visChars As Visio.Characters
   Dim iLen As Integer, i As Integer, iFirstRow As Integer, iRow As Integer
   iRow = -1
   iLen = Len(visShape.Text)
   For i = iBegin To iLen
      Set visChars = visShape.Characters
      visChars.Begin = i
      visChars.End = i + 1
      If iRow = -1 Then iFirstRow = visChars.CharPropsRow(visBiasLeft)
      iRow = visChars.CharPropsRow(visBiasLeft)
      If iRow <> iFirstRow Then
         CharacterFormatEnd = i
         Exit Function
      End If
   Next
   CharacterFormatEnd = Len(visShape.Text)
End Function


Private Sub GetData(pageName As String)
    Set pagesVisio = docVisio.Pages
    Dim pageNumber As Integer
    Dim arcs As Integer
    Dim states As Integer
    Dim labl As String
    pageNumber = 0
    For Each pageVisio In pagesVisio
        arcs = 0
        states = 0
        labl = ""
        If Len(pageName) > 0 Then
            If StrComp(pageName, pageVisio.Name) Then
                GoTo SKIP_PAGE_
            End If
        End If
        outputFile.WriteLine (Chr(10) & "page " & pageVisio.Name)
        List1.AddItem ("page " & pageVisio.Name)
        pageNumber = pageNumber + 1
        Set shapesVisio = pageVisio.Shapes
        For Each shapeVisio In shapesVisio
            Set charactersVisio = shapeVisio.Characters
            If InStr(1, shapeVisio.Name, "state") > 0 Then
                outputFile.WriteLine ("    state " & UCase(charactersVisio.Text))
                List1.AddItem ("    state " & UCase(charactersVisio.Text))
                List1.ListIndex = List1.ListCount - 1
                states = states + 1
            ElseIf InStr(1, shapeVisio.Name, "arrow") > 0 Then
                If shapeVisio.connects.Count > 1 Then
                    Set shapeFrom = shapeVisio.connects(1).ToSheet
                    Set shapeTo = shapeVisio.connects(2).ToSheet
                    If InStr(1, shapeFrom.Name, "state") > 0 And InStr(1, shapeTo.Name, "state") > 0 Then
                        outputFile.WriteLine ("    link " & Replace(shapeVisio.Name, " ", "_") & " [" & UCase(shapeFrom.Characters.Text) & "] -> [" & UCase(shapeTo.Characters.Text) & "]")
                        Dim iBegin As Integer, iEnd As Integer, iRow As Integer, sColor As String, tmpTxt As String
                        tmpTxt = ""
                        iBegin = 0
                        For iRow = 0 To shapeVisio.RowCount(visSectionCharacter)
                            iEnd = CharacterFormatEnd(shapeVisio, iBegin)
                            charactersVisio.Begin = iBegin
                            charactersVisio.End = iEnd
                            Set cellColorVisio = shapeVisio.CellsSRC(visSectionCharacter, iRow, visCharacterColor)
                            Set cellStyleVisio = shapeVisio.CellsSRC(visSectionCharacter, iRow, visCharacterStyle)
                            sColor = Replace(cellColorVisio.Formula, "THEMEGUARD", "")
                            If sColor = "0" Or sColor = "" Then
                                sColor = "(RGB(0;0;0))"
                            ElseIf sColor = "2" Then
                                sColor = "(RGB(255;0;0))"
                            ElseIf sColor = "9" Then
                                sColor = "(RGB(0;128;0))"
                            ElseIf sColor = "4" Then
                                sColor = "(RGB(0;0;255))"
                            ElseIf sColor = "11" Then
                                sColor = "(RGB(128;128;0))"
                            End If
                            sColor = Replace(sColor, "(RGB(", "[")
                            sColor = Replace(sColor, "))", "]")
                            sColor = Replace(sColor, ")", "]")
                            sColor = Replace(sColor, "RGB(", "[")
                            If sColor <> "[0;0;0]" And sColor <> "[255;0;0]" And sColor <> "[0;128;0]" And sColor <> "[0;0;255]" And sColor <> "[128;128;0]" Then
                                outputFile.WriteLine ("        ERROR! text on link [" & shapeVisio.Name & "] have wrong color: " & sColor)
                                List1.AddItem ("ERROR! text on link [" & shapeVisio.Name & "] have wrong color: " & sColor)
                                List1.ListIndex = List1.ListCount - 1
                            End If
                            tmpTxt = tmpTxt & "        " & "{" & sColor & "#" & cellStyleVisio & "#" & Replace(charactersVisio.Text, Chr(10), "\n") & "} " & Chr(10)
                            iBegin = iEnd
                        Next
                        outputFile.WriteLine (tmpTxt)
                        List1.AddItem ("    link " & Replace(shapeVisio.Name, " ", "_") & " [" & UCase(shapeFrom.Characters.Text) & "] -> [" & UCase(shapeTo.Characters.Text) & "]")
                        List1.ListIndex = List1.ListCount - 1
                        arcs = arcs + 1
                        ' List1.Refresh
                End If
                Else
                    outputFile.WriteLine ("        ERROR! link [" & shapeVisio.Name & "] have only " & shapeVisio.connects.Count & " connects")
                    List1.AddItem ("ERROR! link [" & shapeVisio.Name & "] have only " & shapeVisio.connects.Count & " connects")
                    List1.ListIndex = List1.ListCount - 1
                    ' List1.Refresh
                End If
            ElseIf InStr(1, shapeVisio.Name, "label") > 0 Then
                outputFile.WriteLine ("    label " & Replace(charactersVisio.Text, Chr(10), "\n"))
                List1.AddItem ("    label " & Replace(charactersVisio.Text, Chr(10), " "))
                List1.ListIndex = List1.ListCount - 1
                ' List1.Refresh
                labl = Replace(charactersVisio.Text, Chr(10), " ")
            End If
        Next shapeVisio
        If states = 0 Then
            outputFile.WriteLine ("        ERROR! no states found on page " & pageVisio.Name)
            List1.AddItem ("ERROR! no states found on page " & pageVisio.Name)
            List1.ListIndex = List1.ListCount - 1
            ' List1.Refresh
        End If
        If arcs = 0 Then
            outputFile.WriteLine ("        ERROR! no arcs found on page " & pageVisio.Name)
            List1.AddItem ("ERROR! no arcs found on page " & pageVisio.Name)
            List1.ListIndex = List1.ListCount - 1
            ' List1.Refresh
        End If
        If labl = "" Then
            outputFile.WriteLine ("        ERROR! no label found on page " & pageVisio.Name)
            List1.AddItem ("ERROR! no label found on page " & pageVisio.Name)
            List1.ListIndex = List1.ListCount - 1
            ' List1.Refresh
        End If
SKIP_PAGE_:
    Next pageVisio
    List1.AddItem ("DONE, number of pages is " & pageNumber)
    List1.ListIndex = List1.ListCount - 1
    ' List1.Refresh
End Sub


Private Sub GetIndex()
    Set pagesVisio = docVisio.Pages
    Dim pageNumber As Integer
    Dim arcs As Integer
    Dim states As Integer
    Dim labl As String
    pageNumber = 0
    For Each pageVisio In pagesVisio
        arcs = 0
        states = 0
        labl = ""
        outputFile.WriteLine ((pageNumber) & " " & pageVisio.Name)
        List1.AddItem ("page " & pageNumber & " " & pageVisio.Name)
        pageNumber = pageNumber + 1
    Next pageVisio
    List1.AddItem ("DONE, number of pages is " & pageNumber)
    List1.ListIndex = List1.ListCount - 1
End Sub


Sub ScanCurrentDocument()
    Dim sArgs() As String
    Dim iLoop As Integer
    
    outputFilename = "./data.txt"
    
    List1.AddItem ("Looking for Microsoft Visio")
    List1.ListIndex = List1.ListCount - 1
    ' List1.Refresh
    Set appVisio = GetObject(, "visio.application")
    If appVisio Is Nothing Then
        Set appVisio = CreateObject("visio.application")
        If appVisio Is Nothing Then
            List1.AddItem ("Error Opening Visio!")
            List1.ListIndex = List1.ListCount - 1
            ' List1.Refresh
            GoTo EXIT_
        End If
    End If
      
    Set docVisio = appVisio.ActiveDocument
    If docVisio Is Nothing Then
        List1.AddItem ("Please Open Microsoft Visio Document")
        List1.ListIndex = List1.ListCount - 1
        ' List1.Refresh
        GoTo EXIT_
    End If
         
    Set outputFile = FSO.CreateTextFile(outputFilename)
        
    List1.AddItem ("Scanning current Microsoft Visio document")
    List1.ListIndex = List1.ListCount - 1
    ' List1.Refresh
    GetData ("")
    
    outputFile.Close
  
    List1.AddItem ("File  " + outputFilename + " created")
    List1.ListIndex = List1.ListCount - 1
    ' List1.Refresh
     
EXIT_:

End Sub


Sub ScanCurrentPage()
    Dim sArgs() As String
    Dim iLoop As Integer
    
    outputFilename = "./data.txt"
    
    List1.AddItem ("Looking for Microsoft Visio")
    List1.ListIndex = List1.ListCount - 1
    ' List1.Refresh
    Set appVisio = GetObject(, "visio.application")
    If appVisio Is Nothing Then
        Set appVisio = CreateObject("visio.application")
        If appVisio Is Nothing Then
            List1.AddItem ("Error Opening Visio!")
            List1.ListIndex = List1.ListCount - 1
            ' List1.Refresh
            GoTo EXIT_
        End If
    End If
      
    Set docVisio = appVisio.ActiveDocument
    If docVisio Is Nothing Then
        List1.AddItem ("Please Open Microsoft Visio Document")
        List1.ListIndex = List1.ListCount - 1
        ' List1.Refresh
        GoTo EXIT_
    End If
         
    Set outputFile = FSO.CreateTextFile(outputFilename)
        
    List1.AddItem ("Scanning current page")
    List1.ListIndex = List1.ListCount - 1
    ' List1.Refresh
    GetData (appVisio.ActivePage.Name)
    
    outputFile.Close
  
    List1.AddItem ("File  " + outputFilename + " created")
    List1.ListIndex = List1.ListCount - 1
    ' List1.Refresh
     
EXIT_:

End Sub


Sub BuildIndexWholeDocument()
    Dim sArgs() As String
    Dim iLoop As Integer
    
    outputFilename = "./index.txt"
    
    List1.AddItem ("Looking for Microsoft Visio")
    List1.ListIndex = List1.ListCount - 1
    Set appVisio = GetObject(, "visio.application")
    If appVisio Is Nothing Then
        Set appVisio = CreateObject("visio.application")
        If appVisio Is Nothing Then
            List1.AddItem ("Error Opening Visio!")
            List1.ListIndex = List1.ListCount - 1
            GoTo EXIT_
        End If
    End If
      
    Set docVisio = appVisio.ActiveDocument
    If docVisio Is Nothing Then
        List1.AddItem ("Please Open Microsoft Visio Document")
        List1.ListIndex = List1.ListCount - 1
        GoTo EXIT_
    End If
         
    Set outputFile = FSO.CreateTextFile(outputFilename)
        
    List1.AddItem ("Scanning current Microsoft Visio document")
    List1.ListIndex = List1.ListCount - 1
    GetIndex
    
    outputFile.Close
  
    List1.AddItem ("File  " + outputFilename + " created")
    List1.ListIndex = List1.ListCount - 1
     
EXIT_:

End Sub


Private Sub Command1_Click()
    On Error Resume Next
    Set appVisio = GetObject(, "visio.application")
    If appVisio Is Nothing Then
       Set appVisio = CreateObject("visio.application")
    End If
End Sub




Private Sub Command2_Click()
    On Error Resume Next
    ScanCurrentDocument
End Sub



Private Sub Command3_Click()
    Dim cmd As String
    Dim txtline As String
    Dim fin As Integer
    Dim oShell As Object
    cmd = "python data2py.py ./data.txt ./structure.txt " & Text1.Text
    List1.AddItem ("Running command " & cmd)
    List1.ListIndex = List1.ListCount - 1
    Set oShell = CreateObject("Wscript.Shell")
    oShell.Run "%COMSPEC% /c " & cmd & " > generate.txt", 0, True
    fin = FreeFile
    If Dir("generate.txt") <> "" Then
        Open "generate.txt" For Input As #fin
        Do While Not EOF(fin)
            Line Input #fin, txtline$
            List1.AddItem (txtline$)
            List1.ListIndex = List1.ListCount - 1
        Loop
        Close #fin
    End If
End Sub



Private Sub Command4_Click()
    Dim cmd As String
    Dim txtline As String
    Dim fin As Integer
    Dim oShell As Object
    cmd = "python merge.py ./structure.txt " & Text1.Text & " " & Combo1.Text & " " & Check1.Value & " " & Check2.Value & " " & Check3.Value
    List1.AddItem ("Running command " & cmd)
    List1.ListIndex = List1.ListCount - 1
    Set oShell = CreateObject("Wscript.Shell")
    oShell.Run "%COMSPEC% /c " & cmd & " > merge.txt", 0, True
    fin = FreeFile
    If Dir("merge.txt") <> "" Then
        Open "merge.txt" For Input As #fin
        Do While Not EOF(fin)
            Line Input #fin, txtline$
            List1.AddItem (txtline$)
            List1.ListIndex = List1.ListCount - 1
        Loop
        Close #fin
    End If
End Sub



Private Sub Command5_Click()
    On Error Resume Next
    ScanCurrentPage
End Sub


Private Sub Command6_Click()
    Combo1.AddItem (Combo1.Text)
End Sub

Private Sub Command7_Click()
    Dim oShell As Object
    Dim cmd As String
    cmd = "del " & Replace(Text1.Text, "/", "\\") & "\\*.py "
    List1.AddItem ("Running command " & cmd)
    List1.ListIndex = List1.ListCount - 1
    Set oShell = CreateObject("Wscript.Shell")
    oShell.Run "%COMSPEC% /c " & cmd, 0, True
End Sub

Private Sub Command8_Click()
    On Error Resume Next
    BuildIndexWholeDocument
End Sub



Private Sub Form_Load()
    Set FSO = CreateObject("Scripting.FileSystemObject")
    Dim i As Integer
    Dim line, txt As String
    Dim lines() As String
    If FSO.FileExists("visio2python.ini") Then
        Set ts = FSO.opentextfile("visio2python.ini")
        txt = ts.ReadAll
        ts.Close
        lines = Split(txt, vbNewLine)
        For Each line In lines
            i = InStr(1, line, "generated")
            If i = 1 Then
                Text1.Text = Right(line, Len(line) - Len("generated") - 1)
            End If
            i = InStr(1, line, "existed")
            If i = 1 Then
                Combo1.AddItem (Right(line, Len(line) - Len("existed") - 1))
                Combo1.Text = Right(line, Len(line) - Len("existed") - 1)
            End If
        Next line
        List1.AddItem ("Load path locations from visio2python.ini")
        List1.ListIndex = List1.ListCount - 1
        ' List1.Refresh
    Else
        Text1.Text = "./generated"
        Combo1.AddItem ("./")
        Combo1.Text = "./"
    End If
    List1.AddItem ("Current folder: " & App.Path)
    List1.ListIndex = List1.ListCount - 1
    ChDrive App.Path
    ChDir App.Path
End Sub



Private Sub Form_Unload(Cancel As Integer)
    Dim i As Integer
    Set ts = FSO.CreateTextFile("visio2python.ini", True)
    ts.WriteLine "generated " & Text1.Text
    ' ts.WriteLine "existed " & Combo1.Text
    For i = 0 To Combo1.ListCount - 1
        ts.WriteLine "existed " & Combo1.List(i)
    Next i
    ts.Close
    Set ts = Nothing
    Set FSO = Nothing
    Set appVisio = Nothing
End Sub




Private Sub Command9_Click()
    On Error Resume Next

    List1.AddItem ("Looking for Microsoft Visio")
    List1.ListIndex = List1.ListCount - 1
    
    Set appVisio = GetObject(, "visio.application")
    If appVisio Is Nothing Then
        Set appVisio = CreateObject("visio.application")
        If appVisio Is Nothing Then
            List1.AddItem ("Error Opening Visio!")
            List1.ListIndex = List1.ListCount - 1
            ' List1.Refresh
            GoTo EXIT_
        End If
    End If
      
    Set docVisio = appVisio.ActiveDocument
    If docVisio Is Nothing Then
        List1.AddItem ("Please Open Microsoft Visio Document")
        List1.ListIndex = List1.ListCount - 1
        ' List1.Refresh
        GoTo EXIT_
    End If
    
    docVisio.PrintOut visPrintCurrentPage
    
EXIT_:

End Sub


Private Sub Command10_Click()
    On Error Resume Next

    List1.AddItem ("Looking for Microsoft Visio")
    List1.ListIndex = List1.ListCount - 1
    
    Set appVisio = GetObject(, "visio.application")
    If appVisio Is Nothing Then
        Set appVisio = CreateObject("visio.application")
        If appVisio Is Nothing Then
            List1.AddItem ("Error Opening Visio!")
            List1.ListIndex = List1.ListCount - 1
            ' List1.Refresh
            GoTo EXIT_
        End If
    End If
      
    Set docVisio = appVisio.ActiveDocument
    If docVisio Is Nothing Then
        List1.AddItem ("Please Open Microsoft Visio Document")
        List1.ListIndex = List1.ListCount - 1
        ' List1.Refresh
        GoTo EXIT_
    End If
    
    docVisio.PrintOut visPrintAll
    
EXIT_:

End Sub
