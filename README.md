# ismartcsv
### A smart way to work with any character seperated valued datafile. 
___ 

Just declare all the configurations required to read, operate, write in a seperate yaml config file with self explaining fields. This config file is one-time defined config file that works for all the input data files of any particular format or any particular scientific instrument.

#### when we have other python libraries serving the similar purpose, Why use ismartcsv ?

_**smaller learning curve**_


#### What makes ismartcsv so special, let's talk about features and capabilities !!

**_same method calls for different modes_**

_**interpolation**_

_**Basic plotting**_

_**facility to export data to multiple standard data formats**_

#### what should I know before using ismartcsv module ?

This is a python module, especially meant for working with scientific instrument generated csv data. We expect you to have basic knowledge of writing python scripts, better understanding of import system in python, using numpy and plotting.


### Using the module.

#### Disclaimer while working with datafile

**TBD**

#### Disclaimer while working with datafolder

**TBD**

##### Important sections of configuration file

The fields declared in the config file convey a special information essential for the code-engine to understand about the skeleton and behaviour of input datafile.

detailed explanation of the different config field names and their effect on execution is provided below

let's consider, I have a csv data with filename ```uvwD20251009T220158.csv``` with the given headers and sample data

```text

Height(kms),U(mps),V(mps),W(mps),WD(deg),Z_snr(db),Z_dop
1.5,-7.6,0.56,0.24,94.21,-14.54,-0.08
1.65,-0.71,-5.14,0.13,7.81,-2.02,-0.04
1.8,-0.05,-0.3,0.05,8.6,13.93,-0.02
1.95,0.33,-0.34,0.06,315.49,17.2,-0.02
2.1,0.03,-0.29,0.07,354.36,18.48,-0.03
2.25,-0.13,0.01,0.07,92.72,16.3,-0.03
2.4,-0.16,-0.28,0.16,29.51,15.85,-0.06
2.55,-0.2,-0.39,0.26,27.23,16.32,-0.09
2.7,-0.36,-0.48,0.31,36.79,20.56,-0.11
2.85,-0.05,0.46,0.3,173.77,21.89,-0.11

```

lemme dissect the above csv data and write the ismartcsv configuration file. we need to take point out few important things before proceeding further.

- the delimiter( values seperating character ) is comma (```,```)
- lines after which the data starts( i.e., including header )
- Number of fields inclusive for reading (you dont have to include all fields for reading)
- python datetime formatting specifiers represented for filename.
- the field names you want i


#### Important sections of configuration file

**```fields```** config section declares ismartcsv module to read the numbered columns and store that parsed data into a variable of provided field name.

**```interpolate```** config section is used by ismartcsv to pivot a particular input field for interpolation. the values of field name specified as pivot, should be either monotonically increasing or decreasing.

**```output```** config section is used by ismartcsv while creating a output file from the processed data.

**```plot```** config section specifies how and what to plot when plotting action invoked. 

```yaml

delimiter: ","
skip_lines: 1
field_count: 7
filename_format: "uvwD%Y%m%dT%H%M%S.csv"
datetime_format: null
timestamp_in_filename: true


# ftype can be 'int', 'float', 'datetime'

fields:
    - name: "height"
      colno: 1
      ftype: float
      factor: 1
      ifnull: null
      nullval: null
      label: 'Height'
      units: 'km'

    - name: "u"
      colno: 2
      ftype: float
      factor: 1
      ifnull: null
      nullval: null
      label: 'Zonal Wind'
      units: 'm/s'

    - name: "v"
      colno: 3
      ftype: float
      factor: 1
      ifnull: null
      nullval: null
      label: 'Meridional Wind'
      units: 'm/s'

    - name: "w"
      colno: 4
      ftype: float
      factor: 1
      ifnull: null
      nullval: null
      label: 'Vertical Wind'
      units: 'm/s'

    - name: "wd"
      colno: 5
      ftype: float
      factor: 1
      ifnull: null
      nullval: null
      label: 'Wind Direction'
      units: 'deg'

    - name: "zsnr"
      colno: 6
      ftype: float
      factor: 1
      ifnull: null
      nullval: null
      label: 'Zenith SNR'
      units: 'dB'

    - name: "zdop"
      colno: 7
      ftype: float
      factor: 1
      ifnull: null
      nullval: null
      label: 'Zenith'
      units: 'TBD'

interpolation:
  pivot: "height"
  
  ## meta data need to folder reading
  start: 2
  stop: 20
  step: 0.15

output: 
  fields: ["height", "u", "v", "w"]

plot:
  file:
    - type: line
      xaxis: null
      yaxis: 'height'
      title: 'file sample'
      fields: ["u", "v", "w", "wd", "zsnr", "zdop"]

    - type: line
      xaxis: 'height'
      yaxis: null
      title: 'another file sample'
      fields: ['u', 'v', 'w', 'wd', 'zsnr', 'zdop']
  

  folder:
    - type: 'line'
      xaxis: null
      yaxis: height
      title: 'Line Plot'
      fields: ["u", "v", "w"]

    - type: 'contour'
      xaxis: 'filestamp'
      yaxis: 'height'
      title: 'contour plot'
      fields: ["u", "v", "w", "wd"]

    - type: 'contour'
      xaxis: 'filestamp'
      yaxis: 'height'
      title: 'sample contour plot'
      fields: ['u', 'v']

parsers:
  datetime: DATETIME_PARSER
  filename: FILENAME_PARSER

encoders:
  datetime: DATETIME_ENCODER
  filename: FILENAME_ENCODER

```


#### Tool and libraries used

see the content of requirements.txt file for libraries and modules used

#### what can be done
