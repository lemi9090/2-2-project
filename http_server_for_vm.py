from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import subprocess
import cgi


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self): 
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, this is a GET request!')
        elif self.path.startswith('/download'): 
            # the original code (self.path == '/download') can read only "/download" path request.
            # therefore we are change "startwith". It can load "/download~~"" code
            # VM 내부의 파일을 VM 외부에 제공 할 수 있다.
            # 파일 이름 추출
            file_name = self.path.split('?file=')[1]
            file_path = os.path.join('C:/Users/User/Desktop/http_server', file_name)
            try:
                # 파일 크기 얻기
                file_size = os.path.getsize(file_path)
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{file_name}"')
                self.send_header('Content-Length', file_size)
                self.end_headers()
                with open(file_path, 'rb') as file:
                    chunk_size =4096 # 4KB 만큼 읽음
                    while True :
                        chunk = file.read(chunk_size)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                             # 파일 내용 전송 
                    """ 이 메서드는 HTTP 응답의 본문(body)에 데이터를 쓰는 데 사용됩니다. 
                    self.wfile은 클라이언트에게 데이터를 전송하는 데 사용되는, 
                    파일과 유사한 객체입니다. write() 메서드에 전달된 
                    데이터(여기서는 file.read()에 의해 읽힌 파일의 내용)는 
                    클라이언트에게 직접 전송됩니다. """
            except FileNotFoundError:
                # 파일이 존재하지 않는 경우
                self.send_error(404, 'File Not Found: %s' % file_name)
            except Exception as e:
                # 기타 오류 처리
                self.send_error(500, str(e))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    
    def do_POST(self):
        if self.path .startswith ('/command'): # VM 외부로부터 명령을 수신 받을 수 있어야 한다.
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                allowed_commands = ['ipconfig', 'dir']
                command = data ['command']

                if command in allowed_commands:#허용된 명령어에서 
                    result = subprocess.check_output(command, shell=True, timeout=4)
                    response_data = {'message' : 'Command executed successfully','output': result.decode() }
                else:
                    response_data = {'message': 'Command not allowed'}

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                print(408, 'timeout' , str(e))
            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON data')
            except subprocess.CalledProcessError as e:
                self.send_error(500, 'Error executing command: ' + str(e))   
        
        elif self.path.startswith('/executor'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                file_path = data.get('filename')
                allowed_extensions = ['.py', '.csv', '.exe', '.lnk', '.txt']
                if any(file_path.endswith(ext) for ext in allowed_extensions):
                    print(file_path)
                    if file_path.endswith('.py'):
                        result = subprocess.check_output(['python', '-Xfrozen_modules=off' ,file_path])
                    elif file_path.endswith(('.csv', '.exe', '.lnk', '.txt')):
                        result = subprocess.check_output([file_path])
                    response_data = {'message': 'File executed successfully', 'output': result.decode()}
                else:
                    response_data = {'message': 'File execution not allowed'}
            except subprocess.CalledProcessError as e:
                print(f"오류발생: {e}")
            except Exception as e:
                self.send_error(400, f'Error executing file: {e}')

        

        elif self.path .startswith ('/upload'): #VM 외부로부터 파일을 전달 받고 VM 내부에 저장 할 수 있다.
            form = cgi.FieldStorage( #클라이언트의 post 요청 파일을 받아서 파싱함.
            fp=self.rfile,#요청정보
            headers=self.headers,environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })#헤더정보 
            if 'file' in form:# 클라이언트가 파일을 전송했는지 확인
                file_item = form['file'] # 파일을 가져옴
                if file_item.filename: #파일명이 존재하는지 확인
                    # 파일 경로와 이름 설정
                    file_name = file_item.filename
                    file_path = os.path.join('C:/Users/User/Desktop/http_server', file_name) #파일 저장 경로 설정

                    # 파일을 쓰기 모드로 열어서 저장.
                    with open(file_path, 'wb') as output_file:
                        output_file.write(file_item.file.read())
                    self.send_response(200)  #성공 응답 전송
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'File uploaded successfully.')
                else:
                    self.send_error(400, 'No file was uploaded.')
            else:
                self.send_error(400, 'File field not found.')
            pass
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')


def run_server():
    address = ('0.0.0.0', 8080)
    with HTTPServer(address, MyRequestHandler) as server:
        print('Starting server...')
        server.serve_forever()

if __name__ == '__main__':
    run_server()
