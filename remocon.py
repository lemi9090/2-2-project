
def handle_action(action):
    if action == "client":
        import client
        client.main()  
    elif action == "cli_commander":
        import CLI_commander  
        CLI_commander.main()  
    elif action == "csv_export":
        import csv_export
        csv_export.main()
    elif action == "db_upload":
        import CSV_DB_parser
        CSV_DB_parser.main()  
    else:
        print("지원하지 않는 작업입니다.")

def main():

    while True:
        action = input("명령을 입력하세요 (client, cli_commander, csv_export, db_upload): ")
        
        if action == "exit":
            break
        else:
            handle_action(action)

main()