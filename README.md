
---
# AutoRPT: Automatic Rapid Prosody Transcription Tool

**AutoRPT** is a Python command-line tool designed to automatically annotate prosodic features following the Rapid Prosody Transcription (RPT) protocol. It is currently trained on Standard American English (SAE), with future updates planned to include other language varieties.

### About the Project

This project is being developed by a team of undergraduate and graduate students, led by **PI Associate Professor Jonathan Howell** at **Montclair State University**. It is produced in conjunction with research funded by **NSF grant 2316030**, focusing on identifying the prosodic features of **“Three Varieties of English in NJ”**. The tool is designed to streamline the annotation of prosodic events using **Rapid Prosodic Transcription (RPT)**, as outlined by **Cole et al. (2017)**.

### Two Versions

There is both an AutoRPT and an AutoRPT_LSTM folder. The AutoRPT folder runs on a Recurrent Neural Network (RNN) framework and is more focused on the automatic annotation of prosodic events. The LSTM folder runs a Long Short-Term Memory (LSTM) framework and is more focused on the bootstrapping of annotations so that they can be reviewed by human annotators.

### Why We Built This Tool

1. **Limited Corpora for Specific Varieties**: Few corpora (with the exception of **CORAAL**) include **African American English (AAE)** and **Latinae English (LE)**.
2. **Lack of Prosodic Annotations**: Even fewer corpora provide prosodic annotations for these varieties of English.
3. **Incomplete Annotation Schemes**: Current annotation schemes often do not account for the unique prosodic features of AAE and LE.
4. **Challenges in Crowdsourcing**: Annotating prosody through crowdsourcing methods can be difficult and inconsistent.

### Corpus and Training

AutoRPT is currently trained on the **Boston University Radio Corpus**, which serves as the foundation for the tool’s prosodic annotations. As research progresses, the model will be adapted to annotate prosodic features in other varieties of English, including those spoken in New Jersey.

### Prosodic Event Annotation and Detection in Three Varieties of English

AutoRPT is part of ongoing research into the detection of prosodic events across the following varieties:

- **Mainstream American English (MAE)**
- **African American English (AAE)**
- **Latine English (LE)** (as spoken in New Jersey)

---

## Installation Instructions

To run AutoRPT, you'll need to install several Python libraries. Follow the steps below to set up the tool on your system.

### Prerequisites

1. Ensure that you have Python version 3.7 or higher. You can download the latest version of Python [here](https://www.python.org/downloads/).
2. Download and unzip a copy of the repo.
3. It is recommended to create a virtual environment to manage the dependencies specific to AutoRPT.

### Step 1: Create a Virtual Environment (Optional but Recommended)

Setting up a virtual environment ensures that package installations for AutoRPT do not interfere with other Python projects on your machine. Use the command line/terminal to run the following script:

#### For Windows:
```bash
python -m venv AutoRPT
AutoRPT\Scripts\activate
```

#### For macOS/Linux:
```bash
python3 -m venv AutoRPT
source AutoRPT/bin/activate
```

### Step 2: Install Dependencies

Navigate to the directory containing the AutoRPT folder (this may be in your Downloads unless you have since moved it). Navigate into the AutoRPT-main\AutoRPT-main folder (you should be able to see `requirements.txt` when you open the folder in the system explorer or use DIR). 
You can install the required dependencies by running:

```bash
pip install -r requirements.txt
```

This command will install all the necessary Python packages listed in the `requirements.txt` file.

#### Required Python Packages

The key dependencies for AutoRPT are:

1. **Praat-ParselMouth**: A Python interface to Praat for conducting phonetic analyses.
2. **TextGrid**: A library used to handle Praat TextGrid objects for annotating speech.
3. **Scikit-learn**: A widely-used library for machine learning tasks such as classification and regression.
4. **Pandas**: A powerful data manipulation and analysis library.
5. **PyTorch**: An open-source deep learning framework, used for building and training machine learning models.

If you get an error installing PyTorch, go to https://pytorch.org/, scroll to Install PyTorch, and follow its instructions to generate the correct script to run. For me, it was:
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```


### Step 3: Run AutoRPT

Choose whether you want to run the (RNN) AutoRPT or the AutoRPT_LSTM and navigate into that folder.

##LSTM:
You can then run AutoRPT with the following command:

```bash
python LSTM_RPT.py
```

AutoRPT will then start processing and annotating prosodic features based on the input data.

---

##AutoRPT:
Example of how to call the tool:
![](/AutoRPT/CMD_Use_Instructions/AutoRPTCMDEx.jpeg)
The example path is in green. Start typing after the >.
1. Remember to include 'python' before calling the AutoRPT.py file (This is highlighted in Light Blue in the image)
** All parameters are highlighted yellow in the image
** All manually entered file paths are highlighted orange in the image
2. Enter --textgrid and then inside either "" or '' include the path to the desired Textgrid file
3. Enter --wav and then inside either "" or '' include the path to the desired wav file
4. Enter --tier and then inside either "" or '' include the name of the target tier from the Textgrid file

In the general folder of AutoRPT there will be Pitch and Intensity CSVs, feel free to delete these as they are no longer of use.

Within the csv_outputs folder there will be 3 files (per Wav/Textgrid run). These are CSVs that contain the predictions of the model.

Within the tg_outputs folder there will be 3 files (per Wav/Textgrid run). These are Textgrids that contain the predictions of the model.


Step by Step CMD Example

C:\YourFilePath>cd AutoRPT
C:\YourFilePath\AutoRPT>python AutoRPT.py --textgrid "YourTextgridFile.TextGrid" --wav "YourWavFile.wav" --tier "YourTierName"

---
### Script Breakdown

####LSTM_RPT
Requires: os, tkinter, praatio, sys, Clean_I_Model, Clean_P_Model, Utilities

Description: Opens a file dialog to select TextGrid and WAV files, creates tiers in the TextGrid in which it marks suspected boundary and prominence and labels them with confidence percentages.

Functions:
* select_files() - Opens a file dialog to select TextGrid and WAV files. Requests tier names from user. Returns file paths and tier names.
* main(Textgrid_path, Wav_file_path, tier, phone_tier) - Creates tiers and places prosody annotations and confidence degrees from RPT functions in them. No returns.

####Clean_I_Model

Requires: parselmouth, tgt, numpy, spacy, pandas, re, os, tensorflow.keras.models, sklearn.preprocessing, sys, csv, datetime

Description: Defines and runs a number of functions related to intensity measures. 

Class IntensityExtraction Functions:
* getIntensity(self, Wav_file, start_time, end_time) - Gets intensity of an interval.
* getMaxIntensity(self, intensity_full) - Gets maximum intensity of a file.
* getMinIntensity(self, intensity_full) - Gets minimum intensity of a file.
* getSTDIntensity(self, intensity_full) - Gets standard deviation of intensity of a file.
* getAverageIntensity(self, intensity_full) - Gets arithmetic mean of intensity of a file.

Class FileProcessorIntensity Functions:
* __init__(self) - 
* iterateTextGridforIntensity(self, TextGrid_path, tier_name, Wav_file) - Creates array Interval_data, iterates through intervals of specified TextGrid tier, and runs calculations. Returns array interval_data, int error_count, and array error_arr.

Class SpeakerNormalization Functions:
* fileMean(self, interval_data, arr) - Takes arr and returns the average of the values
* fileStd(self, interval_data, avg, arr) - Takes arr and average and returns Standard Deviation (Std) of the values
* fileMin(self, interval_data, arr) - Takes arr and returns the minimum value
* fileMax(self, interval_data, arr) - Takes arr and returns the maximum value
* zScoreAppend(self, interval_data, avg, std, arr) - Takes arr, average, Std and appends the Z-score to dict
* getZScore(self, key, avg, std) - Takes a specific value and finds the Z-score.

Class IntensityFormatToInterval Functions:
* dictToArr(self, arr) - Converts dictionary to array.
* outputArr(self, arr) - Prints array.

Class IntensityFormatting Functions:
* to_csv(self, data, csv_file) - Creates CSV file out of array and saves it. No returns.

Class context functions:
* contextWindow(self, complete_data) - 

Class POS functions:
* add_pos_column_with_pandas(self, input_csv, text_column_name="Text", new_column_name="POS ID's") - Generates POS tags from spaCy model and saves to provided CSV file.
* clean_column(self, input_csv) - Keeps only the first number from part of speech IDs.
* extract_first_number(cell) - defined inside clean_column

Class Saved_Model functions:
* intensity_model(self, csv_file, pred_dict) -  Loads model, extracts and normalizes input data, makes predictions, and writes to dictionary. Returns dictionary pred_dict.

Class Intensity functions:
* run(tier_name, Textgrid_path, Wav_file_path) - Creates Sound object, does calculations on data, and exports the resulting dict.

####Clean_P_Model

Requires: parselmouth, tgt, numpy, spacy, pandas, re, os, tensorflow.keras.models, sklearn.preprocessing, sys, csv, datetime

Description: Defines and runs a number of functions related to pitch measures. 

Class PitchExtraction Functions:
* getMaxPitch(self, Wav_file, start_time, end_time) - Gets maximum pitch of a file.
* getMinPitch(self, Wav_file, start_time, end_time) - Gets minimum pitch of a file.
* getPitchStandardDeviation(self, Wav_file, start_time, end_time) - Gets standard deviation of pitch of a file.
* getAveragePitch(self, Wav_file, start_time, end_time) - Gets arithmetic mean of pitch of an interval.

Class SpeakerNormalization Functions:
* fileMean(self, interval_data, arr) - Takes arr and returns the average of the values
* fileStd(self, interval_data, avg, arr) - Takes arr and average and returns Standard Deviation (Std) of the values
* fileMin(self, interval_data, arr) - Takes arr and returns the minimum value
* fileMax(self, interval_data, arr) - Takes arr and returns the maximum value
* zScoreAppend(self, interval_data, avg, std, arr) - Takes arr, average, Std and appends the Z-score to dict
* getZScore(self, key, avg, std) - Takes a specific value and finds the Z-score.

Class FileProcessor Functions:
* __init__(self) - Runs model by itself calling PitchExtraction()
* iterateTextGridforPitch(self, TextGrid_path, tier_name, Wav_file) - Creates array Interval_data, iterates through intervals of specified TextGrid tier, and runs calculations. Returns array interval_data, int error_count, and array error_arr.
  
Class FormatToInterval Functions:
* dictToArr(self, arr) - Converts dictionary to array.
* outputArr(self, arr) - Prints array.

Class Formatting Functions:
* to_csv(self, data, csv_file) - Creates CSV file out of array and saves it. No returns.

Class plswrk functions:
* contextWindow(self, complete_data) - 

Class POS functions:
* add_pos_column_with_pandas(self, input_csv, text_column_name="Text", new_column_name="POS ID's") - Generates POS tags from spaCy model and saves to provided CSV file.
* clean_column(self, input_csv) - Keeps only the first number from part of speech IDs.
* extract_first_number(cell) - defined inside clean_column

Class Saved_Model functions:
* pitch_model(self, csv_file, pred_dict) -  Loads model, extracts and normalizes input data, makes predictions, and writes to dictionary. Returns dictionary pred_dict.

Class Pitch functions:
* run(tier_name, Textgrid_path, Wav_file_path) - Creates Sound object, does calculations on data, and exports the resulting dict.

####Utilities

Requires: praatio textgrid, re, tgt

Description:  

Class model_join functions:
* static dict_merge(p_dict, i_dict)

Class CTG functions:
* create_textgrid(final_dict, output_file, reference_textgrid)
* create_point_tier(final_dict, textgrid_path, phone_data)

Class Point_Tier functions:
* static phone_data(Textgrid_path, phone_tier)
* static point_tier_setup(start_time, end_time, phone_dict, type)
