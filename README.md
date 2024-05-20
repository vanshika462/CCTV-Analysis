We have implemented three modules in this system

Run the interface using main_gui.py and download darknet,yolov5.weights and yolov5

Module 1 - Vehicle Count
count.py processes 'frames' which are extracted from 'dummy_vids' by extract_frames.py
gui_count.py calls count.py and is the User GUI

Module 2 - Movement Patterns
traffic.py processes a video from 'dummy_vids' and saves the csv file in 'traffic_output'
gui_patterns.py calls traffic.py and is the User GUI

Module 3 - Day Summary
visualization.py analyzes files in 'traffic_output' and plots a line chart
gui_daysummary.py calls visualization.py and is the User GUI

Additional Features:
Loitering
loitering.py processes a video from 'dummy_vids'
gui_loitering.py calls loitering.py and is the User GUI
detecting.py is the initial file that we draw bounding boxes with using yolov5

CONTRIBUTIONS:
Vanshika Shrivastava (https://github.com/vanshika462)
Sarah Nasim (https://github.com/SarahN18)
Surnam Mohith (https://github.com/mohsur)
Stanzin Chamchhen (https://github.com/chamchhen260)
