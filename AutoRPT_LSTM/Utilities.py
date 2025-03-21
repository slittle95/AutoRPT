#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class model_join:
    
    @staticmethod
    def dict_merge(p_dict, i_dict):
        p_intervals = p_dict["Interval"]
        i_intervals = i_dict["Interval"]
        p_start = p_dict["start"]
        i_start = i_dict["start"]
        p_end = p_dict["end"]
        i_end = i_dict["end"]
        i_text = i_dict["Text"]
        p_text = p_dict["Text"]

        total_max = max(max(p_intervals), max(i_intervals))
            
        i = 0
        pitch = 0
        intensity = 0
        
        # Initialize dictionary lists
        final_dict = {
            "Interval": [],
            "Text": [],
            "Prominence": [],
            "Boundary": [],
            "start": [],
            "end": [],
            "Prominence_label": [],
            "Boundary_label" : []
        }

        while i <= total_max:
            
            if i in p_intervals and i in i_intervals:
                final_dict["Interval"].append(i)
                
                i_prom = i_dict["Prominence_raw"][intensity]
                p_prom = p_dict["Prominence_raw"][pitch]
                i_bound = i_dict["Boundary_raw"][intensity]
                p_bound = p_dict["Boundary_raw"][pitch]
                
                text = p_text[pitch]
                final_dict["Text"].append(text)
                
                prom = round((i_prom + p_prom) / 2, 2)
                bound = round((i_bound + p_bound) / 2, 2)
                
                final_dict["Prominence"].append(prom)
                final_dict["Boundary"].append(bound)
                
                final_dict["start"].append(p_start[pitch])
                final_dict["end"].append(p_end[pitch])
                
                pitch += 1
                intensity += 1

            elif i in p_intervals and i not in i_intervals:
                final_dict["Interval"].append(i)
                
                prom = round(p_dict["Prominence_raw"][pitch], 2)
                bound = round(p_dict["Boundary_raw"][pitch], 2)
                text = p_text[pitch]
                
                final_dict["Text"].append(text)
                final_dict["Prominence"].append(prom)
                final_dict["Boundary"].append(bound)
                
                final_dict["start"].append(p_start[pitch])
                final_dict["end"].append(p_end[pitch])
                
                pitch += 1

            elif i in i_intervals and i not in p_intervals:
                final_dict["Interval"].append(i)
                
                prom = round(i_dict["Prominence_raw"][intensity], 2)
                bound = round(i_dict["Boundary_raw"][intensity], 2)
                text = i_text[intensity]  # Fix: Use `i_text` not `p_text`
                
                final_dict["Text"].append(text)
                final_dict["Prominence"].append(prom)
                final_dict["Boundary"].append(bound)
                
                final_dict["start"].append(i_start[intensity])
                final_dict["end"].append(i_end[intensity])
                
                intensity += 1

            i += 1  # Always increment i
        
        return final_dict


# In[ ]:





# In[ ]:


from praatio import textgrid
import re

class CTG:
    
    
    def create_textgrid(final_dict, output_file, reference_textgrid):
        
        tg = textgrid.Textgrid()
        
        ref_tg = textgrid.openTextgrid(reference_textgrid, includeEmptyIntervals=True)
        max_et = ref_tg.maxTimestamp

        text_tier = textgrid.IntervalTier("Text", [], minT=0, maxT=max_et)
        prominence_tier = textgrid.IntervalTier("Prominence", [], minT=0, maxT= max_et)
        boundary_tier = textgrid.IntervalTier("Boundary", [], minT=0, maxT=max_et)
        
        for start, end, text, prominence, boundary in zip(
            final_dict["start"],
            final_dict["end"],
            final_dict["Text"],
            final_dict["Prominence"],
            final_dict["Boundary"]
        ):
            
            start = float(start)
            end = float(end)
            text = str(text)


            text_tier.insertEntry((start, end, text))
            prominence_tier.insertEntry((start, end, str(prominence)))
            boundary_tier.insertEntry((start, end, str(boundary)))

            
        tg.addTier(text_tier)
        tg.addTier(prominence_tier)
        tg.addTier(boundary_tier)
        
        tg.save(output_file, format="long_textgrid", includeBlankSpaces=True)




    def create_point_tier(final_dict, textgrid_path, phone_data):
        tg = textgrid.openTextgrid(textgrid_path, includeEmptyIntervals=True)

        tier = next((t for t in tg.tiers if t.name == "Text"), None)

        if tier is None:
            print("Text tier not found")
            return
        
        intervals = tier.entries
        if not intervals:
            print("No intervals in tier")
            return
        
        
        min_t = intervals[0].start
        max_t = intervals[-1].end

        time_stamps = {}

        for idx, element in enumerate(final_dict["Prominence"]):
            if 0.41 <= element <= 0.7:
                point = Point_Tier.point_tier_setup(final_dict["start"][idx], final_dict["end"][idx], phone_data, "Prominence")
                time_stamps[point] = "*?"

            elif 0.71 <= element <= 1:
                point = Point_Tier.point_tier_setup(final_dict["start"][idx], final_dict["end"][idx], phone_data, "Prominence")
                time_stamps[point] = "*"

        for idx, element in enumerate(final_dict["Boundary"]):
            if 0.16 <= element <= 0.29:
                point = Point_Tier.point_tier_setup(final_dict["start"][idx], final_dict["end"][idx], phone_data, "Boundary")
                time_stamps[point] = "]?"

            elif 0.3 <= element <= 1:
                point = Point_Tier.point_tier_setup(final_dict["start"][idx], final_dict["end"][idx], phone_data, "Boundary")
                time_stamps[point] = "]"


        sorted_time_stamps = [(k, time_stamps[k]) for k in sorted(time_stamps)]

        point_tier = textgrid.PointTier("RPT", sorted_time_stamps, minT=min_t, maxT = max_t)


        if phone_data["Start"] and phone_data["End"]:
            phone_tier = textgrid.IntervalTier("phone", [], minT=min_t, maxT= max_t)

            for start, end, text in zip(phone_data["Start"], phone_data["End"], phone_data["Text"]):
                phone_tier.insertEntry((float(start), float(end), str(text)))

        else:
            print("Phone tier is empty")

        tg.addTier(phone_tier)

        tg.addTier(point_tier)

        tg.save(textgrid_path, format="long_textgrid", includeBlankSpaces=True)

                
        

from praatio import textgrid   
import re     
import tgt


class Point_Tier:

    import re
    
    @staticmethod
    def phone_data(Textgrid_path, phone_tier):

        
    # Load the TextGrid file using `tgt`
        tgt_text_grid = tgt.io.read_textgrid(Textgrid_path)

    # Find the specified tier
        tier = next((t for t in tgt_text_grid.tiers if t.name == phone_tier), None)

        if tier is None:

            return None  # Or raise an error if needed

    # Create the interval dictionary
        interval_dict = {"Start": [], "End": [], "Text": []}

    # Extract data from annotations
        for annotation in tier.annotations:
            interval_dict["Start"].append(annotation.start_time)
            interval_dict["End"].append(annotation.end_time)
            interval_dict["Text"].append(annotation.text)

        return interval_dict  # Returns the same structure as before
    
    @staticmethod

    def point_tier_setup(start_time, end_time, phone_dict, type):
        if start_time in phone_dict["Start"]:
            j = phone_dict["Start"].index(start_time)
        else:
            print(f"Warning: start_time {start_time} not found in phone_dict['Start']")
            return None
    
        continue_loop = True
        temp = {"Start": [], "End": [], "Text": []}

        while continue_loop:
            if j >= len(phone_dict["Start"]):  # Ensure j does not go out of range
                break

            pd_start = phone_dict["Start"][j]
            pd_end = phone_dict["End"][j]
            pd_text = phone_dict["Text"][j]

            if pd_start >= start_time and pd_end <= end_time:
                temp["Start"].append(pd_start)
                temp["End"].append(pd_end)
                temp["Text"].append(pd_text)
                j += 1  # Move to the next index
            else:
                continue_loop = False  # Stop looping if outside range

        if not temp["Text"]:
            print(f"Warning: No matching intervals for start_time {start_time}")
            return None  # Or another fallback value

        stress_index = min(
            range(len(temp["Text"])), 
            key=lambda i: 0 if '1' in temp["Text"][i] else float('inf'),
            default = None
        )

        if stress_index is None:
            print(f"Warning: Could not find valid min_index for start_time {start_time}")
            return None

        low_start = temp["Start"][stress_index]
        low_end = temp["End"][stress_index]

        if type == "Prominence":
            point_time = (low_start + low_end) / 2
        else:
            point_time = end_time #Changed to end_time to put ] to match at end of larger interval (words not phones)

        return point_time
