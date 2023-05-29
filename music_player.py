from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import webbrowser

root = Tk()
root.title('Mandana.musicplayer ')
root.iconbitmap('C:/Users/mandana/Tkinterpro/manii.ico')
root.geometry("1000x650")
root.configure(background="black")

# define image
bg = PhotoImage(file="C:/Users/mandana/Tkinterpro/images/adelle.png")
# create a label
my_label = Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)
pygame.mixer.init()
# grab song length time info
def play_time():
	# check for double timing
	if stopped:
		return
	# grab current song elapsed time 
	current_time = pygame.mixer.music.get_pos() / 1000
	# convert to time format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
	# grab song title from playlist
	song = song_box.get(ACTIVE)
	# add directory structure and mp3 to song tittle
	song = f'C:/Users/mandana/Tkinterpro/audios/{song}.mp3'
	# load song with mutagen
	song_mut = MP3(song)
	# get song length
	global song_length
	song_length = song_mut.info.length
	# convert to time format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
	# increase current time by 1 second
	current_time += 1
	if int(my_slider.get()) == int(song_length):
		status_bar.config(text=f' {converted_song_length}  ')

	elif paused:
		pass
	elif int(my_slider.get()) == int(current_time):
		# update slider to position
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(current_time))

	else:
		# update slider to position
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(my_slider.get()))

		# convert to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
		# output time to status bar
		status_bar.config(text=f' {converted_current_time} of {converted_song_length}  ')
		# move this thing along by one second
		next_time = int(my_slider.get()) + 1
		my_slider.config(value=next_time)
	# update time
	status_bar.after(1000, play_time)

# add many songs to playlist
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='C:/Users/mandana/Tkinterpro/audios', title="choose a song", filetypes=(("mp3 Files", "*.mp3"),))
	# loop thru song list and replace directory info and mp3
	for song in songs:
		song = song.replace("C:/Users/mandana/Tkinterpro/audios/", "")
		song = song.replace(".mp3", "")
		# insert into playlist
		song_box.insert(END, song)

# play selected song
def play():
	# set stopped variable to false so song can play
	global stopped
	stopped = False
	song = song_box.get(ACTIVE)
	song = f'C:/Users/mandana/Tkinterpro/audios/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	# call the play_time function to get song length
	play_time()
	# # update slider to position
	slider_position = int(song_length)
	my_slider.config(to=slider_position, value=0)

# stop playing current song
global stopped
stopped = False
def stop():
	# reset slider and status bar
	status_bar.config(text='')
	my_slider.config(value=0)
	# stop song from playing
	pygame.mixer.music.stop()
	song_box.selection_clear(ACTIVE)
	# Clear the status bar
	status_bar.config(text='')
	# set stop variable to true
	global stopped
	stopped = True

# play the next song in the playlist
def next_song():
	# reset slider and status bar
	status_bar.config(text='')
	my_slider.config(value=0)
	# get the current song tuple number
	next_one = song_box.curselection()
	# add one to the current song number
	next_one = next_one[0]+1
	# grab song title from playlist
	song = song_box.get(next_one)
	# add directory structure and mp3 to song tittle
	song = f'C:/Users/mandana/Tkinterpro/audios/{song}.mp3'
	# load and play song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	# clear active bar in playlist listbox
	song_box.selection_clear(0, END)
	# activate new song bar
	song_box.activate(next_one)
	# set active bar to next song
	song_box.selection_set(next_one, last=None)

# play previous song in playlist
def previous_song():
	# reset slider and status bar
	status_bar.config(text='')
	my_slider.config(value=0)
	# get the current song tuple number
	next_one = song_box.curselection()
	# add one to the current song number
	next_one = next_one[0]-1
	# grab song title from playlist
	song = song_box.get(next_one)
	# add directory structure and mp3 to song tittle
	song = f'C:/Users/mandana/Tkinterpro/audios/{song}.mp3'
	# load and play song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# clear active bar in playlist listbox
	song_box.selection_clear(0, END)

	# activate new song bar
	song_box.activate(next_one)

	# set active bar to next song
	song_box.selection_set(next_one, last=None)

# delete a song
def delete_song():
	stop()
	# delete currently selected song
	song_box.delete(ANCHOR)
	# stop music if it's playing
	pygame.mixer.music.stop()

# delete all songs from playlist
def delete_all_songs():
	stop()
	#delete all songs
	song_box.delete(0, END)
	# stop music if it's playing
	pygame.mixer.music.stop()

# create global pause variable
global paused
paused = False
# pause and unpause the current song
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		# unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		# pause
		pygame.mixer.music.pause()
		paused = True

#create slider fuction
def slide(x):
	song = song_box.get(ACTIVE)
	song = f'C:/Users/mandana/manipro/audios/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

# create volume function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())
	
	# get current volume
	current_volume = pygame.mixer.music.get_volume()
	current_volume = current_volume * 100
	#change volume meter picture
	if int(current_volume) <= 33 :
		volume_meter.config(image=vol0)
	elif int(current_volume) >33 and int(current_volume) <= 70:
		volume_meter.config(image=vol1)
	elif int(current_volume) > 70 and int(current_volume) <= 100:
		volume_meter.config(image=vol2)

def open_browser(e):
	# open specific browser
	webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open_new_tab("https://google.com")
my_button = Button(root, text="open web browser!",font=("helvetica", 10), command=lambda: open_browser(0),bg="black",fg="white",bd=0)
my_button.grid(row=3, column=4)

# creare playlist box
song_box = Listbox(root, bg = "black",fg="white", width=35,relief=FLAT,height = 22, font=("helvetica",10),selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=4,padx=5, pady=1, rowspan=5 )

# define player control buttons images
back_btn_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/back1.png')
pause_btn_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/pause1.png')
play_btn_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/p1.png')
stop_btn_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/stop1.png')
forward_btn_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/for1.png')

# define volume control images
global vol0
global vol1
global vol2
vol0 = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/1.png')
vol1= PhotoImage(file='C:/Users/mandana/Tkinterpro/images/2.png')
vol2= PhotoImage(file='C:/Users/mandana/Tkinterpro/images/3.png')


# create volume label frame
frame = LabelFrame(root,bg="black",  relief=FLAT)
# frame.pack(fill="both", expand="yes")
frame.grid(row=11, column=0 ,columnspan=45, sticky=SE, padx=0,pady=8, ipadx=100)

button_frame = LabelFrame(frame, bg="black", relief=FLAT)
button_frame.grid(row=1, column=4)
# create volume meter
volume_meter = Label(frame,image=vol2, bd=0)
volume_meter.grid(row=1, column=7)

# create player control buttons
back_button = Button(button_frame, image = back_btn_img, borderwidth=0, command=previous_song, bd=0)
forward_button = Button(button_frame, image = forward_btn_img, borderwidth=0, command=next_song,bd=0)
play_button = Button(button_frame, image= play_btn_img, borderwidth=0, command=play, bd=0)
pause_button = Button(button_frame, image= pause_btn_img, borderwidth=0, command=lambda: pause(paused), bd=0)
stop_button = Button(button_frame, image= stop_btn_img, borderwidth=0, command=stop,bd=0)

back_button.grid(row=0, column=0)
forward_button.grid(row=0, column=4)
play_button.grid(row=0, column=2 )
pause_button.grid(row=0, column=1)
stop_button.grid(row=0, column=3)

# create status bar
status_bar = Label(frame, text='', bd=0, relief=GROOVE, anchor=E, bg="black", fg="white")
status_bar.grid(row=1, column=0 )

# create music position slider
my_slider = ttk.Scale(frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide,length=950 )
my_slider.grid(row=0, column=0,pady=10, ipadx=30, columnspan=8)

# create volume slider
volume_slider = ttk.Scale(frame, from_=0, to=1, orient=HORIZONTAL, value=1, command=volume, length=125)
volume_slider.grid(row=1, column=6)

# add labels for artists part
artist = Label(root, text="Albums", fg="white", bg="black", width=20, font=("helvetica", 12))
artist.grid(row=1, column=0, padx=5, pady=5)
art_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/art.png')
artist = Label(root, text="",image=art_img, fg="white", bg="black")
artist.grid(row=0, column=0,padx=5, pady=10)

art_frame = LabelFrame(root, bg="black", relief=FLAT)
art_frame.grid(row=2, column=0, padx=30)

mik_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/mik.png')
mik_button = Button(art_frame,text="" ,image= mik_img, command=add_many_songs)
mik_button.grid(row=0, column=0 )

adele_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/adele.png')
adele_button = Button(art_frame,text="" ,image= adele_img, command=add_many_songs)
adele_button.grid(row=0, column=1 )

hans_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/hans.png')
hans_button = Button(art_frame,text="" ,image= hans_img, command=add_many_songs)
hans_button.grid(row=0, column=2 )

shajarian_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/shajarian.png')
shajarian_button = Button(art_frame,text="" ,image= shajarian_img, command=add_many_songs)
shajarian_button.grid(row=1, column=0 )

jlo_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/jlo.png')
jlo_button = Button(art_frame,text="" ,image= jlo_img, command=add_many_songs)
jlo_button.grid(row=1, column=1 )

hyede_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/hyede.png')
hyede_button = Button(art_frame,text="" ,image= hyede_img, command=add_many_songs)
hyede_button.grid(row=1, column=2 )

hich_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/Hichkas.png')
hich_button = Button(art_frame,text="" ,image= hich_img, command=add_many_songs)
hich_button.grid(row=2, column=0 )

yas_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/yas.png')
yas_button = Button(art_frame,text="" ,image= yas_img, command=add_many_songs)
yas_button.grid(row=2, column=1 )

shakira_img = PhotoImage(file='C:/Users/mandana/Tkinterpro/images/shakira.png')
shakira_button = Button(art_frame,text="" ,image= shakira_img, command=add_many_songs)
shakira_button.grid(row=2, column=2 )

delete_all_button = Button(root,text="delete all songs" ,font=("helvetica", 10),bg="black",fg="white", bd=0 ,command=delete_all_songs)
delete_all_button.grid(row=4, column=4 )

delete_button = Button(root,text="delete song" ,font=("helvetica", 10),bg="black",fg="white", bd=0 ,command=delete_song)
delete_button.grid(row=5, column=4 )
root.mainloop()
