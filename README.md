# DB_Project
2024-2학기 데이터베이스 프로젝트 레포지토리
# 깃 사용법
- Clone
```
git clone https://github.com/KWNahyun/DB_Project.git
```
- Pull
개발 전에 pull해서 꼭 다른 팀원의 변경사항 반영해주기! 안 그러면 나중에 겁나 꼬여요...
```
git pull origin main
```
- Commit
```
git add *
git commit -m "커밋 메시지 상세히 작성해주세요"
```
- Push
개발 이후에 push해서 꼭 변경사항 깃허브에 올려주기~ 안 그러면 나중에 겁나 꼬여요...
```
git push origin main
```
**근데 그냥 vscode에서 add, commit, push, pull하면 편함**
# 가상환경 설정
- 가상환경 생성
```
python -m venv db_env
```
- 라이브러리 설치
```
pip install -r requirements.txt
```
- 가상환경 활성화
```
db_env/Scripts/activate
```
- 가상환경 비활성화
```
deactivate
```
- venv 명령어가 먹히지 않을 경우 powershell을 관리자 권한으로 들어가서 `Set-ExecutionPolicy RemoteSigned` 명령어 실행하기
- 가상환경에 패키지를 설치하면 `pip freeze > requirements.txt`로 패키지 목록 업데이트 바랍니다!

# 아키텍쳐
![alt text](image.png)
**uWSGI를 사용하려면 우분투 환경이 필요하므로 윈도웅에서 사용할 수 있는 gunicorn으로 middleware를 구성하는 것으로 변경한다.**

# 서버 실행
```
python run.py
```
# mysql 서버 접속
```mysql shell
\sql
\connect --mysql nahyun@localhost:3306
```
# 서버 접속 확인 (명령 프롬프트 창에서)
```cmd
net start | find "MySQL"
```
# mysql user 생성
- 기존 user 확인
```mysql
use mysql;
select user, host from user;
```
- 새 user 생성
```mysql
create user USER_ID@localhost identified by 'USER_PASSWORD'; 
grant all privileges on *.* to USER_ID@localhost;
```
- 테스트를 위한 예시 데이터베이스 생성
```
python reset_database.py
```
-> 이후에 'flask run'을 하면 예시 데이터베이스로 초기화된다.
# TODO (2024.11.25)
- Bootstrap 연동해서 프런트 구성
- MYSQL 연동하기