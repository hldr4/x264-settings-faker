import subprocess
import sys
from shutil import which
from datetime import date

# constant
sei_userdata_uuid = 'DC45E9BDE6D948B7962CD820D923EEEF'
header_copyright = f'H.264/MPEG-4 AVC codec - Copyleft 2003-{date.today().year} - http://www.videolan.org/x264.html'

# default, can be changed in the args
x264_version = 'core 133 r2334 a3ac64b'

in_, out_, settings, *extra = sys.argv[1:]

if extra:
    x264_version = extra[0]

exe = which('ffmpeg')
if not exe:
    sys.exit('\nffmpeg not found')
    
# when copying settings from mediainfo the slash separator needs removed
settings = settings.replace(' / ', ' ')
    
# chars that need escaped
escapes = {':': ('\\\\:' if sys.platform == 'win32' else '\\\\\\\\:')} # bash wants \\\\
escapes.update({c: f'\\{c}' for c in '),('})

options = f'{sei_userdata_uuid}+x264 - {x264_version} - {header_copyright} - options: {settings}'

options = ''.join([escapes.get(char, char) for char in options])
    
cmd = [exe, '-i', in_, '-y', '-c:v', 'copy', '-bsf:v', f'h264_metadata=sei_user_data="{options}"', out_]

print('\nChanging settings...')

result = subprocess.run(' '.join(cmd), shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if result.returncode:
    sys.exit(f"\n - Failed to change settings, ffmpeg error: {result.stderr.decode().split(chr(10))[-2]}")

print('\n + Changed successfully')
