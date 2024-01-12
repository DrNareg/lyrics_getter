# Import important modules
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import os

# Structure site link
def get_site():

    artist_name = input("Enter artist name: ")
    # Lowercasing to make sure urls work
    artist_name = artist_name.lower()
    artist_name = artist_name.replace(" ", "")

    song_title = input("Enter song title: ")
    # Lowercasing to make sure urls work
    song_title = song_title.lower()

    # Create artist link
    site = "https://www.azlyrics.com/"+artist_name[0]+"/"+artist_name+".html"

    return site, song_title

# Web scraping part
def silky_soup(site):

    # Checking that the website is reachable
    page = requests.get(site)

    # Create our soup, (Raw html text, method of parsing)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Gathers all the songs
    songs = soup.find_all('div', attrs={"class": "listalbum-item"})

    # Make a list of all the links
    links = re.findall(r'href="([^"]+)"', str(songs))

    return links

# Function to find closest link to a song
def find_best_fitting_link(song_title, links):
    # Split user input into individual words
    input_words = song_title.lower().split()

    best_fitting_link = None
    max_matches = 0

    # Loop through all the links 
    for link in links:

        # Count the number of matching words
        matches = 0
        # Loop through user's input
        for word in input_words:
            if word in link:
                matches += 1

        # Update best fitting link if the current link has more matches
        if matches > max_matches:
            max_matches = matches
            best_fitting_link = link


    if best_fitting_link:
        return best_fitting_link
    else:
        print("Could not find the song")
    

# Getting the lyrics of a song
def get_lyrics(best_fitting_link):
 
    # Checking that the website is reachable
    lyrics_page = requests.get(best_fitting_link)

    # Create our soup, (Raw html text, method of parsing)
    lyrical_soup = BeautifulSoup(lyrics_page.text, 'html.parser') 

    # Find the div containing the lyrics using its selector 
    lyrics_div = lyrical_soup.select('body > div.container.main-page > div.row > div.col-xs-12.col-lg-8.text-center > div:nth-child(8)')

    # Extract text within the div
    if lyrics_div:
        lyrics_text = lyrics_div[0].get_text()
    else:
        lyrics_text = "Lyrics not found."

    return lyrics_text

def save_to_file(lyrics_text):
    
    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the file path in the current directory
    output_file_path = os.path.join(current_directory, "lyrics.txt")

    # Save lyrics to a text file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(lyrics_text)

    print(f"Lyrics saved to {output_file_path}")

# Gather data and such
site, song_title = get_site()
links = silky_soup(site)
best_fitting_link = find_best_fitting_link(song_title, links)

# Create full link to lyrics page
best_fitting_link = "https://www.azlyrics.com"+best_fitting_link

# Extract lyrics
lyrics_text = get_lyrics(best_fitting_link)

# Save lyrics to a .txt file
save_to_file(lyrics_text)
