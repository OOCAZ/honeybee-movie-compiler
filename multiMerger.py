from tkinter import *
from tkinter import filedialog
from moviepy.editor import *


class ClipPair:
    def __init__(self, image_path="", audio_path=""):
        self.image_path = image_path
        self.audio_path = audio_path
        self.image_label = Label(root)
        self.audio_label = Label(root)

    def select_image(self, label):
        filename = filedialog.askopenfilename()
        label.config(text=filename)
        self.image_path = filename

    def select_audio(self, label):
        filename = filedialog.askopenfilename()
        label.config(text=filename)
        self.audio_path = filename


def merge_clips(clip_pairs, output_path, fps=30):
    clips = []
    for clip_pair in clip_pairs:
        if clip_pair.image_path and clip_pair.audio_path:
            img = (
                ImageClip(clip_pair.image_path)
                .set_duration(AudioFileClip(clip_pair.audio_path).duration)
                .set_fps(fps)
            )
            audio = AudioFileClip(clip_pair.audio_path).volumex(0.5)
            clip = img.set_audio(audio)
            clips.append(clip)
            audio.close()
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, codec="libx264", fps=fps)
    final_clip.close()


def add_clip_pair():
    new_clip_pair = ClipPair()
    clip_pairs.append(new_clip_pair)
    update_gui()


def remove_clip_pair(index):
    clip_pairs.pop(index)
    update_gui()


def update_gui():
    # Remove all existing clip pair frames
    for frame in clip_pair_frames:
        frame.destroy()
    clip_pair_frames.clear()

    # Create frames for clip pairs
    for i, clip_pair in enumerate(clip_pairs):
        frame = Frame(root)
        frame.pack(pady=5)

        image_label = Label(frame, text="Image:")
        image_label.pack(side=LEFT, padx=5)

        image_button = Button(
            frame,
            text="Select",
            command=lambda label=clip_pair.image_label: clip_pair.select_image(label),
        )
        image_button.pack(side=LEFT)

        clip_pair.image_label = Label(frame, text=clip_pair.image_path)
        clip_pair.image_label.pack(side=LEFT, padx=5)

        audio_label = Label(frame, text="Audio:")
        audio_label.pack(side=LEFT, padx=5)

        audio_button = Button(
            frame,
            text="Select",
            command=lambda label=clip_pair.audio_label: clip_pair.select_audio(label),
        )
        audio_button.pack(side=LEFT)

        clip_pair.audio_label = Label(frame, text=clip_pair.audio_path)
        clip_pair.audio_label.pack(side=LEFT, padx=5)

        remove_button = Button(
            frame, text="Remove", command=lambda index=i: remove_clip_pair(index)
        )
        remove_button.pack(side=LEFT)

        clip_pair_frames.append(frame)


def select_output():
    output_file = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
    )
    if output_file:
        output_label.config(text=output_file)


def merge_files():
    output_path = output_label.cget("text")
    if output_path:
        merge_clips(clip_pairs, output_path)


# Create main window
root = Tk()
root.title("Clip Merger")

# Create frame for clip pairs
clip_pair_frames = []

# Create initial clip pair
clip_pairs = [ClipPair()]
update_gui()

# Create frame for output file selection
output_frame = Frame(root)
output_frame.pack(pady=10)

output_label = Label(output_frame, text="Select Output File:")
output_label.pack(side=LEFT, padx=5)

output_button = Button(output_frame, text="Browse", command=select_output)
output_button.pack(side=LEFT)

# Create add clip pair button
add_button = Button(root, text="Add Clip Pair", command=add_clip_pair)
add_button.pack(pady=10)

# Create merge button
merge_button = Button(root, text="Merge Clips", command=merge_files)
merge_button.pack(pady=10)

# Run the GUI
root.mainloop()
