### LABELS - USED TO DEFINE LABEL TAGS ###

#label start:
#    $ fireplace_wood = False
#    $ fireplace_lit = False
#    $ active_item = None
    
#    $ living_visit = False
#    $ kitchen_visit = False
#    $ outside_visit = False
#    $ inside_visit = False

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


### SCREENS - USED TO DESIGN THE ROOMS ###




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
    