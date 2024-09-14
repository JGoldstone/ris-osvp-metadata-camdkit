## Naming

## `framework.py`

### Singular or plural?

It's not clear to me when we call something by a plural name or a singular
one. E.g. we have what are mis-termed 'Encoders' (see below) with three
members, and we have 'Distortion' with two members. I fail to see a pattern.

My choice is to name them all with singular forms, but with `Dimension`
turned into `RectangularArea`. Others:
- `Orientations` -> `Orientation`
- `Encoders` -> `FIZEncoder`
- `RawEncoders` -> `RawFizEncoder` or `FizRawEncoder`
- `SynchronizationOffsets` -> `SynchronizationOffset`

### `Orientations` is too general

The only places this gets used are in `lens_exposure_falloff` and in 
`lens_fov_scale`. And something seems dodgy with `lens_exposure_falloff`
because that would seem to have three components, but `Orientations`
only has two.

### `Transformation` not `Transform`

We use `Distortion`, not `Distort`; for parallel construction we should
use `Transformation` instead of `Transform`.

### `Encoders` and `RawEncoders`

These are not generalized encoders, and should not squat on the more
general name. Call them FizEncoders (actually, call one a FizEncoder),
and then if we ever need to come up with a base class for all encoders,
Encoder becomes available.

Also, the docstring comment on `RawEncoders` is wrong; it's not 
normalized.

### lower-case the attribute names in PerspectiveShift

There is no good reason to violate PEP8 here.

### `ExposureFalloff`

Pedantically, there are other ways to make exposure fall off, e.g. put
an ND filter in front of the lens. Are we limiting ourself to models
describing vignetting, and if so, can we just call this `Vignetting`?

### `Slate`

Is there enough commonality on real world slates that we could impose
some structure here? Scene and Take come to mind, and Roll. I could 
use surveys I have done in the past to see what is common across ARRI,
RED, Sony and BMD, as far as data found on slates go.

## `model.py`

### `timing_mode`

`mode` is a terrible canonical name for something that's indicating whether
the transport provides timing info and/or whether the packet explicitly 
contains timing info. What if there's another choice to be made about
timing information that also can take one of a few identified values?

If it makes sense to carry this info (vs. assuming it's the transport's
responsibility if neither timecode nor timestamps are in the packet) then
we could give it a canonical name of `from_transport` and make it a bool,
which would flatten into `timing_from_transport` in the streamed JSON.

### `timing_sample_timestamp` and `timing_recorded_timestamp`

- the two are grammatically inconsistent. Any of these would be better paired:
  - `SamplingTimestamp` and `RecordingTimestamp`
  - `SampledTimestamp` amd `RecordedTimestamp`
  - `TimeSampled` and `TimeRecorded`
  - `SampledAt` and `RecordedAt`

but again see also the discussion about what is being timestamped over in 
transport_assumptions.md

### `transforms` is plural, but other clip attributes are singular

Suggestion: rename `Transforms` to `TransformChain`




