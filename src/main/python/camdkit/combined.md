# Aggregate comments

The comments that follow have been building up for a while. It be unconscionable to monopolize a weekly meeting with them, but you wouldn't have the chance to scroll back, to search, etc. when you comment.

I say this in a final section but will put it up front here: I want to implement the proposed changes in a way that (a) shows the changes can be made while still preserving what we have, (b) doesn't give James a huge amount more creative work and (c) can be done fairly quickly. I should note that with ARRI having laid me off, and my contemplating taking a gap year to work on open-source projects, I have a lot more time.   

I've listened to the recording of the meeting I missed last week and want to congratulate the group on what was achieved. That said, I have a lot of  unresolved issues. The following tries to group some thoughts on:
- unspoken scope and context assumptions
- naming
- extensibility
- suggested refactor #1 (closer to original camdkit spirit)

## unspoken scope and context assumptions

Listening to the recording of the last discussion it seems like this is going on.

There is some system of data transport.

It passes aggregations of metadata in what we have been calling a packet. All of the information in the packet comes from the same metadata producer, i.e., there are no packets where the first part of the packet is written by one device A, and the second by another device B. You could have yet a third device C capture first the packet from A, and then theh packet from B, and glue them together and send that as an integral whole -- but then it would be a single packet authored completely by device C.

There is some way of uniquely identifying packet creators. If a camera has a built-in UUID metadatum, then packets concerning the camera could use that; if a camera did not, but it had a recognizable make, model and serial number, you could join those with hyphens, convert spaces to underscores, etc. to get a UUID. Somehow, you get one.

Why? Because of the case Ramiro first brought up, of two cameras, two lenses, two tracking systems. You either create what once would have been called a virtual circuit, a transport system instance dedicated solely the creator of metadata packets, and then you don't need to transport the packet creator ID in each packet; or you put a packet  rceator ID in each packet.

The minimum packet would carry only identifying metadata regarding the sender. The maximum ... well, there's no packet-structural reason that there would be a maximum, but (a) the transport system probably imposes one, e.g. max frame size and (b) logistically you don't want to slow your network down by transmitting a ton of unneeded metadata.

I vote for no `TimingMode` parameter being defined and sent (vs. the two identical definitions of it now in `model.py`) and the packet either containing rarely-changing metadata, or not.

Pierre's point re: the transport mechanism allowing one to decide whether to skip the packet is one I like very much, but I don't know things like how RTP works (or how much RTP is used on set). If it can be done then all of the discussion two meetings ago about how long it takes to skip over a JSON structure you know you don't care about ... would now be moot.

So coming back to data transport:
- it hands over packets
- it can indicate packet boundaries if found
- it may have a way to indicate that what it is handing the consumer might not be from a start-packet boundary or end-packet boundary
- it may or may not have the ability to carry a 'repeated stuff that rarely changes' flag
- it isn't being tasked with identifying what kind of a thing the creator of a packet is
- the above assumptions plus whatever else we can say about the data transport layer should be in some part of the API documentation. 

Documentation that is nothing but copied-out or rearranged argument lists or attribute lists will not be compelling if unaccompanied by a high-level overview of our motivations.

## naming

When a metadatum is semantically identical with what is in OpenEXR (from which the USD camera project takes as many definitions as possible), it should have the same name.

In what is now called `framework.py`:

When there is no name already, all names should be singular. E.g. we have 'Orientations' with two members as a plural, and 'Dimension' with two members as a singular. I am advocating
- `Orientations` -> `Orientation`
- `Encoders` -> `FIZEncoder`
- `RawEncoders` -> `RawFizEncoder` or `FizRawEncoder`
- `SynchronizationOffsets` -> `SynchronizationOffset`

Note the change that allows for later non-FIZ encoders and even the possible introduction of an abstract encoder base class.

`Orientations` we use to indicate FOV but it's a general term (that I often have heard applied to a collection of Euler angles). That I don't have a specific replacement at the ready is not stopping me here from objecting to the name.

More pedantically perhaps:
- `Tranformation` to be parallel to `Distortion`
- `Vignetting` to be more specific than `ExposureFalloff` unless falloff is a term of art *only* used for vignetting. If we have a very specific concept we should use a very specific word.

and in `model.py`:

timing_sample_timestamp` and `timing_recorded_timestamp` are inconsistent. Consistent possibilities:
  - `SamplingTimestamp` and `RecordingTimestamp`
  - `SampledTimestamp` amd `RecordedTimestamp`
  - `TimeSampled` and `TimeRecorded`
  - `SampledAt` and `RecordedAt`

`transforms` to `transformChain`; the current `transforms` is plural but all other clip attributes are singular.	 

This will probably be controversial but I am not a fan of 'Device-' or 'device_'-prefixed names because ... cameras are devices just as much as tracking systems are. Having `camera_` and `lens_` and then `_device` is a sudden shift in level of specificity. If by `device` you mean 'tracking system' then say so, both to make it clearer for users of the API, and so that if you start introducing other non-camera, non-lens things (like a recorder), you don't have to introduce something hideous like `device2_`, or alternatively, `recorder_` in which case tracking systems' names really stick out like a sore thumb.

I don't see a need to have some abstract `Device` class, at least, not at this point.

## extensibility

Either every packet should be required to contain a metadatum identifying its camdkit version — I am assuming we just have a single version, since AFAIK we are not talking about separate releases for "traditional camdkit", "OpenLensIO" and "OpenTrackingIO" components — or it should be a requirement of *all* transport systems that they identify the camdkit version.

Vagueness in the form of 'free strings' is an opportunity for interoperability islands, where vendors adopt unpublished out-of-camdkit conventions to talk amongst their own products and to selected others. I would relegate free strings to things like names of places and people.

I think two ideas have been advanced for reducing name collisions:
- Joseph's Java-style reverse domain names. This was more a thought experiment than an actual proposal
- Ritchie's quickly-allocated-by-SMPTE vendor prefixes alongside a CamelCasePrefix or snake_case_prefix_ convention

Steve may have advanced something in the last meeting and I may have missed the specifics of it, but I believe it was something like Ritchie's proposal but without the central naming authority.

## a suggested refactor, back on the main branch:

`framework.py` mostly contains three things: a base `Parameter` class, parameter subclasses mapped to primitive data types or to restricted ranges thereof, and a class that serves as the basis for parameter (not parameter type) containers. `model.py` identifies semantically meaningful metadata for cameras and lenses, building those metadata as subclasses of the restricted-range-data-type-specific subclasses of `Parameter`.

The patch to merge in OpenTrackingIO development does not create any new files; it inserts them into what's already there. And this feels wrong to me. In the original `framework.py` the word "mostly" above was there to cover `Dimensions`, a lone higher-level-semantics type. In the OpenTrackingIO branch, that lone type has become twenty-two higher-level-semantics types. And in the origiunal `model.py`, `ShutterAngle` was (for reasons not obvious to me) the only metadatum directly subclassed from `Parameter`; in the OpenTrackerIO `model.py` there are twelve.

Note that I am not suggesting any change in this section in the JSON representation of the metadata we are defining (though changes may have been suggested in earlier sections). I am talking about reworking the Python files for better readability.

I would suggest putting `ParameterContainer` and `Clip` in `container.py`. And there should be exposition (not just in the header files BTW) on clips as multi-sample aggregates, vs. only a single sample in a single packet.

`framework.py` would be split into one file containing `Parameter` subclasses that mapped fairly directly to constrained ranges of primitive types, or to non-application-specific struct-like types (the equivalent of `Imath`'s Vector types, for example). To scope the latter, a good thing to look at would be how many of the metadata that in OpenTrackIO currently inherit directly from `Parameter` could inherit from structs of particular constrained primitive types. Again referring to `Imath`, look at the way V3i, V3f, V3h and so on are aliases for C++ template specializations of an underlying type. If I had actually prototyped such intermediate types I am pretty sure I would have a candidate names. `primitive_types.py`, `compound_base_types.py` and `application_types.py` perhaps.

I don't have a concrete proposal for how `model.py` should be split up; that is something that probably depends on whether we refactor to get a camera to be recognized as a type of device, as discussed in the section on naming above.

## talking about the above, and doing something

If there's a way to submit a PR for review and possible merging into an existing PR, I would like to understand how that works.

Should such a possibility exist, the only decent thing for me to do is to back up the above with code changes.

If it's not possible to basically do a PR on a PR, then I can make the changes off of a fork from James' branch, and submit it as an alternative PR.


