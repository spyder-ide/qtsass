import sass
import argparse
import logging
import os
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



def rgba(r, g, b, a):
    result = "rgba({}, {}, {}, {}%)"
    if isinstance(r, sass.SassNumber):
        return result.format(int(r.value), int(g.value), int(b.value), int(a.value)*100)
    elif isinstance(r, float):
        return result.format(int(r), int(g), int(b), int(a)*100)


def rgba_from_color(color):
    """
    Conform rgba
    :type color: sass.SassColor
    """
    return rgba(color.r, color.g, color.b, color.a)


def qlineargradient(x1, y1, x2, y2, stops):
    """
    :type x1: sass.SassNumber
    :type y1: sass.SassNumber
    :type x2: sass.SassNumber
    :type y2: sass.SassNumber
    :type stops: sass.SassList
    :return:
    """
    stops_str = ""
    for stop in stops[0]:
        pos, color = stop[0]
        stops_str += " stop: {} {}".format(pos.value, rgba_from_color(color))

    return "qlineargradient(x1:{}, y1:{}, x2:{}, y2:{} {})".format(x1.value, y1.value, x2.value, y2.value, stops_str.rstrip(","))


def css_conform(input_file):
    with open(input_file, "r") as f:
        # Remove "!" in selectors
        input_str = f.read().replace(":!", ":_qnot_")
    return input_str


def qt_conform(input_str):
    """
    :param input_str:
    :type input_str: string
    :return:
    """
    conformed = input_str.replace(":_qnot_", ":!")
    return conformed


def compile_to_css(input_file):
    return qt_conform(sass.compile(string=css_conform(input_file),
                                   source_comments=False,
                                   custom_functions={
                                       'qlineargradient': qlineargradient,
                                       'rgba': rgba
                                       }
                                   )
                      )


def compile_to_css_and_save(input_file, dest_file):
    stylesheet = compile_to_css(input_file)
    if dest_file:
        with open(dest_file, 'w') as css_file:
            css_file.write(stylesheet)
            logger.info("Created CSS file {}".format(args.output))
    else:
        print(stylesheet)

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, input_file, dest_file):
        super(MyEventHandler, self).__init__()
        self._input_file = input_file
        self._dest_file = dest_file
        self._watched_extension = os.path.split(self._input_file)[1]

    def on_modified(self, event):
        # TODO: watch a specific kind of file
        #       but for now, watchdog only returns the directory...
        # if os.path.split(event.src_path)[1] == self._watched_extension:
        logger.debug("Have to reload : {}".format(event.src_path))
        compile_to_css_and_save(self._input_file, self._dest_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="QtSASS",
                                     description="Compile a Qt compliant CSS file from a SASS stylesheet.",
                                     )
    parser.add_argument('input', type=str, help="The SASS stylesheet file.")
    parser.add_argument('-o', '--output', type=str, help="The path of the generated Qt compliant CSS file.")
    parser.add_argument('-w', '--watch', help="Whether to watch source file "
                                                         "and automatically recompile on file change.")

    args = parser.parse_args()

    stylesheet = compile_to_css(args.input)

    if args.watch:
        event_handler = MyEventHandler(args.input, args.output)
        observer = Observer()
        observer.schedule(event_handler, os.path.dirname(args.input), recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        compile_to_css_and_save(args.input, None)
