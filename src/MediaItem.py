import pymediainfo
import datetime
import Logger
from os.path import exists
    

class MediaItem:

    # media_type available: upnext, regular
    def __init__(self, video_path, audio_path=None, media_type="regular", overlay_text=None, subtitles=0):
        self.video_path = video_path
        self.audio_path = audio_path
        self.media_type = media_type
        self.overlay_text = overlay_text

        self.media_info = pymediainfo.MediaInfo.parse(self.video_path)

        # Detects dual audio anime, set force English Audio flag
        # If subtitles set to 1, search file for subtitles, 
        # if subtitles not in file search directory for some common subtitle files,
        # if no files found, send an error message to stdout but continue
        self.force_english = False
        self.subtitle_file = False
        langs = []
        for track in self.media_info.tracks:
            if track.track_type == "Audio":
                try :
                    langs.append(track.to_data()['language'])
                except : pass
        if 'en' in langs and 'ja' in langs:
            self.force_english = True
        if subtitles == 1:
            for track in self.media_info.tracks:
                if track.track_type == "Text":
                    self.subtitle_file = self.video_path
                    break
            if (not self.subtitle_file): 
                exts = ['ass', 'srt', 'eng.ass', 'eng.srt', 'sub']
                for ext in exts:
                    if(exists(video_path[:-3] + ext)):
                        self.subtitle_file = video_path[:-3] + ext
                        break
            if (not self.subtitle_file):
                Logger.LOGGER.log(Logger.TYPE_ERROR,
                    'No subs found for file: {}'.format(self.video_path))

        if not self.media_info.tracks[0].other_file_name:
            self.title = self.media_info.tracks[0].file_name
        else:
            self.title = self.media_info.tracks[0].other_file_name[0]
        self.duration = self.media_info.tracks[0].duration or 0
        self.duration_readable = datetime.timedelta(milliseconds=int(float(self.duration)))
        self.file_extension = self.media_info.tracks[0].file_extension

    def __str__(self):
        if self.media_type == "upnext":
            return (self.video_path, self.audio_path, self.overlay_text)
        else:
            return self.video_path
