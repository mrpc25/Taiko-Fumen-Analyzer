from taiko import TaikoFumen
from taiko import TaikoFumenInner
from taiko import TaikoFumenBranched
from taiko import TaikoFumenRealiztion
import predictlevel as pfl

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image, ImageTk
import os
import sys
import shutil
import configparser

#momory problem solved at https://github.com/matplotlib/matplotlib/issues/20490/
import matplotlib
matplotlib.use('agg')
plt.pause(.01)

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

def WipeFileExtension(FileName):
    NewFileName = ""
    for char in FileName:
        if(char=="."): return NewFileName
        NewFileName = NewFileName + char

def Language_Reopen(language):
    WriteConfig("config.ini", "PARAMETERS", "language", language)
    WriteConfig("config.ini", "SELF", "open", "0")
    os.execv(sys.executable, ['python'] + sys.argv)


LangFiles = os.listdir("lang")

Languege = ReadConfig("config.ini", "PARAMETERS", "language")
Languege_Path = "lang/" + Languege + ".ini"

LangChoices = [WipeFileExtension(x) for x in LangFiles]

#TEXT:設定視窗的文字
TEXT_SETTING_TITLE = ReadConfig(Languege_Path, "SETTING", "TEXT_SETTING_TITLE")
TEXT_SETTING_IMAGEDPI = ReadConfig(Languege_Path, "SETTING", "TEXT_SETTING_IMAGEDPI")
TEXT_SETTING_SCANRATE = ReadConfig(Languege_Path, "SETTING", "TEXT_SETTING_SCANRATE")
TEXT_SETTING_APPLY = ReadConfig(Languege_Path, "SETTING", "TEXT_SETTING_APPLY")

TEXT_SETTING_MESSAGE_INVALIDSCANRATE_NUMBER = ReadConfig(Languege_Path, "SETTING", "TEXT_SETTING_MESSAGE_INVALIDSCANRATE_NUMBER")
TEXT_SETTING_MESSAGE_INVALIDSCANRATE_POSITIVE =  ReadConfig(Languege_Path, "SETTING", "TEXT_SETTING_MESSAGE_INVALIDSCANRATE_POSITIVE")
TEXT_SETTING_MESSAGE_INVALIDDPI_POSITIVE = ReadConfig(Languege_Path, "SETTING", "TEXT_SETTING_MESSAGE_INVALIDDPI_POSITIVE")
TEXT_SETTING_MESSAGE_INVALIDDPI_INTEGER = ReadConfig(Languege_Path, "SETTING", "TEXT_SETTING_MESSAGE_INVALIDDPI_INTEGER")

#TEXT:設定主視窗的文字
TEXT_ROOT_WINDOWTITLE = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_WINDOWTITLE")
TEXT_ROOT_FILEPATHDISPLAY = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_FILEPATHDISPLAY")

TEXT_ROOT_NOTE5 = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTE5")
TEXT_ROOT_NOTE6 = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTE6")
TEXT_ROOT_NOTE7 = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTE7")
TEXT_ROOT_NOTE9 = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTE9")

TEXT_ROOT_MESSAGE_NOTLOAD = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_MESSAGE_NOTLOAD")
TEXT_ROOT_MESSAGE_NOTSELECTED = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_MESSAGE_NOTSELECTED")
TEXT_ROOT_MESSAGE_NOTSELECTED_BRANCH = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_MESSAGE_NOTSELECTED_BRANCH")

TEXT_ROOT_TITLE = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_TITLE")
TEXT_ROOT_COURSE = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_COURSE")
TEXT_ROOT_DUAL = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_DUAL")
TEXT_ROOT_BRANCH = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_BRANCH")
TEXT_ROOT_MESSAGE_NOROLLEXIST = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_MESSAGE_NOROLLEXIST")
TEXT_ROOT_NOTAVAILABLE = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTAVAILABLE")
TEXT_ROOT_DRUMHITS = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_DRUMHITS")

TEXT_ROOT_TERMINAL_DETAILEDINFO = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_TERMINAL_DETAILEDINFO")
TEXT_ROOT_BRANCH = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_BRANCH")

TEXT_ROOT_NOTESINFO_UPPER = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTESINFO_UPPER")
TEXT_ROOT_NOTESINFO_LOWER = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTESINFO_LOWER")
TEXT_ROOT_TOTAL = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_TOTAL")
TEXT_ROOT_NOTE1 = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTE1")
TEXT_ROOT_NOTE2 = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTE2")
TEXT_ROOT_NOTE3 = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTE3")
TEXT_ROOT_NOTE4 = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOTE4")

TEXT_ROOT_EXTREME_DENSITY_UPPER = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_EXTREME_DENSITY_UPPER")
TEXT_ROOT_EXTREME_DENSITY_LOWER = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_EXTREME_DENSITY_LOWER")
TEXT_ROOT_LOWEST = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_LOWEST")
TEXT_ROOT_HIGHEST = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_HIGHEST")
TEXT_ROOT_20LOWEST = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_20LOWEST")
TEXT_ROOT_20HIGHEST = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_20HIGHEST") 
#solved at https://stackoverflow.com/questions/56981215/issue-in-python-code-configparser-interpolationsyntaxerror-must-be-follow

TEXT_ROOT_AVERAGEDENSITY = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_AVERAGEDENSITY") 
TEXT_ROOT_TOTALDELAY = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_TOTALDELAY") 
TEXT_ROOT_TOTALTIME = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_TOTALTIME") 

TEXT_ROOT_AVERAGESEENSPEED = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_AVERAGESEENSPEED") 
TEXT_ROOT_LASTFOR = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_LASTFOR") 
TEXT_ROOT_ROLLLOCATION = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_ROLLLOCATION") 

TEXT_ROOT_SEENVELOCITYCHANGE = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_SEENVELOCITYCHANGE") 
TEXT_ROOT_SEENVELOCITYCHANGERATE = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_SEENVELOCITYCHANGERATE") 

TEXT_ROOT_FUMENGEN_UPPER = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_FUMENGEN_UPPER") 
TEXT_ROOT_FUMENGEN_LOWER = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_FUMENGEN_LOWER") 

TEXT_ROOT_GENERATEFIG = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_GENERATEFIG") 
TEXT_ROOT_SAVEFIG = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_SAVEFIG") 
TEXT_ROOT_PICKBARTODISPLAY = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_PICKBARTODISPLAY") 

TEXT_ROOT_LEVELPREDICT_UPPER = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_LEVELPREDICT_UPPER") 
TEXT_ROOT_LEVELPREDICT_LOWER = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_LEVELPREDICT_LOWER") 
TEXT_ROOT_COURSEFORPREDICT = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_COURSEFORPREDICT") 

TEXT_ROOT_RUNPREDICT = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_RUNPREDICT") 
TEXT_ROOT_ACTUALLEVEL = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_ACTUALLEVEL") 
TEXT_ROOT_PREDICTLEVEL = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_PREDICTLEVEL") 

TEXT_ROOT_STANDARD = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_STANDARD") 
TEXT_ROOT_MOEDL = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_MOEDL") 

TEXT_ROOT_MENU_OPEN = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_MENU_OPEN") 
TEXT_ROOT_MENU_SETTING = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_MENU_SETTING") 
TEXT_ROOT_MENU_OPTION = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_MENU_OPTION") 

#TEXT: 放大圖片的視窗
TEXT_ZOOMEDFIG_ZOOMIN = ReadConfig(Languege_Path, "FIGURE_ZOOM", "TEXT_ZOOMEDFIG_ZOOMIN") 

#後來加的
TEXT_ROOT_NOBRANCHFOUNDED = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_NOBRANCHFOUNDED") 
TEXT_ROOT_CODEC = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_CODEC") 
TEXT_ROOT_ROLLSINFO_UPPER = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_ROLLSINFO_UPPER") 
TEXT_ROOT_ROLLSINFO_LOWER = ReadConfig(Languege_Path, "ROOT", "TEXT_ROOT_ROLLSINFO_LOWER") 
TEXT_SETTING_LANGUAGE = ReadConfig(Languege_Path, "SETTING", "TEXT_SETTING_LANGUAGE") 
TEXT_SETTING_MESSAGE_RESTARTBYLARG = ReadConfig(Languege_Path, "SETTING", "TEXT_SETTING_MESSAGE_RESTARTBYLARG") 


def show(x):
    x.set(x.get())

def LeftNumberInString(String):
    NewString = ""
    for char in String:
        if(str.isnumeric(char) or char=='.' or char=='-'):
            NewString = NewString + char
    return NewString

def SettingValue_scanrate():
    global DEFAULT_DPI
    global DEFAULT_SCANRATE
    global adjust_scanrate_Box
    try:
        AfterValue = float(LeftNumberInString(adjust_scanrate_Box.get()))
        if(AfterValue > 0):
            adjust_scanrate_Box.delete(0,'end')
            adjust_scanrate_Box.insert(0, str(AfterValue))
            WriteConfig("config.ini", "PARAMETERS", "scanrate", str(AfterValue))
            DEFAULT_SCANRATE = AfterValue
        else:
            messagebox.showinfo('showinfo', TEXT_SETTING_MESSAGE_INVALIDSCANRATE_POSITIVE)
            adjust_scanrate_Box.delete(0,'end')
            adjust_scanrate_Box.insert(0, str(DEFAULT_SCANRATE))
    except:
        messagebox.showinfo('showinfo', TEXT_SETTING_MESSAGE_INVALIDSCANRATE_NUMBER)
        adjust_scanrate_Box.delete(0,'end')
        adjust_scanrate_Box.insert(0, str(DEFAULT_SCANRATE))

def SettingValue_dpi():
    global DEFAULT_DPI
    global DEFAULT_SCANRATE
    global adjust_dpi_Box
    # global setting
    try:
        AfterValue = int(LeftNumberInString(adjust_dpi_Box.get()))
        if(AfterValue > 0):
            adjust_dpi_Box.delete(0,'end')
            adjust_dpi_Box.insert(0, str(AfterValue))
            WriteConfig("config.ini", "PARAMETERS", "dpi", str(AfterValue))
            DEFAULT_DPI = AfterValue
        else:
            messagebox.showinfo('showinfo',TEXT_SETTING_MESSAGE_INVALIDDPI_POSITIVE)
            adjust_dpi_Box.delete(0,'end')
            adjust_dpi_Box.insert(0, str(DEFAULT_DPI))
    except:
        messagebox.showinfo('showinfo', TEXT_SETTING_MESSAGE_INVALIDDPI_INTEGER)
        adjust_dpi_Box.delete(0,'end')
        adjust_dpi_Box.insert(0, str(DEFAULT_DPI))
    
def SettingValue_language():
    global Language_list
    ChooseLanguage = Language_list.get()
    if(ChooseLanguage!=Languege):
        result = messagebox.askquestion('prompt', TEXT_SETTING_MESSAGE_RESTARTBYLARG)
        if(result=="yes"):
            Language_Reopen(ChooseLanguage)
        else:
            Language_list.set(Languege)

#建立Setting的視窗
def CreateSettingWindow():
    global DEFAULT_DPI
    global DEFAULT_SCANRATE

    global adjust_scanrate_value
    global adjust_scanrate_Box
    global adjust_scanrate_btn

    global adjust_dpi_Box
    global adjust_dpi_btn

    global Language_list

    DEFAULT_SCANRATE = float(ReadConfig("config.ini", "PARAMETERS", "scanrate"))
    DEFAULT_DPI = int(ReadConfig("config.ini", "PARAMETERS", "dpi"))

    setting = tk.Toplevel()   # 建立 tkinter 視窗至頂物件
    setting.grab_set()
    setting.iconbitmap('img/setting.ico')  # 設定 icon ( 格式限定 .ico )

    setting.title(TEXT_SETTING_TITLE)        # 設定標題
    sub_width = 240
    sub_height = 120
    sub_left = root.winfo_x() + round(width/2) - round(sub_width/2)
    sub_top = root.winfo_y() + round(height/2) - round(sub_height/2)
    setting.geometry(f'{sub_width}x{sub_height}+{sub_left}+{sub_top}')  # 定義視窗的尺寸和位置

    adjust_dpi_value = tk.StringVar()
    adjust_dpi_Box = tk.Spinbox(setting, from_=60, to=960, textvariable=adjust_dpi_value, justify='center', width=8, increment=10)
    adjust_dpi_Box.delete(0,'end')
    adjust_dpi_Box.insert(0, str(DEFAULT_DPI))
    adjust_dpi_Box.place(relx=0.5, rely=0.25, anchor='center')
    adjust_dpi = tk.Label(setting, text=TEXT_SETTING_IMAGEDPI, font=('Arial', 8))
    adjust_dpi.place(relx=0.1, rely=0.25, anchor='w')
    adjust_dpi_btn = tk.Button(setting, text=TEXT_SETTING_APPLY, width=5, height=1, justify='center', command=SettingValue_dpi, state='active') 
    adjust_dpi_btn.place(relx=0.9, rely=0.25, anchor='e', height=20)

    adjust_scanrate_value = tk.StringVar()
    adjust_scanrate_Box = tk.Entry(setting, textvariable=adjust_scanrate_value,justify='center')
    adjust_scanrate_Box.insert(0, str(DEFAULT_SCANRATE))
    adjust_scanrate_Box.place(relx=0.5, rely=0.5, anchor='center', width=70)
    adjust_scanrate = tk.Label(setting, text=TEXT_SETTING_SCANRATE, font=('Arial', 8))
    adjust_scanrate.place(relx=0.1, rely=0.5, anchor='w')
    adjust_scanrate_btn = tk.Button(setting, text=TEXT_SETTING_APPLY, width=5, height=1, justify='center', command=SettingValue_scanrate, state='active') 
    adjust_scanrate_btn.place(relx=0.9, rely=0.5, anchor='e', height=20)
    
    Language = tk.Label(setting, text=TEXT_SETTING_LANGUAGE, font=('Arial', 8))
    Language.place(relx=0.1, rely=0.75, anchor='w')
    Language_list = ttk.Combobox(setting, height=5, values=LangChoices, justify='center', state='readonly')        #假譜面選擇框
    Language_list.place(relx=0.5, rely=0.75, anchor='center', width=70)
    Language_list.set(Languege)
    Language_list_btn = tk.Button(setting, text=TEXT_SETTING_APPLY, width=5, height=1, justify='center', command=SettingValue_language, state='active') 
    Language_list_btn.place(relx=0.9, rely=0.75, anchor='e', height=20)

    setting.resizable(False, False)
    setting.mainloop()

ProcessedYet = False

#基本值
DEFAULT_SCANRATE = float(ReadConfig("config.ini", "PARAMETERS", "scanrate"))
DEFAULT_DPI = int(ReadConfig("config.ini", "PARAMETERS", "dpi"))
DEFAULT_CODEC = ReadConfig("config.ini", "PARAMETERS", "codec")

DEFAULT_OPEN_BYUSER = ReadConfig("config.ini", "SELF", "open")

root = tk.Tk()   # 建立 tkinter 視窗物件
root.iconbitmap('img/root.ico')

root.title(TEXT_ROOT_WINDOWTITLE)        # 設定標題
width = 600
height = 400
left = root.winfo_screenwidth() 
top = root.winfo_screenheight() 
root.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置


#純外觀
separator_1 = ttk.Separator(root, orient='horizontal')
separator_1.place(relx=0.5, rely=0.24, relwidth=0.98, anchor='center')

separator_2 = ttk.Separator(root, orient='vertical')
separator_2.place(relx=0.57, rely=0.12, relheight=0.22, anchor='center')

separator_3 = ttk.Separator(root, orient='horizontal')
separator_3.place(relx=0.5, rely=0.485, relwidth=0.98, anchor='center')

separator_4 = ttk.Separator(root, orient='horizontal')
separator_4.place(relx=0.5, rely=0.645, relwidth=0.98, anchor='center')

separator_5 = ttk.Separator(root, orient='horizontal')
separator_5.place(relx=0.5, rely=0.86, relwidth=0.98, anchor='center')

#Step0 / 預設值
file_path = "-"
file_path_value = tk.StringVar()
file_path_text = tk.Label(root, text=TEXT_ROOT_FILEPATHDISPLAY)
file_path_text.place(relx=0, rely=0, anchor='nw')
file_path_display = tk.Entry(root, textvariable=file_path_value, width=35, state="readonly")
file_path_display.place(relx=0.12, rely=0, anchor='nw')

# Codec = "raw_unicode_escape"
Codec = DEFAULT_CODEC
Codec_text = tk.Label(root, text=TEXT_ROOT_CODEC + " = ")
Codec_text.place(relx=0.6, rely=0, anchor='nw')
Codec_Option = ["utf_8", "ascii", "cp860", "johab", "shift_jis", "big5", "hz", "unicode_escape", "raw_unicode_escape"]
CodecOptionList = ttk.Combobox(root, width=22, height=5, values=Codec_Option, justify='center')
CodecOptionList.set(Codec)
def Update_Codec_Option(event):  #隨著選項，更新譜面顯示的相關資訊
    global CodecOptionList
    global Codec
    Codec = CodecOptionList.get()
    WriteConfig("config.ini", "PARAMETERS", "codec", Codec)
CodecOptionList.bind("<<ComboboxSelected>>", Update_Codec_Option)
CodecOptionList.place(relx=0.7, rely=0, anchor='nw')

FumenOptionList_im = ttk.Combobox(root, width=2, height=5, values=[], justify='center', state="disabled")        #假譜面選擇框
FumenOptionList_im.place(relx=0.153, rely=0.1, anchor='w')

BranchOptionList_im = ttk.Combobox(root, width=29, height=10, values=[], justify='center', state='disabled')      #假分歧選擇框
BranchOptionList_im.place(relx=0.153, rely=0.175, anchor='w')

#Step1 / 分辨檔案中的各個譜面
LoadedYet = False

def Reduced_file_path(Og_path):
    New = ""
    for char in Og_path:
        if(char!="/"):
            New = New + char
        else:
            New = ""
    return New

def Ask_forfile():
    global file_path
    global file_path_value
    global LoadedYet

    global song_basic
    global song_selected
    global song_branched

    file_path = filedialog.askopenfilename(filetypes=[(TEXT_ROOT_FUMENGEN_UPPER, '*.tja')])
    if(file_path==""): return
    if(LoadedYet): NewFumen_Initualize()
    LoadedYet = True

    file_path_value.set(Reduced_file_path(file_path))
    Ask_WhichFumen()


def NewFumen_Initualize():
    level_Compute_button.configure(state='disabled')
    GenFig_button.configure(state='disabled')   
    ChooseBranch_btn.configure(state="disabled")

    ViewFigureOptionList.configure(state='disabled', values=[])
    ViewFigureOptionList.set("-")

    RollsOptionList.configure(state='disabled', values=[])
    RollsOptionList.set("")

    BranchOptionList.configure(state='disabled', values=[])
    BranchOptionList.set("")

    #譜面基本資訊顯示
    COURSE_value.set("")
    DUAL_value.set("")
    LEVEL_value.set("")


    #當前譜面資訊
    TITLE.config(text=TEXT_ROOT_TITLE + " : " + "?")
    COURSE.config(text=TEXT_ROOT_COURSE + " : " + "?")
    DUAL.config(text=TEXT_ROOT_DUAL + " : " + "?")
    LEVEL.config(text="★"+"?")
    BRANCH.config(text=TEXT_ROOT_BRANCH + " : " + "?")

    #譜面音符組成
    NotesNum_total_value.set("")
    NotesNum_d_value.set("")
    NotesNum_k_value.set("")
    NotesNum_Bd_value.set("")
    NotesNum_Bk_value.set("")

    #最大/最小/20%最大/20%最小/平均密度
    Highest_density_value.set("")
    Lowest_density_value.set("")
    
    Highest20_density_value.set("")
    Lowest20_density_value.set("")

    av_density_value.set("")

    #譜面時間/使用延遲指令時間
    fumen_period_value.set("")
    delay_period_value.set("")

    #譜面平均視覺速度
    SeenVel_rootav_value.set("")

    #連打資訊
    RollsOptionList.configure(values=[], state="disabled")
    RollType_value.set("")

    Roll_location_beg_value.set("")
    Roll_location_end_value.set("")
    RollLast_value.set("")
    Roll_kick_value.set("")

    #視速變化
    SeenVelChangeLevel_value.set("")
    SeenVelChangeRate_value.set("")

    #預測星數
    ActualLevel_value.configure(text="?")
    PredictLevel_value.configure(text="?")

    #按鈕狀態設定/其他類似的初始話動作
    shutil.rmtree("_figure", True)              #刪除如果上一個譜面有生成譜面的話會有的"_figure"資料夾
    canvas.delete('all')                        #刪除因上一個譜面的最後一個選擇而顯示在視窗的譜面圖

    SaveFig_button.configure(state='disabled')
    zoom_button.configure(state="disabled")

FumenOptionList = ttk.Combobox(root, width=2, height=5, values=[], justify='center')
SelectedYet = False
def Ask_WhichFumen():
    global song_basic
    global Fumen_Option_raw
    global FumenOptionList

    song_basic = TaikoFumen(file_path, Codec)

    Fumen_Option_raw = song_basic.FumanClassfication
    Fumen_Option = list(range(len(Fumen_Option_raw)))

    FumenOptionList = ttk.Combobox(root, width=2, height=5, values=Fumen_Option, justify='center', state="readonly")
    FumenOptionList.set("-")
    FumenOptionList.bind("<<ComboboxSelected>>", Update_FumenOption)
    FumenOptionList.place(relx=0.153, rely=0.1, anchor='w')

def Update_FumenOption(event):  #隨著選項，更新譜面顯示的相關資訊
    global BranchOptionList
    global SelectedYet
    global LoadedYet
    
    FumenOption = FumenOptionList.get()
    if(FumenOption=="-" or FumenOption==None):
        SelectedYet = False
    else:
        SelectedYet = True
    COURSE_value.set(Fumen_Option_raw[int(FumenOption)][1])
    DUAL_value.set(Fumen_Option_raw[int(FumenOption)][2])
    LEVEL_value.set(Fumen_Option_raw[int(FumenOption)][3])

def Update_BranchOption(event):
    level_Compute_button.configure(state='disabled')

def Update_ViewOption(event):
    global ViewOption
    global img_path
    ViewOption = ViewFigureOptionList.get()
    img_path = "_figure/" + str(ViewOption) + ".png"
    ShowFigure(img_path)

def Update_RollsOptions(event):
    global Rolls_info
    global SelectedRollYet
    global Roll_KickState

    RollsOption = RollsOptionList.get()
    
    if(RollsOption=="-" or RollsOption==None):
        SelectedRollYet = False
    else:
        SelectedRollYet = True

    match Rolls_info[int(RollsOption)][0]:
        case 5:
            RollType_value.set(TEXT_ROOT_NOTE5)
        case 6:
            RollType_value.set(TEXT_ROOT_NOTE6)
        case 7:
            RollType_value.set(TEXT_ROOT_NOTE7)
        case 9:
            RollType_value.set(TEXT_ROOT_NOTE9)

    LastingLocation = Rolls_info[int(RollsOption)][1]
    BeginLocationText = str(LastingLocation[0][0] + 1) + " / " + str(LastingLocation[0][1] + 1)
    EndinLocationText = str(LastingLocation[1][0] + 1) + " / " + str(LastingLocation[1][1] + 1)
    RollLastingTime = round(song_branched.Duration(LastingLocation[0],LastingLocation[1])[0], 3)

    Roll_location_beg_value.set(BeginLocationText)
    Roll_location_end_value.set(EndinLocationText)
    RollLast_value.set(RollLastingTime)
    Roll_kick_value.set(Roll_KickState[int(RollsOption)])


#Step2 / 選擇譜面以後，載入基本資訊，並判斷有無分岐
ChoosenBranch = ""
ChoosenBranchValue = tk.StringVar()                                        # 取值
ChoosenBranchValue.set(ChoosenBranch)

Branch = ["0 / 普通譜面 / Normal", "1 / 玄人譜面 / Professional", "2 / 達人譜面 / Master"]
BranchOptionList = ttk.Combobox(root, width=29, height=10, values=[], justify='center', state='disabled')
ProcessedYet_branch = False
def Ask_FumenInner():
    global song_selected
    global BranchOptionList
    global ChoosenBranchValue #test
    global Fumen_Option_raw
    global FumenOption


    if(not LoadedYet):
        messagebox.showinfo('showinfo', TEXT_ROOT_MESSAGE_NOTLOAD)
        return
    if(not SelectedYet):
        messagebox.showinfo('showinfo', TEXT_ROOT_MESSAGE_NOTSELECTED)
        return

    FumenOption = FumenOptionList.get()
    song_selected = TaikoFumenInner(file_path, Codec, int(FumenOption[0]))

    if(song_selected.IsBranchExist):
        #按鈕狀態設定
        ChooseBranch_btn.configure(state="active")

        ChoosenBranchValue.set(Branch[2])

        BranchOptionList = ttk.Combobox(root, width=29, height=10, values=Branch, justify='center', state="readonly")
        BranchOptionList.bind("<<ComboboxSelected>>", Update_BranchOption)
        BranchOptionList.set(Branch[2])
        BranchOptionList.place(relx=0.153, rely=0.175, anchor='w')

        level_Compute_button.configure(state='disabled')
        GenFig_button.configure(state='disabled')   
    else:
        #按鈕狀態設定
        ChooseBranch_btn.configure(state="disabled")

        ChoosenBranchValue.set(None)
        BranchOptionList = ttk.Combobox(root, width=29, height=10, values=[], justify='center', state='disabled')
        BranchOptionList.set(TEXT_ROOT_NOBRANCHFOUNDED)
        BranchOptionList.place(relx=0.153, rely=0.175, anchor='w')

        Ask_FinalFumen()

    #按鈕狀態設定/其他類似的初始話動作
    shutil.rmtree("_figure", True)              #刪除如果上一個譜面有生成譜面的話會有的"_figure"資料夾
    canvas.delete('all')                        #刪除因上一個譜面的最後一個選擇而顯示在視窗的譜面圖
    
    ViewFigureOptionList.configure(state='disabled', values=[])
    ViewFigureOptionList.set("-")

    SaveFig_button.configure(state='disabled')
    zoom_button.configure(state="disabled")


ChooseFumen_btn = tk.Button(root, text=TEXT_ROOT_FUMENGEN_UPPER , width=7, command=Ask_FumenInner, height=1, justify='center')          #不能寫成"Ask_FumenInner()"，這樣會自動執行Ask_FumenInner的函式
ChooseFumen_btn.place(relx=0.01, rely=0.1, anchor='w')

#Step3 / 選擇分期狀態以後，
def Ask_FinalFumen():
    global song_branched
    global SelectedYet
    global BranchOption


    if(not SelectedYet):
        messagebox.showinfo('showinfo', TEXT_ROOT_MESSAGE_NOTSELECTED_BRANCH)
        return

    FumenOption = FumenOptionList.get()
    BranchOption = BranchOptionList.get()
    if(song_selected.IsBranchExist):
        song_branched = TaikoFumenBranched(file_path, Codec, int(FumenOption), int(BranchOption[0]))
    else:
        song_branched = TaikoFumenBranched(file_path, Codec, int(FumenOption), None)

    #按鈕狀態設定/其他類似的初始話動作
    GenFig_button.configure(state='active')     #重新選擇不同譜面後，重置生成圖片的按鈕
    shutil.rmtree("_figure", True)              #刪除如果上一個譜面有生成譜面的話會有的"_figure"資料夾
    canvas.delete('all')                        #刪除因上一個譜面的最後一個選擇而顯示在視窗的譜面圖

    ViewFigureOptionList.configure(state='disabled', values=[])
    ViewFigureOptionList.set("-")

    SaveFig_button.configure(state='disabled')
    zoom_button.configure(state="disabled")
    

    UpdateEveryResult()
    
def UpdateEveryResult():
    global song_branched
    global song_figure
    global NotesInfo        #各類音符數量
    global Extreme_ps       #最大最小密度
    global Rolls_info       #各類連打位置與對應種類
    global Roll_KickState   #各個連打所需打擊數
    global ViewFigureOptionList
    global ComplexWeighyDiff
    global factors          #預測星數用
    
    os.system('cls')        #清空窗口

    #當前譜面資訊
    TITLE.config(text=TEXT_ROOT_TITLE + " : " + song_branched.TITLE)
    COURSE.config(text=TEXT_ROOT_COURSE + " : " + song_branched.COURSE)
    DUAL.config(text=TEXT_ROOT_DUAL + " : " + str(song_branched.DUAL))
    LEVEL.config(text="★"+song_branched.LevelStar)
    BRANCH.config(text=TEXT_ROOT_BRANCH + " : " + str(song_branched.BRANCH))

    ActualLevel_value.config(text=str(song_branched.LevelStar))

    #譜面音符組成
    NotesInfo = song_branched.Get_NumberOfNotes()

    NotesNum_total_value.set(NotesInfo[0])
    NotesNum_d_value.set(NotesInfo[1])
    NotesNum_k_value.set(NotesInfo[2])
    NotesNum_Bd_value.set(NotesInfo[3])
    NotesNum_Bk_value.set(NotesInfo[4])

    #最大/最小/20%最大/20%最小/平均密度
    Extreme_ps = song_branched.FindExtremePeriod()
    Highest_density_value.set(round(1/Extreme_ps[0],3))
    Lowest_density_value.set(round(1/Extreme_ps[1],3))
    
    notesloaction = song_branched.FindEveryKindOfNotesLocation()
    result = song_branched.FindExtremeDensityByScanning(song_branched.Duration(notesloaction[0],notesloaction[-1])[0] * 0.2, DEFAULT_SCANRATE)
    Highest20_density_value.set(round(result[0],3))
    Lowest20_density_value.set(round(result[1],3))

    average_density = song_branched.DensityOfRegion()
    av_density_value.set(round(average_density,3))

    #譜面時間/使用延遲指令時間
    TimeInfo = song_branched.Duration()
    fumen_period_value.set(round(TimeInfo[0],3))
    delay_period_value.set(round(TimeInfo[1],3))


    #譜面平均視覺速度
    Seen_rootav = abs(song_branched.MultipliedRootOf("both"))
    SeenVel_rootav_value.set(round(Seen_rootav,3))

    #連打資訊
    Rolls_info = song_branched.Get_RollInformation()
    RollsNum=len(Rolls_info)
    if( RollsNum > 0):
        RollsOptionList.configure(values=list(range(RollsNum)), state="readonly")
    else:
        RollsOptionList.configure(values=[], state="disabled")
        RollType_value.set(TEXT_ROOT_MESSAGE_NOROLLEXIST)
    RollsOptionList.set("-")

    balloon_count = 0            #處理氣球或彩球的打擊數
    balloon_kick = song_branched.Get_BalloonKickNeeded()
    Roll_KickState = []
    for Roll in Rolls_info:
        match Roll[0]:
            case 5|6:
                Roll_KickState.append(TEXT_ROOT_NOTAVAILABLE)
            case 7|9:
                Roll_KickState.append(str(balloon_kick[balloon_count]) + TEXT_ROOT_DRUMHITS)
                balloon_count = balloon_count + 1

    #視速變化
    SeenVel_Changelevel = song_branched.SeenVelChangeFrequency(True, True, False)[0] - 1
    SeenVel_ChangeRate = song_branched.SeenVelChangeFrequency(True, True, True)[0]

    SeenVelChangeLevel_value.set(round(SeenVel_Changelevel*3, 3))
    SeenVelChangeRate_value.set(round(SeenVel_ChangeRate, 3))

    #換手權重
    ComplexWeighyDiff = song_branched.WeightResultOfComplex()

    #疑他
    RedPercent = (NotesInfo[1]+NotesInfo[3])/NotesInfo[0]
    factors = np.array([TimeInfo[0], RedPercent, average_density, result[0], result[1], 1/Extreme_ps[0], 1/Extreme_ps[1], Seen_rootav, SeenVel_Changelevel, SeenVel_ChangeRate, ComplexWeighyDiff])
    level_Compute_button.configure(state='active')


def GenerateFumenFigure():
    global FumenOption
    global BranchOption
    global img_path
    global song_figure

    if(song_selected.IsBranchExist):
        song_figure = TaikoFumenRealiztion(file_path, Codec, int(FumenOption), int(BranchOption[0]), DEFAULT_DPI)
    else:
        song_figure = TaikoFumenRealiztion(file_path, Codec, int(FumenOption), None, DEFAULT_DPI)

    song_figure.PlotAllNotes(True)
    plt.close('all')
    GenFig_button.configure(state="disabled")

    #譜面圖選項啟用
    ViewFigureOptionList.configure(state='readonly', values=list(range(1, len(song_branched.EveryBar) + 1)))
    ViewFigureOptionList.bind("<<ComboboxSelected>>", Update_ViewOption)
    ViewFigureOptionList.set("-")
    SaveFig_button.configure(state='active')

    img_path="-"

    #譜面圖放大啟用
    zoom_button.configure(state="active")
    
def SaveFumenFigure():
    dir = filedialog.askdirectory()
    if(dir==""): return
    FileList = os.listdir("_figure")
    for file in FileList: 
        shutil.copy("_figure/" + file, dir + "/" + file)

def ComputeLevel():
    global factors
    ch_ourse = level_course_OptionList.get()
    ch_refer = level_reference_OptionList.get()
    ch_model = level_model_OptionList.get()
    Prediction = pfl.PredictFumenLevel(factors, ch_ourse, ch_refer, ch_model)
    print(f"\n{TEXT_ROOT_TERMINAL_DETAILEDINFO}\t:{ch_ourse} / {ch_refer} / {ch_model} / {Prediction}",end='')
    PredictLevel_value.configure(text=round(Prediction, 3)) if (Prediction!=None) else PredictLevel_value.configure(text=TEXT_ROOT_NOTAVAILABLE)

ChooseBranch_btn = tk.Button(root, text=TEXT_ROOT_BRANCH, width=7, command=Ask_FinalFumen, state="disabled")          #同ChooseFumen_btn
ChooseBranch_btn.place(relx=0.01, rely=0.175, anchor='w')

#顯示選擇譜面時的基本資訊
COURSE_text = "-"
COURSE_value = tk.StringVar()              
COURSE_dis = tk.Entry(root, textvariable=COURSE_value, width=6, justify='center', state="readonly")
COURSE_dis.place(relx=0.295, rely=0.1, anchor='center')

DUAL_text = "-"
DUAL_value = tk.StringVar()              
DUAL_dis = tk.Entry(root, textvariable=DUAL_value, width=6, justify='center', state="readonly")
DUAL_dis.place(relx=0.395, rely=0.1, anchor='center')

LEVEL_text = "-"
LEVEL_value = tk.StringVar()              
LEVEL_dis = tk.Entry(root, textvariable=LEVEL_value, width=6, justify='center', state="readonly")
LEVEL_dis.place(relx=0.495, rely=0.1, anchor='center')

#顯示音符組成
Notes_composition = tk.Label(root, text=TEXT_ROOT_NOTESINFO_UPPER + '\n' + TEXT_ROOT_NOTESINFO_LOWER, relief='solid', borderwidth=0.5)
Notes_composition.place(relx=0.06, rely=0.313, width=58,anchor='center')

NotesNum_total_text = "-"
NotesNum_total_value = tk.StringVar()                              
NotesNum_total = tk.Label(root, text=TEXT_ROOT_TOTAL)
NotesNum_total.place(relx=0.045, rely=0.385, anchor='center')
NotesNum_total_dis = tk.Entry(root, textvariable=NotesNum_total_value, width=5, justify='center')
NotesNum_total_dis.place(relx=0.045, rely=0.435, anchor='center')

NotesNum_d_text = "-"
NotesNum_d_value = tk.StringVar()                               
NotesNum_d = tk.Label(root, text=TEXT_ROOT_NOTE1)
NotesNum_d.place(relx=0.14, rely=0.285, anchor='e')
NotesNum_d_dis = tk.Entry(root, textvariable=NotesNum_d_value, width=5, justify='center')
NotesNum_d_dis.place(relx=0.175, rely=0.285, anchor='center')

NotesNum_k_text = "-"
NotesNum_k_value = tk.StringVar()       
NotesNum_k = tk.Label(root, text=TEXT_ROOT_NOTE2)
NotesNum_k.place(relx=0.14, rely=0.335, anchor='e')
NotesNum_k_dis = tk.Entry(root, textvariable=NotesNum_k_value, width=5, justify='center')
NotesNum_k_dis.place(relx=0.175, rely=0.335, anchor='center')

NotesNum_Bd_text = "-"
NotesNum_Bd_value = tk.StringVar()   
NotesNum_Bd = tk.Label(root, text=TEXT_ROOT_NOTE3)
NotesNum_Bd.place(relx=0.14, rely=0.385, anchor='e')
NotesNum_Bd_dis = tk.Entry(root, textvariable=NotesNum_Bd_value, width=5, justify='center')
NotesNum_Bd_dis.place(relx=0.175, rely=0.385, anchor='center')

NotesNum_Bk_text = "-"
NotesNum_Bk_value = tk.StringVar()   
NotesNum_Bk = tk.Label(root, text=TEXT_ROOT_NOTE4)
NotesNum_Bk.place(relx=0.14, rely=0.435, anchor='e')
NotesNum_BK_dis = tk.Entry(root, textvariable=NotesNum_Bk_value, width=5, justify='center')
NotesNum_BK_dis.place(relx=0.175, rely=0.435, anchor='center')

#最低/最高密度
Density = tk.Label(root, text=TEXT_ROOT_EXTREME_DENSITY_UPPER + '\n' + TEXT_ROOT_EXTREME_DENSITY_LOWER, relief='solid', borderwidth=0.5)
Density.place(relx=0.3, rely=0.313, width=58,anchor='center')

Lowest_density_text = "-"
Lowest_density_value = tk.StringVar()                              
Lowest_density = tk.Label(root, text=TEXT_ROOT_LOWEST)
Lowest_density.place(relx=0.445, rely=0.285, anchor='e')
Lowest_density_dis = tk.Entry(root, textvariable=Lowest_density_value, width=7, justify='center')
Lowest_density_dis.place(relx=0.495, rely=0.285, anchor='center')
Lowest_density_unit = tk.Label(root, text='n/s')
Lowest_density_unit.place(relx=0.545, rely=0.285, anchor='w')

Highest_density_text = "-"
Highest_density_value = tk.StringVar()                              
Highest_density = tk.Label(root, text=TEXT_ROOT_HIGHEST)
Highest_density.place(relx=0.445, rely=0.335, anchor='e')
Highest_density_dis = tk.Entry(root, textvariable=Highest_density_value, width=7, justify='center')
Highest_density_dis.place(relx=0.495, rely=0.335, anchor='center')
Highest_density_unit = tk.Label(root, text='n/s')
Highest_density_unit.place(relx=0.545, rely=0.335, anchor='w')

Lowest20_density_text = "-"
Lowest20_density_value = tk.StringVar()                              
Lowest20_density = tk.Label(root, text=TEXT_ROOT_20LOWEST)
Lowest20_density.place(relx=0.445, rely=0.385, anchor='e')
Lowest20_density_dis = tk.Entry(root, textvariable=Lowest20_density_value, width=7, justify='center')
Lowest20_density_dis.place(relx=0.495, rely=0.385, anchor='center')
Lowest20_density_unit = tk.Label(root, text='n/s')
Lowest20_density_unit.place(relx=0.545, rely=0.385, anchor='w')

Highest20_density_text = "-"
Highest20_density_value = tk.StringVar()                              
Highest20_density = tk.Label(root, text=TEXT_ROOT_20HIGHEST)
Highest20_density.place(relx=0.445, rely=0.435, anchor='e')
Highest20_density_dis = tk.Entry(root, textvariable=Highest20_density_value, width=7, justify='center')
Highest20_density_dis.place(relx=0.495, rely=0.435, anchor='center')
Highest20_density_unit = tk.Label(root, text='n/s')
Highest20_density_unit.place(relx=0.545, rely=0.435, anchor='w')

#譜面時間/平均密度
av_density_text = "-"
av_density_value = tk.StringVar()                              
av_density = tk.Label(root, text=TEXT_ROOT_AVERAGEDENSITY)
av_density.place(relx=0.69, rely=0.285, anchor='center')
av_density_dis = tk.Entry(root, textvariable=av_density_value, width=9, justify='center')
av_density_dis.place(relx=0.615, rely=0.335, anchor='w')
av_density_unit = tk.Label(root, text='n/s')
av_density_unit.place(relx=0.731, rely=0.335, anchor='w')

delay_period_text = "-"
delay_period_value = tk.StringVar()                              
delay_period = tk.Label(root, text=TEXT_ROOT_TOTALDELAY)
delay_period.place(relx=0.69, rely=0.385, anchor='center')
delay_period_dis = tk.Entry(root, textvariable=delay_period_value, width=11, justify='center')
delay_period_dis.place(relx=0.615, rely=0.435, anchor='w')
delay_period_unit = tk.Label(root, text='s')
delay_period_unit.place(relx=0.752, rely=0.435, anchor='w')

fumen_period_text = "-"
fumen_period_value = tk.StringVar()                              
fumen_period = tk.Label(root, text=TEXT_ROOT_TOTALTIME)
fumen_period.place(relx=0.885, rely=0.385, anchor='center')
fumen_period_dis = tk.Entry(root, textvariable=fumen_period_value, width=16, justify='center')
fumen_period_dis.place(relx=0.785, rely=0.435, anchor='w')
fumen_period_unit = tk.Label(root, text='s')
fumen_period_unit.place(relx=0.988, rely=0.435, anchor='e')

#視覺均速
SeenVel_rootav_text = "-"
SeenVel_rootav_value = tk.StringVar()                              
SeenVel_rootav = tk.Label(root, text=TEXT_ROOT_AVERAGESEENSPEED)
SeenVel_rootav.place(relx=0.885, rely=0.285, anchor='center')
SeenVel_rootav_dis = tk.Entry(root, textvariable=SeenVel_rootav_value, width=12, justify='center')
SeenVel_rootav_dis.place(relx=0.785, rely=0.335, anchor='w')
fumen_period_unit = tk.Label(root, text='bpm')
fumen_period_unit.place(relx=0.988, rely=0.335, anchor='e')

#顯示連打資訊
Rolls_composition = tk.Label(root, text=TEXT_ROOT_ROLLSINFO_UPPER + '\n' + TEXT_ROOT_ROLLSINFO_LOWER, relief='solid', borderwidth=0.5)
Rolls_composition.place(relx=0.06, rely=0.563, width=58, height=38.5, anchor='center')
RollsOptionList = ttk.Combobox(root, width=2, height=5, values=[], justify='center', state="disabled")        #假譜面選擇框
RollsOptionList.bind("<<ComboboxSelected>>", Update_RollsOptions)
RollsOptionList.place(relx=0.145, rely=0.54, anchor='w')

RollType_text = "-"
RollType_value = tk.StringVar()              
RollType_dis = tk.Entry(root, textvariable=RollType_value, width=16, justify='center', state="readonly")
RollType_dis.place(relx=0.22, rely=0.54, anchor='w')

RollLast = "-"
RollLast= tk.Label(root, text=TEXT_ROOT_LASTFOR)
RollLast.place(relx=0.42, rely=0.54, anchor='w')
RollLast_value = tk.StringVar()              
RollLast_dis = tk.Entry(root, textvariable=RollLast_value, width=8, justify='center', state="readonly")
RollLast_dis.place(relx=0.51, rely=0.54, anchor='w')
RollLast_unit= tk.Label(root, text="s")
RollLast_unit.place(relx=0.61, rely=0.54, anchor='w')

Roll_location_text = "-"
Roll_location_beg = tk.Label(root, text=TEXT_ROOT_ROLLLOCATION)
Roll_location_beg.place(relx=0.145, rely=0.59, anchor='w')

Roll_location_beg_value = tk.StringVar()         
Roll_location_beg_dis = tk.Entry(root, textvariable=Roll_location_beg_value, width=9, justify='center', state="readonly")
Roll_location_beg_dis.place(relx=0.248, rely=0.59, anchor='w')

Roll_location_mid_text = "-"
Roll_location_mid = tk.Label(root, text='~')
Roll_location_mid.place(relx=0.36, rely=0.59, anchor='w')

Roll_location_end_value = tk.StringVar()                             
Roll_location_end_dis = tk.Entry(root, textvariable=Roll_location_end_value, width=9, justify='center', state="readonly")
Roll_location_end_dis.place(relx=0.39, rely=0.59, anchor='w')

Roll_kick_value = tk.StringVar()                             
Roll_kick_dis = tk.Entry(root, textvariable=Roll_kick_value, width=10, justify='center', state="readonly")
Roll_kick_dis.place(relx=0.51, rely=0.59, anchor='w')

#視速變化
SeenVelChangeLevel_text = "-"
SeenVelChangeLevel_value = tk.StringVar()                              
SeenVelChangeLevel = tk.Label(root, text=TEXT_ROOT_SEENVELOCITYCHANGE)
SeenVelChangeLevel.place(relx=0.64, rely=0.54, anchor='w')
SeenVelChangeLevel_dis = tk.Entry(root, textvariable=SeenVelChangeLevel_value, width=12, justify='center')
SeenVelChangeLevel_dis.place(relx=0.82, rely=0.54, anchor='w')
SeenVelChangeLevel_unit= tk.Label(root, text="%")
SeenVelChangeLevel_unit.place(relx=0.988, rely=0.54, anchor='e')

SeenVelChangeRate_text = "-"
SeenVelChangeRate_value = tk.StringVar()                              
SeenVelChangeRate = tk.Label(root, text=TEXT_ROOT_SEENVELOCITYCHANGERATE)
SeenVelChangeRate.place(relx=0.64, rely=0.59, anchor='w')
SeenVelChangeRate_dis = tk.Entry(root, textvariable=SeenVelChangeRate_value, width=8, justify='center')
SeenVelChangeRate_dis.place(relx=0.86, rely=0.59, anchor='w')
SeenVelChangeRate_unit= tk.Label(root, text="/s")
SeenVelChangeRate_unit.place(relx=0.988, rely=0.59, anchor='e')

#當前譜面基本資訊
TITLE = tk.Label(root, text=TEXT_ROOT_TITLE + ' : ?', font=('Arial', 8))
TITLE.place(relx=0.6, rely=0.1, anchor='w')

COURSE = tk.Label(root, text=TEXT_ROOT_COURSE + ' : ?', font=('Arial', 8))
COURSE.place(relx=0.6, rely=0.145, anchor='w')

DUAL = tk.Label(root, text=TEXT_ROOT_DUAL + ' : ?', font=('Arial', 8))
DUAL.place(relx=0.8, rely=0.145, anchor='w')

LEVEL = tk.Label(root, text='★?', font=('Arial', 8))
LEVEL.place(relx=0.6, rely=0.19, anchor='w')

BRANCH = tk.Label(root, text=TEXT_ROOT_BRANCH + ' : ?', font=('Arial', 8))
BRANCH.place(relx=0.775, rely=0.19, anchor='w')

#圖片生成
figure_gen = tk.Label(root, text=TEXT_ROOT_FUMENGEN_UPPER + '\n' + TEXT_ROOT_FUMENGEN_LOWER, relief='solid', borderwidth=0.5)
figure_gen.place(relx=0.064, rely=0.712, width=62, height=30, anchor='center')

def ShowFigure(img_path):    #https://steam.oxxostudio.tw/category/python/tkinter/open-and-show-image.html
    img = Image.open(img_path)           # 取得圖片路徑
    w, h = img.size                      # 取得圖片長寬
    img.thumbnail((60/h*w,60))                                              #等比縮小                              /m
    w, h = img.size                                                         #取得新的圖片長寬                       /m
    tk_img = ImageTk.PhotoImage(img)     # 轉換成 tk 圖片物件
    canvas.delete('all')                 # 清空 Canvas 原本內容

    canvas.config(scrollregion=(0,0,w,h))   # 改變捲動區域
    canvas.create_image(0, 0, anchor='nw', image=tk_img)   # 建立圖片
    canvas.tk_img = tk_img               # 修改屬性更新畫面

def ShowFigure_Seperate(img_path):
    if(img_path=="-"):return
    
    global width
    global height
    global tk_img_full

    WhichBar = int(ViewFigureOptionList.get())
    max_width = root.winfo_screenwidth()
    max_height = root.winfo_screenheight()

    img = Image.open(img_path)           # 取得圖片路徑
    w_fig, h_fig = img.size                      # 取得圖片長寬

    if(w_fig>max_width):
        img.thumbnail((max_width,h_fig*max_width/w_fig))                                              #等比縮小                              /m
        w_fig, h_fig = img.size    

    tk_img_full = ImageTk.PhotoImage(img) 

    figure = tk.Toplevel()   # 建立 tkinter 視窗至頂物件
    figure.grab_set()
    figure.iconbitmap('img/root.ico')  # 設定 icon ( 格式限定 .ico )
    figure.title(TEXT_ZOOMEDFIG_ZOOMIN)        # 設定標題

    frame_fig = tk.Frame(figure, width=w_fig, height=h_fig)
    frame_fig.place(relx=0.5, rely=0.5, anchor='center')

    sub_width = w_fig
    sub_height = h_fig
    sub_left = root.winfo_x() + round(width/2) - round(sub_width/2)
    if(sub_left < 0):
        sub_left = 0
    elif(sub_left + sub_width > max_width):
        sub_left = max_width - sub_width
    sub_top = root.winfo_y() + round(height/2) - round(sub_height/2)
    figure.geometry(f'{sub_width}x{sub_height}+{sub_left}+{sub_top}')  # 定義視窗的尺寸和位置

    canvas_fig = tk.Canvas(frame_fig, width=w_fig, height=h_fig, bg='#E0E0E0')
    canvas_fig.create_image(0, 0, anchor='nw', image=tk_img_full)   # 建立圖片
    canvas_fig.tk_img = tk_img_full
    canvas_fig.pack(side='left')

    #無法拉伸視窗
    figure.resizable(False, False)
    figure.mainloop()

GenFig_button = tk.Button(root, text=TEXT_ROOT_GENERATEFIG, command=GenerateFumenFigure, height=1, state='disabled')
GenFig_button.place(relx=0.012, rely=0.79, anchor='w', height=30)

SaveFig_button = tk.Button(root, text=TEXT_ROOT_SAVEFIG, command=SaveFumenFigure, height=1, state='disabled')
SaveFig_button.place(relx=0.988, rely=0.802, anchor='e', height=20)

frame = tk.Frame(root, width=450, height=60)
frame.place(relx=0.5, rely=0.75, anchor='center')

canvas = tk.Canvas(frame, width=450, height=60, bg='#E0E0E0')
scrollX = tk.Scrollbar(frame, orient='horizontal')
scrollX.place(relx=1, rely=1, width=35, anchor="se")
scrollX.config(command=canvas.xview)

canvas.config(xscrollcommand=scrollX.set)
canvas.pack(side='left')

ViewFigureOptionList = ttk.Combobox(root, height=5, values=[], justify='center', state="disabled")
ViewFigureOptionList.place(relx=0.988, rely=0.744, width=62, anchor='e')

ViewGuide = tk.Label(root, text=TEXT_ROOT_PICKBARTODISPLAY)
ViewGuide.place(relx=0.985, rely=0.693, anchor='e')

zoom_icon_raw = Image.open("img/zoom.png")  #圖片放大
zoom_icon_raw.thumbnail((12,12))     
zoom_icon = ImageTk.PhotoImage(zoom_icon_raw)
zoom_button = tk.Button(root, image=zoom_icon, command=lambda:ShowFigure_Seperate(img_path), state="disabled")
zoom_button.place(relx=0.843, rely=0.675)

#星數預測
level_predict = tk.Label(root, text=TEXT_ROOT_LEVELPREDICT_UPPER + '\n' + TEXT_ROOT_LEVELPREDICT_LOWER, relief='solid', borderwidth=0.5)
level_predict.place(relx=0.064, rely=0.93, width=62, height=35, anchor='center')

level_course = tk.Label(root, text=TEXT_ROOT_COURSEFORPREDICT)
level_course.place(relx=0.135, rely=0.905, anchor='w')
level_course_options = ["Oni/Edit", "Hard", "Normal", "Easy"]
level_course_OptionList = ttk.Combobox(root, height=5, values=level_course_options, justify='center', state="readonly")
level_course_OptionList.set("-")
level_course_OptionList.place(relx=0.225, rely=0.907, width=75, anchor='w', height=19)

level_reference = tk.Label(root, text=TEXT_ROOT_STANDARD)
level_reference.place(relx=0.365, rely=0.905, anchor='w')
level_reference_options = {"Oni/Edit"   :   ["AC14", "AC15.0", "wii4"], 
                           "Hard"       :   ["wii4"], 
                           "Normal"     :   ["wii4"],
                           "Easy"       :   ["wii4"],}
level_reference_OptionList = ttk.Combobox(root, height=5, values=[], justify='center', state="readonly")
level_reference_OptionList.set("-")
level_reference_OptionList.place(relx=0.475, rely=0.907, width=75, anchor='w', height=19)
def Set_LevelCourseOption_By_LevelRef(event):                  #連結不同難易度下可以對應的參考世代選擇
    choosen_level_course = level_course_OptionList.get()
    level_reference_OptionList.configure(values=list(level_reference_options[choosen_level_course]))
    level_reference_OptionList.set("-")
    level_model_OptionList.set("-")
level_course_OptionList.bind("<<ComboboxSelected>>", Set_LevelCourseOption_By_LevelRef)

level_model = tk.Label(root, text=TEXT_ROOT_MOEDL)
level_model.place(relx=0.136, rely=0.955, anchor='w')
level_model_options = []
level_model_OptionList = ttk.Combobox(root, height=5, width=50, values=[], justify='center', state="readonly")
level_model_OptionList.set("-")
level_model_OptionList.place(relx=0.225, rely=0.955, width=225, anchor='w', height=19)
def Set_LevelRefOption_By_LevelModel(event):                   #連結不同世代下可以對應的模型選擇
    choosen_level_course = level_course_OptionList.get()
    choosen_level_ref = level_reference_OptionList.get()
    match choosen_level_course, choosen_level_ref:
        case "Oni/Edit", "AC14":
            Models = [  "1 - 1 layer (Linear)", 
                        "2 - 1 layer (20 Sigmoids)", 
                        "3 - 1 layer (11 HardSigmoids)", 
                        "4 - 3 layers (Linear with ReLUs)", 
                        "5 - 4 layers (Linear with ReLUs)"  ]
        case "Oni/Edit", "AC15.0":
            Models = [  "1 - 1 layer (Linear)", 
                        "2 - 1 layer (20 Sigmoids)", 
                        "3 - 1 layer (11 HardSigmoids)", 
                        "4 - 2 layers (Linear with ReLUs)", 
                        "5 - 4 layers (Linear with ReLUs)"  ]
        case "Oni/Edit", "wii4":
            Models = [  "1 - 1 layer (Linear)", 
                        "2 - 1 layer (20 Sigmoids)", 
                        "3 - 1 layer (11 HardSigmoids)", 
                        "4 - 4 layers (Linear with ReLUs)", 
                        "5 - 11 layers (Linear with ReLUs)" ]
        case "Hard", "wii4":
            Models = ["1 - 1 layer (Linear)"]
        case "Normal", "wii4":
            Models = ["1 - 11 layers (Linear with ReLUs)"]
        case "Easy", "wii4":
            Models = ["1 - 1 layer (Linear)"]
        case _:
            Models = []
    level_model_OptionList.configure(values=Models)
    level_model_OptionList.set("-")
level_reference_OptionList.bind("<<ComboboxSelected>>", Set_LevelRefOption_By_LevelModel)


level_Compute_button = tk.Button(root, text=TEXT_ROOT_RUNPREDICT, command=ComputeLevel, height=1, state='disabled')
level_Compute_button.place(relx=0.63, rely=0.982, anchor='s', height=40)

ActualLevel = tk.Label(root, text=TEXT_ROOT_ACTUALLEVEL, font=('Arial', 8))
ActualLevel.place(relx=0.681, rely=0.96, anchor='w')
ActualLevel_value = tk.Label(root, text='?', font=('Arial', 8))
ActualLevel_value.place(relx=0.8, rely=0.96, anchor='w')

PredictLevel = tk.Label(root, text=TEXT_ROOT_PREDICTLEVEL, font=('Arial', 8))
PredictLevel.place(relx=0.681, rely=0.907, anchor='w')
PredictLevel_value = tk.Label(root, text='?', font=('Arial', 8))
PredictLevel_value.place(relx=0.8, rely=0.907, anchor='w')

M = tk.Label(root, text='By\nM22543105', font=('Courier', 8, 'bold'), justify='right', fg='grey')
M.place(relx=0.988, rely=0.94, anchor='e')

ONI_Model = {}

#主選單
menubar = tk.Menu(root)               # 建立主選單

filemenu = tk.Menu(menubar)           # 建立子選單，選單綁定 menubar 主選單
filemenu.add_command(label=TEXT_ROOT_MENU_OPEN, command=Ask_forfile)    # 子選單項目
filemenu.add_command(label=TEXT_ROOT_MENU_SETTING, command=CreateSettingWindow)    # 子選單項目
menubar.add_cascade(label=TEXT_ROOT_MENU_OPTION, menu=filemenu)   # 建立主選單，內容為子選單

root.config(menu=menubar)             # 主視窗加入主選單

#無法拉伸視窗
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", plt.close("all"))     #solved by Copilot  /   在關掉tkinter視窗的時候，關閉所有matplotlib,pyplot所畫的圖

root.mainloop()  # 放在主迴圈中

shutil.rmtree("_figure", True)
WriteConfig("config.ini", "SELF", "open", "1")