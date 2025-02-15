# 二手書交易網
**組名｜你說的都隊**

**組長｜** 113753128 資科碩一 李昕融

**組員｜**110301026 國貿四 何姿儀 112354002 統碩二 張倢琳 112354003 統碩二 樂沂晨 112354010 統碩二 陳品華 112354021 統碩二 張祐瑜

## 系統架構
- 系統開發程式語言：Python 3.12   
- DBMS與工具：Flask 3.0.3 + SQLite
- 前端： Vue + Vite 
- 系統模組：用戶模組、書籍模組、貼文模組、回應模組


## 資料表概述
| 資料表名稱     | 欄位                                                     |
|---------------|----------------------------------------------------------|
|書籍           |國際標準書號, 作者, 書名, 圖片網址, 出版年份, 出版商, 書本類別|
|書籍類別       |類別編號, 書本類別                                         |
|使用者         |使用者編號, 姓名, 學號, 電子郵件, 電話號碼, 密碼             |
|刊登           |貼文編號, 價格, 書況, 貼文時間, 賣家編號                    |
|回覆           |回覆編號, 回覆內容, 回覆時間, 回覆者, 接收者, 貼文編號       |

## 資料介紹
#### 1.  書籍資料表
| 欄位名稱       | 中文名稱       | 備註          |
|---------------|----------------|---------------|
| ISBN          | 國際標準書號   | 由 13 位數碼組成 |
| Author        | 作者           |               |
| Book_name     | 書名           |               |
| Book_picture_url | 圖片網址    |               |
| Public_year   | 出版年份       |               |
| Publisher     | 出版商         |               | 
| Genre_name    | 書本類別       |分為9類，如：哲學類, 宗教類...等|

#### 2. 書籍類別資料表
| 欄位名稱       | 中文名稱       | 備註          |
|---------------|----------------|---------------|
| Genre_ID      | 類別編號       |    系統生成    |
| Genre_Name    | 書本類別       |分為9類，如：哲學類, 宗教類...等 |

#### 3. 使用者資料表
| 欄位名稱       |中文名稱       | 備註          |
|---------------|----------------|---------------|
| User_ID       | 使用者編號      | 系統生成      |
| Name          | 姓名            |               |
| StudentNumber | 學號            |               |
| Email         | 電子郵件         |               |
| Phone         | 電話號碼         |               |
| Password      | 密碼            |               |

#### 4. 刊登資料表
| 欄位名稱       | 中文名稱       | 備註          |
|---------------|----------------|---------------|
| Post_ID        | 貼文編號       | 系統生成      |
| Price          | 價格           |單位：元       |
| BookCondition  | 書況           |               |
| PostTime       | 貼文時間        |系統生成       |
| Seller_ID      | 賣家編號        | 系統生成      |

#### 5. 回覆資料表
| 欄位名稱   | 中文名稱         |備註          |
|------------|-----------------|--------------|
| Reply_ID   | 回覆編號         |系統生成      |
| Content    | 回覆內容         |              |
| ReplyTime  | 回覆時間         |系統生成      |
| From       | 回覆者           |              |              
| To         | 接收者           |              |
| Post_ID    | 貼文編號         |系統生成      |


## 需求分析
    1. 二手書資料：ISBN、作者、書名、圖片網址、出版年份、書本類別
    
    2. 商品資訊：價格、書況、刊登時間
    
    3. 用戶：姓名、學號、聯絡方式（手機、信箱）、交易紀錄
    
    4. 貼文：傳遞方向、時間、內文、回覆者


## 系統功能分析

    1. 訪客：搜尋、篩選、註冊（登入）

    2. 買家：上傳書籍、留言

    3. 賣家：發貼文、管理已上傳貼文（修改價格及書況）、留言、下架書籍


## ER Model

<img width="1093" alt="image" src="https://github.com/user-attachments/assets/d8987d7d-cf84-4637-a4bd-c27e7cceda20" />


## Relational Schema 

<img width="1197" alt="image" src="https://github.com/user-attachments/assets/7265665a-1c73-46c3-9adb-12da1be2608d" />


## Entity Types

* User(使用者)：*User_id* (使用者編號)、Name (姓名)、Email (電子信箱)、Password (密碼)、Student_number (學號)、Phone (電話)

* Book(書籍)：*Book ID* (書的編號)、 ISBN (國際標準書號)、Book Name (書名)、Author (作者)、Publisher (出版社)、Publication Year (出版年)、Image (書的圖片)

* Genre(種類)：*Genre_ID* (種類編號)、Genre Name (種類名稱)

* (Weak)Post(教師履歷)：*Post ID* (貼文編號)、Price (價格)、Book Condition (書況)、Post Time (貼文時間) 

* (Weak)Reply(回覆)：*Reply ID* (回覆編號)、From (發回覆者)、To (接收回覆者)、Reply Time (回覆時間)

    註：斜體者為 Primary key 或 Partial key。

## Relationship Types

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



## CRUD

1.訪客
    
    不需要註冊就能瀏覽網頁上的書籍資訊，若註冊成為會員，可進一步互動，如刊登二手書貼文與回應
    
    Create：無

    Read：瀏覽書籍、並使用搜尋功能、篩選功能來找到想要的書

    Update：無
    
    Delete：無

2.買家
    
    註冊後成為使用者，不僅能夠瀏覽網頁上所陳列的書籍，也能針對有發貼文的賣家在留言板上進行回覆
    
    Create：新增二手書、與賣家留言做互動

    Read：瀏覽書籍、並使用搜尋功能、篩選功能來找到想要的書，此外，能看到留言紀錄，也能看到貼文列表

    Update：無
    
    Delete：無


3.賣家 
    
    登入後的使用者同時能成為賣家，可以針對書籍發出貼文，提供書名、書況、價格等資訊供人瀏覽，
    將二手書轉讓給有緣人

    Create：發佈二手書資訊的貼文，把書上架賣給需要的人，且能與買家在留言板互動

    Read：查看自己上架的書籍、查看留言板紀錄

    Update：編輯貼文，更改二手書的資訊，也能下架書籍
    
    Delete：刪除貼文

## 心得
**組名｜你說的都隊**

**組長｜113753128 李昕融  資碩一** 

前後端開發 

雖然之前有開發過的經驗，所以做起來比較順手一些，但這也是我第一次用python去開發一個系統，和之前所學的框架還是有些差異，過程中和組員溝通和討論也學到了非常多，和組員溝通開發協作的經驗對我來說是相當可貴的，也感謝大家在這個專案的貢獻！

-----------------------------
**組員｜12354002 張倢琳 統碩二** 

前後端開發

這是我第一次這麼完整的完成一個前後端專案，過程中真的遇到好多好多挑戰（前後端連線問題、session 要怎麼存取跟傳遞、全域變數怎麼設計......等等）。從一開始超崩潰，到開始想各種原因跟方法、查各種資料，再到現在漸漸了解怎麼做，真的學到超級超級多，果然要自己做過一次才知道在幹嘛啊！

謝謝每個組員的努力，以及過程中被我問爆的組員與朋友，大家的合作才能讓這個專案順利完成。終於可以好好睡覺了哈哈

-----------------------------
**組員｜112354003 樂沂晨 統碩二** 

後端開發

這是我第一次完整參與資料庫系統的開發，過程中學習了如何設計資料表與撰寫查詢語句，也對後端架構有了初步了解，例如 API 的測試與建構。
也感謝組員們的耐心指導，從 debug 到協作，讓我從對 git 一無所知到逐漸掌握如何使用版本控制工具來進行團隊開發，每週的開會與討論都讓我收穫滿滿。這次專案久違地讓人感受到團隊合作的力量與快樂，過程不僅非常充實也十分有趣！

-----------------------------
**組員｜112354010 陳品華 統碩二**

後端開發

這是第一次透過協作的方式完整開發資料庫應用系統，過去只有寫過很簡易的網站，但這次學到了以前沒碰過的如api功能測試、版本控制等新功能開發，雖然時間非常緊湊，同時間也有好多課要對付與論文等等，甚至報告前一天大家還在趕工，但組員們非常的積極參與討論，從剛開始的題目需求分析到後續的系統開發，尤其非常感謝倢琳與昕融，在其他人需要幫忙時伸出援手，甚至在半夜測試、debug，沒有大家，想賣二手書的人真的賣不出去。

-----------------------------
**組員｜112354021 張祐瑜 統碩二** 
 
後端開發

第一次寫後端框架，從完全不懂到一步步熟悉，這些都要謝謝各位組員的幫忙，謝謝他們在完成自己負責的項目外依舊耐心指導我。另外，這份專案也讓我更熟悉git版本控制，從中也發現版本控制的實用性。

-----------------------------
**組員｜110301026 何姿儀 國貿四** 

前端開發

這是第一次完成了一套涉及前後端的系統，剛開始完全不理解git是如何操作，即便自己上網查好長一段時間還是不知道下一步該如何進行，浪費很多時間也很有挫敗感，不過這要非常感謝組員們的幫助，一步一步不厭其煩的教我，到後來已經可以自己解決問題真的成就感滿滿，也從中收穫良多，雖然這個專案耗費了很多時間與精力，我還是認為能擁有這樣的經驗和組員是很難能可貴的！


