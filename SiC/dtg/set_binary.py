import pyvisa
import numpy as np
rm = pyvisa.ResourceManager()
dtg = rm.open_resource('TCPIP0::129.69.46.221::inst0::INSTR')

def _channel_write_binary(channel, data):
        c = channel
        max_blocksize = 8 * 800
        dlen = len(data)
        written = 0
        start = 0

        # when there is more than 1MB of data to transfer, split it up
        while dlen >= max_blocksize - 8:
            end = start + max_blocksize
            bytestr = np.packbits(np.fliplr(np.reshape(data[start:end], (-1, 8))))
            print(channel, '->', c, 'start', start, 'end', end, 'len', dlen, 'packed', len(bytestr))
            #print(bytestr)
            dtg.write_binary_values(
                'PGEN{0}:CH{1}:BDATA {2},{3},'.format(c[0], c[1], start, end - start),
                bytestr,
                datatype='B'
            )
            print(dtg.query('*OPC?'))
            written += end - start
            dlen -= end - start
            start = end

        end = start + dlen
        if dlen > 0:
            to_pad = 8 - dlen % 8 if dlen % 8 != 0 else 0

            padded_bytes = np.packbits(
                np.fliplr(
                    np.reshape(
                        np.pad(data[start:end], (0, to_pad), 'constant'),
                        (-1, 8)
                    )
                )
            )
            print('PDB\n', padded_bytes, '\n')
            print(channel, '-->', c, 'start', start, 'end', end,
                  'len', dlen, 'padded', len(padded_bytes))
            dtg.write_binary_values(
                'PGEN{0}:CH{1}:BDATA {2},{3},'.format(c[0], c[1], start, end - start),
                padded_bytes,
                datatype='B'
            )
            print(dtg.query('*OPC?'))
            written += end - start
        return written
_channel_write_binary(['A', 2], [1,1,1,1,1,1])