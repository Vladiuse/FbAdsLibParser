def log_links_in_file(links):
    """Записать ссылки из карточек в лог файл"""
    with open('/home/vlad/links.txt', 'a') as file:
        for link in links:
            file.write(link + '\n')