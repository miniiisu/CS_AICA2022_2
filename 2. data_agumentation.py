import random
import numpy as np
import os
import cv2
import glob
from PIL import Image
import PIL.ImageOps

print(os.getcwd())

# 기본 경로
base_dir = './OX_images/'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')

# 훈련용 O/X 이미지 경로
train_o_dir = train_dir+ '/O'
train_x_dir = train_dir + '/X'
# train_o_dir = os.path.join(train_dir, 'O')
# train_x_dir = os.path.join(train_dir, 'X')
print("train_o_dir = ", train_o_dir)
print("train_x_dir = ", train_x_dir)


dirList = [train_o_dir, train_x_dir]
for j in dirList:
    file_path = j
    file_names = os.listdir(file_path)
    total_origin_image_num = len(file_names)
    augment_cnt = 1

    for i in range(0, total_origin_image_num):
        print("============== ", j, "=>", i, " / ", total_origin_image_num, " ==============")
      
        change_picture_index = i
        print(change_picture_index)
        print(file_names[change_picture_index])
        file_name = file_names[change_picture_index]
        save_file_name = file_name.split(".")[0]

        origin_image_path = j + '/' + file_name
        print(origin_image_path)
        image = Image.open(origin_image_path)
        random_augment = random.randrange(1, 4)

        # 랜덤 값으로 좌우반전 or 회전 or 노이즈 추가 => 6000장
        # if (random_augment == 1):
        # 이미지 좌우 반전
        print(save_file_name + '_inverted.png')
        inverted_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        inverted_image.save(file_path + "/" + save_file_name + '_inverted.png')

    # elif (random_augment == 2):
        # 이미지 기울이기
        print(save_file_name + '_rotated.png')
        rotated_image = image.rotate(random.randrange(-20, 20))
        rotated_image.save(file_path + "/" + save_file_name + '_rotated.png')

    # elif (random_augment == 3):
        # 노이즈 추가하기
        img = cv2.imread(origin_image_path)
        print(save_file_name + '_noiseAdded.png')
        row, col, ch = img.shape
        mean = 0
        var = 0.1
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy_array = img + gauss
        noisy_image = Image.fromarray(np.uint8(noisy_array)).convert('RGB')
        noisy_image.save(file_path + "/" + save_file_name + '_noiseAdded.png')

        augment_cnt += 1