from cgitb import reset
import youtube_dl
import os


class bcolors:
    # https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def reset_color():
    """
    Seems like print is stateful to whatever color is set, so need to reset it
    """
    print(bcolors.OKCYAN, end="")


class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.save_path = './'

    def download(self):
        if self.is_playlist():
            print("Downloading the playlist!")
            item_urls = self.get_items_from_playlist()
            for i, item_url in enumerate(item_urls):
                print(f"{bcolors.HEADER}Downloading {i+1}/{len(item_urls)}:\n")
                reset_color()
                self.download_mp3(item_url)
        else:
            self.download_mp3(self.url)

    def get_items_from_playlist(self):
        info = youtube_dl.YoutubeDL().extract_info(self.url, download=False)
        items_url_list = []
        for item_info in info['entries']:
            items_url_list.append(item_info['webpage_url'])
        self.save_path += info['title']
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        return items_url_list

    def download_mp3(self, url):
        video_info = youtube_dl.YoutubeDL().extract_info(
            url=url, download=False
        )
        filename = f"{self.save_path}/{video_info['title']}.mp3"
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filename,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        print(bcolors.OKGREEN+"Download complete... {}".format(filename))
        reset_color()

    def is_playlist(self):
        return "playlist" in self.url


def run():
    url = input("please enter youtube video/playlist url:")
    ytd = YouTubeDownloader(url)
    ytd.download()


if __name__ == '__main__':
    run()
