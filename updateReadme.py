import os
file_exists=os.path.isdir("graphs")

if file_exists:
    os.remove("README.md")
    
    with open("README.md","a") as fx:
        for image in os.listdir("graphs"):
            image_command=f"![{image}](graphs/{os.path.basename(image)})"
            # print(os.path.abspath(image))
            image_header=f"### {image}"
            fx.write(image_header+"\n")
            fx.write(image_command+"\n")
            