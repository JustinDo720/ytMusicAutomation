from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from bs4 import *
from PIL import ImageTk, Image
import requests
from musicDownload import download_music
from musicSearch import search_for_music
from collections import deque
import os

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
    # if all_urls list exists
    if all_urls:
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


def start_download(event=None):
    link = playlist_entry.get()
    download_dir = one_download_dir[0]
    if link != '':
        if download_dir:
            download_music(playlist_link=link, changed_dir=download_dir, multi_yt_url=None)
        else:
            download_music(playlist_link=link, multi_yt_url=None)


def change_download_dir():
    root.directory = filedialog.askdirectory()
    print(root.directory)
    one_download_dir.append(root.directory)


def fetch_music(event=None):
    # This is the solution! Apparently without the global image var theres an issue displaying the image.
    global video_img1, video_img2, video_img3, video_img4, video_img5

    music_searched = search_bar.get()
    image_path = f'{os.getcwd()}\\yt_thumbnails\\'

    def confirm_choice(choice):
        global tk_choice_photo

        confirm_tab = Toplevel(root)
        confirm_tab.title = 'Confirm Choice'
        confirm_tab.geometry = '500x300'

        confirm_msg = f'Are you sure you want to download {choice["video_title"]}'
        tk_choice_photo = ImageTk.PhotoImage(Image.open(image_path + choice['video_photo']))

        confirm_label = Label(confirm_tab, image= tk_choice_photo, text=confirm_msg, compound='top')
        confirm_label.grid(row=0, column=2)

        decline_button = Button(confirm_tab, text='Decline')
        decline_button.grid(row=1, column=3)

        continue_button = Button(confirm_tab, text='Continue')
        continue_button.grid(row=1, column=1)

    if music_searched:
        # We are using the function imported from musicSearch.py which will return a list titles and their video id
        all_music = search_for_music(music_searched)

        # Option1
        video_img1 = ImageTk.PhotoImage(Image.open(f'{image_path}image_{1}.jpg'))
        video_title1 = all_music[0]['video_title']
        video_frame1 = Button(search_mode, image=video_img1, text=video_title1,
                              compound='top', width=450, height=200,
                              command= lambda: confirm_choice(all_music[0]))
        video_frame1.grid(row=5, column=1)

        # Option2
        video_img2 = ImageTk.PhotoImage(Image.open(f'{image_path}image_{2}.jpg'))
        video_title2 = all_music[1]['video_title']
        video_frame2 = Button(search_mode, image=video_img2, text=video_title2,
                              compound='top', width=450, height=200,
                              command= lambda: confirm_choice(all_music[1]))
        video_frame2.grid(row=6, column=1)

        # Option3
        video_img3 = ImageTk.PhotoImage(Image.open(f'{image_path}image_{3}.jpg'))
        video_title3 = all_music[2]['video_title']
        video_frame3 = Button(search_mode, image=video_img3, text=video_title3,
                              compound='top', width=450, height=200,
                              command= lambda: confirm_choice(all_music[2]))
        video_frame3.grid(row=7, column=1)


        # Option4
        video_img4 = ImageTk.PhotoImage(Image.open(f'{image_path}image_{4}.jpg'))
        video_title4 = all_music[3]['video_title']
        video_frame4 = Button(search_mode, image=video_img4, text=video_title4,
                              compound='top', width=450, height=200,
                              command= lambda: confirm_choice(all_music[3]))
        video_frame4.grid(row=8, column=1)


        # Option5
        video_img5 = ImageTk.PhotoImage(Image.open(f'{image_path}image_{5}.jpg'))
        video_title5 = all_music[4]['video_title']
        video_frame5 = Button(search_mode, image=video_img5, text=video_title5,
                              compound='top', width=450, height=200,
                              command= lambda: confirm_choice(all_music[4]))
        video_frame5.grid(row=9, column=1)


# We set up a root
root = Tk()
root.title('Music Download')
root.geometry('900x900')  # W,H
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
'''

intro_label = Label(root, text=intro_text, bg=COLOR)
intro_label.grid(row=1, column=1)
intro_label.config(font=('Courier', 12))


# Switch between modes
diff_modes = ttk.Notebook(root)
diff_modes.config(width=700, height=600)
download_mode = ttk.Frame(diff_modes, )
playlist_mode = ttk.Frame(diff_modes)
search_mode = ttk.Frame(diff_modes)

diff_modes.add(download_mode, text='Download Music with a link')
diff_modes.add(playlist_mode, text='Download Music with a playlist link')
diff_modes.add(search_mode, text='Search for Music to Download')

diff_modes.grid(row=2, column=1)

# <-- Download Music with a link Mode -->
# Url
instructions = '''
Please enter the name of your song and Url below.
Note: You can remove a link by double clicking'''
url = StringVar()
instruction_label = Label(download_mode, text=instructions)
instruction_label.grid(row=0, column=1)

url_entry = Entry(download_mode, textvariable=url, bg=COLOR, width=80)
url_entry.grid(row=1, column=1)

# If a user presses enter we will save that url
url_entry.bind('<Return>', display_url)

# ScrollWheel for the ListBox
all_urls_scrollbar = Scrollbar(download_mode, orient='vertical')
all_urls_scrollbar.grid(row=2, column=2, sticky=NE)

# Display all the urls
all_urls = Listbox(download_mode, yscrollcommand= all_urls_scrollbar.set, width=100, height=10, bd=0)
all_urls.grid(row=2, column=1)
all_urls.grid_propagate(0)
all_urls.config(highlightthickness=0, scrollregion=all_urls.bbox(5))
all_urls.bind('<Double-Button>', delete_url)
all_urls_scrollbar.config(command=all_urls.yview)

# Download Section
download_button = Button(download_mode, text='Ready', bg=COLOR, command=download)
download_button.grid(row=4, column=1)

# Change Download Directory
switch_dir = Button(download_mode, command=change_download_dir, bg=COLOR, text='Change Download Directory')
switch_dir.grid(row=3, column=1)

# <-- End Download Music with a link Mode -->


# <-- Download Music with a playlist link -->

intro_text_playlist = 'Please enter the link of your youtube playlist below'
intro_label_playlist = Label(playlist_mode, text=intro_text_playlist, bg=COLOR, justify='center')
intro_label_playlist.grid(row=0, column=1)

playlist_entry = Entry(playlist_mode, width=80, bg=COLOR)
playlist_entry.grid(row=1, column=1)
playlist_entry.bind('<Return>', start_download)

download_button_playlist = Button(playlist_mode, text='Download', bg=COLOR, command=start_download)
download_button_playlist.grid(row=2, column=1)


# <-- End Download Music with a playlist link -->

# <-- Search for Music to Download -->

# Instructions
instruction_message = 'Please type the name of the author and also the song for us to search up'
instruction_display = Label(search_mode, text=instruction_message, bg=COLOR)
instruction_display.grid(row=0, column=1)

# Search bar for users to search for a video to download
search_bar = Entry(search_mode, width=80, bg=COLOR)
search_bar.grid(row=1, column=1)
search_bar.bind('<Return>', fetch_music)

# Search Button
search_button = Button(search_mode, text='Search', bg=COLOR, command=fetch_music)
search_button.grid(row=2, column=1)

# <-- End Search for Music to Download -->
# This makes sure that the window does not close
root.mainloop()
