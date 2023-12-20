"""import subprocess
import sys
def command():
    # PowerShell 명령 수정
    order = 'Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" | Export-Csv -Path "C:/Users/User/Desktop/test24/sysmon_log2.csv" -NoTypeInformation'
    
    # PowerShell 명령을 관리자 권한으로 실행하기 위한 명령어 구성
    ps_order = f'Start-Process PowerShell -ArgumentList "-Command {order}" -Verb RunAs'
    
    # Windows에서만 실행
    if sys.platform == 'win32':
        subprocess.run(['Powershell', '-Command', ps_order], shell=True)

command() """

import subprocess

def export_csv (file_path) : # PowerShell 스크립트 파일 경로
    try : 
        order = f'Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" | Export-Csv -Path "{file_path}" -NoTypeInformation'

    # PowerShell 스크립트 실행
        subprocess.run(["powershell", "-Command", order], shell=True, check=True)        
    except Exception as e :
        print(f"{e} : 오류 발생\n관리자 모드로 다시 실행해 주세요.")

def main():
    file_path =  "C:/Users/User/Desktop/sysmon_log2.csv" #input ("저장할 위치와 파일명을 입력해 주세요 (나가기는 'exit' 입력):")
    if file_path:
        export_csv(file_path)
        print("operation sucsess")       
    else:
        print('올바른 파일 경로를 입력해주세요.')

main() # 스크립트를 부르려면(cli 로 실행하려면) 항상 스크립트에 들어와서 디버깅한다고
     # 생각했을 때 함수를 호출해야 클라이언트든 다른 그냥 py 파일을 호출하는 거든 했을 때
    # 원하는데로 py 파일이 실행되고 디버깅된다.  -> 그냥 함수 호출을 안했으니 실행이 안돼서 삽질했다는 소리임.

""" script_path = 'C:/Users/User/Desktop/script.ps1' """





