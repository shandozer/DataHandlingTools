#!/usr/local/bin/python

"""
email scrubber
"""
import email
import poplib
import os
from os import path
from string import split
import logging
import time

root = path.join('/Users/you/somewhere/')

logfile = path.join(root, 'email_scrubber.log')

logging.basicConfig(filename=logfile, level=logging.DEBUG)

_logger = logging.getLogger()


SERVER = 'blah.server.com'
USER = 'user@blah.org'
PW = 'stuff'



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

    filename = 'bhr_email_%s.txt' % datestr
    filepath = path.join(root, filename)

    from_line = full_msg.get("From").lower()

    targets = get_from_line(from_line)
    _logger.info('Targets are: %s' % targets)

    f = open(filepath, 'w')

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


    # EXAMPLE_FROM_LINE = r'From: "Last, First" <First.Last@ucsf.edu>'

    #email_pattern = r"([A-Za-z0-9_-%.]+)@([A-Za-z0-9_]+)\.([A-Za-z]{2,4})"

    from_line = message.lower()

    _logger.debug('from line is %s' % from_line)

    from_chunk = from_line.split('<')[0]
    from_name = from_chunk.strip('from: ').strip(r'\"')

    last = from_name.split(',')[0]
    first = from_name.split(',')[1].strip()

    email_add = from_line.split('<')[1].strip('>')

    _logger.debug('From-line parts are %s, %s, %s' % (email_add, last, first))

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

    if not path.exists(root):
        print 'making email box to store your messages...'
        os.mkdir(root)

    os.chdir(root)

    print 'attempting connection...'

    server = poplib.POP3(SERVER, 110)

    server.user(USER)
    server.pass_(PW)

    print 'connected!\nGetting messages...'

    for msg in get_messages(server):
        msg_num = int(split(msg, " ")[0])
        message = server.retr(msg_num)[1]

        message = "\n".join(message)

        try:
            print 'processing new message...'
            process_message(message)
        except Exception, ex:
            _logger.exception(ex.message)

    print 'closing connection...'

    server.quit()

if __name__ == "__main__":
    main()
