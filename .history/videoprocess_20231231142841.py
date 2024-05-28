
import ffmpeg


def change_frame_rate(input_file, output_file, frame_rate=10):
    try:
        (
            ffmpeg.input(input_file)
            .output(output_file, r=frame_rate)
            .run(overwrite_output=True)
        )
    except ffmpeg._run.Error as e:
        print("FFmpeg Error:")
        print(e.stderr.decode())
        raise
