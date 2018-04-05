# Infection Dating Tool

This tool enables systematic interpretation of diagnostic test histories into formal plausible infection intervals, using data on "diagnostic delays" (i.e. window periods) of tests, and particular (dated) positive and negative test results. It outputs a detectable infection interval: Lower Bound - Date of Detectable Infection (DDI), Upper Bound DDI and the midpoint of the interval as Estimated Date of Detectable Infection (EDDI). Detectable infection (for HIV) is by default defined as test conversion on a viral load assay with a detection threshold of 1 copy/ml, but arbitrary reference tests or the exposure event may be used at time-zero. In addition, the tool uses these data to estimate residual risk of infectious donated blood units, using properties of the screening algorithm and incidence in the donor population.

## Licence

Code is released under the GPL-3 licence and content under the Creative Commons Attribution ShareAlike (CC-BY-SA) International Version 4 license.

## Contributors

The tool is maintained by the South African Centre for Epidemiological Modelling and Analysis (SACEMA) at Stellenbosch University.

* Alex Welte
* Eduard Grebe
* Shelley Facente
* Andrew Powrie
* Jeremy Bingham
* Jarryd Gerber
* Trust Chibawara
* Chris Pilcher
* Gareth Priede
