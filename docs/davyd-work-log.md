- 2026-02-13 Friday (1 hour)
    - Had initial call with Chris Michalowski at 10:00am. Had recap with Brady after the call.
    - Chris sent documents related to the project shortly after the call.

- 2026-02-17 Tuesday (3 hours)
    - Met with Brady in person 2:00-5:00pm.
    - Initial look at the two documents Chris had sent over last week. These were the SGM engineering form report and the CDOT report.
    - Understood the relevant geography and streets by reading the documents and looking up streets in maps. Agate St is what highway 40 becomes once it enters downtown Granby. 4th, 5th, 6th, and Mesa St intersect Agate from the north.
    - Understood the motivations for each report. CDOT document was centered more on vehicle congenstion in 4th-6th street. SGM report was focused on implementing potential safety measures around the Agate and Mesa intersection, which is close to the Granby schools.
    - Understood the basic premise of simulation modeling done in the CDOT document (Synchro and SimTraffic). Initial vehicle flow rate parameters are observed from real life, and are then inputed into simulation software to determine other important values like the average wait time for a vehicle at an intersection. Looked into some underlying math of the program and realized its baed on concepts I had covered in my Probabilistic Modeling class from Fall 2024. Things like M/M/1 queues, Poisson arrival times, and exponential gaps between arrivals.
    - created my work log (davyd-work-log.md) and also a folder for notes that I will take like my statistical concepts document, and other isolated topics I summarize as I go. I decided that the notes will be in the form of pdf documents that I will create in google docs and then upload to the github repo. This will make it easier to format and add screenshots.

- 2026-02-24 Tuesday (4 hours)
    - Met with Brady in person.
    - Check in with Erin over zoom. He gave us some clarity about how we should focus on the traffic/pedestrian volumes visualization first because it is something to show the client and also will give us additional ideas as we go. 
    - went over the SGM 4-6th street traffic simulation tables. We made progress on understanding the underlying data and
    tossed around ideas on what data to start extracting into data structures for visualizations.
    - Brady looked into the Synchro software with a youtube tutorial. It was very helpful for understanding the variables
    produced from simulation
    - figured out how to properly manage github. I have to clone instead of make forks like ive been doing previously...

- 2026-02-24 Thursday (30 minutes)
    - Met with Brady in person before consulting class
    - Briefly discussed some ideas about the simulation data and next steps.
    - Still waiting on Chris's response about where the traffic safety measures actually being built.

-2026-03-01 Sunday (5 hours)
    - Chris had answered on Friday and said that there are 2 measures being implemented. Bulbouts will be on Mesa intersection (for pedestrain safety) and a signal on 4-6th area. Our job is to quantify reduction in pedestrian risk
    and justify the costs of those meaures. He shared the expense estimates too.
    - I looked into how to quantify pedestrian risk (docs/davyd_notes/ways_to_quantify_pedestrain_risk.txt). Learned that 
    we can either quantify direct crash rate before and after those measures with a pre made regression model, or simulate
    "conflicts" which are much more common than direct crashes and could be more informative.
    - I learned there is a free modeling software combination to simulate vehicle paths (SUMO) and then quantify conflict (SSAM). 
    - Actually crudely implemented the crash rate given our set of parameters in the Mesa Area. Had to find the right .xlsx
    document and udnerstand the variables in it. We are working with the suburban version because of the 5 lane road, whcih is considered bigger than the traditional rural roads src/HSM_CPM_UrbanSuburbanArterials_v3.2.xlsx
    - NEXT STEPS:
        - Fully understand the .xlsx sheet and input the correct variables from our data. Figure out what coefficeints to multiply by to find the crash rate after bulbouts are installed. Do same for 4-6th street?
        - Discuss and think about whether the conflict simulation approach is worth implementing.
        - Get the McDowel report from Chris, and any other possible data he may have.
        - convert .txt notes into .docx and then resolve merge conflicts on github


- 2026-03-03 Tuesday (3 hours)
    - started making a cheatsheet on the .xlsx formulas and calculations, but it was difficult to understand. Realized I need to draw information from the Highway Safety Manual (HSM).
    - looked into acquiring a copy of the HSM, which turned out to be accessible via Auraria library. Chapter 12 (Predictive Method for Urban and Suburban Arterials) is the relevant section for our work since Agate Ave is a 5-lane urban arterial.

- 2026-03-05 Thursday (2 hours)
    - read into HSM Chapter 12. Started filling out the cheatsheet with the actual equations. Key realization: the SPF for vehicle-pedestrian collisions at unsignalized intersections (Equation 12-30) is an *adjustment factor* approach — it takes the total intersection crash prediction Nbi (which comes from multi-vehicle + single-vehicle SPFs via Equations 12-21 and 12-24) and multiplies it by f_pedi from Table 12-16. So pedestrian crashes are derived indirectly from vehicle crash rates for stop-controlled intersections, unlike the signalized case which has a dedicated pedestrian SPF (Eq 12-29).

- 2026-03-10 Tuesday (3 hours)
    - realized that the indirect pedestrian crash rate estimate for the Mesa intersection is probably insufficient as a standalone justification for the bulbout. f_pedi = 0.022 for 4ST intersections is a blanket adjustment factor and doesn't actually capture anything about the geometry changes the bulbout introduces (reduced crossing distance, reduced exposure time).
    - looked into the peak pedestrian volume data in the SGM study more carefully. The 1-hour peak is only 6 peds (11.4 adjusted), which feels really low to justify anything on its own. This is another reason the direct crash rate approach alone is shaky — we need the conflict simulation angle to supplement it.

- 2026-03-12 Thursday (1.5 hours)
    - looked into SUMO. It has some limitations for what we want to do but it's not impossible. Key steps for our use case: (1) build the network in netedit with the correct lane geometry for before/after bulbout, (2) define vehicle and pedestrian demand based on SGM counts, (3) run the simulation and export trajectory (.fcd) files, (4) feed those into SSAM to quantify conflicts (TTC, PET).

- 2026-03-15 Sunday (3 hours)
    - cloned the SUMO repository and opened it up on my desktop. There were some package issues I had to figure out — macbook spent about an hour downloading necessary packages via brew (xquartz, proj, gdal, fox toolkit for the GUI). Finally got netedit to launch.

- 2026-03-17 Tuesday (3 hours)
    - successfully opened up the visual editor for SUMO. Drew up a basic intersection approximating Agate & Mesa — 5 lanes on Agate, 2 lanes on Mesa, crosswalks on all legs. One difficulty was exporting the trajectory files in a format SSAM can actually ingest; SSAM expects a specific trajectory file format and SUMO's default fcd-output needs post-processing.

- 2026-03-19 Thursday (2 hours)
    - looked into the trajectory export difficulty from Tuesday. Found that there's a traj conversion script in the SSAM docs that handles the SUMO-to-SSAM pipeline, but I need to double-check the units and timestep alignment.
    - talked with Brady on how to address the Mesa Street volume uncertainty. I thought it was best to rely on just upper and lower bounds based on the 4th and 6th street volumes from the SGM study, but Brady wanted to do a more formal uncertainty analysis using variance. That's problematic because of the n=2 sample size — variance on two data points isn't really meaningful statistically. Agreed to go with the bounds approach for now and revisit if Chris gets us more volume data.

- 2026-03-24 Tuesday (3 hours)
    - created a Python notebook that performs sensitivity analysis on the pedestrian crash rate based on different Mesa Street AADT assumptions. Used Equation 12-21 for multi-vehicle and Equation 12-24 for single-vehicle, then applied f_pedi = 0.022 per Table 12-16. It's reassuring that the upper bound of Mesa volume (with bulbout) generates a pedestrian crash rate still below the lower bound without the bulbout — meaning the bulbout treatment dominates the volume uncertainty, which strengthens the recommendation.

- 2026-03-26 Thursday (2.5 hours)
    - looked into how AADT pedestrian can be calculated from the SGM study. There are some problems with their approach — they apply the NBPD seasonal adjustment factor (1.9x from Feb to May) which is designed for multi use paths and pedestrian entertainment districts, not school crossings on a state highway. Also their counts were only 12-hour (7AM-7PM) and the NBPD hourly adjustment factors assume a specific activity profile we can't verify. But we chose to go with it anyway since it's the only data we have and the CMF treatment effect is large enough to absorb some input error.

- 2026-03-31 Tuesday (3.5 hours)
    - started work on validation document. It is unclear how to satisfy the requirements for the assignment given the unique nature of our work, our "data" isn't the typical csv/excel format with missing values and distributions to check. It's a small set of accepted parameters drawn from CDOT resources and the SGM engineering study.
    - reframed the validation problem as being about the modeling process rather than the data itself. The HSM has many variations of crash prediction models depending on road configuration, and our validation is about making sure we match Agate & Mesa to the correct model (3ST urban) and Agate & 4th to the correct model (4ST urban). Wrote up the road characteristics section.
    - note on the urban vs rural classification: Granby has 2000 population which technically meets the FHWA rural definition (<5000), but the rural HSM chapter doesn't support pedestrian crash estimation. So we're using the urban chapter (Ch 12) instead and documenting that choice.

- 2026-04-02 Thursday (2 hours)
    - finished validation document. Worked through the traffic volume section: Agate AADT is 11,000 from CDOT station 101868 (same source SGM used). 4th street AADT isn't publicly available, so I approximated it using the minor/major peak hourly ratios from Table 6 of the SGM signal warrant study
    - wrote up the pedestrian volume conversion method. The HSM signalized intersection pedestrian SPF needs PedVol as daily volume, but we only have peak hourly counts 
    - nice validation result: the Mesa conversion gives the same 138.40 AADT whether you start from the unadjusted peak or the seasonally adjusted peak.

- 2026-04-07 Tuesday (3 hours)
    - worked on presentation for class. Structured it around: (1) background on Highway 40 and the pedestrian safety concern near the Granby schools, (2) the two proposed treatments (3) data aquisition.
    - Brady and I split the slides — he took the problem/background intro and I took the methodology and results. Also included the sensitivity analysis on Mesa AADT uncertainty.

- 2026-04-09 Thursday (2 hours)
    - finished presentation with Brady right before class. Did one practice round beforehand. Presentation in class went okay but we ran long on some of the methodology slides. the HSM model details are dense and hard to compress without losing the logic. 

- 2026-04-10 Friday (1 hour)
    - met with Chris over zoom and presented our slides. It felt much smoother than during class because of the experience of running through slides and knowing what specific bullets/points become too long-winded. Also used tips from class feedback to make better use of the flowchart that I had included as an image but hadn't focused my speaking on.
