
from subprocess import Popen, PIPE


class ClipboardUtils:

    def copy_text(self, text):

        copy_process = Popen(["wl-copy"], stdout=PIPE, stdin=PIPE)
        copy_process.communicate(input=text.encode())[0]


    def contents(self):

        check_process = Popen(["wl-paste", "-n"], stdout=PIPE)
        return check_process.communicate()[0].decode()
