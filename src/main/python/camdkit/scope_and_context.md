


# camdkit Design questions

## TL:DR;, or, the elevator pitch for `OpenLensIO` and `OpenTrackingIO`

The group that presented the `camdkit` model last year (?) at SMPTE is
extending it to add metadata for real-world lenses and for common virtual
production use cases (for example, gimbal mounted cameras on cranes).
This is being done in sub-projects named `OpenLensIO` and `OpenTrackingIO`,
respectively. The group's goal is to come up with something usable by
all VP components, including "pure software" ones like Unreal Engine, at
a level that could match or exceed that of proprietary systems like the
MoSys F4 protocol. (As evidence of this, the creator of F4 is leading the
`OpenTrackingIO` group.)

## Assumed scope of `camdkit` vs `OpenLensIO` vs `OpenTrackingIO`

`camdkit` has a README describing the project as containing a toolkit for 
making consistent the camera and lens metadata from various camera vendors.
(We did not concern ourselves with obtaining lens metadata without first
passing through a camera and being recorded into something our tools read.)
The metadata making up `camdkit` have an associated JSON representation
suitable for storage and transport.

We have made no assertions regarding
such storage and transport other than that it is 100% reliable; or perhaps
more accurately we have made no provision for detecting or correcting 
errors in storage and transport (ECC schemes, retransmission, etc.)

`OpenLensIO` is an in-progress specification of an extension to `camdkit`
such that extended lens metadata, suitable for characterizing the image 
distortion and image vignetting of a particular lens when mounted on a
particular camera. (More research might result in additional metadata and/or
reorganization of existing metadata that could characterize a lens 
independent of any associated camera body, but we have not done such and
currently consider such research out of scope.)

The metadata present in `OpenLensIO`, like those in `camdkit`, have a JSON
representation.

`OpenTrackingIO` is an in-progress specification of an extension to the
`camdkit` model, describing the semantics and representations of interacting
devices on set — from gimbal-mounted cameras on mobile cranes, to systems
that capture an actor's performance as a set of moving points.

Notably `OpenTrackingIO` discussions consider how metadata would be grouped
together and how they would be transmitted. Like `camdkit1` and `OpenLensIO`
before it, `OpenTrackingIO` provides a JSON representation for anything it
defines. Beyond that, the group is looking at:
- possible reductions in bandwidth via a binary representation (e.g.
  a binary JSON, protobuf, or some other proven scheme)
- nesting metadata to represent a transform stack, e.g. a camera inside
  a gimbal mount on a crane on a track on board a ship as the earth moves
  around the sun -- OK, not the ship and the earth, but still
- design for unreliable transport (damaged or dropped metadata)
- transmission / reception models that allow for dynamic entry of devices
  into an ongoing information flow, either as metadata creators or 
  consumers.
- enhanced JSON through schema that will provide a machine-readable
  assertion of data types, value ranges and associated SI units (if any)

