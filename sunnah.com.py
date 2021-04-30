from import_modules import *
from jild_hadith_parsing import *


book_jild_json = {}


all_jild_links = get_all_jild_links(book_url)

for jild_link in all_jild_links[:]:
    book_jild_jsons = []
    book_jild_json = {}

    print(jild_link)

    jild_response = protect_get_connection_error(url=jild_link)
    jild_soup = BeautifulSoup(jild_response.content, 'html5lib')

    book_title_text = get_book_title(jild_soup)

    book_jild_json['title'] = book_title_text
    book_jild_json = initialize_book_jild_json(book_jild_json)

    file_name = book_title_text.split('/')[-1]

    main_div = jild_soup.find('div', class_='AllHadith').find_all('div')
    hadith_divs = get_all_hadith_divs(jild_soup)
    chapter_json = {}
    print(len(main_div))
    count = 0

    for cr_div in main_div:
        count += 1
        div_class = ' '.join(cr_div['class'])
        if div_class == 'chapter':
            print(f'{count}-----------------{div_class}')
            if chapter_json:
                print(f'if -----------{chapter_json.keys()}')
                book_jild_json['children'].append(chapter_json)
                chapter_json = {}

            chapter_json["string"] = get_chapter_name(cr_div)
            chapter_json["heading"] = 3
            chapter_json["children"] = []

        elif div_class == "actualHadithContainer hadith_container_riyadussalihin":
            print(f'{count}-----------------{div_class}')
            hadith_json = get_hadith_json(cr_div)
            chapter_json["children"].append(hadith_json)

    book_jild_json['children'].append(chapter_json)

    book_jild_jsons.append(book_jild_json)
    print(f'{len(book_jild_jsons)}')
    print(f'{file_name}')

    with open(f'All_Books/{file_name}.json', 'a') as outfile:
        json.dump(book_jild_jsons, outfile)
