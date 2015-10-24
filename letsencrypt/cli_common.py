import os
import traceback
import sys
import logging
import logging.handlers

from letsencrypt.errors import Error

logger = logging.getLogger('__main__')


def handle_exception(exc_type, exc_value, trace, args):
    """Logs exceptions and reports them to the user.

    Args is used to determine how to display exceptions to the user. In
    general, if args.debug is True, then the full exception and traceback is
    shown to the user, otherwise it is suppressed. If args itself is None,
    then the traceback and exception is attempted to be written to a logfile.
    If this is successful, the traceback is suppressed, otherwise it is shown
    to the user. sys.exit is always called with a nonzero status.

    """
    logger.debug(
        "Exiting abnormally:%s%s",
        os.linesep,
        "".join(traceback.format_exception(exc_type, exc_value, trace)))

    if issubclass(exc_type, Exception) and (args is None or not args.debug):
        if args is None:
            logfile = "letsencrypt.log"
            try:
                with open(logfile, "w") as logfd:
                    traceback.print_exception(
                        exc_type, exc_value, trace, file=logfd)
            except:  # pylint: disable=bare-except
                sys.exit("".join(
                    traceback.format_exception(exc_type, exc_value, trace)))

        if issubclass(exc_type, Error):
            sys.exit(exc_value)
        else:
            # Tell the user a bit about what happened, without overwhelming
            # them with a full traceback
            msg = ("An unexpected error occurred.\n" +
                   traceback.format_exception_only(exc_type, exc_value)[0] +
                   "Please see the ")
            if args is None:
                msg += "logfile '{0}' for more details.".format(logfile)
            else:
                msg += "logfiles in {0} for more details.".format(args.logs_dir)
            sys.exit(msg)
    else:
        sys.exit("".join(
            traceback.format_exception(exc_type, exc_value, trace)))
