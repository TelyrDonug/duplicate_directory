import os
import shutil
import subprocess

def duplicate_directory(src_dir, base_dest_dir, num_duplicates):
    # Check if the source directory exists
    if not os.path.exists(src_dir):
        print(f"Source directory '{src_dir}' does not exist.")
        return

    # Create the base destination directory if it doesn't exist
    if not os.path.exists(base_dest_dir):
        os.makedirs(base_dest_dir)

    # Define the starting value for the incrementing argument
    start_value = 0

    # Iterate to create duplicates
    for i in range(1, num_duplicates + 1):
        new_dest_dir = f"{base_dest_dir}.{i}"
        if os.path.exists(new_dest_dir):
            print(f"Directory '{new_dest_dir}' already exists. Skipping...")
            continue
        shutil.copytree(src_dir, new_dest_dir)
        print(f"Directory '{src_dir}' duplicated to '{new_dest_dir}'")

        # Calculate the value for the incrementing argument
        argument_value = start_value + (i - 1) * (2**16)

        # Run MATLAB script with arguments
        matlab_script = os.path.join(new_dest_dir, "tb_verilog", "script.m")
        if os.path.exists(matlab_script):
            print(f"Running MATLAB script '{matlab_script}' with argument value '{argument_value}'...")
            # Specify your MATLAB script arguments here
            script_arguments = [f"arg1", f"arg2", f"{argument_value}"]
            subprocess.run(["matlab", "-batch", f"run('{matlab_script}', {script_arguments})"])

        # Remove files with the suffix *.v_notused from tb_verilog directory
        tb_verilog_dir = os.path.join(new_dest_dir, "tb_verilog")
        if os.path.exists(tb_verilog_dir):
            for file_name in os.listdir(tb_verilog_dir):
                if file_name.endswith(".v_notused"):
                    file_path = os.path.join(tb_verilog_dir, file_name)
                    os.remove(file_path)
                    print(f"Removed file '{file_path}'")

# Example usage:
source_directory = "dected.1"
base_destination_directory = "dected"
number_of_duplicates = 5

duplicate_directory(source_directory, base_destination_directory, number_of_duplicates)
