# huskDeadline

## (huskDeadline)

* Description: Karma/Husk Deadline Submitter for Houdini
* Copyright: AXISFX LTD
* Author: Ewan Davidson
* Email: ewan@axisfx.design
* Release Date: 11.03.2023
* Current Version: 1.0.0

## Installation

* Append to $HOUDINI_PATH

## Dependencies

* Thinkbox Deadline's Houdini Submitter
* Houdini >= 19.0

## Usage

* Add karmarenderproperties to your stage
* Set karma's render settings inside karmarenderproperties
* Add huskSubmitter to Driver (/out) context
* Add the 'LOP Path'
* Define your USD output
* Define your image output
* Click 'Submit to Deadline' button

## Using a Different Husk Renderer

By default, Karma is used. If you want to use a different husk supported renderer, you can do so by:
* Going to 'Advanced > Command Line Options' inside the huskSubmitter ROP
* Add '--renderer "name_of_renderer_you_want_to_use"'

## Changes

### 1.0.0  |  11.03.2023

* Initial release