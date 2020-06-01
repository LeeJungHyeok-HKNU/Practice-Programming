"""

    날짜 계산기입니다.
    추가될 기능
    - index
    - date + x days = ?
    - day of the week of the date
    2020-06-01
    Lee Junghyeok

"""

import time as t

def get_time():
    inputDate = input("\n(년-월-일)\n\n")
    try:
        resultTime = t.strptime(inputDate, "%Y-%m-%d")
        return resultTime
    except:
        print("Please enter right.")
        return get_time()

print("---날짜 계산기---\n")

nowTime_struct = t.localtime()
print(t.asctime(nowTime_struct))

print("시작 날짜를 입력하세요.")

startDate_struct = get_time()
startTime = t.mktime(startDate_struct)
print(startDate_struct)

print("끝 날짜를 입력하세요.")

endDate_struct = get_time()
endTime = t.mktime(endDate_struct)
print(endDate_struct)

difTime = endTime - startTime

print(int(difTime/(60*60*24)), "일 입니다.")
