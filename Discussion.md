Solutions Considered

Using Different Path String Approaches

Backslash Escape: We initially considered using backslashes (e.g., "C:\\Users\\...") which requires escaping each backslash so Python doesn't interpret them as special characters.
Raw String Literals: Another option was using a raw string (e.g., r"C:\Users\..."). This also resolves escape issues in Windows-style paths.
Forward Slashes: We ended up using "C:/Users/..." because Python on Windows accepts forward slashes as valid path separators. This avoids escape-sequence problems and keeps the string readable.
File Extraction Approaches

zipfile + gzip vs. Third-Party Libraries: Python’s standard libraries zipfile and gzip were sufficient for the task of reading .zip and .gz content. We briefly considered third-party libraries like py7zr or pyzipper, but they weren’t necessary since our needs were met by the built-in modules.
Line Matching

Regex Matching vs. Prefix Checking: We chose Python’s built-in re to match lines that start with a date pattern using ^. Alternatively, we could have sliced the string or used str.startswith(), but regex is more flexible for future expansions (e.g., partial date, time stamps, etc.).
Final Solution Summary
We settled on a Python script that:

Uses zipfile to open a ZIP archive.
Iterates through .log and .gz files (using gzip where needed).
Applies a regex to match lines starting with the user-provided date.
Writes all matching lines to an output file in an output folder.
This solution is straightforward, maintainable, and relies solely on standard libraries. By using forward slashes, we avoid escape issues on Windows paths. By modularizing logic (e.g., validation checks, file-opening helpers), we keep the code readable and extensible.

Steps to Run

Open a Terminal/Command Prompt in your project directory.

(Optional) Create and activate a virtual environment:

bash
Copy
Edit
# Create a virtual environment named 'venv'
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Or (Windows CMD)
venv\Scripts\activate.bat

Save the Script as extract_logs.py (if it’s not already).

Make sure your ZIP file is located at the path specified in the code. In this example, it’s:

plaintext
Copy
Edit
C:/Users/YASHK/OneDrive/Desktop/Farmart/logs_2024.log.zip
Adjust the ZIP_ARCHIVE_PATH in the code if needed.

Run the script with the target date:

bash
Copy
Edit
python extract_logs.py 2024-12-01
Replace 2024-12-01 with the date you want to filter for.
Check the output:

A folder named output will be created (if it doesn’t already exist).
A file named output_<target_date>.txt will contain the filtered log lines.
