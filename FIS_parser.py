# -*- coding: utf-8 -*-
#https://github.com/shinyeoeun/RPA_Tools_pakage/blob/master/Scripts/LogParser/LINE_api_logParser.py
#https://hongku.tistory.com/338

import sys
from parse import *
from parse import compile

import sys
from PyQt5.QtWidgets import *

import time
now = time


'''
Vantage 설비 작업위치 파악 시 BF 줄이기 위한
로더 부 FIS 로그 파일 통한 작업 위치 파악 Log parser
'''

'''
[LOG SAMPLE]
2020-03-24 17:32:45(pid=14069,tid=1354) : TalkApi (D) : [res][id=170997684] sendChatChecked[elapsed=55ms] result=Success[null]
[01:50:24] FIS[1]->LDM : [WorkpieceComplete]WorkpieceID : S907891A070802560, Lane : 1, Result : 398025684,Time : 
[02:00:00] AOI[0]->LDM : [WorkpieceComplete]WorkpieceID : S907891A070800134, Lane : 1, Result : 442512324,Time : 
'''
 
 #CSV 추출 용 헤더
def get_csv_header():
    return "TIME,PCBID,DISPENSER,LANE"


#로그 파싱
def parse(line):

    # LOG에서 추출하고자 하는 값이 포함된 문자열 존재여부 확인. 
    if line.find("[WorkpieceComplete]") == -1:
        return

    # LOG 표시시각 취득
    time = line[1:9]

    # 추출대상 값들을 Parser의 {:w}로 파싱 > 각 값들은 배열로 반환됨
    result = search("FIS[{:w}]->LDM : [WorkpieceComplete]WorkpieceID : {:w}, Lane : {:w}", line)
   
  
    #result = search("[{:w}][id={:w}] {:w}[elapsed={:w}ms] result={:w}", line)

    # 파싱결과값들을 CSV형식으로 편집
    if result:
        data = time + "," + str(result[1]) + "," + result[0] + "," + result[2] + "\n"
        return data

    # 파싱에 실패한 라인 출력
    print("Error >> ".format(line))
    return

def write_csv(input_file, output_file):
    # csv파일 작성
    csv_name = output_file
    csv = open(csv_name, 'w', encoding='utf-8')

    # csv 헤더 작성
    csv_head = get_csv_header() + "\n"
    csv.write(csv_head)

    # 로그파일 파싱 및 csv파일에 기록
    with open(input_file, 'r', encoding='utf-8') as log:

        while True:
            # 로그 라인 존재여부 확인
            line = log.readline()
            if not line: break

            # 해당 라인에 파싱 키워드 존재여부 확인
            csv_data = parse(line)
            if csv_data:

                while True:
                    line = log.readline()
                    if not line: break

                    # csv 기록
                    value = parse(line)
                    if value:
                        csv_data += value
                        csv.write(csv_data)
                        break

    csv.close()
    print('    ====== End ======')
    print('    >> Intput={}'.format(input_file))
    print('    >> Outputs={}'.format(csv_name))
    return


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
 
    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle('FIS Log Parser')
 
        self.pushButton = QPushButton('Please FIS Log Open')
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.label = QLabel()
        self.label2 = QLabel() 
 
        layout = QVBoxLayout()
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)
        layout.addWidget(self.label2)

        self.setLayout(layout)
 
    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self, "FIS Log 파일을 열어주세요",'D:\PROJECT\LoadUnloader\History\FIS')
        #fname=QFileDialog.getOpenFileName(self,"FIS Log 파일을 열어주세요",'D:/ubuntu/disks','Text File(*.txt);; PPtx file(*ppt *pptx)' )
        outputpath = QFileDialog. getExistingDirectory(self,"파싱 결과를 저장할 위치 골라주세요")
        
        add_csv = "/"+now.strftime('%m%d %H%M%S')+"_result.csv"
        outputpath = outputpath + add_csv
        write_csv(fname[0], outputpath)
       
        self.label.setText("불러온 Log 입니다. :"+fname[0])
        self.label2.setText("파싱 결과 저장한 위치입니다. :"+outputpath)
 
if __name__=='__main__':
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()
    app.exec_()
