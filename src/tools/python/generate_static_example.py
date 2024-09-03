#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''CLI tool to generate and validate JSON for an example static data frame'''

import json
import uuid

from camdkit.framework import Vector3, Rotator3, Transform
from camdkit.model import *

def main():
  clip = Clip()
  clip.sample_id = (uuid.uuid4().urn,)
  clip.sample_type = ("static",)
  clip.protocol = ("OpenTrackIO_0.1.0",)
  clip.camera_id = "A"
  clip.lens_make = "Canon"
  clip.lens_model = "HJ14"
  clip.lens_nominal_focal_length = 14
  clip.lens_distortion_model = "OpenLensIO_0.1.0"
  clip.device_model = "StarTracker Max"
  clip.device_firmware = "3289"
  clip.device_make = "Mo-Sys"
  clip.device_serial_number = "1234567890A"
  clip.active_sensor_physical_dimensions = Dimensions(width=36000,height=24000)
  clip.active_sensor_resolution = Dimensions(width=3840,height=2160)
  clip.anamorphic_squeeze = 1

  clip_json = clip.validate()

  print(json.dumps(clip_json, indent=2))

if __name__ == "__main__":
  main()