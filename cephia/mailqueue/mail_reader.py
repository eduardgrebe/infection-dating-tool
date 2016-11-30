import imaplib
import logging
import email
logger = logging.getLogger(__name__)

def get_messages(servername, username, password):
  conn = imaplib.IMAP4_SSL(servername)
  conn.login(username, password)
  conn.select('Inbox')
  typ, data = conn.search(None,'(UNSEEN)')
  for num in data[0].split():
    logger.debug('Downloaded message: %s' % num)
    typ, data = conn.fetch(num,'(RFC822)')
    msg = email.message_from_string(data[0][1])
    conn.store(num,'+FLAGS','\\Seen')
    logger.debug('Marked message %s as seen' % num)
    yield num, data[0][1], msg

def get_attachments(msg):
  parts = []
  for part in msg.walk():
    if part.get_filename():
      parts.append((part.get_filename(), part.get_payload(decode=1)))
  return parts


