import gradio as gr
import json
from datetime import date, datetime

# ============================================================
# 🛳 Base Boat Class
# ============================================================


class Boat:
    # Create name, launch date, home port, and flag parameters for the ship
    def __init__(self, name: str, launch_date, home_port: str, flag: str):
        # Validate input types and values
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Ship name must be a non-empty string.")
        if not isinstance(home_port, str) or not home_port.strip():
            raise ValueError("Home port must be a non-empty string.")
        if not isinstance(flag, str) or not flag.strip():
            raise ValueError("Flag must be a non-empty string.")
        if launch_date is None:
            raise ValueError(
                "Launch date cannot be empty. Please input a date.")
        # Convert timestamp from Gradio to datetime.date
        if isinstance(launch_date, (int, float)):
            launch_date = datetime.fromtimestamp(launch_date).date()

        # Store attributes
        self.name = name
        self.launch_date = launch_date
        self.home_port = home_port
        self.flag = flag

        # Track which fleet does this boat belong to
        self.current_fleet = None

        # Keep a record of all fleets
        self.fleet_history = []

        # Track ship position and position history
        self.current_position = None
        self.position_logs = []

    # Create and return a dictionary containing all ship information
    def to_dict(self) -> dict:
        return {
            "name": self.name,  # Ship's name
            "launch_date": str(self.launch_date), # Convert date object to string
            "home_port": self.home_port,  # Home port name
            "flag": self.flag,  # Country flag
            "current_position": self.current_position,  # Current position
            "position_logs": self.position_logs  # Position history
        }

    def log_position(self, position: str):
        # Log the ship's current position
        timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.current_position = position
        log_entry = f"[{timestamp}] Position: {position}"
        self.position_logs.append(log_entry)
        return f"📍 {self.name} position logged: {position}"

    def get_position_history(self):
        # Get the ship's position history
        if not self.position_logs:
            return f"🗒️ No position logs recorded for {self.name}."
        return f"📍 Position History for {self.name}:\n" + "\n".join(self.position_logs)

    # Return text to display ship information
    def __repr__(self) -> str:
        launch_date = self.launch_date
        # Format the launch date properly
        if isinstance(self.launch_date, (int, float)):
            launch_date = str(datetime.fromtimestamp(launch_date).date())
        elif isinstance(self.launch_date, str):
            try:
                launch_date = str(datetime.fromisoformat(launch_date).date())
            except ValueError:
                pass  # Keep as string if not ISO formatted

        position_info = f"Current Position: {self.current_position}" if self.current_position else "Current Position: Unknown"

        return (
            f"Ship Name: {self.name}\n"
            f"Launch Date: {launch_date}\n"
            f"Home Port: {self.home_port}\n"
            f"Flag: {self.flag}\n"
            f"{position_info}"
        )

# ============================================================
# 🚢 CargoBoat Class (inherits from Boat)
# ============================================================

# Create CargoBoat class


class CargoBoat(Boat):
    def __init__(self, name: str, launch_date, home_port: str, flag: str, cargo_capacity: float):
        # reuse parameters from parent class Boat
        super().__init__(name, launch_date, home_port, flag)

        # -- Validation --
        # Validate cargo_capacity is a number (int or float)
        if not isinstance(cargo_capacity, (int, float)):
            raise TypeError("Cargo capacity must be a number (int or float).")

        # Validate cargo_capacity is positive
        if cargo_capacity < 0:
            raise ValueError(
                "Cargo capacity must be a positive value greater than zero.")

        # store cargo_capacity attributes
        self.cargo_capacity = cargo_capacity

    def to_dict(self) -> dict:
        # Create and return a dictionary containing cargo ship information
        base_dict = super().to_dict()  # Get dictionary from the parent Boat class
        # Add cargo-specific field
        base_dict["cargo_capacity"] = self.cargo_capacity
        return base_dict

    def __repr__(self) -> str:
        # Return text to display cargo ship information
        base_info = super().__repr__()  # Reuse parent's display text
        return (
            f"{base_info}\n"
            f"Cargo Capacity: {self.cargo_capacity:.2f} tons"
        )

# ============================================================
# ⚔️ MilitaryBoat Class (inherits from Boat)
# ============================================================

# Create a military ship


class MilitaryBoat(Boat):
    def __init__(self, name: str, launch_date, home_port: str, flag: str, weapon_count: float, is_authorised_by_gov: bool):
        # reuse parameters from parent class Boat
        super().__init__(name, launch_date, home_port, flag)

        # -- Validations --
        # Validate weapon_count is a number (int or float)
        if not isinstance(weapon_count, (int, float)):
            raise TypeError("Weapon count must be a number (int or float).")

        # Validate weapon_count is 0 or positive
        if weapon_count < 0:
            raise ValueError("Weapon count must be zero or a positive value.")

        # Validate is_authorised_by_gov
        if not isinstance(is_authorised_by_gov, bool):
            raise TypeError(
                "Authorisation status must be a boolean value (True or False).")

        # -- Store attributes --
        self.weapon_count = weapon_count
        self.is_authorised_by_gov = is_authorised_by_gov

    def to_dict(self) -> dict:
        # Create and return a dictionary containing military ship information
        base_dict = super().to_dict()  # Get dictionary from the parent Boat class

        # -- Add military-specific field --
        base_dict["weapon_count"] = self.weapon_count
        base_dict["is_authorised_by_gov"] = self.is_authorised_by_gov
        return base_dict

    def __repr__(self) -> str:
        # Return text to display military ship information
        base_info = super().__repr__()  # Reuse parent's display text
        return (
            f"{base_info}\n"
            f"Weapon Count: {self.weapon_count}\n"
            f"Authorised by Government: {self.is_authorised_by_gov}"
        )

# ============================================================
# ⚓ Fleet Class
# ============================================================

class Fleet:
    def __init__(self):
        self.boats = []  # store all boars in the fleet
        self.logs = []    # store log entries

    # add boat to fleet
    def add_boat(self, boat):
        if not isinstance(boat, Boat):
            return "❌ Only Boat objects can be added."
        self.boats.append(boat)
        boat.current_fleet = self
        boat.fleet_history.append(self)
        self.record_log(f"{boat.name} joined the fleet.")
        return f"✅ {boat.name} successfully added to fleet"

    def list_boats(self):
        if not self.boats:
            return "The fleet is empty!"
        return "\n\n".join(str(b) for b in self.boats)  # Join all boat details

    def sort_boats(self, by="name"):
        if not self.boats:
            return "Empty fleet, no boats to sort"

         # Sort the list of boats alphabetically by name
        self.boats.sort(key=lambda boat: boat.name)
        return "✅ Fleet sorted by ship name."

    def filter_boats(self, keyword):
        if not self.boats:
            return "Fleet is empty, no boats to filter."

        # create a list of matching boats
        results = [
            b for b in self.boats
            if keyword.lower() in b.name.lower()
            or keyword.lower() in b.home_port.lower()
            or keyword.lower() in b.flag.lower()
        ]

        # if no match, return message
        if not results:
            return f"No results found for {keyword}."
        # join all matching boat details
        return "\n\n".join(str(b) for b in results)

    def transfer_boat(self, boat, new_fleet):
        # check if boat exists in fleet
        if boat not in self.boats:
            return f"❌ {boat.name} not found in this fleet."
        # remove from this fleet
        self.boats.remove(boat)
        self.record_log(f"{boat.name} left this fleet for another.")
        # add to new fleet
        new_fleet.add_boat(boat)
        self.record_log(f"{boat.name} transferred to new fleet.")
        # confirm transfer
        return f"🔁 {boat.name} transferred successfully."

    def remove_boat(self, boat):
        """Remove a boat from the fleet"""
        if boat not in self.boats:
            return f"❌ {boat.name} not found in this fleet."
        self.boats.remove(boat)
        boat.current_fleet = None
        self.record_log(f"{boat.name} was removed from the fleet.")
        return f"✅ {boat.name} successfully removed from fleet"

    def record_arrival(self, boat: Boat, location: str):
        if boat not in self.boats:
            return f"❌ {boat.name} is not in this fleet."
        self.record_log(f"{boat.name} arrived at {location}.")
        return f"📍 {boat.name} arrival recorded at {location}."

    def record_log(self, message: str):
        timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        entry = f"[{timestamp}] {message}"
        self.logs.append(entry)

    def show_logs(self):
        if not self.logs:
            return "🗒️ No logs recorded yet."
        return "\n".join(self.logs)

    def generate_status_report(self):
        if not self.boats:
            return "📊 Fleet Status Report:\n\nFleet is currently empty."

        total_boats = len(self.boats)
        cargo_boats = sum(1 for b in self.boats if isinstance(b, CargoBoat))
        military_boats = sum(
            1 for b in self.boats if isinstance(b, MilitaryBoat))
        regular_boats = total_boats - cargo_boats - military_boats

        report = f"📊 Fleet Status Report:\n\n"
        report += f"Total Boats: {total_boats}\n"
        report += f"Regular Boats: {regular_boats}\n"
        report += f"Cargo Boats: {cargo_boats}\n"
        report += f"Military Boats: {military_boats}\n"

        if cargo_boats > 0:
            total_cargo_capacity = sum(
                b.cargo_capacity for b in self.boats if isinstance(b, CargoBoat))
            report += f"Total Cargo Capacity: {total_cargo_capacity:.2f} tons\n"

        return report

    def save_to_file(self):
        try:
            filename = "fleet_data.json"
            data = {
                "boats": [boat.to_dict() for boat in self.boats],
                "logs": self.logs,
                "saved_date": str(date.today())
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return f"✅ Fleet data saved to {filename}"
        except Exception as e:
            return f"❌ Error saving fleet data: {e}"

    def load_from_file(self):
        try:
            filename = "fleet_data.json"
            with open(filename, 'r') as f:
                data = json.load(f)

            self.boats = []  # Clear existing boats
            self.logs = data.get("logs", [])  # load logs

            for boat_data in data.get("boats", []):
                # Parse the launch date from the saved data
                launch_date = boat_data["launch_date"]

                if "cargo_capacity" in boat_data:
                    boat = CargoBoat(
                        boat_data["name"],
                        launch_date,
                        boat_data["home_port"],
                        boat_data["flag"],
                        boat_data["cargo_capacity"]
                    )
                elif "weapon_count" in boat_data:
                    boat = MilitaryBoat(
                        boat_data["name"],
                        launch_date,
                        boat_data["home_port"],
                        boat_data["flag"],
                        boat_data["weapon_count"],
                        boat_data["is_authorised_by_gov"]
                    )
                else:
                    boat = Boat(
                        boat_data["name"],
                        launch_date,
                        boat_data["home_port"],
                        boat_data["flag"]
                    )

                # Restore position data if available
                if "current_position" in boat_data:
                    boat.current_position = boat_data["current_position"]
                if "position_logs" in boat_data:
                    boat.position_logs = boat_data["position_logs"]

                self.boats.append(boat)
                boat.current_fleet = self
                boat.fleet_history.append(self)

            return f"✅ Loaded {len(self.boats)} boats from {filename}"
        except FileNotFoundError:
            return "ℹ️ No saved fleet data found. Starting with empty fleet."
        except Exception as e:
            return f"❌ Error loading fleet data: {e}"

# ============================================================
# 🌐 Gradio UI (User Interface)
# ============================================================

def create_ui(registry: Fleet):
    # Creates the Gradio web interface.
  # Helper functions to interact with the registry and update the UI
    def add_and_update(name, location, flag, launch_date, ship_type, cargo_capacity, weapon_count, gov_auth, current_log):
        try:

            # Create different types of boats based on user choice
            if ship_type == "Boat":
                new_boat = Boat(name, launch_date, location, flag)
            elif ship_type == "CargoShip":
                # Use the actual cargo capacity input from the user
                new_boat = CargoBoat(
                    name, launch_date, location, flag, cargo_capacity or 1000)
            elif ship_type == "MilitaryBoat":
                # Use the actual inputs from the user
                new_boat = MilitaryBoat(
                    name, launch_date, location, flag, weapon_count or 0, gov_auth)

            # add boat to fleet
            result = registry.add_boat(new_boat)

        except Exception as e:
            result = f"❌ Error adding ship: {e}"

        # return the updated log and keep current input values
        return f"{current_log}\n> {result}", name, location, flag, launch_date, cargo_capacity, weapon_count, gov_auth

    def report_and_update(current_log):
        result = registry.generate_status_report()
        logs = registry.show_logs()
        new_log = f"{current_log}\n\n{result}\n"
        return new_log

    def list_and_update(current_log):
        result = registry.list_boats()
        new_log = f"{current_log}\n\n{result}\n"
        return new_log

    def save_and_update(current_log):
        result = registry.save_to_file()
        new_log = f"{current_log}\n> {result}"
        return new_log

    def load_and_update(current_log):
        result = registry.load_from_file()
        new_log = f"{current_log}\n> {result}"
        # After loading, also list the boats to show what was loaded
        list_result = registry.list_boats()
        return f"{new_log}\n\n{list_result}\n"

    def filter_and_update(keyword, current_log):
        if not keyword or not keyword.strip():
            result = "❌ Please enter a keyword to filter by."
        else:
            result = registry.filter_boats(keyword.strip())
        new_log = f"{current_log}\n\n🔍 Filter Results for '{keyword}':\n{result}\n"
        return new_log

    def sort_and_update(current_log):
        result = registry.sort_boats()
        new_log = f"{current_log}\n> {result}"
        # After sorting, show the sorted list
        list_result = registry.list_boats()
        return f"{new_log}\n\n{list_result}\n"

    def logs_and_update(current_log):
        result = registry.show_logs()
        new_log = f"{current_log}\n\n📝 Fleet Logs:\n{result}\n"
        return new_log

    def record_arrival_and_update(ship_name, location, current_log):
        if not ship_name or not location:
            result = "❌ Please select a ship and enter a location."
        else:
            # Find the ship by name
            selected_ship = None
            for boat in registry.boats:
                if boat.name == ship_name:
                    selected_ship = boat
                    break

            if selected_ship:
                result = registry.record_arrival(selected_ship, location)
            else:
                result = f"❌ Ship '{ship_name}' not found in fleet."

        new_log = f"{current_log}\n> {result}"
        return new_log

    def log_position_and_update(ship_name, position, current_log):
        if not ship_name or not position:
            result = "❌ Please select a ship and enter a position."
        else:
            # Find the ship by name
            selected_ship = None
            for boat in registry.boats:
                if boat.name == ship_name:
                    selected_ship = boat
                    break

            if selected_ship:
                result = selected_ship.log_position(position)
            else:
                result = f"❌ Ship '{ship_name}' not found in fleet."

        new_log = f"{current_log}\n> {result}"
        return new_log

    def view_position_history_and_update(ship_name, current_log):
        if not ship_name:
            result = "❌ Please select a ship to view history."
        else:
            # Find the ship by name
            selected_ship = None
            for boat in registry.boats:
                if boat.name == ship_name:
                    selected_ship = boat
                    break

            if selected_ship:
                result = selected_ship.get_position_history()
            else:
                result = f"❌ Ship '{ship_name}' not found in fleet."

        new_log = f"{current_log}\n\n{result}\n"
        return new_log

    def remove_boat_and_update(ship_name, current_log):
        if not ship_name:
            result = "❌ Please select a ship to remove."
        else:
            # Find the ship by name
            selected_ship = None
            for boat in registry.boats:
                if boat.name == ship_name:
                    selected_ship = boat
                    break

            if selected_ship:
                result = registry.remove_boat(selected_ship)
            else:
                result = f"❌ Ship '{ship_name}' not found in fleet."

        new_log = f"{current_log}\n> {result}"
        return new_log

    def clear_console():
        """Clear the console like terminal clear command"""
        return "Welcome! Your command results will appear here."

    def update_ship_dropdown():
        choices = [boat.name for boat in registry.boats]
        return (gr.update(choices=choices),
                gr.update(choices=choices),
                gr.update(choices=choices),
                gr.update(choices=choices))

    # Define the Gradio interface layout
    with gr.Blocks(theme=gr.themes.Soft(), title="Fleet Command") as app:
        gr.HTML(
            """
            <style>
                body {background: radial-gradient(900px 500px at 10% 0%, #0b1220 0, #0b1220 30%, #0f172a 100%);}
                .hero {padding: 22px; border-radius: 18px; background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 60%, #a855f7 100%); color: #fff;
                     box-shadow: 0 10px 30px rgba(0,0,0,.25); border:1px solid rgba(255,255,255,.25)}
                .hero h1 {margin: 0; font-size: 26px; font-weight: 800;}
                .hero p {margin: 6px 0 0 0; opacity: .95}
                .terminal textarea {background:#0b1220!important; color:#ffffff!important; border-radius:14px!important;
                                    border:1px solid #1f2a44!important; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace!important;
                                    box-shadow: 0 8px 30px rgba(2, 8, 23, .6)}
                .terminal textarea::placeholder {color:#ffffff!important; opacity:0.7!important;}
                .terminal .label-wrap {color:#ffffff!important;}
                .terminal .label-wrap span {color:#ffffff!important;}
                .gr-button {border-radius: 999px!important; padding: 10px 14px!important; font-weight:700}
                .panel{background:#0c1326; border:1px solid #18233c; border-radius:16px; padding:14px; box-shadow: 0 10px 30px rgba(0,0,0,.25)}
                .gr-accordion{background:#0c1326!important; border-radius:14px!important; border:1px solid #18233c}
                .gr-accordion .label-wrap{font-weight:700}
            </style>
            <div class="hero">
              <h1>🚢 Fleet Command</h1>
              <p>Monitor and manage your fleet with a clean, modern interface.</p>
            </div>
            """
        )
        with gr.Row():
            with gr.Column(scale=2):
                log_textbox = gr.Textbox(
                    label="Log & Reports",
                    value="Welcome! Your command results will appear here.",
                    lines=16,
                    interactive=True,
                    elem_classes=["terminal"]  # styling only
                )
            with gr.Column(scale=1):
                with gr.Group(elem_classes=["panel"]):
                    gr.Markdown("### Quick Actions")
                    with gr.Row():
                        report_btn = gr.Button("📊 Generate Status Report")
                        list_btn = gr.Button("📋 List All Boats")
                    with gr.Row():
                        sort_btn = gr.Button("🔤 Sort Boats by Name")
                        logs_btn = gr.Button("📝 View Fleet Logs")
                    with gr.Row():
                        save_btn = gr.Button("💾 Save Registry")
                        load_btn = gr.Button("📂 Load Registry")
                    clear_btn = gr.Button("🧹 Clear Console")

        with gr.Tabs():
            with gr.TabItem("➕ Add a New Boat"):
                with gr.Row():
                    name_input = gr.Textbox(
                        label="Name", placeholder="e.g., HMS Albion")
                    home_port_input = gr.Textbox(
                        label="Location (Home Port)", placeholder="e.g. London")
                with gr.Row():
                    date_input = gr.DateTime(
                        label="Launch Date", include_time=False)
                    flag_input = gr.Textbox(label="Flag", placeholder="eg. UK")
                with gr.Row():
                    ship_type = gr.Dropdown(
                        ["Boat", "CargoShip", "MilitaryBoat"],
                        label="Ship Type",
                        value="Boat"
                    )
                # inputs specify for cargo ship and military ship:
                with gr.Row(visible=False) as cargo_inputs:
                    cargo_capacity_input = gr.Number(
                        label="Cargo Capacity (tons)")
                with gr.Row(visible=False) as military_inputs:
                    weapon_count_input = gr.Number(label="Weapon Count")
                    gov_auth_input = gr.Checkbox(
                        label="Authorised by Government?")

                # extra fields based on ship type
                def toggle_extra_field(selected_type):
                    if selected_type == "CargoShip":
                        return gr.update(visible=True), gr.update(visible=False)
                    elif selected_type == "MilitaryBoat":
                        return gr.update(visible=False), gr.update(visible=True)
                    else:
                        # Hide both
                        return gr.update(visible=False), gr.update(visible=False)

                ship_type.change(
                    fn=toggle_extra_field,
                    inputs=[ship_type],
                    outputs=[cargo_inputs, military_inputs]
                )

                add_btn = gr.Button("Add Ship")

            with gr.TabItem("📍 Ship Movement & Locations"):
                gr.Markdown("### Record Ship Arrivals")
                with gr.Row():
                    ship_select = gr.Dropdown(
                        label="Select Ship",
                        choices=[],
                        interactive=True
                    )
                    # distinct from Add tab input to avoid name collision
                    arrival_location_input = gr.Textbox(
                        label="Location",
                        placeholder="e.g., Port of London, Atlantic Ocean"
                    )
                    record_arrival_btn = gr.Button("📍 Record Arrival")

                gr.Markdown("### Ship Position Logging")
                with gr.Row():
                    ship_position_select = gr.Dropdown(
                        label="Select Ship",
                        choices=[],
                        interactive=True
                    )
                    position_input = gr.Textbox(
                        label="Position",
                        placeholder="e.g., 51.5074°N, 0.1278°W or Mediterranean Sea"
                    )
                    log_position_btn = gr.Button("📍 Log Position")

                with gr.Row():
                    ship_history_select = gr.Dropdown(
                        label="Select Ship for History",
                        choices=[],
                        interactive=True
                    )
                    view_history_btn = gr.Button("📜 View Position History")

            with gr.TabItem("🔍 Filter Boats"):
                with gr.Row():
                    filter_input = gr.Textbox(
                        label="Search Keyword",
                        placeholder="Enter name, port, or flag to search for...",
                        scale=3
                    )
                    filter_btn = gr.Button("🔍 Filter", scale=1)
                gr.Markdown(
                    "*Search will look for matches in ship name, home port, and flag*")

            with gr.TabItem("➖ Remove a Boat"):
                gr.Markdown("### Remove Ship from Fleet")
                with gr.Row():
                    ship_remove_select = gr.Dropdown(
                        label="Select Ship to Remove",
                        choices=[],
                        interactive=True
                    )
                    remove_boat_btn = gr.Button("🗑️ Remove Ship")

        # Connect UI components to the helper functions
        add_btn.click(
            fn=add_and_update,
            inputs=[
                name_input,
                home_port_input,
                flag_input,
                date_input,
                ship_type,
                cargo_capacity_input,
                weapon_count_input,
                gov_auth_input,
                log_textbox
            ],
            outputs=[log_textbox, name_input, home_port_input, flag_input,
                     date_input, cargo_capacity_input, weapon_count_input, gov_auth_input]
        )
        report_btn.click(fn=report_and_update, inputs=[
                         log_textbox], outputs=[log_textbox])
        list_btn.click(fn=list_and_update, inputs=[
                       log_textbox], outputs=[log_textbox])
        sort_btn.click(fn=sort_and_update, inputs=[
                       log_textbox], outputs=[log_textbox])
        save_btn.click(fn=save_and_update, inputs=[
                       log_textbox], outputs=[log_textbox])
        load_btn.click(fn=load_and_update, inputs=[
                       log_textbox], outputs=[log_textbox])
        filter_btn.click(fn=filter_and_update, inputs=[
                         filter_input, log_textbox], outputs=[log_textbox])
        logs_btn.click(fn=logs_and_update, inputs=[
            log_textbox], outputs=[log_textbox])

        record_arrival_btn.click(fn=record_arrival_and_update, inputs=[
            ship_select, arrival_location_input, log_textbox], outputs=[log_textbox])

        log_position_btn.click(fn=log_position_and_update, inputs=[
            ship_position_select, position_input, log_textbox], outputs=[log_textbox])
        view_history_btn.click(fn=view_position_history_and_update, inputs=[
            ship_history_select, log_textbox], outputs=[log_textbox])

        # Connect the missing buttons
        clear_btn.click(fn=clear_console, outputs=[log_textbox])
        remove_boat_btn.click(fn=remove_boat_and_update, inputs=[
            ship_remove_select, log_textbox], outputs=[log_textbox])

        # Update ship dropdown when boats are added, loaded, or removed
        add_btn.click(fn=update_ship_dropdown, outputs=[
            ship_select, ship_position_select, ship_history_select, ship_remove_select])
        load_btn.click(fn=update_ship_dropdown, outputs=[
            ship_select, ship_position_select, ship_history_select, ship_remove_select])
        remove_boat_btn.click(fn=update_ship_dropdown, outputs=[
            ship_select, ship_position_select, ship_history_select, ship_remove_select])

    return app


# --- Main execution block ---
if __name__ == "__main__":
    # Create a single instance
    fleet_registry = Fleet()
    # Load any existing data on startup
    initial_load_message = fleet_registry.load_from_file()
    print(initial_load_message)  # Print to terminal for the developer
    # Create and launch the Gradio app
    web_app = create_ui(fleet_registry)
    web_app.launch(share=True)
