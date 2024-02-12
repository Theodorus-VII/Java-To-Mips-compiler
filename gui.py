import tkinter as tk
import subprocess
from j2m_parser import Parser

class Main:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()

        # Set the window title
        self.root.title("Java-MIPS Translator")

        # Make the window fullscreen
        self.root.state("zoomed")

        # Configure rows and columns to expand and fill available space
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=2)
        self.root.grid_rowconfigure(5, weight=1)

        # Create a label for the Java text box
        java_label = tk.Label(self.root, text="Java Code", font=("Arial", 14))
        java_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Create the Java text box
        self.java_text = tk.Text(self.root, width=90, height=20)
        self.java_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a Java output box
        java_output_label = tk.Label(self.root, text="Java Output", font=("Arial", 14))
        java_output_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.java_output = tk.Text(self.root, width=90, height=10, state=tk.DISABLED)
        self.java_output.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        # Create a line separator
        line = tk.Canvas(self.root, width=2, height=750, bg="gray")
        line.grid(row=0, column=1, rowspan=5, padx=5, pady=5, sticky="ns")

        # Create a label for the MIPS text box
        mips_label = tk.Label(self.root, text="MIPS Code", font=("Arial", 14))
        mips_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Create the MIPS text box
        self.mips_text = tk.Text(self.root, width=90, height=20, state=tk.NORMAL)
        self.mips_text.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        # Create a MIPS output box
        mips_output_label = tk.Label(self.root, text="MIPS Output", font=("Arial", 14))
        mips_output_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.mips_output = tk.Text(self.root, width=90, height=10, state=tk.DISABLED)
        self.mips_output.grid(row=4, column=2, padx=5, pady=5, sticky="nsew")

        # Create the Run Java button
        java_button = tk.Button(self.root, text="Run Java", command=self.run_java, width=10, height=2)
        java_button.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        # Create the Translate button
        translate_button = tk.Button(self.root, text="Translate", command=self.translate, width=10, height=2)
        translate_button.grid(row=6, column=0, padx=5, pady=5, sticky="e")

        # Create the Run MIPS button
        mips_button = tk.Button(self.root, text="Run MIPS", command=self.run_mips, width=10, height=2)
        mips_button.grid(row=6, column=2, padx=5, pady=5, sticky="w")

        # Create the Clear button
        clear_button = tk.Button(self.root, text="Clear", command=self.clear, width=10, height=2)
        clear_button.grid(row=6, column=2, padx=5, pady=5, sticky="e")

    def run_java(self):
        """
        Runs the Java code and displays the output in the Java output box.
        """
        java_code = self.java_text.get("1.0", tk.END)
        java_output = run_java_code(java_code)
        # print(java_output)
        self.java_output.config(state=tk.NORMAL)
        self.java_output.delete("1.0", tk.END)
        self.java_output.insert(tk.END, java_output)
        self.java_output.config(state=tk.DISABLED)

    def translate(self):
        """
        Translates the Java code to MIPS and displays the output in the MIPS Code box.
        """
        java_code = self.java_text.get("1.0", tk.END)
        mips_code = translate_to_mips(java_code)
        self.mips_text.delete("1.0", tk.END)
        self.mips_text.insert(tk.END, mips_code)

    def run_mips(self):
        mips_code = self.mips_text.get("1.0", tk.END)
        mips_output = run_mips_code(mips_code)
        self.mips_output.config(state=tk.NORMAL)
        self.mips_output.delete("1.0", tk.END)
        self.mips_output.insert(tk.END, mips_output)
        self.mips_output.config(state=tk.DISABLED)

    def clear(self):
        """
        Clears both the Java and MIPS text boxes and output boxes.
        """
        reset()
        self.java_text.delete("1.0", tk.END)
        self.java_output.config(state=tk.NORMAL)
        self.java_output.delete("1.0", tk.END)
        self.java_output.config(state=tk.DISABLED)
        self.mips_text.delete("1.0", tk.END)
        self.mips_output.config(state=tk.NORMAL)
        self.mips_output.delete("1.0", tk.END)
        self.mips_output.config(state=tk.DISABLED)


    def start(self):
        """
        Starts the GUI application.
        """
        self.root.mainloop()

import subprocess

def run_java_code(java_code):
    # Write the code to a file
    with open('java.java', 'w') as f:
        f.write(java_code)
    # Compile the code
    compile_result = subprocess.run(['javac', 'java.java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if compile_result.returncode != 0:
        # There was an error during compilation
        error_message = compile_result.stderr.strip()
        return error_message
    # Run the code and capture the output
    result = subprocess.run(['java', 'java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Return the output as a dictionary with separate keys for stdout and stderr
    return result.stdout + result.stderr



def run_mips_code(mips_code):
    # Write the code to a file
    with open('assembly.asm', 'w') as f:
        f.write(mips_code)
    
    # Run MARS as a subprocess
    result = subprocess.run(['java', '-jar', 'Mars4_5.jar', 'assembly.asm'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Return the output as a dictionary with separate keys for stdout and stderr
    return result.stdout + result.stderr

# def reset():
#     translator.reset()

def translate_to_mips(java_code):
    parser = Parser()
    return parser.parser(java_code)

app = Main()
app.start()
