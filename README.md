# 🚢 Fleet Command
This README file focuses on the new features and functionality of the script and things I have learnt when doing this project. 

---
## ✅ What I Added
### 1. Better Saving System
I added a **Save Registry** feature so the fleet data can be saved into a JSON file.  
To make sure the data saved is always correct, the safest way is:
1. Press 📋 List All Boats to check all current boats.  
2. Make sure it shows the fleet you want to keep.  
3. Then press 💾 Save Registry.  

This way, the registry file will always match what’s currently on the screen.

### 2. Position Tracking
Each boat can now record its **current position** and save it with a timestamp.  
You can also view a full position history for each ship, which makes tracking easier.

### 3. Arrival Logs
When a boat arrives at a port, you can record an **arrival log**.  
This helps keep a record of all major events for your fleet.

### 4. Filtering and Sorting
I added a simple **filter** that lets you search by name, home port, or flag.  
You can also **sort boats alphabetically** by their name.

### 5. More User-Friendly Interface
- The console can be cleared easily with one click.  
- The design looks cleaner and easier to navigate.
- The gradio theme has changed to Soft

---
## 🧭 How It Works
- When you add or edit a boat, the app updates the fleet in memory.  
- Pressing Save Registry writes everything into a file called `fleet_data.json`.  
- When you restart the app, it loads data from that file automatically, so you can continue where you left off.

---
## 🧠 What I Learned

This project taught me a lot — not only about Gradio, but also about organizing code and thinking carefully about how data should be handled.

### 1. Working with Gradio
- I learned how to make components appear or hide depending on user input.  
- I also learned how to display helpful messages instead of leaving blank screens. (Place holders)

### 2. Saving and Loading Data
- I realized that data should be saved in a consistent format (like JSON).  

### 3. Handling Errors
- Adding clear error messages helped me understand what went wrong during testing using `except Exception as e`
- I learned that a friendly message can make debugging much easier.

### 4. Writing Cleaner Code
- I started breaking big functions into smaller ones.  
- I added type hints and comments so that it’s easier to read later.

---
## 🧪 Things I Want to Try Next
- Add an option to export fleet reports to a CSV or PDF file.  
- Show positions on a simple map view.  
