from tkinter import *
from bs4 import *
import html5lib
import requests


# all of our functions that we are going to use with tkinter
def display_url(event):
    yt_link = url_entry.get()
    # We are going to scrape for the name but we are going to use the url_entry as the link
    if yt_link != '':
        src = requests.get(yt_link).text
        soup = BeautifulSoup(src, 'html5lib')
        title = soup.find('title')
        trim_title = title.text.replace('- YouTube', "").rstrip()
        all_urls.insert(END, trim_title)
        url.set("")


def delete_url(event):
    all_urls.delete(ANCHOR)


def download():
    print('Ready')


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

# Download Section
download_button = Button(root, text='Ready', bg=COLOR, command=download)
download_button.grid(row=4, column=1)

# This makes sure that the window does not close
root.mainloop()
