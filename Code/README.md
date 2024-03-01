# PyPong 

## Overview
This version of Pong is written in Python with the player operating in an enclosed environment with walls on the left,
top, and bottom sides of the game arena. The player is given a paddle and tasked with defending the right side for as
long as possible while accumulating as many points during the process. The paddle is controlled by the person's hand and
either hand can be used during the game.

## Game Demo
[Game Demo](https://youtu.be/8mVBlMuIzMU)
Please check out game here or in video saved in repo

## Game Installation & Usage
1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/KrajShuffle/PyPong.git
    ```

2. Navigate to the `Code` directory:

    ```bash
    cd Code
    ```

3. Once you're in the `Code` directory, you can run the game via...
    ```bash
    python Pong_logic.py
    ```
### Alternative Approach

If you prefer not to use Git or prefer a manual setup, you can follow these steps to get started:

1. Download the zip file of the PyPong repository.
2. Unzip the file to your desired location.
3. Open your preferred Integrated Development Environment (IDE).
4. Navigate to the `Code` directory within the unzipped folder.
5. Run the `Pong_logic.py` Python file from your IDE.

## Dependencies
Prior to running project, please make sure your environment has these packages & used Python Version

Before running the project, ensure your environment has the following packages:

1. **Python**: Version 3.8.18

2. **pygame**: Version 2.5.2
   - Please verify if pygame comes with SDL (2.28.5) support. Necessary for handling image formats like PNG & JPEG
     ```bash
     pip install pygame==2.5.2
     ```

3. **cvzone**: Version 1.5.3
   - cvzone is a helpful wrapper package that includes OpenCV and NumPy.
     ```bash
     pip install cvzone==1.5.3
     ```

4. **mediapipe**: Version 4.9.0.80
   ```bash
   pip install mediapipe==0.9.3.0
   ```
Overall, you should end up with
- **Python**: Version 3.8.18
- **Pygame**: Version 2.5.2
- **cvzone**: Version 1.5.3
- **OpenCV-Python**: Version 4.9.0.80
- **OpenCV-Contrib-Python**: Version 4.9.0.80
- **NumPy**: Version 1.24.4
- **mediapipe**: Version 0.9.3.0
- **sdl2**: Version 2.28.5

## Game Mechanics
1. Paddle Control: The player controls the paddle, positioned on the right side of the game, using the palm of their hand (either left or right). Please note that the game is primarily designed for right-handed players since the paddle is on the right side.
2. Scoring System: The objective is to accumulate as many points as possible by successfully bouncing the ball back using the paddle. As the game progresses, it becomes more challenging, and the score awarded for each successful bounce increases relative to the ball's current velocity at the time of impact.
3. Lives: The player starts with 4 lives, indicated by hearts. Each time the player misses the ball, one life is deducted. The ball gets reset to its initial deployed position and starts at a lower velocity than during the miss. To be exact, the ball is redeployed at a velocity, where its smaller by 6 in both x and y velocity. 
4. Obstacles: Obstacles are positioned on the left side of the screen:
   - The far-left obstacle moves the fastest.
   - The obstacle located directly to the left of the paddle moves slowly but becomes increasingly deadly as the ball speed increases.
## Design Considerations
### Transparent Background Containing Laptop Camera Feed View
Initially, my setup featured the laptop camera feed view on a separate panel. The idea was to provide the user information on what hand was being used to move the paddle and what hand region maps to the paddle. However, this made my laptop display extremely cluttered, and it was tough to keep track of the mapping when the ball is moving extremely fast. I have converted this display to the game display's transparent background, which still allows the game elements to be at the forefront of attention, while providing with user with guidance during play. 
### Using Hand Velocity-Constrained Movement over Raw Hand Position Movement
When I initially designed the game, I simply mapped hand position to the paddle's top-left corner y-coordinate. This allowed the paddle to be extremely responsive to hand movement, but also enabled "paddle jumps". These "paddle jumps" are when the hand quickly moves away from the current paddle position forcing the paddle to jump or instant teleport to the new position. This caused a lot of trouble in preventing the paddle from overlapping the ball during this "paddle jump". Later, I played a couple of series of Atari's Pong game and I noticed the paddle is restricted to moving a finite velocity, which ensures difficulty in the game and requires players to predict ball trajectories. Thus, I decided to incorporate hand-paddle mapping movement restrained by a maximum paddle velocity in my version to ensure difficulty and also minimize these troublesome jumps. Of course, if the hand is detected as either above or below game bounds, the paddle should respectively move directly below the top wall or above the bottom wall.  
### Ball Velocity Capped at Slightly Below 1/2 of Frame Rate
This change is designed to prevent a visual aliasing effect where there appears to be 2 "balls" (in reality there is 1) moving along the same trajectory in the game. If there is no maximum ball velocity, the distance between these 2 "balls" grows as the speed of the ball increases. This virtual effect is in line with the Nyquist theorem where the sampling rate or frame rate in this case must be at least twice as large as the highest frequency signal, which in this specific scenario is the ball movement. Otherwise, as previously mentioned, the ball movement will essentially bleed over multiple consecutive frames resulting in this 2 "ball" phenomenon. 

### Tiered Scoring System & Lives
I interpreted this coding challenge as a survival challenge where the player must try to survive as long as possible to get the most amount of points. With that in mind, every survival challenge typically offers the player multiple lives or attempts to keep boosting his/her score. In this case, these lives are represented as hearts, which are lost for every time the ball exceeds the right game boundary. 

Since the ball is increasing in speed over time, it is only right that players in these higher speeds should be given more points. This is implemented in the tiered scoring system where the ball velocity upon impact with the paddle determines the amount of points received by the player. The breakdown is as follows...
1. Ball Velocity between 0 and 9: 10 points
2. Ball Velocity between 10 and 19: 20 points
3. Ball Velocity between 20 and 28: 30 points

If the player completely misses the ball (no contact with paddle), his/her point total does not change. Instead, he/she lose a life. However, if the player contacts the ball and misses (ball still goes out of game display's right bound), the player loses 20 points regardless of the current velocity of the ball and still loses a life. This distinction between complete miss and a partial miss is achieved through the bad hit detection system discussed in next section. 

### Bad Paddle Hit Detection (Partial Miss)
This was developed to address the concern that simply having the ball contact the paddle should not be enough to get points. There are instances where the paddle redirects the ball, but it still goes out of bounds. To detect this, each time the ball is hit by the paddle, there are specific metrics collected:
1. Ball's New X & Y Velocity Components (Ball Velocity increased by 2 in each component after each hit)
2. Time of Paddle-Ball Contact
3. Paddle's current position

When the ball hits the out-of-bounds area, that ball-(out of bounds) time is also recorded. 

Given this information, we can calculate the distance of the ball's longest path to the game's out of bounds area and compare that with the distance the ball is traveling in its current trajectory to that same area. The longest path is if the ball went directly up or down to the furthest wall (either the top or bottom wall) and then moved right to the game's out of bounds area. The path the ball currently takes is a diagonal from the contact point between ball and paddle to the game's out of bounds area. The longest path is just the sum of the vertical distance of the paddle from the furthest wall and the horizontal distance from the paddle to the wall. There is an implicit assumption that the ball is treated as point (not as at its actual circle), which is used to simplify calculations and indirectly gives a slight buffer or increase to the actual or real time required for traveling the longest path. The actual distance traveled by the ball is calculated by taking the difference between ball-paddle contact time and ball-(out of bounds) contact time and multiplying by the speed. Because I do not know what are units of this actual distance, I did trial collisions where the ball purposely went out of bounds to gauge a conversion factor that I can use to compare these 2 distances. Thus, I acknowledge this detection approach may not be 100% accurate, but this is still a viable approach.  

### Used Sounds
I have 2 sounds:
1. Ball-Paddle Contact Sound
2. Ball-(out of bounds) Sound

There is no ball-obstacle sound because it goes off way too often when the player is playing at higher speeds. 

## Resources & References:
1. [Murtaza's Computer Vision Game Development](https://www.youtube.com/watch?v=lDfplevUWRw&t=5459s)
   - Took starter template and used similar approach for game development and hand-tracking integration
2. [StackOverFlow Insight on Collision Detection](https://stackoverflow.com/questions/62864205/sometimes-the-ball-doesnt-bounce-off-the-paddle-in-pong-game?noredirect=1&lq=1)
   - Gained insight on how to approach ball-paddle collision
3. [DaFluffyPotato Collision Detection](https://www.youtube.com/watch?v=a_YTklVVNoQ&t=670s)
   - Used framework for defining ball movement and collision detection
4. [Game Font Location](https://www.fontspace.com/category/ttf)
   - Source of font used in game
5. [Game Sounds](https://opengameart.org/content/nes-sounds)
   - Source of game sounds used 
6. [Paddle Art](https://opengameart.org/content/pong-programmer-art)
   - Source of Paddle Design used in game
7. [ChatGPT](https://chat.openai.com)
   - Used for debugging code issues and verifying correct syntax usage