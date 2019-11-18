# Comparability in Non-Intrusive Load Monitoring

This repository contains source code as well as supplemental material related to our research paper *Towards Comparability in Non-Intrusive Load Monitoring: On Data and Performance Evaluation*. You are free to use, copy, and distribute this code. In any case, we ask you to cite our paper and to make a reference to this repository.

[Download the research paper here.](http://makonin.com/doc/ISGT-NA_2020b.pdf)

* Title: Towards Comparability in Non-Intrusive Load Monitoring: On Data and Performance Evaluation
* Authors: Christoph Klemenjak, Stephen Makonin, and Wilfried Elmenreich
* Conference: 2020 IEEE Power & Energy Society Innovative
Smart Grid Technologies Conference (ISGT)

Recommended Citation:

```
@INPROCEEDINGS{klemenjak2020comparability,
author={Klemenjak, Christoph and Makonin, Stephen and Elmenreich, Wilfried},
booktitle={2020 IEEE Power \& Energy Society Innovative Smart Grid Technologies Conference (ISGT)},
title={Towards Comparability in Non-Intrusive Load Monitoring: On Data and Performance Evaluation},
year={2020},
organization={IEEE}}
```

## NAR - How noisy is a dataset?

The aggregate power signal of a real-world dataset consists not exclusively of known appliance-level signals, but also contains several unknown appliance-level signals that contribute to the error term epsilon (noise). To quantify the amount of noise of an aggregate power signal, we introduce the Noise-to-Aggregate Ratio, NAR, which is defined as:

![NAR](img/NAR.png)

Find more information and a usage note in the [[Jupyter Notebook].](NAR.ipynb)

### NAR in some common energy consumption data sets

We derived the NAR with respect to active and apparent power for some of the most commonly-used energy consumption data sets. Please note that our focus is on their *low-frequency* version.

| Data Set | House | Duration in days | Meters | NAR for P in \%| NAR for S in \%|
|----------|-------:|------------------:|--------:|-----------:|-----------:|
| AMPds 2  |  1    | 730              |   20     |     18      |   6       |
| COMBED   |  1    |  28              |   13    |    34        |    -    |
| DRED     |  1    |  153             |   12     |   -       |     28    |
| ECO      |  1    |  245             |   7     |    68        |     -      |
| ECO      |  6    |  219             |   7     |    74        |   -        |
| iAWE     |  1    |  73              |   10     |   63        |     61      |
| REDD     |  1    |  36                |   16     |  -     |    -        |
| REFIT    |  1    |  638              |    9    |     65      |   -       |
| REFIT    |  8    |  555                |  9      |   78      |    -        |
| REFIT    |  17   |  443             |     9   |      45      |   -       |
| UK-DALE  |  1    |  658              |    52    |    33      |    87       |
| UK-DALE  |  2    |  176             |     18   |     41      |  -       |
| UK-DALE  |  5    |  137             |     24   |     31      |   -       |


## Estimating the number of events in common NILM datasets

We hypothesise that the number of events has a considerable impact on the performance of load disaggregation algorithms since a high number of observed events would reflect a vibrant household. In this context, we define an event to be the transition between two representative states of power consumption. These representative states are obtained by applying methods of statistics, filtering, and clustering:

1. We apply a *median filter* to the signal to fight noise
2. We estimate the number of states by deriving *basic statistics* of the time series
3. We run *k-means clustering* to identify representative appliance states (building on insights from point 2)
4. We *quantise the time series* and count the number of transitions between appliance states

Besides duration of measurement campaigns and installed meters, we report:

1. The *minimum number of events per day*, which states the average number of events of the least-active appliance in a household i.e. appliance with the least events
2. The *average number of events per house*, which states the average number of events of a household per day. In some way, this average provides insights about how vibrant the household is i.e. how much appliances are being used.

| Data Set | House | Duration in days | Meters | Minimum Number of Events per Day | Average Number of Events per House |
|---------|------:|-----------------:|-------:|-----------------:|-----------------:|
| AMPds2  |  1    | 730              |   20     |   0        |   319      |
| COMBED   |  1    |  28              |   13    |     0       |   463   |
| DRED     |  1    |  153             |   12     |    1      |    604   |
| ECO      |  1    |  245             |   7     |      7      |   691      |
| ECO      |  6    |  219             |   7     |      1      |   1166         |
| iAWE     |  1    |  73              |   10     |     1      |   497     |
| REDD     |  1    |  36                |   16     |   0     |    799    |
| REFIT    |  1    |  638              |    9    |     1      |   320       |
| REFIT    |  8    |  555                |  9      |   3      |   229        |
| REFIT    |  17   |  443             |     9   |      1      |   379       |
| UK-DALE  |  1    |  658              |    52    |    0      |   874    |
| UK-DALE  |  2    |  176             |     18   |     0      |   733      |
| UK-DALE  |  5    |  137             |     24   |     0      |   1320       |


## Testset ratio (TSR): How extensively are we testing?

In our research paper, we discuss several aspects related to performance evaluation. One of them concerns testsets.
In order to obtain conclusive results in performance evaluation, NILM algorithms have to be tested on a sufficiently large amount of data. However, we can observe large variations in related work spanning from a few days up to several months of test sets.
We identify the need for a simple measure that gives information on how extensively testing was performed on a dataset.
We suggest reporting the amount of data used for evaluation to get an idea of how many events were embedded in the test set.
To quantify this property, we propose the \emph{test set ratio (TSR)} and the \emph{event ratio (EVR)}, which are defined as

![TSR](img/TSR.png)

the ratio between test duration and the total duration of a time series for energy estimation purposes and the ratio between the number of events in the test set and the total number of events in the dataset. In case of a significant amount of missing data intervals, e.g., a measurement that goes over a year and is missing a month, the duration will be calculated as the aggregation of of all sub-durations.

With these metrics, we are able to put into relation evaluation results and test set size.

**[IN 1]**
```python
# Sample Code: a naive implementation of TSR for NILMTK
from nilmtk import DataSet

def get_duration(data_frame):
    end = data_frame.index[-1].to_pydatetime()
    start = data_frame.index[0].to_pydatetime()
    duration = end - start
    return duration.days + round(duration.seconds/(3600*24), 2)

def test_set_ratio(elec, test_elec):
    total_duration = get_duration(elec.mains().power_series_all_data())
    test_duration = get_duration(test_elec.mains().power_series_all_data())
    return round(100*test_duration / total_duration, 2)

d_dir = '/Users/christoph/datasets/'

data_set = DataSet(d_dir+'{}.h5'.format('iAWE'))
test_set = DataSet(d_dir+'{}.h5'.format('iAWE'))

test_set.set_window(start='2013-07-01', end='2013-08-01')

elec = data_set.buildings[1].elec
test_elec = test_set.buildings[1].elec

print('TSR equals: {} %'.format(test_set_ratio(elec, test_elec)))
```
**[OUT 1]**

```python
Loading data for meter ElecMeterID(instance=2, building=1, dataset='iAWE')     
Done loading data all meters for this chunk.
Loading data for meter ElecMeterID(instance=2, building=1, dataset='iAWE')     
Done loading data all meters for this chunk.

TSR equals: 42.09 %
```
Please note that this is a very simple implementation that serves only to support our point.
