# home/ — the cathedral at love (ai-love.cc)

YOUSPEAK 嘅公開首頁，Cloudflare Pages project 係 **ai-love**（custom domain
ai-love.cc）。`index.html` 同 `assets/app.js` 由人手維護；glyph／lexicon 資料由
agent bundle bake 出嚟。手寫 canon 摘句要另外逐字核對；相遇之間嘅私人回應
唔屬於 baked data。

相遇之間同 cathedral 基線已整合：保留 social metadata、`/true-love/`、署名、
chill-fi embeds，以及 Sophia invitation／nonclaims。發布前仍要更新 `origin` 同
`github` refs，核對新增變動；唔以舊 `home/` 整檔覆蓋較新線上內容。

## Rebuild + deploy

只有 canon／font source 改動時先重建；純 authored HTML／JS 變動唔需要 bake：

```sh
python3 script/tools/export_agent_bundle.py
python3 home/bake.py
open home/proof.html
```

取得發布授權、確認現有 Wrangler 登入同測試通過後，由 repo 根目錄部署乾淨 commit：

```sh
CLOUDFLARE_ACCOUNT_ID=cf4198e651bf3009877d49f688c9d88e \
  wrangler pages deploy home --project-name ai-love --branch main \
  --commit-hash "$(git rev-parse HEAD)" --commit-dirty=false
```

`ai-love` 嘅 production branch 係 `main`，Pages domain 係 `ai-love-c88.pages.dev`。
唔需要複製 credentials 或改 Worker routing。`wrangler whoami` 喺 PTY 而登入失效時
可能開 browser OAuth；唔將 PTY 當成純唯讀 auth 檢查。部署後核對 deployment URL
同 `https://ai-love.cc/#isness`，唔只睇 CLI exit code。現有 `/agent.txt` 可能由
compatibility shim 提供；static deploy 唔代表該 route 會換成 repo 檔案。

## What lives where

- `bake.py` — the only generator. Emits `font/youspeak-v1.otf`,
  `data/{morphemes,lexicon}.min.json`, `data/core.js`, `data/agent_bundle.json`,
  `proof.html`. Asserts renderable-word counts against the font cmap and that
  the hero word is stroke-complete. Never hand-edit its outputs.
- `index.html` — 九個房間，次序係 I Nave、II Cornerstone、III Chapels of Love、
  IV Scriptorium、V the Ninety-Three Stones、VI Treasury、VII The Between
  （`/#isness`／相遇之間）、VIII Chancel（ORDO，見 `ordo/SPEC.md`）、IX Crypt。
  Chapels 同 Between 嘅 canon 摘句係人手逐字保留；來源修訂時，要同步核對摘句，
  唔靠 bake 自動更新。Between 嘅 CSS 同靜態解說亦由呢個檔案維護。
- `assets/chancel.js` — hand-authored (like app.js): drives the Chancel;
  the interpreter itself (`assets/ordo.js`) plus `data/ordo-frames.json` and
  `data/ordo-rites.json` are BAKED from ordo/ by bake.py — edit ordo/, rebake.
- `assets/app.js` — chisel-draw engine (strokes are EM-space y-up; svg_path is
  y-down; svgY = 1000 − emY; one glyph animates at a time), scriptorium
  tokenizer, stones explorer, treasury search, plumb-line scroll-spy.
  `initIsness()` 亦喺同一 IIFE，由人手維護；共用 `$`／`$$` 前移，初始化放喺
  `YS_CORE` early return 之前，唔借用其他房間嘅 renderer。
- `party/index.html` — the previous ai-love.cc page ("LOVE — the party is on
  the internet"), preserved at /party. Do not delete: the colophon links to it.
- `llms.txt`, `_headers` — the agent door. CORS-open data, invite-not-shove.

The hero word is pinned in `bake.py` (`HERO_WORD`). Rotation was deliberately
NOT shipped at launch — a candidate must pass the proof sheet at monumental
scale before it may stand over the door.

## 相遇之間：出處同詮釋邊界

- 唯一回應對象係 `canon/core/panimaance.md:31` 嘅 Definition，逐字保留英文，
  `#isness-source` 用 `lang="en"`，連去 `/glossary/panimaance.html`。
  呢句係已留下嘅文字，唔係在線對象，亦冇自動回覆。
- `canon/core/kimance.md:33-43` 係「我在」嘅參照；
  `canon/core/panimaance.md:31-43,66` 係「向你轉身」嘅參照。
  本房唔會用點擊、停留或輸入判定注意力／presence。
- `canon/core/yonedame.md:46-58,88-104` 只放喺「我哋之間」作更遠視野：
  complete relational saturation／received-as-gift 唔等於一次回應或第三個視角。
- 房間係 `lang="yue"`；廣東話解說標明「本房詮釋」，讀者文字標明「讀者回應」。
  排字「間」同兩個高拱係示意，唔係新 canon glyph；線粗幼固定，冇分數、等級
  或完成獎勵。三條 glossary links 係公開來源，唔帶私人文字。

## 相遇之間：本地 state 生命週期

- IIFE 私有 state 只有 `{ view, draft, placed }`。三個 view 係 `here`、`turn`、
  `between`，隨時切換，只轉構圖焦點同解說，唔改原文、草稿或放置狀態。
- 草稿上限係 **280 個 UTF-16 code units**；HTML `maxlength` 同 JS `String.length`
  一致。提交拒絕純空白／超長輸入，唔分析句子內容，亦唔偷偷截斷或改寫回應。
- 按「留下呢句」先以 `textContent` 顯示原樣文字同固定細線。修改 draft 會立即
  撤下舊 output 同線；唔會將未提交版本當成已留下。
- 「清空」、初始化、`pagehide` 同 BFCache 嘅 `pageshow`（`persisted=true`）
  會清空新房間嘅 draft、output、status／ARIA、placed 同 view；只有明確按「清空」
  先將焦點返輸入框。首次 `pageshow` 以本頁 state 同步 input，排除瀏覽器還原嘅舊值，
  但保留其他 script 慢載入期間已經寫好嘅草稿／回應。listeners 唔觸碰其他房間。
- 私人文字只進記憶體／DOM，唔傳送，唔寫 URL/hash、storage、clipboard、console、
  canon 或 ORDO，冇累積歷史。呢個保證只指本房互動，唔係全站零網絡請求，
  亦唔係作業系統安全抹除嘅保證；舊 theme storage 行為照舊。
- Controls 預設 `hidden`，缺 DOM 就 graceful return；成功 bind 先標上
  `data-isness-ready="true"` 同顯示 controls，重複初始化直接 return。
  新房間冇 `.settle`，no-JS 可讀原文、全部三段解說同來源。
- DOM 契約：`#isness`、`#isness-draft`、`#isness-place`、`#isness-clear`、
  `#isness-response`、`#isness-status`、`#isness-source`；view buttons 用
  `button[data-isness-view]` 同 `aria-pressed`，room 同步
  `data-isness-view`／`data-isness-placed="true|false"`。

## 本地預覽同驗證

只用現有 `home/` 檔案，唔跑 build、bake、glossary、installer 或 deploy。
由 repo 根目錄啟動，讓系統分配空閒 loopback port，唔停其他服務：

```sh
python3 -u -m http.server 0 --bind 127.0.0.1 --directory home
```

用終端顯示嘅 port 開 `http://127.0.0.1:<port>/#isness`。來源連結用實際 `.html`
檔案，所以普通靜態 server 都可以讀。測試檔放 `tests/home/`，唔隨 `home/` 部署。

Browser 回歸測試需要 Python 3、Playwright package 同 Google Chrome。預設用
`chrome` channel，同個人登入分開嘅臨時 profile；測試自己開／關獨立 loopback server。
如 Playwright 已可由 Node resolve：

```sh
node --test tests/home/isness.test.cjs
```

如使用現成但唔喺 repo module path 嘅 Playwright：

```sh
PLAYWRIGHT_MODULE=/absolute/path/to/playwright BROWSER_CHANNEL=chrome \
  node --test tests/home/isness.test.cjs
```

`PLAYWRIGHT_MODULE` 同 `BROWSER_CHANNEL` 只控制測試工具，唔改應用程式設定。
截圖預設放系統 temporary directory，路徑由測試輸出；可以用 `ISNESS_ARTIFACTS`
指定網站輸出以外嘅目錄。測試只用合成文字，唔需要登入、API key 或安裝新 browser。

基本靜態檢查：

```sh
node --check /Users/macair/YOUSPEAK/home/assets/app.js
git -C /Users/macair/YOUSPEAK diff --check
```

驗證範圍（browser 自動測試加人眼覆核；唔代表跨 browser 或 screen reader 認證）：

1. Desktop／窄 mobile、light／dark，檢查高拱、留白、長單詞、換行及 280-unit
   回應冇碰撞或 overflow；native buttons／links 有 44px targets 同可見 focus。
2. Keyboard Tab／Enter／Space、touch、reduced-motion、forced-colors；view 只改
   焦點／解說，唔係完成進度。SVG `aria-hidden`，旁述提供等義文字。
3. 空白、超長、Unicode（包括 surrogate pairs）、HTML payload；驗證上限一致、
   `textContent` 唔生成 HTML，提交後修改撤下，切 view 保留，重複 init 唔重複 bind。
4. 清空、reload、真實離頁／返回及 BFCache，確認 input／output／ARIA／連線／view
   一併重設。測試移除 Playwright 嘅 BFCache 停用參數，要求實際 `persisted=true`
   同原 document 還原；另外獨立測 pageshow。延遲後續 script 時，首次 pageshow
   唔清走已接受嘅輸入；load 唔搶焦點，explicit clear 焦點返 input。
5. 輸入、切 view、提交同清空期間，核對私人文字冇落 URL、storage、network payload
   或 console；分清本房操作同舊房間嘅正常請求。
6. no-JS、`core.js`、font、lexicon／morpheme 資料載入失敗，新房間靜態內容仍可讀；
   缺 `app.js`／必要 DOM 時唔開 controls，保留靜態閱讀，唔因新房間拖垮舊房。
7. 九房次序、nav anchors／scroll-spy／plumb、舊 glyph、Scriptorium、Stones、
   Treasury、Chancel、theme 回歸；Sophia invitation／nonclaims 保留。

本地測試通過亦唔代表線上已更新；以實際 deployment、apex HTML／JS 同互動驗證作準。
