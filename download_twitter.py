import requests
import os
from urllib.parse import unquote

def download(data_list):
    """
    遍历字典数组，下载每个字典中url键指定的文件
    
    Args:
        data_list: 字典列表，每个字典应包含'url'键，可选'filename'键
    """
    for i, item in enumerate(data_list):
        try:
            # 检查字典中是否包含url键
            if 'url' not in item:
                print(f"错误: 第{i}个元素缺少'url'键")
                continue
                
            url:str = item['url']
            url = url.replace("video.twimg", "video-t-2.twimg")
            
            # 获取文件名：优先使用字典中的filename，否则从URL提取
            if 'filename' in item:
                filename = item['filename']
            else:
                # 从URL中提取文件名
                filename = unquote(url.split('/')[-1])
                if not filename or '.' not in filename:
                    # 如果无法从URL获取有效文件名，使用默认命名
                    filename = f'downloaded_file_{i}.bin'
            
            print(f"开始下载: {url} -> {filename}")
            
            # 发送GET请求，启用流式下载以便处理大文件
            response = requests.get(url, stream=True)
            response.raise_for_status()  # 检查请求是否成功
            
            # 写入文件
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # 过滤掉保持连接的空块
                        file.write(chunk)
            
            print(f"成功下载: {filename}")
            
        except requests.exceptions.RequestException as e:
            print(f"下载失败 (第{i}个文件): {str(e)}")
        except Exception as e:
            print(f"发生未知错误 (第{i}个文件): {str(e)}")

# 使用示例
if __name__ == "__main__":
    # 示例数据
    sample_data = {
  "account_info": {
    "name": "lulu463098",
    "nick": "猫头菜",
    "date": "2025-04-08 21:31:56",
    "followers_count": 73701,
    "friends_count": 99,
    "profile_image": "https://pbs.twimg.com/profile_images/1915910559968759808/V3aR0wjp.jpg",
    "statuses_count": 106
  },
  "total_urls": 61,
  "timeline": [
    {
      "url": "https://video.twimg.com/ext_tw_video/1976106839063527427/pu/vid/avc1/720x1280/7CBI6WMZ2TF6OI8K.mp4?tag=12",
      "date": "2025-10-09 02:06:05",
      "tweet_id": 1.9761068657812444e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1975402835128033282/pu/vid/avc1/720x1280/9fTVp5CGY_yQ5wKV.mp4?tag=12",
      "date": "2025-10-07 03:28:39",
      "tweet_id": 1.9754028658680873e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1975025540630540288/pu/vid/avc1/696x1280/HCq7GJWOm9YK5BoS.mp4?tag=12",
      "date": "2025-10-06 02:29:26",
      "tweet_id": 1.9750255755899945e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1973532938609524736/pu/vid/avc1/720x1280/EsEGtM9R4snnklJM.mp4?tag=12",
      "date": "2025-10-01 23:38:22",
      "tweet_id": 1.9735329736025787e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1973287812020707333/pu/vid/avc1/720x1280/0Qkb09p6W0nVh6I1.mp4?tag=12",
      "date": "2025-10-01 07:24:19",
      "tweet_id": 1.9732878489474583e+18,
      "type": "video"
    },
    {
      "url": "https://pbs.twimg.com/media/G2Cz64za8AACSk8?format=jpg&name=orig",
      "date": "2025-09-29 21:24:19",
      "tweet_id": 1.9727744639190346e+18,
      "type": "photo"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1972644618312544256/pu/vid/avc1/720x1280/Em782GGzD5x2miyz.mp4?tag=12",
      "date": "2025-09-29 12:48:29",
      "tweet_id": 1.9726446521144445e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1972207614366044162/pu/vid/avc1/696x1280/HSPapDS-W8ODgqTl.mp4?tag=12",
      "date": "2025-09-28 07:51:58",
      "tweet_id": 1.9722076408278756e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1971881396890476544/pu/vid/avc1/696x1280/WT510qVxormRqB--.mp4?tag=12",
      "date": "2025-09-27 10:16:07",
      "tweet_id": 1.971881529317249e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1970025377411268608/pu/vid/avc1/696x1280/qTZbfczxOIZRXovt.mp4?tag=12",
      "date": "2025-09-22 07:20:35",
      "tweet_id": 1.970025419295564e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1968538229315092482/pu/vid/avc1/720x1280/kYmyz_y-h2uWvaNE.mp4?tag=12",
      "date": "2025-09-18 04:51:16",
      "tweet_id": 1.9685382876701862e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1968150156773367808/pu/vid/avc1/696x1280/RBcQsbuoSdZIW13P.mp4?tag=12",
      "date": "2025-09-17 03:09:20",
      "tweet_id": 1.9681502508935662e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1967868245689659392/pu/vid/avc1/696x1280/jDOETKpL-Re2dxVx.mp4?tag=12",
      "date": "2025-09-16 08:29:03",
      "tweet_id": 1.9678683219882191e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1965250408303263748/pu/vid/avc1/720x1280/HDv5LKGGifT0xtFq.mp4?tag=12",
      "date": "2025-09-09 03:06:35",
      "tweet_id": 1.9652504530229332e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1962304415488241664/pu/vid/avc1/720x1280/3M41tV_8b_htLnYP.mp4?tag=12",
      "date": "2025-09-01 00:00:19",
      "tweet_id": 1.9623044770186693e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1955913343589605381/pu/vid/avc1/720x1280/bUc58pGWsuak40ZM.mp4?tag=12",
      "date": "2025-08-14 08:44:24",
      "tweet_id": 1.9559133829615375e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1955910780530122754/pu/vid/avc1/720x1280/TKg-veYBQ5yMPNQP.mp4?tag=12",
      "date": "2025-08-14 08:34:19",
      "tweet_id": 1.9559108452356918e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1954802891858067456/pu/vid/avc1/720x1280/pPlL-iQMzGdTFAfK.mp4?tag=12",
      "date": "2025-08-11 07:11:50",
      "tweet_id": 1.9548029264062917e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1953312076908400640/pu/vid/avc1/720x1280/HshBPBN7reuK4Jnr.mp4?tag=12",
      "date": "2025-08-07 04:27:55",
      "tweet_id": 1.953312122269778e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1953311379966119936/pu/vid/avc1/720x1280/a7BpJQqrmDAuXK24.mp4?tag=12",
      "date": "2025-08-07 04:25:55",
      "tweet_id": 1.953311619418583e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1950143836220772352/pu/vid/avc1/720x1280/NImgvETPMTvowlRE.mp4?tag=12",
      "date": "2025-07-29 10:38:24",
      "tweet_id": 1.9501438678539348e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1950143682856046594/pu/vid/avc1/720x1280/4lDDjsyfySC9rTrB.mp4?tag=12",
      "date": "2025-07-29 10:37:48",
      "tweet_id": 1.9501437152568159e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1948322264384167936/pu/vid/avc1/720x1280/otbbuSTyiS9ZoujA.mp4?tag=12",
      "date": "2025-07-24 10:00:07",
      "tweet_id": 1.9483222923225175e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1948320999314976768/pu/vid/avc1/568x1280/pN-xm1mRBC4dMxi0.mp4?tag=12",
      "date": "2025-07-24 09:55:50",
      "tweet_id": 1.9483212169193761e+18,
      "type": "video"
    },
    {
      "url": "https://pbs.twimg.com/media/GwRG8JIXIAAgnc-?format=jpg&name=orig",
      "date": "2025-07-20 02:27:55",
      "tweet_id": 1.9467589405928986e+18,
      "type": "photo"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1946467108797427712/pu/vid/avc1/720x1280/MuBDfVWixdcKaIUJ.mp4?tag=12",
      "date": "2025-07-19 07:08:25",
      "tweet_id": 1.9464671435260928e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1942455737529282560/pu/vid/avc1/720x1280/bni23jls1Wn-O6U2.mp4?tag=12",
      "date": "2025-07-08 05:28:41",
      "tweet_id": 1.9424557798663785e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1942455654146347008/pu/vid/avc1/720x1280/oAEY8FwEe7Kz9YrM.mp4?tag=12",
      "date": "2025-07-08 05:28:41",
      "tweet_id": 1.9424557778365565e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1940927584688021504/pu/vid/avc1/720x1280/nwdSlsnNKQlDesbp.mp4?tag=12",
      "date": "2025-07-04 00:16:22",
      "tweet_id": 1.9409276327593126e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1940927330891038720/pu/vid/avc1/720x1280/hfM_84Q7tSlUt522.mp4?tag=12",
      "date": "2025-07-04 00:15:21",
      "tweet_id": 1.9409273735806853e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1940063088847273985/pu/vid/avc1/696x1280/cvAUbSjJNZUHdre0.mp4?tag=12",
      "date": "2025-07-01 15:01:09",
      "tweet_id": 1.9400631316672433e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1940063008622825472/pu/vid/avc1/696x1280/xu4QpanBxLaf3WSA.mp4?tag=12",
      "date": "2025-07-01 15:01:09",
      "tweet_id": 1.9400631291128545e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1939498211846008832/pu/vid/avc1/720x1280/Yj7a0vpkeSfjabpq.mp4?tag=12",
      "date": "2025-06-30 01:36:56",
      "tweet_id": 1.9394983537396247e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1939498086046261248/pu/vid/avc1/720x1280/MvycFUweEwcx9tu8.mp4?tag=12",
      "date": "2025-06-30 01:36:26",
      "tweet_id": 1.9394982291184765e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1937798487380512768/pu/vid/avc1/720x1280/mwBnIxQa4j-713iA.mp4?tag=12",
      "date": "2025-06-25 09:02:23",
      "tweet_id": 1.9377985154866056e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1937798240528920576/pu/vid/avc1/720x1280/gP2nHcFk0caiD5U8.mp4?tag=12",
      "date": "2025-06-25 09:01:24",
      "tweet_id": 1.937798268031054e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1937051781541867520/pu/vid/avc1/960x720/pUhN-iRblKhSffBA.mp4?tag=12",
      "date": "2025-06-23 07:36:10",
      "tweet_id": 1.9370520433756777e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1932330908859977728/pu/vid/avc1/720x1280/v-aBH7tGBQXVZirI.mp4?tag=12",
      "date": "2025-06-10 06:58:53",
      "tweet_id": 1.9323316177015726e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1932330893915668480/pu/vid/avc1/720x1280/yUzbp0Q-UzC_pt4p.mp4?tag=12",
      "date": "2025-06-10 06:58:36",
      "tweet_id": 1.9323315480383493e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1928311782399168513/pu/vid/avc1/720x1280/FA_e1UtO90PP5n2C.mp4?tag=12",
      "date": "2025-05-30 04:45:36",
      "tweet_id": 1.9283118092131412e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1928311002501894144/pu/vid/avc1/720x1280/HzZXN__SFpwvTIFf.mp4?tag=12",
      "date": "2025-05-30 04:45:13",
      "tweet_id": 1.928311712739926e+18,
      "type": "video"
    },
    {
      "url": "https://pbs.twimg.com/media/GsFrXG6XEAE3F4x?format=jpg&name=orig",
      "date": "2025-05-29 04:08:49",
      "tweet_id": 1.9279401664143977e+18,
      "type": "photo"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1926923113213636608/pu/vid/avc1/720x1280/DoYHReOEkcXk9IY4.mp4?tag=12",
      "date": "2025-05-26 08:47:42",
      "tweet_id": 1.926923183204057e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1926586432971227137/pu/vid/avc1/1280x720/xaFhakayWPw98-Ax.mp4?tag=12",
      "date": "2025-05-25 10:29:39",
      "tweet_id": 1.9265864554191997e+18,
      "type": "video"
    },
    {
      "url": "https://pbs.twimg.com/media/Grn6ESMWMAAAh8c?format=jpg&name=orig",
      "date": "2025-05-23 09:24:28",
      "tweet_id": 1.9258452728206502e+18,
      "type": "photo"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1925781436516212736/pu/vid/avc1/720x1280/FX3H49I0yeVwHmV7.mp4?tag=12",
      "date": "2025-05-23 05:17:26",
      "tweet_id": 1.9257831074387766e+18,
      "type": "video"
    },
    {
      "url": "https://pbs.twimg.com/media/GricTVUboAA7FvF?format=jpg&name=orig",
      "date": "2025-05-22 07:56:19",
      "tweet_id": 1.9254607026948877e+18,
      "type": "photo"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1925422574089166848/pu/vid/avc1/720x1280/q1HuQZd1OMsV_ZVc.mp4?tag=12",
      "date": "2025-05-22 05:26:10",
      "tweet_id": 1.9254229162437924e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1925064762330906625/pu/vid/avc1/720x1280/d5D9kxhhxjVg4R0b.mp4?tag=12",
      "date": "2025-05-21 05:43:59",
      "tweet_id": 1.9250650133474186e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1925062749719298048/pu/vid/avc1/720x1280/ng1bNZ98Xp4rBKSQ.mp4?tag=12",
      "date": "2025-05-21 05:35:37",
      "tweet_id": 1.9250629069637555e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1924040458906312704/pu/vid/avc1/720x960/YO4nlWp6RdQ1ZZA_.mp4?tag=12",
      "date": "2025-05-18 09:52:57",
      "tweet_id": 1.924040502640546e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/ext_tw_video/1924040302257422336/pu/vid/avc1/720x960/0vMCy9oY5pMyaOnd.mp4?tag=12",
      "date": "2025-05-18 09:52:19",
      "tweet_id": 1.9240403419776942e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/amplify_video/1921097519192309760/vid/avc1/720x1280/cyKVMsnh8kgY-jjp.mp4?tag=14",
      "date": "2025-05-10 06:58:51",
      "tweet_id": 1.9210975856259116e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/amplify_video/1921094930560413698/vid/avc1/720x1280/KQ-iQ6zr9q6Zfa1h.mp4?tag=14",
      "date": "2025-05-10 06:48:35",
      "tweet_id": 1.9210950028154476e+18,
      "type": "video"
    },
    {
      "url": "https://pbs.twimg.com/media/GqUCkLpaEAAhcYE?format=jpg&name=orig",
      "date": "2025-05-07 02:33:32",
      "tweet_id": 1.9199436531847086e+18,
      "type": "photo"
    },
    {
      "url": "https://video.twimg.com/amplify_video/1919238408985247744/vid/avc1/720x1280/Q6jVBuzN0-Ue23t5.mp4?tag=14",
      "date": "2025-05-05 03:51:25",
      "tweet_id": 1.9192384799149632e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/amplify_video/1918606522176970752/vid/avc1/720x1280/secbfw66fwRzwwBL.mp4?tag=14",
      "date": "2025-05-03 10:00:33",
      "tweet_id": 1.918606597196268e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/amplify_video/1918442212150702080/vid/avc1/720x1280/r-vnZe6cMDYRkw-f.mp4?tag=14",
      "date": "2025-05-02 23:07:39",
      "tweet_id": 1.9184422893426606e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/amplify_video/1917561451813953539/vid/avc1/720x1280/Sgo99tXdRN-I73d4.mp4?tag=14",
      "date": "2025-04-30 12:47:47",
      "tweet_id": 1.9175615181426772e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/amplify_video/1916685740211314688/vid/avc1/720x1280/9UWmE1oWHeuGIxNi.mp4?tag=14",
      "date": "2025-04-28 02:48:11",
      "tweet_id": 1.91668585101652e+18,
      "type": "video"
    },
    {
      "url": "https://video.twimg.com/amplify_video/1916076208342933504/vid/avc1/720x1280/Hgx_KbUU5eOjuWCx.mp4?tag=14",
      "date": "2025-04-26 10:25:57",
      "tweet_id": 1.9160762765338913e+18,
      "type": "video"
    }
  ],
  "metadata": {
    "new_entries": 61,
    "cursor": "null"
  }
}
    
    download(sample_data["timeline"])