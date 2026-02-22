Master Reference List
=====================

All publications, datasets, and resources referenced across the OpenWorm documentation and Design Documents. The **Description** column indicates which Design Documents cite each reference.

---

## Core OpenWorm Publications

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Sarma et al. 2018](https://doi.org/10.1098/rstb.2017.0382) | Phil Trans R Soc B 373:20170382 | 2018 | OpenWorm: overview and recent advances in integrative biological simulation of *C. elegans*. [DD011](design_documents/DD011_Contributor_Progression_Model.md) |
| [Gleeson et al. 2018](https://doi.org/10.1098/rstb.2017.0379) | Phil Trans R Soc B 373:20170379 | 2018 | c302: a multiscale framework for modelling the nervous system of *C. elegans*. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md) |
| [Sarma et al. 2016](https://doi.org/10.12688/f1000research.9095.1) | F1000Research 5:1946 | 2016 | Unit testing, model validation, and biological simulation. [DD010](design_documents/DD010_Validation_Framework.md), [DD013](design_documents/DD013_Simulation_Stack_Architecture.md), [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) |

---

## Connectome & Neural Wiring

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [White et al. 1986](https://doi.org/10.1098/rstb.1986.0056) | Phil Trans R Soc B 314:1-340 | 1986 | The original *C. elegans* connectome — "The Mind of a Worm". [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md), [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md), [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) |
| [Varshney et al. 2011](https://doi.org/10.1371/journal.pcbi.1001066) | PLoS Comput Biol 7:e1001066 | 2011 | Updated connectome with corrected synapse counts. [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) |
| [Cook et al. 2019](https://doi.org/10.1038/s41586-019-1352-7) | Nature 571:63-71 | 2019 | Whole-animal connectome of adult hermaphrodite and male — **primary connectome for OpenWorm**. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD002](design_documents/DD002_Muscle_Model_Architecture.md), [DD003](design_documents/DD003_Body_Physics_Architecture.md), [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD008](design_documents/DD008_Data_Integration_Pipeline.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD014](design_documents/DD014_Dynamic_Visualization_Architecture.md), [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md), [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md), [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Witvliet et al. 2021](https://doi.org/10.1038/s41586-021-03778-8) | Nature 596:257-261 | 2021 | Developmental connectomes across 8 stages (L1 → adult). [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD004](design_documents/DD004_Mechanical_Cell_Identity.md), [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD008](design_documents/DD008_Data_Integration_Pipeline.md), [DD014](design_documents/DD014_Dynamic_Visualization_Architecture.md), [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) |
| [Brittin et al. 2021](https://doi.org/10.1038/s41586-021-03284-x) | Nature 591:105-110 | 2021 | Contact-area-based connectome weighting. [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) |
| [Wang et al. 2024](https://doi.org/10.7554/eLife.95402) | eLife 13:RP95402 | 2024 | Neurotransmitter identity for every synapse. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) |
| [Yim et al. 2024](https://doi.org/10.1038/s41467-024-45943-3) | Nat Commun 15:1546 | 2024 | Comparative connectomics of dauer. [DD014](design_documents/DD014_Dynamic_Visualization_Architecture.md), [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) |
| [Bentley et al. 2016](https://doi.org/10.1371/journal.pcbi.1005283) | PLoS Comput Biol 12:e1005283 | 2016 | Multilayer connectome of *C. elegans* (synaptic + gap junction + neuropeptide layers). [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md) |
| [Bargmann & Marder 2013](https://doi.org/10.1038/nmeth.2451) | Nat Methods 10:483-490 | 2013 | From the connectome to brain function — connection topology is necessary but not sufficient. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md) |

---

## Whole-Brain Imaging & Neural Dynamics

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) | Nature 623:406-414 | 2023 | Whole-brain calcium imaging — **primary data for Tier 2 validation**. [Validation](validation.md), [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md), [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD008](design_documents/DD008_Data_Integration_Pipeline.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md), [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Kato et al. 2015](https://doi.org/10.1016/j.cell.2015.09.034) | Cell 163:656-669 | 2015 | Global brain dynamics embed the motor command sequence of *C. elegans* — PCA of whole-brain dynamics. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD010](design_documents/DD010_Validation_Framework.md) |
| [Atanas et al. 2022](https://doi.org/10.1101/2022.11.11.516186) | bioRxiv 2022.11.11.516186 | 2022 | Brain-wide representations of behavior spanning multiple timescales and states. [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md) |

---

## Neuropeptide & Neuromodulatory Signaling

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Ripoll-Sanchez et al. 2023](https://doi.org/10.1016/j.neuron.2023.09.043) | Neuron 111:3570-3589 | 2023 | Neuropeptide connectome — 31,479 peptide-receptor interactions. [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD008](design_documents/DD008_Data_Integration_Pipeline.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) |
| [Li et al. 1999](https://doi.org/10.1016/S0006-8993(99)01972-1) | Brain Res 848:26-34 | 1999 | FMRFamide-related neuropeptide gene family in *C. elegans*. [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD010](design_documents/DD010_Validation_Framework.md) |
| [Rogers et al. 2003](https://doi.org/10.1038/nn1140) | Nat Neurosci 6:1178-1185 | 2003 | FLP peptide loss-of-function phenotypes. [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD010](design_documents/DD010_Validation_Framework.md) |
| [Choi et al. 2013](https://doi.org/10.1016/j.neuron.2013.04.002) | Neuron 78:869-880 | 2013 | PDF-1 neuropeptide modulates arousal state. [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md) |
| [Pereira et al. 2015](https://doi.org/10.7554/eLife.12432) | eLife 4:e12432 | 2015 | Cellular and regulatory map of the cholinergic nervous system of *C. elegans*. [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD010](design_documents/DD010_Validation_Framework.md) |
| [Beets et al. 2022](https://doi.org/10.7554/eLife.81548) | eLife 12:e81548 | 2022 | System-wide mapping of neuropeptide-GPCR interactions in *C. elegans*. [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md) |
| [Flavell et al. 2020](https://doi.org/10.1534/genetics.120.303539) | Genetics 216:315-332 | 2020 | Behavioral states in *C. elegans*. [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Marder et al. 2014](https://doi.org/10.1146/annurev-neuro-071013-013958) | Annu Rev Neurosci 37:329-346 | 2014 | Neuromodulation of circuits with variable parameters. [DD015](design_documents/DD015_AI_Contributor_Model.md) |

---

## Single-Cell Electrophysiology (Tier 1 Validation)

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Goodman et al. 1998](https://doi.org/10.1016/S0896-6273(00)81014-4) | Neuron 20:763-772 | 1998 | Active currents regulate sensitivity and dynamic range in *C. elegans* neurons — evidence for graded potentials. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD002](design_documents/DD002_Muscle_Model_Architecture.md), [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Goodman et al. 2002](https://doi.org/10.1038/4151039a) | Nature 415:1039-1042 | 2002 | Touch receptor whole-cell patch-clamp — **primary Tier 1 data for ALM, AVM, PLM**. [DD010](design_documents/DD010_Validation_Framework.md), [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [O'Hagan et al. 2005](https://doi.org/10.1038/nn1362) | Nat Neurosci 8:43-50 | 2005 | MEC-4 DEG/ENaC channel kinetics in touch neurons. [DD010](design_documents/DD010_Validation_Framework.md), [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Suzuki et al. 2003](https://doi.org/10.1016/S0896-6273(03)00539-7) | Neuron 39:1005-1017 | 2003 | In vivo calcium imaging of mechanosensory neurons (ALM, AVM, PLM). [DD010](design_documents/DD010_Validation_Framework.md) |
| [Chalasani et al. 2007](https://doi.org/10.1038/nature06292) | Nature 449:63-71 | 2007 | AWC olfactory neuron calcium imaging, TAX-2/TAX-4 channel characterization. [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md), [DD010](design_documents/DD010_Validation_Framework.md) |
| [Lindsay et al. 2011](https://doi.org/10.1038/ncomms1304) | Nat Commun 2:306 | 2011 | AVA command interneuron whole-cell recordings — graded potential dynamics. [DD010](design_documents/DD010_Validation_Framework.md) |
| Liu et al. 2018 | eLife 7:e36607 | 2018 | RIM motor neuron electrophysiology, EGL-19/UNC-2 channel characterization. [DD010](design_documents/DD010_Validation_Framework.md) |
| [Mellem et al. 2002](https://doi.org/10.1016/S0896-6273(02)01088-7) | Neuron 36:933-944 | 2002 | Interneuron electrophysiology — AVA, AVD, AVB recordings. [DD010](design_documents/DD010_Validation_Framework.md) |
| [Hendricks et al. 2012](https://doi.org/10.1038/nature11081) | Nature 487:99-103 | 2012 | Compartmentalized calcium dynamics in a *C. elegans* interneuron — evidence for spatially compartmentalized signaling within neurons. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md) |
| [Liu et al. 2018b](https://doi.org/10.1016/j.cell.2018.08.018) | Cell 175:57-70 | 2018 | *C. elegans* AWA olfactory neurons fire calcium-mediated all-or-none action potentials — evidence that some neurons use action potentials. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md) |
| [Nicoletti et al. 2019](https://doi.org/10.1371/journal.pone.0218738) | PLoS ONE 14:e0218738 | 2019 | Biophysical modeling of *C. elegans* neurons: Single ion currents and whole-cell dynamics of AWCon and RMD. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md) |
| [Leifer et al. 2011](https://doi.org/10.1038/nmeth.1140) | Nat Methods 8:147-152 | 2011 | Optogenetic stimulation with whole-brain imaging. [DD010](design_documents/DD010_Validation_Framework.md) |

---

## Gene Expression & Transcriptomics

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Taylor et al. 2021](https://doi.org/10.1016/j.cell.2021.06.023) | Cell 184:4329-4347 | 2021 | **CeNGEN** — single-cell transcriptome atlas of 128 neuron classes. [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md), [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD010](design_documents/DD010_Validation_Framework.md) |
| [Packer et al. 2019](https://doi.org/10.1126/science.aax1971) | Science 365:eaax1971 | 2019 | Embryonic single-cell RNA-seq atlas. [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md), [DD008](design_documents/DD008_Data_Integration_Pipeline.md) |
| [Yemini et al. 2021](https://doi.org/10.1016/j.cell.2020.12.012) | Cell 184:272-288 | 2021 | NeuroPAL: Multicolor atlas for whole-brain neuronal identification in *C. elegans*. [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md) |
| [Alon et al. 2021](https://doi.org/10.1126/science.aax2656) | Science 371:eaax2656 | 2021 | Expansion sequencing: spatially precise in situ transcriptomics in intact biological systems. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md) |
| [Shaib et al. 2023](https://doi.org/10.1038/s41587-024-02431-9) | Nat Biotechnol | 2023 | *C. elegans*-optimized expansion microscopy — synapse-level molecular identity with 20-fold expansion. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md) |

---

## Muscle & Body Physics

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Boyle & Cohen 2008](https://doi.org/10.1016/j.biosystems.2008.05.025) | Biosystems 94:170-181 | 2008 | Muscle model with calcium-force coupling — **basis for [DD002](design_documents/DD002_Muscle_Model_Architecture.md)**. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD002](design_documents/DD002_Muscle_Model_Architecture.md), [DD003](design_documents/DD003_Body_Physics_Architecture.md), [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md), [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) |
| [Müller et al. 2003](https://doi.org/10.2312/SCA03/154-159) | Proc. ACM SIGGRAPH/Eurographics SCA pp. 154-159 | 2003 | Particle-based fluid simulation for interactive applications — SPH kernel functions. [DD003](design_documents/DD003_Body_Physics_Architecture.md) |
| [Solenthaler & Pajarola 2009](https://doi.org/10.1145/1531326.1531346) | ACM Trans Graphics 28(3):40 | 2009 | Predictive-Corrective Incompressible SPH (PCISPH) — pressure solver used in Sibernetic. [DD003](design_documents/DD003_Body_Physics_Architecture.md) |
| [Bouaziz et al. 2014](https://doi.org/10.1145/2601097.2601116) | ACM Trans Graphics 33:154 | 2014 | Projective Dynamics: fusing constraint projections for fast simulation — FEM alternative to SPH. [DD003](design_documents/DD003_Body_Physics_Architecture.md) |
| [Wen et al. 2012](https://doi.org/10.1016/j.neuron.2012.08.032) | Neuron 76:750-761 | 2012 | Proprioceptive coupling within motor neurons drives undulatory locomotion in *C. elegans*. [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md), [DD023](design_documents/DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) |

---

## Touch & Mechanosensation

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Chalfie et al. 1985](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985) | J Neurosci 5:956-964 | 1985 | Discovery of gentle touch response circuit. [Validation](validation.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [O'Hagan et al. 2005](https://doi.org/10.1038/nn1362) | Nat Neurosci 8:43-50 | 2005 | MEC-4 channel electrophysiology (DEG/ENaC mechanotransduction). [DD010](design_documents/DD010_Validation_Framework.md), [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Wicks et al. 1996](https://doi.org/10.1523/JNEUROSCI.16-12-04017.1996) | J Neurosci 16:4017-4031 | 1996 | Tap withdrawal circuit — anterior vs. posterior discrimination. [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md) |
| [Goodman et al. 2002](https://doi.org/10.1038/4151039a) | Nature 415:1039-1042 | 2002 | Touch receptor electrophysiology. [DD010](design_documents/DD010_Validation_Framework.md), [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Suzuki et al. 2003](https://doi.org/10.1016/S0896-6273(03)00539-7) | Neuron 39:1005-1017 | 2003 | In vivo calcium imaging of mechanosensory neurons. [DD010](design_documents/DD010_Validation_Framework.md) |
| [Chalasani et al. 2007](https://doi.org/10.1038/nature06292) | Nature 449:63-71 | 2007 | Chemosensory transduction in AWC neurons. [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md), [DD010](design_documents/DD010_Validation_Framework.md) |

---

## Pharynx & Feeding

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Raizen & Avery 1994](https://doi.org/10.1016/0896-6273(94)90207-0) | Neuron 12:483-495 | 1994 | Electropharyngeogram (EPG) recordings — **pharyngeal validation data**. [DD007](design_documents/DD007_Pharyngeal_System_Architecture.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Avery & Horvitz 1989](https://doi.org/10.1016/0896-6273(89)90037-8) | Neuron 3:473-485 | 1989 | Pharyngeal pumping continues after laser killing of the pharyngeal nervous system. [DD007](design_documents/DD007_Pharyngeal_System_Architecture.md) |

---

## Intestine & Defecation

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Thomas 1990](https://doi.org/10.1093/genetics/124.4.855) | Genetics 124:855-872 | 1990 | Defecation motor program timing (50s cycle). [DD009](design_documents/DD009_Intestinal_Oscillator_Model.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Dal Santo et al. 1999](https://doi.org/10.1016/S0092-8674(00)81510-X) | Cell 98:757-767 | 1999 | Cell-autonomous IP3/calcium oscillations in intestinal cells. [DD009](design_documents/DD009_Intestinal_Oscillator_Model.md) |
| [Teramoto & Iwasaki 2006](https://doi.org/10.1016/j.ceca.2006.08.012) | Cell Calcium 40:319-327 | 2006 | Intestinal calcium waves coordinate a behavioral motor program. [DD009](design_documents/DD009_Intestinal_Oscillator_Model.md) |

---

## Egg-Laying & Reproductive Circuit

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Trent et al. 1983](https://doi.org/10.1093/genetics/104.4.619) | Genetics 104:619-647 | 1983 | 145 egg-laying defective (Egl) mutants, 4 pharmacological classes. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) |
| [Waggoner et al. 1998](https://doi.org/10.1016/S0896-6273(00)80527-9) | Neuron 21:203-214 | 1998 | Serotonin pharmacology of egg-laying — two-state behavioral model. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) |
| [Schafer 2006](https://doi.org/10.1895/wormbook.1.38.1) | WormBook | 2006 | Egg-laying comprehensive review. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) |
| [Zhang et al. 2008](https://doi.org/10.1016/j.cub.2008.09.005) | Curr Biol 18:1445-1455 | 2008 | Self-regulating feed-forward circuit controlling egg-laying behavior. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) |
| [Sun & Bhatt 2010](https://doi.org/10.1186/1752-0509-4-81) | BMC Syst Biol 4:81 | 2010 | Computational model of egg-laying circuit temporal pattern generation. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) |
| [Collins & Koelle 2013](https://doi.org/10.1523/JNEUROSCI.3587-12.2013) | J Neurosci 33:761-775 | 2013 | UNC-103 ERG potassium channel in vulval muscles — two-state excitability mechanism. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) |
| [Collins et al. 2016](https://doi.org/10.7554/eLife.21126) | eLife 5:e21126 | 2016 | Calcium imaging of egg-laying circuit — **two-state behavioral pattern**. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Brewer et al. 2019](https://doi.org/10.1371/journal.pgen.1007896) | PLoS Genet 15:e1007896 | 2019 | Tyramine/octopamine signaling in egg-laying. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) |
| [Ravi et al. 2020](https://doi.org/10.1523/JNEUROSCI.0173-20.2020) | J Neurosci 40:7475-7488 | 2020 | Expression, function, and pharmacological analysis of all 26 neurotransmitter GPCRs in *C. elegans*. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) |
| [Kopchock et al. 2021](https://doi.org/10.1523/JNEUROSCI.2599-20.2021) | J Neurosci 41:3635-3650 | 2021 | VC neurons are mechanically activated motor neurons in the egg-laying circuit. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) |
| [Collins & Bhatt 2022](https://doi.org/10.1093/genetics/iyac084) | Genetics 221:iyac084 | 2022 | Serotonin signals through Gαq/Trio/DAG in egg-laying circuit. [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) |

---

## Behavioral Analysis & Neuroethology

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Schafer 2005](https://doi.org/10.1016/j.cub.2005.08.020) | Curr Biol 15:R723-R729 | 2005 | Deciphering the neural and molecular mechanisms of *C. elegans* behavior. [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) |
| [Yemini et al. 2013](https://doi.org/10.1038/nmeth.2560) | Nat Methods 10:877-879 | 2013 | Schafer lab behavioral feature database — **primary Tier 3 validation data**. [Validation](validation.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) |
| [Brown et al. 2013](https://doi.org/10.1073/pnas.1211447110) | PNAS 110:791-796 | 2013 | A dictionary of behavioral motifs reveals clusters of genes affecting locomotion. [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) |
| [Berman et al. 2014](https://doi.org/10.1098/rsif.2014.0672) | J R Soc Interface 11:20140672 | 2014 | Mapping the stereotyped behaviour of freely moving fruit flies — behavioral embedding methods. [DD010](design_documents/DD010_Validation_Framework.md) |
| [Javer et al. 2018](https://doi.org/10.1038/s41592-018-0112-1) | Nat Methods 15:645-646 | 2018 | Tierpsy Tracker — multi-worm behavioral tracking. [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) |
| [Datta et al. 2019](https://doi.org/10.1016/j.neuron.2019.09.038) | Neuron 104:11-24 | 2019 | Computational neuroethology: a call to action. [DD010](design_documents/DD010_Validation_Framework.md) |
| [Pereira TD et al. 2022](https://doi.org/10.1038/s41592-022-01426-1) | Nat Methods 19:486-495 | 2022 | SLEAP: deep learning system for multi-animal pose estimation. [DD010](design_documents/DD010_Validation_Framework.md) |

---

## Chemotaxis & Sensory Processing

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Pierce-Shimomura et al. 1999](https://doi.org/10.1523/JNEUROSCI.19-21-09557.1999) | J Neurosci 19:9557-9569 | 1999 | Fundamental role of pirouettes in *C. elegans* chemotaxis — biased random walk strategy. [DD022](design_documents/DD022_Environmental_Modeling_and_Stimulus_Delivery.md) |
| [Iino & Yoshida 2009](https://doi.org/10.1523/JNEUROSCI.3633-08.2009) | J Neurosci 29:5370-5380 | 2009 | Parallel use of two behavioral mechanisms for NaCl chemotaxis. [DD022](design_documents/DD022_Environmental_Modeling_and_Stimulus_Delivery.md) |

---

## Anatomy & 3D Atlas

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Long et al. 2009](https://doi.org/10.1038/nmeth.1366) | Nat Methods 6:667-672 | 2009 | 3D nuclear positions atlas (357 nuclei, L1 larva). [DD004](design_documents/DD004_Mechanical_Cell_Identity.md), [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md) |

---

## Neural Circuit Variability & Parameter Fitting

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Prinz et al. 2004](https://doi.org/10.1038/nn1312) | Nat Neurosci 7:1345-1352 | 2004 | Similar network activity from disparate circuit parameters. [FAQ](faq.md) |
| [Achard & De Schutter 2006](https://doi.org/10.1371/journal.pcbi.0020094) | PLoS Comput Biol 2:e94 | 2006 | Complex parameter landscape for a complex neuron model — the solution space approach. [FAQ](faq.md) |
| [Marder & Taylor 2011](https://doi.org/10.1038/nrn3056) | Nat Rev Neurosci 12:563-574 | 2011 | Multiple models to capture the variability in biological neurons and networks. [FAQ](faq.md) |
| [Kawano et al. 2011](https://doi.org/10.1016/j.neuron.2011.09.005) | Neuron 72:572-586 | 2011 | An imbalancing act: gap junctions reduce backward motor circuit activity to bias *C. elegans* for forward locomotion. [DD015](design_documents/DD015_AI_Contributor_Model.md) |

---

## Computational Methods & Machine Learning

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Cannon et al. 2014](https://doi.org/10.3389/fninf.2014.00079) | Front Neuroinform 8:79 | 2014 | LEMS: a language for expressing complex biological models — underpinning NeuroML 2. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md) |
| [Linka et al. 2023](https://doi.org/10.1016/j.actbio.2023.01.055) | Acta Biomater | 2023 | Automated model discovery using constitutive artificial neural networks — RNN approach for inferring biophysical parameters. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md) |
| [Zhao et al. 2024](https://doi.org/10.1038/s43588-024-00738-w) | Nat Comp Sci 4:978-990 | 2024 | MetaWorm: integrative data-driven *C. elegans* brain-body-environment simulation — **key related work**. [Validation](validation.md), [Full History](fullhistory.md#projects-similar-to-openworm), [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD003](design_documents/DD003_Body_Physics_Architecture.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md), [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md), [DD022](design_documents/DD022_Environmental_Modeling_and_Stimulus_Delivery.md) |
| Chen et al. 2018 | NeurIPS 2018 | 2018 | Neural Ordinary Differential Equations — foundational differentiable ODE solvers. [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) |
| Rackauckas et al. 2020 | arXiv:2001.04385 | 2020 | Universal Differential Equations for Scientific Machine Learning — hybrid mechanistic-ML theory. [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) |
| [Jumper et al. 2021](https://doi.org/10.1038/s41586-021-03819-2) | Nature 596:583-589 | 2021 | AlphaFold: highly accurate protein structure prediction — used for ion channel kinetics pipeline. [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) |
| [Lin et al. 2023](https://doi.org/10.1126/science.ade2574) | Science 379:1123-1130 | 2023 | ESM2/ESM3: evolutionary-scale protein structure prediction with a language model. [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) |
| [Kochkov et al. 2024](https://doi.org/10.1038/s41586-024-07744-y) | Nature 632:1060-1066 | 2024 | Neural General Circulation Models for weather and climate — precedent for learned surrogates in physical simulation. [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) |

---

## Philosophical Foundations

| Citation | Journal | Year | Description |
|----------|---------|------|-------------|
| [Machamer et al. 2000](https://doi.org/10.1086/392759) | Philos Sci 67:1-25 | 2000 | Thinking about Mechanisms — biological understanding requires identifying organized systems of entities and activities. [Background](background.md#philosophical-foundations) |
| [Pearl 2000](https://doi.org/10.1017/CBO9780511803161) | Cambridge University Press | 2000 | *Causality: Models, Reasoning, and Inference* — causal models vs. statistical models. [Background](background.md#philosophical-foundations) |
| [Chalmers 2006](https://doi.org/10.1093/acprof:oso/9780199544318.003.0011) | Oxford University Press | 2006 | "Strong and Weak Emergence" — whether higher-level properties are deducible from lower-level laws. [Background](background.md#philosophical-foundations) |
| [Haspel et al. 2023](https://arxiv.org/abs/2308.06578) | arXiv [q-bio.NC] 2308.06578 | 2023 | To reverse engineer an entire nervous system — observational and perturbational completeness. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md), [Background](background.md#philosophical-foundations) |
| Pearl & Mackenzie 2018 | Basic Books (ISBN: 978-0465097609) | 2018 | *The Book of Why: The New Science of Cause and Effect*. [Validation](validation.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD024](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md), [Background](background.md#philosophical-foundations) |
| Rosen 1991 | Columbia University Press (ISBN: 978-0231075640) | 1991 | *Life Itself: A Comprehensive Inquiry Into the Nature, Origin, and Fabrication of Life* — causal loop philosophy. [DD001](design_documents/DD001_Neural_Circuit_Architecture.md) |

---

## Online Datasets & Resources

| Resource | URL | Description | Used In |
|----------|-----|-------------|---------|
| **CeNGEN** | [cengen.org](https://cengen.org) | Single-cell transcriptome atlas of 128 *C. elegans* neuron classes | [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md), [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD010](design_documents/DD010_Validation_Framework.md) |
| **WormAtlas** | [wormatlas.org](https://wormatlas.org) | Anatomical atlas, cell descriptions, EM images, Slidable Worm | [DD004](design_documents/DD004_Mechanical_Cell_Identity.md), [DD007](design_documents/DD007_Pharyngeal_System_Architecture.md), [DD008](design_documents/DD008_Data_Integration_Pipeline.md), [DD014.1](design_documents/DD014.1_Visual_Rendering_Specification.md) |
| **WormBase** | [wormbase.org](https://wormbase.org) | Gene annotation, cell ontology (WBbt), phenotype data | [DD004](design_documents/DD004_Mechanical_Cell_Identity.md), [DD008](design_documents/DD008_Data_Integration_Pipeline.md), [DD014.1](design_documents/DD014.1_Visual_Rendering_Specification.md) |
| **Schafer Lab Database** | [wormbehavior.mrc-lmb.cam.ac.uk](https://wormbehavior.mrc-lmb.cam.ac.uk/) | Behavioral feature database for N2 and mutant strains | [DD010](design_documents/DD010_Validation_Framework.md), [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) |
| **ConnectomeToolbox** | [github.com/openworm/ConnectomeToolbox](https://github.com/openworm/ConnectomeToolbox) | Canonical API for all connectome datasets (`cect`) | [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md), [DD008](design_documents/DD008_Data_Integration_Pipeline.md), [DD010](design_documents/DD010_Validation_Framework.md), [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) |
| **open-worm-analysis-toolbox** | [github.com/openworm/open-worm-analysis-toolbox](https://github.com/openworm/open-worm-analysis-toolbox) | Movement analysis and Tier 3 behavioral validation | [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) |
| **OpenWorm Docker** | [github.com/openworm/OpenWorm](https://github.com/openworm/OpenWorm) | Meta-repository and simulation stack | [DD013](design_documents/DD013_Simulation_Stack_Architecture.md) |
| **AlphaFold Protein Structure Database** | [alphafold.ebi.ac.uk](https://alphafold.ebi.ac.uk) | Predicted protein structures for ion channels | [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) |

---

## How References Are Used

OpenWorm validates its simulation against experimental data at four tiers ([DD010](design_documents/DD010_Validation_Framework.md)):

| Tier | What's Validated | Key Data Sources |
|------|-----------------|------------------|
| **Tier 1** | Single-cell electrophysiology | [Goodman et al. 1998](https://doi.org/10.1016/S0896-6273(00)81014-4), [Goodman et al. 2002](https://doi.org/10.1038/4151039a) (touch neurons), [O'Hagan et al. 2005](https://doi.org/10.1038/nn1362) (MEC-4 channels), [Chalasani et al. 2007](https://doi.org/10.1038/nature06292) (AWC), [Lindsay et al. 2011](https://doi.org/10.1038/ncomms1304) (AVA), Liu et al. 2018 (RIM) |
| **Tier 2** | Circuit functional connectivity | [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) |
| **Tier 3** | Behavioral kinematics | [Yemini et al. 2013](https://doi.org/10.1038/nmeth.2560), [Schafer Lab Database](https://wormbehavior.mrc-lmb.cam.ac.uk/) |
| **Tier 4** | Causal/interventional | [Chalfie et al. 1985](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985), [Pearl & Mackenzie 2018](https://www.hachettebookgroup.com/titles/judea-pearl/the-book-of-why/9780465097616/) |
