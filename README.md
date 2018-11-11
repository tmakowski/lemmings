# lemmings
### Questions
- [ ] Should I delete every field of the Lemming in it's destructor?

### Completed
- [x] Implement a basic lemming.
- [x] Move the lemming.
- [x] Add image to the lemming.
- [x] Collide the lemming with a map edges.
- [x] Add a wall.
- [x] Collide the lemming with the wall.
- [x] Add floor -- as long as the lemming has the floor underneath it won't fall.
- [x] Implement falling (use angled walls as a floor).

### Reading:
- [ ] How to use sprites
- [ ] How to use surface rotation
- [ ] (?) How to rotate an object (and not just it's image!)

### ToDo:
- [ ] **Collideable** walls at an angle.
- [ ] Define block size (== lemming's size).
- [ ] Add water at the bottom of a level which kills the lemming.
- [ ] Create more lemming types:
    - [ ] stopper,
    - [ ] miner,
    - [ ] parachute,
    - [ ] step-placer.
- [ ] Create a simple first level.
- [ ] Implement entrance and exit.
    - [ ] Entrance:
        - [ ] Generates set number of lemmings.
    - [ ] Exit:
        - [ ] Deletes lemmings on appropriate
        - [ ] Counts deleted lemmings
        - [ ] Stops game as a win if there was sufficient amount of lemmings deleted.
- [ ] Level timer
- [ ] Statistics:
    - [ ] Lemmings alive
    - [ ] All lemmings
    - [ ] Timer display
- [ ] Create menu:
    - [ ] Start new level
        - [ ] Add level generation // add manual levels.
        - [ ] Create introduction (first levels with hints)
    - [ ] Load game
- [ ] In-game menu:
    - [ ] Pause on call
    - [ ] Save game:
        - [ ] Save the map
        - [ ] Save the lemming positions
        - [ ] Save the lemming types
        - [ ] Save the time left
    - [ ] Exit game -- return to main menu.
- [ ] Merge menus
- [ ] Improve graphics:
    - [ ] Lemming animations
    - [ ] Different terrain