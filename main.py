import tkinter as tk
from tkinter import filedialog
import threading
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip


def combine_audio_video():
    def select_audio_file():
        audio_file = filedialog.askopenfilename(
            title="Select Audio File", filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg")]
        )
        if audio_file:
            audio_entry.delete(0, tk.END)
            audio_entry.insert(0, audio_file)

    def select_image_file():
        image_file = filedialog.askopenfilename(
            title="Select Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
        )
        if image_file:
            image_entry.delete(0, tk.END)
            image_entry.insert(0, image_file)

    def select_output_file():
        output_file = filedialog.asksaveasfilename(
            defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")]
        )
        if output_file:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, output_file)

    def combine_files():
        audio_file = audio_entry.get()
        image_file = image_entry.get()
        output_file = output_entry.get()

        if audio_file and image_file and output_file:
            audio_clip = AudioFileClip(audio_file)
            image_clip = ImageClip(image_file).set_duration(audio_clip.duration)
            final_clip = CompositeVideoClip([image_clip.set_audio(audio_clip)])
            final_clip.write_videofile(
                output_file, fps=audio_clip.fps, codec="mpeg4"
            ).set_duration(audio_clip.duration)
            status_label.config(text="Video created successfully!")

            # Close the final_clip to terminate MoviePy processes
            audio_clip.close()
            image_clip.close()
            final_clip.close()
            # Explicitly terminate the ffmpeg process
            if hasattr(final_clip, "process") and final_clip.process:
                final_clip.process.terminate()

        else:
            status_label.config(text="No file selected. Exiting...")

        # Notify the main thread that the combining process is complete
        combining_complete_event.set()
        combine_button.config(state=tk.NORMAL)
        return 1

    def combine_button_clicked():
        combine_button.config(state=tk.DISABLED)
        threading.Thread(target=combine_files).start()

    def on_closing():
        root.destroy()
        root.quit()

    root = tk.Tk()
    root.title("Audio Video Combiner")

    # Audio File Selection
    audio_label = tk.Label(root, text="Audio File:")
    audio_label.grid(row=0, column=0, padx=5, pady=5)
    audio_entry = tk.Entry(root, width=50)
    audio_entry.grid(row=0, column=1, padx=5, pady=5)
    audio_button = tk.Button(root, text="Browse", command=select_audio_file)
    audio_button.grid(row=0, column=2, padx=5, pady=5)

    # Image File Selection
    image_label = tk.Label(root, text="Image File:")
    image_label.grid(row=1, column=0, padx=5, pady=5)
    image_entry = tk.Entry(root, width=50)
    image_entry.grid(row=1, column=1, padx=5, pady=5)
    image_button = tk.Button(root, text="Browse", command=select_image_file)
    image_button.grid(row=1, column=2, padx=5, pady=5)

    # Output File Selection
    output_label = tk.Label(root, text="Output File:")
    output_label.grid(row=2, column=0, padx=5, pady=5)
    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=2, column=1, padx=5, pady=5)
    output_button = tk.Button(root, text="Browse", command=select_output_file)
    output_button.grid(row=2, column=2, padx=5, pady=5)

    # Combine Button
    combine_button = tk.Button(root, text="Combine", command=combine_button_clicked)
    combine_button.grid(row=3, column=1, pady=10)

    # Status Label
    status_label = tk.Label(root, text="")
    status_label.grid(row=4, column=1, pady=10)

    # Create a threading event to signal when the combining process is complete
    combining_complete_event = threading.Event()

    # Close the program gracefully when the window is closed
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


def main():
    combine_audio_video()


if __name__ == "__main__":
    main()
