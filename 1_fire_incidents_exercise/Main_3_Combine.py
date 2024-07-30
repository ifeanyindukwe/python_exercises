import subprocess

def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")
        raise

if __name__ == "__main__":
    try:
        # Run the first script
        run_script('Main_1_ScrapyRunner.py')
        
        # If the first script succeeds, run the second script
        run_script('Main_2_AnalyzeData.py')
    except Exception as e:
        print(f"Execution halted due to error: {e}")
