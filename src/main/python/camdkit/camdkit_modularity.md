# Modularity and the one-file-per-concept idea

## pre-OpenTrackingIO `camdkit` structure

When Pierre first put it together, the structure of top-level `camdkit`
(as opposed to that of vendor-specific subdirectories) was:

### `framework.py`:
- defined a non-parameter type to hold the height and width of a rectangular
  area.
- defined parameter types in a very generic way, not specific to cameras at all
- defined `ParameterContainer` as the basis of any structure aggregating
  metadata implemented out of the defined parameter types

### `model.py`:
- identified semantically meaningful metadata that could be aggregated
  together to describe camera and lens state during some period of time
- defined a `Clip` as a collection of that semantically meaningful
  metadata, where some of the semantically meaningful metadata occurred
  just once and signified they were in force during the entire period
  covered by the `Clip` and some were in force only for a single frame's
  duration.

## current (`juren-trackerkit`) `camdkit` structure

### `framework.py`

The single non-parameter type present in the original `framework.py` file
has now become twenty-two types. What was once
- Dimensions
is now
- Sampling
- Dimensions
- Orientations
- Vector3
- Rotator3
- Transform
- Encoders
- RawEncoders
- ExposureFalloff
- Distortion
- PerspectiveShift
- CentreShift
- GlobalPosition
- Timestamp
- BaseEnum
- SampleTypeEnum
- SynchronizationSourceEnum
- SynchronizationOffsets
- TimingModeEnum
- TimecodeFormat
- Timecode
- Synchronization

As for the application-agnostic parameter types, they are interwoven with many
application-specific (that is, camera- and lens-metadata relevant) parameter
types. Originally, `framework.py` defined the following parameter types, all
subclasses of `Parameter`
- IntegerDimensionsParameter
- StringParameter
- UUIDURNParameter (could have been a subclass of StringParameter, really)
- StrictlyPositiveRationalParameter
- RationalParameter
- StrictlyPositiveIntegerParameter

The `juren-trackerkit` branch of `framework.py` adds the following types,
which are still fairly abstract and map to native data types:
- BooleanParameter
- ArrayParameter
- IntegerParameter
- NonNegativeIntegerParameter
- NonNegativeRealParameter
- EnumParameter
and one which is not abstract:
- TimestampParameter

### `model.py`

In the pre-`juren-trackerkit` branch of `camdkit`, the following
application-specific metadata were defined in `model.py` as subclasses
of parameter types defined in `framework.py`:

- IntegerDimensionsParameter:
  - ActiveSensorPhysicalDimensions
- StrictlyPositiveRationalParameter:
  - Duration
  - CaptureFPS
- StrictlyPositiveIntegerParameter
  - ISO
  - TStop
  - FStop
  - FocalLength
  - FocusPosition
  - AnamorphicSqueeze
- StringParameter
  - LensSerialNumber
  - LensMake
  - LensModel
  - LensFirmware
  - CameraSerialNumber
  - CameraMake
  - CameraModel
  - CameraFirmware
- RationalParameter
  - EntrancePupilPosition
- UUIDURNParameter
  - FDLLink
- Parameter (!!)
  - ShutterAngle

Clip is also defined in `model.py` and this is different than everything
else in that file. Everything before the definition of `Clip` defines a new
class that is a derivation of a parameter subclass. But `Clip` doesn't
define a direct or indirect subclass of `Parameter`; it defines a subclass
of `ParameterContainer`.

With the `juren-trackerkit` branch, the following additional classes
were derived from `model.py`-defined subclasses of `Parameter`:
- IntegerDimensionsParameter
  - ActiveSensorResolution
- StringParameter
  - LensDistortionModel
  - CameraId
  - DeviceSerialNumber
  - DeviceMake
  - DeviceModel
  - DeviceFirmware
  - Protocol
  - Status
  - Slate
  - Notes
- UUIDURNParameter
  - SampleId
- EnumParameter
  - SampleType
  - TimingMode
- BooleanParameter
  - Recording
- ArrayParameter
  - RelatedSamples
  - LensCustom
- Parameter (!!)
  - GlobalStagePosition
  - Transforms
  - TimingSynchronization
  - LensEncoders
  - LensRawEncoders
  - TimingTimecode
  - FOVScale
  - LensExposureFalloff
  - LensDistortion
    - LensUndistortion
  - LensCentreShift
  - LensPerspectiveShift
- TimestampParameter
  - TimingTimestamp
  - RecordedTimestamp
- NonNegativeIntegerParameter
  - TimingSequenceNumber
- StrictlyPositiveRationalParameter
  - TimingFrameRate
- StrictlyPositiveIntegerParameter
  - NominalFocalLength
- NonNegativeRealParameter
  - FocalLength
- RationalParameter
  - EntrancePupilDistance (was: EntrancePupilPosition)

There are 