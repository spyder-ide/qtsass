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
    logger.debug("Compiling {}...".format(input_file))
    try:
        return qt_conform(sass.compile(string=css_conform(input_file),
                                       source_comments=False,
                                       custom_functions={
                                           'qlineargradient': qlineargradient,
                                           'rgba': rgba
                                           }
                                       )
                          )
    except sass.CompileError as e:
        logging.error("Failed to compile {}:\n{}".format(input_file, e))
    return ""

def compile_to_css_and_save(input_file, dest_file):
    stylesheet = compile_to_css(input_file)
    if dest_file:
        with open(dest_file, 'w') as css_file:
            css_file.write(stylesheet)
            logger.info("Created CSS file {}".format(dest_file))
    else:
        print(stylesheet)


class SourceModificationEventHandler(FileSystemEventHandler):
    def __init__(self, input_file, dest_file):
        super(SourceModificationEventHandler, self).__init__()
        self._input_file = input_file
        self._dest_file = dest_file
        self._watched_extension = os.path.splitext(self._input_file)[1]

    def _recompile(self):
        i = 0
        success = False
        while i < 10 and not success:
            try:
                time.sleep(0.2)
                compile_to_css_and_save(self._input_file, self._dest_file)
                success = True
            except FileNotFoundError:
                i += 1

    def on_modified(self, event):
        # On Mac, event will always be a directory.
        # On Windows, only recompile if event's file has the same extension as the input file
        if event.is_directory or os.path.splitext(event.src_path)[1] == self._watched_extension:
            self._recompile()

    def on_created(self, event):
        if os.path.splitext(event.src_path)[1] == self._watched_extension:
            self._recompile()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="QtSASS",
                                     description="Compile a Qt compliant CSS file from a SASS stylesheet.",
                                     )
    parser.add_argument('input', type=str, help="The SASS stylesheet file.")
    parser.add_argument('-o', '--output', type=str, help="The path of the generated Qt compliant CSS file.")
    parser.add_argument('-w', '--watch', action='store_true', help="Whether to watch source file "
                                                                   "and automatically recompile on file change.")

    args = parser.parse_args()
    compile_to_css_and_save(args.input, args.output)

    if args.watch:
        event_handler = SourceModificationEventHandler(args.input, args.output)
        logging.info("qtsass is watching {}...".format(args.input))
        observer = Observer()
        observer.schedule(event_handler, os.path.dirname(args.input), recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
