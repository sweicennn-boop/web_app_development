# 路由設計文件 (ROUTES)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 首頁 | GET | `/` | `index.html` | 顯示心情與天氣按鈕介面 |
| 選歌結果 | GET | `/result` | `result.html` | 根據 query 參數 (`type` 與 `tag`) 隨機取得歌曲並顯示 |
| 推薦曲目清單 | GET | `/recommendations` | `recommend/list.html` | 列出已審核通過的他人推薦歌曲 |
| 提交推薦表單 | GET | `/recommendations/new`| `recommend/form.html` | 顯示提交推薦歌曲的表單 |
| 儲存推薦 | POST | `/recommendations` | — | 接收推薦表單，存入 DB，重導向至清單頁 |
| 管理員登入 | GET/POST | `/admin/login` | `admin/login.html` | 顯示登入表單與驗證帳號密碼 |
| 管理員登出 | GET | `/admin/logout` | — | 處理登出邏輯並重導向至登入頁 |
| 管理員儀表板 | GET | `/admin/songs` | `admin/dashboard.html` | 列出所有歌曲，供管理員增刪改查 |
| 新增歌曲表單 | GET | `/admin/songs/new` | `admin/song_form.html` | 顯示新增歌曲的空白表單 |
| 創建歌曲 | POST | `/admin/songs` | — | 接收表單並儲存歌曲，重導向至儀表板 |
| 編輯歌曲表單 | GET | `/admin/songs/<id>/edit` | `admin/song_form.html` | 顯示編輯歌曲的預填表單 |
| 更新歌曲 | POST | `/admin/songs/<id>/update` | — | 更新特定歌曲資料，重導向至儀表板 |
| 刪除歌曲 | POST | `/admin/songs/<id>/delete` | — | 刪除指定歌曲，重導向至儀表板 |

## 2. 每個路由的詳細說明

### `main` 藍圖
- **GET `/`**
  - **輸入**：無
  - **處理**：純前端頁面渲染
  - **輸出**：渲染 `index.html`
- **GET `/result`**
  - **輸入**：接收 URL Query string `?type=xxx&tag=yyy`
  - **處理**：檢查參數有效性，並呼叫 `Song.get_random_by_tag`
  - **輸出**：成功渲染 `result.html`；失敗導回 `/` 或顯示錯誤

### `recommend` 藍圖
- **GET `/recommendations`**
  - **輸入**：無
  - **處理**：呼叫 `Recommendation.get_all_approved()`
  - **輸出**：渲染 `recommend/list.html`
- **GET `/recommendations/new`**
  - **處理**：單純顯示表單
  - **輸出**：渲染 `recommend/form.html`
- **POST `/recommendations`**
  - **輸入**：表單欄位包含 `title`, `artist`, `reason`, `submitter_name`
  - **處理**：建立新的 pending recommendation 狀態
  - **輸出**：重導向至 `/recommendations`

### `admin` 藍圖
- **GET/POST `/admin/login`**
  - **輸入**：管理員認證資訊
  - **處理**：比對加密密碼，成功後寫入 Session
  - **輸出**：重導向至儀表板 `/admin/songs` 或回傳認證錯誤模板
- **CRUD for admin**
  - 使用 Session 裝飾器要求登入狀態
  - 出錯時能利用 `flash` 機制傳遞錯誤訊息然後重導向
  - 在更新(POST)或刪除(POST)行為完成後，必須使用 `redirect` 防止表單重複送出

## 3. Jinja2 模板清單

- `templates/base.html` - 共用 Base 模板（含 Navbar 與 Footer）
- `templates/index.html` - 繼承 base，首頁選擇區域
- `templates/result.html` - 繼承 base，結果顯示頁面
- `templates/recommend/list.html` - 繼承 base，推薦清單
- `templates/recommend/form.html` - 繼承 base，推薦表單
- `templates/admin/login.html` - 繼承 base，後台登入頁面
- `templates/admin/dashboard.html` - 繼承 base，歌曲列表儀表板
- `templates/admin/song_form.html` - 繼承 base，新增/編輯共用表單

## 4. 路由骨架程式碼
路由骨架已經實作於 `app/routes/` 下的 `main.py`, `recommend.py`, `admin.py` 中。
