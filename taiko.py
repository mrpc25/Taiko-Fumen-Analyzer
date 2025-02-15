import math
import os
import matplotlib.pyplot as plt
import configparser

def WriteConfig(configpath,SECTION,KEY,value):  #https://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python3
    config = configparser.ConfigParser()
    config.read(configpath)
    config[SECTION][KEY] = value
    with open(configpath, 'w') as configfile:    # save
        config.write(configfile)

def ReadConfig(configpath,SECTION,KEY):
    config = configparser.ConfigParser()
    config.read(configpath, encoding="utf-8")
    return config[SECTION][KEY]


class TaikoFumen():
    def __init__(self, Path, codec):
        with open(Path + "", mode='r' ,encoding = codec) as f:
            words_raw = f.read()

        #按行將原始檔案做切割
        EveryRow = []
        TempRow = ""
        for char in words_raw:
            if(char!="\n"):
                TempRow = TempRow + char
            else:
                EveryRow.append(TempRow)
                TempRow = ""
        EveryRow.append(TempRow)

        self.words_raw = words_raw
        self.EveryRow = EveryRow

        Command_BPMCHANGE_storage = ""
        Command_SCROLL_storage = ""
        Command_MEASURE_storage = ""
        Command_DELAY_storage = ""
        Command_BARLINE_storage = ""
        Command_GOGO_storage = ""

        new_EveryRow = []
        BranchEncounter = False

        def IsPhraseShowUpBeforeComma(phrase, rowindex):
          while("," not in EveryRow[rowindex]):
            #print(EveryRow[rowindex], phrase in EveryRow[rowindex])
            if(phrase in EveryRow[rowindex]): return True
            rowindex = rowindex + 1
          return False

        for x in range(len(EveryRow)):
          row = EveryRow[x]

          if "#BPMCHANGE" in row: Command_BPMCHANGE_storage = row
          if "#SCROLL" in row: Command_SCROLL_storage = row
          if "#MEASURE" in row: Command_MEASURE_storage = row
          if "#DELAY" in row: Command_DELAY_storage = row
          if "#BARLUNE" in row: Command_BARLINE_storage = row
          if "#GOGO" in row: Command_GOGO_storage = row

          if "#BRANCHSTART" in row:
            BranchEncounter = True
            Command_BPMCHANGE_BeforeBranch = Command_BPMCHANGE_storage
            Command_SCROLL_BeforeBranch = Command_SCROLL_storage
            Command_MEASURE_BeforeBranch = Command_MEASURE_storage
            Command_DELAY_BeforeBranch = Command_DELAY_storage
            Command_BARLINE_BeforeBranch = Command_BARLINE_storage
            Command_GOGO_BeforeBranch = Command_GOGO_storage
          
          new_EveryRow.append(row)
          if BranchEncounter:
            if ("#N" in row) or ( ("#E" in row) and ("#END" not in row) ) or ( ("#M" in row) and ("#MEASURE" not in row) ):
              if ( Command_BPMCHANGE_BeforeBranch!="" ) and ( not IsPhraseShowUpBeforeComma("#BPMCHANGE", x) ): new_EveryRow.append(Command_BPMCHANGE_BeforeBranch)
              if ( Command_SCROLL_BeforeBranch!="" ) and ( not IsPhraseShowUpBeforeComma("#SCROLL", x) ): new_EveryRow.append(Command_SCROLL_BeforeBranch)
              if ( Command_MEASURE_BeforeBranch!="" ) and ( not IsPhraseShowUpBeforeComma("#MEASURE", x) ): new_EveryRow.append(Command_MEASURE_BeforeBranch)
              if ( Command_DELAY_BeforeBranch!="" ) and  ( not IsPhraseShowUpBeforeComma("#DELAY", x) ): new_EveryRow.append(Command_DELAY_BeforeBranch)
              if ( Command_BARLINE_BeforeBranch!="" ) and not ( IsPhraseShowUpBeforeComma("#BARLUNE", x) ): new_EveryRow.append(Command_BARLINE_BeforeBranch)
              if ( Command_GOGO_BeforeBranch!="" ) and ( not IsPhraseShowUpBeforeComma("#GOGO", x) ): new_EveryRow.append(Command_GOGO_BeforeBranch)
              pass

          if "#END" in row:
          # if "#BRANCHEND" in row:
            Command_BPMCHANGE_storage = ""
            Command_SCROLL_storage = ""
            Command_MEASURE_storage = ""
            Command_DELAY_storage = ""
            Command_BARLINE_storage = ""
            Command_GOGO_storage = ""
            BranchEncounter = False


        EveryRow = new_EveryRow
        self.EveryRow = EveryRow

        #先尋找所有難度以及星級
        Song_Difficulty = self.FindPhraseInRow("COURSE:")
        Song_level = self.FindPhraseInRow("LEVEL:")

        Song_Begin = self.FindPhraseInRow("#START")
        Song_Endin = self.FindPhraseInRow("#END")

        assert len(Song_Begin)==len(Song_Endin), \
          "The amount of \"#START(P1/2)\' and \"#END\" command is not equal, you might need to check if some necessary command was lost."
            
        self.Song_Begin = Song_Begin
        self.Song_Endin = Song_Endin

        self.FumanClassfication = []
        self.BasicInfoOverViewDict = []           #20240622 更新
        self.BasicInfoOverViewDictWithIndex = []  #20240622 更新

        #20240909 更新: 若同檔案超過一個譜面，則除了位於最上面的譜面以外，並不一定需要填進所有資訊，可以以預設資訊或先前資訊替代。
        _last_record_difficulty = "N/A"
        _last_record_side = "-"
        _last_record_level = "?"
        _last_record_style = ""

        #20240914 更新: 改動偵測譜面的方式，不再先區分是否含有雙人譜面。
        for i in range(len(Song_Begin)):
            end, start = (Song_Endin[i-1]+1, Song_Begin[i]) if (i!=0) else (0, Song_Begin[0])

            difficulty = self.OffsetThingsValue("COURSE:", [end, start])
            level = self.OffsetThingsValue("LEVEL:", [end, start])
            style = self.OffsetThingsValue("STYLE:", [end, start])
            directness = self.OffsetThingsValue("SIDE:", [end, start])
            StringOfSTART = self.OffsetThingsValue("#START", [end, start])
            hbscroll = self.FindPhraseInRow("#HBSCROLL", [end, start])
            bmscroll = self.FindPhraseInRow("#BMSCROLL", [end, start])

            difficulty = difficulty.replace(" ", "")
            level = level.replace(" ", "")
            style = style.replace(" ", "")
            directness = directness.replace(" ", "")
            dualstatestr = ""
            for x in StringOfSTART: #把偵測到的文字裡，只留下P/1/2三種（因為只有#START/#START P1/#START P2三種可能）
                if(x=="P" or x=="1" or x=="2"): dualstatestr = dualstatestr + x

            #20250208 更新: 檢測HBS/BMS
            if(len(hbscroll)+len(bmscroll)>1): raise Exception(f"Multiple #HBSCROLL or #BMSCROLL command.")
            HBSCROLL = len(hbscroll)==1
            BMSCROLL = len(bmscroll)==1

            #20240909 更新:
            still_in_same_course = False
            match difficulty.lower():
                case "4"|"edit"  : difficulty = "Edit"
                case "3"|"oni"   : difficulty = "Oni"
                case "2"|"hard"  : difficulty = "Hard"
                case "1"|"normal": difficulty = "Normal"
                case "0"|"easy"  : difficulty = "Easy"
                case "": 
                  difficulty = _last_record_difficulty
                  still_in_same_course = True
                case _: raise Exception(f"difficulty not existed. (Input: \"{difficulty}\")")
            _last_record_difficulty = difficulty

            if level=="" : level = _last_record_level
            _last_record_level = level
                
            #20240622 更新:
            match directness.lower():
                case "1"|"normal": side = "EXT"
                case "2"|"ex": side = "INT"
                case "3": side = "-"
                case "": side = _last_record_side
                case _: raise Exception(f"Not a available side symbol, expect 1/2/3/None, (Input: \"{directness}\")")
            _last_record_side = side

            #20240914 更新:
            match dualstatestr:
               case "P1": dual = "P1"
               case "P2": dual = "P2"
               case "": dual = "-"
               case _: raise Exception(f"Invalid input for \"dualstatestr\". (input: {dualstatestr})")
            if style=="" and still_in_same_course: style = _last_record_style
            _last_record_style = style

            style_declaration = style.lower()=="double" or style=="2"
            extracted_dual_sign = dual=="P1" or dual=="P2"
            if (not style_declaration) and extracted_dual_sign : 
               raise Exception("Find that \"#START P1/2\" is written in file, but \"STYLE:\" section doesn't declare it's as a fumen for double player.")
            if style_declaration and (not extracted_dual_sign) :
               raise Exception("Find that double player mode is mentioned in \"STYLE:\" section, but \"#START P1/2\" is not written.")
            
            self.FumanClassfication.append([i, difficulty, dual, side, level])

            #20240622 更新:
            fumen_dict = {'difficulty':difficulty, 'dual':dual, 'side':side, 'level':level, 'operation':(HBSCROLL, BMSCROLL)}
            self.BasicInfoOverViewDictWithIndex.append([i, fumen_dict])
            self.BasicInfoOverViewDict.append(fumen_dict)
        
        #20240914 更新: "IsAnyDual"不再作為必要的判斷過程後，轉而使用分類後的譜面資訊來判斷
        IsAnyDual = False
        for fumrn in self.BasicInfoOverViewDict:
           if(fumrn['dual']!="-"): 
              IsAnyDual = True
              break

        self.Song_Difficulty = Song_Difficulty
        self.Song_level = Song_level
        self.IsAnyDual = IsAnyDual

    #定義在指定的行內（範圍），是否有出現過特定文字，並輸出所有含有該特定文字的所在行數，形式是List
    #out of index problem is caused by List Default Arguments, solve by 
    #https://www.pullrequest.com/blog/python-pitfalls-the-perils-of-using-lists-and-dicts-as-default-arguments/
    def FindPhraseInRow(self, Phrase, Coverage=None):
        if(Coverage is None):
            Coverage = [0, len(self.EveryRow)]
        Order = []
        for i in range(Coverage[0],Coverage[1]):
            #20240909更新
            reference = self.EveryRow[i].find(Phrase)
            annotation = self.EveryRow[i].find("//")
            reference_exist = reference!=-1                           #確認目標的字眼到底在不在該行內
            annotation_exist = annotation!=-1                         #確認該行有沒有註解符號
            if (not annotation_exist) and reference_exist: Order.append(i)
            if annotation_exist and reference_exist and (reference < annotation): Order.append(i)
        return Order
    
    def FindPhraseInRowRev(self, Phrase, Coverage=None):
        if(Coverage is None):
            Coverage = [0, len(self.EveryRow)]
        Order = []
        for i in range(Coverage[0],Coverage[1]):
            if(self.EveryRow[i].rfind(Phrase)!=-1):
                Order.append(i)
        return Order
    
    #尋找特定字詞所在地，在那個字詞之後出現的字詞，並去除在註解符號"//"後的部分
    def OffsetThingsValue(self,Phrase,Range):
        PhraseInRegion = self.FindPhraseInRow(Phrase,Range)
        output = ""
        if(len(PhraseInRegion)>0):
            Observed = self.EveryRow[PhraseInRegion[0]]
            Anno = Observed.find("//")
            lebr = Observed.find("(")
            if(Anno == -1 and lebr == -1):
                EndLocation = len(Observed)
            elif(Anno == -1):
                EndLocation = lebr
            elif(lebr == -1):
                EndLocation = Anno
            else:
                if(lebr<Anno):
                    EndLocation = lebr
                else:
                    EndLocation = Anno

            for i in range(Observed.find(Phrase)+len(Phrase),EndLocation):
                output = output + Observed[i]
        return output
    
    #尋找特定字詞所在地，在那個字詞之後出現的字詞，並去除在註解符號"//"後的部分（"("不受影響）。
    def OffsetThingsValue_PareIgnored(self,Phrase,Range):
      PhraseInRegion = self.FindPhraseInRow(Phrase,Range)
      output = ""
      if(len(PhraseInRegion)==0): return output
      Observed = self.EveryRow[PhraseInRegion[0]]
      Anno = Observed.find("//")
      EndLocation = len(Observed) if (Anno == -1) else Anno
      for i in range(Observed.find(Phrase)+len(Phrase),EndLocation): output = output + Observed[i]
      return output
    
    def abc(self):
        print("blablablaJustTesting")

class TaikoFumenInner(TaikoFumen):
    def __init__(self, Path, codec, UserChosenFumen):

        super().__init__(Path, codec)
        EveryBar = []          #每個小節的內容
        EveryBarRowLocation = []    #每個小節所在的行數(位置)
        CurrentMeasure = ""         #每次迴圈內暫存的小節內容
        CurrentMeasureRowLocation = []   #每次迴圈內暫存的小節位置

        if(UserChosenFumen>=0):
          if(UserChosenFumen==0):
            ChosenReady = 0
          else:
            ChosenReady = self.Song_Endin[UserChosenFumen-1]
          ChosenBegin = self.Song_Begin[UserChosenFumen]
          ChosenEndin = self.Song_Endin[UserChosenFumen]

        self.ChosenBegin = ChosenBegin
        self.ChosenEndin = ChosenEndin
        self.ChosenReady = ChosenReady

        for i in range(ChosenBegin+1,ChosenEndin):

            #檢查該小節是否有註解用的"//"符號，並記錄位置
            Annotation = self.EveryRow[i].find("//")

            #檢查該小節是否有譜面功能用的"#"符號，並記錄位置
            if(Annotation==-1):
                FunctionUsage = self.EveryRow[i].find("#")
            else:
                FunctionUsage = self.EveryRow[i].find("#", 0, Annotation)

            #判斷是否有使用函式"#"
            if(FunctionUsage==-1):
                for j in range(len(self.EveryRow[i])):
                    if(self.EveryRow[i][j]!=","):

                        #確認這一行文字中有沒有註解用的"//"
                        if(Annotation==-1):
                          #逐一檢視小節當中的字元，是數字就紀錄
                          if(str.isnumeric(self.EveryRow[i][j])):
                                #紀錄實際的字元
                                CurrentMeasure = CurrentMeasure + self.EveryRow[i][j]

                                #記錄這個字源所在的行
                                CurrentMeasureRowLocation.append(i)
                        else:
                          #逐一檢視小節當中的字元，是數字且是註解記號以前的文字就紀錄
                          if(str.isnumeric(self.EveryRow[i][j]) and j<Annotation):
                                #紀錄實際的字元
                                CurrentMeasure = CurrentMeasure + self.EveryRow[i][j]

                                #記錄這個字源所在的行
                                CurrentMeasureRowLocation.append(i)
                    else:
                        CurrentMeasure = CurrentMeasure + self.EveryRow[i][j]
                        CurrentMeasureRowLocation.append(i)

                        #小節結束時，暫時紀錄的str輸出到另外一個list，再讓暫時紀錄的str清空。
                        EveryBar.append(CurrentMeasure)
                        CurrentMeasure = ""

                        #小節結束時，暫時紀錄的str行位置輸出到另外一個list，再讓暫時紀錄清空。
                        EveryBarRowLocation.append(CurrentMeasureRowLocation)
                        CurrentMeasureRowLocation = []

        EveryBarWithoutComma = []
        for Bar in EveryBar:
          BarWithoutComma = ""
          for i in range(len(Bar)-1):
            BarWithoutComma = BarWithoutComma + Bar[i]
          EveryBarWithoutComma.append(BarWithoutComma)
        
        self.EveryBar = EveryBar

        #每個小節開始時在檔案內所位於的行數
        BarBeginLoaction = []
        temp = EveryBarRowLocation[0][0]
        BarBeginLoaction.append(temp)
        for bar in EveryBarRowLocation:
            for notesLocation in bar:
                if(notesLocation != temp):
                    temp = notesLocation
                    BarBeginLoaction.append(temp)

        temp = None
        BarLocation = []
        for bar in EveryBarRowLocation:
            #針對同一個小節，找出所有notes出現過的行數。
            NotesInBarLocation = []
            for notesLocation in bar:
                #紀錄同一個小節內的每個notes，是否有出現過不同的行數，有的話就做紀錄
                if(notesLocation != temp):
                    temp = notesLocation
                    NotesInBarLocation.append(temp)
            #記錄所有小節的結果
            BarLocation.append(NotesInBarLocation)
            
        self.BarBeginLoaction = BarBeginLoaction
        self.EveryBarRowLocation = EveryBarRowLocation

        #將譜面的所有資訊座儲存
        ScrollSet = self.Find_Scroll_Of_EachNotesInLoaction()
        BPMValueSet = self.Find_BPM_Of_EachNotesInLoaction()
        BeatsToMeasureSet = self.Find_BeatsToMeasure_Of_EachNotesInLoaction()
        SeenVelSet = self.Find_SeenVelocity_Of_EachNotesInLoaction()
        DelaySet = self.Find_Delay_Of_EachNotesInLoaction()
        BarlineSet = self.Find_Barline_Of_EachNotesInLoaction()
        GOGOSet = self.Find_GOGO_Of_EachNotesInLoaction()

        BeatsToMeasureSetPure = self.DeleteCommmaInfo(self.Find_BeatsToMeasure_Of_EachNotesInLoaction())
        BPMValueSetPure = self.DeleteCommmaInfo(self.Find_BPM_Of_EachNotesInLoaction())
        ScrollSetPure = self.DeleteCommmaInfo(self.Find_Scroll_Of_EachNotesInLoaction())
        SeenVelSetPure = self.DeleteCommmaInfo(self.Find_SeenVelocity_Of_EachNotesInLoaction())

        HasBrachProcessYet = False
        BranchStateSet = self.Find_Branch_Of_EachNotesInLoaction()

        self.ScrollSet = ScrollSet
        self.BPMValueSet = BPMValueSet
        self.BeatsToMeasureSet = BeatsToMeasureSet
        self.SeenVelSet = SeenVelSet
        self.DelaySet = DelaySet
        self.BarlineSet = BarlineSet
        self.GOGOSet = GOGOSet

        self.BeatsToMeasureSetPure = BeatsToMeasureSetPure
        self.BPMValueSetPure = BPMValueSetPure
        self.ScrollSetPure = ScrollSetPure
        self.SeenVelSetPure = SeenVelSetPure

        self.HasBrachProcessYet = HasBrachProcessYet
        self.BranchStateSet = BranchStateSet

        # @title
        if(len(self.FindPhraseInRow("#BRANCHSTART",[ChosenBegin, ChosenEndin]))==0):
          self.IsBranchExist = False
        else:
          self.IsBranchExist = True

    def Find_Scroll_Of_EachNotesInLoaction(self):
      LastLocation = self.ChosenBegin
      MeasureInfo = []
      TempContent = "1" #預設值1
      for MeasureLocationList in self.EveryBarRowLocation:
        NotesInfo = []
        for NotesLocation in MeasureLocationList:
          Content = self.OffsetThingsValue("#SCROLL",[LastLocation,NotesLocation])
          if(Content!="" and not str.isspace(Content)):
            TempContent = ""
            for char in Content:
              if(str.isnumeric(char) or char=="+" or char=="-" or char=="." or char=="i"):
                if(char != "i"):
                    TempContent = TempContent + char
                else:
                    TempContent = TempContent + "j"
            #TempContent = complex(TempContent) #複數譜面會有虛數
          TempContent = complex(TempContent) #同BPM作法

          NotesInfo.append(TempContent)
          LastLocation = NotesLocation
        MeasureInfo.append(NotesInfo)
      return MeasureInfo

    def Find_BPM_Of_EachNotesInLoaction(self):
      LastLocation = self.ChosenBegin
      MeasureInfo = []
      TempContent = self.OffsetThingsValue("BPM:",[self.ChosenReady,self.ChosenBegin]) #預設使用譜面開始前設定的BPM
      if(TempContent==""):
        TempContent = self.OffsetThingsValue("BPM:",[0, self.Song_Begin[0]]) #沒有該譜面自設定的BPM，則沿用譜面檔案一開始能找到的數值

      for MeasureLocationList in self.EveryBarRowLocation:
        NotesInfo = []
        for NotesLocation in MeasureLocationList:
          Content = self.OffsetThingsValue("#BPMCHANGE",[LastLocation,NotesLocation])
          if(Content!="" and not str.isspace(Content)):
            TempContent = ""
            for char in Content:
              if(str.isnumeric(char) or char=="+" or char=="-" or char=="."):
                  TempContent = TempContent + char
            #TempContent = float(TempContent)  #原先這行在這，移下去看有沒有問題
          TempContent = float(TempContent) #???

          NotesInfo.append(TempContent)
          LastLocation = NotesLocation
        MeasureInfo.append(NotesInfo)
      return MeasureInfo
    
    def Find_SeenVelocity_Of_EachNotesInLoaction(self):
      MeasureInfo = []
      bpmSet = self.Find_BPM_Of_EachNotesInLoaction()
      scrSet = self.Find_Scroll_Of_EachNotesInLoaction()

      for bpmBar, scrBar in zip(bpmSet, scrSet):
        NotesInfo = []
        for bpm, scr in zip(bpmBar, scrBar):
          NotesInfo.append(bpm * scr)
        MeasureInfo.append(NotesInfo)

      return MeasureInfo
    
    def Find_BeatsToMeasure_Of_EachNotesInLoaction(self):
      LastLocation = self.ChosenBegin
      MeasureInfo = []
      TempContent = [4, 4] #預設4/4拍
      for MeasureLocationList in self.EveryBarRowLocation:
        NotesInfo = []
        for NotesLocation in MeasureLocationList:
          Content = self.OffsetThingsValue("#MEASURE",[LastLocation,NotesLocation])
          if(Content!="" and not str.isspace(Content)):
            TempContent = ""
            for char in Content:
              if(str.isnumeric(char) or char=="+" or char=="-" or char=="/" or char=="-"):
                  TempContent = TempContent + char
            TempContent = TempContent.split("/")
            TempContent = [int(TempContent[0]), int(TempContent[1])]

          NotesInfo.append(TempContent)
          LastLocation = NotesLocation
        MeasureInfo.append(NotesInfo)
      return MeasureInfo
    
    def Find_Delay_Of_EachNotesInLoaction(self):
      LastLocation = self.ChosenBegin
      MeasureInfo = []
      for MeasureLocationList in self.EveryBarRowLocation:
        NotesInfo = []
        for NotesLocation in MeasureLocationList:
          Content = self.OffsetThingsValue("#DELAY",[LastLocation,NotesLocation])
          if(Content!="" and not str.isspace(Content)):
            TempContent = ""
            for char in Content:
              if(str.isnumeric(char) or char=="+" or char=="-" or char=="."):
                  TempContent = TempContent + char
            TempContent = float(TempContent)
          else:
            TempContent = 0.0
          NotesInfo.append(TempContent)
          LastLocation = NotesLocation
        MeasureInfo.append(NotesInfo)
      return MeasureInfo
    
    def Find_Barline_Of_EachNotesInLoaction(self):
      LastLocation = self.ChosenBegin
      MeasureInfo = []
      TempContent = True
      for MeasureLocationList in self.EveryBarRowLocation:
        NotesInfo = []
        for NotesLocation in MeasureLocationList:
          Content = self.OffsetThingsValue("#BARLINE",[LastLocation,NotesLocation])
          if(Content!="" and not str.isspace(Content)):
            TempContent = ""
            for char in Content:
              if(char!="" and char!=" " and char!="　"):
                  TempContent = TempContent + char
            if(TempContent=="ON"):
              TempContent = True
            else:
              TempContent = False

          NotesInfo.append(TempContent)
          LastLocation = NotesLocation
        MeasureInfo.append(NotesInfo)
      return MeasureInfo
    
    def Find_GOGO_Of_EachNotesInLoaction(self):
      LastLocation = self.ChosenBegin
      MeasureInfo = []
      TempContent = False
      for MeasureLocationList in self.EveryBarRowLocation:
        NotesInfo = []
        for NotesLocation in MeasureLocationList:
          Content = self.OffsetThingsValue("#GOGO",[LastLocation,NotesLocation])
          if(Content!="" and not str.isspace(Content)):
            TempContent = ""
            for char in Content:
              if(char!="" and char!=" " and char!="　"):
                  TempContent = TempContent + char
            if(TempContent=="START"):
              TempContent = True
            else:
              TempContent = False

          NotesInfo.append(TempContent)
          LastLocation = NotesLocation
        MeasureInfo.append(NotesInfo)
      return MeasureInfo
    
    #處理分歧問題
    def Find_Branch_Of_EachNotesInLoaction(self):
      LastLocation = self.ChosenBegin
      MeasureInfo = []

      TempIsBranched = False
      BranchCondition = None
      BranchSwitchSide = None
      if(len(self.FindPhraseInRow("#SECTION",[self.ChosenBegin, self.ChosenEndin]))!=0):
        ConditionResetTimes = 0
      else:
        ConditionResetTimes = None

      for MeasureLocationList in self.EveryBarRowLocation:
        NotesInfo = []
        for NotesLocation in MeasureLocationList:
          if(len(self.FindPhraseInRow("#BRANCHSTART",[LastLocation,NotesLocation]))!=0):
            TempIsBranched = True
            BranchCondition = self.OffsetThingsValue("#BRANCHSTART",[LastLocation,NotesLocation])
            BranchCondition = BranchCondition.split(",")
            BranchCondition[1]=float(BranchCondition[1])
            BranchCondition[2]=float(BranchCondition[2])
          if(TempIsBranched):
            if(len(self.FindPhraseInRow("#N",[LastLocation,NotesLocation]))!=0):
              BranchSwitchSide = 0
            elif(( len(self.FindPhraseInRow("#E",[LastLocation,NotesLocation])) - len(self.FindPhraseInRow("#END",[LastLocation,NotesLocation])) ) != 0):
              BranchSwitchSide = 1
            elif(( len(self.FindPhraseInRow("#M",[LastLocation,NotesLocation])) - len(self.FindPhraseInRow("#MEASURE",[LastLocation,NotesLocation])) ) != 0):
              BranchSwitchSide = 2
          else:
            pass

          if(len(self.FindPhraseInRow("#BRANCHEND",[LastLocation,NotesLocation]))!=0):
            TempIsBranched = False
            BranchCondition = None
            BranchSwitchSide = None
          else:
            pass

          if(len(self.FindPhraseInRow("#SECTION",[LastLocation,NotesLocation]))!=0):
            ConditionResetTimes = ConditionResetTimes + 1


          #TempContent形式: [是否在分歧狀態， 這個分岐的條件， 有分歧的話目前是在哪一個譜面, 條件重設次數]
          NotesInfo.append([TempIsBranched, BranchCondition, BranchSwitchSide, ConditionResetTimes])
          LastLocation = NotesLocation
        MeasureInfo.append(NotesInfo)
      return MeasureInfo
    
    def FindWhereCommandShowUp(self, command):
      command_list = self.FindPhraseInRow(command,[self.ChosenBegin, self.ChosenEndin])
      command_line_check = []

      for commad_location_row in command_list:
        temp_last = -1
        for i in range(len(self.EveryBarRowLocation)):
          MeasureLocationList = self.EveryBarRowLocation[i]
          for j in range(len(MeasureLocationList)):
            NotesLocation = MeasureLocationList[j]
            if(temp_last < commad_location_row < NotesLocation):
              command_line_check.append([i,j])
              temp_last = commad_location_row
              break
          if(temp_last==commad_location_row):
            break

      return command_line_check
    
    def FindEveryActualNotesLocation(self):
      locationinfo = []
      for i in range(len(self.EveryBar)):
        for j in range(len(self.EveryBar[i])):
          notes = self.EveryBar[i][j]
          if(notes=="1" or notes=="2" or notes=="3" or notes=="4"):
            locationinfo.append([i,j])
      return locationinfo

    def FindEveryKindOfNotesLocation(self):
      locationinfo = []
      for i in range(len(self.EveryBar)):
        for j in range(len(self.EveryBar[i])):
          notes = self.EveryBar[i][j]
          if(notes!="0" and str.isnumeric(notes)):
            locationinfo.append([i,j])
      return locationinfo

    def FindEveryPassedNotesLocation(self):
      locationinfo = []
      for i in range(len(self.EveryBar)):
        for j in range(len(self.EveryBar[i])):
          notes = self.EveryBar[i][j]
          if(notes!=","):
            locationinfo.append([i,j])
      return locationinfo
    
    def DeleteCommmaInfo(self, KindOfEveryBar):
      KindOfEveryBarWithoutComma = []
      for Bar in KindOfEveryBar:
        try:
          KindOfBarWithoutComma = ""
          for i in range(len(Bar)-1):
            KindOfBarWithoutComma = KindOfBarWithoutComma + Bar[i]
        except:
          KindOfBarWithoutComma = []
          for i in range(len(Bar)-1):
            KindOfBarWithoutComma.append(Bar[i])

        KindOfEveryBarWithoutComma.append(KindOfBarWithoutComma)
      return KindOfEveryBarWithoutComma
    
class TaikoFumenBranched(TaikoFumenInner):
    def __init__(self, Path, codec, UserChosenFumen, UserChosenBranchDirection):
        super().__init__(Path, codec, UserChosenFumen)
        if(not self.HasBrachProcessYet):

            OG_BranchStateSet = self.BranchStateSet

            OG_EveryBarRowLocation = self.EveryBarRowLocation
            OG_EveryBar = self.EveryBar

            OG_ScrollSet = self.ScrollSet
            OG_BPMValueSet = self.BPMValueSet
            OG_BeatsToMeasureSet = self.BeatsToMeasureSet
            OG_SeenVelSet = self.SeenVelSet
            OG_DelaySet = self.DelaySet
            OG_BarlineSet = self.BarlineSet
            OG_GOGOSet = self.GOGOSet

            HasBrachProcessYet = True

        EveryBarRowLocation = []
        EveryBar = []

        ScrollSet = []
        BPMValueSet = []
        BeatsToMeasureSet = []
        SeenVelSet = []
        DelaySet = []
        BarlineSet = []
        GOGOSet = []

        BranchStateSet = []       #2024.03.22 新增

        for i in range(len(OG_EveryBar)):
            if(OG_BranchStateSet[i][0][2]==None or OG_BranchStateSet[i][0][2]==int(UserChosenBranchDirection)):
                EveryBarRowLocation.append(OG_EveryBarRowLocation[i])
                EveryBar.append(OG_EveryBar[i])

                ScrollSet.append(OG_ScrollSet[i])
                BPMValueSet.append(OG_BPMValueSet[i])
                BeatsToMeasureSet.append(OG_BeatsToMeasureSet[i])
                SeenVelSet.append(OG_SeenVelSet[i])
                DelaySet.append(OG_DelaySet[i])
                BarlineSet.append(OG_BarlineSet[i])
                GOGOSet.append(OG_GOGOSet[i])

                BranchStateSet.append(OG_BranchStateSet[i])

        self.EveryBarRowLocation = EveryBarRowLocation
        self.EveryBar = EveryBar

        self.ScrollSet = ScrollSet
        self.BPMValueSet = BPMValueSet
        self.BeatsToMeasureSet = BeatsToMeasureSet
        self.SeenVelSet = SeenVelSet
        self.DelaySet = DelaySet
        self.BarlineSet = BarlineSet
        self.GOGOSet = GOGOSet

        self.BranchStateSet = BranchStateSet

        TempContent = self.OffsetThingsValue("BPM:",[self.ChosenReady,self.ChosenBegin]) #預設使用譜面開始前設定的BPM
        if(TempContent==""):
            TempContent = self.OffsetThingsValue("BPM:",[0, self.Song_Begin[0]]) #沒有該譜面自設定的BPM，則沿用譜面檔案一開始能找到的數值
        TempContent = float(TempContent)
        self.TempContent = TempContent

        #譜面基本資訊
        TITLE = self.OffsetThingsValue_PareIgnored("TITLE:", [0, self.Song_Begin[0]])
        if(not self.IsAnyDual):
            COURSE = self.OffsetThingsValue("COURSE:", [self.ChosenReady, self.ChosenBegin])
            LevelStar = self.OffsetThingsValue("LEVEL:", [self.ChosenReady, self.ChosenBegin])
        else:
            COURSE = self.OffsetThingsValue("COURSE:", [self.Song_Difficulty[int(UserChosenFumen)], self.Song_Difficulty[int(UserChosenFumen)]+1])
            LevelStar = self.OffsetThingsValue("LEVEL:", [self.Song_level[int(UserChosenFumen)], self.Song_level[int(UserChosenFumen)]+1])
        COURSE = COURSE.replace(" ", "")

        match COURSE.lower():
          case "4"|"edit"   : COURSE = "Edit"
          case "3"|"oni"    : COURSE = "Oni"
          case "2"|"hard"   : COURSE = "Hard"
          case "1"|"normal" : COURSE = "Normal"
          case "0"|"easy"   : COURSE = "Easy"
          case "" : COURSE = "N/A"
          case _  : raise Exception("Course Is Invalid.")
           
        DUAL = None
        StringOfStartType = self.OffsetThingsValue("#START",[self.Song_Begin[UserChosenFumen],self.Song_Begin[UserChosenFumen]+1])
        dualstatestr = ""
        for Type in StringOfStartType:
            if(Type=="P" or Type=="1" or Type=="2"): dualstatestr = dualstatestr + Type

        #20250129 更新
        match dualstatestr:
          case "P1" : DUAL = "Player 1"
          case "P2" : DUAL = "Player 2"
          case ""   : pass
          case _    : raise Exception(f"Not a vaild player command. ({dualstatestr})")

        BRANCH = None
        match UserChosenBranchDirection:
          case 0: BRANCH = "普通譜面"
          case 1: BRANCH = "玄人譜面"
          case 2: BRANCH = "達人譜面"

        self.TITLE = TITLE
        self.COURSE = COURSE
        self.LevelStar = LevelStar
        self.DUAL = DUAL
        self.BRANCH = BRANCH


    def Get_NumberOfNotes(self):
      d = 0
      k = 0
      Bd = 0
      Bk = 0
      for bar in self.EveryBar:
        for notes in bar:
          if(notes=="1"):
            d = d + 1
          elif(notes=="2"):
            k = k + 1
          elif(notes=="3"):
            Bd = Bd + 1
          elif(notes=="4"):
            Bk = Bk + 1
      return d+k+Bd+Bk, d, k ,Bd, Bk

    def Get_NumberOfNotes_InRegion(self, x=[0, 0], y=None):
      EveryBar = self.EveryBar

      if(y==None):
         y = [len(EveryBar)-1, len(EveryBar[-1])-1]
      d = 0
      k = 0
      Bd = 0
      Bk = 0
      for i in range(x[0],y[0]+1):
        if(x[0]==y[0]):
            a = x[1]
            b = y[1]
        else:
            if(i==x[0]):
                  a = x[1]
                  b = len(EveryBar[i]) - 1 #小節資訊的最後一個是逗號，因此考慮實際譜面要-1，其他地方以此類推
            elif(i==y[0]):
                  a = 0
                  b = y[1]
            else:
                  a = 0
                  b = len(EveryBar[i]) - 1
        for j in range(a,b):
          # print(i,j)
          notes = EveryBar[i][j]
          if(notes=="1"):
            d = d + 1
          elif(notes=="2"):
            k = k + 1
          elif(notes=="3"):
            Bd = Bd + 1
          elif(notes=="4"):
            Bk = Bk + 1
      return d+k+Bd+Bk, d, k ,Bd, Bk
    
    def Get_RollInformation(self):
      RollLoaction = []

      IsDurningRoll = False
      RollType = None
      RollLocation = [None, None]

      EveryBarWithoutComma = self.DeleteCommmaInfo(self.EveryBar)


      for i in range(len(EveryBarWithoutComma)):
        for j in range(len(EveryBarWithoutComma[i])):

          Notes = EveryBarWithoutComma[i][j]
          if(not IsDurningRoll):
            if(Notes=="5" or Notes=="6" or Notes=="7" or Notes=="9"):
              RollType = int(Notes)
              RollLocation[0] = [i,j]
              IsDurningRoll = True
          else:
            if(Notes=="8" or Notes=="1" or Notes=="2" or Notes=="3" or Notes=="4"):
              RollLocation[1] = [i,j]
              IsDurningRoll = False

          if(RollType!=None and RollLocation[0]!=None and RollLocation[1]!=None):
            RollLoaction.append([RollType, RollLocation])
            RollType = None
            RollLocation = [None, None]

      return RollLoaction
    
    def Get_BalloonKickNeeded(self):
       BalloonsInString = self.OffsetThingsValue("BALLOON:",[self.ChosenReady, self.ChosenBegin]).split(",")
       Balloons = []
       for Balloon in BalloonsInString:
          if(str.isnumeric(Balloon)):
              Balloons.append(int(Balloon))
       return Balloons
    
    #2024/04/12 新增
    def Get_IfKickNeeded_And_Hits_ForEveryRolls(self):
      Rolls_info = self.Get_RollInformation()
      balloon_count = 0            #處理氣球或彩球的打擊數
      balloon_kick = self.Get_BalloonKickNeeded()
      Roll_KickState = []
      for Roll in Rolls_info:
          match Roll[0]:
              case 5|6:
                  Roll_KickState.append(None)
              case 7|9:
                  Roll_KickState.append(balloon_kick[balloon_count])
                  balloon_count = balloon_count + 1
      return Roll_KickState

    
    def Duration(self, x=[0, 0], y=None):
         EveryBar = self.EveryBar
         DelaySet = self.DelaySet
         BeatsToMeasureSet = self.BeatsToMeasureSet
         BPMValueSet = self.BPMValueSet


         if(y==None):
            y=[len(EveryBar)-1, len(EveryBar[-1])-1]
         OverallDuration = 0
         DELAYinProcess = 0
         ProcessDirectionElement = 1

         if(x[0]>y[0] or (x[0]==y[0] and x[1]>y[1])):
              Temp = [x, y]
              x = Temp[1]
              y = Temp[0]
              ProcessDirectionElement = -1
              del Temp

         #起頭點部分的DELAY不應該被記入
         OverallDuration = OverallDuration - DelaySet[x[0]][x[1]]
         DELAYinProcess = DELAYinProcess - DelaySet[x[0]][x[1]]

         for j in range(x[0],y[0]+1):
              if len(EveryBar[j])==1:
                   MeasureBeat, MeasureForm = BeatsToMeasureSet[j][0]

                   #可能與真正樂理上的算法有出入，這邊以太鼓次郎的判定作計算
                   OverallDuration = OverallDuration + 60 / BPMValueSet[j][0] * 4 * ( MeasureBeat / MeasureForm )
              else:
                   if(x[0]==y[0]):
                        a = x[1]
                        b = y[1]
                   else:
                        if(j==x[0]):
                             a = x[1]
                             b = len(EveryBar[j]) - 1 #小節資訊的最後一個是逗號，因此考慮實際譜面要-1，其他地方以此類推
                        elif(j==y[0]):
                             a = 0
                             b = y[1]
                        else:
                             a = 0
                             b = len(EveryBar[j]) - 1

                   for i in range(a,b):
                        MeasureBeat, MeasureForm = BeatsToMeasureSet[j][i]
                        OverallDuration = OverallDuration + DelaySet[j][i] + 60 / BPMValueSet[j][i] * 4 * ( MeasureBeat / MeasureForm ) / ( len(EveryBar[j]) - 1 )
                        DELAYinProcess = DELAYinProcess + DelaySet[j][i]

              #由於每個小節尾端(也就是逗號所在位置)也能夠加上指令，故須考慮
              if(x[0]!=y[0] and j!=y[0]):
                  OverallDuration = OverallDuration + DelaySet[j][-1]
                  DELAYinProcess = DELAYinProcess + DelaySet[j][-1]

         #最後點所屬的部份的DELAY應該被考慮
         OverallDuration = OverallDuration + DelaySet[y[0]][y[1]]
         DELAYinProcess = DELAYinProcess + DelaySet[y[0]][y[1]]

         return OverallDuration * ProcessDirectionElement, DELAYinProcess * ProcessDirectionElement
    
    #找出所有相鄰鼓點間，持續時間最短和最長的值
    def FindExtremePeriod(self):
        Noteslist = self.FindEveryActualNotesLocation()
        assert(len(Noteslist)>0), "This fumen doesn't have any notes."
        if(len(Noteslist)==1): return 0, 0
        initial = self.Duration(Noteslist[0], Noteslist[1])[0]
        if(len(Noteslist)==2): return initial, initial
        tempL, tempH = initial, initial
        for i in range(len(Noteslist)-2):
            Latest = self.Duration(Noteslist[i+1], Noteslist[i+2])[0]
            if(tempL > Latest): tempL = Latest
            if(tempH < Latest): tempH = Latest
        return tempL, tempH
    
    #計算密度
    #輸入為開始位置和結束位置，預設為第一個和最後音符位置
    def DensityOfRegion(self, x=None, y=None):
         if(x==None):
            x=self.FindEveryActualNotesLocation()[0]
         if(y==None):
            y=self.FindEveryActualNotesLocation()[-1]

         #Amount = Get_NumberOfNotes_InRegion(x,y)[0] - 1
         Amount = self.Get_NumberOfNotes_InRegion(x,y)[0]
         Length = self.Duration(x,y)[0]
         if(Length>0 and Amount>0):
              return Amount / Length
         else:
              return "沒有音符"
         
    #尋找一個中心點周遭特定時間長度的打點密度
    def DensityInSpreadRange(self, Center, t):
        i = 0
        j = 0
        k = 0
        Noteslist = self.FindEveryActualNotesLocation()
        while(Noteslist[i][0]<Center[0]):
            i = i + 1
        while(Noteslist[i][0]<=Center[0] and Noteslist[i][1]<Center[1]):
            i = i + 1

        time = t / 2
        if(self.Duration(Center,Noteslist[i])[0]<time):
            while(self.Duration(Center,Noteslist[i+j])[0]<time and (i+j)>=0):
                  j = j + 1
                  if(i+j>len(Noteslist)-1):
                      break

        if(self.Duration(Noteslist[i],Center)[0]<time):
            while(self.Duration(Noteslist[i-k],Center)[0]<time and (i-k)<=len(Noteslist)-1):
                  k = k + 1
                  if(i-k<0):
                      break

        if(i+j==0):
          Upperbound = Noteslist[0]
        else:
          Upperbound = Noteslist[i+j-1]

        if(i-k==len(Noteslist)-1):
          Lowerbound = Noteslist[len(Noteslist)-1]
        else:
          Lowerbound = Noteslist[i-k+1]

        return (self.Get_NumberOfNotes_InRegion(Lowerbound,Upperbound)[0]+1) / t
    
    #計算時間，並顯示固定的位數
    import math
    import sys
    sys.setrecursionlimit(3000)
    def chechforms(self, x):
      if(x>=10):
        x = str(x)
      elif(x>=0):
        x = "0" + str(x)
      return x

    def TimeDisplay(self, t):
      sec = math.floor( t % 60 )
      min = math.floor( ( t % 3600 ) / 60 )
      hr = math.floor( ( t % 86400 ) / 3600 )
      return str(self.chechforms(hr)) + ":" + str(self.chechforms(min)) + ":" + str(self.chechforms(sec))

    #尋找周遭秒數內，從頭到尾尋找的過程中所出現過的最大密度
    def DensityInSepecificTimeRegion(self, T):
      AllRelativeLocation = self.FindEveryActualNotesLocation()
      Noteslist = self.FindEveryActualNotesLocation()
      ALLnotes = len(AllRelativeLocation)
      Temp = self.DensityInSpreadRange(AllRelativeLocation[0],T)

      ProcessUnitTime = []
      ProcessTime = 0
      import time
      for i in range(len(Noteslist)):
          start = time.time()
          Compared = self.DensityInSpreadRange(Noteslist[i],T)
          if(Temp < Compared):
              Temp = Compared
          end = time.time()

          ProcessUnitTime.append(end - start)
          if(i+1<=100):
            ProcessTime = sum(ProcessUnitTime)
            Average = ProcessTime / (i+1)
          else:
            ProcessTime = 0
            for x in range(100):
              ProcessTime = ProcessTime + ProcessUnitTime[len(ProcessUnitTime)-1-x]
            Average = ProcessTime / 100

          EstimateTime = Average * (len(Noteslist)-(i+1))
          print(f"\rLatest Highest:{round(Temp,3)} notes/s\t/  {Noteslist[i]}\t/{round((i+1)/len(Noteslist)*100,2)}%\t\t/Estimate Time Left:\t{self.TimeDisplay(EstimateTime)}",end='')
      time.sleep(1.5)
      print(f"\r                                                                                                ")

      return Temp

    def DensityInSepecificTimeRegionBoth(self, T):
      AllRelativeLocation = self.FindEveryActualNotesLocation()
      Noteslist = self.FindEveryActualNotesLocation()
      ALLnotes = len(AllRelativeLocation)


      Temp = self.DensityInSpreadRange(AllRelativeLocation[0],T)
      TempL = Temp
      TempH = Temp

      ProcessUnitTime = []
      ProcessTime = 0
      import time
      for i in range(len(Noteslist)):
          start = time.time()
          Compared = self.DensityInSpreadRange(Noteslist[i],T)
          if(TempH < Compared):
              TempH = Compared
          if(TempL > Compared):
              TempL = Compared
          end = time.time()

          ProcessUnitTime.append(end - start)
          if(i+1<=100):
            ProcessTime = sum(ProcessUnitTime)
            Average = ProcessTime / (i+1)
          else:
            ProcessTime = 0
            for x in range(100):
              ProcessTime = ProcessTime + ProcessUnitTime[len(ProcessUnitTime)-1-x]
            Average = ProcessTime / 100

          EstimateTime = Average * (len(Noteslist)-(i+1))
          print(f"\rLatest\t:{round(TempH,3)}\t/{round(TempL,3)}\tnotes/s\t/  {Noteslist[i]}\t/{round((i+1)/len(Noteslist)*100,2)}%\t\t/Estimate Time Left:\t{self.TimeDisplay(EstimateTime)}",end='')
      time.sleep(1.5)
      print(f"\r                                                                                                ")

      return TempH, TempL
    
    #將所有譜面裡的鼓點時間點標出，再用時間範圍求值
    def FindExtremeDensityByTimeStrap(self, T):
      t = T / 2

      Location = self.FindEveryActualNotesLocation()
      RelativeTime = [0]
      total = 0
      for i in range(len(Location)-1):
        total = total + self.Duration(Location[i],Location[i+1])[0]
        RelativeTime.append(total)

      LatestLow = float("inf")
      LatestHigh = 0
      for i in range(len(RelativeTime)):
        if(RelativeTime[i] - t < 0 or RelativeTime[i] + t > RelativeTime[-1] ):
          pass
        else:
          j = 0
          while(RelativeTime[i+j]-RelativeTime[i]<t):
            j = j + 1
          #HighEnd = j - 1

          k = 0
          while(RelativeTime[i]-RelativeTime[i-k]<t):
            k = k + 1
          #LowEnd = k - 1

          #NumberOfNotesInsidePeriod = HighEnd + LowEnd + 1
          NumberOfNotesInsidePeriod = j + k - 1

          CurrentDensity = NumberOfNotesInsidePeriod / T

          if(CurrentDensity > LatestHigh):
            LatestHigh = CurrentDensity
          if(CurrentDensity < LatestLow):
            LatestLow = CurrentDensity

      #print(j-1,k-1,NumberOfNotesInsidePeriod)
      return LatestHigh, LatestLow
    
    #將所有譜面裡的鼓點時間點標出，再依照最低時間單位掃描指定時間範圍
    def FindExtremeDensityByScanning(self, T, ScanRate):
      Location = self.FindEveryActualNotesLocation()
      RelativeTime = [0]
      for i in range(len(Location)-1):
        temp = self.Duration(Location[0],Location[i+1])[0]
        RelativeTime.append(temp)

      LatestLow = float("inf")
      LatestHigh = 0
      PrintThresHold = 0

      import math
      import time
      ScanningLocation = -ScanRate/math.exp(1)
      while(ScanningLocation < RelativeTime[-1]):
        i = 0
        while(RelativeTime[i] < ScanningLocation):
          i = i + 1

        j = 0
        while(RelativeTime[j] < ScanningLocation + T):
          if(j + 1 == len(RelativeTime)):
            j = j + 1
            break
          j = j + 1
        NumberOfNotesInsidePeriod = j - i

        CurrentDensity = NumberOfNotesInsidePeriod / T

        if(CurrentDensity > LatestHigh):
          LatestHigh = CurrentDensity
        if(CurrentDensity < LatestLow):
          LatestLow = CurrentDensity
        ScanningLocation = ScanningLocation + ScanRate

        if(ScanningLocation + T > RelativeTime[-1]):
          break


        if(ScanningLocation>PrintThresHold):
          print(f"\rLatest\t:{round(LatestHigh,3)}\t/{round(LatestLow,3)}\tnotes/s\t/  Location:\t{self.TimeDisplay(ScanningLocation)}|{self.TimeDisplay(RelativeTime[-1])}",end='')
          PrintThresHold = PrintThresHold + 1
      print("\n")
      # time.sleep(1.5)
      # print(f"\r                                                                                                ")

      return LatestHigh, LatestLow
    
    #依照選擇的運算方式，輸出個別位置的相對位置和對應位置的視覺速度
    def SetSeenVelocityListedinLocation(self, Range, Comparison):
         SeenVelocity_list = []

         if(Range):
              NoteList = self.FindEveryPassedNotesLocation()
         else:
              NoteList = self.FindEveryActualNotesLocation()

         tenp_sc_before = None
         tenp_bpm_before = None

         for RelatedLocation in NoteList:
              tenp_sc_after = self.ScrollSet[RelatedLocation[0]][RelatedLocation[1]]
              tenp_bpm_after = self.BPMValueSet[RelatedLocation[0]][RelatedLocation[1]]


              if(Comparison):
                if(tenp_sc_after!=tenp_sc_before or tenp_bpm_after!=tenp_bpm_before):
                    SeenVelocity_list.append([RelatedLocation , tenp_bpm_after * tenp_sc_after])
                tenp_sc_before = tenp_sc_after
                tenp_bpm_before = tenp_bpm_after
              else:
                SeenVelocity_list.append([RelatedLocation , tenp_bpm_after * tenp_sc_after])

         return SeenVelocity_list
    
    #依照選擇的運算方式，輸出相應的變化值和變化次數
    #而其中主要計算的值為流速變化大小，也就是兩個點之間的變化倍數，值會大於1。
    #如果譜面有3個點，分別是流速從200變成400再變回200，那麼就算是變動2次，而兩次的倍數都計為2。
    def SeenVelChangeFrequency(self, Range, Comparison, IsDuration, Ref=None, ReCompute=False, ReCompureCause=None, HiLo=[None, None]):
         if(Ref==None):
            Ref = 24
         if(ReCompute):
          print(f"\r(Restart Computing Process...\tCurrent Reference = {round(Ref,3)}\tLast Result : {ReCompureCause}\t{HiLo}\t{HiLo[0]!=None and HiLo[1]!=None}", end='')
         #print(T)
         MultipleBase = 1
         ChangedTimes = 0
         SeenVelInfoCouple = self.SetSeenVelocityListedinLocation(Range, Comparison)
         PointNum = len(SeenVelInfoCouple)
         if(PointNum>=2):
              for i in range(PointNum-1):
                   Amplification = abs(SeenVelInfoCouple[i][1]/SeenVelInfoCouple[i+1][1])
                   if(Amplification!=1):
                        ChangedTimes = ChangedTimes + 1
                        if(Amplification<1):
                             Amplification = 1 / Amplification
                   if(IsDuration):
                      ChageVelocity = Amplification / ( self.Duration(SeenVelInfoCouple[i][0] , SeenVelInfoCouple[i+1][0])[0] )
                      MultipleBase = MultipleBase * (ChageVelocity / Ref)
                   else:
                      ChageVelocity = Amplification
                      MultipleBase = MultipleBase * ChageVelocity

              if(IsDuration):
                  #由於考慮進去兩點之間的時間差，而在瞬間密度很高且流速變化高的情形之下，值會變得非常的高。
                  #由於這邊採取的計算方式是所有資料相乘再做開特定次數的根號，因此在前面相乘的過程，就很容易先超過python的計算極限導致出現"inf"的結果。
                  #所以在這邊先令要計算的值除以一個特定的值(預設是24)，讓相乘之後的值降到可以計算，到了輸出時再把這個值乘回來。
                  #而若預設的值還是導致計算最後出現無限大，則將值增大再做一次，直到可以輸出正常值為止。
                  #而除以特定的值也可能導致相乘過後的數值太小，超過python運算極限導致出現0的結果，因此這個情況會反過來將值縮小，再做一遍

                  ReturnedResult = ( MultipleBase ** ( 1 / ( PointNum - 1 ) ) ) * Ref
                  #print(ReturnedResult)

                  if(ReturnedResult==float("inf")):
                      high_N_low = HiLo
                      if(HiLo[0]!=None and HiLo[1]!=None):
                        Reference = HiLo[1] - (HiLo[1] - HiLo[0]) / 3
                      else:
                        Reference = Ref*1.25
                      if(ReCompureCause=="zero"):
                        high_N_low[0] = Ref
                      ReturnedResult = self.SeenVelChangeFrequency(Range, Comparison, IsDuration, Reference, True, "Infinite", high_N_low)[0]
                  elif(ReturnedResult==0):
                      high_N_low = HiLo
                      if(HiLo[0]!=None and HiLo[1]!=None):
                        Reference = HiLo[0] + (HiLo[1] - HiLo[0]) / 3
                      else:
                        Reference = Ref/1.25
                      if(ReCompureCause=="Infinite"):
                        high_N_low[1] = Ref
                      ReturnedResult = self.SeenVelChangeFrequency(Range, Comparison, IsDuration, Reference, True, "zero", high_N_low)[0]
                  else:
                      return ReturnedResult , ChangedTimes

                  return ReturnedResult , ChangedTimes
              else:
                return MultipleBase ** ( 1 / ( PointNum - 1 ) ) , ChangedTimes
         else:
            if(IsDuration):
              return 0, ChangedTimes
            else:
              return 1, ChangedTimes
            
    def MultipliedRootOf(self, WantedType=None, precision_ref=None, x=[0,0], y=None, ReCompute=False):
         EveryBar = self.EveryBar
         SeenVelSet = self.SeenVelSet
         BPMValueSet = self.BPMValueSet
         ScrollSet = self.ScrollSet
         BeatsToMeasureSet = self.BeatsToMeasureSet

         if(WantedType==None):
            WantedType = "both"
         if(precision_ref==None):
            precision_ref = self.TempContent*3
         if(y==None):
            y = [len(EveryBar)-1, len(EveryBar[-1])-1]

         if(ReCompute):
          print(f"\r(Restart Computing Process... Current Reference = {round(precision_ref,3)})", end='')
         MulipliedThings = 1
         PortionPassedBy = 0

         if(WantedType.lower()=="both"):
              ChoosenFunction = SeenVelSet
         elif(WantedType.lower()=="bpm"):
              ChoosenFunction = BPMValueSet
         elif(WantedType.lower()=="scroll"):
              ChoosenFunction = ScrollSet

         #小節
         for j in range(x[0],y[0]+1):
              if(len(EveryBar[j])==1):
                   MeasureBeat, MeasureForm = BeatsToMeasureSet[j][0]
                   TargetValueT = ChoosenFunction[j][0]
                   if(WantedType.lower()=="both" or WantedType.lower()=="bpm"):
                        TargetValueT = TargetValueT / precision_ref

                   #可能與真正樂理上的算法有出入，這邊以太鼓次郎的判定作計算
                   MulipliedThings = MulipliedThings * ( TargetValueT ** ( MeasureBeat / MeasureForm ) )
                   PortionPassedBy = PortionPassedBy + ( MeasureBeat / MeasureForm )
              else:
                   if(x[0]==y[0]):
                        a = x[1]
                        b = y[1]
                   else:
                        if(j==x[0]):
                             a = x[1]
                             b = len(EveryBar[j]) - 1 #小節資訊的最後一個是逗號，因此考慮實際譜面要-1，其他地方以此類推
                        elif(j==y[0]):
                             a = 0
                             b = y[1]
                        else:
                             a = 0
                             b = len(EveryBar[j]) - 1

                   for i in range(a,b):
                        MeasureBeat, MeasureForm = BeatsToMeasureSet[j][i]
                        TargetValueF = ChoosenFunction[j][i]
                        if(WantedType.lower()=="both" or WantedType.lower()=="bpm"):
                             TargetValueF = TargetValueF / precision_ref
                        MulipliedThings = MulipliedThings * ( TargetValueF ** ( MeasureBeat / MeasureForm / (len(EveryBar[j]) - 1) ) )
                        PortionPassedBy = PortionPassedBy + ( MeasureBeat / MeasureForm / (len(EveryBar[j]) - 1) )

         if(WantedType.lower()=="both" or WantedType.lower()=="bpm"):
              WaitForReturning = MulipliedThings ** ( 1 / PortionPassedBy ) * precision_ref
              if(WaitForReturning==float("inf")):
                WaitForReturning = self.MultipliedRootOf(WantedType, precision_ref*2, x, y, True)
              elif(WaitForReturning==0):
                WaitForReturning = self.MultipliedRootOf(WantedType, precision_ref/1.1, x, y, True)
              else:
                return WaitForReturning
              return WaitForReturning
         else:
              return MulipliedThings ** ( 1 / PortionPassedBy )
         
    def SumAverageBPM(self, x=[0, 0], y=None):
         EveryBar = self.EveryBar

         DelaySet = self.DelaySet
         BeatsToMeasureSet = self.BeatsToMeasureSet
         BPMValueSet = self.BPMValueSet

         if(y==None):
            y = [len(EveryBar)-1, len(EveryBar[-1])-1]
         

         OverallDuration = 0
         PortionPassedBy = 0
         ProcessDirectionElement = 1

         if(x[0]>y[0] or (x[0]==y[0] and x[1]>y[1])):
              Temp = [x, y]
              x = Temp[1]
              y = Temp[0]
              ProcessDirectionElement = -1
              del Temp

         #起頭點部分的DELAY不應該被記入
         OverallDuration = OverallDuration - DelaySet[x[0]][x[1]]

         for j in range(x[0],y[0]+1):
              if len(EveryBar[j])==1:
                   MeasureBeat, MeasureForm = BeatsToMeasureSet[j][0]

                   #可能與真正樂理上的算法有出入，這邊以太鼓次郎的判定作計算
                   OverallDuration = OverallDuration + DelaySet[j][0] + 60 / BPMValueSet[j][0] * 4 * ( MeasureBeat / MeasureForm )
                   PortionPassedBy = PortionPassedBy + 4 * ( MeasureBeat / MeasureForm )
              else:
                   if(x[0]==y[0]):
                        a = x[1]
                        b = y[1]
                   else:
                        if(j==x[0]):
                             a = x[1]
                             b = len(EveryBar[j]) - 1 #小節資訊的最後一個是逗號，因此考慮實際譜面要-1，其他地方以此類推
                        elif(j==y[0]):
                             a = 0
                             b = y[1]
                        else:
                             a = 0
                             b = len(EveryBar[j]) - 1

                   for i in range(a,b):
                        MeasureBeat, MeasureForm = BeatsToMeasureSet[j][i]
                        OverallDuration = OverallDuration + DelaySet[j][i] + 60 / BPMValueSet[j][i] * 4 * ( MeasureBeat / MeasureForm ) / ( len(EveryBar[j]) - 1 )
                        PortionPassedBy = PortionPassedBy + 4 * ( MeasureBeat / MeasureForm / ( len(EveryBar[j]) - 1 ) )

              #由於每個小節尾端(也就是逗號所在位置)也能夠加上指令，故須考慮
              if(x[0]!=y[0] and j!=y[0]):
                  OverallDuration = OverallDuration + DelaySet[j][-1]

         #最後點所屬的部份的DELAY應該被考慮
         OverallDuration = OverallDuration + DelaySet[y[0]][y[1]]

         return 60 / ( OverallDuration / PortionPassedBy ) * ProcessDirectionElement
    
    def DefineAndFindComplexLocation(self, ref, type_mode=None):
      if(type_mode==None):
         type_mode="den"

      NotesLocation = self.FindEveryActualNotesLocation()
      ComplexesLocation = []
      IsInDenseThreshold = False

      if(type_mode=="den"):
        Threshold = 1 / ref
      elif(type_mode=="sec"):
        Threshold = ref
      elif(type_mode=="bpm"):
        Threshold = 60 / ref / 4

      TempComplexesLocation = []
      for i in range(len(NotesLocation)-1):

        if(self.Duration(NotesLocation[i],NotesLocation[i+1])[0]<=Threshold):
          IsInDenseThreshold = True
        else:
          IsInDenseThreshold = False

        if(IsInDenseThreshold):
          if(len(TempComplexesLocation)==0):
            TempComplexesLocation = [NotesLocation[i], NotesLocation[i+1]]
          else:
            TempComplexesLocation.append(NotesLocation[i+1])
        else:
          if(len(TempComplexesLocation)!=0):
            ComplexesLocation.append(TempComplexesLocation)
            TempComplexesLocation = []

      ComplexesLocation.append(TempComplexesLocation)

      return ComplexesLocation
    
    def DefineDiffucultyOfComplex(self, random_complex):
      ppp = random_complex
      aaa = ""
      for _ in ppp:
        if(_ == "1" or _ == "3"):
          aaa = aaa + "d"
        elif(_ == "2" or _ == "4"):
          aaa = aaa + "k"

      sign_change = 0
      hand_change = 0
      if(len(aaa)!=0):
        temp = aaa[0]
        sign_change = 0
        temp_str = ""
        new_str = []

        for _ in aaa:
          if(temp!=_):
            temp = _
            sign_change = sign_change + 1

          if(len(temp_str)<2):
            temp_str = temp_str + _
          else:
            new_str.append(temp_str)
            temp_str = ""
            temp_str = temp_str + _

        new_str.append(temp_str)

        hand_change = 0
        for k in range(len(new_str)-1):
          if(new_str[k][0]!=new_str[k][1] and new_str[k][1]==new_str[k+1][0]):
            hand_change = hand_change + 1

      return sign_change, hand_change
    
    #複合複雜性定義測試:
    #權重定義為：1/任一發生換手情況時的反應時間，之平方總和，最後除上所需換手次數再開根號 (單位:1/時間)
    #最後even與odd相乘再娶一次跟號
    def WeightOfDiffucultyOfComplex(self, IsEven):
      NotesLocation = self.FindEveryActualNotesLocation()
      FullSeriesNotes = ""
      for each in NotesLocation:
        if((not IsEven) and each == NotesLocation[0]):
          continue
        FullSeriesNotes = FullSeriesNotes + self.EveryBar[each[0]][each[1]]

      Original = FullSeriesNotes
      Transformed = ""
      for _ in Original:
        if(_ == "1" or _ == "3"):
          Transformed = Transformed + "d"
        elif(_ == "2" or _ == "4"):
          Transformed = Transformed + "k"

      sign_change = 0
      hand_change = 0

      if(len(Transformed)!=0):
        temp = Transformed[0]
        sign_change = 0
        temp_str = ""
        new_str = []

        for _ in Transformed:
          if(temp!=_):
            temp = _
            sign_change = sign_change + 1

          if(len(temp_str)<2):
            temp_str = temp_str + _
          else:
            new_str.append(temp_str)
            temp_str = ""
            temp_str = temp_str + _

        new_str.append(temp_str)

        hand_change = 0
        hand_change_weight = 1

        for k in range(len(new_str)-1):
          if(new_str[k][0]!=new_str[k][1] and new_str[k][1]==new_str[k+1][0]):
            hand_change = hand_change + 1
            if(IsEven):
              hand_change_weight = hand_change_weight + 10 ** ( 1 / self.Duration(NotesLocation[2*k], NotesLocation[2*(k+1)])[0] )
            else:
              hand_change_weight = hand_change_weight + 10 ** ( 1 / self.Duration(NotesLocation[2*k+1], NotesLocation[2*(k+1)+1])[0] )
      if(hand_change!=0):
        return sign_change, hand_change, hand_change_weight
      else:
        return sign_change, 0, 1

    def WeightResultOfComplex(self):

      even = self.WeightOfDiffucultyOfComplex(True)
      odd = self.WeightOfDiffucultyOfComplex(False)

      if(even[1]!=0):
        even_weight = ( even[2]*even[1] ) ** 0.5
      else:
        even_weight = 1

      if(even[1]!=0):
        odd_weight = ( odd[2]*odd[1] ) ** 0.5
      else:
        odd_weight = 1

      if(even_weight>odd_weight):
        high = even_weight
        low = odd_weight
      else:
        low = even_weight
        high = odd_weight

      if(low!=0 and high!=0):
        return math.log10( 1 + ( low ** 0.8 ) * ( high ** 0.2 ) )
      else:
        return 0
      
class TaikoFumenRealiztion(TaikoFumenBranched):
    def __init__(self, Path, codec, UserChosenFumen, UserChosenBranchDirection, Dots_per_inch):
        super().__init__(Path, codec, UserChosenFumen, UserChosenBranchDirection)
        self.Dots_per_inch = Dots_per_inch

    def ExtendBar(self, TargetBar, adjustratio, threshold=24):
      JudgeStandard = threshold * adjustratio
      if(len(TargetBar) > 1):
        NewBar = TargetBar
        k = 0
        while(len(NewBar) - 1 < JudgeStandard):
          k = k + 1
          NewBar = ""
          for Note in TargetBar:
            if(Note==","):
              break
            NewBar = NewBar + Note + "0" * k
          NewBar = NewBar + ","
        return NewBar
      else:
        return "0" * math.ceil(JudgeStandard) + ","

    def DetectRollSign(self, TargetBar):
      for piece in TargetBar:
        match piece:
          case "5" | "6" | "7" | "9":
            return True
      return False
    
    def PlotNotes_2(self, InputAboutBar, InputAboutMeasure, iteInRoll=None, iteRollsize=None, iteSelected_color=None, go=None, bpm=None, scr=None, balloon_count=None, PlotAct=True):
      if(balloon_count==None):
         balloon_count = 0

      FindWhereCommandShowUp = self.FindWhereCommandShowUp
      Get_BalloonKickNeeded = self.Get_BalloonKickNeeded
      DetectRollSign = self.DetectRollSign
      ExtendBar = self.ExtendBar

      EveryBar = self.EveryBar
      GOGOSet = self.GOGOSet
      ScrollSet = self.ScrollSet
      BPMValueSet = self.BPMValueSet
      BranchStateSet = self.BranchStateSet

      if(InputAboutMeasure[0]<=0 or InputAboutMeasure[1]<=0):
        raise Exception("\"" + str(InputAboutMeasure[0]) + "/" + str(InputAboutMeasure[1]) + "\" is not a beat that makes sense.")

      branch_start_cmd_loc = FindWhereCommandShowUp("#BRANCHSTART")
      branch_endin_cmd_loc = FindWhereCommandShowUp("#BRANCHEND")
      section_cmd_loc = FindWhereCommandShowUp("#SECTION")

      adjustratio = InputAboutMeasure[0]/InputAboutMeasure[1]
      BalloonKick = Get_BalloonKickNeeded()
      balloon = balloon_count

      if(isinstance(InputAboutBar, int)):     #輸入是小節數
        SomeBar = EveryBar[InputAboutBar]         #依照指定小節數字擷取其內容
        go_state = GOGOSet[InputAboutBar]         #擷取該小節的燃燒段狀態
        scr_state = ScrollSet[InputAboutBar]       #擷取該小節的倍速狀態
        bpm_state = BPMValueSet[InputAboutBar]      #擷取該小節的歌速狀態
        branch_state = BranchStateSet[InputAboutBar]   #擷取該小節的分歧狀態
        os.system('cls')
        print(f"\rGenerating Figure ({self.Dots_per_inch}dpi) ...\t{InputAboutBar+1} / {len(self.EveryBar)}",end='')

      elif(isinstance(InputAboutBar, str)):    #直接輸入小節內容
        if(InputAboutBar[-1]!=","):
          raise Exception("The end sign of a bar \",\" is lost.")
        SomeBar = InputAboutBar

      if(DetectRollSign(SomeBar) or iteInRoll==True):
        SomeBar = ExtendBar(SomeBar, adjustratio)

      DisplayedUnitWidth = 1.25
      plt.figure(figsize=(DisplayedUnitWidth + 5 * DisplayedUnitWidth * adjustratio,1), dpi=self.Dots_per_inch)      #圖片解析度
      plt.axhline(y=0, color='grey', linestyle='-', alpha=0.3, zorder=0)
      plt.xticks([])
      plt.yticks([])
      ax = plt.gca()
      ax.set_xlim([0-0.1/adjustratio, 1+0.1/adjustratio])
      ax.set_ylim([-0.1, 0.1])

      if(iteInRoll==None):
        InRoll = False
      else:
        InRoll = iteInRoll

      Selected_color = None
      Selected_marker = None
      SelectedEdgeColor = None
      size = None
      Rollsize = None
      existing = 0

      if(InRoll):
        Rollsize = iteRollsize
        Selected_color = iteSelected_color

      SignSizeToAxisValueRatio = 0.00194
      StartPosistionOffset = 0.0006
      Display_axis_bpm = 0.0865
      Display_axis_scr = -0.0890

      Display_fontsize = math.ceil(float(ReadConfig('config.ini', 'FIGURE', 'command_text_size')))
      balloonfontsize = math.ceil(float(ReadConfig('config.ini', 'FIGURE', 'ballon_text_size')))
      value_decimaldigits = math.ceil(float(ReadConfig('config.ini', 'FIGURE', 'round_decimalpoints')))

      WriteConfig('config.ini', 'FIGURE', 'command_text_size', str(Display_fontsize))
      WriteConfig('config.ini', 'FIGURE', 'ballon_text_size', str(balloonfontsize))
      WriteConfig('config.ini', 'FIGURE', 'round_decimalpoints', str(value_decimaldigits))

      plt.plot(0, 0, color="black", marker="o", markersize=25, mew=2.5, mec="grey", alpha=0.25, zorder=0)
      if(len(SomeBar)!=1):
        for i in range(len(SomeBar)):
          target_notes = SomeBar[i]
          if(InRoll):
            match target_notes:
              case "0" | "5" | "6" | "7" | "9":
                SafeDrawSize = (len(SomeBar)-1) / 16         #有連打的情況下，繼續用正方形可能會導致無法畫出圓形的頭尾
                #Selected_color = Rollcolor = Selected_color
                Selected_color = Selected_color
                if(i < SafeDrawSize * Rollsize / 20  or i > len(SomeBar) - 1 - SafeDrawSize * Rollsize / 20):
                  Selected_marker = "o"
                else:
                  Selected_marker = "s"
                SelectedEdgeColor = Selected_color
                size = Rollsize
                existing = 1
              case "8":
                #Selected_color = Rollcolor = Selected_color
                Selected_color = Selected_color
                Selected_marker = "o"
                SelectedEdgeColor = Selected_color
                size = Rollsize
                existing = 1
                InRoll = False
              case "1":
                Selected_color = "red"
                Selected_marker = "o"
                SelectedEdgeColor = "grey"
                size = 25
                existing = 1
                InRoll = False
              case "2":
                Selected_color = "blue"
                Selected_marker = "o"
                SelectedEdgeColor = "grey"
                size = 25
                existing = 1
                InRoll = False
              case "3":
                Selected_color = "red"
                Selected_marker = "o"
                SelectedEdgeColor = "grey"
                size = 40
                existing = 1
                InRoll = False
              case "4":
                Selected_color = "blue"
                Selected_marker = "o"
                SelectedEdgeColor = "grey"
                size = 40
                existing = 1
                InRoll = False
            if(not InRoll):
              plt.plot(i/(len(SomeBar)-1), 0, color=Selected_color, marker=Selected_marker, markersize=size, mew=2.5, mec=SelectedEdgeColor, alpha=existing, zorder=len(SomeBar)-i)
            else:
              if(i!=0 and i!=len(SomeBar)-1):
                ax.add_patch(plt.Rectangle((i/(len(SomeBar)-1), -size*SignSizeToAxisValueRatio-StartPosistionOffset), 1/(len(SomeBar)-1), (size-0)*SignSizeToAxisValueRatio*2, facecolor=Selected_color, alpha=1, zorder=len(SomeBar)-i))
              else:
                if(i==0):
                  ax.add_patch(plt.Rectangle((i/(len(SomeBar)-1), -size*SignSizeToAxisValueRatio-StartPosistionOffset), 1/(len(SomeBar)-1), (size-0)*SignSizeToAxisValueRatio*2, facecolor=Selected_color, alpha=1, zorder=len(SomeBar)-i))
                plt.plot(i/(len(SomeBar)-1), 0, color=Selected_color, marker=Selected_marker, markersize=size, mew=2.5, mec=Selected_color, alpha=existing, zorder=len(SomeBar)-i)
          else:
            match target_notes:
              case "1":
                Selected_color = "red"
                Selected_marker = "o"
                SelectedEdgeColor = "grey"
                size = 25
                existing = 1
              case "2":
                Selected_color = "blue"
                Selected_marker = "o"
                size = 25
                SelectedEdgeColor = "grey"
                existing = 1
              case "3":
                Selected_color = "red"
                Selected_marker = "o"
                SelectedEdgeColor = "grey"
                size = 40
                existing = 1
              case "4":
                Selected_color = "blue"
                Selected_marker = "o"
                SelectedEdgeColor = "grey"
                size = 40
                existing = 1
              case "5":
                Selected_color = "#FFD000"
                Selected_marker = "o"
                SelectedEdgeColor = "grey"
                size = 25
                Rollcolor = Selected_color
                Rollsize = size
                existing = 1
                InRoll = True
                NeedKick = False
              case "6":
                Selected_color = "#FFCC00"
                Selected_marker = "o"
                SelectedEdgeColor = "grey"
                size = 40
                Rollcolor = Selected_color
                Rollsize = size
                existing = 1
                InRoll = True
                NeedKick = False
              case "7":
                Selected_color = "#4EFEB3"
                Selected_marker = "D"
                SelectedEdgeColor = "grey"
                size = 25
                Rollcolor = Selected_color
                Rollsize = size
                existing = 1
                InRoll = True
                NeedKick = True
              case "9":
                Selected_color = "#FF7700"
                Selected_marker = "h"
                SelectedEdgeColor = "grey"
                size = 40
                Rollcolor = Selected_color
                Rollsize = size
                existing = 1
                InRoll = True
                NeedKick = True
              case _:
                existing = 0

            if(InRoll):
              ax.add_patch(plt.Rectangle((i/(len(SomeBar)-1), -size*SignSizeToAxisValueRatio-StartPosistionOffset), 1/(len(SomeBar)-1), (size-0)*SignSizeToAxisValueRatio*2, facecolor=Selected_color, alpha=1, zorder=len(SomeBar)-i))
              if(NeedKick):
                ax.text(i/(len(SomeBar)-1), 0, str(BalloonKick[balloon]), horizontalalignment='center', verticalalignment='center', weight="bold", fontsize=balloonfontsize, zorder=len(SomeBar)+1, color='black', alpha=1)
                balloon = balloon + 1

            plt.plot(i/(len(SomeBar)-1), 0, color=Selected_color, marker=Selected_marker, markersize=size, mew=2.5, mec=SelectedEdgeColor, alpha=existing, zorder=len(SomeBar)-i)


        else:
          plt.plot(0, 0, color="black", marker="o", markersize=25, mew=2.5, mec="grey", alpha=0, zorder=0)
      plt.plot(1, 0, color="black", marker="o", markersize=25, mew=2.5, mec="grey", alpha=0.2, zorder=0)
      if(isinstance(InputAboutBar, int)):  #輸入小節數
        Current_go = go
        Current_bpm = bpm
        Current_scr = scr

        if(len(EveryBar[InputAboutBar])!=1):
          for j in range(len(EveryBar[InputAboutBar])):
            pos = j/(len(EveryBar[InputAboutBar])-1)
            seg = 1/(len(EveryBar[InputAboutBar])-1)
            if(Current_bpm!=bpm_state[j]):
              Current_bpm = bpm_state[j]
              ax.text(pos, Display_axis_bpm, " " + str(round(Current_bpm, value_decimaldigits)), fontsize=Display_fontsize, zorder=len(SomeBar)+1 , color='red', alpha=1, verticalalignment='top')
              ax.axvline(pos, color='red', linestyle='-', alpha=0.3, zorder=0)
            #原先有考慮到複素數譜面，但基本沒有，所以以絕對值為值
            if(Current_scr!=scr_state[j]):
              Current_scr = scr_state[j]
              ax.text(pos, Display_axis_scr, " " + str(round(abs(Current_scr), value_decimaldigits)), fontsize=Display_fontsize, zorder=len(SomeBar)+1, color='blue', alpha=1, verticalalignment='bottom')
              ax.axvline(pos, color='blue', linestyle='-', alpha=0.3, zorder=0)
            #燃燒段
            if(go_state[j]):
              if(j!=len(EveryBar[InputAboutBar])-1):
                ax.add_patch(plt.Rectangle((pos, -0.1), seg, 0.2, facecolor="orange", alpha=0.2, zorder=0))
            #分岐
            if(j!=len(EveryBar[InputAboutBar])-1):
              match branch_state[j][2]:
                case 2:
                  ax.add_patch(plt.Rectangle((pos, 0.075), seg, 0.025, facecolor="#FFA8EC", alpha=0.5, zorder=0))
                  ax.add_patch(plt.Rectangle((pos, -0.1), seg, 0.025, facecolor="#FFA8EC", alpha=0.5, zorder=0))
                case 1:
                  ax.add_patch(plt.Rectangle((pos, 0.075), seg, 0.025, facecolor="#BAE3FF", alpha=0.5, zorder=0))
                  ax.add_patch(plt.Rectangle((pos, -0.1), seg, 0.025, facecolor="#BAE3FF", alpha=0.5, zorder=0))
                case 0:
                  ax.add_patch(plt.Rectangle((pos, 0.075), seg, 0.025, facecolor="grey", alpha=0.15, zorder=0))
                  ax.add_patch(plt.Rectangle((pos, -0.1), seg, 0.025, facecolor="grey", alpha=0.15, zorder=0))

            #與分岐相關的點
            for location in branch_start_cmd_loc:
              if(location == [InputAboutBar,j]):
                ax.axvline(pos, color='#FDE168', linestyle='-', alpha=1, zorder=0, linewidth=3)
                break
            for location in branch_endin_cmd_loc:
              if(location == [InputAboutBar,j]):
                ax.axvline(pos, color='#FDE168', linestyle='-', alpha=1, zorder=0, linewidth=3)
                break
            for location in section_cmd_loc:
              if(location == [InputAboutBar,j]):
                ax.axvline(pos, color='#FDE168', linestyle='-', alpha=1, zorder=0, linewidth=3)
                break
        else:
          if(Current_bpm!=bpm_state[0]):
            Current_bpm = bpm_state[0]
            ax.text(0, Display_axis_bpm, " " + str(round(Current_bpm, value_decimaldigits)), fontsize=Display_fontsize, zorder=len(SomeBar)+1 , color='red', alpha=1, verticalalignment='top') 
            ax.axvline(0, color='red', linestyle='-', alpha=0.3, zorder=0)
          #原先有考慮到複素數譜面，但基本沒有，所以先以絕對值為值
          if(Current_scr!=scr_state[0]):
            Current_scr = scr_state[0]
            ax.text(0, Display_axis_scr, " " + str(round(abs(Current_scr), value_decimaldigits)), fontsize=Display_fontsize, zorder=len(SomeBar)+1, color='blue', alpha=1, verticalalignment='bottom')
            ax.axvline(0, color='blue', linestyle='-', alpha=0.3, zorder=0)
          #燃燒段
          if(go_state[0]):
            ax.add_patch(plt.Rectangle((0, -0.1), 1, 0.2, facecolor="orange", alpha=0.2, zorder=0))
          #分岐
          if(branch_state[0]):
            match branch_state[0][2]:
              case 2:
                #FFA8EC
                ax.add_patch(plt.Rectangle((0, 0.075), 1, 0.025, facecolor="#FFA8EC", alpha=0.5, zorder=0))
                ax.add_patch(plt.Rectangle((0, -0.1), 1, 0.025, facecolor="#FFA8EC", alpha=0.5, zorder=0))
              case 1:
                #BAE3FF
                ax.add_patch(plt.Rectangle((0, 0.075), 1, 0.025, facecolor="#BAE3FF", alpha=0.5, zorder=0))
                ax.add_patch(plt.Rectangle((0, -0.1), 1, 0.025, facecolor="#BAE3FF", alpha=0.5, zorder=0))
              case 0:
                ax.add_patch(plt.Rectangle((0, 0.075), 1, 0.025, facecolor="grey", alpha=0.15, zorder=0))
                ax.add_patch(plt.Rectangle((0, -0.1), 1, 0.025, facecolor="grey", alpha=0.15, zorder=0))

          #與分岐相關的點
          for location in branch_start_cmd_loc:
            if(location == [InputAboutBar,0]):
              ax.axvline(0, color='#FDE168', linestyle='-', alpha=1, zorder=0, linewidth=3)
              break
          for location in branch_endin_cmd_loc:
            if(location == [InputAboutBar,0]):
              ax.axvline(0, color='#FDE168', linestyle='-', alpha=1, zorder=0, linewidth=3)
              break
          for location in section_cmd_loc:
            if(location == [InputAboutBar,0]):
              ax.axvline(0, color='#FDE168', linestyle='-', alpha=1, zorder=0, linewidth=3)
              break


        ax.text(-0.09/adjustratio, -0.0875, str(len(EveryBar)), fontsize=8, zorder=len(SomeBar)+1 , alpha=1)
        ax.text(-0.09/adjustratio, 0.0660, str(InputAboutBar+1), fontsize=8, zorder=len(SomeBar)+1 , alpha=1)

      for k in range(InputAboutMeasure[0]+1):
        if(k/InputAboutMeasure[1]/adjustratio>1):
          continue
        ax.axvline(x=k/InputAboutMeasure[1]/adjustratio, color='grey', linestyle='-', alpha=0.1, zorder=-1)

      if(isinstance(InputAboutBar, int)):
        return InRoll, Rollsize, Selected_color, go, Current_bpm, Current_scr, balloon
      
    def PlotAllNotes(self):
        PassRoll, PassRollSize, PassNoteColor, go, bpm, scr, balloon = None, None, None, None, None, None, 0
        BarNum = len(self.EveryBar)
        for x in range(BarNum):
            
            PassRoll, PassRollSize, PassNoteColor, go, bpm, scr, balloon = \
              self.PlotNotes_2(x, self.BeatsToMeasureSet[x][0], PassRoll, PassRollSize, PassNoteColor, go, bpm, scr, balloon)
            plt.show(block=False)


    def PlotAllNotes(self, SaveRequired=False):
      PassRoll, PassRollSize, PassNoteColor, go, bpm, scr, balloon = None, None, None, None, None, None, 0
      if(SaveRequired):
        os.mkdir("_figure")
        for x in range(len(self.EveryBar)):
          PassRoll, PassRollSize, PassNoteColor, go, bpm, scr, balloon = \
            self.PlotNotes_2(x, self.BeatsToMeasureSet[x][0], PassRoll, PassRollSize, PassNoteColor, go, bpm, scr, balloon)
          plt.axis('off')
          plt.savefig("_figure/" + str(x+1) + '.png', bbox_inches='tight', pad_inches=0)  #Sovled By Copilot
          plt.clf()   
          plt.close('all')
          
        print("\n")

      else:
        for x in range(len(self.EveryBar)):
          PassRoll, PassRollSize, PassNoteColor, go, bpm, scr, balloon = self.PlotNotes_2(x, self.BeatsToMeasureSet[x][0], PassRoll, PassRollSize, PassNoteColor, go, bpm, scr, balloon)

    def PlotSingleNotes(self, InputAboutBar, InputAboutMeasure, iteInRoll=None, iteRollsize=None, iteSelected_color=None, go=None, bpm=None, scr=None, balloon_count=None):
      if(os.path.isdir("_tempfig")):
        raise Exception("Please rename or delete the \"_tempfig\" folder lest the following executing process goes wrong.")
      if(balloon_count==None):
        balloon_count = 0
      self.PlotNotes_2(InputAboutBar, InputAboutMeasure, iteInRoll, iteRollsize, iteSelected_color, go, bpm, scr, balloon_count)
      os.mkdir("_tempfig")
      plt.savefig("_tempfig/cur.png")