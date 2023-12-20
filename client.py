import requests
import json

VM_path = "192.168.56.1:8080/"

def account(VM_path, order):
    # 일반적인 GET 요청
    try:
        response = requests.get(f'http://{VM_path}{order}')
        print("GET Response:")
        print(response.text)
    except Exception as e:
        print('NOPE!')
        pass

def download(VM_path, order, desired_download_location,sellected_filename):
    # download 요청
    with requests.get(f'http://{VM_path}{order}?file={sellected_filename}', stream=True) as response: 
        if response.status_code == 200:
            with open(f'{desired_download_location}', 'wb') as file:
                for chunk in response.iter_content(chunk_size=4096):
                    file.write(chunk)
            print('파일 다운 성공')
        else:
            print('Error', response.status_code)
            print(response.text)
            pass

def command(VM_path, order, instruction):
    # post 요청. json 형식. command 요청
    data = {'command': f'{instruction}'}
    headers = {'Content-type': 'application/json'}
    try:
        response = requests.post(f'http://{VM_path}{order}', json=data, headers=headers)
        print("\nPOST Response:")
        print(response.text)
    except Exception as e:
        print ('nope!')
        pass
def executor(VM_path, order, filename):
    data = {'filename': filename}
    headers = {'Content-type' : "application/json"}
    try:
        response = requests.post(f"http://{VM_path}/{order}", json=data, headers=headers)
        print("\nPOST Response:")
        print(response.text)
    except Exception as e :
        print("all done.")
        pass
    

def upload(VM_path, order, file_path):
    # post 요청. upload 요청
    try:
        files = {'file': open(file_path, 'rb')}
    
        response = requests.post(f"http://{VM_path}{order}", files=files)
        files['file'].close()
        print("\nPost Response:")
        print(response.text)
    except Exception as e:
        print('please check your file path')
        pass
def append(VM_path, order, post, file_name):
    # post 요청. json 형식. append 요청
    data = {"content": post}
    headers = {'Content-type': 'application/json'}
    try:
        response = requests.post(f"http://{VM_path}{order}?file={file_name}", json=data, headers=headers)
        print("\nPOST Response:")
        print(response.text)
    except Exception as e:
        print('nope')
        pass

def main():
    while True:
        # 사용자 입력 처리
        order = input("명령을 입력하세요 ('', 'download', 'command', 'upload', 'append', 'executor', 'exit'): ")
    
        if order == "":
            account(VM_path, order)
        elif order == "download":
            sellected_filename = input("원하는 파일명을 확장자와 같이 적으세요 :")
            desired_download_location = input("다운받을 경로를 파일명과 같이 적으세요 : ")
            download(VM_path, order,desired_download_location,sellected_filename)
        elif order == "command":
            instruction = input("원하는 명령어를 입력하세요 :")
            command(VM_path, order,instruction)
        elif order == 'executor':
            filename = input('실행시키려는 파일경로를 입력하세요: ')
            executor(VM_path, order, filename)
        elif order == "upload":
            file_path = input("파일 경로를 입력하세요: ")
            upload(VM_path, order, file_path)
        elif order == "append":
            post = input("추가할 내용을 입력하세요: ")
            file_name = input("파일명을 입력하세요 (확장자 포함): ")
            append(VM_path, order, post, file_name)
        elif order.lower() =="exit":
            break
        else:
            print("지원하지 않는 작업입니다.")

main()