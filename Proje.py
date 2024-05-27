from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
import os

driver = webdriver.Chrome()

kullanici_adi = []
yorumlar = []
ozellikler = []


def Isim():
    url = "https://www.gaming.gen.tr/urun/261368/gaming-6600-amd-ryzen-5-5500-asus-radeon-dual-rx-6600-8gb-16gb-ram-500gb-m-2-ssd-gaming-bilgisayar/"
    driver.get(url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    name = soup.find("h1", class_="product_title entry-title").text.strip()
    return name


def Fiyat():
    url = "https://www.gaming.gen.tr/urun/261368/gaming-6600-amd-ryzen-5-5500-asus-radeon-dual-rx-6600-8gb-16gb-ram-500gb-m-2-ssd-gaming-bilgisayar/"
    driver.get(url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    st1 = soup.find("ins")
    price = st1.find("span", class_="woocommerce-Price-amount").text
    return price


def Ozellikler():
    url = "https://www.gaming.gen.tr/urun/261368/gaming-6600-amd-ryzen-5-5500-asus-radeon-dual-rx-6600-8gb-16gb-ram-500gb-m-2-ssd-gaming-bilgisayar/"
    driver.get(url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    features = soup.find_all("div", class_="su-table")

    for feature in features:
        rows = feature.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            selected_columns = [column.text.strip() for i, column in enumerate(columns) if i == 1]
            for value in selected_columns:
                ozellikler.append(value)
    print(f"Özellikleri: {ozellikler}")


def Yorum():
    i = 1
    while i < 4:

        url = f"https://www.gaming.gen.tr/urun/261368/gaming-6600-amd-ryzen-5-5500-asus-radeon-dual-rx-6600-8gb-16gb-ram-500gb-m-2-ssd-gaming-bilgisayar/comment-page-{i}/#comments"
        driver.get(url)
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        comments = soup.find_all("div", class_="comment-text")

        for comment in comments:
            user_name = comment.find("strong", class_="woocommerce-review__author").text.strip()
            kullanici_adi.append(user_name)
            comment_text = comment.find("div", class_="description").text.strip()
            yorumlar.append(comment_text)
        i = i + 1

    print(f"Kullanıcı: {kullanici_adi}\nYorum: {yorumlar}")


def Puan():
    url = "https://www.gaming.gen.tr/urun/261368/gaming-6600-amd-ryzen-5-5500-asus-radeon-dual-rx-6600-8gb-16gb-ram-500gb-m-2-ssd-gaming-bilgisayar/"
    driver.get(url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rating = soup.find("strong", class_="rating").text
    return rating


isim = Isim()
print("Ürünün ismi: ", isim)
fiyat = Fiyat()
print("Fiyatı: ", fiyat)
puan = Puan()
print("Puanı: ", puan)
Ozellikler()
Yorum()
driver.quit()

db_name = "deneme.db"

if os.path.exists(db_name):
    os.remove(db_name)
    conn = sqlite3.connect(db_name)
else:
    conn = sqlite3.connect(db_name)

bag = conn.cursor()
query = """
         CREATE TABLE IF NOT EXISTS veriler1 (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         fiyat TEXT NOT NULL,
         puan TEXT NOT NULL
         )
         """
bag.execute(query)

con = sqlite3.connect(db_name)
cur = con.cursor()
query = """
         INSERT INTO veriler1
         (fiyat, puan)
         VALUES (?,?)
         """
degerler = (fiyat, puan)
cur.execute(query, degerler)
con.commit()

bag = conn.cursor()
query = """
         CREATE TABLE IF NOT EXISTS veriler2 (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         ozellikler TEXT NOT NULL
         )
         """
bag.execute(query)

con = sqlite3.connect(db_name)
cur = con.cursor()
values = [(ozellik,) for ozellik in ozellikler]
cur.executemany('INSERT INTO veriler2 (ozellikler) VALUES (?)', values)

con.commit()

bag = conn.cursor()
query = """
         CREATE TABLE IF NOT EXISTS veriler3 (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         kullanici_adi TEXT NOT NULL,
         yorumlar TEXT NOT NULL

         )
         """
bag.execute(query)

con = sqlite3.connect(db_name)
cur = con.cursor()
values = [(kullanici_adi, yorum) for kullanici_adi, yorum in zip(kullanici_adi, yorumlar)]
cur.executemany('INSERT INTO veriler3 (kullanici_adi,yorumlar) VALUES (?, ?)', values)

con.commit()

print("Veriler başarıyla SQLite veritabanına eklendi.")