# 系統流程圖與使用者操作路徑 (Flowcharts) - 心情選歌系統

以下文件根據現有的 [PRD.md](./PRD.md) 和 [ARCHITECTURE.md](./ARCHITECTURE.md) 設計，透過視覺化圖表釐清使用者的操作路徑與後端的資料流，並定義出各個功能的對應路由。

## 1. 使用者流程圖（User Flow）

此流程圖呈現一般使用者從進入網站開始，可能採取的各項操作行為。包含了「心情選歌」、「天氣選歌」、「他人推薦」以及「管理員後台」等核心情境。

```mermaid
flowchart TD
  A([使用者開啟網頁]) --> B[首頁 - 選擇模式]

  %% 三種選擇模式
  B --> C{選擇推薦方式}
  C -->|依心情| D[心情選擇頁面]
  C -->|依天氣| E[天氣選擇頁面]
  C -->|他人推薦| F[他人推薦曲目清單]

  %% 心情分支
  D --> D1{選擇心情}
  D1 -->|開心| G[選歌結果頁面]
  D1 -->|悲傷| G
  D1 -->|放鬆| G
  D1 -->|焦慮| G
  D1 -->|興奮| G

  %% 天氣分支
  E --> E1{選擇天氣}
  E1 -->|晴天| G
  E1 -->|雨天| G
  E1 -->|陰天| G
  E1 -->|下雪| G

  %% 結果頁面操作
  G --> H{對推薦結果滿意嗎？}
  H -->|滿意| I[點擊試聽連結聆聽歌曲]
  H -->|不滿意| J{下一步}
  J -->|換一首| G
  J -->|重新選擇| B

  %% 他人推薦分支
  F --> K{操作項目}
  K -->|瀏覽推薦清單| L[查看推薦歌曲詳情]
  K -->|我也想推薦| M[填寫推薦歌曲表單]
  M -->|送出| N([儲存推薦至資料庫])
  N --> F

  %% 管理員分支
  B --> O{身分}
  O -->|管理員| P[管理員登入頁面]
  P -->|登入成功| Q[歌曲管理儀表板]
  Q --> R{管理操作}
  R -->|新增歌曲| S[填寫新增歌曲表單]
  R -->|編輯歌曲| T[填寫編輯歌曲表單]
  R -->|刪除歌曲| U([確認刪除並重導向])
  S -->|儲存| V([資料庫處理並重導向])
  T -->|儲存| V
  V --> Q
  U --> Q
```

## 2. 系統序列圖（Sequence Diagram）

此圖以「**使用者依心情選歌**」這項核心操作為例，詳細描繪整個系統後端（MVC 架構）的運作順序——從使用者點擊心情按鈕到顯示推薦歌曲的完整流程。

```mermaid
sequenceDiagram
  actor User as 使用者
  participant Browser as 瀏覽器
  participant Route as Flask Route (Controller)
  participant Model as Model (資料庫互動層)
  participant DB as SQLite DB

  User->>Browser: 進入首頁，點擊「依心情選歌」
  Browser->>Route: 發送 GET / 請求
  Route-->>Browser: 回傳首頁 HTML (含心情按鈕)

  User->>Browser: 點選「開心」心情按鈕
  Browser->>Route: 發送 GET /result?type=mood&tag=happy 請求

  Route->>Model: 呼叫 Song.get_random_by_mood("happy")
  Model->>DB: 執行 SELECT * FROM songs JOIN song_mood ... ORDER BY RANDOM() LIMIT 1
  DB-->>Model: 回傳一筆歌曲資料 (歌名、歌手、風格、連結)
  Model-->>Route: 回傳歌曲 Python 物件

  Route-->>Browser: 回傳結果頁面 HTML (render_template with song data)
  Browser-->>User: 顯示推薦歌曲 (歌名、歌手、風格、試聽連結、換一首按鈕)

  User->>Browser: 點擊「換一首」按鈕
  Browser->>Route: 發送 GET /result?type=mood&tag=happy 請求 (重新隨機)
  Route->>Model: 再次呼叫 Song.get_random_by_mood("happy")
  Model->>DB: 執行隨機查詢
  DB-->>Model: 回傳另一筆歌曲資料
  Model-->>Route: 回傳歌曲物件
  Route-->>Browser: 回傳新的結果頁面 HTML
  Browser-->>User: 顯示新的推薦歌曲
```

## 3. 功能清單對照表

本清單列出所有將實作的功能，以及對應的 URL 路徑 (Routes) 和 HTTP 請求方法。由於原生 HTML 表單僅支援 GET 與 POST，故我們在更新/刪除資源時會透過 `POST` 方法加上特定後綴路徑來實作。

| 功能模塊 | 具體功能描述 | HTTP 方法 | URL 路徑 (Route) | 備註 |
| --- | --- | --- | --- | --- |
| **首頁與選歌** | 網站首頁（心情 & 天氣選擇介面） | GET | `/` | 顯示心情按鈕與天氣按鈕 |
| | 選歌結果頁面 | GET | `/result?type=mood&tag=<tag>` | 依心情隨機推薦一首歌 |
| | 選歌結果頁面 | GET | `/result?type=weather&tag=<tag>` | 依天氣隨機推薦一首歌 |
| | 換一首（重新隨機） | GET | `/result?type=<type>&tag=<tag>` | 相同參數重新查詢即可 |
| | 重新選擇（回首頁） | GET | `/` | 導回首頁重新選擇 |
| **他人推薦** | 推薦曲目清單頁面 | GET | `/recommendations` | 瀏覽所有使用者推薦的歌曲 |
| | 提交推薦歌曲表單頁面 | GET | `/recommendations/new` | 顯示空白推薦表單 |
| | 儲存推薦歌曲 | POST | `/recommendations` | 將推薦資料寫入資料庫 |
| **管理員後台** | 管理員登入頁面 | GET / POST | `/admin/login` | 含登入表單渲染(GET)與驗證(POST) |
| | 管理員登出 | GET | `/admin/logout` | 清除管理員 Session |
| | 歌曲管理儀表板 | GET | `/admin/songs` | 列出所有歌曲供管理 |
| | 新增歌曲表單頁面 | GET | `/admin/songs/new` | 提供空白輸入表單 |
| | 儲存新歌曲 | POST | `/admin/songs` | 將歌曲資料寫入資料庫 |
| | 編輯歌曲表單頁面 | GET | `/admin/songs/<int:song_id>/edit` | 填入既有資料供修改 |
| | 儲存修改的歌曲 | POST | `/admin/songs/<int:song_id>/update` | 更新歌曲資料 |
| | 刪除歌曲 | POST | `/admin/songs/<int:song_id>/delete` | 驗證權限後刪除歌曲 |
