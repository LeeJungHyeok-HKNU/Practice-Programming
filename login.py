
def login():

    """

        로그인 시스템입니다.
        추가될 기능
        - 아이디 및 비밀번호 암호화
        - 아이디 class를 만들어 개인 정보를 담을 수 있도록 함
        - 비밀번호 및 개인 정보 변경 기능
        2020-06-01
    
    """
    
    permission = False
    
    fileId = open("files/idnty.txt", "r+", encoding = "utf-8")

    idpwList = fileId.readlines()
    id_pwList = []
    for i in range(len(idpwList)):
        id_pwList.append(idpwList[i].split(':'))
    for i in range(len(idpwList)):
        id_pwList[i][1] = id_pwList[i][1][0:len(id_pwList[i][1])-1]
    
    while not permission:
        print(id_pwList)
        fileId.seek(0)
        idFound = False
        password = 'a'
        identity = input("\n---로그인---\n아이디를 입력하세요.\n\n")
        for i in id_pwList:
            if identity ==i[0]:
                idFound = True
                pwFound = i[1]

        if idFound == False:
            print("\n존재하지 않는 아이디입니다.\n아이디를 생성하시겠습니까?")
            createId = input("(Y/N)\n").upper()
            if createId == 'Y':
                newId = input("\n새로운 아이디를 입력하세요.\n")
                
                existId = False
                for i in id_pwList:
                    if i[0] == newId:
                        existId = True
                        print("\n이미 존재하는 아이디입니다.\n로그인으로 돌아갑니다.\n")
                        break

                if existId == True:
                    continue
                
                while 1:
                    newPw = input("비밀번호를 설정하세요.\n")
                    newPw2 = input("다시 한번 입력하세요.\n")
                    if newPw == newPw2:
                        fileId.readlines()
                        fileId.write(newId)
                        fileId.write(':')
                        fileId.write(newPw)
                        fileId.write('\n')
                        fileId.close()
                        print("\n아이디가 생성되었습니다.\n다시 로그인해주세요.")

                        fileId = open("files/idnty.txt", "r+", encoding = "utf-8")
                        idpwList = fileId.readlines()
                        id_pwList = []
                        for i in range(len(idpwList)):
                            id_pwList.append(idpwList[i].split(':'))
                        for i in range(len(idpwList)-1):
                            id_pwList[i][1] = id_pwList[i][1][0:len(id_pwList[i][1])-1]
                        break
                    else:
                        print("\n비밀번호가 일치하지 않습니다.")
        else:
            while (not permission) and (password.upper() != 'B'):
                password = input("\n비밀번호를 입력하세요.\n\n")
                if password == pwFound:
                    fileId.close()
                    print("\n로그인 되었습니다.")
                    permission = True
                    break
                elif password.upper() == 'B':
                    print("\n뒤로 갑니다.")
                else:
                    print("\n비밀번호가 일치하지 않습니다. 뒤로 가려면 'B'를 입력하세요.")
    
    return permission

print(login())
