#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import os
import tgt
import traceback
import tkinter as tk
from tkinter import filedialog
from praatio import textgrid

#Add the current directory to sys.path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import Clean_I_Model
import Clean_P_Model
import Utilities
from Utilities import *
from Clean_P_Model import Pitch
from Clean_I_Model import Intensity

def select_files():
    """
    Opens a file dialog to select TextGrid and WAV files.
    Args: none
    Returns: path-like string textgrid_path, path-like string wav_file_path, string tier, string phone-tier
    """
    root = tk.Tk()
    root.withdraw() 

    print("Choose a TextGrid file from the file dialog.")
    textgrid_path = filedialog.askopenfilename(title="Select TextGrid File", filetypes=[("TextGrid files", "*.TextGrid")])
    if not textgrid_path:
        print("No TextGrid file selected. Exiting.")
        quit()
        return None, None, None

    print("Choose a WAV file from the file dialog.") 
    wav_file_path = filedialog.askopenfilename(title="Select WAV File", filetypes=[("WAV files", "*.wav")])
    if not wav_file_path:
        print("No WAV file selected. Exiting.")
        quit()
        return None, None, None

    tgt_text_grid = tgt.io.read_textgrid(textgrid_path)
    all_tiers = [t.name for t in tgt_text_grid.tiers]

    continue_prog = False
    while not continue_prog:
        tier = input("Enter the word tier name in the TextGrid: ")
        if tier in all_tiers:
            continue_prog = True
        elif tier in ["Cancel","cancel","quit","Quit","exit", "Exit"]:
            print("Exiting.")
            quit()
        else:
            print("Not a valid tier.")

    continue_prog = False
    while not continue_prog:
        phone_tier = input("Enter the phone tier name in the TextGrid: ")
        if phone_tier in all_tiers:
            continue_prog = True
        elif phone_tier in ["Cancel","cancel","quit","Quit","exit", "Exit"]:
            print("Exiting.")
            quit()
        else:
            print("Not a valid tier.")

    # phone_tier = input("Enter the phone tier name in the TextGrid: ")
    
    return textgrid_path, wav_file_path, tier, phone_tier


def pull_files_from_drive():
    # Selects source files directly from Google Drive.
    # Args: None
    # Returns: path-like string textgrid_path, path-like string wav_file_path, string tier, string phone-tier
    
    root = tk.Tk()
    root.withdraw()

    f = open("pull_files_from_drive.txt")
    gen_textgrid_path = f.readline()[0:-1]
    gen_wav_path = f.readline()[0:-1]
    gen_save_path = f.readline()
    print(gen_textgrid_path)
    print(gen_save_path)
    f.close()
    print("\nYou said you keep your textgrid files here: ", gen_textgrid_path)
    # print("And your WAV files here: ", gen_wav_path)
    continue_prog = input("If that isn't right, please update pull_files_from_drive.txt and restart this program. Continue? (Y/N)")
    if (continue_prog not in ['Y', 'y', "yes", "Yes", "correct"]):
        print("Exiting.")
        quit()
        return None, None, None
    
    wav_file_path = filedialog.askopenfilename(title="Select WAV File", filetypes=[("WAV files", "*.wav")])
    if not wav_file_path:
        print("No WAV file selected. Exiting.")
        quit()
        return None, None, None
    
    filename = wav_file_path.split('/')[-1]
    filename_stripped = filename[0:-6]
    textgrid_path = os.path.join(gen_textgrid_path,(filename_stripped + ".TextGrid"))
    #print (textgrid_path)

    if (filename[-5] == '1'):
        word_tier = filename[9:13]+(' L - words')
        phone_tier = filename[9:13]+(' L - phones')
    elif (filename[-5] == '2'):
        word_tier = filename[13:17].join(' R - words')
        phone_tier = filename[13:17].join(' R - phones')
    else:
        print("Incorrect file naming convention. Please select manually.")
        textgrid_path, wav_file_path, tier, phone_tier = select_files()


    return textgrid_path, wav_file_path, word_tier, phone_tier

def integration_test1():
    f = open("pull_files_from_drive.txt")
    gen_textgrid_path = f.readline()[0:-1]
    gen_wav_path = f.readline()[0:-1]
    f.close()
    word_tier = "92zr - words"
    phone_tier = "92zr - phones"
    textgrid_path = os.path.join(gen_textgrid_path, "1213p48mx92zr82pv.TextGrid")
    wav_file_path = os.path.join(gen_wav_path, "1213p48mx92zr82pv_1.wav")
    print(textgrid_path)
    print(wav_file_path)
    return textgrid_path, wav_file_path, word_tier, phone_tier

def main(Textgrid_path, Wav_file_path, tier, phone_tier):
    # Gets provided metadata from select_data and runs pitch and intensity functions.
    # Args: path-like string textgrid_path, path-like string wav_file_path, string tier, string phone-tier
    # Returns: none
    
    wav_file_name = os.path.basename(Wav_file_path)
    wav_to_csv = wav_file_name + "_Predictions.TextGrid"
    
    current_path = os.getcwd()
    #csv_path = os.path.join(current_path, "TextGrid_output")
    csv_path = os.path.join(os.path.dirname(Wav_file_path), "TextGrid_output")
    print("csv_path =",csv_path)
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)
    
    csv_file = os.path.join(csv_path, wav_to_csv)

    try:
        pitch_dict = Pitch.run(tier, Textgrid_path, Wav_file_path)
        intensity_dict = Intensity.run(tier, Textgrid_path, Wav_file_path)
    except:
        print(traceback.format_exc())
    
    pred_dict = model_join.dict_merge(pitch_dict, intensity_dict)
    
    CTG.create_textgrid(pred_dict, csv_file, Textgrid_path)

    phone_dict = Point_Tier.phone_data(Textgrid_path, phone_tier)

    CTG.create_point_tier(pred_dict, csv_file, phone_dict)
    printable = mdictToArr(pred_dict)
    filepath=os.path.join(os.path.dirname(Wav_file_path),"final.csv")
    mto_csv(data=printable,csv_file=filepath)
    print("reached end of main")

    #if scheme == "y":
        #CTG.replace_numbers_in_tiers(csv_file, tiers = ["Prominence", "Boundary"])

if __name__ == "__main__":
    #textgrid_path, wav_file_path, tier, phone_tier = select_files()
    #textgrid_path, wav_file_path, tier, phone_tier = pull_files_from_drive()
    textgrid_path, wav_file_path, tier, phone_tier = integration_test1()
    
    if textgrid_path and wav_file_path and tier and phone_tier:
        main(textgrid_path, wav_file_path, tier, phone_tier)
