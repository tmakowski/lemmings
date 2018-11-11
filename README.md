# lemmings
## Questions
- [ ] Should I delete every field of the Lemming in it's destructor?

## Game's development note
#### Loop structure
1. [x] Exit if game was closed.
1. [ ] Objects collisions:
    1. [ ] water,
    1. [ ] exit.
1. For each lemming:
    1. check wall collisions,
    1. check if it stands on the floor,
    1. move it.
1. Draw:
    1. background,
    1. every lemming, object etc.
1. Switch display to contain drawn objects.

### Tasks
#### Lemmings
- [x] Implement a basic lemming.
- [x] Added left/right movement.
- [x] Added image to the lemming.
- [x] Added collision with walls.
- [x] Added collision with floors.
- [x] Created destructor.
- [x] Implemented falling.
- [ ] Implement additional lemming types:
    - [ ] blocker,
    - [ ] miner,
    - [ ] parachute lemming,
    - [ ] step placer,
    - [ ] teleport-builder.

#### Objects
- [x] Added walls. 
- [x] Added floors.
- [x] Implement falling (use angled walls as a floor).
- [ ] Extend floor class to water:
    - [ ] Make it kill lemmings on contact.
- [ ] Extend floor class to steps:
    - [ ] on collision move lemming onto the first step,
    - [ ] ensure that the difference between the step level and the current level is below a certain threshold.
- [ ] Implement entrance:
    - [ ] Generates lemmings.
    - [ ] Generates lemmings with globally set interval.
- [ ] Implement exit:    
    - [ ] delete lemmings when they move onto the exit block,
    - [ ] have a variable counting number of lemmings that made it to the exit.
    
#### Level tied stuff
- [ ] Timer.
- [ ] Stats for lemmings:
    - [ ] how many of them were spawned by the entrance,
    - [ ] how many are still alive (percentage),
    - [ ] ... 
- [ ] Create level translator, that is a function to generate map from provided manually created layout:
    * **Dictionaries will come in handy!**
    - [ ] **B**: map **b**order wall,
    - [ ] **W**: **w**ater,
    - [ ] **S**: **s**tarting point (entrance),
    - [ ] **E**: **e**xit,
    - [ ] ...
- [ ] Create tutorial levels -- about 3-5 of them:
    - [ ] should contain tips,
        * Those might be hard coded into the map background.
        * Might as well be a game pauses to do specific actions.
    - [ ] ...
- [ ] Create other levels, preferably, with various difficulty levels.

#### User interface
- [ ] Create level interface:
    - [ ] in-game menu call,
    - [ ] row with different lemming types,
    - [ ] ...
- [ ] Create main menu:
    - [ ] starting a new level:
        - [ ] Tutorial levels on top.
        - [ ] Grid of selectable levels.
    - [ ] load game,
    - [ ] exit game.
- [ ] Create in-game menu:
    - pause the game on call,
    - save the game,
    - exit to main menu.

#### Other
- [ ] One file with all global variables.
- [ ] Define block's size (equal to lemming's size).
- [ ] Implement game saving:
    - [ ] save lemmings as a dictionary where the keys are the attributes,
    - [ ] save the map layout,
    - [ ] save the map stats,
    - [ ] save the graphics set used (?).
- [ ] Implement game loading.
- [ ] Improve game graphics with:
    - [ ] various objects,
    - [ ] different sets of walls,
    - [ ] additional backgrounds,
    - [ ] animations for lemmings,
    - [ ] different looks for each lemming type.

### To consider:
- Walls at an angle (could be just steps, to be honest).
- Fancy stats:
    - detailed info on lemmings' deaths.
- Random level generator.
- In-game menu and main menu merge.
- Change walls to be class extension of the floor. Tbh I don't think it'd be that useful.
