file_path = 'TH1.txt'


def read_all_image_urls_from_file(path=file_path):
    path = f'/home/lap15768/Desktop/LRU-Cache/data2/{path}'
    
    urls = []
     
    file = open(path, 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        urls.append(line.strip())
    return urls
