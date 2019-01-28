
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: [REDACTED]
#    Student name: Ayden Hull
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files may be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Task Description-----------------------------------------------#
#
#  The Top Ten of Everything 
#
#  In this task you will combine your knowledge of HTMl/XML mark-up
#  languages with your skills in Python scripting, pattern matching
#  and Graphical User Interface design to produce a useful
#  application for accessing online data.  See the instruction
#  sheet accompanying this template for full details.
#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
#  Import the modules needed for this assignment.  You may not import
#  any other modules or rely on any other files.  All data and images
#  needed for your solution must be sourced from the Internet.
#

# Import the function for downloading web pages
from urllib import urlopen

# Import the regular expression function
from re import findall

# Import the Tkinter functions
from Tkinter import *

# Import Python's HTML parser
from HTMLParser import *



#--------------------------------------------------------------------#
#
#  Utility function:
#  Given the raw byte stream of a GIF image, return a Tkinter
#  PhotoImage object suitable for use as the 'image' attribute
#  in a Tkinter Label widget or any other such widget that
#  can display images.
#
def gif_to_PhotoImage(gif_image):

    # Encode the byte stream as a base-64 character string
    # (MIME Base 64 format)
    characters = raw_bytes.encode('base64', 'strict')

    # Return the result as a Tkinter PhotoImage
    return PhotoImage(data = characters)



#--------------------------------------------------------------------#
#
#  Utility function:
#  Given the raw byte stream of a JPG or PNG image, return a
#  Tkinter PhotoImage object suitable for use as the 'image'
#  attribute in a Tkinter Label widget or any other such widget
#  that can display images.  If positive integers are supplied for
#  the width and height (in pixels) the image will be resized
#  accordingly.
#
def image_to_PhotoImage(image, width = None, height = None):

    # Import the Python Imaging Library, if it exists
    try:
        from PIL import Image, ImageTk
    except:
        raise Exception, 'Python Imaging Library has not been installed properly!'

    # Import StringIO for character conversions
    from StringIO import StringIO

    # Convert the raw bytes into characters
    image_chars = StringIO(image)

    # Open the character string as a PIL image
    pil_image = Image.open(image_chars)
    
    # Resize the image, if a new size has been provided
    if type(width) == int and type(height) == int and width > 0 and height > 0:
        pil_image = pil_image.resize((width, height), Image.ANTIALIAS)

    # Return the result as a Tkinter PhotoImage
    return ImageTk.PhotoImage(pil_image)



#-----Student's Solution---------------------------------------------#
#
#  Complete the assignment by putting your solution below.
#
# The below imports are not necessary, just used to improve the
# functionality of the program. Commenting out the lines
# for imports continues to allow the program to work.
# I spoke with Colin about the imports, and he says they're fine as
# they are used to go above the requirements of the program.

# Used for the progress bar when downloading data
# Program works without importing either or both
import threading
from ttk import Progressbar

# Used to allow user to open the source in their default web browser
# Program works without importing
import webbrowser

# Used as a quick way to have a "range" with no end
# Program works without importing
import itertools

import sqlite3

# Create a replacement if itertools isn't imported
if not "itertools" in globals():
    class Object():
        pass

    def count(start = 0, step = 1):
        num = start

        while True:
            yield num

            num += step

    itertools = Object()
    itertools.count = count

PADDING = 5

# Scale an image proportionally into the width or height to either cover the dimensions, or contain it
def scaled_image(image, width = None, height = None, mode = "contain"):
    # Import the Python Imaging Library, if it exists
    try:
        from PIL import Image, ImageTk
    except:
        raise Exception, 'Python Imaging Library has not been installed properly!'

    # Import StringIO for character conversions
    from StringIO import StringIO

    # Convert the raw bytes into characters
    image_chars = StringIO(image)

    # Open the character string as a PIL image
    pil_image = Image.open(image_chars)

    if width != None or height != None:
        # Find the current size of the image
        curr_width, curr_height = pil_image.size
        ratio = float(curr_width) / float(curr_height)

        if width != None and height != None:
            if curr_width < width:
                curr_width = width
                curr_height = curr_width / ratio

            if curr_height < height:
                curr_height = height
                curr_width = curr_height * ratio

            if mode == "contain":
                if curr_width > width:
                    curr_width = width
                    curr_height = curr_width / ratio

                if curr_height > height:
                    curr_height = height
                    curr_width = curr_height * ratio
        elif width == None:
            curr_height = height
            curr_width = curr_height * ratio
        elif height == None:
            curr_width = width
            curr_height = curr_width / ratio

        curr_width = int(curr_width)
        curr_height = int(curr_height)

        pil_image = pil_image.resize((curr_width, curr_height), Image.ANTIALIAS)

    return ImageTk.PhotoImage(pil_image)

# A class that represents a HTML element
class Node():
    def __init__(self, tag, attrs):
        self.tag = tag
        self.children = []
        self.attrs = dict(attrs)
        self.data = ""

        self.class_name = ""
        self.id = ""

        for name, value in attrs:
            if name == "class":
                self.class_name = value
            elif name == "id":
                self.id = id
    def get_descendants(self):
        nodes = []

        def process(node):
            for child in node.children:
                nodes.append(child)
                process(child)

        process(self)

        return nodes
    def get_descendants_by_tag_name(self, tag_name):
        nodes = self.get_descendants()

        if tag_name == "*":
            return nodes
        
        return filter(lambda x: x.tag == tag_name, nodes)
    def get_descendants_by_class_name(self, class_name):
        nodes = self.get_descendants()

        def filter_class(node):
            classes = node.class_name.split(" ")

            return class_name in classes

        return filter(filter_class, nodes)
    def get_descendant_by_id(self, id):
        nodes = self.get_descendants()

        return filter(lambda x: x.id == id, nodes)

# A class to parse a HTML document into a tree
class TreeParser(HTMLParser):
    def __init__(self):
        self.root = None
        self.stack = []

        # Tags that can't contain content
        # https://www.w3.org/TR/html4/index/elements.html

        self.__self_closing_tags = ["area", "base", "basefont", "br", "col", "frame", "hr", "img", "input", "isindex", "link", "meta", "param"]

        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs, skip_close = False):
        # skip_close is used internally for self-closing tags
        node = Node(tag, attrs)

        if len(self.stack):
            self.stack[-1].children.append(node)
        else:
            self.root = node

        self.stack.append(node)

        if (tag in self.__self_closing_tags) and not skip_close:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        index = None

        # Traverse the stack backwards to find the matching close tag
        for i in xrange(len(self.stack) - 1, -1, -1):
            if self.stack[i].tag == tag:
                index = i
                break

        if index != None:
            self.stack = self.stack[:index]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, True)
        self.handle_endtag(tag)
    def handle_data(self, data):
        if len(self.stack):
            self.stack[-1].data += data
    def get_tree(self):
        return self.root

# Debug method to display a TreeParser instance
def print_tree(tree):
    class value():
        def __init__(self, val = None):
            self.val = val

    level = value(0)

    def print_node(level, node):
        attrs = ", ".join(["%s=%s" % (a, b) for a, b in node.attrs])

        print "%s+ %s" % (" " * level.val, node.tag)

        for child in node.children:
            level.val += 1
            print_node(level, child)
            level.val -= 1

    print_node(level, tree)

# Hold all the necessary data for a top 10 list
class Top10List():
    def __init__(self, name, image = "", items = None, url = None):
        if items == None:
            items = []

        self.name = name
        self.image = image
        self.items = items
        self.url = url

        self.bg = None
        self.fg = None
    def append(self, text):
        self.items.append(text)

# Create a get_source function that displays a progress bar while downloading
def get_source_factory(window):
    if "threading" in globals():
        # Another thread is used to actually download the data to avoid blocking the main thread
        class GetSource(threading.Thread):
            def __init__(self, url):
                self.url = url
                self.data = None

                threading.Thread.__init__(self)
            def run(self):
                self.data = urlopen(self.url).read()
    
    def get_source(url):
        # Create a popup to display the progress bar
        progress_popup = Toplevel(window)

        progress_popup.title("Loading...")

        display_url = url

        # Shorten the URL if it is too long
        if len(display_url) > 50:
            display_url = display_url[:47] + "..."

        # Display the URL
        label = Label(progress_popup, text = "Downloading %s" % display_url)

        label.pack(padx = PADDING, pady = PADDING)

        if "Progressbar" in globals():
            # Create a progress bar
            bar = Progressbar(progress_popup, orient = HORIZONTAL, mode = "indeterminate")

            bar.pack(expand = True, fill = BOTH, side = TOP, padx = PADDING, pady = PADDING)
            bar.start()

        window.config(cursor = "wait")
        window.update()

        # Lock the window
        progress_popup.focus_set()
        progress_popup.grab_set()
        progress_popup.transient(window)

        downloader = GetSource(url)

        downloader.start()

        # Wait for the file to finish downloading
        while downloader.is_alive():
            # Keep the main thread updated to avoid a not responding window
            window.update_idletasks()
            window.update()

            downloader.join(0.0001)

        # Close the popup dialog
        progress_popup.destroy()

        window.config(cursor = "")
        window.update()

        # Return the data to the calling function
        return downloader.data

    def get_source_normal(url):
        return urlopen(url).read()

    # Return the generated function
    if "threading" in globals():
        return get_source
    else:
        return get_source_normal

def top10_github():
    url = "https://github.com/trending"
    data = get_source(url)

    # Create a parser for the document
    parser = TreeParser()

    parser.feed(data)

    # Get the tree from the parser
    tree = parser.get_tree()

    # Find the list of repositories by its class
    repo_list = tree.get_descendants_by_class_name("repo-list")[0]

    # Create a Top10List with a title, a header image, and a url
    # Originally used the display picture of the first repo, but it's way too small
    top10 = Top10List("Top 10 Trending Repositories", "http://www.molecularecologist.com/wp-content/uploads/2013/11/github-logo.jpg", url = url)

    top10.bg = "#ffffff"

    # Done is used to only get the first 10 repositories
    done = 0

    for child in repo_list.children:
        if done < 10:
            name = child.get_descendants_by_class_name("repo-list-name")[0].get_descendants_by_tag_name("a")[0].attrs["href"]

            # Only get the author and the repository name
            matches = re.match(r"\/([^\/]+)\/([^\/]+)", name)

            name = matches.group(1) + "/" + matches.group(2)
            
            # Add the repository to the top10 list
            top10.append(name)

            done += 1
        else:
            # Avoid looping through the rest of the data
            break

    return top10

def top10_youtube():
    url = "https://www.youtube.com/feed/trending"
    data = get_source(url)

    # Create a parser for the document
    parser = TreeParser()

    parser.feed(data.decode("utf-8"))

    # Get the tree from the parser
    tree = parser.get_tree()

    # Get a list of videos. All the videos on the trending page have the below class
    videos = tree.get_descendants_by_class_name("expanded-shelf-content-item-wrapper")

    # Keep track of how many videos we've added
    done = 0

    # Create a Top10List with a title, and a url
    top10 = Top10List("Top 10 Trending YouTube Videos", "https://cdn3.iconfinder.com/data/icons/leaf/256/youtube.png", url = url)

    top10.bg = "#b62025"
    top10.fg = "#ffffff"

    for video in videos:
        # Find the video title
        title = video.get_descendants_by_class_name("yt-uix-tile-link")

        if done < 10:
            # Sometimes the video elements don't have any text, so skip those
            if len(title):
                top10.append(title[0].data)
                done += 1
        else:
            # Avoid looping through the rest of the data
            break

    return top10

def top10_asx_stocks():
    url = "http://www.marketindex.com.au/asx20"
    data = get_source(url)

    # Create a parser for the document
    parser = TreeParser()

    parser.feed(data.decode("utf-8"))

    # Get the tree from the parser
    tree = parser.get_tree()

    # Find the table contain stocks, it's the first one with the class .sortable
    stock_table = tree.get_descendants_by_class_name("sortable")[0].get_descendants_by_tag_name("tbody")[0]
    # Get every row in the table
    stocks = stock_table.get_descendants_by_tag_name("tr")

    # Create a Top10List with a title, a header image, and a url
    # The header image is hard coded in because the page does not have any images on it
    top10 = Top10List("Top 10 ASX Stocks", "https://askmeboy.com/wp-content/uploads/2014/09/List-your-Favorite-Companies-Under-Windows-8-Finance-App-Watchlist.png", url = url)

    top10.bg = "#008a00"
    top10.fg = "#ffffff"
    
    # Keep track of how many stocks we've gone over
    done = 0

    for stock in stocks:
        # Find the company name, removing whitespace on the start and end
        name = stock.get_descendants_by_tag_name("td")[2].data.strip()

        if done < 10:
            # Add the repository to the top 10 list
            top10.append(name)
            done += 1
        else:
            # Avoid looping through the rest of the data
            break

    return top10

# region HyperlinkManager
# Taken from http://effbot.org/zone/tkinter-text-hyperlink.htm
# Modified to use Label instead of Text
class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        
        self.text.configure(foreground="blue")
        self.text.bind("<Enter>", self._enter)
        self.text.bind("<Leave>", self._leave)
        self.text.bind("<Button-1>", self._click)

        self.action = lambda ev: None
    def _enter(self, ev):
        self.text.config(cursor="hand2")
    def _leave(self, ev):
        self.text.config(cursor="")
    def _click(self, ev):
        self.action(ev)
# endregion HyperlinkManager

# Create an exit function for the popups
def exit_factory(popup):
    def exit_fn():
        popup.destroy()

    return exit_fn

# Create a function to open a link
def open_link_factory(link):
    def open_link(event):
        webbrowser.open(link)

    def open_link_normal(event):
        pass
    
    if "webbrowser" in globals():
        return open_link
    else:
        return open_link_normal

def save_factory(top10):
    def save():
        # Open the database to save the top ten items
        conn = sqlite3.connect("top_ten.db")

        cursor = conn.cursor()

        # Remove existing data in the table
        cursor.execute("DROP TABLE IF EXISTS `Top_Ten`;")
        cursor.execute("CREATE TABLE `Top_Ten` (`Rank` INTEGER, `Description` TEXT, PRIMARY KEY (`Rank`));")

        # Keep track of the position of the item
        item_number = itertools.count(1)

        # Add each item to the database
        for item in top10.items:
            cursor.execute("INSERT INTO `Top_Ten` (`Rank`, `Description`) VALUES (?, ?);", (item_number.next(), item))

        # Save and close
        conn.commit()
        conn.close()

    return save

# Create a function that will create a popup for the top 10 list when called
def open_popup_factory(window, lister):
    def open_popup():
        # Get the data and the top 10 list
        top10 = lister()
        popup_header_img = scaled_image(get_source(top10.image), 333, 200, "contain")

        # Create the popup
        popup = Toplevel(window)

        # Let child labels use the same background and foreground
        if top10.bg != None:
            popup.configure(bg = top10.bg)

        popup.top10_foreground = "#000000"

        if top10.fg != None:
            popup.top10_foreground = top10.fg

        popup.configure(takefocus = True)
        popup.title(top10.name)

        # Keep track of what grid row we are at
        row_index = itertools.count()

        popup_header = Label(popup, image = popup_header_img, bg = popup["bg"])

        # The Python garbage collector destroys the image before it is displayed
        # http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        popup_header.__prevent_gc_collect = popup_header_img

        popup_header.grid(row = row_index.next(), column = 0, padx = PADDING, pady = PADDING, columnspan = 2)

        # Keep track of the position in the list
        item_number = itertools.count(1)
        
        # Add the items
        for text in top10.items:
            label = Label(popup, text = "%2d. %s" % (item_number.next(), text), bg = popup["bg"], fg = popup.top10_foreground)

            label.grid(row = row_index.next(), column = 0, padx = PADDING, pady = PADDING, columnspan = 2, sticky = W)

        button_row = row_index.next()
        
        # Add a way to exit the window
        exit_button = Button(popup, text = "Exit", command = exit_factory(popup), width = 15)

        exit_button.grid(row = button_row, column = 0, padx = PADDING, pady = PADDING)

        # A button to save the list
        save_button = Button(popup, text = "Save", command = save_factory(top10), width = 15)

        save_button.grid(row = button_row, column = 1, padx = PADDING, pady = PADDING)

        # Allow the user to find the source of the list
        link = Label(popup, text = top10.url, bg = popup["bg"])

        link_man = HyperlinkManager(link)
        link_man.action = open_link_factory(top10.url)

        link.grid(row = row_index.next(), column = 0, padx = PADDING, pady = PADDING, columnspan = 2)

        # Focus the window
        popup.focus_set()
        popup.transient(window)

    return open_popup

if __name__ == "__main__":
    # Create the main window
    splash_window = Tk()

    splash_window.title("Top 10")
    splash_window.configure(background = "#009ce5")

    column = itertools.count()

    # Create the get source function
    get_source = get_source_factory(splash_window)

    # Create the header image
    header_img_url = "https://0.s3.envato.com/files/167125872/Top-10.png"
    header_img = scaled_image(get_source(header_img_url))

    functions = [(top10_github, "GitHub"), (top10_youtube, "YouTube"), (top10_asx_stocks, "ASX Stocks")]
    function_count = len(functions)

    # Place the image on the splash window
    header = Label(splash_window, image = header_img, borderwidth = 0)

    header.grid(row = 0, column = 0, columnspan = function_count, padx = PADDING, pady = PADDING)

    # Add the buttons for the top 10 lists
    for lister, label in functions:
        # Frame's width and height are in pixels, so we use a frame to make square buttons
        frame = Frame(splash_window, width = 150, height = 150)

        frame.pack_propagate(0)

        # Create a button that fills the frame
        btn = Button(frame,
                     text = label,
                     command = open_popup_factory(splash_window, lister),
                     bg = "#002130",
                     fg = "#ffffff",
                     font = ("Segoe UI", 16, "bold"),
                     borderwidth = 0,
                     cursor = "hand2"
            )

        btn.pack(fill = BOTH, expand = True)

        frame.grid(row = 1, column = column.next(), padx = PADDING, pady = PADDING)

    splash_window.mainloop()

##### DEVELOP YOUR SOLUTION HERE #####
