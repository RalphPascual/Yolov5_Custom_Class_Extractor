

# YOLO-Coco-Dataset-Custom-Classes-Extractor

- Download specific classes from the **Coco Dataset** for custrom object detection needs.
- Download multiple classes at the same time (Multi-threaded).
- Pickup where you left off if your connection is interrupted.
- Combine annotations into a single folder in Yolov5 annotation format.

## Packages Required
**1. pycocotools**  
`pip install pycocotools`

## Usage
#### 1. Clone this repository:  
`git clone https://github.com/RalphPascual/Yolov5_Custom_Class_Extractor.git`
#### 2. Download the **[2017 Train/Val annotations \[241MB\]](https://cocodataset.org/#download)** zip file and put the **instances_train2017.json** file in the cloned repository's main directory.
#### 3. See the various classes available:  
`python coco-extractor.py --help` 
#### 4. Download a specific class:  
`python coco-extractor.py "person"`
#### 5. Download multiple classes:  
`python coco-extractor.py "person" "sports ball" "zebra"`
#### 6. Combine annotations:
`python coco-extractor.py --combineanns`

### Happy Detecting!
