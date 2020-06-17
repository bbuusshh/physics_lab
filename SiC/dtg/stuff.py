def pulser_on(self):
    """ Switches the pulsing device on.

    @return int: error code (0:OK, -1:error)
    """
    self.dtg.write('OUTP:STAT:ALL ON;*WAI')
    self.dtg.write('TBAS:RUN ON')
    state = 0 if int(self.dtg.query('TBAS:RUN?')) == 1 else -1
    return state

def pulser_off(self):
    """ Switches the pulsing device off.

    @return int: error code (0:OK, -1:error)
    """
    self.dtg.write('OUTP:STAT:ALL OFF;*WAI')
    self.dtg.write('TBAS:RUN OFF')
    state = 0 if int(self.dtg.query('TBAS:RUN?')) == 0 else -1
    return state

def clear_all(self):
    """ Clears all loaded waveforms from the pulse generators RAM/workspace.

    @return int: error code (0:OK, -1:error)
    """
    self.dtg.write('GROUP:DEL:ALL;*WAI')
    self.dtg.write('BLOC:DEL:ALL;*WAI')
    self.current_loaded_assets = {}
    return 0
def get_sample_rate(self):
    """ Get the sample rate of the pulse generator hardware

    @return float: The current sample rate of the device (in Hz)

    Do not return a saved sample rate from an attribute, but instead retrieve the current
    sample rate directly from the device.
    """
    return float(self.dtg.query('TBAS:FREQ?'))

  def set_sample_rate(self, sample_rate):
        """ Set the sample rate of the pulse generator hardware.

        @param float sample_rate: The sampling rate to be set (in Hz)

        @return float: the sample rate returned from the device (in Hz).

        Note: After setting the sampling rate of the device, use the actually set return value for
              further processing.
        """
        self.dtg.write('TBAS:FREQ {0:e}'.format(sample_rate))
        return self.get_sample_rate()



 def get_digital_level(self, low=None, high=None):
        """ Retrieve the digital low and high level of the provided/all channels.

        @param list low: optional, if the low value (in Volt) of a specific channel is desired.
        @param list high: optional, if the high value (in Volt) of a specific channel is desired.

        @return: (dict, dict): tuple of two dicts, with keys being the channel descriptor strings
                               (i.e. 'd_ch1', 'd_ch2') and items being the values for those
                               channels. Both low and high value of a channel is denoted in volts.

        Note: Do not return a saved low and/or high value but instead retrieve
              the current low and/or high value directly from the device.
        """
        if low is None:
            low = self.get_constraints().activation_config['all']
        if high is None:
            high = self.get_constraints().activation_config['all']

        ch_low = {
            chan:
                float(
                    self.dtg.query('PGEN{0}:CH{1}:LOW?'.format(
                        *(self.ch_map[chan])
                    ))
                )
            for chan in low
        }

        ch_high = {
            chan:
                float(
                    self.dtg.query('PGEN{0}:CH{1}:HIGH?'.format(
                        *(self.ch_map[chan])
                    ))
                )
            for chan in high
        }

        return ch_high, ch_low

    def set_digital_level(self, low=None, high=None):
        """ Set low and/or high value of the provided digital channel.

        @param dict low: dictionary, with key being the channel descriptor string
                         (i.e. 'd_ch1', 'd_ch2') and items being the low values (in volt) for the
                         desired channel.
        @param dict high: dictionary, with key being the channel descriptor string
                          (i.e. 'd_ch1', 'd_ch2') and items being the high values (in volt) for the
                          desired channel.

        @return (dict, dict): tuple of two dicts where first dict denotes the current low value and
                              the second dict the high value for ALL digital channels.
                              Keys are the channel descriptor strings (i.e. 'd_ch1', 'd_ch2')

        If nothing is passed then the command will return the current voltage levels.

        Note: After setting the high and/or low values of the device, use the actual set return
              values for further processing.
        """
        if low is None:
            low = {}
        if high is None:
            high = {}

        for chan, level in low.items():
            gen, gen_ch = self.ch_map[chan]
            self.dtg.write('PGEN{0}:CH{1}:LOW {2}'.format(gen, gen_ch, level))

        for chan, level in high.items():
            gen, gen_ch = self.ch_map[chan]
            self.dtg.write('PGEN{0}:CH{1}:HIGH {2}'.format(gen, gen_ch, level))

        return self.get_digital_level()

  def write_sequence(self, name, sequence_parameters):
        """
        Write a new sequence on the device memory.

        @param name: str, the name of the waveform to be created/append to
        @param sequence_parameters: dict, dictionary containing the parameters for a sequence

        @return: int, number of sequence steps written (-1 indicates failed process)
        """
        num_steps = len(sequence_parameters)

        # Check if sequence already exists and delete if necessary.
        #if sequence_name in self._get_sequence_names_memory():
        #    self.dtg.write('BLOC:DEL "{0}"'.format(sequence_name))
        self._set_sequence_length(num_steps)
        for line_nr, (wfms, params) in enumerate(sequence_parameters):
            print(line_nr, params)
            go_to = '' if params['go_to'] <= 0 else params['go_to']
            jump_to = '' if params['event_jump_to'] <= 0 else params['event_jump_to']
            reps = 0 if params['repetitions'] <= 0 else params['repetitions']
            self._set_sequence_line(
                line_nr,
                '{0}'.format(line_nr + 1),
                0,
                params['name'][0].rsplit('.')[0],
                reps,
                jump_to,
                go_to
            )

        # Wait for everything to complete
        while int(self.dtg.query('*OPC?')) != 1:
            time.sleep(0.2)

        self.sequence_names.add(name)
        return 0
    def _set_sequence_line(self, line_nr, label, trigger, block, repeat, jump, goto):
        print(line_nr, label, trigger, block, repeat, jump, goto)
        self.dtg.write('SEQ:DATA {0}, "{1}", {2}, "{3}", {4}, "{5}", "{6}"'.format(
            line_nr, label, trigger, block, repeat, jump, goto
        ))

    def _get_sequence_length(self):
        return int(self.dtg.query('SEQ:LENG?'))

    def _set_sequence_length(self, length):
        self.dtg.write('SEQ:LENG {0}'.format(length))

    def _get_sequencer_mode(self):
        return self.dtg.query('TBAS:SMODE?')



def _is_output_on(self):
        return int(self.dtg.query('TBAS:RUN?')) == 1

def _block_length(self, name):
    return int(self.dtg.query('BLOC:LENG? "{0}"'.format(name)))

    def _is_output_on(self):
        return int(self.dtg.query('TBAS:RUN?')) == 1

    def _block_length(self, name):
        return int(self.dtg.query('BLOC:LENG? "{0}"'.format(name)))

    def _block_exists(self, name):
        return self._block_length(name) != -1

    def _block_delete(self, name):
        self.dtg.write('BLOC:DEL "{0}"'.format(name))

    def _block_new(self, name, length):
        if self._block_exists(name):
            self._block_delete(name)

        self.dtg.write('BLOC:NEW "{0}", {1}'.format(name, length))
        self.dtg.query('*OPC?')
        self.dtg.write('BLOC:SEL "{0}"'.format(name))
        self.dtg.query('*OPC?')

    def _block_write(self, name, digital_samples):
        written = []
        self.dtg.write('BLOC:SEL "{0}"'.format(name))

        for ch, data in sorted(digital_samples.items()):
            written.append(self._channel_write_binary(ch, data))

        self.dtg.query('*OPC?')
        return written

    def _channel_write(self, channel, data):
        c = self.ch_map[channel]
        max_blocksize = 500
        dlen = len(data)
        written = 0
        start = 0

        # when there is more than 1MB of data to transfer, split it up
        print('Starting chunked transfer')
        while dlen >= max_blocksize:
            end = start + max_blocksize
            datstr = ''.join(map(lambda x: str(int(x)), data[start:end]))
            print(channel, 'loop', dlen, len(datstr))
            self.dtg.write('PGEN{0}:CH{1}:DATA {2},{3},"{4}"'.format(
                c[0], c[1], start, end - start, datstr))
            self.dtg.query('*OPC?')
            written += end - start
            dlen -= end - start
            start = end

        end = start + dlen
        if dlen > 0:
            datstr = ''.join(map(lambda x: str(int(x)), data[start:end]))
            print(channel, 'last', len(datstr))
            self.dtg.write(
                'PGEN{0}:CH{1}:DATA {2},{3},"{4}"'.format(
                    c[0], c[1], start, end - start, datstr)
            )
            self.dtg.query('*OPC?')
            written += end - start
        return written

    def _channel_write_binary(self, channel, data):
        c = self.ch_map[channel]
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
            self.dtg.write_binary_values(
                'PGEN{0}:CH{1}:BDATA {2},{3},'.format(c[0], c[1], start, end - start),
                bytestr,
                datatype='B'
            )
            print(self.dtg.query('*OPC?'))
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
            #print(padded_bytes)
            print(channel, '-->', c, 'start', start, 'end', end,
                  'len', dlen, 'padded', len(padded_bytes))
            self.dtg.write_binary_values(
                'PGEN{0}:CH{1}:BDATA {2},{3},'.format(c[0], c[1], start, end - start),
                padded_bytes,
                datatype='B'
            )
            print(self.dtg.query('*OPC?'))
            written += end - start
        return written

    def _get_sequence_line(self, line_nr):
        fields = self.dtg.query('SEQ:DATA? {0}'.format(line_nr)).split(', ')
        print(fields)
        label, trigger, block, repeat, jump, goto = fields
        return (
            label.strip('"'),
            int(trigger),
            block.strip('"'),
            int(repeat),
            jump.strip('"'),
            goto.strip('"')
        )

    def _set_sequence_line(self, line_nr, label, trigger, block, repeat, jump, goto):
        print(line_nr, label, trigger, block, repeat, jump, goto)
        self.dtg.write('SEQ:DATA {0}, "{1}", {2}, "{3}", {4}, "{5}", "{6}"'.format(
            line_nr, label, trigger, block, repeat, jump, goto
        ))

    def _get_sequence_length(self):
        return int(self.dtg.query('SEQ:LENG?'))

    def _set_sequence_length(self, length):
        self.dtg.write('SEQ:LENG {0}'.format(length))

    def _get_sequencer_mode(self):
        return self.dtg.query('TBAS:SMODE?')
