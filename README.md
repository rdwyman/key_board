# Customizable Accessability Keycaps
_There are as many unique accessibility needs as there are individulas with accessibility needs. One-size-fits all solutions are insufficient. 3D Printing is here to help._

## Included Models

## Make it yours
Here are some ideas on how to adapt this to your (or a loved ones) specific needs. These are just to get you started, your imaginiation is the only limit! Upload your make or remix so others can adapat it and our accessibility reach can grow!

Accessibility:
* Multi lingual accessibility - Accessibility is needed the world over - add braille support for another language. see the Korean Braille keyboard in `./demos/` for a proof of concept implementation!
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

### Configuration Files
The software uses JSON to specify the keycaps to be made. It organizes the key caps in a tree stucture with a each node potentially contributing a partial or full recipe for how a key cap should be generated. Recipes are merged on top of more basal recipes to compute an effective recipe for the node. This allows a base recipe to be inherited by lower levels. Each node may optionally include an array of children which are in and of themselves nodes. Leaf nodes are actualized into a key cap. Non-leaf nodes are only storage. They do not represent key caps. Nodes may also include an optional overlays parameter. This is an array of file paths to other configuration files that are mergedd on top of the the node at that level. **All** file paths are resolved relative to the folder the program is ran from. The examples are formulated on the assumption the generator is invoked from the root folder of this repository (within the foloder containing [__main__.py](./__main__.py)).

See the configuration files for examples of how the configuration recipes can be composed together.

### Recipes
Recipes are specified by applicators which are small sub recipes specifying a portion of a keycap. Applicators are all optional with the exeption of the cap applicator.

#### Cap Applicator
The cap appllicator determines what key cap is used. It is specifified in a recipe by the property name "cap" and a JSON value as follows. 
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
TODO:

#### Marking Applicator
TODO:

#### Nub Applicator
TODO:

#### Stem Applicator
The cap appllicator determines what key cap is used. It is specifified in a recipe by the property name "cap" and a JSON value as follows. 
```json
{
  "capSolidFile": "./path/to/solidKeyCap.step",
  "capShellFile": "./path/to/shellKeyCap",
  "keyCapThickness": 2.5
}
```

Some of the provided shell key caps are derived from the [Logitech keyboard reference](https://www.printables.com/model/1846004-official-mx-keyboard-cad-templates/files). They do not contain stems - appropriate stem applicators shold be applied to the recipe when using these models. The provided [solid cap](https://www.printables.com/model/1866637-logitech-mx-mechanical-official-cad-keycap-referen/files) files from Logitech already contain stems in them. It is the users responsibility to ensure that the provided stem applicators do not negatively interfere with these.

## How to print the keycaps
Load the STEP file into [Prusaslicer](https://www.prusa3d.com/p/prusaslicer/). If the STEP file is large, you may need to use a lower quality discretization resolution. The STEP file will contain different compounds named "primary", "markings", "nubs", and "braille". Assign colors to each compound per your preference. Depending on the keycap models and stem lengths you use, you may or may not need to enable supports.

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
* The STEP file emitted by this software can be very large. When importing to Prusa slicer, you may need to either turn down the mesh resolution or emit fewer keys per STEP file.
* Custom font files are not as reliable as I wish they were. They will be hit or miss from letter to font.