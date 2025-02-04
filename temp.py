# Using Keyboard module in Python 
import keyboard 
  
# It writes the content to output 
# keyboard.write("GEEKS FOR GEEKS\n") 
  
# It writes the keys r, k and endofline  
keyboard.press_and_release(35)

def w_press_callback(e):
    print('w key is pressed')
    
def w_release_callback(e):
    print('w key is released')
  
keyboard.on_press(w_press_callback)
keyboard.on_release(w_release_callback)
# it blocks until ctrl is pressed 
keyboard.wait(57)