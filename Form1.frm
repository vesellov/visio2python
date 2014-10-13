VERSION 5.00
Begin VB.Form Form1 
   BackColor       =   &H80000001&
   BorderStyle     =   1  'Fixed Single
   Caption         =   "visio2python"
   ClientHeight    =   8505
   ClientLeft      =   45
   ClientTop       =   435
   ClientWidth     =   15255
   FillStyle       =   2  'Horizontal Line
   BeginProperty Font 
      Name            =   "Arial"
      Size            =   8.25
      Charset         =   0
      Weight          =   400
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   Icon            =   "Form1.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   8505
   ScaleWidth      =   15255
   Begin VB.ListBox List1 
      Appearance      =   0  'Flat
      BeginProperty Font 
         Name            =   "Courier New"
         Size            =   12
         Charset         =   204
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   5430
      Left            =   120
      TabIndex        =   10
      Top             =   3000
      Width           =   15015
   End
   Begin VB.Frame Frame4 
      Appearance      =   0  'Flat
      BackColor       =   &H80000001&
      Caption         =   "Step 3"
      BeginProperty Font 
         Name            =   "Arial"
         Size            =   9.75
         Charset         =   204
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H8000000E&
      Height          =   2895
      Left            =   10200
      TabIndex        =   13
      Top             =   0
      Width           =   4935
      Begin VB.CommandButton Command6 
         Appearance      =   0  'Flat
         BackColor       =   &H80000014&
         Caption         =   "Add"
         Height          =   340
         Left            =   4200
         Style           =   1  'Graphical
         TabIndex        =   16
         Top             =   1560
         Width           =   615
      End
      Begin VB.ComboBox Combo1 
         Height          =   330
         ItemData        =   "Form1.frx":33E2
         Left            =   120
         List            =   "Form1.frx":33E4
         TabIndex        =   15
         Text            =   "Combo1"
         Top             =   1560
         Width           =   3975
      End
      Begin VB.CheckBox Check3 
         Appearance      =   0  'Flat
         BackColor       =   &H80000001&
         Caption         =   "don't modify any files, jsut show difference"
         ForeColor       =   &H8000000E&
         Height          =   255
         Left            =   120
         TabIndex        =   9
         Top             =   2520
         Width           =   4215
      End
      Begin VB.CheckBox Check2 
         Appearance      =   0  'Flat
         BackColor       =   &H80000001&
         Caption         =   "remove generated files after merge with existing code"
         ForeColor       =   &H8000000E&
         Height          =   255
         Left            =   120
         TabIndex        =   8
         Top             =   2280
         Width           =   4215
      End
      Begin VB.CheckBox Check1 
         Appearance      =   0  'Flat
         BackColor       =   &H80000001&
         Caption         =   "update existing files only, don't create new files"
         ForeColor       =   &H8000000E&
         Height          =   255
         Left            =   120
         TabIndex        =   7
         Top             =   2040
         Value           =   1  'Checked
         Width           =   4095
      End
      Begin VB.CommandButton Command4 
         Appearance      =   0  'Flat
         BackColor       =   &H80000014&
         Caption         =   "Merge with existing files"
         BeginProperty Font 
            Name            =   "Tahoma"
            Size            =   12
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   855
         Left            =   120
         Style           =   1  'Graphical
         TabIndex        =   6
         Top             =   360
         Width           =   4695
      End
      Begin VB.Label Label1 
         Appearance      =   0  'Flat
         BackColor       =   &H80000001&
         Caption         =   "Existing python files location:"
         ForeColor       =   &H8000000E&
         Height          =   255
         Left            =   240
         TabIndex        =   0
         Top             =   1320
         Width           =   4095
      End
   End
   Begin VB.Frame Frame3 
      Appearance      =   0  'Flat
      BackColor       =   &H80000001&
      Caption         =   "Step 2"
      BeginProperty Font 
         Name            =   "Arial"
         Size            =   9.75
         Charset         =   204
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H8000000E&
      Height          =   2895
      Left            =   5160
      TabIndex        =   12
      Top             =   0
      Width           =   4935
      Begin VB.CommandButton Command8 
         Appearance      =   0  'Flat
         BackColor       =   &H80000014&
         Caption         =   "Build index file"
         BeginProperty Font 
            Name            =   "Tahoma"
            Size            =   12
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   735
         Left            =   120
         Style           =   1  'Graphical
         TabIndex        =   18
         Top             =   2040
         Width           =   2295
      End
      Begin VB.CommandButton Command7 
         Appearance      =   0  'Flat
         BackColor       =   &H80000014&
         Caption         =   "Remove all generated files"
         BeginProperty Font 
            Name            =   "Tahoma"
            Size            =   12
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   735
         Left            =   2520
         Style           =   1  'Graphical
         TabIndex        =   17
         Top             =   2040
         Width           =   2295
      End
      Begin VB.TextBox Text1 
         BeginProperty Font 
            Name            =   "Arial"
            Size            =   8.25
            Charset         =   204
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   285
         Left            =   120
         TabIndex        =   5
         Text            =   "Text1"
         Top             =   1560
         Width           =   4695
      End
      Begin VB.CommandButton Command3 
         Appearance      =   0  'Flat
         BackColor       =   &H80000014&
         Caption         =   "Generate Python Code"
         BeginProperty Font 
            Name            =   "Tahoma"
            Size            =   12
            Charset         =   204
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   855
         Left            =   120
         Style           =   1  'Graphical
         TabIndex        =   4
         Top             =   360
         Width           =   4695
      End
      Begin VB.Label Label2 
         Appearance      =   0  'Flat
         BackColor       =   &H80000001&
         Caption         =   "Location for generated files:"
         BeginProperty Font 
            Name            =   "Arial"
            Size            =   8.25
            Charset         =   204
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H8000000E&
         Height          =   255
         Left            =   120
         TabIndex        =   14
         Top             =   1320
         Width           =   4095
      End
   End
   Begin VB.Frame Frame2 
      Appearance      =   0  'Flat
      BackColor       =   &H80000001&
      Caption         =   "Step 1"
      BeginProperty Font 
         Name            =   "Arial"
         Size            =   9.75
         Charset         =   204
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H8000000E&
      Height          =   2895
      Left            =   120
      TabIndex        =   11
      Top             =   0
      Width           =   4935
      Begin VB.CommandButton Command5 
         Appearance      =   0  'Flat
         BackColor       =   &H80000014&
         Caption         =   "Scan current page only"
         BeginProperty Font 
            Name            =   "Tahoma"
            Size            =   12
            Charset         =   204
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   735
         Left            =   120
         MaskColor       =   &H00FFFFFF&
         Style           =   1  'Graphical
         TabIndex        =   3
         Top             =   2040
         Width           =   4695
      End
      Begin VB.CommandButton Command1 
         Appearance      =   0  'Flat
         BackColor       =   &H80000014&
         Caption         =   "Run Microsoft Visio"
         BeginProperty Font 
            Name            =   "Tahoma"
            Size            =   12
            Charset         =   204
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   735
         Left            =   120
         MaskColor       =   &H8000000E&
         Style           =   1  'Graphical
         TabIndex        =   1
         Top             =   360
         UseMaskColor    =   -1  'True
         Width           =   4695
      End
      Begin VB.CommandButton Command2 
         Appearance      =   0  'Flat
         BackColor       =   &H80000014&
         Caption         =   "Scan opened MS Visio document"
         BeginProperty Font 
            Name            =   "Tahoma"
            Size            =   12
            Charset         =   204
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   735
         Left            =   120
         MaskColor       =   &H00FFFFFF&
         Style           =   1  'Graphical
         TabIndex        =   2
         Top             =   1200
         Width           =   4695
      End
   End
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

