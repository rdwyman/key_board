


## Known Issues
* The code does very little error checking. If you feed it garbage, you'll get garbage squared out. It is your responsiblity to invoke it with reasonable inputs.
* This implementation is very inefficient. Data is re-read from disk for each key. It should be cached. There are many such improvements that can be made.
* The STEP file emitted by this software can be very large. When importing to Prusa slicer, you may need to either turn down the mesh resolution or emit fewer keys per STEP file.
