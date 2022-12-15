import os
import numpy as np
from PIL import Image

print(os.getcwd())

print(os.listdir(os.getcwd() + '/input/detect-person-on-motorbike-or-scooter/dataset/obj/'))



def get_files_count(folder_path):
    dirListing = os.listdir(folder_path)
    return len(dirListing)

wd = os.getcwd() + '/input/detect-person-on-motorbike-or-scooter/dataset/obj/'
print(type(wd))
file_name = []
for file in wd:
    for k in range(len(file) - 1, 0, -1):
        if file[k] == '.':
            file_name.append(file[:k])
            break

print(file_name)

if __name__ == "__main__":
    wd = os.getcwd() + '/input/detect-person-on-motorbike-or-scooter/dataset/obj/'

    print(get_files_count(wd))



# 경로에서 *.jpg이면 array로 바꿔서 추가

wd = os.getcwd()+'/input/detect-person-on-motorbike-or-scooter/dataset/obj/'

# print(wd.listdir())

img = Image.open('./input/detect-person-on-motorbike-or-scooter/dataset/obj/115.jpg')
img.show()

train_images = np.array(img)
print("x = ", train_images)
print("x.shape = ", train_images.shape) # (1390, 867, 3)


print('Before reshaping....')
print(np.shape(train_images)) # (60000, 28, 28)

train_images = train_images.reshape((10000, 28, 28, 1))
# test_images = test_images.reshape((10000, 28, 28, 1))

print('After reshaping....')
print(np.shape(train_images)) # (60000, 28, 28, 1)

