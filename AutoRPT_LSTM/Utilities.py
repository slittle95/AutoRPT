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
            "end": []
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

    

    def replace_numbers_in_tiers(textgrid_path, tiers=["Prominence", "Boundary"]):
        with open(textgrid_path, "r", encoding="utf-8") as file:
         lines = file.readlines()
    
        in_target_tier = False
        current_tier = None
        modified_lines = []
        tier_pattern = re.compile(r'\s*name\s*=\s*"(.*?)"')
        number_pattern = re.compile(r'\b0\.\d+\b|\b1\.0\b')
    
        def replace_number(match, tier_name):
            num = float(match.group())
            if tier_name == "Prominence":
                if 0 <= num <= 0.4:
                    return " "  # Blank space
                elif 0.41 <= num <= 0.7:
                    return "?"
                elif 0.71 <= num <= 1:
                    return "*"
            elif tier_name == "Boundary":
                if 0 <= num <= 0.15:
                    return " "  # Blank space
                elif 0.16 <= num <= 0.29:
                    return "?"
                elif 0.3 <= num <= 1:
                    return "]"
            return match.group()
    
        for line in lines:
            match = tier_pattern.search(line)
            if match:
                current_tier = match.group(1)
                in_target_tier = current_tier in tiers
        
            if in_target_tier:
                line = number_pattern.sub(lambda m: replace_number(m, current_tier), line)
        
            modified_lines.append(line)
    
        with open(textgrid_path, "w", encoding="utf-8") as file:
            file.writelines(modified_lines)
    
        #print(f"Numbers in tiers {tiers} replaced based on the given ranges in {textgrid_path}")


        

        




# In[1]:


# In[ ]:




