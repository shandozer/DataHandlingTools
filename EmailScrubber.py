#!/usr/bin/env python
__author__ = 'Shannon T. Buckley'
"""
email scrubber
"""
import email
import poplib
import os
import sys
from os import path
from string import split
import logging
import time
import optparse
import getpass

root = path.join(path.expanduser('~'), 'blah_emails')

_logger = logging.getLogger()

SERVER = 'anyserver.com'


def get_messages(server):
    """
    Downloads the messages from specified server (default port=110), for given user/pw combo.
    Returns list of messages.
    """
    _logger.debug('getting messages')

    messages = server.list()[1]

    msg_num = len(messages)

    _logger.info("there are %s messages" % msg_num)

    return messages


def process_message(an_email):
    """
    Parses one email object.
    Returns a dictionary with the header pieces.
    """
    full_msg = email.message_from_string(an_email)

    datestr = full_msg.get("Date")
    messagedate = email.utils.parsedate(datestr)
    datestr = time.strftime("%Y.%m.%d.%H%M", messagedate)

    to_line = full_msg.get("To")
    to_line = to_line.split('"')[1]

    filename = '%s_%s.txt' % (to_line, datestr)
    filepath = path.join(output_path, filename)

    sub_line = full_msg.get("Subject")

    from_line = full_msg.get("From").lower()

    targets = get_from_line(from_line)

    f = open(filepath, 'w')

    f.write("Subject: " + sub_line)

    for part in full_msg.walk():

        if part.get_content_type() == "text/plain":

            msg_body = part.get_payload(decode=True)

            redacted = redact_message_body(msg_body, targets)

            f.write((redacted + datestr))

    f.close()


def get_from_line(message):
    """
    :param message_text: email message (as string)
    :return: list of from-line elements we care about.
    """

    #email_pattern = r"([A-Za-z0-9_-%.]+)@([A-Za-z0-9_]+)\.([A-Za-z]{2,4})"

    from_line = message.lower()

    from_chunk = from_line.split('<')[0]
    from_name = from_chunk.strip('from: ').strip(r'\"')

    last = from_name.split(',')[0]
    first = from_name.split(',')[1].strip()

    email_add = from_line.split('<')[1].strip('>')

    targets = [last, first, email_add]

    return targets


def redact_message_body(message_body, targets=None):
    """
    Takes message body as string and a list of targets to redact.
    Returns body with 'REDACTED' in place of targeted items.
    """
    message_body = message_body.lower()

    if not targets:
        return message_body
    elif targets:
        for targ in targets:
            message_body = message_body.replace(targ, '|REDACTED|')

    return message_body


def main():

    global output_path

    logfile = path.join(output_path, 'email_scrubber.log')
    logging.basicConfig(filename=logfile, level=logging.DEBUG)

    parser = optparse.OptionParser()
    parser.add_option('-u', '--username', dest="user", type="string", help="Username takes the form: user@domain.org")
    parser.add_option("-o", "--output_to", dest="output_path", default=root, type="string", help="Enter a path to a folder.")

    (options, args) = parser.parse_args()

    if options.user is None:
        print "\n\tOops! You need to supply a user name.\n"
        parser.print_help()
        sys.exit(1)
    else:
        user = options.user

    output_path = path.join(options.output_path)

    if not path.exists(output_path):
        os.mkdir(output_path)

    os.chdir(output_path)

    # MAKE SURE YOU SET YOUR SERVER UP FIRST!
    server = poplib.POP3(SERVER, 110)

    try:
        server.user(user)
        pw = getpass.getpass()
        server.pass_(pw)
    except Exception:
        print "\n\tsomething is wrong with either username or Password\n"
        parser.print_help()
        sys.exit(1)

    print 'Connecting and downloading messges...'
    print 'Messages will be found in %s' % output_path

    for msg in get_messages(server):
        msg_num = int(split(msg, " ")[0])
        message = server.retr(msg_num)[1]

        message = "\n".join(message)

        try:
            process_message(message)
        except Exception, ex:
            _logger.exception(ex.message)

    server.quit()

if __name__ == "__main__":
    main()
