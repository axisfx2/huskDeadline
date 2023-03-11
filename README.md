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

* Add the karmarenderproperties node to your stage
* Set karma's render settings inside karmarenderproperties
* Add huskSubmitter to Driver (/out) context
* Set the 'LOP Path' to the output of your stage
* Set the 'USD output'
* Set the 'Image Output'
* Click 'Submit to Deadline' button

## Changes

### 1.0.0  |  11.03.2023

* Initial release