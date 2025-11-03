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
from Utilities import model_join, CTG, Point_Tier
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

 
    
def main():
    # Args: none
    # Returns: none
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
    print("And your WAV files here: ", gen_wav_path)
    continue_prog = input("If that isn't right, please update pull_files_from_drive.txt and restart this program. Continue? (Y/N)")
    if (continue_prog not in ['Y', 'y', "yes", "Yes", "correct"]):
        print("Exiting.")
        quit()
        return None, None, None
    for filename in os.listdir(gen_wav_path):           
        #filename = Wav_file_path.split('/')[-1]
        filename_stripped = filename[0:-6]
        textgrid_path = os.path.join(gen_textgrid_path,(filename_stripped + ".TextGrid"))
        skipped_files = ""
        print('\n')
        print (textgrid_path)

        if (filename[-5] == '1'):
            word_tier = filename[9:13]+(' - words')
            phone_tier = filename[9:13]+(' - phones')
        elif (filename[-5] == '2'):
            word_tier = filename[13:17]+(' - words')
            phone_tier = filename[13:17]+(' - phones')
        else:
            print("Incorrect file naming convention. Please select manually.")
            textgrid_path, wav_file_path, word_tier, phone_tier = select_files()

        wav_file_path = os.path.join(gen_wav_path, filename)
        print(wav_file_path)       
        #wav_file_name = os.path.basename(wav_path)
        wav_to_csv = filename + "_Predictions.TextGrid"
        
        #current_path = os.getcwd()
        #csv_path = os.path.join(current_path, "TextGrid_output")
        csv_path = gen_save_path
        
        if not os.path.exists(csv_path):
            os.makedirs(csv_path)
        
        csv_file = os.path.join(csv_path, wav_to_csv)
        try:
            pitch_dict = Pitch.run(word_tier, textgrid_path, wav_file_path)
            intensity_dict = Intensity.run(word_tier, textgrid_path, wav_file_path)
        except (TypeError, FileNotFoundError):
            skipped_files += (wav_file_path, '\n', traceback.format_list(traceback.extract_stack()), '\n')
            continue
        pred_dict = model_join.dict_merge(pitch_dict, intensity_dict)
          
        CTG.create_textgrid(pred_dict, csv_file, textgrid_path)

        phone_dict = Point_Tier.phone_data(textgrid_path, phone_tier)

        CTG.create_point_tier(pred_dict, csv_file, phone_dict)
    if skipped_files != "":
        print("Skipped files: \n", skipped_files)
        #if scheme == "y":
            #CTG.replace_numbers_in_tiers(csv_file, tiers = ["Prominence", "Boundary"])

if __name__ == "__main__":
    main()
