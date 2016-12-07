image hallwayImage = "backgrounds/hallway.jpg"


##############################
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


####################################
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