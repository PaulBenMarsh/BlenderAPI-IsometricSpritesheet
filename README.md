# BlenderAPI-IsometricSpritesheet


A Python script which uses the Blender API to generate an isometric (technically dimetric) projection 2D spritesheet of a 3D animation.
For a walk cycle containing 24 frames, and 8 different viewing directions, this script will pan and orbit the orthographic camera around the origin of the scene at 360°/8 degree intervals, rendering the entire walk cycle once for each pass into seperate images. The images are then merged into a final composite spritesheet image using a glob pattern and the Python Imaging Library.

I made this script to automate the spritesheet rendering process for my Godot GDscript game project <a href="https://github.com/PaulBenMarsh/Isometric">"Isometric"</a>.

<p align="center">
<img src="https://github.com/PaulBenMarsh/BlenderAPI-IsometricSpritesheet/blob/master/screenshots/loop.gif?raw=true">
</p>

<p align="center">
<img src="https://github.com/PaulBenMarsh/BlenderAPI-IsometricSpritesheet/blob/master/screenshots/spritesheet_000_walk_24x8.png?raw=true">
</p>
