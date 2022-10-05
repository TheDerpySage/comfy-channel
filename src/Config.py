# Auto-Channel configuration file

# Gets current time for upnext time calculation
TIME_INDEX = None

# Desired Resolution
W = 854 
H = 480

MAX_SAME_FILE_RETRIES = 3  # Number of times to attempt playing a file before giving up
MAX_CONSECUTIVE_RETRIES = 3  # If several consecutive files fail, exit program

PLAYOUT_FILE = 'playout.ini'
TRACKER_FILE = 'comfy-tracker.json'
OUTPUT_LOCATION = 'rtmp://localhost/live/stream'
LOOP = True

SCHEDULER_UPNEXT_VIDEO_FOLDER = 'upnext/video'
SCHEDULER_UPNEXT_AUDIO_FOLDER = 'upnext/audio'
SCHEDULER_UPNEXT_WISDOM_FILE = 'upnext/wisdom.txt'

BUMP_FOLDER = 'bumpers'

OVERLAY_FILE = 'upnext/moe_scaled.png'
OVERLAY_FILE_OUTLINE = False
OVERLAY_X = W - 120
OVERLAY_Y = 0

# Settings that are the same between Serv and Client
PIX_FMT = 'yuv420p'
PRESET = 'ultrafast'

SERV_DRAWTEXT_X = 25
SERV_DRAWTEXT_Y = 25
SERV_DRAWTEXT_SHADOW_X = 2
SERV_DRAWTEXT_SHADOW_Y = 2
SERV_DRAWTEXT_SHADOW_COLOR = 'black'
SERV_DRAWTEXT_FONT_FILE = 'fonts/hc-too5.ttf'
SERV_DRAWTEXT_FONT_SIZE = 20
SERV_DRAWTEXT_FONT_COLOR = 'white'

SERV_OUTPUT_VCODEC = 'h264'
SERV_OUTPUT_ASPECT = "%s:%s" % (W, H)
SERV_OUTPUT_CRF = 18
SERV_OUTPUT_ACODEC = 'aac'
SERV_OUTPUT_FORMAT = 'flv'

CLIENT_DRAWTEXT_X = 25
CLIENT_DRAWTEXT_Y = 90
CLIENT_DRAWTEXT_SHADOW_X = 2
CLIENT_DRAWTEXT_SHADOW_Y = 2
CLIENT_DRAWTEXT_SHADOW_COLOR = 'black'
CLIENT_DRAWTEXT_FONT_FILE = 'fonts/hc-too5.ttf'
CLIENT_DRAWTEXT_FONT_SIZE = 16
CLIENT_DRAWTEXT_FONT_COLOR = 'white'

CLIENT_VCODEC = 'h264'
CLIENT_ASPECT = "%s:%s" % (W, H)
CLIENT_FLAGS = '+cgop'
CLIENT_G = 25
CLIENT_ACODEC = 'aac'
CLIENT_STRICT = 1
CLIENT_AUDIO_BITRATE = '168k'
CLIENT_AUDIO_RATE = 44100
CLIENT_HLS_ALLOW_CACHE = 0
CLIENT_HLS_TIME = 3
CLIENT_HLS_LIST_SIZE = 5
CLIENT_FORMAT = 'hls'
CLIENT_FLEX = 3
CLIENT_ENABLE_DEINTERLACE = True
