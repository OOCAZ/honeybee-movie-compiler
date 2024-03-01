from moviepy.editor import *

import tkinter as tk
from tkinter import filedialog


def merge_image_audio(image_path, audio_path, output_path, fps=30):
    # Load image
    img = ImageClip(image_path)

    # Load audio
    audio = AudioFileClip(audio_path)

    # Set audio duration to match video duration
    img.set_duration(audio.duration)

    # Set audio volume to 0.5 (adjust as needed)
    audio = audio.volumex(0.5)

    # Set fps for the video
    img = img.set_fps(fps)

    # Combine image and audio
    final_clip = img.set_audio(audio).set_duration(audio.duration)

    # Write video file
    final_clip.write_videofile(output_path, codec="libx264", fps=fps)


def select_file(label):
    filename = filedialog.askopenfilename()
    label.config(text=filename)
    return filename


def merge_files():
    image_path = image_label.cget("text")
    audio_path = audio_label.cget("text")
    if image_path and audio_path:
        output_path = "output_video.mp4"
        merge_image_audio(image_path, audio_path, output_path)


# Create main window
root = tk.Tk()
root.title("Image and Audio Merger")

# Create image selection button
image_label = tk.Label(root, text="Select Image")
image_label.pack()
image_button = tk.Button(
    root, text="Select Image", command=lambda: select_file(image_label)
)
image_button.pack()

# Create audio selection button
audio_label = tk.Label(root, text="Select Audio")
audio_label.pack()
audio_button = tk.Button(
    root, text="Select Audio", command=lambda: select_file(audio_label)
)
audio_button.pack()

# Create merge button
merge_button = tk.Button(root, text="Merge Files", command=merge_files)
merge_button.pack()

# Run the GUI
root.mainloop()
