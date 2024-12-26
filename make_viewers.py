import os
import shutil

STEREO_JS_SOURCE='example/stereo.js'
SAVE_PATH = 'viewers'
PAIRS_USER_STUDY_PATH = "pairs-user-study"  # Relative path used inside <source>

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>360 stereo video</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <link type="text/css" rel="stylesheet" href="../css/main.css">
    <script type="importmap">
        {{
          "imports": {{
            "three": "https://cdn.jsdelivr.net/npm/three@0.166.1/build/three.module.js",
            "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.166.1/examples/jsm/"
          }}
        }}
    </script>
</head>
<body>
    <div id="container" style="position: absolute; top: 50%; left: 50%; 
         transform: translate(-50%, -50%); display: flex; 
         justify-content: center; align-items: center; width: auto; height: auto;">
    </div>
    
    <video id="video" loop muted crossorigin="anonymous" playsinline style="display:none">
      <!-- <source src="{commented_path}" type="video/mp4"> -->
      <source src="{actual_path}" type="video/mp4">
    </video>
    
    <script type="module" src="stereo.js"></script>
</body>
</html>
"""

def create_html(prompt_name: str, result: str) -> str:
    """
    Generate the HTML content for a given prompt and result.
    E.g. result can be 'ours' or 'depth_c'.
    """
    commented_path = f"../{PAIRS_USER_STUDY_PATH}/{prompt_name}/{result}.mp4"
    actual_path = f"../{PAIRS_USER_STUDY_PATH}/{prompt_name}/{result}.mp4"
    
    return HTML_TEMPLATE.format(
        commented_path=commented_path,
        actual_path=actual_path
    )

def main():
    # Go through each item in the video folder
    for prompt in os.listdir(PAIRS_USER_STUDY_PATH):
        prompt_path = os.path.join(PAIRS_USER_STUDY_PATH, prompt)
        
        # Skip if it's not a directory
        if not os.path.isdir(prompt_path):
            continue
        
        # We expect 'ours.mp4' and 'depth_c.mp4' inside each prompt directory
        ours_mp4 = os.path.join(prompt_path, "ours.mp4")
        depthc_mp4 = os.path.join(prompt_path, "depth_crafter.mp4")
        
        # Only proceed if both files exist
        if not (os.path.isfile(ours_mp4) and os.path.isfile(depthc_mp4)):
            continue
        
        # Create subfolders for each result type
        ours_folder = os.path.join(SAVE_PATH, f"{prompt}_ours")
        depthc_folder = os.path.join(SAVE_PATH, f"{prompt}_depthc")
        
        os.makedirs(ours_folder, exist_ok=True)
        os.makedirs(depthc_folder, exist_ok=True)
        
        # Generate the HTML for each result
        ours_html = create_html(prompt, "ours")
        depthc_html = create_html(prompt, "depth_c")
        
        # Write index.html into each subfolder
        with open(os.path.join(ours_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(ours_html)
        
        with open(os.path.join(depthc_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(depthc_html)
        
        # Copy stereo.js to each subfolder
        shutil.copy2(STEREO_JS_SOURCE, ours_folder)
        shutil.copy2(STEREO_JS_SOURCE, depthc_folder)
        print(f"Created HTML for prompt: {prompt}")

if __name__ == "__main__":
    main()