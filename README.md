# nccu_dbms
- [專案題目說明]()
- [ER-model](docs/ER-model.pdf)
- [Relational-Schema](docs/Relational-Schema.pdf)







### Entity Types

* User(使用者)：*User_id* (使用者編號)、Name (姓名)、Email (電子信箱)、Password (密碼)、Student_number (學號)、Phone (電話)

* Book(書籍)：*ISBN* (國際標準書號)、Book ID (書的編號)、Book Name (書名)、Author (作者)、Publisher (出版社)、Publication Year (出版年)、Image (書的圖片)

* Genre(種類)：*Genre_ID* (種類編號)、Genre Name (種類名稱)

* (Weak)Post(教師履歷)：*Post ID* (貼文編號)、Price (價格)、Book Condition (書況)、Post Time (貼文時間) 

* (Weak)Reply(回覆)：*Reply ID* (回覆編號)、From (發回覆者)、To (接收回覆者)、Reply Time (回覆時間)

    註：斜體者為 Primary key 或 Partial key。

### Relationship Types

    1. 一位 User (使用者)可以發多則 Post (貼文)
    2. 一則 Post (貼文)只會被一位 User (使用者)所發出
    3. 一本 Book (書籍)可以存在於多個 Post (貼文)
    4. 一則 Post (貼文)只會包含一本 Book (書籍)
    5. 一本 Book (書)只屬於一個 Genre (種類)
    6. 一個 Genre (種類)可以包涵多本 Book (書)
    7. 一位 User (使用者)可以發個 Reply (回覆)
    8. 一則 Reply (回覆)只會被一位 User (使用者)所發出
    9. 一則 Post (貼文)可以有多個 Reply (回覆)
    10. 一則 Reply (回覆)只能針對一則 Post (貼文)

## 系統功能分析

    1. 訪客：搜尋、篩選、註冊（登入）

    2. 登入User：徵求、留言

    3. 賣家：發貼文、管理已上傳貼文（編輯、下架）、留言

## CRUD

1.訪客
    
    不需要註冊就能瀏覽網頁上的書籍資訊，若註冊成為會員，可進一步互動，如刊登二手書貼文與回應
    
    Create：無

    Read：瀏覽書籍、並使用搜尋功能、篩選功能來找到想要的書，並且能看到貼文列表

    Update：無
    
    Delete：無

2.已登入User
    
    註冊後成為使用者，不僅能夠瀏覽網頁上所陳列的書籍，也能針對有發貼文的賣家在留言板上進行回覆
    
    Create：新增二手書、與賣家留言做互動

    Read：瀏覽書籍、並使用搜尋功能、篩選功能來找到想要的書，此外，能看到留言紀錄，也能看到貼文列表

    Update：無
    
    Delete：無


3.賣家 
    
    登入後的使用者同時能成為賣家，可以針對書籍發出貼文，提供書名、書況、價格等資訊供人瀏覽，
    將二手書轉讓給有緣人

    Create：發佈二手書資訊的貼文，把書上架賣給需要的人，且能與買家留言互動

    Read：查看自己上架的書籍、查看留言板紀錄

    Update：編輯貼文，更改二手書的資訊，也能下架書籍
    
    Delete：刪除貼文

## 心得
**組名｜你說的都隊**


**組員｜112354010 陳品華 統碩二**

後端開發

心得心得心得心得心得心得心得心得心得心得心得心得心得心得心得心得心得
