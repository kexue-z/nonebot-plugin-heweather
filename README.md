# nonebot-plugin-heweather

获取和风天气信息并转换为图片

# 配置

## apikey

注意保留 `&key=`

```
QWEATHER_APIKEY = &key=xxx
```

## 字体文件

在`resource`里

默认路径`./data/heweather/font.ttc`

### 环境配置
```
QWEATHER_FONT = "./data/heweather/font.ttc'
```

- 使用 truetype 字体
- 建议使用微软雅黑

## 图标文件

在`resource`里

### 环境配置

**注意**末端的`/`, 代表目录！

默认路径`./data/heweather/icon/`

```
QWEATHER_ICON_DIR = "./data/heweather/icon/'
```

## 背景文件

在`resource`里

### 环境配置

默认路径`./data/heweather/backgroud.png`

```
QWEATHER_ICON_DIR = "./data/heweather/backgroud.png'
```

- [下载地址](https://dev.qweather.com/docs/start/icons/)

# 指令

`天气+地区`

