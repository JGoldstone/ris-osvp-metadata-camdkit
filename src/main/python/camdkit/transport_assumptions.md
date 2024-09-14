### Periodic refresh of [relatively] static information

We think of things like "lens firmware" as being static. But
aren't we assuming some sort of context here? Namely, aren't we
temporally scoping that metadata to a single shot that would be recorded
as a single clip?

But is that the only way to play? Suppose that one shoots with camera A
and lens B all morning; during lunch, the representative you've been 
waiting for from the lens manufacturer shows up with a new firmware version
custom built just for you to fix the bad bug you found, and you install
that lens firmware build; and in the afternoon, you shoot with it.

If metadata is temporally scoped to clips, then the lens firmware version
could be considered static; but if the camera just generates metadata all
the time, whether or not it's recording, then (unless you turned off power
to the camera while crew ate lunch) it's dynamic.

We could give up distinguishing between static and dynamic metadata at the
structural level (which would also solve the problem of "what about
one-off or irregularly spaced metdata?") and receivers would just update
(or ignore) metadata as they came in.

The ability to recognize that expected updates from a transmitter hadn't
arrived, and that perhaps some sort of warning should be issued, could be
handled in several ways:
- there could be something in the JSON schema that specified a maximum
  between-samples interval
- metadata-consuming devices could configure their own maximum
  between-samples interval
- the sender could periodically send out JSON that contained pairs of
  metadata identifier and maximum between-samples interval 

### Assumptions of the transport layer

There may be multiple devices of the same type emitting similar metadata
on the same physical network. We can handle this in several ways:
- every metadata emitter gets a unique ID; every metadata group contains
  the unique ID of its emitter
- require the transport layer to provide a filtered view into what's going
  on in the underlying physical layer, e.g. every emitter is assigned or
  negotiates a multicast address that interested parties can monitor
- there might be other schemes people with more on-set time could name

### TimingMode and TimingModeEnum

It feels like the idea was that instead of being an EnumParameter, TimingMode
(which is defined twice in the file, by the way) would inherit from
TimingModeEnum and not from EnumParameter; but I could be missing something.

Anyway: I feel as if we have two possibilities: explicitly or implicitly
indicate whether the transport layer is responsible for providing
timestamps for metadata. That in turn has consequences:
- if we explicitly denote transport-vs-packet responsibility for timing:
  - what happens if the transport provides timing info AND either timecode
    or a PTP timestamp is found in the packet?
  - what happens if the transport is supposed to provide timing info, 
    and does not, and the packet contains neither timecode nor PTP timestamp?
  - what happens if the transport is supposed to provide timing info,
    and does not, and the packet contains either timecode or PTP timestamp?
  - the only easy case here is: transport provides timing info, no timing info
    found (neither timecode nor PTP timestamp) in the packet
- if we explicitly denote packet responsibility for testing, one can do a
  similar case analysis and again, there will be three erroneous
  cases and one easy and correct one.

If it's legitimate to have both timecode and timestamps in a file, then what
does TimingMode mean, exactly?

### What is being timestamped?

`TimingTimestamp` for capture and `RecordedTimestamp` for recording are
confusing because they aren't granular enough and they are named inconsistently:
- we don't have exact definitions for when capture happens (e.g. start of
  charge integration vs. start of readout
- we don't define what 'recording' means - is this end of readout, or is it
  the time an image or metadata buffer begins to be written to stable storage,
  or what?

### Transport-sensitive metadata: `Protocol`, `Status` and `Recording`

There are three metadata defined in `framework.py` that I find problematic
in that their scope is unclear to me.

The first is `protocol`, a string.
How is it used? If one needs this metadatum to interpret other metadata,
then that means nothing can be interpreted until the (let us say)
once-every-two-seconds group of relatively unchanging metadata is seen.
Different instances of the same device might be running different
firmware versions and support different protocols; should we require all
metadata communication via a particular channel (e.g. through a particular
IP multicast address) be of metadata sharing the same protocol version?

The second is `status`. Again, if we have multiple devices on-set (say a
giant gimbal holding up a piece of a sailing ship, rocking it back and
forth to simulate wave motion) and a camera in a gimbal, and they both
prodiuce and multicast status information out to any consumers that care,
how to avoid one consumer mis-interpreting one producer's output for
another? Saying the status is a 'free string' is just kicking the
namespace can down the road. See the discussion of extensibility
for some more thoughts on this.

The third is `recording`. This seems a specialization of `status` and as
such, all the considerations in the discussion on extensibility 
apply as well.

