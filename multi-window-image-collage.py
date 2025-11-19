import subprocess
import os
import time
import argparse
import sys
import tkinter

total_images = 3
ZOOM_IN_AMOUNT = 2
files_to_destroy = []

app = tkinter.Tk()
screenwidth = app.winfo_screenwidth()
screenheight = app.winfo_screenheight()
app.destroy()

def create_html(width, length, xpos, ypos, image, file_name):
    script_path = os.path.abspath(__file__)
    directory = os.path.dirname(script_path)
    
    percent_right = (xpos / (100 - width)) * (100 * (ZOOM_IN_AMOUNT - 1) / ZOOM_IN_AMOUNT)

    path_image = image
    if os.path.exists(image):
        path_image = "file://" + image
    
    html_path = os.path.join(directory, file_name)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Python Generated Page</title>
    </head>
    <body>
        <div style="width:{ZOOM_IN_AMOUNT*100}%; height: {ZOOM_IN_AMOUNT*100}%; overflow: hidden; ">
            <img src="{path_image}" alt="image mashup" style="height:{length}%; object-fit: cover; margin-left: -{xpos * screenwidth}px; margin-top:-{ypos*screenheight}px">
        </div>
        <p>{html_path}</p>
        <p>screen width: {screenwidth}</p>
        <p>screen height: {screenheight}</p>
    </body>
    </html>
    """
    
    with open(file_name, "w") as f:
        f.write(html_content)
    try:
        subprocess.run(["/Applications/Firefox.app/Contents/MacOS/firefox",
        "--new-window",
        f"file://{html_path}"])
        #time.sleep(0.0005)
        MoveWindow(xpos, ypos, width, length)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("osascript command not found")

def MoveWindow(xpos, ypos, windowwidth, windowheight):        
   x = xpos * screenwidth 
   y = ypos * screenheight
   width = screenwidth * (windowwidth)
   height = screenheight * (windowheight)
   osascript = f'''
    tell application "System Events"
        tell process "Firefox"
            set frontmost to true
            set position of front window to {{{x}, {y}}}
            set size of front window to {{{width}, {height}}}
        end tell
    end tell
    ''' 
   subprocess.run(["osascript", "-e", osascript])
   

def delete_placeholders():
    script_path = os.path.abspath(__file__)
    directory = os.path.dirname(script_path)
    for i in files_to_destroy:
        html_path = os.path.join(directory, i)
        if os.path.exists(html_path):
            try:
                os.remove(html_path)
                print(f"File '{html_path}' deleted successfully.")
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}.")
        else:
            print(f"File '{html_path}' does not exist.")


if __name__ == "__main__":
    
    image = "https://www.nomadfoods.com/wp-content/uploads/2018/08/placeholder-1-e1533569576673-960x960.png"
    layout = "layout1.txt"
    if len(sys.argv) > 1:
        print("Arguments received:")
        for i, arg in enumerate(sys.argv):
            if i == 0:
                print(f"Script name: {arg}")
            elif i == 1:
                image = arg
            elif i == 2:
                layout = arg
    else:
        print("No command-line arguments provided.")

    windows_to_make = []
    with open(layout, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            words = stripped_line.split()
            
            if(words and words[0] == "Window"):
                windows_to_make.append({
                "Width":  words[1],
                "Height": words[2],
                "XPos":   words[3],
                "YPos":   words[4],})
    

    for i in range (len(windows_to_make)):
        files_to_destroy.append("output" + str(i))
        create_html (float(windows_to_make[i]["Width"]), float(windows_to_make[i]["Height"]), float(windows_to_make[i]["XPos"]), float(windows_to_make[i]["YPos"]), image, "output" + str(i))
    
    time.sleep(10)
    delete_placeholders()

