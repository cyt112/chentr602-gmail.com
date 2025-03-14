import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置下载路径
download_dir = r"D:\各省份各月份电网电价"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 设置Chrome浏览器
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式运行，不显示浏览器窗口
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_experimental_option('prefs', {
    "download.default_directory": download_dir,  # 设置下载路径
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True  # 设置为True时，PDF会自动在外部程序中打开，而不是在浏览器中打开
})
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 打开目标网站
url = "https://www.95598.cn/osgweb/ipElectrovalenceStandard"
driver.get(url)


def click_text(expected_text):
    try:
        # 使用显式等待找到包含目标文字的元素
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{expected_text}')]"))
        )
        # 点击该元素
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        print(f"未识别到目标文字 {expected_text}")


def click_element(xpath):
    try:
        # 使用显式等待找到元素
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        # 滚动到元素
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # 点击该元素
        driver.execute_script("arguments[0].click();", element)
        print(f"成功点击元素: {xpath}")
    except Exception as e:
        print(f"未找到元素 {xpath}")


def rename_latest_file(province):
    """
    重命名最新下载的文件为“省份+2月.pdf”
    """
    # 获取下载目录中的所有文件
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    # 按修改时间排序，获取最新的文件
    latest_file = max(files, key=os.path.getmtime)
    # 新文件名
    new_file_name = os.path.join(download_dir, f"{province}.pdf")
    # 重命名文件
    os.rename(latest_file, new_file_name)
    print(f"文件已重命名为: {new_file_name}")


provinces = [
    "浙江", "安徽", "北京", "重庆", "江苏", "江西", "黑龙江", "陕西", "辽宁", "上海",
    "四川", "河南", "宁夏", "青海", "福建", "吉林"
]

for province in provinces:
    print(f"正在处理省份: {province}")

    # 当前页面选取网页元素关闭
    click_element('//i[@data-v-40fe627e and contains(@class, "el-icon-close dele")]')

    # 当前选取网页元素<div data-v-07831be2="" id="city_select" class="l left">
    click_element('//div[@data-v-07831be2 and contains(@class, "l left")]')

    # 点击网页元素<a data-v-07831be2="" href="javascript:;" class="f66 fsize14"> 替换为当前省份
    click_element(f'//a[@data-v-07831be2 and contains(text(), "{province}")]')

    # 点击第一个符合条件的<li>元素
    click_element('(//li[@data-v-40fe627e and @class="tab-con-box-li"])[27]')
    time.sleep(2)

    # 根据省份调整列表项索引
    if province in ["四川", "河南"]:
        target_index = 50
    elif province in ["青海", "宁夏"]:
        target_index = 34
    elif province in ["福建", "吉林"]:
        target_index = 38
    else:
        # 其他省份保持42
        target_index = 42

#天津河北湖北山东陕西新疆42 湖南50 内蒙26-28 是图片，冀北属于河北但是pdf名称需要区别

    # 点击对应的列表项
    click_element(
        '(//li[@data-v-40fe627e and @class="tab-con-box-li"])[{target_index}]'.format(target_index=target_index))

    # 处理代理购电
    click_text('代理购电')
    # 修改月份
    click_text('3月')

    # 下载PDF（假设会自动跳转到包含PDF的页面）
    time.sleep(5)  # 等待PDF下载完成，时间可能需要根据网络速度调整

    # 重命名文件
    rename_latest_file(province)

    # 返回原始页面
    driver.get(url)
    print(f"省份 {province} 处理完成，返回原始页面")

# 关闭浏览器
driver.quit()
