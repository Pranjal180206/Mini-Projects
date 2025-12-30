import os
import cv2
import albumentations as A

Input_Dir = 'dataset/train/bufallo'
Output_Dir = 'dataset/train/bufallo'
Aug_Per_Image = 2

augmenter = A.Compose([
    A.HorizontalFlip(p = 0.5),
    A.Rotate(limit = 10, p = 0.5),
    A.RandomBrightnessContrast(p = 0.5),
    A.RandomResizedCrop(size = (64, 64), scale = (0.9, 1.0), p = 0.5),
])

images = [f for f in os.listdir(Input_Dir) if f.endswith(('.jpg', '.png'))]

count = 0
for img_name in images:
    img_path = os.path.join(Input_Dir, img_name)
    image = cv2.imread(img_path)

    if image is None:
        continue

    for i in range(Aug_Per_Image):
        augmented = augmenter(image = image)['image']
        new_name = f"aug_{i}_{img_name}"
        cv2.imwrite(os.path.join(Output_Dir, new_name), augmented)
        count += 1

print(f"Generated {count} augmented buffalo images")

print("Buffalo:", len(os.listdir("dataset/train/bufallo")))
print("Cattle :", len(os.listdir("dataset/train/cattle")))
