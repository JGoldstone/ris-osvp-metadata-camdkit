#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Mo-Sys tracking data reader tests'''

import unittest
import uuid

from camdkit.framework import Vector3, Rotator3, Synchronization, SynchronizationSourceEnum, \
                              Timecode, TimecodeFormat, Encoders, Distortion, CentreShift
from camdkit.mosys import reader

class MoSysReaderTest(unittest.TestCase):
  
  def test_reader(self):
    clip = reader.to_clip("src/test/resources/mosys/A003_C001_01 15-03-47-01.f4", 20)

    # Test parameters against known values across multple frames
    self.assertEqual(clip.protocol[0], "OpenTrackIO_0.1.0")
    self.assertEqual(len(clip.packet_id[1]), len(uuid.uuid4().urn))
    self.assertEqual(clip.metadata_recording[2], True)
    self.assertEqual(clip.metadata_status[3], "Optical Good")
    self.assertEqual(clip.timing_frame_rate[4], 25.0)
    self.assertEqual(clip.timing_mode[5], "internal")
    self.assertEqual(clip.timing_sequence_number[6], 13)
    self.assertEqual(clip.timing_synchronization[7], Synchronization(25.0, True, SynchronizationSourceEnum.GENLOCK, None, True))
    self.assertEqual(clip.timing_timecode[8], Timecode(15,3,47,10,TimecodeFormat.TC_25))
    self.assertEqual(clip.transforms[9][0].translation, Vector3(x=-8.121, y=-185.368, z=119.806))
    self.assertEqual(clip.transforms[10][0].rotation, Rotator3(pan=-2.969, tilt=-28.03, roll=3.1))
    self.assertEqual(clip.lens_encoders[11], Encoders(focus=0.7643280029296875, zoom=0.0014190673828125))
    self.assertEqual(clip.lens_distortion[12], Distortion([0.15680991113185883, -0.0881580114364624]))
    self.assertEqual(clip.lens_centre_shift[13], CentreShift(-7.783590793609619, 6.896144866943359))
    self.assertAlmostEqual(clip.lens_focal_length[14], 22.35, 2)
    self.assertEqual(clip.lens_focus_position[15], 2313)
