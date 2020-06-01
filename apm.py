
"""
    Army Personal Management

        2020-06-01
        Lee JungHyeok
        
        이 프로그램은 아래와 같은 기능을 수행합니다.

        - Excel 파일에 병사 신상 저장 및 수정
        
        - 모든 병사 신상 조회
        - 모든 병사 신상 및 휴가 조회
        - 병사 신상 추가
        - 병사 신상 수정
        - 병사 휴가 조회
        - 병사 휴가 추가
        - 병사 휴가 사용
        - 모든 병사 휴가 추가
        - 프로그램을 종료하지 않고 저장
        - 저장 후 프로그램 종료

        - 병사 신상 정보:
            이름
            군번
            계급
            소대
            분대
            입대일
            전역일
            휴가

        추가될 기능

        - 휴가 수정
        - 휴가자 현황
        - 전역한 병사의 신상 삭제
        - 로그인 시스템
                
"""

import pandas as pd
import time

soldiers = []
excel_file = 'files/3corps_soldiers.xlsx'
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')


class soldier():

    """
        
        병사 클래스입니다.
        
    """
    
    def __init__(self, name, armyCode, rank, platoon, squad, indate, outdate):
        self.name = name
        self.armyCode = armyCode
        self.rank = rank
        self.platoon = platoon
        self. squad = squad
        self.indate = indate
        self.outdate = outdate
        self.furlough = []
        soldiers.append(self)
        
    def printFurlough(self):

        """
        
            soldier 객체가 사용하는 보유한 휴가를 print하는 함수입니다.
            만기일이 전역날을 넘길 시, 사용은 전역날 까지로 print됩니다.
        
        """
        if len(self.furlough) != 0:
            print('\n', len(self.furlough), "개의 휴가가 있습니다.\n\n")
            for furlough_tmp in self.furlough:
                print('-----', self.furlough.index(furlough_tmp)+1,'-----\n')
                print('휴가 종류:', furlough_tmp.type)
                if furlough_tmp.term == 1:
                    print('기간: 하루')
                else:
                    print('기간: ', furlough_tmp.term-1, '박', furlough_tmp.term, '일')
                furlough_tmp_dateS = time.strptime(furlough_tmp.date, "%Y-%m-%d")
                
                tmpDeadlineM = furlough_tmp_dateS.tm_mon + furlough_tmp.deadline
                if tmpDeadlineM > 12:
                    tmpDeadlineM -=12
                    tmpDeadlineY = furlough_tmp_dateS.tm_year + 1
                else:
                    tmpDeadlineY = furlough_tmp_dateS.tm_year
                tmpDeadlineD = furlough_tmp_dateS.tm_mday
                tmpDeadline = str(tmpDeadlineY) + '-' + str(tmpDeadlineM) + '-' + str(tmpDeadlineD)
                furlough_tmp_deadlineS = time.strptime(tmpDeadline, "%Y-%m-%d")

                outdateS = time.strptime(self.outdate, "%Y-%m-%d")
                if time.mktime(furlough_tmp_deadlineS) > time.mktime(outdateS):
                    furlough_tmp_deadlineS = outdateS
                
                print('받은 날짜: ', furlough_tmp_dateS.tm_year, '년', furlough_tmp_dateS.tm_mon, '월', furlough_tmp_dateS.tm_mday, '일')
                    
                print('사용기한: ', furlough_tmp_deadlineS.tm_year, '년', furlough_tmp_deadlineS.tm_mon, '월', furlough_tmp_deadlineS.tm_mday, '일', end=' 까지\n\n')
            return 1
        else:
            print(self.name, "는 휴가가 없습니다.")
            return 0
class furlough():

    """
        
        휴가 클래스입니다.
        
    """
    
    def __init__(self, typ, term, date, deadline):
        self.type = typ
        self.term = term
        self.date = date
        self.deadline = deadline

def login():

    """

        로그인 시스템입니다.
        아직 구현 전입니다.
    
    """
    
    permission = False

    
    
    return permission

def loadSoldiers():

    """

        불러온 Excel(xlsx) 파일에 있는 병사들의 정보를 불러옵니다.
        불러온 병사의 정보는 각 병사마다 하나의 soldier 객체로 생성되어 soldiers 배열에 들어갑니다.
        불러온 휴가 정보는 furlough 객체로 생성되고, 휴가를 소지한 병사의 furlough attribute에 append됩니다.
    
    """
    
    dataSoldiers = pd.read_excel(excel_file, 0, 0)
    for sol in dataSoldiers.values:
        if (str(sol[0]) != 'nan'):
            if (str(sol[0]) != ''):
                tmp_sol = soldier(sol[0], sol[1], int(sol[2]), sol[3], int(sol[4]), sol[5], sol[6])
        elif (sol[1] == '휴가'):
            tmp_fur = furlough(sol[2], int(sol[3]), sol[4], sol[5])
            tmp_sol.furlough.append(tmp_fur)

def findSoldier_ac(armyCode):

    """

        군번을 인수로 받아 soldiers 배열에 있는 객체들의 armyCode attribute와 비교합니다.
        armyCode가 일치하는 soldier 객체가 있으면 해당 객체를, 일치하는 soldier가 없으면 0을 return합니다.
    
    """
    
    result = 0
    for sol in soldiers:
        if sol.armyCode == armyCode:
            result = sol
    if result == 0:
        print(armyCode, "군번에 맞는 병사를 찾을 수 없습니다.")
    return result

def showSoldiers():

    """

        모든 병사의 신상을 print합니다.
        배열 soldiers에 있는 객체들의 attributes를 print합니다.
    
    """
    
    if len(soldiers) != 0:
        for sol in soldiers:
            print(sol.platoon, '소대', sol.squad, '분대')
            if sol.rank == 1:
                print('이병', end=' ')
            elif sol.rank == 2:
                print('일병', end=' ')
            elif sol.rank == 3:
                print('상병', end=' ')
            elif sol.rank == 4:
                print('병장', end=' ')
            print(sol.name)
            print('군번: ', sol.armyCode)
            print('입대일: ', sol.indate)
            print('전역일: ', sol.outdate, end='\n\n')
        print("\n총계: ", len(soldiers))
    else:
        print("부대에 병사가 없습니다.")
        
def showSoldiersFurlough():

    """

        모든 병사의 신상과 휴가를 print합니다.
        배열 soldiers에 있는 객체들의 정보 및 해당 병사의 휴가를 soldier.printFurlough()를 이용해 print합니다.
    
    """
    
    if len(soldiers) != 0:
        for sol in soldiers:
            print(sol.platoon, '소대', sol.squad, '분대')
            if sol.rank == 1:
                print('이병', end=' ')
            elif sol.rank == 2:
                print('일병', end=' ')
            elif sol.rank == 3:
                print('상병', end=' ')
            elif sol.rank == 4:
                print('병장', end=' ')
            print(sol.name)
            print('군번: ', sol.armyCode)
            print('입대일: ', sol.indate)
            print('전역일: ', sol.outdate, end='\n\n')
            sol.printFurlough()
            print('\n')
            
        print("\n총계: ", len(soldiers))
    else:
        print("부대에 병사가 없습니다.")

def addSoldier():

    """

        soldiers에 새로운 병사를 한 명 추가합니다.
        soldier의 attributes를 입력받아 새 soldier 객체를 생성합니다.
    
    """
    
    print("병사를 추가합니다. 정보를 입력하세요.\n")
    name = input("이름: ")
    armyCode = input("군번: ")
    while 1:
        rank = int(input("계급(1~4): "))
        if (rank > 0) and (rank< 5):
            break
        else:
            print("잘못된 입력입니다.")
    while 1:
        print("1: 본부")
        print("2: 경비")
        print("3: 수송")
        print("4: 군악")
        plat = int(input("소대: "))
        if plat == 1:
            platoon = "본부"
            break
        elif plat == 2:
            platoon = "경비"
            break
        elif plat == 3:
            platoon = "수송"
            break
        elif plat == 4:
            platoon = "군악"
            break
        else:
            print("잘못된 입력입니다.")
    squad = input("분대: ")
    indate = input("입대일: ")
    outdate = input("전역일: ")
    soldier(name, armyCode, rank, platoon, squad, indate, outdate)

def addFurlough(sol):

    """

        한 병사에게 휴가를 부여합니다.
        soldier class를 인수로 받고 입력받은 휴가를 furlough class로 만들어 해당 객체의 furlough attribute에 추가합니다.
    
    """
    
    print(sol.platoon, sol.name, "에게 추가할 휴가의 정보를 입력하세요.")
    typ = input("휴가 종류: ")
    term = int(input("휴가 기간: "))
    date = input("받은 날짜: ")
    if typ[-4:len(typ)] != "위로휴가":
        deadline = int(input("사용 기한: "))
    else:
        deadline = 18
    furlough_tmp = furlough(typ, term, date, deadline)
    sol.furlough.append(furlough_tmp)
    print("휴가가 추가되었습니다.")

def addFurloughAll():

    """

        모든 병사에게 휴가를 부여합니다.
        입력받은 휴가를 furlough class로 만들어 soldiers의 모든 soldier 객체의 furlough attribute에 추가합니다.
    
    """
    
    print("모든 병사에게 추가할 휴가를 입력하세요.")
    typ = input("휴가 종류: ")
    term = int(input("휴가 기간: "))
    date = input("받은 날짜: ")
    if typ[-4:len(typ)] != "위로휴가":
        deadline = int(input("사용 기한: "))
    else:
        deadline = 18
    furlough_tmp = furlough(typ, term, date, deadline)
    for sol in soldiers:
        sol.furlough.append(furlough_tmp)
    print("모든 병사에게 휴가를 추가하였습니다.")

def useFurlough(sol):

    """

        한 병사의 휴가를 사용합니다. 현재로선 삭제와 같습니다.(2020-05-31)
        soldier class를 인수로 받고 입력받은 휴가 번호에 해당하는 furlough class를 soldier.furlough 배열에서 삭제합니다.
    
    """
    
    if sol.printFurlough() == 0:
        return 0
    index_fur = int(input("사용할 휴가 번호를 입력하세요.\n"))-1
    sol.furlough.remove(sol.furlough[index_fur])

def editSoldier(sol):

    """

        병사의 정보를 수정합니다.
        pick에 수정할 데이터 종류를 입력받아
        if문을 돌며 해당하는 데이터를 수정합니다.
        이 때, 새로운 데이터를 제대로 입력하였는지 확인합니다.

    """
    
    print("수정 전 데이터: ")
    print(sol.platoon, '소대', sol.squad, '분대')
    if sol.rank == 1:
        print('이병', end=' ')
    elif sol.rank == 2:
        print('일병', end=' ')
    elif sol.rank == 3:
        print('상병', end=' ')
    elif sol.rank == 4:
        print('병장', end=' ')
    print(sol.name)
    print('군번: ', sol.armyCode)
    print('입대일: ', sol.indate)
    print('전역일: ', sol.outdate, end='\n\n')

    while 1:
        print("수정할 데이터를 입력하세요.")
        try:
            pick = int(input("\n1. 소대\n2. 분대\n3. 계급\n4. 이름\n5. 군번\n6. 입대일\n7. 전역일\n8. 취소\n\n"))
            if pick == 1:
                newPlatoon = input("새로운 소대를 입력하세요.\n")
                print('소대를', newPlatoon, "(으)로 설정하시겠습니까?", end='')
                yes = input("(Y/N)\n")
                if yes.upper() == 'Y':
                    sol.platoon = newPlatoon
                    print("수정되었습니다.")
                else:
                    print("취소합니다.")
            elif pick == 2:
                newSquad = input("새로운 분대를 입력하세요.\n")
                print('분대를', newSquad, "(으)로 설정하시겠습니까?", end='')
                yes = input("(Y/N)\n")
                if yes.upper() == 'Y':
                    sol.squad = newSquad
                    print("수정되었습니다.")
                else:
                    print("취소합니다.")
            elif pick == 3:
                try:
                    newRank = int(input("새로운 계급(1~4)를 입력하세요.\n"))
                except:
                    print("1~4 정수로 입력해주세요.\n")
                    continue
                print('계급을', newRank, "(으)로 설정하시겠습니까?", end='')
                yes = input("(Y/N)\n")
                if yes.upper() == 'Y':
                    sol.rank = newRank
                    print("수정되었습니다.")
                else:
                    print("취소합니다.")
            elif pick == 4:
                newName = input("새로운 이름을 입력하세요.\n")
                print('이름을', newName, "(으)로 설정하시겠습니까?", end='')
                yes = input("(Y/N)\n")
                if yes.upper() == 'Y':
                    sol.name = newName
                    print("수정되었습니다.")
                else:
                    print("취소합니다.")
            elif pick == 5:
                newArmycode = input("새로운 군번을 입력하세요.\n")
                print('군번을', newArmycode, "(으)로 설정하시겠습니까?", end='')
                yes = input("(Y/N)\n")
                if yes.upper() == 'Y':
                    sol.armyCode = newArmycode
                    print("수정되었습니다.")
                else:
                    print("취소합니다.")
                
            elif pick == 6:
                newIndate = input("새로운 입대일을 입력하세요.\n")
                print('입대일을', newIndate, "(으)로 설정하시겠습니까?", end='')
                yes = input("(Y/N)\n")
                if yes.upper() == 'Y':
                    sol.indate = newIndate
                    print("수정되었습니다.")
                else:
                    print("취소합니다.")
                
            elif pick == 7:
                newOutdate = input("새로운 전역일을 입력하세요.\n")
                print('전역일을', newOutdate, "(으)로 설정하시겠습니까?", end='')
                yes = input("(Y/N)\n")
                if yes.upper() == 'Y':
                    sol.outdate = newOutdate
                    print("수정되었습니다.")
                else:
                    print("취소합니다.")
                
            elif pick == 8:
                print("취소합니다.")
                break
                
        except:
            print("1~8 정수로 다시 입력해주세요.")



def index():

    """

        이 프로그램의 메인 루프입니다.
        pick에 0을 input하지 않는 이상 무한 반복합니다.

        + 휴가 수정
        + 휴가 현황 (휴가 사용)
        + 전역한 병사 신상 삭제
        + Think about every exception

    """

    pick = 0
    while 1:
        print("\n-----------APM-----------\n")
        print("Army Personal Management\n")
        
        print(time.ctime(time.time()), end = '\n\n')
        
        print("1. 모든 병사 신상 조회")
        print("2. 모든 병사 신상 및 휴가 조회")
        print("3. 병사 신상 추가")
        print("4. 병사 신상 수정")
        print("5. 병사 휴가 조회")
        print("6. 병사 휴가 추가")
        print("7. 병사 휴가 사용")
        print("8. 모든 병사 휴가 추가")
        print("9. 프로그램을 종료하지 않고 저장")
        print("0. 저장 후 프로그램 종료")
        try:
            pick = int(input("\n"))
        except:
            print("\n0~9 정수를 입력해주세요.")
        if pick == 1:
            showSoldiers()
        elif pick == 2:
            showSoldiersFurlough()
        elif pick == 3:
            addSoldier()
        elif pick == 4:
            ac = input("수정할 병사의 군번을 입력하세요.\n")
            sol = findSoldier_ac(ac)
            if sol != 0:
                editSoldier(sol)
        elif pick == 5:
            ac = input("휴가를 조회할 병사의 군번을 입력하세요.\n")
            sol = findSoldier_ac(ac)
            if sol != 0:
                sol.printFurlough()
        elif pick == 6:
            ac = input("휴가를 추가할 병사의 군번을 입력하세요.\n")
            sol = findSoldier_ac(ac)
            if sol != 0:
                addFurlough(sol)
        elif pick == 7:
            ac = input("휴가를 사용할 병사의 군번을 입력하세요.\n")
            sol = findSoldier_ac(ac)
            if sol != 0:
                useFurlough(sol)
        elif pick == 8:
            addFurloughAll()
        elif pick == 9:
            try:
                end()
                print("저장되었습니다.")
            except:
                print("\n종료 에러: 데이터 파일을 종료하고 다시 시도하세요.")
        elif pick == 0:
            try:
                print("프로그램을 종료합니다.")
                end()
                break
            except:
                print("\n종료 에러: 데이터 파일을 종료하고 다시 시도하세요.")


def end():

    """

        배열 soldiers를 DataFrame으로 만들어 파일(xlsx)에 작성합니다.
        휴가는 소지한 병사 밑의 2 열 부터 작성됩니다.

    """

    names = []
    codes = []
    ranks = []
    platoons = []
    squads = []
    indates = []
    outdates = []
    for sol in soldiers:
        names.append(sol.name)
        codes.append(sol.armyCode)
        ranks.append(sol.rank)
        platoons.append(sol.platoon)
        squads.append(sol.squad)
        indates.append(sol.indate)
        outdates.append(sol.outdate)
        for i in range(len(sol.furlough)):
            names.append('')
            codes.append('휴가')
            ranks.append(sol.furlough[i].type)
            platoons.append(sol.furlough[i].term)
            squads.append(sol.furlough[i].date)
            indates.append(sol.furlough[i].deadline)
            outdates.append('')
        names.append('')
        codes.append('')
        ranks.append('')
        platoons.append('')
        squads.append('')
        indates.append('')
        outdates.append('')
                            
    result = zip(names, codes, ranks, platoons, squads, indates, outdates)
    datas = pd.DataFrame(data = result, columns = ['이름', '군번', '계급', '소대', '분대', '입대일', '전역일'])
    
    datas.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
    return 0

loadSoldiers()
index()
