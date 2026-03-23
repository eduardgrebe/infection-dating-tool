# Infection Dating Tool

This tool enables systematic interpretation of diagnostic test histories into formal plausible
infection intervals, using data on "diagnostic delays" (i.e. window periods) of tests, and
particular (dated) positive and negative test results. It outputs a detectable infection
interval: Earliest Plausible Date of Detectable Infection (EP-DDI), Latest Plausible DDI
(LP-DDI) and the midpoint of the interval as an infection time point estimate, or Estimated
Date of Detectable Infection (EDDI). Detectable infection (for HIV) is by default defined as
test conversion on a viral load assay with a detection threshold of 1 RNA copy/ml, but
arbitrary reference tests or the exposure event may be used as time-zero.

## Method

EP-DDI and LP-DDI are computed using a Bayesian posterior probability density approach. For
each participant, test dates are adjusted by the diagnostic delay of the relevant assay. The
posterior distribution of the infection date is then derived from the joint likelihood of the
observed negative and positive test results. By default, EP-DDI and LP-DDI are the bounds of
a 95% credibility interval of this posterior. Alternatively, they may be set to the adjusted
dates of the latest negative and earliest positive tests directly (median diagnostic delay
mode). The EDDI is the midpoint of the EP-DDI / LP-DDI interval.

Diagnostic delays and their uncertainty (sigma) for ~50 HIV assays are bundled with the tool,
drawn primarily from Delaney et al. (2017) *Clinical Infectious Diseases* 64(1):53–59. For
viral load assays, the diagnostic delay is derived from the assay detection threshold and an
assumed viral load growth rate (default: 0.35 log₁₀ copies/ml/day; Fiebig et al. 2003).

The method is documented in 
> Grebe E, Facente SN, Bingham J, Pilcher CD, Powrie A, Gerber J, 
> Priede G, Chibawara T, Busch MP, Murphy G, Kassanjee R, Welte A; Consortium for the Evaluation 
> and Performance of HIV Incidence Assays (CEPHIA). Interpreting HIV diagnostic histories into 
> infection time estimates: analytical framework and online tool. BMC Infect Dis. 2019 Oct 
> 26;19(1):894. doi: [10.1186/s12879-019-4543-9](https://doi.org/10.1186/s12879-019-4543-9). 
> PMID: 31655566; PMCID: PMC6815418.

## Usage

### Running the app

```bash
uv run streamlit run app.py
```

Or, with the virtual environment activated:

```bash
streamlit run app.py
```

### Input format

Upload a CSV file with the following four columns:

| Column | Description |
|--------|-------------|
| `Participant` | Participant identifier |
| `Date` | Test date in `YYYY-MM-DD` format |
| `Test` | Test code (any string; mapped to a known assay in Step 2) |
| `Result` | `positive`, `pos`, or `+` / `negative`, `neg`, or `-` |

An example input file is available for download within the app, or directly at
`data/ExampleData.csv` in this repository.

### Workflow

1. **Upload** — provide a CSV test history file
2. **Map tests** — assign each test code in the file to a known diagnostic assay
3. **Parameters** — optionally adjust the viral load growth rate and credibility interval settings
4. **Calculate** — run the EDDI estimation
5. **Results** — view and download the results table (Participant, EP-DDI, LP-DDI, Interval Size, EDDI, Flags)

## License

Copyright of code derived or ported from the original Infection Dating Tool vests jointly in
[Stellenbosch University](https://www.sun.ac.za) and [Eduard Grebe Consulting (Pty) Ltd](https://grebe.consulting) and 
any other existing copyright holders. Copyright of new code written for this rewrite vests in Eduard Grebe Consulting (Pty) Ltd. 
Content copyright vests in the authors.

Code is released under the
[GNU General Public License v3 (GPL-3)](https://www.gnu.org/licenses/gpl-3.0.en.html)
or any later version. Content is released under the Creative Commons
[Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)
license.

## Credits

This application is a rewrite of the original Infection Dating Tool, performed using
[Claude Code](https://claude.ai/claude-code) under the direction of [Eduard Grebe](https://grebe.consulting). The core
statistical logic — in particular the Bayesian posterior probability density method for
credibility interval estimation — is ported directly from that earlier work. All contributors
to the original tool are acknowledged below.

The original tool was associated with the
[South African Centre for Epidemiological Modelling and Analysis (SACEMA)](http://www.sacema.org)
at Stellenbosch University. The original codebase was developed collaboratively by a team at
SACEMA and [Implicit Design](http://www.impd.co.za).

### Conceptualisation, design, code & data curatorship

* Alex Welte (SACEMA, University of KwaZulu-Natal)
* Eduard Grebe (SACEMA, Vitalant Research Institute, Eduard Grebe Consulting)
* Shelley Facente (Vitalant Research Institute, Facente Consulting)

The person who originally developed the conceptual framework is Alex Welte.

### Design & code

* Andrew Powrie (Implicit Design)
* Gareth Priede (Implicit Design)

### Code

* Jarryd Gerber (Implicit Design)
* Keith Grootboom (Implicit Design)
* Trust Chibawara (SACEMA)
* Jeremy Bingham (SACEMA)

### Conceptualisation

* Reshma Kassanjee (SACEMA, University of Cape Town)
* Christopher D. Pilcher (University of California San Francisco)
* Gary Murphy (Public Health England)
* Michael P. Busch (Vitalant Research Institute)

### Data

* Kevin P. Delaney (US Centers for Disease Control and Prevention)

## Funding

This tool was based on a system originally developed to support the
[Consortium for the Evaluation and Performance of HIV Incidence Assays (CEPHIA)](http://www.incidence-estimation.org/page/cephia).

CEPHIA comprises: Oliver Laeyendecker, Thomas Quinn, David Burns (National Institutes of
Health); Alex Welte, Eduard Grebe, Reshma Kassanjee, David Matten, Hilmarié Brand, Trust
Chibawara (South African Centre for Epidemiological Modelling and Analysis); Gary Murphy,
Elaine Mckinney, Jake Hall (Public Health England); Michael Busch, Sheila Keating, Mila
Lebedeva, Dylan Hampton (Blood Systems Research Institute); Christopher Pilcher, Kara Marson,
Shelley Facente, Jeffrey Martin (University of California, San Francisco); Susan Little
(University of California, San Diego); Anita Sands (World Health Organization); Tim Hallett
(Imperial College London); Sherry Michele Owen, Bharat Parekh, Connie Sexton (Centers for
Disease Control and Prevention); Matthew Price, Anatoli Kamali (International AIDS Vaccine
Initiative); Lisa Loeb (The Options Study – University of California, San Francisco); Jeffrey
Martin, Steven G Deeks, Rebecca Hoh (The SCOPE Study – University of California, San
Francisco); Zelinda Bartolomei, Natalia Cerqueira (The AMPLIAR Cohort – University of São
Paulo); Breno Santos, Kellin Zabtoski, Rita de Cassia Alves Lira (The AMPLIAR Cohort – Grupo
Hospital Conceição); Rosa Dea Sperhacke, Leonardo R Motta, Machline Paganella (The AMPLIAR
Cohort – Universidade Caxias Do Sul); Esper Kallas, Helena Tomiyama, Claudia Tomiyama,
Priscilla Costa, Maria A Nunes, Gisele Reis, Mariana M Sauer, Natalia Cerqueira, Zelinda
Nakagawa, Lilian Ferrari, Ana P Amaral, Karine Milani (The São Paulo Cohort – University of
São Paulo, Brazil); Salim S Abdool Karim, Quarraisha Abdool Karim, Thumbi Ndungu, Nelisile
Majola, Natasha Samsunder (CAPRISA, University of Kwazulu-Natal); Denise Naniche (The GAMA
Study – Barcelona Centre for International Health Research); Inácio Mandomando, Eusebio V
Macete (The GAMA Study – Fundacao Manhica); Jorge Sanchez, Javier Lama (SABES Cohort –
Asociación Civil Impacta Salud y Educación (IMPACTA)); Ann Duerr (The Fred Hutchinson Cancer
Research Center); Maria R Capobianchi (National Institute for Infectious Diseases
"L. Spallanzani", Rome); Barbara Suligoi (Istituto Superiore di Sanità, Rome); Susan Stramer
(American Red Cross); Phillip Williamson (Creative Testing Solutions / Blood Systems Research
Institute); Marion Vermeulen (South African National Blood Service); and Ester Sabino
(Hemocentro do Sao Paolo).

CEPHIA was supported by grants from the Bill and Melinda Gates Foundation (OPP1017716,
OPP1062806 and OPP1115799). Additional support for analysis was provided by a grant from the
US National Institutes of Health (R34 MH096606) and by the South African Department of
Science and Technology and the National Research Foundation. Specimen and data collection were
funded in part by grants from the NIH (P01 AI071713, R01 HD074511, P30 AI027763, R24
AI067039, U01 AI043638, P01 AI074621 and R24 AI106039); the HIV Prevention Trials Network
(HPTN) sponsored by the NIAID, National Institutes of Child Health and Human Development
(NICH/HD), National Institute on Drug Abuse, National Institute of Mental Health, and Office
of AIDS Research, of the NIH, DHHS (UM1 AI068613 and R01 AI095068); the California HIV-1
Research Program (RN07-SD-702); Brazilian Program for STD and AIDS, Ministry of Health
(914/BRA/3014-UNESCO); and the São Paulo City Health Department (2004-0.168.922–7). M.A.P.
and selected samples from IAVI-supported cohorts are funded by IAVI with the generous support
of USAID and other donors; a full list of IAVI donors is available at www.iavi.org.

The rewrite was sponsored by [Eduard Grebe Consulting](https://grebe.consulting).
