import os
import gzip
from pathlib import Path

fileDir:str
content:bytes

for root,subFolders,files in os.walk('staticfiles'):
    for file in files:
        if file.split('.')[-1].lower() in ['css','js','svg','png']:
            pathDir = f'{root}'.replace('\\','/').replace('staticfiles','static')
            if not os.path.exists(pathDir):
                path = Path(pathDir)
                path.mkdir(parents=True,exist_ok=True)
            fileDir = f'{root}\\{file}'.replace('\\','/')
            content = open(fileDir,'rb').read()
            gzip.open(filename=f'{fileDir}.gz'.replace('staticfiles','static'),mode='wb').write(content)
  
              