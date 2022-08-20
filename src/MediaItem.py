import pymediainfo
import datetime
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
        # if only Japanese audio, set Subtitles File and Force Subtitles flag
        # if Force Subtitles already set True, set Subtitles File
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
            if self.video_path[-3:] == "mkv":
                self.subtitle_file = self.video_path
            elif exists(self.video_path[:-3] + "ass"):
                self.subtitle_file = self.video_path[:-3] + "ass"
            elif exists(self.video_path[:-3] + "eng.ass"):
                self.subtitle_file = self.video_path[:-3] + "eng.ass"
            elif exists(self.video_path[:-3] + "srt"):
                self.subtitle_file = self.video_path[:-3] + "srt"
            elif exists(self.video_path[:-3] + "eng.srt"):
                self.subtitle_file = self.video_path[:-3] + "eng.srt"
            else : print("No Subs Found for file %s\nContinuing anyway..." % self.video_path)

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
