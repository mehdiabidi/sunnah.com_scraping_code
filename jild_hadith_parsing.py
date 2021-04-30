from import_modules import *

def get_all_jild_links(book_url):
    jild_links = []

    book_response = protect_get_connection_error(url=book_url)
    soup = BeautifulSoup(book_response.content, 'html5lib')

    jild_link_tags = soup.find_all('div', class_="book_title title")

    for jild_link_tag in jild_link_tags:
        link_tag = jild_link_tag.find('a')
        jild_link = link_tag['href']

        jild_links.append(str(base_url)+str(jild_link))

    return jild_links


def initialize_book_jild_json(b_jild_json):

    b_jild_json["children"] = []

    return b_jild_json


def get_all_hadith_divs(jild_soup):
    hadith_divs = jild_soup.find_all(
        'div', class_="actualHadithContainer hadith_container_riyadussalihin")
    return hadith_divs


def get_chapter_name(ch_div):
    chaper_no_tag = ch_div.find('div', class_="echapno")
    chaper_no_tag_text = chaper_no_tag.text
    chaper_tag = ch_div.find('div', class_="englishchapter")
    chaper_name_text = chaper_tag.text
    return str(chaper_no_tag_text) + str(chaper_name_text)


def get_book_title(jild_soup):
    book_title_tag = jild_soup.find('div', class_='crumbs')
    book_title__tag_text = book_title_tag.text
    book_title_text_partial = book_title__tag_text.replace(
        'Home', '').replace(' » ', '/')
    book_title_text = str('hadith') + str(book_title_text_partial)
    return book_title_text


def get_hadith_and_nataraion_text(dev_text):
    reg = r'\[.{0,40}\]'
    mo = re.search(reg, dev_text)
    h_text = dev_text
    hadith_info = " "
    try:
        h_text = dev_text[:mo.span()[0]]+dev_text[mo.span()[1]:]
        hadith_info = mo.group()
    except:
        traceback.print_exc()

    obj = {
        'hadith_text': h_text,
        'hadith_info': hadith_info
    }
    return obj


def get_hadith_json(hadith_div):
    global base_url
    hadith_json = {}
    hadith_and_nataraion_text_obj = get_hadith_and_nataraion_text(
        hadith_div.find('div', class_="text_details").text)

    hadith_json['string'] = hadith_and_nataraion_text_obj['hadith_text']

    hadith_json['children'] = []

    natarion_json = {}
    try:
        natarion_json['string'] = hadith_div.find(
            'div', class_='hadith_narrated').text

    except:
        natarion_json['string'] = ''
        traceback.print_exc()
        print(hadith_json['string'])

    hadith_info_json = {}

    info_addr = hadith_div.find('table', class_="hadith_reference")
    info_addr_trs = info_addr.find_all('td')
    info_addr_tr = info_addr_trs[1]
    info_addr_tr_text = info_addr_tr.text.split('\xa0')[-1]
    info_addr_tr_link = info_addr_tr.find('a')['href']
    try:

        info_addr_tr_text1 = hadith_and_nataraion_text_obj['hadith_info']
    except:
        info_addr_tr_text1 = ' '
        traceback.print_exc()
        print(hadith_json['string'])

    hadith_info_json['string'] = f'{info_addr_tr_text1}' + \
        f'- [Source]({base_url}{info_addr_tr_link})'

    hadith_json['children'].append(natarion_json)
    hadith_json['children'].append(hadith_info_json)
    return hadith_json

