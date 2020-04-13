# Todo: migrate stuffs to pdu.py

# All heavily based on functions available at:
#  https://github.com/pmarti/python-messaging/blob/master/messaging/mms/wsp_pdu.py
#  https://github.com/pmarti/python-messaging/blob/master/messaging/mms/mms_pdu.py

# MMS Version 1.1 is a good solid one

import array
import itertools

from wap_mms_message.const import ADDRESS_PRESENT_TOKEN


class MMSMessageHeader(object):

    type_code = 0x00

    def __init__(self, *args, **kwargs):
        self.buffer = []
        self.initialize(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        pass

    # These encoding functions assume the user knows what they are doing.

    def encode(self):

        type_code_buffer = []

        if self.type_code:
            type_code_buffer = self.encode_short_integer(self.type_code)

        return array.array(
            'B',
            itertools.chain(
                type_code_buffer,
                self.buffer
            )
        )

    @staticmethod
    def encode_short_integer(integer: int) -> [int]:
        """
        Assumes an integer between 0 and 128 is being encoded.  The integer
        will have a new base of 0x80.
        """

        return [integer | 0x80]

    @staticmethod
    def encode_long_integer(long: int) -> [int]:
        """
        Assumes a very long integer that isn't long enough to not be a
        python long.
        """

        encoded_long_int = []
        long_int = long

        while long_int > 0:
            # chomp chomp
            byte = 0xff & long_int
            encoded_long_int.append(byte)
            long_int = long_int >> 8

        return [len(encoded_long_int)] + encoded_long_int

    @staticmethod
    def encode_uint_var(integer: int) -> [int]:
        integer_var = [integer & 0x7f]

        integer = integer >> 7

        while integer > 0:
            integer_var.insert(0, 0x80 | (integer & 0x7f))
            integer = integer >> 7

        return integer_var

    @staticmethod
    def encode_string(string: str) -> [int]:
        return [ord(c) for c in string] + [0x00]

    @staticmethod
    def encode_version(version: str) -> [int]:
        major, minor = map(int, version.split('.'))
        return MMSMessageHeader.encode_short_integer(major << 4 | minor)


class MMSIntegerHeader(MMSMessageHeader):

    type_code = None

    def initialize(self, i: str) -> None:
        self.buffer.extend(self.encode_short_integer(i))


class MMSStringHeader(MMSMessageHeader):

    type_code = None

    def initialize(self, s: str) -> None:
        self.buffer.extend(
            self.encode_string(s)
        )


class MMSTextStringHeader(MMSMessageHeader):

    type_code = None

    def initialize(self, t: str, s: str) -> None:
        self.buffer.extend(self.encode_string(t))
        self.buffer.extend(self.encode_string(s))


class MMSMessageTypeHeader(MMSIntegerHeader):
    type_code = 0x0c


class MMSTransactionIdHeader(MMSStringHeader):
    type_code = 0x18


class MMSVersionHeader(MMSMessageHeader):

    type_code = 0x0d

    def initialize(self, s: str) -> None:
        self.buffer.extend(self.encode_version(s))

# Assumes that ordering is completely under the control of the user


class MMSFromHeader(MMSMessageHeader):

    type_code = 0x09

    def initialize(self, s: str) -> None:
        # TODO: Modify to utilize insert token rather than always use string
        encoded_string = self.encode_string(s)
        self.buffer.append(len(encoded_string) + 1)
        self.buffer.extend(self.encode_short_integer(ADDRESS_PRESENT_TOKEN))
        self.buffer.extend(encoded_string)


class MMSToHeader(MMSStringHeader):
    type_code = 0x17


class MMSContentTypeHeader(MMSMessageHeader):

    type_code = 0x04

    def initialize(self, m: str, l: int) -> None:
        encoded_string = self.encode_string(m)
        # print(len(encoded_string))

        # application/vnd.wap.multipart.mixed See WSP 30-April-1998, section 8.4.2.24, for more information.
        self.buffer.extend(self.encode_short_integer(0x23))

        self.buffer.extend(self.encode_long_integer(len(encoded_string)))
        self.buffer.extend(self.encode_uint_var(l))
        self.buffer.extend(encoded_string)


class MMSMessage(object):

    def __init__(self, headers: [MMSMessageHeader] = []):
        self.headers = headers

    def add_header(self, header):
        self.headers.append(header)

    def encode(self):

        byte_array = array.array('B')

        for header in self.headers:
            byte_array.extend(header.encode())

        return byte_array.tobytes()


if __name__ == "__main__":
    # Lets run a test
    import sys
    from wap_mms_message.const import MSG_TYPE_SEND_REQ

    mms = MMSMessage()

    # Well-Known Header
    mms.add_header(MMSMessageTypeHeader(MSG_TYPE_SEND_REQ))
    mms.add_header(MMSTransactionIdHeader('5E90EBA9'))
    mms.add_header(MMSVersionHeader('1.1'))
    # Weird Date-Created Header
    mms.add_header(MMSTextStringHeader('date-created', '5e90eba9'))
    # From Headers
    mms.add_header(MMSFromHeader('+16305327102/TYPE=PLMN'))
    mms.add_header(MMSTextStringHeader('from-name', '(630) 532-7102'))
    # To Header
    mms.add_header(MMSToHeader('+19074062591/TYPE=PLMN'))
    # Weird Msg-Type Header
    mms.add_header(MMSTextStringHeader('msg-type', '80005'))
    # Content-Type Header (includes magic)
    mms.add_header(MMSContentTypeHeader('audio/amr', 6310))

    sys.stdout.buffer.write(mms.encode())
