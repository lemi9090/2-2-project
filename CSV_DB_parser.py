import csv
import pymysql ## 성공 ##
import re

def parse_row(lines):
    patterns = { 
        #각 라인에 정규표현식을 사용해 데이터를 추출
        #각 라인을 돌면서 패턴에 맞는 데이터를 추출한다.
        #포괄 범위가 더 세세한걸 먼저 잡은 후 작은 범위를 세워야 정확성을 높일 수 있다.
        #파이썬도 검색 순서가 중요하다. user를 먼저 검사 후 parentuser을 검사하면 앞에서 그냥 다 user로 잡혀서 parentuser은 하나도 없게 된다.
        #추출한 데이터는 parsed_data에 저장된다
        "ParentImage": re.compile(r'ParentImage: (.+)'),
        "ParentProcessGuid": re.compile(r'ParentProcessGuid: (.+)'),
        "ParentProcessID": re.compile(r'ParentProcessID: (\d+)'),
        "ParentCommandLine": re.compile(r'ParentCommandLine: (.+)'),
        "ParentUser": re.compile(r'ParentUser: (.+)'),
        "Image": re.compile(r'Image: (.+)'),
        "ProcessGuid": re.compile(r'ProcessGuid: (.+)'),
        "ProcessId": re.compile(r'ProcessId: (\d+)'),
        "Utctime": re.compile(r'UtcTime: (.+)'),
        "CommandLine": re.compile(r'CommandLine: (.+)'),
        "User": re.compile(r'User: (.+)'),
        "Hashes": re.compile(r'Hashes: (.+)'),
    }

    parsed_data = {}
    for line in lines:
        for key, pattern in patterns.items():
            if key not in parsed_data:
                match = pattern.search(line)
                if match:
                    parsed_data[key] = match.group(1)
                    break

    return parsed_data

def csv_load(file_path, db_params): 
    conn = pymysql.connect(**db_params) #mysql에 연결하여 DB에 접근한다. 현재 스크립트에서 mysql을 안켜놓으면 여기서 오류가 발생한다.
    cursor = conn.cursor()#읽어들일 커서를 생성한다.

    with open(file_path, 'r', encoding='utf-8') as file:
        record_lines = []# 현재 처리중인 레코드의 모든 라인을 저장하는 리스트
        new_record = False  # 새로운 레코드의 시작을 기다리다가
        for row in file:
            if row.startswith('"Process terminated:\n') or row.startswith('"Process Create:\n'):
                #new_record = True # 위 문자열이 나오면 시작으로 생각한다!!
                if new_record and record_lines:# 모든 레코드 라인 중 시작 조건이 맞으면 이제 작업 시작
                    parsed_data = parse_row(record_lines) #데이터를 parsed_data에 담고
                    
                    if parsed_data:
                        columns = ', '.join(parsed_data.keys()) #각 항목이 나뉘는 공통적인 형식
                        placeholders = ', '.join(['%s'] * len(parsed_data)) #파싱해 얻은 데이터, 길이값
                        values = tuple(parsed_data.values()) #튜플 : 중복 X
                        cursor.execute(f"INSERT INTO sysmon_log ({columns}) VALUES ({placeholders})", values)
                        #쿼리 실행
                        
                        print(parsed_data) 
                    else:
                        print(f"Record parsing failed: {record_lines}")
                    
                    record_lines = [] # 다시 다음을 위해 초기화한다.
                new_record = True # 새로운 시작이라고 인식한다. 
            elif new_record:#위에서 인식했으면 아래에서 추가한다.
                record_lines.append(row)

        # 시작 문자열을 계속 받다가 마지막 파일이 이제 문자열을 받을게 없어지면 
        # 레코드 라인이 시작 부분이 없어서 그냥 덩그러니 있게된다.
        #그래서 아래 record_lines은 마지막으로 한번 더 지금까지 모은 데이터를 parsed_data에 넣어서
        # 출력시킨다.
        if record_lines: 
            parsed_data = parse_row(record_lines)
            if parsed_data:
                print(parsed_data)  
            else:
                print(f"Record parsing failed: {record_lines}")



    conn.commit() #얻은 정보 저장
    cursor.close()#위에서 연결해줬으니 항상 종료해주기
    conn.close() # 종료!!

def main():
    while True:

        file_path = input("원하는 파일의 경로를 입력하세요:" )  
        db_params = {

        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': 'test'
        }
        csv_load(file_path, db_params)
        if file_path == "exit":
            break
    # 데이터베이스 접속 정보

if __name__ == "__main__":
    main()






