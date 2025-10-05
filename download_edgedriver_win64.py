import winreg
import os
import zipfile

# reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'SOFTWARE\Microsoft\Edge\BLBeacon')
user_data_dir, _ = winreg.QueryValue(key, "version")
print(user_data_dir)

url = rf'https://msedgedriver.azureedge.net/{user_data_dir}/edgedriver_win64.zip'
os.system(rf'curl {url} > edgedriver_win64.zip')
zipfile.ZipFile(r"./edgedriver_win64.zip").extractall(r'edgedriver_win64')
# 下载edgedriver