file_path = 'data2/TH1.txt'


def read_all_image_urls_from_file(path=file_path):
    urls = []

    file = open(path, 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        urls.append(line.strip())
    return urls
