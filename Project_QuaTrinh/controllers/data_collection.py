import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

class DataDownloader:
    def __init__(self, url=None):
        """Khởi tạo bộ thu thập dữ liệu"""
        self.url = url
        self.soup = None

    def fetch_webpage(self, url):
        """Dùng Selenium để lấy HTML đầy đủ"""
        try:
            options = Options()
            options.headless = True  # Chạy trình duyệt ẩn (không hiển thị cửa sổ)
            options.add_argument("--disable-blink-features=AutomationControlled")  # Tránh bị phát hiện là bot

            # Khởi chạy ChromeDriver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)

            # Đợi trang web tải đầy đủ (5 giây, có thể tăng nếu trang load chậm)
            driver.implicitly_wait(5)

            # Lấy HTML đầy đủ
            html = driver.page_source
            driver.quit()

            # Parse HTML bằng BeautifulSoup
            self.url = url
            self.soup = BeautifulSoup(html, "html.parser")

            # # Lưu HTML vào file để kiểm tra
            # with open("full_page.html", "w", encoding="utf-8") as f:
            #     f.write(self.soup.prettify())

            # print("✅ Đã lưu HTML vào full_page.html, hãy mở file để kiểm tra.")
            return self.soup.prettify()

        except Exception as e:
            return f"❌ Lỗi khi tải trang: {e}"

    def get_all_classes(self):
        """Trích xuất tất cả class có trong trang"""
        if self.soup is None:
            return []

        class_list = set()
        for tag in self.soup.find_all(True):  # Lấy tất cả thẻ
            if tag.get("class"):
                class_list.update(tag.get("class"))

        return sorted(class_list)  # Trả về danh sách class đã sắp xếp

    def get_sub_classes(self, list_class):
        """Lấy danh sách các class con bên trong danh sách chính"""
        if self.soup is None:
            return []

        parent_elements = self.soup.find_all(class_=list_class)
        if not parent_elements:
            return []

        sub_class_list = set()
        for parent in parent_elements:
            for tag in parent.find_all(True):  # Lấy tất cả thẻ con trong danh sách chính
                if tag.get("class"):
                    sub_class_list.update(tag.get("class"))

        return sorted(sub_class_list)

    def extract_data(self, list_class, column_classes):
        """Trích xuất dữ liệu từ danh sách chính + tối đa 5 cột"""
        if self.soup is None:
            return "❌ Chưa có trang web nào được tải. Vui lòng nhập URL trước."

        items = self.soup.find_all(class_=list_class)
        if not items:
            return "⚠️ Không tìm thấy danh sách với class đã nhập."

        data = []
        for item in items:
            row = []
            for col_class in column_classes:
                col = item.find(class_=col_class)
                row.append(col.text.strip() if col else "N/A")
            data.append(row)

        df = pd.DataFrame(data, columns=[f"Cột {i+1}" for i in range(len(column_classes))])
        return df
