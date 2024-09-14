### Extensibility

How do we denote, for a particular metadatum, the camdkit revision to
which it belongs? Should emitters send out the version they are using
once a second, say, and collectors of metadata hold off on interpreting
it until they see that version number?

Where do we see metadata today where there is disagreement on semantics?
We will reduce uptake of our work if someone has a different distortion
model and `camdkit/OpenLensIO/OpenTrackingIO` has no accomodation for it.
This could be as simple as interposing a layer under lensDistortion that
was the JSON equivalent of a Python dict keyed by distortion model name.
To me both `Distortion` and `Vignetting` (neé `ExposureFalloff`) are
candidates for this treatment. This would let us carry both agreed-on
distortion metadata (e.g. Brown-Conradi) and proprietary distortion 
metadata. 3DE has its own model, for example. Moreover I am pretty sure
there are competing distortion models for zooms and also competing
distortion models for anamorphics.

Deliberately vague metadata like `status`, with its content being termed
a 'free string', is basically dodging the fundamental problem: there is
no namespace system in the `camdkit/OpenLensIO/OpenTrackingIO` architecture
and so semantic collisions are just punted up to the application level.
This is not a good look.

One way out is to make individual 'status' metadata for each thing that
could have a status, e.g. `opticalTrackerStatus`. This doesn't scale well
when there are multiple instances of a system, e.g. let's say you had
two different witness cameras on the set. Without some sort of ID for the
originating device, `witnessCameraStatus` metadata are ambiguous.
