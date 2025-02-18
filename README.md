# NTCU Course Bot

這是一個自動加選課程的爬蟲機器人，適用於國立臺中教育大學（NTCU）的選課系統。  
透過 Selenium 自動登入、解析驗證碼，並定期檢查課程人數，當有空位時自動加選。  

## 📌 功能特色
- 自動登入選課系統
- OCR 辨識驗證碼（支援 Tesseract 與 ddddocr）
- 定時檢查課程人數，並在可加選時自動提交
- 支援無頭模式（Headless）

## 🔧 環境需求
- Python 3.7 以上
- Google Chrome 瀏覽器
- ChromeDriver

## 📦 安裝方式

1. **下載專案**
   ```bash
   git clone https://github.com/jimmy92919/NTCU-Course-Bot.git
   cd NTCU-Course-Bot
2. **安裝依賴套件**
   安裝依賴套件 請使用以下命令安裝所有的依賴套件：

   ```bash
   pip install -r requirements.txt
3. **運行程式**
   運行爬蟲 修改爬蟲配置後，執行下列命令來啟動爬蟲：

   ```bash
   python bot.py
