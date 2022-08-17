## function searchBluePerson
##スクリーンショットをとって指定の矩形から青の矩形領域を取得する


import pyautogui as gui
import sys
import time
import cv2
import speech_recognition as sr

SAY_FLG_NONE = 1
SAY_FLG_CAMERA_UP = 2
SAY_FLG_CAMERA_DOWN = 3
SAY_FLG_CAMERA_LEFT = 4
SAY_FLG_CAMERA_LEFTUP = 5
SAY_FLG_CAMERA_LEFTDOWN = 6
SAY_FLG_CAMERA_RIGHT = 7
SAY_FLG_CAMERA_RIGHTUP = 8
SAY_FLG_CAMERA_RIGHTDOWN = 9
SAY_FLG_MOVE_NORTH = 10
SAY_FLG_MOVE_SOUTH = 11
SAY_FLG_MOVE_WEST = 12
SAY_FLG_MOVE_EAST = 13
SAY_FLG_MOVE_FORWARD = 14
SAY_FLG_MOVE_BACKWARD = 15

parse1_point = [86, 335]
parse2_point = [117,333]

mitorizu_lect = [399, 361, 1323, 498]

g_width = 320;
g_height = 240;

g_dw_c_x = 811
g_dw_c_y = 635

#カメラのサイズを適宜変更して処理速度を調整
g_width2 = 100;
g_height2 = 100;

out_img = cv2.imread("C:\\Users\hogehoge\\white.jpg");
out_img = cv2.resize(out_img, (g_width2, g_height2))


timeStart = 0
timeEnd = 0
spanTime = 0

args = sys.argv

print(len(sys.argv))

if len(args) < 2:
 exit()
 
#差分判定率
DiffJudgePercent = float(args[1])

# VideoCapture オブジェクトを取得します
g_capture = cv2.VideoCapture(0)

print(g_capture.set(cv2.CAP_PROP_FRAME_WIDTH, g_width2))
print(g_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, g_height2)) 


ExecFlg = SAY_FLG_NONE;
PrevZahyoIdoFlg = False;


def calcWhiteRate(img1):

    global g_width2
    global g_height2
    
    WCount = 0
    
    for x in range(0, g_width2) :
         for y in range(0, g_height2) :
             
             if ( img1[y, x, 0] == 255 and
                  img1[y, x, 1] == 255 and
                  img1[y, x, 2] == 255 ) :
                    WCount = WCount+1
    
    WRate = WCount / (g_width2 * g_height2)
    WRate = WRate * 100.0
    
    return WRate

def Diff(img1, img2):
    
    global g_width
    global g_height
    global out_img

    for x in range(0, g_width2) :
         for y in range(0, g_height2) :
            if img1[y, x, 0] >= img2[y, x, 0]:
                out_img[y, x, 0] = abs(img1[y, x, 0] - img2[y, x, 0]);
            else:
                out_img[y, x, 0] = abs(img2[y, x, 0] - img1[y, x, 0]);

            if img1[y, x, 1] >= img2[y, x, 1]:
                out_img[y, x, 1] = abs(img1[y, x, 1] - img2[y, x, 1]);
            else:
                out_img[y, x, 1] = abs(img2[y, x, 1] - img1[y, x, 1]);

            if img1[y, x, 2] >= img2[y, x, 2]:
                out_img[y, x, 2] = abs(img1[y, x, 2] - img2[y, x, 2]);
            else:
                out_img[y, x, 2] = abs(img2[y, x, 2] - img1[y, x, 2]);

            absSum = int(out_img[y, x, 0]) + int(out_img[y, x, 1]) + int(out_img[y, x, 2])
            if absSum >= 120:
                    out_img[y, x, 0] = 255
                    out_img[y, x, 1] = 255
                    out_img[y, x, 2] = 255
            else:
                    out_img[y, x, 0] = 0
                    out_img[y, x, 1] = 0
                    out_img[y, x, 2] = 0
                    
    return out_img

    

def searchBluePerson(LeftUpX, LeftUpY, RightDownX, RightDownY, img):

    leftUpBlue = [9999, 9999];
    rightDownBlue = [0, 0];
    
    
    min_x = 9999
    max_x = 0
    min_y = 9999
    max_y = 0
    
    for x in range(RightDownX - LeftUpX):
        for y in range(RightDownY - LeftUpY):
        
            
            r, g, b = img.getpixel((x+LeftUpX, y+LeftUpY))
            if b >= 150 and g <= 100 and r <= 100:
                if x+LeftUpX <= min_x:
                    min_x = x+LeftUpX
                elif x+LeftUpX >= max_x:
                    max_x = x+LeftUpX
                    
                if y+LeftUpY <= min_y:
                    min_y = y+LeftUpY
                elif y+LeftUpY >= max_y:
                    max_y = y+LeftUpY


    leftUpBlue = [min_x, min_y]
    rightDownBlue = [max_x, max_y]
                
    return leftUpBlue, rightDownBlue


def CameraMoveLeft():
    global PrevZahyoIdoFlg
    global g_dw_c_x
    global g_dw_c_y

    drag_x = 5
    drag_y = 5
    
    print("eee")    

    gui.mouseDown(g_dw_c_x, g_dw_c_y,button='left')
    gui.dragTo(g_dw_c_x - drag_x , g_dw_c_y,1)
    gui.mouseUp(g_dw_c_x - drag_x, g_dw_c_y, button='left')
    
    PrevZahyoIdoFlg = False
    
    return

def CameraMoveLeftUp():
    global PrevZahyoIdoFlg
    global g_dw_c_x
    global g_dw_c_y
    drag_x = 5
    drag_y = 5

    gui.mouseDown(g_dw_c_x, g_dw_c_y,button='left')
    gui.dragTo(g_dw_c_x - drag_x , g_dw_c_y - drag_y,1)
    gui.mouseUp(g_dw_c_x - drag_x, g_dw_c_y - drag_y, button='left')

    PrevZahyoIdoFlg = False
    
    return
    
def CameraMoveLeftDown():
    global PrevZahyoIdoFlg
    global g_dw_c_x
    global g_dw_c_y

    drag_x = 5
    drag_y = 5


    gui.mouseDown(g_dw_c_x, g_dw_c_y,button='left')
    gui.dragTo(g_dw_c_x - drag_x , g_dw_c_y + drag_y,1)
    gui.mouseUp(g_dw_c_x - drag_x, g_dw_c_y + drag_y, button='left')
    
    PrevZahyoIdoFlg = False
    
    return
    
def CameraMoveRight():
    global PrevZahyoIdoFlg
    global g_dw_c_x
    global g_dw_c_y

    drag_x = 5
    drag_y = 5

    gui.mouseDown(g_dw_c_x, g_dw_c_y,button='left')
    gui.dragTo(g_dw_c_x + drag_x , g_dw_c_y,1)
    gui.mouseUp(g_dw_c_x + drag_x, g_dw_c_y, button='left')
    
    PrevZahyoIdoFlg = False
    
    return
    
def CameraMoveRightUp():
    global PrevZahyoIdoFlg
    global g_dw_c_x
    global g_dw_c_y

    drag_x = 5
    drag_y = 5

    gui.mouseDown(g_dw_c_x, g_dw_c_y,button='left')
    gui.dragTo(g_dw_c_x + drag_x , g_dw_c_y - drag_y,1)
    gui.mouseUp(g_dw_c_x + drag_x, g_dw_c_y - drag_y, button='left')
    
    PrevZahyoIdoFlg = False
    
    return

def CameraMoveRightDown():
    global PrevZahyoIdoFlg
    global g_dw_c_x
    global g_dw_c_y

    drag_x = 5
    drag_y = 5

    gui.mouseDown(g_dw_c_x, g_dw_c_y,button='left')
    gui.dragTo(g_dw_c_x + drag_x , g_dw_c_y + drag_y,1)
    gui.mouseUp(g_dw_c_x + drag_x, g_dw_c_y + drag_y, button='left')
    
    PrevZahyoIdoFlg = False
    
    return    

def CameraMoveUp():
    global PrevZahyoIdoFlg
    global g_dw_c_x
    global g_dw_c_y

    drag_x = 5
    drag_y = 5

    gui.mouseDown(g_dw_c_x, g_dw_c_y,button='left')
    gui.dragTo(g_dw_c_x, g_dw_c_y - drag_y,1)
    gui.mouseUp(g_dw_c_x, g_dw_c_y - drag_y, button='left')
    
    PrevZahyoIdoFlg = False
    
    return

def CameraMoveDown():
    global PrevZahyoIdoFlg
    global g_dw_c_x
    global g_dw_c_y

    drag_x = 5
    drag_y = 5

    gui.mouseDown(g_dw_c_x, g_dw_c_y,button='left')
    gui.dragTo(g_dw_c_x, g_dw_c_y + drag_y,1)
    gui.mouseUp(g_dw_c_x, g_dw_c_y + drag_y, button='left')
    
    PrevZahyoIdoFlg = False
    
    return

def ZahyoMoveForward():
    global PrevZahyoIdoFlg
    global g_dw_c_x
    global g_dw_c_y
    
    gui.click(g_dw_c_x, g_dw_c_y)
    gui.press('up')
    
    PrevZahyoIdoFlg = False
    
    
    return
    
def ZahyoMoveBackward():
    global PrevZahyoIdoFlg
    global g_dw_c_x
    global g_dw_c_y 
    
    gui.click(g_dw_c_x, g_dw_c_y)
    gui.press('down')
    
    PrevZahyoIdoFlg = False
    
    
    return
    
def SelectBluePerson():
    global PrevZahyoIdoFlg
    
    if PrevZahyoIdoFlg == False:
        gui.click(parse1_point[0], parse1_point[1])
    
    gui.click(parse2_point[0], parse2_point[1])
    
    screen_shot = gui.screenshot()
    leftUpPt, rightDownPt = searchBluePerson(mitorizu_lect[0], mitorizu_lect[1], mitorizu_lect[2], mitorizu_lect[3], screen_shot)

    
    cx = int( ((leftUpPt[0] + rightDownPt[0])/2) )
    cy = int( ((leftUpPt[1] + rightDownPt[1])/2) )
    
    gui.click(cx, cy)
    
    return
    
def ZahyoMoveNorth():
    global PrevZahyoIdoFlg
    
    SelectBluePerson()
    gui.press('up')
    PrevZahyoIdoFlg = True
    return
    
def ZahyoMoveSouth():
    global PrevZahyoIdoFlg
        
    SelectBluePerson()
    gui.press('down')
    PrevZahyoIdoFlg = True    
    return
    
def ZahyoMoveWest():
    global PrevZahyoIdoFlg
        
    SelectBluePerson()
    gui.press('left')
    PrevZahyoIdoFlg = True
    return
    
def ZahyoMoveEast():
    global PrevZahyoIdoFlg
        
    SelectBluePerson()
    gui.press('right')
    PrevZahyoIdoFlg = True
    return

def getSayWord(q_text):
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        print(q_text)
        audio = r.listen(source)

    text = r.recognize_google(audio, key=None, language='ja-JP')

    print("発話文:"+text)
    
    return text

print("start3")

def selectFlg(text):

    flg = SAY_FLG_NONE
    
    if text.find("カメラ") != -1:
        if text.find("上") != -1 or text.find("アップ") != -1:
            if text.find("右") != -1:
                flg = SAY_FLG_CAMERA_RIGHTUP;

            elif text.find("左") != -1:
                flg = SAY_FLG_CAMERA_LEFTUP;
                    
            else:
                flg = SAY_FLG_CAMERA_UP;
                    
        elif text.find("下") != -1 or text.find("ダウン") != -1:
            if text.find("右") != -1:
                flg = SAY_FLG_CAMERA_RIGHTDOWN;
                    
            elif text.find("左") != -1:
                flg = SAY_FLG_CAMERA_LEFTDOWN;
                    
            else:
                flg = SAY_FLG_CAMERA_DOWN

        elif text.find("右") != -1:
            flg = SAY_FLG_CAMERA_RIGHT;
        
        elif text.find("左") != -1:
            flg = SAY_FLG_CAMERA_LEFT;
                
        elif text.find("アップ") != -1:
            flg = SAY_FLG_CAMERA_UP;

        elif text.find("ダウン") != -1:
            flg = SAY_FLG_CAMERA_DOWN;

    elif text.find("移動") != -1 or text.find("異動") != -1:

        if text.find("北") != -1:
            flg = SAY_FLG_MOVE_NORTH
            
        elif text.find("南") != -1 or text.find("みなみ") != -1:
            flg = SAY_FLG_MOVE_SOUTH
            
        elif text.find("西") != -1:
            flg = SAY_FLG_MOVE_WEST
                
        elif text.find("東") != -1:
            flg = SAY_FLG_MOVE_EAST
        
        elif text.find("前") != -1:
            flg = SAY_FLG_MOVE_FORWARD

        elif text.find("後") != -1:
            flg = SAY_FLG_MOVE_BACKWARD
    
    
    return    flg


def Play():

    global g_capture
    global g_width
    global g_height

    global out_img
    global WalkFlg
    global DiffJudgePercent
    
    global MatchCount
    global ExecFlg
    
    timeStart = 0.0
    timeEnd = 0.0
    spanTime = 0.0
    timeSpan = 0.1;

    StopCount = 0
    
    ExecFlg = SAY_FLG_NONE
    
    breakFlg = False;
    WalkFlg = False;
    while True:
        print("qを押して終了")

        ret, frame = g_capture.read()
        img1 = frame;

        cv2.imshow('frame', frame)
        
        while WalkFlg == False:
            text1 = getSayWord("何か発話してください(「終了」で終了)")
            if text1.find("終") != -1:
                breakFlg = True;
                break
            text2 = getSayWord("以下の発話でよい場合は「OK」と言ってください(「もう一度」でもう一度発話")
            
            if text2.find("OK") != -1 :
                WalkFlg = True;
                ExecFlg = selectFlg(text1)
                time.sleep(5)
                print("aaa")
                break
                
        
        if breakFlg == True:
            break
        execute(ExecFlg)
        str1 = cv2.waitKey(1)
                
        if str1 == ord("q"):
            break
            
        currentTime = time.time()
        if timeStart == 0:
            timeStart = time.time()
            timeEnd = time.time()
            img2 = img1
            
        else:
            timeEnd = time.time()
            
        timeDiff = timeEnd - timeStart
        
        if(timeDiff >= timeSpan):
            img3 = Diff(img1, img2)
            WRate = calcWhiteRate(img3)
            print(WRate)
            if WRate >= DiffJudgePercent:
                StopCount = 0
                WalkFlg = True
                print("walkFlg:True");
                
            else:
                if StopCount >= 3:
                    WalkFlg = False
                    StopCount = 0
                else:
                    StopCount = StopCount + 1
                    
                print("walkFlg:False")

            timeStart = currentTime
       
        img2 = img1
    
    g_capture.release()

    cv2.destroyAllWindows()
    
    return

def execute(ExecFlg):

    if SAY_FLG_NONE == ExecFlg:
        return
    elif SAY_FLG_CAMERA_UP == ExecFlg:
        CameraMoveUp()
        
    elif SAY_FLG_CAMERA_DOWN == ExecFlg:
        CameraMoveDown()
        
    elif SAY_FLG_CAMERA_LEFT == ExecFlg: 
        CameraMoveLeft()
        
    elif SAY_FLG_CAMERA_LEFTUP == ExecFlg:
        CameraMoveLeftUp()
        
    elif SAY_FLG_CAMERA_LEFTDOWN == ExecFlg:
        CameraMoveLeftDown()
        
    elif SAY_FLG_CAMERA_RIGHT == ExecFlg:
        CameraMoveRight()
        
    elif SAY_FLG_CAMERA_RIGHTUP == ExecFlg:
        CameraMoveRightUp()
        
    elif SAY_FLG_CAMERA_RIGHTDOWN == ExecFlg:
        CameraMoveRightDown()
        
    elif SAY_FLG_MOVE_NORTH == ExecFlg:
        ZahyoMoveNorth()
        
    elif SAY_FLG_MOVE_SOUTH == ExecFlg:
        ZahyoMoveSouth()
        
    elif SAY_FLG_MOVE_WEST == ExecFlg:
        ZahyoMoveWest()
        
    elif SAY_FLG_MOVE_EAST == ExecFlg:
        ZahyoMoveEast()
        
    elif SAY_FLG_MOVE_FORWARD == ExecFlg:
        ZahyoMoveForward()
        
    elif SAY_FLG_MOVE_BACKWARD == ExecFlg:
        ZahyoMoveBackward()
        
    return

def main(): 

    Play()


    return 0
   

    
        
main()

    