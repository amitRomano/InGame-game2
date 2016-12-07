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
    iDanceshoes = Item("DanceNote","inventory/Danceshoes.png")
    iController = Item("BrunetteNote","inventory/Controller.png")
    iGuitar = Item("BrunetteNote","inventory/Guitar.png")
    iNotebook = Item("Notebook","inventory/Notebook.png")

init python:
    def inventory_dragged(drags, drop):

        if not drop:
            return

        return True
    
######### START OF GAMEPLAY #########

label start:
    $ clues_count = 0
    $ total_clues = 9
    $ matWidth, matHeight = 4, 4
    $ Matrix = [[0 for x in range(matWidth)] for y in range(matHeight)]
    $ CluesArray = [False for y in range(total_clues)]
    $ inventory = []
    $ hallway_visit = False
    $ Ashtray_found = False
    $ Danceshoes_found = False
    $ Controller_found = False
    $ Guitar_found = False
    $ Notebook_found = False
    
label textsForScreens:
    # The sexroom items all get "hoverText" for hovering before pressing them, and their respective texts for both pressing and hovering after pressing them."
    $ HoverText = "What's this? Better try to touch it!"
    $ AshtrayText = "Huh, so she's a smoker."
    $ DanceshoesText = "You know what they say, dancers are...\nUgh I forgot it."
    $ ControllerText = "A gamer. Just my type!"
    $ GuitarText = "I wonder what kind of music she likes..."
    $ NotebookHover = "This pen and notebook may be useful."
    $ NotebookAction = "I'll take it!\nBetter write down all of the clues I'll find."
    
    # All items in other rooms get one text for hovering before pressing, one text for pressing (before flashback), one text for hovering after flashback.
    $ ConsoleHoverPre = "'Member when we played the PS4? Ooh, I 'member!"
    $ ConsoleAction = "Actually, now I 'member something else..."
    $ ConsoleHoverPost = "Dragon Age Inquisition is awesome!"
    $ WeedbagHoverPre = ""
    $ WeedbagAction = ""
    $ WeedbagHoverPost = ""
    $ StereoHoverPre = ""
    $ StereoAction = ""
    $ StereoHoverPost = ""
    $ AlcoholHoverPre = ""
    $ AlcoholAction = ""
    $ AlcoholHoverPost = ""

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
    "breakfast is gonna be so awkward unless I'll figure it out quickly...\n
    I better look around and click on random things so that I can recognize her."
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
    call screen hallway
    
label notebookLabel:
    show screen sexroom
    show screen notebook_screen
    with pixellate
    "Tip" "You can now look at the clues you've picked up in your notebook!"
    "Tip" "Press on the notebook or use the Esc button\n
        to read the notebook and other useful features."
    call screen sexroom

######### END OF GAMEPLAY ###########
    







######## SCREEN DEFINITIONS #########
            
screen sexroom:
    on "hide" action Hide("displayTextScreen")
    
    imagebutton: # Ashtray
        xanchor 0.5
        yanchor 0.5
        xpos 200
        ypos 200
        idle iAshtray.image_name
        if not Ashtray_found:
            hover iAshtray.hover_image
            action [Show("displayTextScreen", displayText = AshtrayText),SetVariable("Ashtray_found", True)]
            hovered Show("displayTextScreen", displayText = HoverText) 
            unhovered Hide("displayTextScreen")
        else:
            action [Hide("displayTextScreen")]
            hovered Show("displayTextScreen", displayText = AshtrayText) 
            unhovered Hide("displayTextScreen")
    
    imagebutton: # Dance shoes
        xanchor 0.5
        yanchor 0.5
        xpos 400
        ypos 200
        idle iDanceshoes.image_name
        if not Danceshoes_found:
            hover iDanceshoes.hover_image
            action [Show("displayTextScreen", displayText = DanceshoesText),SetVariable("Danceshoes_found", True)]
            hovered Show("displayTextScreen", displayText = HoverText) 
            unhovered Hide("displayTextScreen")
        else:
            action [Hide("displayTextScreen")]
            hovered Show("displayTextScreen", displayText = DanceshoesText)
            unhovered Hide("displayTextScreen")
            
    imagebutton: # Controller
        xanchor 0.5
        yanchor 0.5
        xpos 600
        ypos 200
        idle iController.image_name
        if not Controller_found:
            hover iController.hover_image
            action [Show("displayTextScreen", displayText = ControllerText),SetVariable("Controller_found", True)]
            hovered Show("displayTextScreen", displayText = HoverText) 
            unhovered Hide("displayTextScreen")
        else:
            action [Hide("displayTextScreen")]
            hovered Show("displayTextScreen", displayText = ControllerText)
            unhovered Hide("displayTextScreen")
            
    imagebutton: # Guitar
        xanchor 0.5
        yanchor 0.5
        xpos 200
        ypos 400
        idle iGuitar.image_name
        if not Guitar_found:
            hover iGuitar.hover_image
            action [Show("displayTextScreen", displayText = GuitarText),SetVariable("Guitar_found", True)]
            hovered Show("displayTextScreen", displayText = HoverText) 
            unhovered Hide("displayTextScreen")
        else:
            action [Hide("displayTextScreen")]
            hovered Show("displayTextScreen", displayText = GuitarText)
            unhovered Hide("displayTextScreen")
             
    if not Notebook_found:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 400
            ypos 400
            idle iVibrator.image_name
            hover iVibrator.hover_image
            action [Show("displayTextScreen", displayText = NotebookAction),SetVariable("Notebook_found", True),Jump("notebookLabel")]
            hovered Show("displayTextScreen", displayText = NotebookHover)
            unhovered Hide("displayTextScreen")
    
    imagebutton: # Exit to hallway
        xanchor 0.5
        yanchor 0.5
        xpos 600
        ypos 400
        idle "inventory/empty.png"
        hover "inventory/yellow.png"
        action Jump("hallway")
        hovered Show("displayTextScreen", displayText = "go to hallway") 
        unhovered Hide("displayTextScreen")   
        
screen gameroom:
    imagebutton: # Console
        xanchor 0.5
        yanchor 0.5
        xpos 200
        ypos 200
        idle iConsole.image_name
        if not CluesArray[4]:
            hover iConsole.hover_image
            action [Show("displayTextScreen", displayText = ConsoleAction),SetVariable("CluesArray[4]", True)]
            hovered Show("displayTextScreen", displayText = ConsoleHoverPre) 
            unhovered Hide("displayTextScreen")
        else:
            action [Hide("displayTextScreen")]
            hovered Show("displayTextScreen", displayText = ConsoleHoverPost)
            unhovered Hide("displayTextScreen")
            
    imagebutton: # Weedbag
        xanchor 0.5
        yanchor 0.5
        xpos 400
        ypos 200
        idle iWeedbag.image_name
        if not CluesArray[5]:
            hover iWeedbag.hover_image
            action [Show("displayTextScreen", displayText = WeedbagAction),SetVariable("CluesArray[5]", True)]
            hovered Show("displayTextScreen", displayText = WeedbagHoverPre) 
            unhovered Hide("displayTextScreen")
        else:
            action [Hide("displayTextScreen")]
            hovered Show("displayTextScreen", displayText = WeedbagHoverPost)
            unhovered Hide("displayTextScreen")
            
    imagebutton: # Stereo
        xanchor 0.5
        yanchor 0.5
        xpos 600
        ypos 200
        idle iStereo.image_name
        if not CluesArray[2]:
            hover iStereo.hover_image
            action [Show("displayTextScreen", displayText = StereoAction),SetVariable("CluesArray[2]", True)]
            hovered Show("displayTextScreen", displayText = StereoHoverPre) 
            unhovered Hide("displayTextScreen")
        else:
            action [Hide("displayTextScreen")]
            hovered Show("displayTextScreen", displayText = StereoHoverPost)
            unhovered Hide("displayTextScreen")
            
    imagebutton: # Alcohol
        xanchor 0.5
        yanchor 0.5
        xpos 200
        ypos 400
        idle iAlcohol.image_name
        if not CluesArray[7]:
            hover iAlcohol.hover_image
            action [Show("displayTextScreen", displayText = AlcoholAction),SetVariable("CluesArray[7]", True)]
            hovered Show("displayTextScreen", displayText = AlcoholHoverPre) 
            unhovered Hide("displayTextScreen")
        else:
            action [Hide("displayTextScreen")]
            hovered Show("displayTextScreen", displayText = AlcoholHoverPost)
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