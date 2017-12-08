from email.header import decode_header
from email.parser import HeaderParser
import logging
import email
import re
import mailbox
import codecs
import io
import mmap
from base64 import b64decode
import quopri
import re
from email.header import decode_header

class EmailUtility:
    logger = logging.getLogger(__name__)
    
    re_bq_encoding = re.compile(r'=\?(.*?)\?(B|Q)\?(.*?)\?=')

    @staticmethod
    def get_headers(sample_path):
        try:
            with codecs.open(sample_path, 'r', encoding='utf-8', errors='ignore') as f:
                parser = email.parser.HeaderParser()
                headers = parser.parse(f)

                return headers
        except Exception as ex:
            EmailUtility.logger.warn('Exception occurs while doing get_headers of [%s]: %s' %(sample_path, ex))

    @staticmethod
    def get_body(sample_path, content_type='text/plain'):
        target_data = None

        with codecs.open(sample_path, 'r', encoding='utf-8', errors='ignore') as f:
            msg_obj = email.message_from_file(f)

            if msg_obj.is_multipart():
                for part in msg_obj.walk():
                    ctype = part.get_content_type()

                    # skip any text/plain (txt) attachments
                    if ctype == content_type:
                        target_data = part.get_payload(decode=True)
                        break
            else:            
                target_data = msg_obj.get_payload(decode=True)

        return target_data

    @classmethod
    def decode_bq_str(cls, bq_str):
        '''
        =?utf-8?B?5aaC5L2V5oqK5o+h6LWi5Y+W5aSn6K6i5Y2V5b+F5aSH5p2h5Lu277yfNjAueGxz?=
        '''

        try:
            matches = re.findall(cls.re_bq_encoding, bq_str)
            if matches:
                new_str = ''
                for match in matches:
                    if match[1] == 'B':
                        new_str += b64decode(match[2]).decode(match[0], 'ignore')
                    elif match[1] == 'Q':
                        new_str += quopri.decodestring(match[2]).decode(match[0], 'ignore')

                return new_str
        except Exception as ex:
            cls.logger.warn('Exception occurs while doing decode_bq_str(%s): %s' %(bq_str, ex))

        try:
            return bq_str.decode('utf-8', 'ignore')
        except:
            return bq_str

    @classmethod
    def get_attachment_filename(cls, sample_path, ext=None):
        try:
            with codecs.open(sample_path, 'r', encoding='utf-8', errors='ignore') as f:
                msg = email.message_from_file(f)
    
                for part in msg.walk():
                    filename = part.get_filename()

                    if filename:
                        filename = cls.decode_bq_str(filename)

                        if ext:
                            if filename.endswith(ext):
                                return filename
                        else:
                            return filename
                        
        except Exception as ex:
            EmailUtility.logger.warn('Exception occurs while doing get_attachment_filename of [%s]: %s' %(sample_path, ex))


    @staticmethod
    def parseaddr(line):
        return email.utils.parseaddr(line)

if __name__ == '__main__':
    print(EmailUtility.get_body('1471965162-03747399510295751170.eml').decode())
    pass

