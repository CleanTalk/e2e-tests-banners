from selenium import webdriver

from inc.options import *

# Define driver as a global variable
driver = None

def browser_init():
    global driver
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "CleanTalk Bot to check connection 1.0 (https://cleantalk.org/help/cleantalk-servers-ip-addresses)")
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    #options.add_argument('-private') # открывает в режиме инкогнито

    if br_headless == 'yes':
        options.headless = True
    if browser_JS == 'no':
        options.set_preference("javascript.enabled", False)
    driver = webdriver.Firefox(options=options)


    if br_headless == 'yes':
        driver.set_window_size(2560, 1600) # для headless там делее все равно full screen
    else:
        # Calculate 80% of screen size
        import tkinter as tk
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        
        width = int(screen_width * 0.9)
        height = int(screen_height * 0.8)
        
        # Position window at center of screen
        x_position = int((screen_width - width) / 2)
        y_position = int((screen_height - height) / 2)
        
        driver.set_window_size(width, height)
        driver.set_window_position(x_position, y_position)
        
        print(f"Window set to {width}x{height} (90% of screen size)")
    
    return driver
