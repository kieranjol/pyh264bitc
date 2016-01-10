import subprocess
import sys
import os
from glob import glob
import pdb
from sys import platform as _platform
print _platform

# Directory with files that we want to transcode losslessly and generate metadata for
video_dir = sys.argv[1]

# Change directory to directory with video files
wd = os.path.dirname(video_dir)
os.chdir(wd)

# Find all video files to transcode
video_files =  glob('*.mov') + glob('*.mp4') + glob('*.mxf')

for filename in video_files: #loop all files in directory
    output = filename + "_vimeo.mov"
    def getffprobe(variable, streamvalue, which_file):
        variable = subprocess.check_output(['ffprobe',
                                                    '-v', 'error',
                                                    '-select_streams', 'v:0',
                                                    '-show_entries', 
                                                    streamvalue,
                                                    '-of', 'default=noprint_wrappers=1:nokey=1',
                                                    which_file])
        return variable
    video_height = float(getffprobe('video_height','stream=height', filename))
    video_width = float(getffprobe('video_width','stream=width', filename))
	
    print video_height
    print video_width
	# Calculate x and y coordinates of the timecode and watermark
    vertical_position_timecode = video_height / 1.2
    horizontal_position_timecode = video_width / 2
    horizontal_watermark_position_timecode = video_width / 2
    vertical_watermark_position_timecode = video_height / 2.1
    # Calculate appropriate font size
    font_size = video_height / 12
    watermark_size = video_height / 14
    #pdb.set_trace()
	
    if _platform == "darwin":
        textoptions = ("fontsize=%d:x=%d-text_w/2:y=%d" % 
        (font_size,horizontal_position_timecode,vertical_position_timecode))
        print "OS X"
        font_path= "fontfile=/Library/Fonts/AppleGothic.ttf"
    elif _platform == "linux2":
        textoptions = ("fontsize=%d:x=%d-text_w/2:y=%d" % 
        (font_size,horizontal_position_timecode,vertical_position_timecode))
        print "OS X"
        font_path= "fontfile=/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
	
    elif _platform == "win32":
        textoptions = ("fontsize=%d:x=%d-text_w/2:y=%d'" % 
        (font_size,horizontal_position_timecode,vertical_position_timecode))
        font_path = "'fontfile=C\:\\\Windows\\\Fonts\\\\'arial.ttf'"
    
    watermark_options = ("fontsize=%d:x=%d-text_w/2:y=%d-text_h/2:alpha=0.3" % 
    (watermark_size,horizontal_watermark_position_timecode,vertical_watermark_position_timecode))
    print  textoptions
	
    # Get starting timecode. In a raw state that requires further processing further on in the script.
    timecode_test_raw = getffprobe('timecode_test_raw','format_tags=timecode:stream_tags=timecode', filename)
    get_framerate = getffprobe('get_frame_rate','stream=avg_frame_rate', filename)
	
	# This tests if there is actually a timecode present in the file.								
    if not timecode_test_raw:
		# The timecode needs to be phrased in a way unique to each operating system.
		# Note the backslashes.
		# This section makes up a timecode if none is present in the file.
        if _platform == "darwin" or _platform == "linux2":
            print "OS X"
            timecode_test = '01\\\:00\\\:00\\\:00'
        elif _platform == "win32":
            print "Windows"
            
            timecode_test = '01\:00\:00\:00'
			
    else:
		# If timecode is present, this will escape the colons
		# so that it is compatible with each operating system.
        if _platform == "darwin" or _platform == "linux2":
            print "OS X"
            timecode_test = timecode_test_raw.replace(':', '\\\:').replace('\n', '')
        elif _platform == "win32":
            print "Windows"
		    
            timecode_test = timecode_test_raw.replace(':', '\\:').replace('\n', '').replace('\r', '')
            print "Windows"

		#pdb.set_trace()
	# This removes the new line character from the framemrate.
    fixed_framerate = get_framerate.rstrip()
	
	#all these prints are just for testing. Will be removed later.
    print fixed_framerate	
    drawtext_options = ("drawtext=%s:fontcolor=white:timecode=%s:\
    rate=%s:boxcolor=0x000000AA:box=1:%s,\
    drawtext=%s:fontcolor=white:text='INSERT WATERMARK TEXT HERE':%s" % 
    (font_path, timecode_test, fixed_framerate, textoptions, font_path, watermark_options))
    print drawtext_options
    print timecode_test
    print get_framerate

    subprocess.call(['ffmpeg',
                    '-i', filename,
                    '-c:v', 'libx264',
                    '-crf', '22',
                    '-pix_fmt', 'yuv420p',
                    '-vf',drawtext_options, output])
