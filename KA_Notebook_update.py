from tkinter import *
class MyNotebook(Frame):
    def __init__(self,*args,**kwargs):
        """
            This Notebook widget is used to give you control on tab switching.
            You can easily create new tabs manually or dynamically using this.
            Alrights are reserved to Kanwar Adnan.
         """

        """ Example:
        from tkinter import * # Importing every class from module.
        from KA_notebook import MyNotebook # Importing MyNotebook class from module

        root = Tk()
        nb = MyNotebook(root)
        nb.pack(fill = 'both' , expand = True)

        page1 = Frame(nb,bg='red')
        page2 = Frame(nb,bg='green')

        nb.add(page1,'page1')
        nb.add(page2,'page2')

        nb.show(1)
        nb.enabletraversal(root)
        root.mainloop()
        """

        # Calling Frame init
        Frame.__init__(self,*args,**kwargs)

        # Frame to hold Buttons i.e Tabs
        self.header = Frame(self)
        self.header.pack(side='top',fill='x')

        # Local Variables
        self.current = None
        self.side = None
        self.fill = None

        # Used to store the location of Buttons i.e Tabs
        self.btnslocations = {}

        # Used to store Button's i.e. tab's additional settings
        self.taboptions = {}

        # Default Styling Dictonary
        self.nbcolors = {'bg' : '#097FC8' , 'bd' : 0 , 'fg' : 'white' , 'fieldbackground' : '#097FC8' ,
                        'tabbg' : '#0866A1','activebackground':'#097FC8','activeforeground' : 'white'
                        }

        # Default Styling Color for focused Buttons i.e Tabs
        self.hovcolors = {'focusbg':'#109DF4'}

        # Used to store all the frames
        self.frames = []

        # Used to store the buttons i.e Tabs
        self.btns = []

        # Used to store total Indexes of Tabs
        self.totalTabs = []

        # Used to indexes of Hidden Tabs
        self.hiddentabs = []

        # Used to store indexes of Active Tabs
        self.activetabs = []

        # Used  to store the names of the Tabs
        self.framenames = []

        # Used to store IntVar() for menu checkbuttons
        self.Vars = []

        # Binding menu to objects
        self.bind("<Button-3>" , self.popup)
        self.header.bind("<Button-3>" , self.popup)

        # Menu object
        self.popup_menu = Menu(self.header, tearoff=0)

    def add(self,frame,text,limit=None,*args,**kwargs):
        """ This method adds a new tab to notebook whether it's created dynamically or manually. """

        if self.side == 'bottom' or self.side=='top' or self.side == None:
            self.btnslocations[len(self.totalTabs)] = {'row' : 0 , 'column' : len(self.totalTabs)}
        else:
            self.btnslocations[len(self.totalTabs)] = {'column' : 0 , 'row' : len(self.totalTabs)}

        # Making Button/Tab
        self.button = Button(self.header,text=text,*args,**kwargs)
        self.button.grid(**self.btnslocations[len(self.totalTabs)])

        # Making Button/Tab able to switch frames
        self.button.config(command = lambda : self.display(frame=frame))

        # Binding Menu to Current Button/Tab 
        self.button.bind("<Button-3>" , self.popup)

        # Adding data to iterables

        # These store the indexes
        self.totalTabs.append(len(self.frames))
        self.activetabs.append(self.totalTabs[-1])

        # These store the information
        self.frames.append(frame)
        self.btns.append(self.button)
        self.framenames.append(text)

        # Making dynamic Variable for checkbutton of menu
        self.var = IntVar(value=1)

        # Storing this variable in list so it shouldnt lost.
        self.Vars.append(self.var)

        # Adding Labels to Menu
        self.popup_menu.add_checkbutton(label=self.btns[self.frames.index(frame)]['text'], command = lambda : self.menu(self.frames.index(frame)) , variable=self.var)

        # Binding functions to current Button/Tab
        self.button.bind("<Enter>",lambda e :self.focusIn(e,frame))
        self.button.bind("<Button-1>",lambda e :self.focused(e,frame))
        self.button.bind("<Leave>",lambda e :self.focusOut(e,frame))

    def hide_all_frames(self):
        """ Hides all the of its children. """
        for frame in self.frames:
            frame.pack_forget()

    def display(self,frame):
        """ Displays a required frame. """
        self.hide_all_frames()
        self.current = self.frames.index(frame)
        frame.pack(fill='both',expand=True)
        self.style(**self.nbcolors)        

    def open(self,text='Untitled'):
        """ This method is used to dynamically add a new tab to notebook."""
        # Making a new dynamic Tab
        newtab = self.add(Frame(self),text)

        # Calling style method to apply current theme to new tab/button
        self.style(**self.nbcolors)

        # Returning the newtab object so it may be used by user to perform tasks.
        return newtab

    def show(self,index):
        """
            This method is used to display a desired tab using it's index.
            Note just for setting current tab manually you should be using
            1 as the current tab.
                nb.show(1) """
        if index in self.activetabs:
                self.display(self.winfo_children()[index])
        else:
            if index>len(self.activetabs):
                self.display(self.frames[self.activetabs[-1]])
            else:
                self.display(self.frames[self.activetabs[0]])

    def hide(self,index,tabindex=None):
        """ This method hides a specific tab using that tab's index, You can also
            give tabindex to automatically display the tab if active tab was removed
            or the programm will automatically select new tab to display. """

        if index in self.totalTabs:
            self.frames[index].pack_forget()
            self.btns[index].grid_forget()
            self.Vars[index].set(0)

        if not index in self.hiddentabs:
            self.hiddentabs.append(index)
            self.activetabs.remove(index)
            if tabindex in self.totalTabs:
                self.display(self.frames[tabindex])
            else:
                index = self.provide_index(index+1)
                self.display(self.frames[index])
        else:
            self.error('hide method')

    def unhide(self,index):
        """ This method unhides the tab using it's index. """
        if  index in self.totalTabs:
            self.btns[index].grid(**self.btnslocations[index],**self.taboptions)
            self.Vars[index].set(1)
            if index in self.hiddentabs:
                self.hiddentabs.remove(index)
            self.activetabs.append(index)
            self.activetabs = sorted(self.activetabs)
        else:
            self.error('unhide method')

    def make_body(self,side=None,fill=None):
        """ This method is used to make the body of the notebook. """
        self.header.pack_forget()
        self.hide_all_frames()
        for btn in self.totalTabs:
            if btn not in self.hiddentabs:
                self.btns[btn].grid(**self.btnslocations[btn],**self.taboptions)

        self.header.pack(side=side,fill=fill)
        self.style(**self.nbcolors)
        self.display(self.frames[self.current])

    def provide_index(self,index):
        """ This method provides a convinent index of tab. """
        if index > len(self.totalTabs)-1:
            return 0
        elif index < 0 and index==-1:
            return (len(self.totalTabs)-1)
        else:
            return index

    def next(self,e=None):
        """ Jumps to next active tab. """
        i=1
        while i<=len(self.totalTabs):
            index = self.provide_index(self.current+i)
            if not index in self.hiddentabs:
                self.display(self.frames[index])
                break
            i += 1

    def previous(self,e=None):
        """ Jumps to previous active tab. """
        i=1
        while i<=len(self.totalTabs):
            index = self.provide_index(self.current-i)
            if not index in self.hiddentabs:
                self.display(self.frames[index])
                break
            i += 1

    def remove(self,index):
        """ Completely deletes a specific tab using it's index. """
        # Removing tab from every iterable
        if index in self.totalTabs:
            self.btns[index].destroy()
            self.frames[index].destroy()
            self.frames.pop(index)
            self.Vars.pop(index)
            self.btns.pop(index)
            self.totalTabs.pop(index)
            self.btnslocations.pop(index)
            if index in self.activetabs:
                self.activetabs.pop(index)
            if index in self.hiddentabs:
                self.hiddentabs.pop(index)
        else:
            self.error('remove method')

    def tab_positions(self,side,*args,**kwargs):
        """ This method is used to change the location or position of tabs. """
        self.side = side
        self.taboptions.update(**kwargs)

        if side == 'left' or side == 'right':
            for btn in self.totalTabs:
                self.btnslocations[btn] = {'row' : btn , 'column' : 0}
            self.fill = 'y'
        else:
            for btn in self.totalTabs:
                self.btnslocations[btn] = {'row' : 0 , 'column' : btn}
            self.fill = 'x'

        self.make_body(self.side,self.fill)

    def style(self,focusbg=None,fieldbackground=None,tabbg=None,*args,**kwargs):
        """ Use to customize the objects of notebook. """
        self.nbcolors.update(**kwargs)

        if focusbg:
            self.hovcolors['focusbg']=focusbg

        for button in self.btns:
            button.config(*args,**kwargs)

        if fieldbackground:
            self.nbcolors['fieldbackground'] = fieldbackground
            self.config(bg=fieldbackground)
            self.header.config(bg=fieldbackground)

        if tabbg:
            self.nbcolors['tabbg'] = tabbg

        self.btns[self.current].config(bg=self.nbcolors['tabbg'])

    def current_tab(self):
        """ Returns the current active tab's index. """
        return self.current

    def all_tabs(self):
        """ Returns the names and objects of all the tabs. """
        return self.frames,self.framenames

    def menu(self,index):
        """ This method makes menu for the hiding displaying tabs. """
        if index in self.hiddentabs:
            self.unhide(index)
        else:
            self.hide(index)

    def popup(self, event):
        """ Part of menu method. """
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def enabletraversal(self,master):
        """ This method will bind Alt-q,Alt-e to jump to previous and next tab
            respectively. Note the master should be your root object (main object).
        """
        master.bind("<Alt-e>",lambda e : self.next(e))
        master.bind("<Alt-q>",lambda e : self.previous(e))

    def disabletraversal(self,master):
        """ This method will unbind hotkeys. """
        master.unbind("<Alt-e>")
        master.unbind("<Alt-q>")

    def focusIn(self,event,frame):
        """ Changes the color of tab when mouse's cursor enters. """
        self.hovcolor = self.btns[self.frames.index(frame)]['bg']
        self.btns[self.frames.index(frame)].config(bg=self.hovcolors['focusbg'])

    def focused(self,event,frame):
        """ Changes the the color of tab when it's pressed. """
        self.hovcolor = self.nbcolors['tabbg']
        self.btns[self.frames.index(frame)].config(bg=self.hovcolors['focusbg'])

    def focusOut(self,event,frame):
        """ Makes Tab color as it was before focusIn. """
        self.btns[self.frames.index(frame)].config(bg=self.hovcolor)

    def error(self,method=None,error_no=None):
        """ Prints Error Currently not functional. """
        print("Error , bad index : {} , erorr : {}".format(method,error_no))

        """ 
         Hacks:
            1) Hack for placing header tab to desired positoin is use pack method
         yourself and pack it desired place.

            2) Hack for binding keys with to switch tab to next or previous can be done 
         using next,previous method of class.

        """

if __name__ == '__main__':

    root = Tk()

    nb = MyNotebook(root)
    nb.pack(fill = 'both' , expand = True)

    page1 = Frame(nb,bg='red')
    page2 = Frame(nb,bg='green')

    nb.add(page1,'page1')
    nb.add(page2,'page2')

    nb.show(1)
    nb.enabletraversal(root)
    #Button(root,text='hide' , command = lambda : nb.hide(0)).pack(side = 'right')
    #Button(root,text='unhide' , command = lambda : nb.unhide(0)).pack(side = 'left')
    root.mainloop()
