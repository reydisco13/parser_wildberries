import mechanicalsoup as ms
from bs4 import BeautifulSoup as bs
from time import sleep
import openpyxl


url = 'https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki'
# обходим защиту сайта для парсинга
b = ms.StatefulBrowser()
b.set_user_agent('my-awesome-script')
#создаем файл xlsx формата для записи
book = openpyxl.Workbook()
sheet = book.active
sheet['A1'] = 'ARTICUL'
sheet['B1'] = 'NAME'
sheet['C1'] = 'BASE_PRISE'
sheet['D1'] = 'PRISE'
sheet['E1'] = 'HREF'
sheet['F1'] = 'URL_IMAGE'
sheet['G1'] = 'URL_NOUTBUK'
book.save('wildberries_nouts.xlsx')

def get_html(url):
    r = b.get(url)
    return r.text


def get_total_pages(html):
    soup = bs(html, 'lxml')
    pages = soup.findAll('a', class_='pagination-item')[-1].get_text()
    return int(pages)


def write_xlsx(data, row):
    sheet[row][0].value = data['articul']
    sheet[row][1].value = data['name']
    sheet[row][2].value = data['base_prise']
    sheet[row][3].value = data['prise']
    sheet[row][4].value = data['href']
    sheet[row][5].value = data['url_image']
    sheet[row][6].value = data['url_noutbuk']
    book.save('wildberries_nouts.xlsx')



def main():
    base_url = 'https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki?page='
    row = 2
    for i in range(1, 3):       #(1, total_pages + 1) - если хочешь спарсить все
        url_gen = base_url + str(i)
        print(url_gen)
        soup_n = bs(get_html(url_gen), 'lxml')
        urls_n = soup_n.findAll('div', class_="dtList")
        for i in range(len(urls_n)):
            url_noutbuk = 'https://www.wildberries.ru' + urls_n[i].find('a', class_='ref_goods_n_p').get('href')
            soup_noutbuk = bs(get_html(url_noutbuk), 'lxml')
            sleep(1)
            articul = soup_noutbuk.find('div', class_='article').text.split()[-1]
            name = soup_noutbuk.find('div', class_='brand-and-name').text.strip('\n')
            price1 = soup_noutbuk.find('div', class_='final-price-block').text.split()
            price = price1[0] + price1[1]
            url_image = 'https:' + soup_noutbuk.find('div', id='scrollImage').find('a').get('href')
            data = {
                    'articul': 'AAA'+articul,
                    'name': name,
                    'base_prise': '',
                    'prise': price,
                    'href': url_noutbuk,
                    'url_image': url_image,
                    'url_noutbuk': url_noutbuk,
                    }
            write_xlsx(data, row)
            row += 1


if __name__ == '__main__':
    main()

book.close()

