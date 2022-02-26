from pycocotools.coco import COCO # pip install pycocotools
import requests
import os
import sys
import threading
import shutil

def makeDirectory(dirName):
    try:
        os.mkdir(dirName)
        print(f"\nMade {dirName} Directory.\n")
    except:
        pass

def getImagesFromClassName(className):
    makeDirectory(f'downloaded_images/{className}')
    makeDirectory(f'annotations/{className}')
    catIds = coco.getCatIds(catNms=[className])
    imgIds = coco.getImgIds(catIds=catIds )
    images = coco.loadImgs(imgIds)
    index = classes.index(className)

    print(f"Total Images: {len(images)} for class '{className}'")

    for im in images:
        image_file_name = im['file_name']
        label_file_name = im['file_name'].split('.')[0] + '.txt'

        fileExists = os.path.exists(f'downloaded_images/{className}/{image_file_name}')
        if(not fileExists):
            img_data = requests.get(im['coco_url']).content
            annIds = coco.getAnnIds(imgIds=im['id'], catIds=catIds, iscrowd=None)
            anns = coco.loadAnns(annIds)    
            print(f"{className}. Downloading - {image_file_name}")
            for i in range(len(anns)):
                # Yolo Format: center-x center-y width height
                # All values are relative to the image.
                topLeftX = anns[i]['bbox'][0] / im['width']
                topLeftY = anns[i]['bbox'][1] / im['height']
                width = anns[i]['bbox'][2] / im['width']
                height = anns[i]['bbox'][3] / im['height']
                
                s = str(index) + " " + str((topLeftX + (topLeftX + width)) / 2) + " " + \
                str((topLeftY + (topLeftY + height)) / 2) + " " + \
                str(width) + " " + \
                str(height)
                
                if(i < len(anns) - 1):
                    s += '\n'
            
            with open(f'downloaded_images/{className}/{image_file_name}', 'wb') as image_handler:
                image_handler.write(img_data)
            with open(f'annotations/{className}/{label_file_name}', 'w') as label_handler:
                label_handler.write(s)
        else:
           print(f"{className}. {image_file_name} - Already Downloaded.")

def combineAnns():
    makeDirectory('combined_annotations')
    classNames = os.listdir("annotations/")
    for className in classNames:
        annFiles = os.listdir(f'annotations/{className}/')
        for annFile in annFiles:
            fileExists = os.path.exists(f'combined_annotations/{annFile}')
            if (not fileExists):
                copy(f'annotations/{className}/{annFile}', 'combined_annotations/')
            else:
                data1 = data2 = ""
                with open(f'combined_annotations/{annFile}') as fp:
                    data1 = fp.read()
                with open(f'annotations/{className}/{annFile}') as fp:
                    data2 = fp.read()
                data1 += '\n'
                data1 += data2
                with open(f'combined_annotations/{annFile}', 'w') as fp:
                    fp.write(data1)


def copy(src, dst):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    shutil.copyfile(src, dst)

argumentList = sys.argv

classes = argumentList[1:]

classes = [class_name.lower() for class_name in classes] # Converting to lower case


if(classes[0] == "--help"):
    with open('classes.txt', 'r') as fp:
        lines = fp.readlines()
    print("**** Classes ****\n")
    [print(x.split('\n')[0]) for x in lines]
    exit(0)     

if(classes[0] == "--combineanns"):
    combineAnns()
    exit(0)

print("\nClasses to download: ", classes, end = "\n\n")

makeDirectory('downloaded_images')
makeDirectory('annotations')

coco = COCO('instances_train2017.json')
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]

for name in classes:
    if(name not in nms):
        print(f"{name} is not a valid class, Skipping.")
        classes.remove(name)

with open('labelmap.txt', 'w') as f:
    for i in range(len(classes) - 1):
        f.write(classes[i])
        f.write('\n')
    if (len(classes) - 1) >= 0:
        f.write(classes[len(classes) - 1])
        

threads = []

# Creating threads for every class provided.
for i in range(len(classes)):
    t = threading.Thread(target=getImagesFromClassName, args=(classes[i],)) 
    threads.append(t)
    
for t in threads:
    t.start()

for t in threads:
    t.join()

print("Done.")
