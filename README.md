# huskDeadline

## (huskDeadline)

* Description: Karma/Husk Deadline Submitter for Houdini
* Copyright: AXISFX LTD
* Author: Ewan Davidson
* Email: ewan@axisfx.design
* Release Date: 11.03.2023
* Current Version: 1.0.2

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

## Limitations

* Exporting as EXR is the only way to write additional AOVs

## Changes

### 1.0.3  |  10.04.2023

* Deadline job suffixed with renderer name instead of 'Karma'

### 1.0.2  |  18.03.2023

* Deadline task errors when no Karma license is found
* USD ROP flattens all layers

### 1.0.1  |  12.03.2023

* Fixed re.Pattern and re.Match not existing in older versions of houdini
* Attempts to decifer $F from keyframed parameters (when hou.Parm.unexpandedString fails)
* Added --make-output-path argument - huskDeadline plugin handled missing output path creation originally

### 1.0.0  |  11.03.2023

* Initial release