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
import sliceUtterances

def select_files():
    """
    Opens a file dialog to select TextGrid and WAV files.
    Args: none
    Returns: path-like string textgrid_path, path-like string wav_file_path, string word_tier, string phone-tier
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
        word_tier = input("Enter the word tier name in the TextGrid: ")
        if word_tier in all_tiers:
            continue_prog = True
        elif word_tier in ["Cancel","cancel","quit","Quit","exit", "Exit"]:
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

   
    return textgrid_path, wav_file_path, word_tier, phone_tier


def pull_files_from_drive():
    # Selects source files directly from Google Drive.
    # Args: None
    # Returns: path-like string textgrid_path, path-like string wav_file_path, string word_tier, string phone-tier,
    #   string gen_ save_path
    
    root = tk.Tk()
    root.withdraw()

    f = open("pull_files_from_drive.txt")
    gen_textgrid_path = f.readline()[0:-1]
    gen_wav_path = f.readline()[0:-1]
    gen_save_path = f.readline()[0:-1]
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
        word_tier = filename[9:13]+(' - words')
        phone_tier = filename[9:13]+(' - phones')
    elif (filename[-5] == '2'):
        word_tier = filename[13:17]+(' - words')
        phone_tier = filename[13:17]+(' - phones')
    else:
        print("Incorrect file naming convention. Please select manually.")
        textgrid_path, wav_file_path, word_tier, phone_tier = select_files()


    return textgrid_path, wav_file_path, word_tier, phone_tier, gen_save_path

def integration_test1():
    # Quickest way to test the file. Works on a specific set of 2-minute files in a specific file directory.
    # Args: None.
    # Returns: path-like string textgrid_path, path-like string wav_file_path, string word_tier, string phone-tier,
    #   string gen_ save_path
    print("Reading files...")
    f = open("pull_files_from_drive.txt")
    gen_textgrid_path = f.readline()[0:-1]
    gen_wav_path = f.readline()[0:-1]
    gen_save_path = f.readline()[0:-1]
    f.close()
    word_tier = "92zr - words"
    phone_tier = "92zr - phones"
    textgrid_path = os.path.join(gen_textgrid_path, "1213p48mx92zr82pv.TextGrid")
    wav_file_path = os.path.join(gen_wav_path, "1213p48mx92zr82pv_1.wav") 
    print(textgrid_path)
    print(wav_file_path)
    return textgrid_path, wav_file_path, word_tier, phone_tier, gen_save_path

def integration_test2():
    #same as integration test 1 but with a full length file
    print("Reading files...")
    f = open("pull_files_from_drive.txt")
    gen_textgrid_path = f.readline()[0:-1]
    gen_wav_path = f.readline()[0:-1]
    gen_save_path = f.readline()[0:-1]
    f.close()
    word_tier = "09rl - words"
    phone_tier = "09rl - phones"
    textgrid_path = os.path.join(gen_textgrid_path, "1213p02fm02kw09rl.TextGrid")
    wav_file_path = os.path.join(gen_wav_path, "1213p02fm02kw09rl_2.wav") 
    print(f"Textgrid path ={textgrid_path}")
    print(f"WAV file path ={wav_file_path}")
    return textgrid_path, wav_file_path, word_tier, phone_tier, gen_save_path


def main(Textgrid_path, Wav_file_path, word_tier, phone_tier, save_path = None, split_utterances=True):
    # Gets provided metadata from one of the data select functions and runs pitch and intensity functions.
    # Args: path-like string textgrid_path, path-like string wav_file_path, string word_tier, string phone-tier
    # Kwargs: path-like string save_path, boolean split_utterances
    # Returns: none
    
    wav_file_name = os.path.basename(Wav_file_path)
    pred_textgrid_name = wav_file_name[:-4] + "_Predictions.TextGrid"
    
    #prep save environment
    print(save_path)
    if not save_path:
        current_path = os.getcwd()
        save_path = current_path
    print(save_path)
    tg_output_path=os.path.join(save_path, "TextGrid_output")
    csv_path = os.path.join(save_path, "CSV_output")                                
    print("tg_output_path =",tg_output_path)
    if not os.path.exists(tg_output_path):
        os.makedirs(tg_output_path)
    print("csv_path =",csv_path)
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)
        
    tg_output_file = os.path.join(tg_output_path, pred_textgrid_name)

    try:
        pitch_dict = Pitch.run(word_tier, Textgrid_path, Wav_file_path, save_path)
        intensity_dict = Intensity.run(word_tier, Textgrid_path, Wav_file_path, save_path)
    except:
        print(traceback.format_exc())
        quit()
    print("Joining model...")
    pred_dict = model_join.dict_merge(pitch_dict, intensity_dict)

    print("Creating textgrid...")
    CTG.create_textgrid(pred_dict, tg_output_file, Textgrid_path)
    phone_dict = Point_Tier.phone_data(Textgrid_path, phone_tier)
    CTG.create_point_tier(pred_dict, tg_output_file, phone_dict)
   
    print("Creating and outputting final_dict...")
    printable = mdictToArr(pred_dict)
    filepath=os.path.join(csv_path,wav_file_name[:-4]+"_final.csv")
    mto_csv(data=printable,csv_file=filepath)

    if split_utterances:
        print("Splitting utterances...")
        sliceUtterances.just_one_moneypenney(Wav_file_path, Textgrid_path, save_path, pred_dict, word_tier, phone_tier)

    print("Operation complete.")

    #if scheme == "y":
        #CTG.replace_numbers_in_tiers(tg_output_file, tiers = ["Prominence", "Boundary"])

if __name__ == "__main__":
    """
    Only one of these three should be uncommented at a time. See descriptions of methods to pick one.
    """
    #textgrid_path, wav_file_path, word_tier, phone_tier = select_files()
    #textgrid_path, wav_file_path, word_tier, phone_tier, save_path = pull_files_from_drive()
    textgrid_path, wav_file_path, word_tier, phone_tier, save_path = integration_test2()
    
    if textgrid_path and wav_file_path and word_tier and phone_tier:
        main(textgrid_path, wav_file_path, word_tier, phone_tier, save_path=save_path)
