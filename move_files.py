import os, shutil

folder=r"G:\mcd43c4_product\ppi_monthly_mean"
des_folderName='summer'
os.chdir(folder)  # used to change the current working directory to specified path
os.mkdir(des_folderName)

for f in os.listdir(folder):
    folderName = f[-6:-4]
    #if (folderName=='05') or (folderName=='06')or (folderName=='07') or (folderName=='08')or (folderName=='09'):
    if (folderName == '06') or (folderName == '07') or (folderName == '08'):
      if os.path.exists(des_folderName):
        shutil.move(os.path.join(folder, f), des_folderName)
