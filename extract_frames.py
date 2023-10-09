import cv2
import os

def extract_frames_from_videos(video_dir, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of video files in the directory
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]

    # Loop over the video files
    for video_file in video_files:
        video_path = os.path.join(video_dir, video_file)
        video_name = os.path.splitext(video_file)[0]
        frames_output_dir = os.path.join(output_dir, video_name)

        # Create a directory for the frames of this video
        os.makedirs(frames_output_dir, exist_ok=True)

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        while cap.isOpened():
            # Read the frame from the video
            ret, frame = cap.read()

            if not ret:
                break

            # Save the frame as an image
            frame_filename = f"frame_{frame_count:04d}.jpg"
            frame_path = os.path.join(frames_output_dir, frame_filename)
            cv2.imwrite(frame_path, frame)

            frame_count += 1

        cap.release()

# Specify the directory containing the input video files
video_dir = 'dummy_vids'

# Specify the output directory where the frames will be saved
output_dir = 'frames'

# Call the function to extract frames from the videos
extract_frames_from_videos(video_dir, output_dir)
