import unittest

from nepali.char import nepali_to_english_text
from nepali.datetime import nepalidatetime
from nepali.datetime import parser as nepalidatetime_parser
from nepali.datetime.parser.validators import NepaliTimeRE, extract
from nepali.exceptions import InvalidDateTimeFormatException


class TestNepaliDateTimeParserValidators(unittest.TestCase):
    '''
    Tests nepali date
    '''

    def setUp(self) -> None:
        self.nepali_time_re = NepaliTimeRE()
        return super().setUp()
    
    # nepali time re tests

    def test_format_to_regex(self):
        format_to_regex = self.nepali_time_re.pattern('%Y $ \d %-d *')
        self.assertEqual(format_to_regex, r'(?P<Y>\d\d\d\d)\s+\$\s+\\d\s+(?P<d>3[0-1]|[1-2]\d|0[1-9]|[1-9]| [1-9])\s+\*')

    def test_all_format_to_regex(self):
        format_to_regex = self.nepali_time_re.pattern('%a %A %w %d %b %B %m %y %Y %H %I %p %M %S')
        expected_output = r'(?P<a>Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s+(?P<A>Wednesday|Thursday|Saturday|Tuesday|Sunday|Monday|Friday)\s+(?P<w>[0-6])\s+(?P<d>3[0-1]|[1-2]\d|0[1-9]|[1-9]| [1-9])\s+(?P<b>Baishakh|Sharwan|Mangsir|Chaitra|Jestha|Bhadra|Ashwin|Kartik|Falgun|Ashad|Poush|Magh)\s+(?P<B>Baishakh|Sharwan|Mangsir|Chaitra|Jestha|Bhadra|Ashwin|Kartik|Falgun|Ashad|Poush|Magh)\s+(?P<m>1[0-2]|0[1-9]|[1-9])\s+(?P<y>\d\d)\s+(?P<Y>\d\d\d\d)\s+(?P<H>2[0-3]|[0-1]\d|\d)\s+(?P<I>1[0-2]|0[1-9]|[1-9])\s+(?P<p>AM|PM)\s+(?P<M>[0-5]\d|\d)\s+(?P<S>6[0-1]|[0-5]\d|\d)'
        self.assertEqual(format_to_regex, expected_output)

    # test extract

    def test_simple_extract(self):
        extracted_data = extract("2078-01-12", format="%Y-%m-%d")
        self.assertEqual(extracted_data.get('Y'), '2078')
        self.assertEqual(extracted_data.get('m'), '01')
        self.assertEqual(extracted_data.get('d'), '12')

    def test_complex_extract(self):
        extracted_data = extract("Wed Wednesday 3 28 Sharwan Sharwan 04 51 2051 05 05 AM 28 23", format="%a %A %w %d %b %B %m %y %Y %H %I %p %M %S")
        self.assertEqual(extracted_data.get('a'), 'Wed')
        self.assertEqual(extracted_data.get('A'), 'Wednesday')
        self.assertEqual(extracted_data.get('w'), '3')
        self.assertEqual(extracted_data.get('d'), '28')
        self.assertEqual(extracted_data.get('b'), 'Sharwan')
        self.assertEqual(extracted_data.get('B'), 'Sharwan')
        self.assertEqual(extracted_data.get('m'), '04')
        self.assertEqual(extracted_data.get('y'), '51')
        self.assertEqual(extracted_data.get('Y'), '2051')
        self.assertEqual(extracted_data.get('H'), '05')
        self.assertEqual(extracted_data.get('I'), '05')
        self.assertEqual(extracted_data.get('p'), 'AM')
        self.assertEqual(extracted_data.get('M'), '28')
        self.assertEqual(extracted_data.get('S'), '23')

    def test_nepali_to_english_text_conversion(self):
        self.assertEqual(
            nepali_to_english_text('बुध बुधबार ३ २८ साउन साउन ०४ ५१ २०५१ ०५ ०५ शुभप्रभात २८ २३'),
            'Wed Wednesday 3 28 Sharwan Sharwan 04 51 2051 05 05 AM 28 23'
        )

    def test_complex_extract_in_nepali(self):
        extracted_data = extract("बुध बुधबार ३ २८ साउन साउन ०४ ५१ २०५१ ०५ ०५ शुभप्रभात २८ २३", format="%a %A %w %d %b %B %m %y %Y %H %I %p %M %S")
        self.assertEqual(extracted_data.get('a'), 'Wed')
        self.assertEqual(extracted_data.get('A'), 'Wednesday')
        self.assertEqual(extracted_data.get('w'), '3')
        self.assertEqual(extracted_data.get('d'), '28')
        self.assertEqual(extracted_data.get('b'), 'Sharwan')
        self.assertEqual(extracted_data.get('B'), 'Sharwan')
        self.assertEqual(extracted_data.get('m'), '04')
        self.assertEqual(extracted_data.get('y'), '51')
        self.assertEqual(extracted_data.get('Y'), '2051')
        self.assertEqual(extracted_data.get('H'), '05')
        self.assertEqual(extracted_data.get('I'), '05')
        self.assertEqual(extracted_data.get('p'), 'AM')
        self.assertEqual(extracted_data.get('M'), '28')
        self.assertEqual(extracted_data.get('S'), '23')

    

class TestNepaliDateTimeParser(unittest.TestCase):
    '''
    Tests nepali datetime parser.
    '''

    def test_normal_string_parse(self):
        parsed_datetime = nepalidatetime_parser.parse('2071-01-24')
        test_datetime = nepalidatetime(2071, 1, 24)
        self.assertEqual(parsed_datetime, test_datetime)

    def test_parse_failed(self):
        with self.assertRaises(InvalidDateTimeFormatException):
            parsed_datetime = nepalidatetime_parser.parse('')
