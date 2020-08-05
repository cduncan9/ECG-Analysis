# Electrocardiogram Project [![Build Status](https://travis-ci.com/BME547-Summer2020/ecg-analysis-cduncan9.svg?token=RLd1CpbXx8eP2MxfSyyp&branch=master)](https://travis-ci.com/BME547-Summer2020/ecg-analysis-cduncan9)
---
### Using This Program
This program is very simple and user friendly. Using the computer terminal, navigate to the folder containing the python module ecg_analysis. Start running the module ecg_analysis. You will be prompted to enter the name of the file containing the ECG time and voltage data. This software only works with '.csv' files, so ensure that you have your data in the correct file type. Enter the name of the '.csv' file and hit enter. The rest of the ECG analysis works behind the scenes and requires no further user input. The output of this software is located in a JSON file which is saves with the same name as the input data file except with '.json' as the file extension. Contained within this file are the ECG metrics `beats`, `mean_hr_bpm`, `voltage_extremes`, `num_beats`, and `duration` which are all described in the following section. 
### ECG Metrics Calculated
This program provides an analysis of ECG data contained within a CSV file. The two parameters contained within the CSV file are time and voltage points which represent the electric pulses occuring within the heart. From the time and voltage data the following ECG metrics are calculated:

* `duration`: The time period that the ECG data spans
* `voltage_extremes`: The max and min of the voltage data
* `num_beats`: The number of heart beats that occur over the data
* `mean_hr_bpm`: The average heart rate over the data
* `beats`: A list of time points that corresponds to heart beats

### Locating Heart Beats
Several of these metrics require knowledge of when the heart beats occur in the ECG data. The voltage points which are considered to be heart beats in this software are found in three steps. First, all of the points in the voltage data that have magnitudes greater than half of the maximum voltage point are stored in a list. Each heart beat has several data points that are above half of the max value and are thus stored. Then the values in this list are grouped into smaller lists that represent the heart beats by grouping similar time values. Finally the median value of each of these smaller lists is selected to be the point for that heart beat, and this data point is stored into a list that contains all of the heart beats for a data set.

### Calculating Mean Heart Rate
One of the metrics that this program calculates is the mean heart rate for a data set in beats-per-minute. This is done by first finding the metric `beats`, which gives the time points that correspond to heart beats. The list contained in the metric `beats` is used to create another list that contains the time between each beat in the ECG data. Then each time period in this list is plugged into the following equation to get a list of heart rates:

$$beats per minute = \frac{1}{period between heart beats} * 60$$

Then the average of this list of heart rates is found and used as the mean heart rate.
### Software Liscensing
MIT License

Copyright (c) 2020 Canyon Duncan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
