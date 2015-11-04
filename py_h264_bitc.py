import subprocess
import sys
import os
from glob import glob


# Directory with files that we want to transcode losslessly and generate metadata for
video_dir = sys.argv[1]

# Change directory to directory with video files
wd = os.path.dirname(video_dir)
os.chdir(wd)

# Find all video files to transcode
video_files =  glob('*.mov') + glob('*.mp4')

for filename in video_files: #loop all files in directory
	
	video_height = float(subprocess.check_output(['ffprobe', 
									'-v', 'error',
									'-select_streams', 'v:0',
									'-show_entries', 'stream=height',
									'-of', 'default=noprint_wrappers=1:nokey=1',
									filename]))
	
	video_width = float(subprocess.check_output(['ffprobe', 
									'-v', 'error',
									'-select_streams', 'v:0',
									'-show_entries', 'stream=width',
									'-of', 'default=noprint_wrappers=1:nokey=1',
									filename]))	
	
	
	vertical_position_timecode = video_height / 1.2
	print vertical_position_timecode
	horizontal_position_timecode = video_width /2))
	#font_size = ($(bc <<< $size/12))
	
		#wsize=($(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 "$1"))
