cd yolo
call git clone https://github.com/WongKinYiu/yolov7.git
cd ..
call python -m venv venv
cmd /k "venv\Scripts\activate && pip install -r requirements.txt"