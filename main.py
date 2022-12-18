import requests
import json
import os
import re

file_path = 'KJV_unprocessed.sog'

if os.path.exists(file_path):
    os.remove(file_path)


def run():
    all_data = requests.get(
        'https://cloud.eternalwords.net/ext/readeronline/bible/2')
    all_book = json.loads(all_data.text)

    for book in all_book:
        glava_list_req = requests.get(
            f'https://cloud.eternalwords.net/ext/readeronline/bible/2/{book["number"]}')
        glava_list_str = glava_list_req.text
        glava_list = glava_list_str[1:-1].split(',')

        for glava_num in glava_list:
            glava_data = requests.get(
                f'https://cloud.eternalwords.net/ext/readeronline/bible/2/{book["number"]}/{int(glava_num)}')
            glava_current = json.loads(glava_data.text)

            for stih in glava_current:
                # Удалить тег с содержимым <f>*</f>
                stih_final = re.sub(
                    r'\<f\>[^>]*\<\/f\>', '', glava_current[stih])
                # Удалить тег с содержимым <s>*</s>
                stih_final = re.sub(r'\<s\>[^>]*\<\/s\>', '', stih_final)
                # Удалить все остальные теги
                stih_final = re.sub(r'\<[^>]*\>', '', stih_final)

                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write(
                        f"{book['title']}\t{glava_num}\t{stih}\t{stih_final}\n")

                # print(
                #     f"{book['title']}\t{glava_num}\t{stih}. {stih_final}")


def main():
    run()


if __name__ == '__main__':
    main()
