import ffmpeg
from tqdm import tqdm


def change_frame_rate(input_file, output_file, frame_rate=10):
    try:
        process = (
            ffmpeg.input(input_file)
            .output(output_file, r=frame_rate)
            .run_async(pipe_stdout=True, pipe_stderr=True)
        )
        progress_bar = tqdm(total=int(process.stderr.readline()), ncols=100)
        for line in process.stderr:
            if b'frame=' in line:
                progress_bar.n = int(line.split(b'frame=')[1].split(b'fps')[0])
                progress_bar.refresh()
        progress_bar.close()
    except ffmpeg._run.Error as e:
        print("FFmpeg Error:")
        print(e.stderr.decode())
        raise
