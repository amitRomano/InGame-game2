# You can place the script of your game in this file.

###### ASSET DECLARATION ######
# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

image sexroom_floor = "backgrounds/sexroom_floor.png"
image partySceneImage = "backgrounds/party_scene.png"
image mysteryImage = "backgrounds/mysteryshot.png"
image ceilingImage = "backgrounds/sexroom_ceiling.png"
image sexroomImage = "backgrounds/sexroom_floor.png"
image gameroomImage = "backgrounds/gameroom.png"
image hallwayImage = "backgrounds/hallway.jpg"
image ConsoleScene = "backgrounds/ConsoleScene.png"
image WeedbagScene = "backgrounds/WeedbagScene.png"
image bookscene = "backgrounds/bookScene.png"
image StereoScene = "backgrounds/StereoScene.png"
image AlcoholScene = "backgrounds/AlcoholScene.png"
image toiletImage = "backgrounds/Toilet.png"
image laundryImage = "backgrounds/laundry.jpg"
image drawerImage = "backgrounds/drawer.jpg"

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
    iVibrator = Item("Vibrator","inventory/Vibrator.png")
    iAshtray = Item("Ashtray","inventory/Ashtray.png")
    iDanceshoes = Item("Danceshoes","inventory/Danceshoes.png")
    iController = Item("Controller","inventory/Controller.png")
    iGuitar = Item("Guitar","inventory/Guitar.png")
    iNotebook = Item("Notebook","inventory/Notebook.png")
    iConsole = Item("Console","inventory/Console.png")
    iWeedbag = Item("Weedbag","inventory/Weedbag.png")
    iStereo = Item("Stereo","inventory/Stereo.png")
    iAlcohol = Item("Alcohol","inventory/Alcohol.png")
    iShoes = Item("Shoes","furniture/Shoes.png")
    iPrizes = Item("Prizes","furniture/Prizes.png")
    iBookPile = Item("Books","furniture/BookPile.png")
    iBook = Item("Book","inventory/Book.png")
    iSwearshirt = Item("Sweatshirt","inventory/Sweatshirt.png")
    iShampoo = Item("Shampoo","inventory/Shampoo.png")
    iSoap = Item("Soap","inventory/Soap.png")
    iTap = Item("Tap","inventory/Tap.png")
    iDisc = Item("Disc","inventory/Disc.png")
    iCarpet = Item("Carpet","inventory/Carpet.png")
    iPick = Item("Pick","inventory/Pick.png")
    iShelf = Item("Shelf","inventory/Shelf.png")
    iClip = Item("Clip","inventory/Clip.png")
    iKey = Item("Key","inventory/Key.png")
    
init python:
    def inventory_dragged(drags, drop):

        if not drop:
            return

        return True

init python:
    def hide_screens():
        renpy.hide_screen("hallway")
        renpy.hide_screen("sexroom")
        renpy.hide_screen("gameroom")
        renpy.hide_screen("toilet")
        renpy.hide_screen("drawer")

######### START OF GAMEPLAY #########

label start:
    $ clue0 = False
    $ clue1 = False
    $ clue2 = False
    $ clue3 = False
    $ clue4 = False
    $ clue5 = False
    $ clue6 = False
    $ clue7 = False
    $ clue8 = False
    $ clickFlag = True
    $ inventory = []
    $ hallway_visit = False
    $ gameroom_visit = False
    $ clues_count = 0
    $ matWidth, matHeight = 4, 4
    $ Matrix = [[0 for x in range(matWidth)] for y in range(matHeight)]
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
    
    #the items that are stored in the inventory (Hover+Action)
    $ VibratorHover = "Never know when I'm gonna use that ;)"
    $ DiscHover = "disc"
    $ DiscAction = "it's a cd... I have no idia of what"
    $ PickHover = "a guitar pick"
    $ PickAction = "I could use this pick"
    $ ClipHover = "laundry clip"
    $ ClipAction = "maybe I could use that for something"
    $ KeyHover = "key"
    $ KeyAction = "I bet it opens that drawer by the bed"
    
    # All items in other rooms get one text for hovering before pressing, one text for pressing (before flashback), one text for hovering after flashback.
    $ ConsoleHoverPre = "'Member when we played the PS4? Ooh, I 'member!"
    $ ConsoleAction = "Wait, I suddenly remember something about this PS4..."
    $ ConsoleHoverPost = "Dragon Age Inquisition is awesome!"
    $ WeedbagHoverPre = "'Member weed? I 'member!"
    $ WeedbagAction = "Wait, I 'member some more weed..."
    $ WeedbagHoverPost = "lol weed!"
    $ StereoHoverPre = "'Member music? I 'member!"
    $ StereoAction = "Wait, I suddenly 'member more..."
    $ StereoHoverPost = "Music is fun when you're with someone!"
    $ AlcoholHoverPre = "'Member alcohol? I 'member!"
    $ AlcoholAction = "Wait, I 'member dead brain cells now!"
    $ AlcoholHoverPost = "Empty alcohol bottles all around."
    $ ShoesHover = "A pair of shoes..."
    $ ShoesAction = "Last night was really wild."
    $ PrizesHover = "Look at all these prizes!"
    $ PrizesAction = "Someone's probably really successful!"
    $ BookPileHover = "So many books..."
    $ BookPileAction = "The person this room belongs to is a huge nerd!"
    $ BookHoverPre = "book"
    $ BookAction = "you remember:"
    $ BookHoverPost = "the-humus-king-and-the-bathtub-queen, by Ilan Heitner"
    $ SweatshirtHoverPre = "an old sweatshirt"
    $ SweatshirtAction = "you remember lucy putting on her sweatshirt before you went outside to smoke weed together"
    $ SweatshirtHoverPost = "lucy's sweatshirt"
    $ ShampooHoverPre = "shampoo"
    $ ShampooAction = "you remember hearing angie singing Aerosmith from the tub"
    $ ShampooHoverPost = "shampoo"
    $ SoapHover = "soap"
    $ SoapAction = "smells like memum.. which is an exotic flower that's indigenous to the hills of Costa Rica (and not my mom)"
    $ TapHover = "tap"
    $ TapAction = "I dont have time to brush my teeth.. got to find out what happend last night!"
    $ CarpetHoverPre = "this carpet looks familiar"
    $ CarpetAction = "you remember: lucy is dancing with you barefoot on the carpet"
    $ CarpetHoverPost = "it's just a carpet"
    $ ShelfHoverPre = "shelf"
    $ ShelfAction = "you remember hitting your head against this shelf, it still hurts a bit.. damn shelf!"
    $ ShelfHoverPost = "damn shelf!"
    $ MemberBerries = "I suddenly remember something..."
    
    

    
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
    "breakfast is gonna be so awkward unless I'll figure it out quickly.."
    "I better look around and find out!"
    
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
    $ hide_screens()
    scene sexroomImage
    call screen sexroom 
    
label hallway:
    $ hide_screens()
    show screen hallway
    scene hallwayImage
    if not hallway_visit:
        "???" "are you coming to the table?"
        "you" "be there in a few minutes"
        $ hallway_visit = True    
    scene hallwayImage
    call screen hallway   

label drawer:
    $ hide_screens()
    scene drawerImage
    call screen drawer


label toilet:
    $ hide_screens()
    scene toiletImage
    call screen toilet

label laundry:    
    $ hide_screens()
    scene laundryImage
    call screen laundry
    
label gameroomLabel: 
    $ hide_screens()
    scene gameroomImage
    show screen gameroom
    if not gameroom_visit:
        "This room looks cool!"
        $ gameroom_visit = True    
    call screen gameroom
    
#events labels
label notebookLabel:
    show screen sexroom
    $ clickFlag = False
    "Let's pick this up!"
    with pixellate
    show screen notebook_screen
    "Tip" "You can now look at the clues you've picked up in your notebook!"
    "Tip" "Press on the notebook or use the Esc button\n
        to read the notebook and other useful features."
    $ clickFlag = True
    call screen sexroom
    
label CarpetLabel:
    show screen hallway
    $ clickFlag = False
    "[MemberBerries]"
    "[CarpetAction]"
    $ Matrix[2][1] = +1
    $ clue0 = True
    $ clues_count += 1
    $ clickFlag = True
    call screen hallway
    
label pick:
    show screen hallway
    $ clickFlag = False
    "[MemberBerries]"
    "[PickAction]"
    $ Matrix[1][3] = +1
    $ Matrix[2][3] = -1
    $ clue1 = True
    $ clues_count += 1
    $ clickFlag = True
    call screen toilet    

label StereoLabel:
    show screen gameroom
    $ clickFlag = False
    "[MemberBerries]"
    "[StereoAction]"
    scene StereoScene
    with pixellate
    "angie have some cd's (her name is written on them)"
    scene gameroomImage
    with pixellate
    $ Matrix[0][3] = 1
    $ clue2 = True
    $ clues_count += 1
    $ clickFlag = True
    call screen gameroom
    
label BookLabel:
    show screen toilet
    $ clickFlag = False
    "[MemberBerries]"
    "[BookAction]"
    scene bookScene
    with pixellate
    "roxanne is telling you that she much rather read books then playing video games"
    scene toiletImage
    with pixellate
    $ Matrix[1][2] = -1
    $ clue3 = True
    $ clues_count += 1
    $ clickFlag = True
    call screen toilet

label ConsoleLabel:
    show screen gameroom
    $ clickFlag = False
    "[MemberBerries]"
    "[ConsoleAction]"
    scene ConsoleScene
    with pixellate
    "Joelene and Angie played Dragon Age: Inquisition"
    scene gameroomImage
    with pixellate
    $ Matrix[0][2] = 1
    $ Matrix[3][2] = 1
    $ clue4 = True
    $ clues_count += 1
    $ clickFlag = True
    call screen gameroom
    
label WeedbagLabel:
    show screen gameroom
    $ clickFlag = False
    "[MemberBerries]"
    "[WeedbagAction]"
    scene WeedbagScene
    with pixellate
    "angie is asking for you to smoke on the porch"
    scene gameroomImage
    with pixellate
    $ Matrix[0][0] = -1
    $ clue5 = True
    $ clues_count += 1
    $ clickFlag = True
    call screen gameroom
    
label SweatshirtLabel:
    show screen toilet
    $ clickFlag = False
    "[MemberBerries]"
    "[SweatshirtAction]"
    $ Matrix[2][0] = +1
    $ clue6 = True
    $ clues_count += 1
    $ clickFlag = True
    call screen toilet
    
label AlcoholLabel:
    show screen gameroom
    $ clickFlag = False
    "[MemberBerries]"
    "[AlcoholAction]"
    scene AlcoholScene
    with pixellate
    "joeling told you she never drinks alcohol while she smokes"
    scene gameroomImage
    with pixellate
    $ Matrix[3][0] = 1
    $ clue7 = True
    $ clues_count += 1
    $ clickFlag = True
    call screen gameroom
    
label ShampooLabel:
    show screen toilet
    $ clickFlag = False
    "[MemberBerries]"
    "[ShampooAction]"
    $ Matrix[0][3] = +1
    $ clue8 = True
    $ clues_count += 1
    $ clickFlag = True
    call screen toilet




######### END OF GAMEPLAY ###########
    







######## SCREEN DEFINITIONS #########
            
screen sexroom:
    on "hide" action Hide("displayTextScreen")
    
    imagebutton: # Ashtray
        xanchor 0.5
        yanchor 0.5
        xpos 511
        ypos 306
        idle iAshtray.image_name
        if clickFlag:
            hover iAshtray.hover_image
            if not Ashtray_found:
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
        if clickFlag:
            hover iDanceshoes.hover_image
            if not Danceshoes_found:
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
        if clickFlag:
            hover iController.hover_image
            if not Controller_found:
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
        if clickFlag:
            hover iGuitar.hover_image
            if not Guitar_found:
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
            idle iNotebook.image_name
            if clickFlag:
                hover iNotebook.hover_image
                action [Show("displayTextScreen", displayText = NotebookAction),SetVariable("Notebook_found", True),Jump("notebookLabel")]
                hovered Show("displayTextScreen", displayText = NotebookHover)
                unhovered Hide("displayTextScreen")
   
    imagebutton: # open drawer
        xanchor 0.5
        yanchor 0.5
        xpos 521
        ypos 372
        idle "inventory/empty.png"
        if clickFlag:
            hover "inventory/yellow.png"
            action Jump("drawer")
            hovered Show("displayTextScreen", displayText = "open drawer") 
            unhovered Hide("displayTextScreen")
        
    imagebutton: # Exit to hallway
        xanchor 0.5
        yanchor 0.5
        xpos 600
        ypos 400
        idle "inventory/empty.png"
        if clickFlag:
            hover "inventory/yellow.png"
            action Jump("hallway")
            hovered Show("displayTextScreen", displayText = "go to hallway") 
            unhovered Hide("displayTextScreen")
    
    imagebutton: # Exit to hallway
        xanchor 0.5
        yanchor 0.5
        xpos 800
        ypos 400
        idle "inventory/empty.png"
        if clickFlag:
            hover "inventory/yellow.png"
            action Jump("laundry")
            hovered Show("displayTextScreen", displayText = "look out the window") 
            unhovered Hide("displayTextScreen")
    
    if iKey not in inventory: # Key
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 200
            ypos 550
            idle iKey.image_name
            if clickFlag:
                hover iKey.hover_image
                action [Hide("displayTextScreen"), addItem(iKey)]
                hovered Show("displayTextScreen", displayText = KeyHover)
                unhovered Hide("displayTextScreen")
            


screen drawer:
    if iVibrator not in inventory: # Vibrator
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 200
            ypos 550
            idle iVibrator.image_name
            if clickFlag:
                hover iVibrator.hover_image
                action [Hide("displayTextScreen"), addItem(iVibrator)]
                hovered Show("displayTextScreen", displayText = VibratorHover)
                unhovered Hide("displayTextScreen")
            
    imagebutton: #sexroom
        xanchor 0.5
        yanchor 0.5
        xpos 400
        ypos 600
        idle "inventory/empty.png"
        if clickFlag:
            hover "inventory/yellow.png"
            action Jump("sexroom")
            hovered Show("displayTextScreen", displayText = "close the drawer") 
            unhovered Hide("displayTextScreen")
        
screen laundry:
    if iClip not in inventory: # luandry clip
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 200
            ypos 550
            idle iClip.image_name
            if clickFlag:
                hover iClip.hover_image
                action [Hide("displayTextScreen"), addItem(iClip)]
                hovered Show("displayTextScreen", displayText = ClipHover)
                unhovered Hide("displayTextScreen")
            
    imagebutton: #sexroom
        xanchor 0.5
        yanchor 0.5
        xpos 400
        ypos 600
        idle "inventory/empty.png"
        if clickFlag:
            hover "inventory/yellow.png"
            action Jump("sexroom")
            hovered Show("displayTextScreen", displayText = "Go back inside") 
            unhovered Hide("displayTextScreen")

screen toilet:
    on "hide" action Hide("displayTextScreen")
   
    imagebutton: # book
        xanchor 0.5
        yanchor 0.5
        xpos 400
        ypos 200
        idle iBook.image_name
        if clickFlag:
            hover iBook.hover_image
            if not clue3:
                action [Hide("displayTextScreen"), Jump("BookLabel")]
                hovered Show("displayTextScreen", displayText = BookHoverPre) 
                unhovered Hide("displayTextScreen")
            else:
                action [Hide("displayTextScreen")]
                hovered Show("displayTextScreen", displayText = BookHoverPost)
                unhovered Hide("displayTextScreen")
            
    imagebutton: # sweat-shirt
        xanchor 0.5
        yanchor 0.5
        xpos 200
        ypos 200
        idle iSwearshirt.image_name
        if clickFlag:
            hover iSwearshirt.hover_image
            if not clue6:
                action [Hide("displayTextScreen"), Jump("SweatshirtLabel")]
                hovered Show("displayTextScreen", displayText = SweatshirtHoverPre) 
                unhovered Hide("displayTextScreen")
            else:
                action [Hide("displayTextScreen")]
                hovered Show("displayTextScreen", displayText = SweatshirtHoverPost)
                unhovered Hide("displayTextScreen")
            
            
    imagebutton: #shampoo-bottle
        xanchor 0.5
        yanchor 0.5
        xpos 200
        ypos 400
        idle iShampoo.image_name
        if clickFlag:
            hover iShampoo.hover_image
            if not clue8:
                action [Hide("displayTextScreen"), Jump("ShampooLabel")]
                hovered Show("displayTextScreen", displayText = ShampooHoverPre) 
                unhovered Hide("displayTextScreen")
            else:
                action [Hide("displayTextScreen")]
                hovered Show("displayTextScreen", displayText = ShampooHoverPost)
                unhovered Hide("displayTextScreen")     
            
    imagebutton: # soap
        xanchor 0.5
        yanchor 0.5
        xpos 400
        ypos 400
        idle iSoap.image_name
        hover iSoap.hover_image
        if clickFlag:
            action Show("displayTextScreen", displayText = SoapAction)
            hovered Show("displayTextScreen", displayText = SoapHover) 
            unhovered Hide("displayTextScreen")
        
    imagebutton: # tap
        xanchor 0.5
        yanchor 0.5
        xpos 200
        ypos 500
        idle iTap.image_name
        hover iTap.hover_image
        if clickFlag:
            action Show("displayTextScreen", displayText = TapAction)
            hovered Show("displayTextScreen", displayText = TapHover) 
            unhovered Hide("displayTextScreen")
    
        
    if iDisc not in inventory: # disc
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 200
            ypos 600
            idle iDisc.image_name
            hover iDisc.hover_image
            if clickFlag:
                action [Hide("displayTextScreen"), addItem(iDisc)]
                hovered Show("displayTextScreen", displayText = DiscHover)
                unhovered Hide("displayTextScreen")
        
    imagebutton: # Exit to hallway
        xanchor 0.5
        yanchor 0.5
        xpos 600
        ypos 400
        idle "inventory/empty.png"
        hover "inventory/yellow.png"
        if clickFlag:
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
        if clickFlag:
            hover iConsole.hover_image
            if not clue4:
                action [Hide("displayTextScreen"), Jump("ConsoleLabel")]
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
        if clickFlag:
            hover iWeedbag.hover_image
            if not clue5:
                action [Hide("displayTextScreen"), Jump("WeedbagLabel")]
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
        if clickFlag:
            hover iStereo.hover_image
            if not clue2:
                action [Hide("displayTextScreen"), Jump("StereoLabel")]
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
        if clickFlag:
            hover iAlcohol.hover_image
            if not clue7:
                action [Hide("displayTextScreen"), Jump("AlcoholLabel")]
                hovered Show("displayTextScreen", displayText = AlcoholHoverPre) 
                unhovered Hide("displayTextScreen")
            else:
                action [Hide("displayTextScreen")]
                hovered Show("displayTextScreen", displayText = AlcoholHoverPost)
                unhovered Hide("displayTextScreen")
    
    imagebutton: # Exit to hallway
        xanchor 0.5
        yanchor 0.5
        xpos 600
        ypos 400
        idle "inventory/empty.png"
        hover "inventory/yellow.png"
        if clickFlag:
            action Jump("hallway")
            hovered Show("displayTextScreen", displayText = "go to hallway") 
            unhovered Hide("displayTextScreen")

    imagebutton: # BookPile
        xanchor 0.5
        yanchor 0.5
        xpos 200
        ypos 500
        idle iBookPile.image_name
        hover iBookPile.hover_image
        if clickFlag:
            action Show("displayTextScreen", displayText = BookPileAction)
            hovered Show("displayTextScreen", displayText = BookPileHover) 
            unhovered Hide("displayTextScreen")
        
    imagebutton: # Prizes
        xanchor 0.5
        yanchor 0.5
        xpos 400
        ypos 500
        idle iPrizes.image_name
        hover iPrizes.hover_image
        if clickFlag:
            action Show("displayTextScreen", displayText = PrizesAction)
            hovered Show("displayTextScreen", displayText = PrizesHover) 
            unhovered Hide("displayTextScreen")
        
    imagebutton: # Shoes
        xanchor 0.5
        yanchor 0.5
        xpos 600
        ypos 500
        idle iShoes.image_name
        hover iShoes.hover_image
        if clickFlag:
            action Show("displayTextScreen", displayText = ShoesAction)
            hovered Show("displayTextScreen", displayText = ShoesHover) 
            unhovered Hide("displayTextScreen")


screen hallway:
    on "hide" action Hide("displayTextScreen")
    if iPick not in inventory: # guitar-pick
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 200
            ypos 550
            idle iPick.image_name
            hover iPick.hover_image
            if clickFlag:
                action [Hide("displayTextScreen"), addItem(iPick)]
                hovered Show("displayTextScreen", displayText = PickHover)
                unhovered Hide("displayTextScreen")
        
    imagebutton: #carpet
        xanchor 0.5
        yanchor 0.5
        xpos 600
        ypos 400
        idle iCarpet.image_name
        if clickFlag:
            hover iCarpet.hover_image
            if not clue0:
                action [Hide("displayTextScreen"), Jump("CarpetLabel")]
                hovered Show("displayTextScreen", displayText = CarpetHoverPre) 
                unhovered Hide("displayTextScreen")
            else:
                action [Hide("displayTextScreen")]
                hovered Show("displayTextScreen", displayText = CarpetHoverPost)
                unhovered Hide("displayTextScreen")      
            
    imagebutton: #Gameroom
        xpos 200
        ypos 200
        xanchor 0.5
        yanchor 0.5
        idle "inventory/empty.png"
        hover "inventory/yellow.png"
        if clickFlag:
            action Jump("gameroomLabel")
            hovered Show("displayTextScreen", displayText = "Go to game room") 
            unhovered Hide("displayTextScreen")
        
    imagebutton: #sexroom
        xanchor 0.5
        yanchor 0.5
        xpos 400
        ypos 600
        idle "inventory/empty.png"
        hover "inventory/yellow.png"
        if clickFlag:
            action Jump("sexroom")
            hovered Show("displayTextScreen", displayText = "Go to the girl's Room") 
            unhovered Hide("displayTextScreen")
    
    imagebutton:#Toilet
        xpos 745
        ypos 235
        xanchor 0.5
        yanchor 0.5
        idle "inventory/empty.png"
        hover "inventory/yellow.png"
        if clickFlag:
            action Jump("toilet")
            hovered Show("displayTextScreen", displayText = "Go to the toilet.") 
            unhovered Hide("displayTextScreen")


###### SPECIAL SCREEN DEFINITIONS - DO NOT TOUCH ######
    
screen displayTextScreen:  
    default displayText = ""
    vbox:
        xalign 0.5
        yalign 0.8
        frame:
            text displayText
        
screen inventory_screen:
    zorder 100
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
    zorder 50
    frame:
        grid 1 1:
        
            spacing 5
            xpos 700
            ypos 500

            imagebutton: 
               idle iNotebook.image_name 
               hover iNotebook.hover_image
               action ShowMenu("notebook")