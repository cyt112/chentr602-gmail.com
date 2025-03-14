import requests

# 构造真实的PDF文件URL
pdf_url = "https://cdn035.yun-img.com/static/upload/qfpx620/download/20200425103926_35835.pdf"

# 添加必要的请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.yiqifuwu.com/statics/js/pdf/web/viewer.html"
}

if __name__ == '__main__':
    # 发送GET请求
    response = requests.get(pdf_url, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 保存为PDF文件
        with open("document.pdf", "wb") as f:
            f.write(response.content)
        print("PDF下载成功！")
    else:
        print(f"下载失败，状态码：{response.status_code}")