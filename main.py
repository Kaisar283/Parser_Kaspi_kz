from selenium import webdriver
from bs4 import BeautifulSoup
import time
import undetected_chromedriver
import pickle
import json
from functions import find_page_count, normalize_short_discription


def get_data_with_selenium(url):
    try:

        driver = undetected_chromedriver.Chrome()
        driver.get(url)
        time.sleep(3)
        # pickle.dump(driver.get_cookies(), open(f"kaspi_cookies", "wb"))
        # time.sleep(10)
        for cookie in pickle.load(open(f"kaspi_cookies", "rb")):
            driver.add_cookie(cookie)
        time.sleep(3)
        driver.refresh()

        main_page = driver.page_source
        soup = BeautifulSoup(main_page, "lxml")
        page_count = soup.find(class_="search-result__title-count").text
        page_count = find_page_count(page_count)
        products_path = {}
        for page in range(1, page_count + 1):
            driver.get(f"https://kaspi.kz/shop/search/?text=%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D1%8B&page={page}")
            current_page = driver.page_source
            current_page_soup = BeautifulSoup(current_page, 'lxml')
            all_cards = current_page_soup.find_all(class_="item-card__name-link")

            for item in all_cards:
                product_name = item.text
                product_link = item['href']
                products_path[product_name] = product_link
            time.sleep(1)
        with open('Products_links.json', 'w', encoding='utf-8') as file:
            json.dump(products_path, file, indent=4, ensure_ascii=False)

        with open("Products_links.json", "r", encoding='utf-8') as read_file:
            data = json.load(read_file)

        count = len(data)
        print(count)
        for Product_name, Product_link in data.items():
            each_item_info = []
            print(f'Started {count} iteration')
            driver.get(Product_link)
            item_page = driver.page_source
            soup = BeautifulSoup(item_page, 'lxml')
            print(f'create soup {count} iteration')
            item_name = soup.find(class_='item__heading').text
            item_price = soup.find(class_='item__price-once').text
            short_discription = soup.find(class_="item__description-text").text
            short_discription = normalize_short_discription(short_discription)
            seller = soup.find(class_="sellers-table__cell").find('a')
            seller_name = seller.text
            seller_link = 'https://kaspi.kz/' + seller['href']

            each_item_info.append(
                {
                    "Product_name": item_name,
                    "Product_price": item_price,
                    "Seller_name": seller_name,
                    "Seller_link": seller_link,
                    "Short_discription": short_discription
                }
            )
            print(f"finished {count} iteration")
            count -= 1
            time.sleep(1)
            try:
                with open(f'data/all_products_info.json', 'a', encoding='utf-8') as file:
                    json.dump(each_item_info, file, indent=4, ensure_ascii=False)
                    print(f"The recording was successful. Iteration {count}")
            except Exception as ex:
                print(ex)

        time.sleep(3)
        print('Success!')
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_data_with_selenium("https://kaspi.kz/shop/search/?text=%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%BA%D0%BE%D0%BF%D1%8B")

if __name__ == '__main__':
    main()


#  all_products_info