import torch
import cv2
import time
from pathlib import Path
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import check_img_size, non_max_suppression, scale_coords
from yolov5.utils.augmentations import letterbox
from yolov5.utils.plots import plot_one_box
from yolov5.utils.torch_utils import select_device, time_sync

def detect(source, weights, img_size=640, conf_thres=0.25, iou_thres=0.45, output_dir="output"):
    source = str(Path(source))  # convert to str
    # Initialize
    device = select_device('')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(img_size, s=model.stride.max())  # check img_size

    # Set Dataloader
    vid_path, vid_writer = None, None

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once

    cap = cv2.VideoCapture(source)
    frames = 0
    start_time = time.time()
    loitering_time = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames += 1

        img = letterbox(frame, imgsz, stride=model.stride)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_sync()
        pred = model(img, augment=False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=False)
        t2 = time_sync()
        loitering = False

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    label = '%s %.2f' % ('person', conf)
                    plot_one_box(xyxy, frame, label=label, color=(0, 255, 0), line_thickness=3)

                    # Check if person is loitering
                    if cls == 0:
                        loitering_time = time.time() - start_time
                        if loitering_time > 180:  # 3 minutes
                            loitering = True
                            # Change bounding box color to pink
                            plot_one_box(xyxy, frame, label=label, color=(255, 0, 255), line_thickness=3)
                            cv2.putText(frame, "Loitering", (int(xyxy[0]), int(xyxy[1] - 5)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        # Save annotated frame
        output_path = Path(output_dir) / f"output_frame_{frames}.jpg"
        cv2.imwrite(str(output_path), frame)

        if loitering:
            break

    cap.release()
    cv2.destroyAllWindows()

    return str(output_path)  # Return the path to the saved output image

# Example usage:
# output_image_path = detect("input_video.mp4", "yolov5s.pt", output_dir="output")
# print("Output image saved to:", output_image_path)
