


# Customizable Accessability Keycaps

_There are as many unique accessibility needs as there are individulas with accessibility needs. One-size-fits all solutions are insufficient. 3D Printing is here to help._

## Table of Contents

## Included Models

## Make it yours

Here are some ideas on how to adapt this to your (or a loved ones) specific needs. These are just to get you started, your imaginiation is the only limit! Upload your make or remix so others can adapat it and our accessibility reach can grow!

Accessibility:
* Multi lingual accessibility - Accessibility is needed the world over - add braille support for another language. see the Korean Braille keyboard in `./demos/` for a proof of concept implementation!
* Make a phonetic keyboard - "A" is for "Apple" - Help those still learning letter sounds, great for kids too! Use multiple "markings" applicators - one for the letter and one for the glyph.
* Customize it - Make Braille dots larger, use your favorite accessiblity focused font, and more. Ones accessibility needs are unique, their keyboard should be too.
* Use an accessible keycap - add a keycap with a depression so stick typers stick's don't slip when typing or make some keycaps larger and others smaller based on particular needs.

Just for fun / other:
* Change the stem dimensions - If keys pop off, make the slot width tighter, change the stem height for each row of keys to be "just right", add your own stem applicator to support different physical keyboard mounts 
* Print keycaps using an invented language (Elvish? Klingon? Why not?)
* Add musical note keycaps for music annotation software
* Print markings in glow-in-the-dark filament

## How to run the software


## How to print the keycaps


## Notes
Remixed from:
* https://www.printables.com/model/1846004-official-mx-keyboard-cad-templates/files
* https://www.printables.com/model/1866637-logitech-mx-mechanical-official-cad-keycap-referen/files


## Known Issues
* The code does very little error checking. If you feed it garbage, you will get garbage squared out. It is your responsiblity to invoke it with reasonable inputs.
* This implementation is very inefficient. Data is re-read from disk for each key. It should be cached. There are many such improvements that can be made. In practice, I've found generation of even full keyboard sets to only take a minute or two.
* The STEP file emitted by this software can be very large. When importing to Prusa slicer, you may need to either turn down the mesh resolution or emit fewer keys per STEP file.
