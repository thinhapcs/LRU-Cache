namespace py tutorial

typedef string str
typedef binary bin
service DownloadImageService {
    bin download_image(1:str url)
}