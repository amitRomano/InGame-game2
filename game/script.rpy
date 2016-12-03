# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.    
image livingroom_bg = "fireplace_empty.jpg"
image livingroom_wood_bg = "fireplace_wood.jpg"
image livingroom_lit_bg = "fireplace_lit.jpg"
image kitchen_bg = "kitchen_match.jpg"
image outside_bg = "outside_wood.jpg"
image inside_bg = "room_empty.png"
image eileen happy = "eileen happy.png"
image eileen sad = "eileen concerned.png"
image eileen surprised = "eileen vhappy.png"


init python:
    
    class Item:
        hover_image = None
        selected = False
        def __init__(self, name,image_name):
            self.name = name
            self.image_name = image_name
            self.hover_image = im.Composite((100, 100),
                                        (0, 0), "yellow.png",
                                        (0, 0), image_name)
            self.selected_image = im.Composite((100, 100),
                                        (0, 0), "red.png",
                                        (0, 0), image_name)
        def __eq__(self, other):
            return self.name == other.name
                                        

    iMatch = Item("Match","match.png")
    iFirewood = Item("Firewood","wood.png")
    iFish = Item("Fish","herring_item.png")
    iGlasses = Item("Glasses","vr_glasses.png")
              
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

            
init python:
    def inventory_dragged(drags, drop):

        if not drop:
            return

        return True
# The game starts here.
label start:
    $ fireplace_wood = False
    $ fireplace_lit = False
    $ active_item = None
    
    $ living_visit = False
    $ kitchen_visit = False
    $ outside_visit = False
    $ inside_visit = False
    
    
    $ inventory = []
    
    ### Transition from mm_root to girls_room.jpg ###
    
    scene outside_bg
    
    
    show eileen happy at left
    "Mysterious Girl" "Good morning! I had a really great time last night. I’m going to get milk for coffee, be back in 5 minutes."
    
    show eileen surprised at left
    "Mysterious Girl" "Feel at home."
    
    hide eileen
    
    "You think to yourself..."
    
    "Where the heck am I? Who was this girl just now?!"
    
    "She was hot though.\n
     ...What happened last night?"
    
    show screen inventory_screen

label living:
    if not living_visit:
        scene livingroom_bg
        "Look at that nice fireplace."
        "I wonder if I could light it."
        $ living_visit = True
    call screen living_room

label kitchen:    
    if not kitchen_visit:
        scene kitchen_bg
        "Look at this nice kitchen."
        $ kitchen_visit = True
    call screen kitchen_room
    
label outside:    
    if not outside_visit:
        scene outside_bg
        "Brr! It's cold out here!"
        $ outside_visit = True
    call screen outside_room
    
label inside:
    if not inside_visit:
        scene inside_bg
        "Finally! My brand new VR set had arrived!"
        "But wait, where is it? Is it possible Ido hadn't placed the object yet?!"
        $ inside_visit = True
    call screen inside_room
        
label end:
    hide screen inventory_screen
    scene livingroom_lit_bg
    "You stay very cozy in your little cabin."
    if iFish in inventory:
        "And dine on lovely Red Herring."
    ".:. The End"
    return
#using the format [idle image, hover image, description] for the items



screen kitchen_room: 
    on "hide" action Hide("displayTextScreen")
    if iMatch not in inventory and not fireplace_lit:
        add "kitchen_match.jpg"
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 516
            ypos 507
            idle "empty.png"
            hover "yellow.png"
            action [Hide("displayTextScreen"),addItem(iMatch)]
            hovered Show("displayTextScreen", displayText = "Better not burn yourself.") 
            unhovered Hide("displayTextScreen")
    else:
        add "kitchen.jpg"
        
    
    
    imagebutton:
        xpos 745
        ypos 235
        xanchor 0.5
        yanchor 0.5
        idle "empty.png"
        hover "yellow.png"
        action Jump("living")
        hovered Show("displayTextScreen", displayText = "Go to Living Room.") 
        unhovered Hide("displayTextScreen")     
    imagebutton:
        xpos 189
        ypos 372
        xanchor 0.5
        yanchor 0.5
        idle "empty.png"
        hover "yellow.png"
        action Jump("outside")
        hovered Show("displayTextScreen", displayText = "Go Outside.") 
        unhovered Hide("displayTextScreen")     
           
screen inside_room: 
    on "hide" action Hide("displayTextScreen")
    if iMatch not in inventory and not fireplace_lit:
        add "room_empty.png"
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 516
            ypos 507
            idle "empty.png"
            hover "yellow.png"
            action [Hide("displayTextScreen"),addItem(iMatch)]
            hovered Show("displayTextScreen", displayText = "Better not burn yourself.") 
            unhovered Hide("displayTextScreen")
    else:
        add "room_empty.png"
    if iGlasses not in inventory:
        add "vr_glasses.png" xpos 170 ypos 489 xanchor 0.5 yanchor 0.5
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 170
            ypos 489
            idle "empty.png"
            hover "yellow.png"
            action [Hide("displayTextScreen"),addItem(iGlasses)]
            hovered Show("displayTextScreen", displayText = "Oh wait, they did arrive!") 
            unhovered Hide("displayTextScreen")


screen outside_room: 
    on "hide" action Hide("displayTextScreen")
    if iFirewood not in inventory and not fireplace_wood:
        add "outside_wood.jpg"
        imagebutton:
            xpos 370
            ypos 462
            xanchor 0.5
            yanchor 0.5
            idle "empty.png"
            hover "yellow.png"
            action [Hide("displayTextScreen"),addItem(iFirewood)]
            hovered Show("displayTextScreen", displayText = "Someone left some wood here.") 
            unhovered Hide("displayTextScreen")
    else:
        add "outside.jpg"
       
    imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 650
            ypos 322
            idle "empty.png"
            hover "yellow.png"
            action Jump("kitchen")
            hovered Show("displayTextScreen", displayText = "Go to Kitchen.") 
            unhovered Hide("displayTextScreen")     
    
    
    
screen living_room: 
    on "hide" action Hide("displayTextScreen")
    if fireplace_lit:
        add "fireplace_lit.jpg"
    elif fireplace_wood:
        add "fireplace_wood.jpg"
    else:
        add "fireplace_empty.jpg"
        
    if fireplace_lit:
        imagebutton:
            xpos 464
            ypos 364
            idle "empty.png"
            hover "yellow.png"
            hovered Show("displayTextScreen", displayText = "Now I can warm myself! (Click to Finish)") 
            unhovered Hide("displayTextScreen")
            action [Hide("displayTextScreen"),Jump("end")]
    elif fireplace_wood:
        imagebutton:
            xpos 464
            ypos 364
            idle "empty.png"
            hover "yellow.png"
            action [Hide("displayTextScreen"),testItem(iMatch,"fireplace_lit", True)]
            hovered Show("displayTextScreen", displayText = "How can I light it?") 
            unhovered Hide("displayTextScreen")
    else:
        imagebutton:
            xpos 464
            ypos 364
            idle "empty.png"
            hover "yellow.png"
            action [Hide("displayTextScreen"),testItem(iFirewood,"fireplace_wood", True)]
            hovered Show("displayTextScreen", displayText = "Could use some wood.") 
            unhovered Hide("displayTextScreen")
    
    if iFish not in inventory:
        add "herring.png" xpos 500 ypos 160 xanchor 0.5 yanchor 0.5
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 500
            ypos 160
            idle "empty.png"
            hover "yellow.png"
            action [Hide("displayTextScreen"),addItem(iFish)]
            hovered Show("displayTextScreen", displayText = "Someone left this fish out.") 
            unhovered Hide("displayTextScreen")
            
    imagebutton:
        xpos 745
        ypos 235
        xanchor 0.5
        yanchor 0.5
        idle "empty.png"
        hover "yellow.png"
        action Jump("kitchen")
        hovered Show("displayTextScreen", displayText = "Go to Kitchen.") 
        unhovered Hide("displayTextScreen")   
    
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 100
        ypos 100
        idle "empty.png"
        hover "yellow.png"
        action Jump("inside")
        hovered Show("displayTextScreen", displayText = "I'm your master now.") 
        unhovered Hide("displayTextScreen")   
    
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
    frame:
        grid 1 4:
        
            spacing 15
            xpos 0
            ypos 0

            for index, item in enumerate(inventory):
                imagebutton: 
                   idle item.image_name 
                   hover item.hover_image
                   selected_idle item.selected_image
                   action selectItem(item)

            for i in range(4 - len(inventory)):
                add "empty.png"
