import os
from rembg import remove
from PIL import Image, ImageOps
import requests
from io import BytesIO
import pandas as pd
import torch
from torchvision import models, transforms
import numpy as np

# 定義資料夾與目標大小
final_folder = 'final_data'
clothes_folder = 'clothes_data'
preprocessed_folder = 'preprocessed_data'  # 預處理後的資料夾
desired_size = (512, 512)  # 目標圖片大小
background_color = (0, 0, 0)  # 黑色背景

# 創建輸出資料夾
os.makedirs(final_folder, exist_ok=True)
os.makedirs(clothes_folder, exist_ok=True)
os.makedirs(preprocessed_folder, exist_ok=True)

# 讀取 Google 表單資料
df = pd.read_csv('google_form_data.csv')

# 轉換 Google Drive URL 為可下載格式
def convert_drive_url_to_downloadable(url):
    if 'open?id=' in url:
        file_id = url.split('open?id=')[-1]
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    elif 'file/d/' in url:
        file_id = url.split('file/d/')[-1].split('/view')[0]
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    else:
        return url

# 加載 DeepLabV3 模型
model = models.segmentation.deeplabv3_resnet101(pretrained=True).eval()

# 定義預處理函數
preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# 使用 DeepLabV3 進行語義分割，保留衣服部分
def segment_clothes(img):
    img_tensor = preprocess(img).unsqueeze(0)

    # 使用模型進行推斷
    with torch.no_grad():
        output = model(img_tensor)['out'][0]

    # 生成預測標籤
    output_predictions = output.argmax(0).byte().cpu().numpy()

    # 人體部位的標籤 (COCO數據集中，15代表身體)
    PERSON_LABEL = 15
    
    # 將非人體部位設為背景，保留衣服
    mask = (output_predictions == PERSON_LABEL)

    # 將mask應用到原始圖片上
    result_img = np.array(img) * mask[:, :, np.newaxis]
    result_img = Image.fromarray(result_img.astype('uint8'))
    
    return result_img

# 定義真實的放大操作
def zoom_in_image(img, zoom_factor=1.5):
    width, height = img.size
    # 計算要裁剪的區域（從中心部分進行放大）
    new_width = int(width / zoom_factor)
    new_height = int(height / zoom_factor)

    # 計算中心點
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = (width + new_width) // 2
    bottom = (height + new_height) // 2

    # 裁剪圖片
    cropped_img = img.crop((left, top, right, bottom))

    # 將裁剪後的圖片放大回到原始尺寸
    zoomed_img = cropped_img.resize((width, height), Image.LANCZOS)

    return zoomed_img

# 定義圖片處理函數
def preprocess_image(img, output_dir, image_name):
    # 旋轉圖片
    rotated_img = img.rotate(45)
    rotated_img.save(os.path.join(output_dir, f"{image_name}_rotated.jpg"))
    
    # 水平翻轉
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    flipped_img.save(os.path.join(output_dir, f"{image_name}_flipped.jpg"))

    # 真實的放大操作
    zoomed_img = zoom_in_image(img, zoom_factor=1.5)
    zoomed_img.save(os.path.join(output_dir, f"{image_name}_zoomed.jpg"))

# 指定開始處理的索引 (例如，從第90筆資料開始)
start_index = 0

# 遍歷表單資料，從指定索引開始
for index, row in df.iterrows():
    if index < start_index:
        continue  # 跳過已經處理過的資料

    image_url = row['照片 Picture']  # 從表單中的照片 URL 讀取
    download_url = convert_drive_url_to_downloadable(image_url)  # 轉換成可下載的URL
    try:
        # 從 URL 下載圖片
        response = requests.get(download_url)
        img = Image.open(BytesIO(response.content))

        # 背景移除
        output = remove(img)
        output = output.convert('RGB')

        # 調整圖片大小並添加邊框
        output.thumbnail(desired_size, Image.LANCZOS)
        delta_w = desired_size[0] - output.size[0]
        delta_h = desired_size[1] - output.size[1]
        padding = (delta_w // 2, delta_h // 2, delta_w - delta_w // 2, delta_h - delta_h // 2)
        padded_img = ImageOps.expand(output, padding, background_color)

        # 使用 DeepLabV3 進行人頭和衣服分割，保留衣服部分
        # clothes_only = segment_clothes(padded_img)

        # 保存去除人頭的圖片到 clothes_folder
        final_filename = f"image_{index}.jpg"
        clothes_path = os.path.join(clothes_folder, final_filename)
        padded_img.save(clothes_path, 'JPEG')
        print(f"{clothes_path}（去除人頭） 已成功處理並保存")

        # 圖片預處理 (旋轉、翻轉、縮放)
        preprocess_image(padded_img, preprocessed_folder, f"image_{index}")

    except Exception as e:
        print(f"處理 {download_url} 時出錯：{e}")
        continue

# 更新表單資料並保存
new_rows = []
for index, row in df.iterrows():
    image_name = f"image_{index}"
    for variant in ["original", "rotated", "flipped", "zoomed"]:
        new_row = row.copy()
        new_row['照片 Picture'] = f"{image_name}_{variant}.jpg"
        new_rows.append(new_row)

# 將新資料轉換為 DataFrame 並儲存
new_df = pd.DataFrame(new_rows)
new_df.to_csv('updated_google_form_data.csv', index=False)