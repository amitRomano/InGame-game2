# You can place the script of your game in this file.

###### ASSET DECLARATION ######
# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

image sexroom_floor = "backgrounds/sexroom_floor.png"
image partySceneImage = "backgrounds/party_scene.png"
image mysteryImage = "backgrounds/mysteryshot.png"
image ceilingImage = "backgrounds/sexroom_ceiling.png"
image sexroomImage = "backgrounds/sexroom_floor.png"
image hallwayImage = "backgrounds/hallway.jpg"

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
    iAshtray = Item("Ashtray","inventory/Ashtray.png")
    iDanceNote = Item("DanceNote","inventory/DanceNote.png")
    iBrunetteNote = Item("BrunetteNote","inventory/BrunetteNote.png")
    iNotebook = Item("Notebook","inventory/Notebook.png")

init python:
    def inventory_dragged(drags, drop):

        if not drop:
            return

        return True
    
######### START OF GAMEPLAY #########

label start:
    $ clues_count = 0
    $ matWidth, matHeight = 4, 4 
    $ Matrix = [[0 for x in range(matWidth)] for y in range(matHeight)]
    $ inventory = []
    $ hallway_visit = False

label partySceneLabel:
    scene partySceneImage
    "Angie" "this is so fun!"
    "Roxanne" "yeah, I'm having a great time!"
    "Lucy" "I think I'm a bit too drunk"
    "you" "yeah me too"
    "Joelene" "we should do that more"
    scene mysteryImage
    with dissolve
    "???" "I'm so glad we invited you over...\n"
    "???" "how about we go to my room?"


label wakeUpLabel:
    scene ceilingImage:
        yalign 0.5
    with dissolve
    "hey sleepyhead\n
     my roomates made breakfast.. come to to table when you're ready"
    #change screen- she leaves the room
    "W...Where am I?"
    "What am I doing here?"
    "Wait, I'm in someone's bed...\n
     did we sleep together last night?"
    "but which girl did i sleep with?"
    "breakfast is gonna be so awkward unless I'll figure it out quickly"
    show sexroomImage:
        yalign 1.0 yanchor 0.0        # pic_2 will be placed at right offscreen
    with None

    show ceilingImage:
        yalign 0.0 yanchor 1.0        # pic_1 will be placed at left offscreen
    show sexroomImage:
        yalign 0.5
    with MoveTransition(1)                         # will change positions of all images above it
    scene sexroomImage
    show screen inventory_screen
    show screen notebook_screen
    call screen sexroom

label sexroom:
    scene sexroomImage
    call screen sexroom 
    
label hallway:    
    scene hallwayImage
    if not hallway_visit:
        "???" "are you coming to the table?"
        "you" "be there in a few minutes"
        $ hallway_visit = True
    
    scene hallwayImage
    show screen inventory_screen
    show screen notebook_screen
    call screen hallway

######### END OF GAMEPLAY ###########
    







######## SCREEN DEFINITIONS #########

screen experiment_screen: 
    on "hide" action Hide("displayTextScreen")
    
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
            
screen sexroom:
    on "hide" action Hide("displayTextScreen")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 200
        ypos 200
        idle iAshtray.image_name
        if iAshtray not in inventory:
            hover iAshtray.hover_image
            action [Hide("displayTextScreen"),addItem(iAshtray)]
            hovered Show("displayTextScreen", displayText = "Better not burn yourself.") 
            unhovered Hide("displayTextScreen")
        else:
            action [Hide("displayTextScreen")]
            hovered Show("displayTextScreen", displayText = "Careful, I've been burned before!") 
            unhovered Hide("displayTextScreen")
 
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 100
        ypos 100
        idle "inventory/empty.png"
        hover "inventory/yellow.png"
        action Jump("hallway")
        hovered Show("displayTextScreen", displayText = "go to hallway") 
        unhovered Hide("displayTextScreen")   
        


screen hallway:
    on "hide" action Hide("displayTextScreen")
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 400
        ypos 600
        idle "inventory/empty.png"
        hover "inventory/yellow.png"
        action Jump("sexroom")
        hovered Show("displayTextScreen", displayText = "Go to the girl's Room") 
        unhovered Hide("displayTextScreen")
    
    imagebutton:
        xpos 745
        ypos 235
        xanchor 0.5
        yanchor 0.5
        idle "inventory/empty.png"
        hover "inventory/yellow.png"
        action Jump("sexroom")
        hovered Show("displayTextScreen", displayText = "Go to the roomate's Room.") 
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
    zorder 2
    #a sexy grid
    $ num = 4
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
                
screen notebook_screen:
    zorder 2
    frame:
        grid 1 1:
        
            spacing 5
            xpos 700
            ypos 500

            imagebutton: 
               idle iNotebook.image_name 
               hover iNotebook.hover_image
               action selectItem(iNotebook)