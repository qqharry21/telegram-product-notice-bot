# 使用官方的 Python 基礎映像
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 複製當前目錄的內容到工作目錄中
COPY . /app

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 設置環境變量
ENV PRODUCT_URL=https://www.5music.com.tw/CDList-C.asp?cdno=445425679120
ENV TELEGRAM_TOKEN=7110618214:AAGSwNTTPnC0VaJLgrGApc9Vw2KKfK89ESg

# 暴露端口
EXPOSE 5000

# 運行 Flask 應用
CMD ["python", "app.py"]
