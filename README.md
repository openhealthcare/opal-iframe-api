This is iframeapi - an [OPAL](https://github.com/openhealthcare/opal) plugin.

This plugin allows people to create api keys (via the admin).

This key can then be combined the hospital number of a patient and an opal column name
in a get request and get a plain text result.

All models must subclass PatientSubrecord or EpisodeSubrecord and a template for the result
needs to be put in iframe_templates with the model name in lowercase (examples included are iframe_templates/allergies, iframe_templates/antimicrobial).

If you're subclassing EpisodeSubrecord you can use a mostRecent argument to get the latest
episode subrecord.
