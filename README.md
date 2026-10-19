# Customizable Accessability Keycaps
_There are as many unique accessibility needs as there are individulas with accessibility needs. One-size-fits all solutions are insufficient. 3D Printing is here to help._

## Included Models

## Make it yours
Here are some ideas on how to adapt this to your (or a loved ones) specific needs. These are just to get you started, your imaginiation is the only limit! Upload your make or remix so others can adapat it and our accessibility reach can grow!

Accessibility:
* Multi lingual accessibility - Accessibility is needed the world over - add braille support for another language. see the Korean Braille keyboard in `./assets/` for a proof of concept implementation!
* Make a phonetic keyboard - "A" is for "Apple" - Help those still learning letter sounds, great for kids too! Use multiple "markings" applicators - one for the letter and one for the glyph.
* Customize it - Make Braille dots larger, use your favorite accessiblity focused font, and more. Ones accessibility needs are unique, their keyboard should be too.
* Use an accessible keycap - add a stick typer friendly keycap with a depression in the middle so the stick doesn't slip when typing - see the [stick keycap](./assets/keyCaps/stickTypingKeyCap.step) for an example implementation
* Make some keycaps larger and others smaller based on particular accessibility or preference needs.

Just for fun / other:
* Change the stem dimensions - If keys pop off, make the slot width tighter, change the stem height for each row of keys to be "just right", add your own stem applicator to support different physical keyboard mounts 
* Print keycaps using an invented language (Elvish? Klingon? Why not?)
* Add musical note keycaps for music annotation software
* Print markings in glow-in-the-dark filament

## How to run the keycap generator software

Quick start for those familar with python. See next section if unfamiliar.
* set up a venv
* install from requirements.txt
* run from command line or an IDE

### Instructions for Python noobs

Using the command line (recommended only if you just want to run the software)
* Install the most recent version of [Python](https://www.python.org/downloads/) - v3.12.3 is known to work
* Download and unzip the source code to a folder on your computer ([direct ZIP download](https://github.com/rdwyman/key_board/archive/refs/heads/master.zip))
* Open a terminal of your choice. I recommend PowerShell on Windows (will be pre-installed) or bash on Linux, though any terminal will likely work
* Use the [`cd` command](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cd) to navigate your terminal to where the code was unzipped. ex for Windows: `cd C:\Users\myUserName\Documents\path\to\key_board`
* Run the command `python -m venv .venv` to create a virtual environemtn (see [here](https://www.xanthium.in/configuring-python-virtual-environment-venv-tutorial-on-windows-linux-os) for details)
* Activate your environment
  * Windows: `.\.venv\Scripts\activate`
  * Linux: `source .venv/bin/activate`
* Install dependencies - `pip install -r requirments.txt`
* Run the software - `python __main__.py ./assets/keyboard.json`. You can point the software at any JSON configuration file you wish. There are some other examples in the `./assets/` folder. See the recipes section for how to mofidy the config file.
* The sofware will generate a `./result.step` file that can be loaded into PrusaSlicer or another slicing program

Using Visual Studio Code (recommended for those who want to run and/or modify the software)
* Install [Visual Studio Code](https://code.visualstudio.com/)
* Install the most recent version of [Python](https://www.python.org/downloads/) - v3.12.3 is known to work
* Download and unzip the source code to a folder on your computer ([direct ZIP download](https://github.com/rdwyman/key_board/archive/refs/heads/master.zip))
* Open this folder in Visual Studio Code - see [here](https://code.visualstudio.com/docs/editing/getting-started/editor-tutorial#_open-a-folder-in-vs-code) for help
* Press F5 to run the software - follow any instructions needed to configure your environment
* You can modify the `.vscode/launch.json` file to change run configurations

### Configuration Files
The software uses JSON to specify the keycaps to be made. It organizes the key caps in a tree stucture with a each node potentially contributing a partial or full recipe for how a key cap should be generated. Recipes are merged on top of more basal recipes to compute an effective recipe for the node. This allows a base recipe to be inherited by lower levels. Each node may optionally include an array of children which are in and of themselves nodes. Leaf nodes are actualized into a key cap. Non-leaf nodes are only storage. They do not represent key caps. Nodes may also include an optional overlays parameter. This is an array of file paths to other configuration files that are mergedd on top of the the node at that level. **All** file paths are resolved relative to the folder the program is ran from. The examples are formulated on the assumption the generator is invoked from the root folder of this repository (within the foloder containing [__main__.py](./__main__.py)).

See the configuration files for examples of how the configuration recipes can be composed together.

### Recipes
Recipes are specified by applicators which are small sub recipes specifying a portion of a keycap. Applicators are all optional with the exeption of the cap applicator.

#### Cap Applicator
The cap applicator determines what key cap is used. It is specifified in a recipe by the property name "cap" and a JSON value as follows. 
```json
{
  "capSolidFile": "./path/to/solidKeyCap.step",
  "capShellFile": "./path/to/shellKeyCap",
  "keyCapThickness": 2.5
}
```
Either a `capSolidFile` or a `capShellFile` must be provided. If a `capShellFile` is provided an optional `keyCapThickness` may be provided to determine how thick it will be. Excessive thicknesses may cause the CAD engine to fail. 

This is the only required applicator within a recipe. A leaf node key cap whose resolved recipe does not contain a cap applicator will raise an exception.

#### Braille Applicator
The braille applicator determines if Braille is shown on the key cap. It is specifified in a recipe by the property name "braille" and a JSON value as follows. The "bindings" key should specify a "letter" key with a value equal to the name of the key of the child data packet that Braille should be generated for. See the demos for examples. The encoding is a mapping from unicode characters to the 6 dot Braille associated with the character. If a child data packet does not contain this key, no braille is generated. The dot diameter, height and spacing are in mm.
```json
"braille": {
    "bindings": {
      "letter": "primary"
    },
    "encoding": {
      "A": "100000",
      "B": "110000",
      "C": "100100",
      "D": "100110",
      "E": "100010",
      "F": "110100"
    },
    "dotDiameter": 2.88,
    "dotHeight": 0.96,
    "dotHorizontalSpacing": 2.34,
    "dotVerticalSpacing": 2.34
}
```

#### Marking Applicator
The markings applicator determines what glyphs are shown on the key. Any unicode character (or string) is theoroetically supported as long as an appropriate font file is provided. It is specifified in a recipe by the property name "markings" and a JSON array of objects as follows. The center is an array of two numbers whose value should be between -1 and 1. These specify the relative location of the glyph on the key cap with 0,0 being the center and 1,1 being the most extreme upper right corner. The "datum" key's value is equal to the name of the key of the child data packet that a glyph should be generated for. If a child data packet does not contain this key, no glyph marking is generated.
```json
"markings": [
    {
        "datum": "primary",
        "center": [
            0.0,
            0.0
        ],
        "fontSize": 11,
        "fontFile": "./assets/fonts/Roboto.ttf",
        "recess": 0.1,
        "extrusion": 0.0
    }
]
```

#### Stem Applicator
The stem applicator determines what stems are used. It is specifified in a recipe by the property name "stems" and a JSON value as follows. Note that this is an array allowing for multiple stems to be specified (though this functionality has not bee tested). The stem uses a cherry profile. See the [standard stem](./assets/overlays/applicatorStemStd.json) for a typical stem dimension, though you will likely want to tweak the slot depth and stem height.
```json
"stems": [
    {
        "center": [
            0,
            0
        ],
        "verticalSlotLength": 4.1,
        "verticalSlotWidth": 1.17,
        "horizontalSlotLength": 4.1,
        "horizontalSlotWidth": 1.17,
        "slotDepth": 6,
        "slotFillet": 0.3,
        "stemHeight": 4.0,
        "stemDiameter": 6.0
    }
]
```

Some of the provided shell key caps are derived from the [Logitech keyboard reference](https://www.printables.com/model/1846004-official-mx-keyboard-cad-templates/files). They do not contain stems - appropriate stem applicators shold be applied to the recipe when using these models. The provided [solid cap](https://www.printables.com/model/1866637-logitech-mx-mechanical-official-cad-keycap-referen/files) files from Logitech already contain stems in them. It is the users responsibility to ensure that the provided stem applicators do not negatively interfere with these.

## How to print the keycaps
Load the STEP file into [PrusalSicer](https://www.prusa3d.com/p/prusaslicer/). If the STEP file is large, you may need to use a lower quality discretization resolution. The STEP file will contain different compounds named "primary", "markings", "nubs", and "braille". Assign colors to each compound per your preference. Depending on the keycap models and stem lengths you use, you may or may not need to enable supports.

I recommend printing with PLA. If you use a softer filament like PETG, consider using a slightly tighter stem width so the keycaps won't slip off. Print per normal settings. If available, I strongly recommend using an automated color changing system. If you do not have one, you can perform your own manual color swaps though note this can be tedious. If doing your own color swaps, consider using a flatter keycap and a shallow marking depth to minimize the number of changes you need to perform. Though not recommended, you may also print the markings separate from the caps and press the markings into the caps in post processing. A dob of glue may help with mounting. This option is easier than manual color swaps but will produce a low quality keycap.

## How to install the keycaps
Follow the Logitech keycap [replacement guide](https://www.logitech.com/en-us/discover/a/keycap-replacement-guide). Keep your original keycaps so they can be swapped back later if needed. If you don't have a keycap removal tool, consider [searching](https://www.printables.com/search/all-models?ctx=models&q=keycap+puller) printables.com for one.

## References
Remixed from:
* https://www.printables.com/model/1846004-official-mx-keyboard-cad-templates/files
* https://www.printables.com/model/1866637-logitech-mx-mechanical-official-cad-keycap-referen/files
* The software relies on the [buiild123d](https://github.com/gumyr/build123d) Python modeling library offered under an [Apache-2.0](https://github.com/gumyr/build123d/blob/dev/LICENSE) license.
* The build123d library uses the [OpenCASCADE Geometry Kernel](https://github.com/Open-Cascade-SAS/OCCT) which is provided under an [LGPL license](https://github.com/Open-Cascade-SAS/OCCT/blob/master/LICENSE_LGPL_21.txt) with a custom [OCCT LGPL exeption](https://github.com/Open-Cascade-SAS/OCCT/blob/master/OCCT_LGPL_EXCEPTION.txt).
* The code leverages the [deepmerge](https://github.com/toumorokoshi/deepmerge) library available on [pip](https://pypi.org/project/deepmerge/) which is offeredd under an [MIT](https://github.com/toumorokoshi/deepmerge/blob/master/LICENSE) license

Note that the build123d bindings to OpenCASCADE are formulated such that the OpenCASCADE library can be swapped out per LGPL requirements while still being offered under an MIT licensse. This licensing explanation is offered as a courtesy and is not an official interpretation of licensing. Consult a lawyer if more authoritative interprestations are needed. This is the most legalese I've ever written - I hope it remains the most.

## Developers
The code is written in Python.
_Confession time. I'm primarily a C++ guy_. I know python but it is not my "first language". [Issues](https://github.com/rdwyman/key_board/issues) and [PRs](https://github.com/rdwyman/key_board/pulls) to improve this code are welcome. Developer focused conversations should be conducted on GitHub. Usage focused conversatiosn should be directed towards Printables.

The software can most easily be extended by adding or improving the various applicator files. The code is relatively simple and should be easy to build upon. If adding a new applicator, ensure to incorporate it's invocation into the `actualize` method in the [__main__.py](./__main__.py) file.

I have included MyPy annotations. Some of the MyPy annotations are known to be incorrect. Treat them as a best cut of what could be available. Improvements to the annotations are appreciated. The code is formatted using [Black](https://pypi.org/project/black/).

There are some improvements in organization that I didn't get around to. I would prefer a factory pattern where each applicator is more consistent with the others. I frankly ran out of time and had to switch to "make it work" mode. My wife needs her husband back 😜

## Known Issues
* The code does very little error checking. If you feed it garbage, you will get garbage squared out. It is your responsiblity to invoke it with reasonable inputs.
* This implementation is very inefficient. Data is re-read from disk for each key. It should be cached. There are many such improvements that can be made. In practice, I've found generation of even full keyboard sets to only take a minute or two.
* The STEP file emitted by this software can be very large. When importing to a slicing progarm, you may need to either turn down the mesh resolution or emit fewer keys per STEP file.
* Custom font files are not as reliable as I wish they were. They will be hit or miss from letter to font.