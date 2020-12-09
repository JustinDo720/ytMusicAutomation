from tkinter import *
from tkinter import filedialog
from bs4 import *
import html5lib
import requests
from musicDownload import download_music
from collections import deque

all_yt_urls = []
one_download_dir = deque(maxlen=1)
# We set this to an empty string as a default value
one_download_dir.append('')


# all of our functions that we are going to use with tkinter
def display_url(event):
    yt_link = url_entry.get()
    # We are going to scrape for the name but we are going to use the url_entry as the link
    if yt_link != '':
        src = requests.get(yt_link).text
        soup = BeautifulSoup(src, 'html5lib')
        title = soup.find('title')
        trim_title = title.text.replace('- YouTube', "").rstrip()
        all_yt_urls.append({'url': yt_link, 'yt_name': trim_title})
        all_urls.insert(END, trim_title)
        url.set("")


def delete_url(event):
    url_to_delete = all_urls.get(ANCHOR)
    all_urls.delete(ANCHOR)
    for urls in all_yt_urls:
        if urls['yt_name'] == url_to_delete:
            all_yt_urls.remove(urls)


def download():
    print('Ready', all_yt_urls)
    # We are going to take down the download directory and since there is only one index we use [0]
    download_dir = one_download_dir[0]
    # If the root directory is blank then we use our default download directory
    if download_dir == '':
        print('Failed test')
        download_music(all_yt_urls)
    else:
        print('Test completed', download_dir)
        download_music(all_yt_urls, changed_dir=download_dir)


def download_from_playlist():

    def start_download():
        link = playlist_entry.get()
        download_dir = one_download_dir[0]
        if link != '':
            if download_dir:
                download_music(playlist_link=link, changed_dir=download_dir, multi_yt_url=None)
            else:
                download_music(playlist_link=link, multi_yt_url=None)

    playlist_root = Toplevel(root)
    playlist_root.title = 'Download Playlist'
    playlist_root.geometry('500x100')
    playlist_root.config(bg=COLOR)

    intro_text_playlist = 'Please enter the link of your youtube playlist below'
    intro_label_playlist = Label(playlist_root, text=intro_text_playlist, bg=COLOR, justify='center')
    intro_label_playlist.grid(row=0, column=1)

    playlist_entry = Entry(playlist_root, width=80, bg=COLOR)
    playlist_entry.grid(row=1, column=1)

    download_button_playlist = Button(playlist_root, text='Download', bg=COLOR, command= start_download)
    download_button_playlist.grid(row=2, column=1)


def change_download_dir():
    root.directory = filedialog.askdirectory()
    print(root.directory)
    one_download_dir.append(root.directory)

# We set up a root
root = Tk()
root.title('Music Download')
root.geometry('900x500')  # W,H
COLOR = 'snow'
root.config(bg=COLOR)
# The Title
title_name = 'Automated Music Download'
title_label = Label(root, text=title_name, bg=COLOR)
title_label.grid(row=0, column=1)
title_label.config(font=('Courier', 12))

# Introduction
intro_text = '''
Our program aims to reduce the time you take to download music. Usually you would do:
1. Head to youtube and find your music
2. Copy the link
3. Head to a youtube to mp3 converter website 
4. Enter in the link and then click download

We perform the steps as above but you won't have to do this for every single link. 
Rather, you just need to enter all your links here and we will take care of the rest :)

Please enter the name of your song and Url below.
Note: You can remove a link by double clicking'''
intro_label = Label(root, text=intro_text, bg=COLOR)
intro_label.grid(row=1, column=1)
intro_label.config(font=('Courier', 12))

# Url
url = StringVar()
url_entry = Entry(root, textvariable=url, bg=COLOR, width=80)
url_entry.grid(row=2, column=1)

# If a user presses enter we will save that url
url_entry.bind('<Return>', display_url)

# Display all the urls
all_urls = Listbox(root, background=COLOR, width=100, bd=0)
all_urls.grid(row=3, column=1)
all_urls.grid_propagate(0)
all_urls.config(highlightthickness=0)
all_urls.bind('<Double-Button>', delete_url)

# Change to download playlist mode
switch_to_playlist_mode = Button(root, command=download_from_playlist, text= 'Download from Playlist Here', bg=COLOR)
switch_to_playlist_mode.grid(row=4, column=1)


# Change Download Directory
switch_dir = Button(root, command=change_download_dir, bg=COLOR, text='Change Download Directory')
switch_dir.grid(row=5, column=1)

# Download Section
download_button = Button(root, text='Ready', bg=COLOR, command=download)
download_button.grid(row=6, column=1)

# This makes sure that the window does not close
root.mainloop()
