# Data Analysis in Sports
## Project Overview

## Data Collection

Data are collected and parsed using the `scraper.py`:

- **Source Fetching**  
  - Crawls the ISU results portal (`URL_TEMPLATE`) with `requests` and `BeautifulSoup`  
  - Gathers all PDF links for short program, free skate/dance, and team events  

- **Parallel Download**  
  - Downloads each PDF concurrently via `ThreadPoolExecutor`  
  - Skips known non-entry-list files and logs any download errors  

- **PDF Extraction & Parsing**  
  - Opens each PDF with `pdfplumber`, concatenates page text, and normalizes whitespace  
  - Identifies segments (e.g. “Short Program”, “Free Skating”, “Rhythm Dance”, “Free Dance”) and categories (Men’s, Women’s, Pairs, Ice Dance, Team) by filename pattern  
  - Uses regular expressions to split and extract:  
    - **Skater metadata** (rank, names, NOC, scores, deductions)  
    - **Executed elements** (element number, name, base value, GOE, individual judge scores)  
    - **Program components** (component name, factor, individual judge scores)  

- **Data Assembly & Output**  
  - Aggregates parsed records into three pandas DataFrames:  
    - `skaters.xlsx`  
    - `executed_elements.xlsx`  
    - `program_components.xlsx`  
  - Saves each table to the `data/` folder and logs completion status  

This pipeline ensures repeatable, automated collection of structured figure-skating results for downstream analysis.```

## Data Description
The raw data for this repository is organized into three related tables—skaters, executed_elements, and program_components—each capturing a different aspect of the competition scoring process.
### 1. Skaters (243 records)
Each row represents one skater’s performance in a given segment. Key fields include:
* skater_id: Unique alphanumeric identifier for each skater.
* rank: Final placement in the segment (integer).
* skater_name_1, skater_name_2: Given name and family name of the skater.
* noc: Three-letter National Olympic Committee code (e.g., USA, JPN).
* starting_number: Order in which the skater took the ice.
* segment: Type of segment (e.g., “Short Program”, “Free Skate”).
* category: Discipline category (e.g., “Men’s Singles”, “Ice Dance”).
* total_segment_score: Sum of all element and component scores minus deductions.
* total_element_score: Aggregate of all executed element scores.
* total_program_component_score: Sum of all program component evaluations.
* total_deductions: Penalty points subtracted (falls, time violations, etc.).
### 2. Executed Elements (2 072 records)
Details every individual technical element attempted by skaters. Each row corresponds to one element execution:
* element_number: Position of the element within the program sequence.
* element_name: Standard notation for the jump, spin, or step.
* info_symbol: Additional technical annotation.
* base_value: Assigned base score for the element difficulty.
* x_symbol: Marker for “x” - credit for highlight distribution, base value multiplied by 1.1.
* goe: Total Grade of Execution awarded (sum of judge GOEs).
* judge_1 … judge_9: Individual GOE scores from each of the nine judges.
* total_score: Base value plus GOE (and any adjustment factors).
* component_type: Type classification.
* skater_id: Foreign key linking back to the skaters table.
### 3. Program Components (1 215 records)
Captures the nine program component marks for each skater’s segment:
* component_type: Category of component (e.g., “Skating Skills”, “Performance”).
* element_name: Full name of the component.
## Data Analysis (figure_skating.ipynb)

A data analysis was performed on the three tables—**skaters**, **executed_elements**, and **program_components**—to understand score distributions, judge behaviors, and relationships between technical and component marks:

**Descriptive Statistics**  
- Generated summary statistics (mean, median, standard deviation, min/max) for numeric fields:  
  - `total_segment_score`, `total_element_score`, `total_program_component_score`  

- **Gender Comparison**  
  Histograms and violin plots show women generally score lower than men in both Free Skate and Short Program; cross-gender comparisons confirm larger score gaps in most countries.

- **Country-Level Distributions**  
  Violin plots of Short Program scores highlight top men’s performers from USA, JPN, KOR and women’s performers from RUS, JPN, KOR, with notably wider score ranges for KOR and CAN. Free Skate distributions rank men: USA, JPN, ITA and women: RUS, JPN, KOR.

- **Start Order Effects**  
  Scatter plots reveal a weak positive trend between start order and total score in Free Skate (especially women) and a subtler upward trend in men’s Short Program.

- **Penalty (Falls) Impact**  
  Negative correlation between number of falls and Free Skate score; this trend is absent or minimal in Ice Dance.

- **Segment Comparison**  
  Across all disciplines, Free Skate yields higher average scores than Short Program, with men’s events exhibiting higher absolute values.

- **Element Complexity vs GOE**  
  Simpler elements (base ≤ 8) are executed more cleanly (positive GOEs) and more frequently; mid-difficulty elements (8–12) show uniform GOE spread; high-difficulty elements (≥ 12) are rarer but often executed with positive GOE.

- **Country Discipline Performance**  
  Grouped bar charts reveal some countries excel in specific disciplines (e.g., one country leads in Ice Dance but trails in Singles).

- **Complexity vs Execution Quality by Segment and Gender**  
  In both segments and for both genders, higher average base values generally align with higher average GOEs, though some skaters achieve high GOE on lower-value elements, indicating exceptional execution.
