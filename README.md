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
