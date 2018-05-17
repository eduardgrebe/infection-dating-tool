# Infection Dating Tool

This tool enables systematic interpretation of diagnostic test histories into formal plausible infection intervals, using data on "diagnostic delays" (i.e. window periods) of tests, and particular (dated) positive and negative test results. It outputs a detectable infection interval: Earliest Plausible Date of Detectable Infection (EP-DDI), Latest Plausible DDI (LP-DDI) and the midpoint of the interval as an infection time 'point estimate' or Estimated Date of Detectable Infection (EDDI). Detectable infection (for HIV) is by default defined as test conversion on a viral load assay with a detection threshold of 1 RNA copy/ml, but arbitrary reference tests or the exposure event may be used as time-zero. In addition, the tool uses these data to estimate residual risk of infectious donated blood units, using properties of the screening algorithm and incidence in the donor population.

This repository contains the source code for the tool, but potential users are directed to the publicly-available hosted version available at [https://tools.incidence-estimation.org/idt/](https://tools.incidence-estimation.org/idt/).

## License

Copyright of code and content vests in the authors. Code is released under the [GNU General Public License v3 (GPL-3)](https://www.gnu.org/licenses/gpl-3.0.en.html), and content under the Creative Commons [Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode) license.

## Contributors

The tool is maintained by the [South African Centre for Epidemiological Modelling and Analysis (SACEMA)](http://www.sacema.org) at Stellenbosch University. Code was developed was collaboratively by a team at SACEMA and at [Implicit Design](http://www.impd.co.za). Current and past direct contributors include:

* Alex Welte
* Eduard Grebe
* Shelley Facente
* Chris Pilcher
* Andrew Powrie
* Jeremy Bingham
* Jarryd Gerber
* Keith Grootboom
* Trust Chibawara
* Gareth Priede

This tool was based on a system originally developed to support the [Consortium for the Evaluation and Performance of HIV Incidence Assays (CEPHIA)](http://www.incidence-estimation.org/page/cephia).

CEPHIA comprises: Oliver Laeyendecker, Thomas Quinn, David Burns (National Institutes of Health); Alex Welte, Eduard Grebe, Reshma Kassanjee, David Matten, Hilmarié Brand, Trust Chibawara (South African Centre for Epidemiological Modelling and Analysis); Gary Murphy, Elaine Mckinney, Jake Hall (Public Health England); Michael Busch, Sheila Keating, Mila Lebedeva, Dylan Hampton (Blood Systems Research Institute); Christopher Pilcher, Kara Marson, Shelley Facente, Jeffrey Martin; (University of California, San Francisco); Susan Little (University of California, San Diego); Anita Sands (World Health Organization); Tim Hallett (Imperial College London); Sherry Michele Owen, Bharat Parekh, Connie Sexton (Centers for Disease Control and Prevention); Matthew Price, Anatoli Kamali (International AIDS Vaccine Initiative); Lisa Loeb (The Options Study – University of California, San Francisco); Jeffrey Martin, Steven G Deeks, Rebecca Hoh (The SCOPE Study – University of California, San Francisco); Zelinda Bartolomei, Natalia Cerqueira (The AMPLIAR Cohort – University of São Paulo); Breno Santos, Kellin Zabtoski, Rita de Cassia Alves Lira (The AMPLIAR Cohort – Grupo Hospital Conceição); Rosa Dea Sperhacke, Leonardo R Motta, Machline Paganella (The AMPLIAR Cohort – Universidade Caxias Do Sul); Esper Kallas, Helena Tomiyama, Claudia Tomiyama, Priscilla Costa, Maria A Nunes, Gisele Reis, Mariana M Sauer, Natalia Cerqueira, Zelinda Nakagawa, Lilian Ferrari, Ana P Amaral, Karine Milani (The São Paulo Cohort – University of São Paulo, Brazil); Salim S Abdool Karim, Quarraisha Abdool Karim, Thumbi Ndungu, Nelisile Majola, Natasha Samsunder (CAPRISA, University of Kwazulu-Natal); Denise Naniche (The GAMA Study – Barcelona Centre for International Health Research); Inácio Mandomando, Eusebio V Macete (The GAMA Study – Fundacao Manhica); Jorge Sanchez, Javier Lama (SABES Cohort – Asociación Civil Impacta Salud y Educación (IMPACTA)); Ann Duerr (The Fred Hutchinson Cancer Research Center); Maria R Capobianchi (National Institute for Infectious Diseases "L. Spallanzani", Rome); Barbara Suligoi (Istituto Superiore di Sanità, Rome); Susan Stramer (American Red Cross); Phillip Williamson (Creative Testing Solutions / Blood Systems Research Institute); Marion Vermeulen (South African National Blood Service); and Ester Sabino (Hemocentro do Sao Paolo).

CEPHIA was supported by grants from the Bill and Melinda Gates Foundation (OPP1017716, OPP1062806 and OPP1115799). Additional support for analysis was provided by a grant from the US National Institutes of Health (R34 MH096606) and by the South African Department of Science and Technology and the National Research Foundation. Specimen and data collection were funded in part by grants from the NIH (P01 AI071713, R01 HD074511, P30 AI027763, R24 AI067039, U01 AI043638, P01 AI074621 and R24 AI106039); the HIV Prevention Trials Network (HPTN) sponsored by the NIAID, National Institutes of Child Health and Human Development (NICH/HD), National Institute on Drug Abuse, National Institute of Mental Health, and Office of AIDS Research, of the NIH, DHHS (UM1 AI068613 and R01 AI095068); the California HIV-1 Research Program (RN07-SD-702); Brazilian Program for STD and AIDS, Ministry of Health (914/BRA/3014-UNESCO); and the São Paulo City Health Department (2004-0.168.922–7). M.A.P. and selected samples from IAVI-supported cohorts are funded by IAVI with the generous support of USAID and other donors; a full list of IAVI donors is available at www.iavi.org.

## Release note

The tool was originally developed as part of the CEPHIA data management system. It is now a standalone tool, but the codebase currently still contains numerous superfluous components reflecting this heritage. These extraneous components do not affect the infection date estimation procedure, and will be removed in due course.

Contributions (by forking the repository and generating pull requests) are encouraged.

For further information, contact [Eduard Grebe](mailto:eduardgrebe@sun.ac.za).
