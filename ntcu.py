import time
import pytesseract
from PIL import Image
from io import BytesIO
import base64
import ddddocr
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    NoSuchElementException,
    UnexpectedAlertPresentException,
)

# 設定 Tesseract 路徑
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def recaptchaByPass(code_image: str) -> str:
    ocr = ddddocr.DdddOcr()
    base64_string = code_image.split(",")[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    res = ocr.classification(image)
    return res


def login_and_check_course():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1280, 800)

    while True:
        try:
            driver.get("https://ecsb.ntcu.edu.tw/")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "User_Account"))
            )

            driver.find_element(By.ID, "User_Account").send_keys("ACS111143")
            driver.find_element(By.ID, "User_Password").send_keys("(Jimmy92919")

            # 透過 Selenium 拿到驗證碼圖片
            captcha_element = driver.find_element(By.ID, "Check_Code_Img")
            captcha_screenshot = captcha_element.screenshot_as_png
            captcha_image = Image.open(BytesIO(captcha_screenshot))

            # 使用 OCR 進行圖片辨識
            captcha_text = pytesseract.image_to_string(
                captcha_image, config="--psm 7"
            ).strip()
            if not captcha_text:
                # 如果 OCR 識別失敗，可以使用 ddddocr 作為備選方案
                code_image = captcha_element.get_attribute("src")
                captcha_text = recaptchaByPass(code_image)

            # 填入驗證碼
            driver.find_element(By.ID, "Check_Code").send_keys(captcha_text)
            driver.find_element(By.ID, "Client_Login").click()

            time.sleep(1)  # 等待登入

            # 檢查是否有彈出警告（驗證碼錯誤）
            try:
                alert = driver.switch_to.alert
                print("驗證碼錯誤，重新嘗試...")
                alert.accept()
                continue  # 重新嘗試
            except Exception:
                pass
            time.sleep(4)
            driver.get("https://ecsb.ntcu.edu.tw/STDWEB/SelChoose/SelChooseMain.aspx")
            time.sleep(2)

            driver.find_element(By.ID, "cmdInquire").click()
            print("已點擊查詢課程！")
            dept_select = Select(driver.find_element(By.ID, "cboDept"))
            dept_select.select_by_visible_text("資工系")
            print("已選擇資工系！")
            driver.find_element(By.ID, "txtGrade").send_keys("3")
            print("已輸入年級！")
            driver.find_element(By.ID, "cmdQueryCur").click()
            print("已點擊查詢！")
            time.sleep(2)
            course_table = driver.find_element(By.ID, "td_cur_list")
            print("已找到課程表格！")
            rows = course_table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                try:
                # 1. 抓取課程名稱（第 5 個 <td>）
                    course_name = row.find_elements(By.TAG_NAME, "td")[4].text.strip()

                # 2. 如果課程名稱是「雲端運算概論」
                    if "雲端運算概論" in course_name:
                        print(f"找到課程：{course_name}")

                    # 3. 抓取人數資訊（第 10 個 <td>）
                        count_text = row.find_elements(By.TAG_NAME, "td")[9].text.strip()

                    # 4. 解析人數 "29/52" -> current_count=29, max_count=52
                        current_count, max_count = map(int, count_text.split("/"))
                        print(f"目前人數: {current_count}/{max_count}")

                    # 5. 如果目前人數小於 29，點擊加選按鈕（第 1 個 <td> 裡的按鈕）
                        
                        add_button = row.find_element(By.CSS_SELECTOR, "input.red_M[value='加選']")
                        add_button.click()
                        print("成功點擊加選按鈕！")
                        time.sleep(120)
                except Exception as e:
                    print(f"處理課程時發生錯誤：{e}")
                    continue
        except NoSuchElementException:
            print("找不到元素，重新整理頁面...")
            driver.refresh()
            time.sleep(2)
        except UnexpectedAlertPresentException:
            print("遇到彈出視窗，可能是驗證碼錯誤，重新嘗試...")
            driver.switch_to.alert.accept()
            time.sleep(2)
        except Exception as e:
            print("發生錯誤：", e)
            driver.refresh()
            time.sleep(2)

    driver.quit()


if __name__ == "__main__":
    while True:
        print("\n===== 開始檢查課程人數 =====")
        login_and_check_course()
