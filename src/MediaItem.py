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

        # Detects dual audio anime, and forces English
        # TODO: if ja, force subtitles?
        try :
            langs = []
            for track in self.media_info.tracks:
                if track.track_type == "Audio":
                    langs.append(track.to_data()['language'])
            if 'en' in langs and 'ja' in langs:
                self.force_english = True
            else : self.force_english = False
        except : 
            self.force_english = False

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
