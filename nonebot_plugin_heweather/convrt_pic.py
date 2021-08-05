import nonebot
from nonebot.log import logger
from PIL import (
    Image, 
    ImageDraw, 
    ImageFont)
from pathlib import Path

font = nonebot.get_driver().config.qweather_font
icon_dir = nonebot.get_driver().config.qweather_icon_dir 

if not font:
    font = str(Path("data/heweather/font.ttc").absolute())
if not icon_dir:
    icon_dir = str(Path("data/heweather/icon").absolute()) + '/'

try:
    s20 = ImageFont.truetype(font, 20)
    s30 = ImageFont.truetype(font, 30)
    s40 = ImageFont.truetype(font, 40)
    s50 = ImageFont.truetype(font, 50)
    s100 = ImageFont.truetype(font, 100)
except OSError:
    raise OSError(f'请检查字体文件和图标文件是否正确放置或配置qweather_font和qweather_icon_dir\n路径:\n{font}\n{icon_dir}')
    
background_hight=700
background_width=1160
mid_box_height=154
mid_box_width=500
bottom_box_height=180
bottom_box_width=1080

    
# 载入天气图标
def load_icon(id) -> Image:
    im = Image.open(icon_dir + id + ".png")
    im = im.convert('RGBA')
    return im
    
def load_small_icon(id) -> Image:

    im = Image.open(icon_dir + id + ".png")
    icon = im.resize((im.width//2, im.height//2))
    icon = icon.convert('RGBA')
    return icon
    
    
# load_icon(data['day1']['iconDay'])
    
def draw(data) -> Image:
    height = 2000
    width = 1200
    
    im = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(im)
    # 背景框1
    d.rounded_rectangle([(20,20),(20+background_width,20+background_hight)], radius = 40, fill = '#DBDBDB')
    d.rounded_rectangle([(60,306),(60+mid_box_width,306+mid_box_height)], radius = 20, fill = '#CCE1EB')
    d.rounded_rectangle([(640,306),(640+mid_box_width,306+mid_box_height)], radius = 20, fill = '#4C4C4C')
    d.rounded_rectangle([(60,500),(60+bottom_box_width,500+bottom_box_height)], radius = 20, fill = '#AAAAAA')
    # 背景框2
    d.rounded_rectangle([(20,740),(20+background_width,740+606)], radius = 40, fill = '#DBDBDB')
    d.rounded_rectangle([(60,932),(60+mid_box_width,932+mid_box_height)], radius = 20, fill = '#CCE1EB')
    d.rounded_rectangle([(640,932),(640+mid_box_width,932+mid_box_height)], radius = 20, fill = '#4C4C4C')
    d.rounded_rectangle([(60,1126),(60+bottom_box_width,1126+bottom_box_height)], radius = 20, fill = '#AAAAAA')
    # 背景框3
    d.rounded_rectangle([(20,1366),(20+background_width,1366+606)], radius = 40, fill = '#DBDBDB')
    d.rounded_rectangle([(60,1558),(60+mid_box_width,1558+mid_box_height)], radius = 20, fill = '#CCE1EB')
    d.rounded_rectangle([(640,1558),(640+mid_box_width,1558+mid_box_height)], radius = 20, fill = '#4C4C4C')
    d.rounded_rectangle([(60,1752),(60+bottom_box_width,1752+bottom_box_height)], radius = 20, fill = '#AAAAAA')
    
    # 今天
    d.text((88, 77), data['city'], fill = 'black', font = s50)
    icon = load_icon(data['now']['icon'])
    im.paste(icon, (370,36), icon)
    d.text((620,58), data['now']['temp']+'°C', fill = 'black', font = s100)
    d.text((620,189), data['now']['text']+'（实时）',fill = 'black', font = s50)
    obsTime = data['now']['obsTime'][5:10] +' '+data['now']['obsTime'][11:16]
    d.text((1012,86), obsTime,fill = 'black', font = s20)
    d.text((936.5,172), data['now']['feelsLike']+'°C',fill = 'black', font = s40)
    d.text((922,218.5), '体感温度',fill = 'black', font = s30)
    # 左中框
    icon = load_small_icon(data['day1']['iconDay'])
    im.paste(icon, (180,316), icon)
    d.text((315,355), data['day1']['textDay'],fill = 'black', font = s50)
    d.text((315,340), '白天',fill = 'black', font = s20)
    # 右中框
    icon = load_small_icon(data['day1']['iconNight'])
    im.paste(icon, (768,316), icon)
    d.text((915,355), data['day1']['textNight'],fill = 'white', font = s50)
    d.text((915,340), '夜间',fill = 'white', font = s20)
    # 底框
    d.text((90,530), data['day1']['uvIndex'],fill = 'black', font = s40)
    d.text((90,584.5), '紫外线指数',fill = 'black', font = s30)
    
    d.text((322,530), data['day1']['humidity']+'%',fill = 'black', font = s40)
    d.text((322,584.5), '相对湿度',fill = 'black', font = s30)
    
    d.text((564,530), data['day1']['precip']+'mm',fill = 'black', font = s40)
    d.text((564,584.5), '降水量',fill = 'black', font = s30)
    
    d.text((800.5,530), data['day1']['windScaleDay']+'级',fill = 'black', font = s40)
    d.text((800,584.5), data['day1']['windDirDay'],fill = 'black', font = s30)
    
    d.text((1008,530), data['day1']['vis']+'km',fill = 'black', font = s40)
    d.text((1008,584.5), '能见度',fill = 'black', font = s30)
    
    #明天
    d.text((377,784), data['day2']['tempMax']+'-'+data['day2']['tempMin']+'°C', fill = 'black', font = s100)
    d.text((550,758), '明天',fill = 'black', font = s50)

    # 左中框
    icon = load_small_icon(data['day2']['iconDay'])
    im.paste(icon, (180,945), icon)
    d.text((315,983.5), data['day2']['textDay'],fill = 'black', font = s50)
    d.text((315,970), '白天',fill = 'black', font = s20)
    # 右中框
    icon = load_small_icon(data['day2']['iconNight'])
    im.paste(icon, (768,938), icon)
    d.text((923,985), data['day2']['textNight'],fill = 'white', font = s50)
    d.text((926,971), '夜间',fill = 'white', font = s20)
    # 底框
    d.text((90,1157), data['day2']['uvIndex'],fill = 'black', font = s40)
    d.text((90,1210.5), '紫外线指数',fill = 'black', font = s30)
    
    d.text((322,1157), data['day2']['humidity']+'%',fill = 'black', font = s40)
    d.text((322,1210.5), '相对湿度',fill = 'black', font = s30)
    
    d.text((564,1157), data['day2']['precip']+'mm',fill = 'black', font = s40)
    d.text((564,1210.5), '预计降水量',fill = 'black', font = s30)
    
    d.text((800.5,1157), data['day2']['windScaleDay']+'级',fill = 'black', font = s40)
    d.text((800,1210.5), data['day2']['windDirDay'],fill = 'black', font = s30)
    
    d.text((1008,1157), data['day2']['vis']+'km',fill = 'black', font = s40)
    d.text((1008,1210.5), '能见度',fill = 'black', font = s30)
    
    # 后天
    d.text((377,1410), data['day3']['tempMax']+'-'+data['day3']['tempMin']+'°C', fill = 'black', font = s100)
    d.text((550,1384), '后天',fill = 'black', font = s50)

    # 左中框
    icon = load_small_icon(data['day3']['iconDay'])
    im.paste(icon, (180,1571), icon)
    d.text((315,1611), data['day3']['textDay'],fill = 'black', font = s50)
    d.text((315,1600), '白天',fill = 'black', font = s20)
    # 右中框
    icon = load_small_icon(data['day3']['iconNight'])
    im.paste(icon, (768,1571), icon)
    d.text((925,1611), data['day3']['textNight'],fill = 'white', font = s50)
    d.text((925,1600), '夜间',fill = 'white', font = s20)
    # 底框
    d.text((90,1780), data['day3']['uvIndex'],fill = 'black', font = s40)
    d.text((90,1836.5), '紫外线指数',fill = 'black', font = s30)
    
    d.text((322,1780), data['day3']['humidity']+'%',fill = 'black', font = s40)
    d.text((322,1836.5), '相对湿度',fill = 'black', font = s30)
    
    d.text((564,1780), data['day3']['precip']+'mm',fill = 'black', font = s40)
    d.text((564,1836.5), '预计降水量',fill = 'black', font = s30)
    
    d.text((800.5,1780), data['day3']['windScaleDay']+'级',fill = 'black', font = s40)
    d.text((800,1836.5), data['day3']['windDirDay'],fill = 'black', font = s30)
    
    d.text((1008,1780), data['day3']['vis']+'km',fill = 'black', font = s40)
    d.text((1008,1836.5), '能见度',fill = 'black', font = s30)
    
    return im
    