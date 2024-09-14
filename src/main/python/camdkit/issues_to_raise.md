
## `framework.py`

### Parameter inheritance relationships are inconsistent
The following concrete classes inherit directly from Parameter:
- IntegerDimensionsParameter
- BooleanParameter
- StringParameter
- ArrayParameter
- UUIDURNParameter
- StrictlyPositiveRationalParameter
- RationalParameter
- IntegerParameter
- NonNegativeRealParameter
- TimestampParameter

The following concrete classes inherit directly from IntegerParameter:
- NonNegativeIntegerParameter
- StrictlyPositiveIntegerParameter

The following concrete class inherits directly from StringParameter:
- EnumParameter

## `model.py`

### Why does EnumParameter 

Why aren't the enum values just given as an argument to an `__init__` argument
to the EnumParemeter constructor, instead of referencing a separate, presumably
Enum-based class via a dynamic mechanism? Is this in support of run-time
extensibility?

### Why doesn't Parameter have required parameters?

### `model.py`
To be in a container a Parameter must have canonical_name and
sampling parameters or a TypeError (!!!) is raised. This seems like
an oppportunity to put those attributes in a base class, and 
Parameter seems like a good one. So why wasn't that done?

The parameters in `model.py` are different than those in `framework.py`;
some number of them seem to have canonical name and sampling.

Some number of them also contain 'section' and 'units' attributes.

The most common combination at the top of the file is to have
- `canonical_name`
- `sampling`
- `units`
- `section`

This combination is found in:
- ActiveSensorPhysicalDimensions
- CaptureFPS
- ISO
- LensSerialNumber
- LensMake
- LensModel
- LensFirmware - suggest it be lens_firmware_version as per canonical_name
- LensDistortionModel
- CameraSerialNumber
- CameraMake
- CameraModel
- CameraFirmware - suggest it be camera_firmware_version as per canonical_name
- CameraId [does this map to OpenEXR's / ACES's "index"?]
- DeviceSerialNumber
- DeviceMake
- DeviceModel
- DeviceFirmware- suggest it be device_firmware_version as per canonical_name
- Status

The following lack a '`section`' attribute:
- Duration
- PacketID
- Protocol


## `model.py`

`TimingSequenceNumber` is not defined in the camera and lens table repository.
It seems analogous to the ACES Container's `imageCounter` attribute, but
more general, _i.e._ not just image data.

`TimingFrameRate` is unclear as to whether this is the rate at which frames
are captured, or the rate at which they are intended to be played back. The
ACES Container distinguishes between the two via `captureRate` and
`framesPerSecond`. If I recall correctly, the reason the latter is not
`playbackRate` is historical -- the OpenEXR reference implementation used
`framesPerSecond` (this could be verified with `git blame`, as OpenEXR's
history has been preserved in full)

Anyway I would recommend carrying both `captureRate` and `playbackRate` as
Fraction attributes.

`TimingTimecode` is currently an amalgam of three things: HH:MM:SS:FF timecode,
a rate of some type relating to frames, probably playback rate, and a signifier
that drop-rate timecode is in use. I would recommend the following:
- `timecode` as a tuple of four integers with appropriate value constraints
- `captureRate` and `playbackRate`, each carried as a `Fraction`
- `dropFrame` as a bool

`LensExposureFalloff` I would rename to `Vignetting`. Do all the major players
(Zeiss, Cooke Optics, RED, ARRI, 3DE, Foundry, _&c_) agree on a three-parameter
model? If not, then either rename to something indicating the three-parameter
model, or add another level where multiple models could co-exist.

For `LensDistortion`, see comments on `LensExposureFalloff` regarding
accommodating multiple models.

## Implementation questions

## `framework.py`

The four static methods on `Parameter`, which all raise
`NotImplementedError`, make me think of abstract base classes. Can't we
have `Parameter` actually be an abstract base class with `validate`,
`to_json`, `from_json` and `make_json_schema` abstract methods?

Is there a reason we are implementing rational numbers when the standard
library has Fraction?

Places where open-source libraries provide mechanism we implement today:
- Pydantic instead of our jsonification and verification

## `model.py`:

Why is `TimingMode` defined twice, identically except for the comment formatting?


This seems like it should be calling a Transform to_json method repeatedly


## Miscellaneous

## `framework.py`

## `model.py`

A comment at the top of `model.py` beyond "Data Model" would be good.
In particular, what's up with 'sections'? Pierre's comment about taking
'lens' out of the name makes me curious as to how they are used at runtime.



PEP 8:
- docstrings with three double quotes at each end
  - _but do we have an agreed-on docstring convention, e.g. NumPy's?_

Unclear analogy to real world:
- Sampling describes how often data is recorded to capture some phenomenon,
  intention, etc. If we have STATIC and REGULAR I would argue for there to
  also be an IRREGULAR. The current state of affairs where we have only
  STATIC and REGULAR has led parts of the API to use REGULAR to mean dynamic,
  where the really useful thing would be to indicate whether something was
  constant or could change.

  One possible way out would be to have two enums, one describing SCOPE of a
  metadatum, with values CLIP or SAMPLE, and one describing the sampling of
  a metadatum, with values REGULAR or IRREGULAR. It would be invalid to have
  the second enum present when the first is CLIP. 

- For the Transform geometry chains, is it the case that the name serves as
  an ID and the parent is a reference to it? In such a case, how are
  namespace collisions avoided when multiple vendors are contributing
  data to the stream? We don't have to design a mechanism to prevent
  namespace collisions; it would suffice to just note their possibility
  and leave their avoidance to application-level. 
 
- In the real world, I hear people discuss orientations such as vertical,
  horizontal, diagonal, skewed, etc. but never assign them numeric values.
  Can we come up with a better name? 

- Use of default values vs. requiring values:
  - Do we want to make Vector3 be an abstract class and have Location and
    Translation be concrete subclasses, or maybe, this is a case where we
    use the type system to make an entirely new tupe?
  - Are there cases where we would need to distinguish between values not
    having been specified by the instance creator vs. values being the
    default? If not I would prefer to specify no-op defaults or if not
    no-op, then something that is Falsey, e.g. translation defaults of 0,
    rotation defaults of 0, scale defaults of 1.
  
- Encoders should be an ABC named EncoderValues
  - FIZEncoderValues should subclass EncoderValues
