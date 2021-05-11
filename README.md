# Flexible Table Recognition and Semantic Interpretation System
This repository contains the resources from our table interpretation experiment that were presented in our paper: "**Flexible Table Recognition and Semantic Interpretation System**", which was submitted to the [GCPR 2021](dagm-gcpr.de) conference.

## Background

`**TODO**: explain table interpretation`

## Project Structure

The structure of the project is as follows:

```
.
├── eval_interpretation.py
├── README.md
├── requirements.txt
├── gt
│   ├── 01_page04_table0.json
│   ├── ...
│   └── 13_page10_table1.json
└── res
    ├── 01_page04_table0.json
    ├── ...
    └── 13_page10_table1.json
```

* [eval_interpretation.py](./eval_interpretation.py) - the Python evaluation script.
* [README.md](./README.md) - this readme file.
* [requirements.txt](./requirements.txt) - Python packages required to run the evaluation script.
* [gt](./gt) - ground-truth annotations containing relevant tuples of information that need to be extracted.
* [res](./res) - the tuples extracted by our table interpretation method. 

## Quick Start

### Prerequisites

1. Please install the python packages as shown below:

```shell
pip install -r requirements.txt
```

## Using the script

To execute the script with default configuration just call:

```shell
python3 eval_interpretation.py
```

The last line of the output produced by the script contains the final information extraction scores, e.g., in the case of the results produced by our method:

```
TP:69 FP:4 FN:45 PRECISION=0.9452 RECALL=0.6053 F1=0.7380
```

where `TP`,`FP`,`FN` indicate the number of true-positive, false-positive, and false-negative relations, respectively.

The script calculates the scores of the end-to-end table extraction process by default. In order to switch to the calculation solely from the correctly recognized tables, you need to set the following line in the code:

```py
include_missed_tables = False
```

The script should then produce the following output:

```
TP:69 FP:4 FN:5 PRECISION=0.9452 RECALL=0.9324 F1=0.9388
```

## Data Set 

### Annotations

The ground-truth annotations containing the lists of tuples of relevant information are provided in this repository. The name pattern of the ground-truth and the recognized files is as follows:

```
<FILE_ID>_<PAGE_NR>_<TABLE_IDX>.json
```
where `<FILE_ID>` is the file identifier (see the explanation in [Data Set](README.md#data-set)), `<PAGE_NR>` is the page number in the PDF file, and `<TABLE_IDX>` is the index of a table on a page (starting from "0").

### PDF Files

The PDF files containing the tables with the tuples of information that has been extracted in our experiments can be downloaded from the below listed locations. The numbers in the square brackets indicate the `FILE_IDs` of each PDF file, which are used to identify and match the gold and the recognized sets of tuples.

#### Evaluation Set

We fed the following PDF files to our table extraction system for evaluation:

[01] Asfaha, Y., Schrenk, C., Alves Avelar, L. A., Lange, F., Wang, C., Bandolik, J. J., Hamacher, A., Kassack, M. U., & Kurz, T. (2020). Novel alkoxyamide-based histone deacetylase inhibitors reverse cisplatin resistance in chemoresistant cancer cells. Bioorganic & medicinal chemistry, 28(1), 115108. https://doi.org/10.1016/j.bmc.2019.115108

[02] Basso, M., Chen, H. H., Tripathy, D., Conte, M., Apperley, K., De Simone, A., Keillor, J. W., Ratan, R., Nebbioso, A., Sarno, F., Altucci, L., & Milelli, A. (2018). Designing Dual Transglutaminase 2/Histone Deacetylase Inhibitors Effective at Halting Neuronal Death. ChemMedChem, 13(3), 227–230. https://doi.org/10.1002/cmdc.201700601

[03] Chen, J., Sang, Z., Jiang, Y., Yang, C., & He, L. (2019). Design, synthesis, and biological evaluation of quinazoline derivatives as dual HDAC1 and HDAC6 inhibitors for the treatment of cancer. Chemical biology & drug design, 93(3), 232–241. https://doi.org/10.1111/cbdd.13405

[04] Kassab, S. E., Mowafy, S., Alserw, A. M., Seliem, J. A., El-Naggar, S. M., Omar, N. N., & Awad, M. M. (2019). Structure-based design generated novel hydroxamic acid based preferential HDAC6 lead inhibitor with on-target cytotoxic activity against primary choroid plexus carcinoma. Journal of enzyme inhibition and medicinal chemistry, 34(1), 1062–1077. https://doi.org/10.1080/14756366.2019.1613987

[05] Sharma, C., Oh, Y. J., Park, B., Lee, S., Jeong, C. H., Lee, S., Seo, J. H., & Seo, Y. H. (2019). Development of Thiazolidinedione-Based HDAC6 Inhibitors to Overcome Methamphetamine Addiction. International journal of molecular sciences, 20(24), 6213. https://doi.org/10.3390/ijms20246213

[06] Miao, H., Gao, J., Mou, Z., Wang, B., Zhang, L., Su, L., Han, Y., & Luan, Y. (2019). Design, synthesis and biological evaluation of 4-piperidin-4-yl-triazole derivatives as novel histone deacetylase inhibitors. Bioscience trends, 13(2), 197–203. https://doi.org/10.5582/bst.2019.01055

[07] Lv, W., Zhang, G., Barinka, C., Eubanks, J. H., & Kozikowski, A. P. (2017). Design and Synthesis of Mercaptoacetamides as Potent, Selective, and Brain Permeable Histone Deacetylase 6 Inhibitors. ACS medicinal chemistry letters, 8(5), 510–515. https://doi.org/10.1021/acsmedchemlett.7b00012

[08] Zhang, Y., Yan, J., & Yao, T. P. (2017). Discovery of a fluorescent probe with HDAC6 selective inhibition. European journal of medicinal chemistry, 141, 596–602. https://doi.org/10.1016/j.ejmech.2017.10.022

[09] Negmeldin, A. T., Knoff, J. R., & Pflum, M. (2018). The structural requirements of histone deacetylase inhibitors: C4-modified SAHA analogs display dual HDAC6/HDAC8 selectivity. European journal of medicinal chemistry, 143, 1790–1806. https://doi.org/10.1016/j.ejmech.2017.10.076

[10] Reßing, N., Marquardt, V., Gertzen, C., Schöler, A., Schramm, A., Kurz, T., Gohlke, H., Aigner, A., Remke, M., & Hansen, F. K. (2018). Design, synthesis and biological evaluation of β-peptoid-capped HDAC inhibitors with anti-neuroblastoma and anti-glioblastoma activity. MedChemComm, 10(7), 1109–1115. https://doi.org/10.1039/c8md00454d

[11] Choi, M. A., Park, S. Y., Chae, H. Y., Song, Y., Sharma, C., & Seo, Y. H. (2019). Design, synthesis and biological evaluation of a series of CNS penetrant HDAC inhibitors structurally derived from amyloid-β probes. Scientific reports, 9(1), 13187. https://doi.org/10.1038/s41598-019-49784-9

[12] Debnath, S., Debnath, T., Bhaumik, S., Majumdar, S., Kalle, A. M., & Aparna, V. (2019). Discovery of novel potential selective HDAC8 inhibitors by combine ligand-based, structure-based virtual screening and in-vitro biological evaluation. Scientific reports, 9(1), 17174. https://doi.org/10.1038/s41598-019-53376-y

[13] Xia, J., Hu, H., Xue, W., Wang, X. S., & Wu, S. (2018). The discovery of novel HDAC3 inhibitors via virtual screening and in vitro bioassay. Journal of enzyme inhibition and medicinal chemistry, 33(1), 525–535. https://doi.org/10.1080/14756366.2018.1437156

#### Development Set

We used the following PDF files to tune the hyper-parameter for our method:

[14] Kozikowski, A. P., Shen, S., Pardo, M., Tavares, M. T., Szarics, D., Benoy, V., Zimprich, C. A., Kutil, Z., Zhang, G., Bařinka, C., Robers, M. B., Van Den Bosch, L., Eubanks, J. H., & Jope, R. S. (2019). Brain Penetrable Histone Deacetylase 6 Inhibitor SW-100 Ameliorates Memory and Learning Impairments in a Mouse Model of Fragile X Syndrome. ACS chemical neuroscience, 10(3), 1679–1695. https://doi.org/10.1021/acschemneuro.8b00600

[15] Lee, H. Y., Fan, S. J., Huang, F. I., Chao, H. Y., Hsu, K. C., Lin, T. E., Yeh, T. K., Lai, M. J., Li, Y. H., Huang, H. L., Yang, C. R., & Liou, J. P. (2018). 5-Aroylindoles Act as Selective Histone Deacetylase 6 Inhibitors Ameliorating Alzheimer's Disease Phenotypes. Journal of medicinal chemistry, 61(16), 7087–7102. https://doi.org/10.1021/acs.jmedchem.8b00151

[16] Stenzel, K., Hamacher, A., Hansen, F. K., Gertzen, C., Senger, J., Marquardt, V., Marek, L., Marek, M., Romier, C., Remke, M., Jung, M., Gohlke, H., Kassack, M. U., & Kurz, T. (2017). Alkoxyurea-Based Histone Deacetylase Inhibitors Increase Cisplatin Potency in Chemoresistant Cancer Cell Lines. Journal of medicinal chemistry, 60(13), 5334–5348. https://doi.org/10.1021/acs.jmedchem.6b01538

[17] Yu, C. W., Hung, P. Y., Yang, H. T., Ho, Y. H., Lai, H. Y., Cheng, Y. S., & Chern, J. W. (2019). Quinazolin-2,4-dione-Based Hydroxamic Acids as Selective Histone Deacetylase-6 Inhibitors for Treatment of Non-Small Cell Lung Cancer. Journal of medicinal chemistry, 62(2), 857–874. https://doi.org/10.1021/acs.jmedchem.8b01590

