import requests
import textwrap
import constant
import _json
from requests_oauthlib import OAuth1
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
#deploy
class Media:
    def __init__(self):
        print("Initialize media..")

    def download_image(self,media_url):
        arr = str(media_url).split('/')
        auth = OAuth1(client_key=constant.CONSUMER_KEY,
                      client_secret=constant.CONSUMER_SECRET,
                      resource_owner_secret=constant.ACCESS_SECRET,
                      resource_owner_key=constant.ACCESS_KEY)
        r = requests.get(media_url, auth=auth)

        with open(arr[9], 'wb') as f:
            f.write(r.content)
        image = Image.open(arr[9])
        image.save("ready.png")
        print("Media downloaded successfully!")

    def process_image(self, text, author):
        text = textwrap.fill(text, width=35)
        image = Image.open("downloaded_bg.png").filter(ImageFilter.GaussianBlur(5))
        image = ImageEnhance.Brightness(image)
        image.enhance(0.75).save('image.png')
        image = Image.open('image.png')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('Calistoga-Regular.ttf', size = 29)
        w, h = draw.textsize(text, font = font)
        draw.text(((720 - w) / 2, (720 - h) / 2), text, (255, 255, 255), align="center", font = font)
        if author is not None:
            _author = '@%s' % str(author)
            x, y = draw.textsize(_author, font =  font)
            font = ImageFont.truetype('Livvic-Bold.ttf', size = 20)
            draw.text(((720 - x) / 2, ((720 / 2) + h) + 60), _author, (255, 255, 255),font = font, align="bottom")
        image.save('ready.png')
