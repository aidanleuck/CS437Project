import tkinter
from tkinter import *


# Function for checking the
# key pressed and updating
# the listbox
def checkkey(event):

    value = event.widget.get()
    print(value)

    # get data from l
    if value == '':
        # data = l
        data = ''
    else:
        data = []
        for item in l:
            if value.lower() in item.lower():
                data.append(item)

    # update data in listbox
    update(data)


def update(data):

    # clear previous data
    lb.delete(0, 'end')

    # put new data
    for item in data:
        lb.insert('end', item)


# Driver code
l = ('C','C++','Java', 'Python','Perl', 'PHP','ASP','JS', 'people', 'ugly','frighten','deer','lyrical','chalk','society','capture','pet','mine','push','zonked','overwrought','draconian','modify','disease','expand','billowy','can','range','glorious','satisfying','cannon','cooperative','key','spoon','rabbits','lock','verdant','library','harm','crooked','flippant','erect','download','powerful','modern','do','cluttered','pest','fluttering','snotty','comparison','sound','infuse','confess','miniature','dreary','animal','paint','honorable','delicious','structure','victorious','mundane','determine','horrible','riddle','savor','burly','range','cowardly','windy','hop','rural','warlike','infest','accurate','medical','sea','quince','tendency','follow','curb','smooth','empty','hole','toy','buzz','print','precious','tasty','alike','drive','crazy','battle','wooden','jar')

root = Tk()
root.title('Welcome')
root.geometry('400x300')
root.config(bg='#66cc00')

Label(
    root,
    bg='#66cc00',
    font = ('Times',21),
    text='Query Entry'
).pack()

#creating text box
Entry(
    root,
    width=40,
    font=('Times', 18),
).pack()
root.bind('<KeyRelease>', checkkey)

#creating list box
scrollbar = tkinter.Scrollbar(root, orient="vertical")
lb = Listbox(
    root,
    width=60,
    bg='#66cc00',
    yscrollcommand=scrollbar.set
)
scrollbar.config(command=lb.yview)
scrollbar.pack(side='right',fill="y")
lb.pack(side="left",fill="both",expand=True,padx=10,pady=10)

root.mainloop()
