# Exoplanet Simulator
# https://github.com/ProfShibe

import xml.etree.ElementTree as ET, urllib.request, gzip, io
from ursina import *
#######################################################
def main():
    # get input
    planet_name = get_exoplanet()

    # get info about planet
    data = get_object_data(planet_name)

    #display window then (it will open a blank window beforehand if not displayed after user input)
    app = Ursina(development_mode=False)

    # update function to spin planet must be outside main
    global planet

    #textures for the planet models
    textures = [ 
        'mercury.jpg',
        'saturn.jpg',
        'uranus.jpg',
        'mars.png',
        'neptune.jpg',
        'venus.jpg'
    ]
    #setup the window
    window.title = "Exoplanet Simulation"
    window.borderless = False
    window.fullscreen = False
    window.position = (100, 100)

    #background texture
    skybox_image = load_texture('gravity.jpg')
    #Sky(texture=skybox_image, scale = (1,1,1))

    #pick a random color and texture
    rgb_color = color.random_color()
    planet_texture = load_texture(random.choice(textures))

    #create a planet with random color and texture
    planet = Entity(model='sphere', color=rgb_color, texture=planet_texture, scale=(2, 2, 2))

    # place a plane behind the planet to display a background
    # skybox will be distorted so I used this instead.
    # Use a skybox and scale if you want user to be able to move around
    background = Entity(model='quad', texture=skybox_image, scale=(14, 7, 1), position=(0, 0, 5))

    
    #display planet info in window next to planet
    display_info(data)

    #set our camera angle
    camera.position = (0, 0, -10)
    camera.look_at(planet)

    app.run()
#######################################################
def get_exoplanet():  # Prompt user for an Exoplanet name
    exoplanet = input("Enter a planet: ")
    return exoplanet
#######################################################
#spin planet around every tick
def update(): 
    planet.rotation_x += .01
    planet.rotation_y += .01
    planet.rotation_z += .01
#######################################################
def get_object_data(p):  
    # Get GitHub (NASA) data about that planet
    url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
    response = urllib.request.urlopen(url)  # get and open URL

    with gzip.GzipFile(fileobj=io.BytesIO(response.read())) as f:
        oec = ET.parse(f)  # parse XML file

    # Find planet in github
    for planet in oec.findall(".//planet"):
        if planet.findtext("name") == p:
            # retrieve basic info of the planet
            mass = planet.findtext("mass") or "Unknown"
            radius = planet.findtext("radius") or "Unknown"
            sma = planet.findtext("semimajoraxis") or "Unknown"
            temp = planet.findtext("temperature") or "Unknown or fluctuating"
            desc = planet.findtext("description") or "Lacking information about planet"
            period = planet.findtext("period") or "Unknown"
            method = planet.findtext("discoverymethod") or "Lacking information or directly observed"
            # Neatly gather info
            info = (
                f"\n{p}: \n{desc}\n"
                f"Mass: {mass} Jupiter masses.\n"
                f"Radius: {radius} Jupiter Radii.\n"
                f"Average AU from Parent star: {sma}.\n" # SMA is not actually average but good enough
                f"Temperature: {temp} Kelvin.\n"
                f"Orbital Period: {period} days.\n"
                f"Discovery method: {method}."
            )

            # Return info based on length!
            if len(info) > 400:
                return format_info(info)
            else:
                return info

    return "No planet found! Have a random planet instead!" # Generate a random planet to play with
#######################################################
def format_info(data):  # squish the text down if its too detailed
    
    words = data.split()
    formatted = ""
    line = ""

    for word in words:
        if len(line) + len(word) > 80:
            formatted += line + "\n"
            line = word + " "
        else:
            line += word + " "

    formatted += line
    return formatted
#######################################################
def display_info(data):  # display planet info
    return Text(
        text = data,
        position = (0, 0.37),
        origin = (0, 0),
        scale = .6,
        background = True # text background so it's more readable
    )
#######################################################
if __name__ == "__main__":
    main()
#######################################################
