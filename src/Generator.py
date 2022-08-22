import os
import random
import json
from datetime import timedelta
from pymediainfo import MediaInfo

import Logger
import Config as c
from MediaItem import MediaItem


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield os.path.join(path, f)

def listdir_file_walk(dir):
    directory_listing = []

    for path, dirs, files in os.walk(dir):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for name in files:
            directory_listing += [os.path.join(path, name)]

    return directory_listing

def get_tracker_val(dir):
    with open(c.TRACKER_FILE, 'r') as f:
        j = json.loads(f.read())
        return j[dir]

def set_tracker_val(dir, val):
    with open(c.TRACKER_FILE, 'r') as f:
        j = json.loads(f.read())
    j[dir] = val
    with open(c.TRACKER_FILE, 'w') as f:
        json.dump(j, f, indent=4)


def gen_playlist(dir, mode="sequential", num_files=None, subtitles=0):
    playlist = []

    # Single (No need to do all the extra processing)
    if mode == "single":
        Logger.LOGGER.log(Logger.TYPE_INFO,
                      'Generating playlist from single file: {}'.format(dir))
        playlist.append(MediaItem(dir, subtitles=subtitles))
        return playlist

    Logger.LOGGER.log(Logger.TYPE_INFO,
                      'Generating playlist from directory: {}'.format(dir))

    directory_listing = []
    x = 0

    # https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files
    for path, dirs, files in os.walk(dir):
        dirs.sort()
        files.sort()
        # Walks dirs and files, filtering dot files and folders, extensions commonly used for subtitles, and the Specials folder
        files = [f for f in files if (not f[0] == '.') and (not f.split('.')[-1] in ['srt', 'ass', 'idx', 'sub'])]
        dirs[:] = [d for d in dirs if (not d[0] == '.') and (not d[0] == 'Specials')]
        for name in files:
            directory_listing += [os.path.join(path, name)]

    # If no num_files is passed, just use whole dir
    # (Used mainly by generating the bump playlist)
    if num_files == None:
        num_files = len(directory_listing)

    # Shuffle directory listing
    if mode == "shuffle":
        random.SystemRandom().shuffle(directory_listing, random.SystemRandom().random)
    # Tracker gets the current tracked value, and sets the beginning index to it
    elif mode == "tracker":
        try:
            x = get_tracker_val(dir)
        except KeyError:
            set_tracker_val(dir, 0)
        set_tracker_val(dir, x + num_files)
    # Sequential does nothing else, just nop
    elif mode == "sequential":
        pass
    else: raise ValueError("Mode %s not valid for a playlist" % mode)

    # Deal with Overflow (will start the listing over if there isnt num_files in it)
    difference = (x + num_files) - len(directory_listing)
    if difference > 0:
        # When theres overflow and tracking is enabled, write the difference the tracker (so we don't overflow again)
        if mode == "tracker": set_tracker_val(dir, difference)
        for i in directory_listing[x:x+(num_files-difference)]:
            playlist.append(MediaItem(i, subtitles=subtitles))
        for i in directory_listing[0:difference]:
            playlist.append(MediaItem(i, subtitles=subtitles))
    else:
        for i in directory_listing[x:x+num_files]:
            playlist.append(MediaItem(i, subtitles=subtitles))

    return playlist


def gen_upnext(video_dir, audio_dir=None, name=None, playlist=None, info_file=None):
    video_file = None
    audio_file = None
    info_text = None

    video_file = random.SystemRandom().choice(list(listdir_nohidden(video_dir)))
    audio_file = random.SystemRandom().choice(listdir_file_walk(audio_dir))

    if playlist:
        info_text = gen_upnext_text(playlist, name, info_file=info_file, duration=MediaInfo.parse(video_file).tracks[0].duration/1000)

    return MediaItem(video_path=video_file, audio_path=audio_file, media_type="upnext", overlay_text=info_text)


def gen_upnext_text(playlist, name=None, info_file=None, duration=0):
    # Displayed times will get a touch off the more Bumps happen
    overlay_text = ""
    if name is not None : overlay_text += name + "\n\n"
    c.TIME_INDEX += timedelta(seconds=duration) # Upnext Length 
    for item in playlist:
        if playlist[0].title == item.title:
            overlay_text += 'Next -' + \
            "  " + item.title + "\n\n"
        else:
            overlay_text += c.TIME_INDEX.strftime("%H:%M") + ' -' + \
            "  " + item.title + "\n\n"
        c.TIME_INDEX += timedelta(seconds=(item.duration/1000))
    if info_file:
        overlay_text += "\n" + get_random_line(info_file)
    return overlay_text

def just_advance_timeindex(playlist):
    for item in playlist:
        c.TIME_INDEX += timedelta(seconds=(item.duration/1000))


def get_random_line(file):
    file = open(file)
    random_line = random.SystemRandom().choice(file.readlines())
    random_line += str("\n")
    file.close()
    return random_line
