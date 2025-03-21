#!/usr/bin/env python
# coding: utf-8

# # Extraction

# In[1]:


import parselmouth
import tgt
import numpy as np

class IntensityExtraction:
    
    def getIntensity(self, Wav_file, start_time, end_time):
        interval_file = Wav_file.extract_part(from_time=start_time, to_time=end_time)
        intensity = interval_file.to_intensity()
        return intensity

    def getMaxIntensity(self, intensity_full):
        intensity_max = np.max(intensity_full)
        return intensity_max

    def getMinIntensity(self, intensity_full):
        intensity_min = np.min(intensity_full)
        return intensity_min

    def getSTDIntensity(self, intensity_full):
        intensity_std = np.std(intensity_full)
        return intensity_std

    def getAverageIntensity(self, intensity_full):
        intensity_mean = np.mean(intensity_full)
        return intensity_mean


# # Iterate

# In[2]:


import parselmouth
import tgt
import numpy as np


class FileProcessorIntensity:
    

    def __init__(self):
        self.ie = IntensityExtraction()

    
    def iterateTextGridforIntensity(self, TextGrid_path, tier_name, Wav_file):
    
        error_count = 0
        error_arr = []
        #Create Dictionary
        interval_data = {"Interval":[],"Text":[], "min":[], "max":[], "mean":[], "Std":[], "z-score":[], "start":[], "end":[], "STD":[], "Z-SCORE":[], "dur":[]}
    
        #Load the TextGrid using tgt
        tgt_text_grid = tgt.io.read_textgrid(TextGrid_path)
    
        average_sum = 0
        count = 0
        dict_iterable = 0

        #Get the specified tier
        tier = None
        for t in tgt_text_grid.tiers:
            if t.name == tier_name:
                tier = t
                break

        if tier is None:
            print(f"Tier '{tier_name}' not found in the TextGrid.")
            return

        #Iterate through intervals on the tier
        for interval in tier:
            start_time = interval.start_time
            end_time = interval.end_time
            interval_text = interval.text
            #print("start time:", start_time, ", end time:", end_time, ", text:", interval_text)
            
            if interval_text[0] == "{":
                pass
            else:
                
                
                try:
            
                #Calculate Intensity of the interval
                    initial_intensity = self.ie.getIntensity(Wav_file, start_time, end_time)
        
                #Calculate the pitch standard deviation for the interval
                    intensity_std_dev = self.ie.getSTDIntensity(initial_intensity)
        
                    interval_data["Std"].append(intensity_std_dev)
        
                #Calculate Max pitch of interval
                    high = self.ie.getMaxIntensity(initial_intensity)
        
                    interval_data["max"].append(high)
            
                    interval_data["start"].append(start_time)
                    interval_data["end"].append(end_time)
                    
                    dur = end_time - start_time
                    
                    interval_data["dur"].append(dur)
        
                #Calculate Min pitch of interval
                    low = self.ie.getMinIntensity(initial_intensity)
        
                    interval_data["min"].append(low)
            
                    interval_data["Text"].append(interval_text)
        
                    dict_iterable += 1
        
                    interval_data["Interval"].append(dict_iterable)
            
                #get the average pitch of interval
                    average = self.ie.getAverageIntensity(initial_intensity)
        
                    interval_data["mean"].append(average)
        
                #Find the average of all intervals so far
                    average_sum += average
                    count += 1
                    total_average = average_sum / count
                    
                except Exception as e:
                    #print(f"Skipping interval due to error: {e}")
                    error_count = error_count + 1 
                    dict_iterable += 1
                    error_arr.append(dict_iterable)
                    
        
        return interval_data, error_count, error_arr


# # Normalization

# In[3]:


import parselmouth
import tgt
import numpy as np

class SpeakerNormalization:

    #Takes arr and returns the average of the values
    def fileMean(self, interval_data, arr):
        mean_sum = 0
        mean_n = len(interval_data[arr])
        sqr_diff = 0
        for value in interval_data[arr]:
            mean_sum += value
        file_avg = mean_sum / mean_n
        
        return file_avg
    
    #Takes arr and average and returns Standard Deviation (Std) of the values
    def fileStd(self, interval_data, avg, arr):
        
        mean_n = len(interval_data[arr])
        
        sqr_diff = 0
        
        for value in interval_data[arr]:
            
            sqr_diff += (value - avg) * (value - avg)
    
        sqr_mean = sqr_diff / mean_n
    
        file_std = sqr_mean ** 0.5
        
        return file_std
    
    #Takes arr and returns the minimum value
    def fileMin(self, interval_data, arr):
    
        file_min = min(interval_data[arr])
        
        return file_min
    
    #Takes arr and returns the maximum value
    def fileMax(self, interval_data, arr):
    
        file_max = max(interval_data[arr])
    
        return file_max
    
    #Takes arr, average, Std and appends the Z-score to dict
    def zScoreAppend(self, interval_data, avg, std, arr):
    
        for value in interval_data[arr]:
        
            z_score = (value - avg) / std
        
            interval_data["z-score"].append(z_score)
    
        return interval_data
    
    def getZScore(self, key, avg, std):
        z_score = (key - avg) / std
        return z_score


# # Format

# In[4]:


class IntensityFormatToInterval:
    
    def dictToArr(self, arr):
        
        tier_arrays = []
        
        # Initialize first array with formatting
        header = ["Interval", "Text", "Min", "Max", "Mean", "Standard Deviation", "Z-Score", "Start", "End", "Duration"]
        tier_arrays.append(header)
        
        # Create User-Output Array
        for i in range(len(arr["Interval"])):
            row = [
                arr["Interval"][i],
                arr["Text"][i],
                arr["min"][i],
                arr["max"][i],
                arr["mean"][i],
                arr["STD"][i],
                arr["Z-SCORE"][i],
                arr["start"][i],
                arr["end"][i],
                arr["dur"][i]
            ]
            tier_arrays.append(row)
            
        return tier_arrays

    def outputArr(self, arr):
        
        for i, array in enumerate(arr):
            print(array)


# # CSV

# In[5]:


import csv

class IntensityFormatting():
    def to_csv(self, data, csv_file):
        # Specify the CSV file name
        csv_directory = os.path.dirname(csv_file)
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)
        
        
        # Write the sub-arrays to the CSV file
        with open(csv_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
    
            # Iterate through the sub-arrays and write each element in separate columns
            for sub_array in data:
                 csv_writer.writerow(sub_array)

        print(f'Data has been written to {csv_file}.')


# # Context Window

# In[6]:


class context:
    
    def contextWindow(self, complete_data):
    
        f = -3
        g = -2
        h = -1
        i= 0
        j= 1
        k= 2
        l = 3

        for element in complete_data['max']:
    
            #After only
            if i == 0:
                num = [complete_data['max'][i], complete_data['max'][j], complete_data['max'][k], complete_data['max'][l]]
            
            #1 Before
            elif i == 1:
                num = [complete_data['max'][h], complete_data['max'][i], complete_data['max'][j], complete_data['max'][k], complete_data['max'][l]]
        
            #2 before
            elif i == 2:
                num = [complete_data['max'][g], complete_data['max'][h], complete_data['max'][i], complete_data['max'][j], complete_data['max'][k], complete_data['max'][l]]
                  
##################################################################
        
            #2 after
            elif i == (len(complete_data['max'])- 3):
                num = [complete_data['max'][f], complete_data['max'][g], complete_data['max'][h], complete_data['max'][i], complete_data['max'][j], complete_data['max'][k]]
    
            #1 after
            elif i == (len(complete_data['max']) -2):
                num = [complete_data['max'][f], complete_data['max'][g], complete_data['max'][h], complete_data['max'][i], complete_data['max'][j]]
        
            #Before only
            elif i == (len(complete_data['max']))-1:
                num = [complete_data['max'][f], complete_data['max'][g], complete_data['max'][h], complete_data['max'][i]]
            
########################################################
            #All other cases
            else:
                num = [complete_data['max'][f], complete_data['max'][g], complete_data['max'][h], complete_data['max'][i], complete_data['max'][j], complete_data['max'][k], complete_data['max'][l]]
            
            
            std = np.std(num)
            avg = np.mean(num)
            z_score = (complete_data['max'][i] - avg) / std            
            complete_data['STD'].append(std)
            complete_data['Z-SCORE'].append(z_score)
        
            f += 1
            g += 1
            h += 1
            i += 1
            j += 1
            k += 1
            l += 1
            
        return complete_data


# # POS Addition

# In[7]:


import pandas as pd
import spacy
import re


class POS:

    def add_pos_column_with_pandas(self, input_csv, text_column_name="Text", new_column_name="POS ID's"):
       
        nlp = spacy.load("en_core_web_sm")  # Load the spaCy model
    
        try:
            # Read the CSV into a DataFrame
            df = pd.read_csv(input_csv)

            if text_column_name in df.columns:
                # Generate POS tags for the text column
                df[new_column_name] = df[text_column_name].astype(str).apply(lambda text: " ".join([str(token.pos) for token in nlp(text)]))
                # Save the updated DataFrame back to the same CSV file
                df.to_csv(input_csv, index=False)
                #print(f"POS column added to {input_csv}.")
            else:
                print(f"Column '{text_column_name}' not found in {input_csv}.")
        except Exception as e:
            print(f"Error processing {input_csv}: {e}")


    def clean_column(self, input_csv):
        
        df = pd.read_csv(input_csv)
        
        if "POS ID's" not in df.columns:
            #print("Column 'POS ID'S' not found in the CSV file.")
            return
    
        # Function to extract only the first number from a cell
        def extract_first_number(cell):
            numbers = re.findall(r'\d+', str(cell))  # Find all numbers
            return numbers[0] if numbers else cell   # Keep only the first number
    
        # Apply the function to column POS ID'S
        df["POS ID's"] = df["POS ID's"].apply(extract_first_number)
    
        # Overwrite the original CSV file
        df.to_csv(input_csv, index=False)
        #print(f"Processed file saved as {input_csv}")


# # Model

# In[8]:


import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os
import sys


class Saved_Model:
    
    def intensity_model(self, csv_file, pred_dict):
        # Load the trained model
        working_dir = os.getcwd()
        folder_name = "Model_paths"
        folder_path = os.path.join(working_dir, folder_name)
        model_save_path = os.path.join(folder_path, "Intensity_LSTM_model.h5")
        model = load_model(model_save_path)
        print("Model loaded successfully.")

        # Load the new CSV data
        df = pd.read_csv(csv_file, header=0)  #Assumes first row is header

        #Extract features (same columns as in training)
        features = df.iloc[:, [2, 3, 4, 5, 6, 9, 10]].values  

        #Normalize using MinMaxScaler (must be the same as training)
        scaler = MinMaxScaler()
        features = scaler.fit_transform(features)  # Fit only if new, else use saved scaler

        #Reshape for LSTM input
        time_steps = 1  # Adjust if needed
        features = features.reshape((features.shape[0], time_steps, features.shape[1]))

            #Make predictions
        raw_predictions = model.predict(features)  # Raw model outputs
        binary_predictions = (raw_predictions > 0.4).astype(int)  # Convert to binary labels
    
        #Store predictions in the provided dictionary
        pred_dict["Prominence"] = [int(pred[0]) for pred in binary_predictions]
        pred_dict["Boundary"] = [int(pred[1]) for pred in binary_predictions]
        pred_dict["Prominence_raw"] = [float(pred[0]) for pred in raw_predictions]
        pred_dict["Boundary_raw"] = [float(pred[1]) for pred in raw_predictions]
        
            #Save predictions to CSV
        df["Prominence"] = pred_dict["Prominence"]
        df["Boundary"] = pred_dict["Boundary"]
        df["Prominence_raw"] = pred_dict["Prominence_raw"]
        df["Boundary_raw"] = pred_dict["Boundary_raw"]
        df.to_csv(csv_file, index=False)
        
        return pred_dict


# # Final



# # Playtest

# In[ ]:


import csv
import parselmouth
import tgt
import numpy as np
import datetime
import os


class Intensity:
    
    def run(tier_name, Textgrid_path, Wav_file_path):
        

        #Work Environment

        fpi = FileProcessorIntensity()
        ie = IntensityExtraction()
        spn = SpeakerNormalization()
        ifti = IntensityFormatToInterval()
        ifo = IntensityFormatting()
        cx = context()
        pos = POS()
        sm = Saved_Model()

        wav_file_name = os.path.basename(Wav_file_path)
        wav_file_name_woe = os.path.splitext(wav_file_name)[0]
        wav_to_csv = wav_file_name_woe + "_Intensity.csv"
        current_path = os.getcwd()
        csv_path = os.path.join(current_path, "CSV_output")
        csv_file = os.path.join(csv_path, wav_to_csv)

        Wav_file = parselmouth.Sound(Wav_file_path)
            
        data, error, error_arr = fpi.iterateTextGridforIntensity(Textgrid_path, tier_name, Wav_file)

        file_mean = spn.fileMean(data, "max")
        file_std = spn.fileStd(data, file_mean, "max")
        file_min = spn.fileMin(data, "min")
        file_max = spn.fileMax(data, "max")
        complete_data = spn.zScoreAppend(data, file_mean, file_std, "max")
    
        full_complete_data = cx.contextWindow(complete_data)

        tier_arrays = ifti.dictToArr(full_complete_data)

        #print("\n")

        ifo.to_csv(tier_arrays, csv_file)

        pos.add_pos_column_with_pandas(csv_file, text_column_name = "Text", new_column_name="POS ID's")
        pos.clean_column(csv_file)

        final_intensity_data = sm.intensity_model(csv_file, full_complete_data)

        return final_intensity_data

