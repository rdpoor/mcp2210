# NOTE: these are not unit tests in the strict sense: they require an MCP2210 to
# be present on the USB chain

import unittest
import hid
import mcp2210

class CustomAssertions:
    def assertUInt8(self, value):
        if value < 0 or value > 255:
            # b/c "value cannot be represented as an unsigned 8 bit integer"
            # is too verbose!
            raise AssertionError('Value ' + str(value) + ' is not an 8-bit int.')

class TestMCP2210(unittest.TestCase, CustomAssertions):

    def setUp(self):
        self.dev = None

    def tearDown(self):
        if (self.dev):
            self.dev.hid.close()

    def test_construct_positional(self):
        '''Verify the constructor accepts positional vid, pid arguments'''
        self.dev = mcp2210.MCP2210(0x04d8, 0x00de)
        self.assertIsInstance(self.dev, mcp2210.device.MCP2210)

    def test_construct_vid_pid_keyword(self):
        '''Verify the constructor accepts keyword vid, pid'''
        self.dev = mcp2210.MCP2210(vid=0x04d8, pid=0x00de)
        self.assertIsInstance(self.dev, mcp2210.device.MCP2210)

    def test_construct_default(self):
        '''Verify the constructor finds an MCP2210 with no arguments'''
        self.dev = mcp2210.MCP2210()
        self.assertIsInstance(self.dev, mcp2210.device.MCP2210)

    def test_construct_invalid_vid_pid(self):
        '''Verify the constructor fails with invalid vid, pid arguments'''
        with self.assertRaises(OSError):
            self.dev = mcp2210.MCP2210(vid=0xffff, pid=0xfff)

    def test_construct_path(self):
        '''Verify the constructor accepts a USB path'''
        descriptors = hid.enumerate(mcp2210.MCP2210.VID, mcp2210.MCP2210.PID)
        self.dev = mcp2210.MCP2210(path=descriptors[0]['path'])
        self.assertIsInstance(self.dev, mcp2210.device.MCP2210)

    # ==========================================================================
    # EEPROM operations

    def test_eeprom_read_single(self):
        self.dev = mcp2210.MCP2210()
        val = self.dev.eeprom[0]
        self.assertUInt8(val)

    def test_eeprom_read_slice(self):
        self.dev = mcp2210.MCP2210()
        vals = self.dev.eeprom[0:4]
        self.assertEqual(len(vals), 4)
        for val in vals:
            self.assertUInt8(val)

    # WARNING: overwrites values!
    def test_eeprom_write_single(self):
        self.dev = mcp2210.MCP2210()
        val = (self.dev.eeprom[0] + 1) & 0xff
        self.dev.eeprom[0] = val
        self.assertEqual(self.dev.eeprom[0], val)

    def test_eeprom_write_slice(self):
        self.dev = mcp2210.MCP2210()
        vals = [(v+1) & 0xff for v in self.dev.eeprom[0:4]]
        self.dev.eeprom[0:4] = vals
        self.assertEqual(vals, self.dev.eeprom[0:4])

    def test_eeprom_write_list(self):
        self.dev = mcp2210.MCP2210()
        vals = [11, 22, 33, 44]
        self.dev.eeprom = vals
        self.assertEqual(vals, self.dev.eeprom[0:4])

    def test_readme_examples(self):
        self.dev = mcp2210.MCP2210()
        self.dev.eeprom[10:14] = [2, 4, 8, 16]
        self.assertEqual(self.dev.eeprom[10:14], [2, 4, 8, 16])
        self.assertEqual(self.dev.eeprom[12], 8)
