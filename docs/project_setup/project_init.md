# Project Setup and Start
## Backend
- 透過 script 初始化
```bash
# 進入 scripts 資料夾
cd backend/scripts

# 透過 bash 執行
bash init.sh

# 直接執行
./init.sh
```

- 不透過 script 初始化 ( 無法初始化 grnre 所需基本資料 )
```bash
cd backend

# for Mac
export FLASK_APP=src/app

# for Windows
set FLASK_APP=src/app.py

# initialize database (run before strat server)
flask init-db

# run server
flask run
```