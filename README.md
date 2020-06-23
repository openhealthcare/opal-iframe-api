This is iframeapi - an [OPAL](https://github.com/openhealthcare/opal) plugin.

## ! Important Notice !

This plugin is no longer actively maintiained - as it depends on a version of django that is no longer supported by OPAL


This plugin allows you to embed records from an OPAL application in an external application.

For example, you could embed the most recent piece of Clinical Advice given about a patient, or
a patient's allergy information in an Iframe (or similar).

## Installation

Add to your INSTALLED_APPLICATIONS.

Run

    $python manage.py migrate iframeapi

## Usage

An API key can be combined the hospital number of a patient and an OPAL record name
in a get request and get a plain text result.

Good requests look like: 

    /iframeapi/?hospitalNumber=XXXXXXXXXXXX&key=XXXXXXXXXXXXXXX&record=XXXXXXXXXX    

All models must subclass PatientSubrecord or EpisodeSubrecord and a template for the result
needs to be put in iframe_templates with the model name in lowercase (examples included are iframe_templates/allergies, iframe_templates/antimicrobial).


### Limiting to the latest entry

You may also limit the display to the latest entry by adding the `latest` parameter e.g.

    /iframeapi/?hospitalNumber=XXXXXXXXXXXX&key=XXXXXXXXXXXXXXX&record=XXXXXXXXXX&latest=true
