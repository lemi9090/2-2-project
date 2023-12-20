import subprocess

## "cd :\Program Files\Oracle " , "sartvm", "sand2"
    ## == 이건 cd 명령에 한줄로 쭉 가는거다. 그러니 아래처럼 해야한다.

vboxmanage_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

def start_vm(vm_name):
    try:
        subprocess.call([vboxmanage_path, "startvm", vm_name, "--type", "gui"])
        print("서버가 실행되기까지 2분정도 소요됩니다.")
    except Exception :
        pass

def poweroff_vm(vm_name):
    try:
        subprocess.call([vboxmanage_path, "controlvm", vm_name, "poweroff"])
    except Exception :
        pass
def snapshot_vm(vm_name, snapshot_name):
    try:
        subprocess.call([vboxmanage_path, "snapshot", vm_name, "take", snapshot_name])
    except Exception :
        pass
def rollback_vm(vm_name, snapshot_name):
    try:
        subprocess.call([vboxmanage_path, "snapshot", vm_name, "restore", snapshot_name])
    except Exception :
        pass
def list_vm():
    try:
        subprocess.call([vboxmanage_path, "list", "vms"])
    except Exception :
        pass
""" def remotcon(vm_name,username, password, remote_command): 
    subprocess.call([vboxmanage_path,"guestcontrol", vm_name, "run", "--username", username, "--password", password, "--", remote_command])
 """
def my_sql(file_path): # 로컬에서 mysql 접근 명령
    try:
        subprocess.call([file_path, "-u", "root", "-p", "", "-e", "use test"])
    except Exception :
        pass


def main():
    while True:
        vm_name = input ("명령을 내릴 가상머신 이름을 입력하세요 : ")
        action = input("명령을 입력하세요 (start, power-off, snapshot, rollback, machine_list, mysql, exit): ")

        if action == "start":
            start_vm(vm_name)
        elif action == "power-off":
            poweroff_vm(vm_name)
        elif action == "snapshot":
            snapshot_name = input("스냅샷 이름을 입력하세요: ")
            snapshot_vm(vm_name, snapshot_name)
        elif action == "rollback":
            snapshot_name = input("복원할 스냅샷 이름을 입력하세요: ")
            rollback_vm(vm_name, snapshot_name)
        elif action == "machine_list":
            list_vm()
        elif action.lower() =="exit":
            break
        else:
            print("지원하지 않는 작업입니다.")

""" elif action == "etc":
        username = input("가상머신의 사용자 이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        python_path = input("가상머신의 Python 인터프리터 경로를 입력하세요: ")
        script_path = input("실행할 Python 스크립트의 경로를 입력하세요: ")
        remote_command = f"{python_path} {script_path}"
        remotcon(vm_name, username, password, remote_command) """
