import os
import re
import copy
import shutil

distance = 8
number_of_frames = 3
object_movement_interval = distance / number_of_frames

script_list = ["main0.pbrt", "main1.pbrt", "main2.pbrt", "main3.pbrt", "main4.pbrt"]
script_list = ["main1.pbrt"]

c1_tag_current_value_list = [];
c2_tag_current_value_list = [];
c3_tag_current_value_list = [];

for script in script_list:

    # find and record initial values of x-axis in the script
    with open(script, "r") as f:
        content = f.read()

    # recording all tags index wise
    # these will be replaced with x-axis values
    c1_tag_list = re.findall(r"\$c1&-?\d+\$", content)
    c2_tag_list = re.findall(r"\$c2&-?\d+\$", content)
    c3_tag_list = re.findall(r"\$c3&-?\d+\$", content)
    
    for c1_tag in c1_tag_list:
        c1_tag_current_value = c1_tag.split("&")[1].split("$")[0]
        c1_tag_current_value_list.append(c1_tag_current_value)
        
    for c2_tag in c2_tag_list:
        c2_tag_current_value = c2_tag.split("&")[1].split("$")[0]
        c2_tag_current_value_list.append(c2_tag_current_value)
        
    for c3_tag in c3_tag_list:
        c3_tag_current_value = c3_tag.split("&")[1].split("$")[0]
        c3_tag_current_value_list.append(c3_tag_current_value)
    
    # all initial values of x-axis are recorded index wise
    combined_tag_list = c1_tag_list + c2_tag_list + c3_tag_list
    combined_current_value_list = c1_tag_current_value_list + c2_tag_current_value_list + c3_tag_current_value_list

    render_script_name = script.split(".")[0]
    render_folder_name = f"{render_script_name}_renders" 

    for n_frame in range(number_of_frames):
        new_content = copy.deepcopy(content)
        # replace tags with new x-axis values
        for index, tag in enumerate(combined_tag_list):
            current_value = combined_current_value_list[index]
            new_content = new_content.replace(tag, current_value)
            combined_current_value_list[index] = str(float(current_value) + object_movement_interval)
        
        script_name = f"frame{n_frame}.pbrt"
        script_save_path = f"Renders/{render_folder_name}/scripts/frame{n_frame}.pbrt"
        frame_save_path = f"Renders/{render_folder_name}/frames/frame{n_frame}.png"
        
        with open(script_name, "w") as f:
            f.write(new_content)
        
        cmd = f"C:\\Users\\hassa\\Studies\\IDIG4002\\pbrt-v3\\build\\Release\\pbrt.exe {script_name}"
        os.system(cmd)

        shutil.move(f"new_frame.png", frame_save_path)
        shutil.move(script_name, script_save_path)
    

    
