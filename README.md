# Data Analysis in Sports
## Project Overview

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
## Exploratory Data Analysis (EDA)

A comprehensive EDA was performed on the three tables—**skaters**, **executed_elements**, and **program_components**—to understand score distributions, judge behaviors, and relationships between technical and component marks:

**Descriptive Statistics**  
- Generated summary statistics (mean, median, standard deviation, min/max) for all numeric fields:  
  - `total_segment_score`, `total_element_score`, `total_program_component_score`, `total_deductions` (skaters table)  
  - `base_value`, `goe`, `total_score` (executed_elements table)  
  - `total_score`, `factor` (program_components table)  
- Identified a handful of extreme outliers in element GOE (±5+) and segment deductions (>3), which were flagged for manual review.

**Univariate Analysis**  
- **Histograms** for `total_segment_score`, `total_element_score`, and `total_program_component_score` revealed left-skew in component scores but right-skew in element and segment scores.  
- **Density plots** for `base_value` showed bi-modal peaks corresponding to jump vs. spin/step elements.  
- **Boxplots** for each judge’s GOE and component marks (`judge_1`…`judge_9`) highlighted a slight upward bias in judges 5–7 compared to judges 1–4 and 8–9.

**Categorical Distributions**  
- **Bar charts** of `segment` (“Short Program” vs. “Free Skate”) and `category` (“Men’s Singles”, “Ladies’ Singles”, “Pairs”, “Ice Dance”) showed a roughly even split across segments but a higher frequency of Men’s and Ladies’ events.  
- **Countplots** of `component_type` in executed elements (“Jump”, “Spin”, “Step Sequence”) confirmed jumps account for ~45% of all elements attempted.

**Bivariate Relationships**  
- **Scatter plots** of `total_element_score` vs. `total_program_component_score` uncovered a moderate positive correlation (ρ≈0.6), reinforcing that stronger technical performances often coincide with stronger components.  
- **Heatmap** of Pearson correlations among all numeric features (scores, GOEs, deductions) guided the removal of highly collinear variables (e.g., overall GOE vs. summed GOE).

**Country-Level and Judge Analysis**  
- **Boxplots** of `total_segment_score` by `noc` illustrated that the top five NOCs (e.g., JPN, USA, RUS) had both higher medians and tighter score distributions.  
- **Heatmaps** of average GOE per judge across all skaters uncovered subtle inter-judge variability, prompting a small adjustment in later modeling to normalize judge biases.

After filtering out any records with missing `skater_id` or invalid GOE entries, these EDA insights informed feature selection, outlier treatment, and normalization steps for all downstream modeling.```

* judge_1 … judge_9: Individual component scores from each judge.
* total_score: Sum of the nine judges’ marks.
* factor: Scaling multiplier applied to arrive at the final component score.
* skater_id: Foreign key linking back to the skaters table.

