import cv2
import os, os.path
import sys
import time

try:
    # NAME OF FOLDER. In this case: For masked, use "with_mask" else "without_mask"
    # with_mask
    # without_mask
    label_name = sys.argv[1]
    # NUMBER OF IMAGES NEED COLLECTED
    num_samples = int(sys.argv[2])
except:
    print("Arguments missing.")
    exit(-1)

# PATH_TO_SAVE Dataset
IMG_SAVE_PATH = 'dataset'
IMG_CLASS_PATH = os.path.join(IMG_SAVE_PATH, label_name)

try:
    os.mkdir(IMG_SAVE_PATH)
except FileExistsError:
    pass
try:
    os.mkdir(IMG_CLASS_PATH)
except FileExistsError:
    print("{} directory already exists.".format(IMG_CLASS_PATH))
    print("All images gathered will be saved along with existing items in this folder")

cap = cv2.VideoCapture(0)

start = False
count = 0
for root_dir, cur_dir, files in os.walk(IMG_CLASS_PATH):
    count += len(files)
print('file count:', count)

addittion_samples = count + num_samples
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    if count ==  addittion_samples:
        break

    label = "Recognition Region"
    cv2.rectangle(frame,(100, 100),(500,450), (0, 255, 0), 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (100, 90)
    fontScale = 1
    color = (0, 255, 0)
    thickness = 2
    image = cv2.putText(frame, label, org, font, 
                        fontScale, color, thickness, cv2.LINE_AA)
    if start:
        roi = frame[105:445, 105:495]
        time.sleep(0.1)
        save_path = os.path.join(IMG_CLASS_PATH, '{}.jpg'.format(count + 1))
        cv2.imwrite(save_path, roi)
        count += 1

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "{} - Collecting {}".format(label_name, count),
            (10, 20), font, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.imshow("Gathering Dataset", frame)

    k = cv2.waitKey(10)
    if k == ord('a'):
        start = not start

    if k == ord('q'):
        break

print("\nHaving {} image(s) saving to location: {}".format(count, IMG_CLASS_PATH))
cap.release()
cv2.destroyAllWindows()
