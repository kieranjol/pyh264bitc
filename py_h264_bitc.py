import subprocess
import sys
import os
from glob import glob
import pdb
from sys import platform as _platform

# Determine which operating system. Only important for locating bitc fonts.
if _platform == "linux" or _platform == "linux2":
    print "linux"
elif _platform == "darwin":
    print "OS X"
    font_path= "fontfile=/Library/Fonts/AppleGothic.ttf"
elif _platform == "win32":
    print "Windows"
    font_path = "fontfile='C\:\\\Windows\\\Fonts\\\\'arial.ttf'"

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
	horizontal_position_timecode = video_width / 3
	
	# Calculate appropriate font size
	font_size = video_height / 12
	#pdb.set_trace()
	
	textoptions = ("fontsize=%d:x=%d:y=%d" % (font_size,horizontal_position_timecode,vertical_position_timecode))
	print  textoptions
	
	# Get starting timecode. In a raw state that requires further processing further on in the script.
	timecode_test_raw = subprocess.check_output(['ffprobe',
									'-v', 'error',
									'-select_streams', 'v:0',
									'-show_entries', 'format_tags=timecode:stream_tags=timecode',
									'-of', 'default=noprint_wrappers=1:nokey=1',
									filename])
	
	# Get framerate so that bitc is accurate.
	get_framerate = subprocess.check_output(['ffprobe',
									'-v', 'error',
									'-select_streams', 'v:0',
									'-show_entries', 'stream=avg_frame_rate',
									'-of', 'default=noprint_wrappers=1:nokey=1',
									filename])
									
	# This tests if there is actually a timecode present in the file.								
	if not timecode_test_raw:
		# The timecode needs to be phrased in a way unique to each operating system. Note the backslashes.
		# This section makes up a timecode if none is present in the file.
		if _platform == "darwin":
		    print "OS X"
		    timecode_test = '01\\\:00\\\:00\\\:00'
		elif _platform == "win32":
		    print "Windows"
		    font_path = "fontfile='C\:\\\Windows\\\Fonts\\\\'arial.ttf'"
		    timecode_test = '01\:00\:00\:00'
			
	else:
		# If a timecode is present, this will modify the raw input so that it is compatible with each operating system.
		if _platform == "darwin":
		    print "OS X"
		    timecode_test = timecode_test_raw.replace(':', '\\\:').replace('\n', '')
		elif _platform == "win32":
		    print "Windows"
		    font_path = "fontfile='C\:\\\Windows\\\Fonts\\\\'arial.ttf'"
		    timecode_test = timecode_test_raw.replace(':', '\\:').replace('\n', '')
		
		
		
	
		#pdb.set_trace()
	# This removes the new line character from the framemrate.
	fixed_framerate = get_framerate.rstrip()
	
	#all these prints are just for testing. Will be removed later.
	print fixed_framerate	
	drawtext_options = "drawtext=%s:fontcolor=white:timecode=%s:rate=%s:boxcolor=0x000000AA:box=1:%s" % (font_path,timecode_test, fixed_framerate, textoptions)
	print drawtext_options
	print timecode_test
	print get_framerate

	subprocess.call(['ffmpeg',
 			'-i', filename,
			'-c:v', 'libx264',
			'-crf', '22',
			'-pix_fmt', 'yuv420p',
			'-vf',drawtext_options, output])
