# What

A workspace for generating some charts for performance metrics. Part of a performance report we are doing for the 2025 Rafiki work week.

I recorded a bunch of performance metrics in google sheets but found the google sheets charts too tedious to use (the way I recorded was also not optimized for plotting). So I am using this workspace to generate some charts. The google sheets were exported to `./data` as cvs.

# Data

There are both empty and `NA` values in the csvs. NA means the VUs were observed for that category (2024 remote, etc.) but not reported (or it could safely be assumed it wouldnt report, because the previous didnt). Empty cells mean that I did not observe the performance at these VUs (primarily because they failed to report TPS so I didnt need to measure). Im unsure how I want to handle this - perhaps all should be treated as 0, or just terminate the line. Just preserving this detail so I can decide as needed.

The source data for the x axis (VUs) do not have a fixed step. They were a product of essentially a binary search for the max VUs. 1,5,7,10,20,40,80, wait 80 is too high, lets gog back to 60. etc. This poses some issues with displaying the data. I experimented with a few different ways of handling this one the x axis.

- super naive: just use it directly. The datapoints are not discernable on the low end, nor the labels.
- slightly less naive but still bad: derive labels from the data with a fixed step and display the data as-is. The labels are fine but the data looks the same as the previous method (unreadable)
- using a log scale. This is the best solution I found. As this article says, a logarithmic axes works well when the data spans several orders of magnitude. https://www.geeksforgeeks.org/python/how-to-plot-logarithmic-axes-in-matplotlib/

# How to run

Install [Poetry](https://python-poetry.org/), then run `poetry install` and `poetry run python main.py`.
