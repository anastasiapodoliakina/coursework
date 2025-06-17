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
* judge_1 … judge_9: Individual component scores from each judge.
* total_score: Sum of the nine judges’ marks.
* factor: Scaling multiplier applied to arrive at the final component score.
* skater_id: Foreign key linking back to the skaters table.

