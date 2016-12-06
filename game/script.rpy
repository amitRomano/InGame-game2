# You can place the script of your game in this file.

###### ASSET DECLARATION ######
# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

image sexroom_floor = "backgrounds/sexroom_floor.png"





######### PYTHON CODE #########

init python:
    
    class Item:
        hover_image = None
        selected = False
        def __init__(self, name,image_name):
            self.name = name
            self.image_name = image_name
            self.hover_image = im.Composite((100, 100),
                                        (0, 0), "inventory/yellow.png",
                                        (0, 0), image_name)
            self.selected_image = im.Composite((100, 100),
                                        (0, 0), "inventory/red.png",
                                        (0, 0), image_name)
        def __eq__(self, other):
            return self.name == other.name
    
    class Notebook(Item):
        w, h = 4, 5. 
        Matrix = [[0 for x in range(w)] for y in range(h)]
        def __init__(self, name,image_name):
            super(self,name,image_name)
            
            

    class testItem(Action):

        def __init__(self, item, switch, value, remove = True):
            self.item = item
            self.switch = switch
            self.value = value
            self.remove = remove
        
        def __call__(self):
            if store.active_item != None and store.active_item == self.item:
                setattr(store, self.switch, self.value)
                if self.remove:
                    store.inventory.remove(self.item)
                    store.active_item = None
            renpy.restart_interaction()


            
    class addItem(Action):

        def __init__(self, item):
            self.item = item
        
        def __call__(self):
            store.inventory.append(self.item)
            renpy.restart_interaction()
            
            
    class selectItem(Action):

        def __init__(self, object):
            self.object = object
        
        def __call__(self):
            new_value = not self.object.selected
            for item in store.inventory:
                setattr(item, "selected", False)
            store.active_item = None
            setattr(self.object, "selected", new_value)
            if (new_value):
                store.active_item = self.object
            renpy.restart_interaction()

        def get_selected(self):
            return self.object.selected

###### ITEM DEFINITIONS ########
    iVibrator = Item("Vibrator","inventory/vibrator.png")
    iSmokeNote = Item("SmokeNote","inventory/SmokeNote.png")
    iDanceNote = Item("DanceNote","inventory/DanceNote.png")
    iBrunetteNote = Item("BrunetteNote","inventory/BrunetteNote.png")

init python:
    def inventory_dragged(drags, drop):

        if not drop:
            return

        return True
    
######### START OF GAMEPLAY #########

label start:
    $ inventory = []
    scene sexroom_floor
    "Hello World"
    show screen inventory_screen

label this_happens_immediately_after_start:
    call screen experiment_screen


######### END OF GAMEPLAY ###########
    







######## SCREEN DEFINITIONS #########

screen experiment_screen: 
    on "hide" action Hide("displayTextScreen")
    add "backgrounds/sexroom_floor.png"
    
    screen grid_test:
     grid 2 3:
         text "Top-Left"
         text "Top-Right"

         text "Center-Left"
         text "Center-Right"

         text "Bottom-Left"
         text "Bottom-Right"
    
    # Inventory item that's added to the inventory by itself and disappears
    if iVibrator not in inventory:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 566
            ypos 322
            idle iVibrator.image_name
            hover iVibrator.hover_image
            action [Hide("displayTextScreen"),addItem(iVibrator)]
            hovered Show("displayTextScreen", displayText = "Better not burn yourself.") 
            unhovered Hide("displayTextScreen")



    # Static item (furniture) that adds info to the inventory
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 200
        ypos 200
        idle iVibrator.image_name
        if iVibrator not in inventory:
            hover iVibrator.hover_image
            action [Hide("displayTextScreen"),addItem(iVibrator)]
            hovered Show("displayTextScreen", displayText = "Better not burn yourself.") 
            unhovered Hide("displayTextScreen")
        else:
            action [Hide("displayTextScreen"),addItem(iVibrator)]
            hovered Show("displayTextScreen", displayText = "Careful, I've been burned before!") 
            unhovered Hide("displayTextScreen")
            








###### SPECIAL SCREEN DEFINITIONS - DO NOT TOUCH ######

screen displayTextScreen:  
    default displayText = ""
    vbox:
        xalign 0.5
        yalign 0.5
        frame:
            text displayText
        
screen inventory_screen:
    zorder 100
    #a sexy grid
    $ num = 10
    frame:
        grid 1 num:
        
            spacing 5
            xpos 0
            ypos 0

            for index, item in enumerate(inventory):
                imagebutton: 
                   idle item.image_name 
                   hover item.hover_image
                   selected_idle item.selected_image
                   action selectItem(item)

            for i in range(num - len(inventory)):
                add "inventory/empty.png"