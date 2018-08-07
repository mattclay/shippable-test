from __future__ import absolute_import, print_function


class Display:
    def info(self, message):
        print(message, flush=True)


display = Display()
