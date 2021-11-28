import pymediainfo
import datetime


class MediaItem:

    # media_type available: upnext, regular
    def __init__(self, video_path, audio_path=None, media_type="regular", overlay_text=None):
        self.video_path = video_path
        self.audio_path = audio_path
        self.overlay_text = overlay_text
        self.media_type = media_type

        self.media_info = pymediainfo.MediaInfo.parse(self.video_path)

        # Hard coded detection of Japanese Audio, setting this allows the Client to select English Audio
        try :
            for track in self.media_info.tracks:
                if track.track_type == "Audio":
                    self.lang = track.to_data()['language']
                    if self.lang == 'ja':
                        break
        except : 
            self.lang = 'en'

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
