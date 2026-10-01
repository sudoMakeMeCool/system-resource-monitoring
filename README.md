# System Resource Monitoring Script

A Python-based system monitoring and browser performance experiment that records system CPU usage and Brave browser activity at one-second intervals.

The project was created to study the performance overhead of browser extensions such as **Dark Reader** across webpages with different rendering and workload characteristics.

## Overview

The monitoring script uses `psutil` to record:

- Overall system CPU usage
- Brave browser CPU usage
- Number of active Brave processes
- Experiment timestamp
- Dark Reader ON/OFF state

The collected measurements are written to CSV files for later analysis.

A separate plotting script processes the experiment data and generates a comparison chart of average CPU usage across different webpage workloads.

## Project Structure

```text
SYS PERFORMANCE/
│
├── data/
│   ├── performance_static.csv
│   ├── performance_longtext.csv
│   ├── performance_longcolor.csv
│   ├── performance_dom_explosion.csv
│   └── performance_color_mutation_storm.csv
│
├── results/
│   ├── resource_comparison.png
│   ├── static_page_colorblock_scrolling.png
│   ├── static_page_div_color_scrolling.png
│   ├── static_page_divs_color_changing_noise.png
│   ├── static_page_no_scrolling.png
│   └── static_page_scrolling.png
│
├── workloads/
│   ├── test.html
│   ├── long_test.html
│   ├── long_test.html
│   ├── dom_explosion_divs.html
│   └── color_mutation_storm.html
│
├── performance.py
├── performance_plot.py
├── requirements.txt
└── README.md