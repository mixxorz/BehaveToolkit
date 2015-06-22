import subprocess
import threading

import sublime

from .mixins.output_panel import OutputPanelMixin
from .mixins.steps import StepsMixin


class BehaveCommand(OutputPanelMixin,
                    StepsMixin):

    '''
    Base class for all Sublime commands that interact with behave
    '''

    def behave(self, *args, **kwargs):
        '''
        Run the behave command specified in `*args` and return the output
        of the command as a string. If print_stream=True, the output will be
        streamed in an output panel.
        '''

        command = tuple(self.behave_command) + \
            tuple(arg for arg in args if arg)

        print('Command %s' % (command,))

        return self._launch_process(command,
                                    print_stream=kwargs.get('print_stream'))

    @property
    def behave_command(self):
        '''
        The command used to launch behave. This can be set by modifying the
        behave_command setting. The setting should be a list. If not set, the
        plugin uses value of `which behave`.
        '''
        behave = self.view.settings().get('behave_command')

        if behave:
            return behave
        else:
            # Find the behave executable
            which = 'which'
            if sublime.platform() == 'windows':
                which = 'where'

            out = self._launch_process([which, 'behave'])
            return [out.strip()]

    def _launch_process(self, command, print_stream=False):
        '''
        Launches a process and returns its output as a string. If
        print_stream=True, it will also stream the output to an output panel.
        '''

        startupinfo = None
        if sublime.platform() == 'windows':
            # Prevent Windows from opening a console when starting a process
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   bufsize=1,
                                   universal_newlines=True,
                                   cwd=self.view.window().folders()[0],
                                   startupinfo=startupinfo)

        if print_stream:
            self.erase()
            streamer = StreamerThread(self.append, process.stdout)
            streamer.start()
            streamer.join()

        stdout, stderr = process.communicate()

        return stdout


class StreamerThread(threading.Thread):

    '''
    Streams `stream` to the output panel.
    '''

    def __init__(self, append, stream):
        super(StreamerThread, self).__init__()
        self.append = append
        self.stream = stream

    def run(self):
        for line in self.stream:
            self.append(line, end='')
