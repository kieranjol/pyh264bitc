import subprocess
import sys
import os
from glob import glob
import pdb


# Directory with files that we want to transcode losslessly and generate metadata for
video_dir = sys.argv[1]

# Change directory to directory with video files
wd = os.path.dirname(video_dir)
os.chdir(wd)

# Find all video files to transcode
video_files =  glob('*.mov') + glob('*.mp4') + glob('*.mxf')

for filename in video_files: #loop all files in directory
	output = filename + "_vimeo.mov"
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
	
	# Calculate x and y coordinates of the timecode
	vertical_position_timecode = video_height / 1.2
	horizontal_position_timecode = video_width / 2
	# Calculate appropriate font size
	font_size = video_height / 12
	#pdb.set_trace()
	textoptions = ("fontsize=%d:x=%d-text_w/2:y=%d" % (font_size,horizontal_position_timecode,vertical_position_timecode))
	print  textoptions
	timecode_test_raw = subprocess.check_output(['ffprobe',
									'-v', 'error',
									'-select_streams', 'v:0',
									'-show_entries', 'format_tags=timecode:stream_tags=timecode',
									'-of', 'default=noprint_wrappers=1:nokey=1',
									filename])
	
	get_framerate = subprocess.check_output(['ffprobe',
									'-v', 'error',
									'-select_streams', 'v:0',
									'-show_entries', 'stream=avg_frame_rate',
									'-of', 'default=noprint_wrappers=1:nokey=1',
									filename])
									
	if not timecode_test_raw:
		timecode_test = "01\\\:00\\\:00\\\:00"
	else:
		timecode_test = timecode_test_raw.replace(':', '\\\:').replace('\n', '')
	
		#pdb.set_trace()
	gd = get_framerate.rstrip()

	print gd	
	drawtext_options = "drawtext=fontfile=/Library/Fonts/AppleGothic.ttf:fontcolor=white:timecode=%s:rate=%s:boxcolor=0x000000AA:box=1:%s" % (timecode_test, gd, textoptions)

	print timecode_test
	print get_framerate

	subprocess.call(['ffmpeg',
 			'-i', filename,
			'-c:v', 'libx264',
			'-crf', '19',
			'-pix_fmt', 'yuv420p',
			'-vf',drawtext_options, output])
