#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import os
import tkinter as tk
from tkinter import filedialog
from praatio import textgrid

#Add the current directory to sys.path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import Clean_I_Model
import Clean_P_Model
import Utilities
from Utilities import model_join, CTG
from Clean_P_Model import Pitch
from Clean_I_Model import Intensity

def select_files():
    """Open a file dialog to select TextGrid and WAV files."""
    root = tk.Tk()
    root.withdraw() 
    
    textgrid_path = filedialog.askopenfilename(title="Select TextGrid File", filetypes=[("TextGrid files", "*.TextGrid")])
    if not textgrid_path:
        print("No TextGrid file selected. Exiting.")
        return None, None, None
    
    wav_file_path = filedialog.askopenfilename(title="Select WAV File", filetypes=[("WAV files", "*.wav")])
    if not wav_file_path:
        print("No WAV file selected. Exiting.")
        return None, None, None
    
    tier = input("Enter the tier name in the TextGrid: ")  

    scheme = input("Use RPT annotation as output? (y/n): ")
    
    return textgrid_path, wav_file_path, tier, scheme

def main(Textgrid_path, Wav_file_path, tier, scheme):
    
    wav_file_name = os.path.basename(Wav_file_path)
    wav_to_csv = wav_file_name + "_Predictions.TextGrid"
    
    current_path = os.getcwd()
    csv_path = os.path.join(current_path, "TextGrid_output")
    
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)
    
    csv_file = os.path.join(csv_path, wav_to_csv)
    
    pitch_dict = Pitch.run(tier, Textgrid_path, Wav_file_path)
    intensity_dict = Intensity.run(tier, Textgrid_path, Wav_file_path)
    
    pred_dict = model_join.dict_merge(pitch_dict, intensity_dict)
    
    CTG.create_textgrid(pred_dict, csv_file, Textgrid_path)

    if scheme == "y":
        CTG.replace_numbers_in_tiers(csv_file, tiers = ["Prominence", "Boundary"])

if __name__ == "__main__":
    textgrid_path, wav_file_path, tier, scheme = select_files()
    
    if textgrid_path and wav_file_path and tier and scheme:
        main(textgrid_path, wav_file_path, tier, scheme)
