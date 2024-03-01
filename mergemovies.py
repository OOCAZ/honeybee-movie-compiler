import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, concatenate_videoclips


class VideoConcatenator:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 Concatenator")

        self.clips = []

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.add_button = tk.Button(
            self.frame, text="Add Video", command=self.add_video
        )
        self.add_button.pack(side=tk.LEFT)

        self.merge_button = tk.Button(
            self.frame, text="Merge Videos", command=self.merge_videos
        )
        self.merge_button.pack(side=tk.LEFT)

        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=50)
        self.listbox.pack(padx=10, pady=10)

    def add_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.clips.append(VideoFileClip(file_path))
            self.listbox.insert(
                tk.END, file_path.split("/")[-1]
            )  # Display only the filename

    def merge_videos(self):
        if self.clips:
            final_clip = concatenate_videoclips(self.clips)
            output_path = filedialog.asksaveasfilename(
                defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")]
            )
            if output_path:
                final_clip.write_videofile(output_path)
                print(f"Merged videos saved to: {output_path}")
                final_clip.close()
            else:
                print("Please provide a valid output file path.")
        else:
            print("No videos selected to merge.")


def main():
    root = tk.Tk()
    app = VideoConcatenator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
