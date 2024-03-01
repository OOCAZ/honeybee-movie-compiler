from tkinter import *
from tkinter import filedialog
from moviepy.editor import *

# This is the one! this one works great!


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

    # Close clips
    audio.close()
    img.close()
    final_clip.close()


def select_file(label):
    filename = filedialog.askopenfilename()
    label.config(text=filename)
    return filename


def browse_image():
    image_file = select_file(image_label)
    if image_file:
        image_label.config(text=image_file)


def browse_audio():
    audio_file = select_file(audio_label)
    if audio_file:
        audio_label.config(text=audio_file)


def select_output():
    output_file = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
    )
    if output_file:
        output_label.config(text=output_file)


def merge_files():
    image_path = image_label.cget("text")
    audio_path = audio_label.cget("text")
    output_path = output_label.cget("text")
    if image_path and audio_path and output_path:
        merge_image_audio(image_path, audio_path, output_path)


# Create main window
root = Tk()
root.title("Image and Audio Merger")

# Frame for image selection
image_frame = Frame(root)
image_frame.pack(pady=10)

image_label = Label(image_frame, text="Select Image:")
image_label.pack(side=LEFT, padx=5)

image_button = Button(image_frame, text="Browse", command=browse_image)
image_button.pack(side=LEFT)

# Frame for audio selection
audio_frame = Frame(root)
audio_frame.pack(pady=10)

audio_label = Label(audio_frame, text="Select Audio:")
audio_label.pack(side=LEFT, padx=5)

audio_button = Button(audio_frame, text="Browse", command=browse_audio)
audio_button.pack(side=LEFT)

# Frame for output file selection
output_frame = Frame(root)
output_frame.pack(pady=10)

output_label = Label(output_frame, text="Select Output File:")
output_label.pack(side=LEFT, padx=5)

output_button = Button(output_frame, text="Browse", command=select_output)
output_button.pack(side=LEFT)

# Create merge button
merge_button = Button(root, text="Merge Files", command=merge_files)
merge_button.pack(pady=10)

# Run the GUI
root.mainloop()
