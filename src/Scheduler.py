import configparser
import os.path
import Config as c
import Generator
import Logger

class Block:

    def __init__(self, name, folder, num_files, mode, bump_chance, upnext_enabled):
        self.name = name
        self.folder = folder
        self.num_files = int(num_files)
        self.mode = mode
        self.bump_chance = float(bump_chance)
        self.upnext_enabled = int(upnext_enabled)
        self.playlist = []
        playlist = Generator.gen_playlist(self.folder, self.mode, self.num_files)
        if(upnext_enabled == 1):
            upnext = Generator.gen_upnext(c.SCHEDULER_UPNEXT_VIDEO_FOLDER,
                                        c.SCHEDULER_UPNEXT_AUDIO_FOLDER,
                                        self.name,
                                        playlist,
                                        c.SCHEDULER_UPNEXT_WISDOM_FILE)
        self.playlist += [upnext] + playlist


class Scheduler:

    def __init__(self, input_file):
        self.config = configparser.ConfigParser()
        if not os.path.isfile(input_file):
            Logger.LOGGER.log(Logger.TYPE_INFO,
                    'Playout file not found!: {}'.format(input_file))
        self.config.read(input_file)

        self.blocklist = []

        c = self.config
        for i in self.config.sections():
            block = Block(c[i]['name'], c[i]['folder'], c[i]['files'], c[i]['mode'], c[i]['bump_chance'], c[i]['upnext_enabled'])
            self.blocklist.append(block)
