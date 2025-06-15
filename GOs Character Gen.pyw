import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.ttk as ttk
import random, os, json

# ==========================
# Global State Variables
# ==========================
global_root = None      # Dictionary for root stats and derived values.
global_armor = []       # List of armor dictionaries.
global_weapons = []     # List of weapon dictionaries.
global_powers = []      # List of power dictionaries.
characters = {}         # Saved characters
groups = []             # Character groups
keywords = {}           # Keyword -> description
save_group_listbox = None
filter_group_var = None
filter_group_menu = None
keywords_listbox = None
keyword_desc_text = None
tooltip_window = None
encounters = {}
tracker_entities = []
encounter_listbox = None
encounter_char_listbox = None
tracker_listbox = None
tracker_display = None

# ==========================
# Presets Data and File Path
# ==========================
presets = {"root": {}, "armor": {}, "weapon": {}, "power": {}}
presets_dir = os.path.join(os.path.expanduser("~"), "Documents", "GOsCharacterGen")
presets_file = os.path.join(presets_dir, "presets.json")
os.makedirs(presets_dir, exist_ok=True)
characters_file = os.path.join(presets_dir, "characters.json")
keywords_file = os.path.join(presets_dir, "keywords.json")
armor_file = os.path.join(presets_dir, "armor.json")
weapon_file = os.path.join(presets_dir, "weapons.json")
encounters_file = os.path.join(presets_dir, "encounters.json")

# ==========================
# Data Definitions
# ==========================

# These JSON files contain lists of armors and weapons.  If they do not exist in
# the user's install directory they will be created from the bundled defaults.
default_armor_path = os.path.join(os.path.dirname(__file__), "default_armors.json")
default_weapon_path = os.path.join(os.path.dirname(__file__), "default_weapons.json")

armors_data = []
weapons_data = []

def load_armor_data():
    global armors_data
    if os.path.exists(armor_file):
        try:
            with open(armor_file, "r") as f:
                armors_data = json.load(f)
        except Exception as e:
            print("Error loading armor file:", e)
            armors_data = json.load(open(default_armor_path))
    else:
        armors_data = json.load(open(default_armor_path))
        try:
            with open(armor_file, "w") as f:
                json.dump(armors_data, f, indent=2)
        except Exception as e:
            print("Error saving armor file:", e)

def load_weapon_data():
    global weapons_data
    if os.path.exists(weapon_file):
        try:
            with open(weapon_file, "r") as f:
                weapons_data = json.load(f)
        except Exception as e:
            print("Error loading weapon file:", e)
            weapons_data = json.load(open(default_weapon_path))
    else:
        weapons_data = json.load(open(default_weapon_path))
        try:
            with open(weapon_file, "w") as f:
                json.dump(weapons_data, f, indent=2)
        except Exception as e:
            print("Error saving weapon file:", e)

def detect_list_keywords():
    """Add any tags found in armor or weapon lists to the keywords dict."""
    found = set()
    for a in armors_data:
        if len(a) > 2:
            found.update(a[2])
    for w in weapons_data:
        if len(w) > 2 and w[2]:
            found.update(t.strip() for t in w[2].split(',') if t.strip())
    added = False
    for kw in found:
        if kw not in keywords:
            keywords[kw] = "Description TBD"
            added = True
    if added:
        save_keywords_to_file()

# Power list: index 0 corresponds to Frequency #1, etc.
power_list = [
    "Absolute Silence", "Adaptive Resistance", "Age Immunity", "Air Manipulation",
    "Animal Communication", "Atomic Duplicate Fabrication", "Bodily Weapon Suite", "Cloning",
    "Configurable General Locator", "Contagious Configurable Pathogen Generator", "CQC Correction System",
    "Danger Sense", "Defense", "DNA Manipulation", "Earth Manipulation", "Eidetic Memory",
    "Electricity Absorption", "Electricity Manipulation", "Energy Blasts", "Energy Form",
    "Energy Steal", "Enhanced Awareness", "Enhanced Biometric Tracking", "Enhanced Fighting",
    "Enhanced Fortitude", "Enhanced Great One Authority", "Enhanced Hearing", "Enhanced Intelligence",
    "Enhanced Presence", "Enhanced Will", "Enhanced Smell/Taste", "Enhanced Speed",
    "Enhanced Stamina", "Enhanced Strength", "Environmental Condition Generator",
    "Extreme Temperature Immunity", "Fire Absorption", "Fire Manipulation", "Flight",
    "Forcefield Projection", "Growth/Shrinking", "Hardlight Summoning", "Hawkeye", "Healing",
    "Illusions", "Instant Information Internalization", "Invisibility", "Kinetic Absorption",
    "Light Manipulation", "Local Environmental Control", "Luck Control", "Matter Absorption",
    "Matter Transmutation", "Mind Control", "Mind Reading", "Nanite Cloud Control", "Nanite Nucleation",
    "Nanite Nullification", "Nanite Overclock", "Nanoscopic Sight", "Personal Pocket Dimension",
    "Personality Instinct", "Phasing", "Poison Immunity", "Portals", "Predictive Precognition",
    "Predictive Premonition", "Projectile Reflect", "Proximity Alarm", "Psychometry",
    "Radiation Immunity", "Regeneration", "Regenerative Immortality", "Repulsion Burst",
    "Shapeshifting", "Skill Mastery", "Summon Micro Assistants", "Synaptic Regen",
    "Tactical Targeting System", "Tag Tracker", "Technopathy", "Telekinesis", "Telepathy",
    "Teleportation", "Unlimited Digestion", "Water Manipulation", "Water/Nutrient Recycle",
    "Weather Manipulation", "Webbing", "X-ray Vision"
]

# ==========================
# Advanced Powers Generation Functions
# ==========================
def generate_single_power(existing_powers):
    while True:
        r = random.randint(1, 100)
        if 1 <= r <= 90:
            return {'frequency': r, 'name': power_list[r-1], 'rank': 1, 'alpha': False}
        elif 91 <= r <= 99:
            if existing_powers:
                chosen = random.choice(existing_powers)
                chosen['rank'] += 1
            return None
        elif r == 100:
            if existing_powers:
                chosen = random.choice(existing_powers)
                chosen['rank'] += 5
                chosen['alpha'] = True
                return None
            else:
                continue

def generate_powers_advanced():
    global global_powers
    global_powers = []
    try:
        base_num = int(entry_power_base.get())
        extra_chance = float(entry_power_extra.get())
        extra_ranks_chance = float(entry_power_ranks.get())
    except ValueError:
        return
    for i in range(base_num):
        new_power = generate_single_power(global_powers)
        if new_power is not None:
            global_powers.append(new_power)
        current_extra = extra_chance
        while True:
            roll = random.randint(1, 100)
            if roll <= current_extra:
                new_extra = generate_single_power(global_powers)
                if new_extra is not None:
                    global_powers.append(new_extra)
                current_extra -= 1
                if current_extra <= 0:
                    break
            else:
                break
    for power in global_powers:
        while random.randint(1, 100) <= extra_ranks_chance:
            power['rank'] += 1
    consolidate_powers()
    refresh_display()

def consolidate_powers():
    global global_powers
    consolidated = {}
    for power in global_powers:
        key = (power['frequency'], power['name'])
        if key in consolidated:
            consolidated[key]['rank'] += power['rank']
            if power.get('alpha', False):
                consolidated[key]['alpha'] = True
        else:
            consolidated[key] = power.copy()
    global_powers = list(consolidated.values())

# ==========================
# Advanced Armor Generation Function
# ==========================
def generate_armors_advanced():
    global global_armor
    try:
        num_armors = int(entry_armor_num.get())
    except ValueError:
        num_armors = 1
    specific_tags_str = entry_armor_tag.get().strip().lower()
    if specific_tags_str:
        specific_tags = [tag.strip() for tag in specific_tags_str.split(",") if tag.strip()]
    else:
        specific_tags = []
    filtered = []
    for armor in armors_data:
        armor_tags = [t.lower() for t in armor[2]]
        if all(req_tag in armor_tags for req_tag in specific_tags):
            filtered.append(armor)
    if not filtered:
        filtered = armors_data
    selected = []
    for i in range(num_armors):
        selected.append(random.choice(filtered))
    global_armor = []
    for armor in selected:
        name, bonus, tags = armor
        global_armor.append({
            'name': name,
            'bonus': bonus,
            'tags': tags
        })
    refresh_display()

# ==========================
# Advanced Weapon Generation Function
# ==========================
def generate_weapons_advanced():
    global global_weapons, weapons_data
    try:
        num_weapons = int(entry_weapon_num.get())
    except ValueError:
        num_weapons = 1
    specific_tags_str = entry_weapon_tag.get().strip().lower()
    if specific_tags_str:
        required_tags = [tag.strip() for tag in specific_tags_str.split(",") if tag.strip()]
    else:
        required_tags = []
    filtered = []
    for weapon in weapons_data:
        weapon_tags = weapon[2].lower() if weapon[2] else ""
        if all(req_tag in weapon_tags for req_tag in required_tags):
            filtered.append(weapon)
    if not filtered:
        filtered = weapons_data
    selected = []
    for i in range(num_weapons):
        selected.append(random.choice(filtered))
    global_weapons = []
    for weapon in selected:
        name, damage, tags, stat = weapon
        global_weapons.append({"name": name, "damage": damage, "tags": tags, "stat": stat})
    refresh_display()

# ==========================
# Root and Display Functions
# ==========================
def refresh_display():
    if global_root is not None:
        total_dex_penalty = 0
        total_agl_penalty = 0
        total_speed_penalty = 0
        if global_armor:
            for armor in global_armor:
                tags_lower = [t.lower() for t in armor['tags']]
                if "power" in tags_lower:
                    penalty_dex = 0
                    penalty_agl = 0
                    penalty_speed = 0
                else:
                    if "medium" in tags_lower:
                        penalty_dex = -1
                        penalty_agl = -1
                        penalty_speed = 0
                    elif "heavy" in tags_lower:
                        penalty_dex = -3
                        penalty_agl = -3
                        penalty_speed = -5
                    else:
                        penalty_dex = 0
                        penalty_agl = 0
                        penalty_speed = 0
                total_dex_penalty += penalty_dex
                total_agl_penalty += penalty_agl
                total_speed_penalty += penalty_speed
        base_agl = global_root['AGL']
        effective_agl = base_agl + total_agl_penalty
        agl_display = f"{base_agl}+(AGL){total_agl_penalty}({effective_agl})"
        base_dex = global_root['DEX']
        effective_dex = base_dex + total_dex_penalty
        dex_display = f"{base_dex}+(DEX){total_dex_penalty}({effective_dex})"
        base_sta = global_root['STA']
        toughness_base = global_root['Toughness']
        toughness_total = toughness_base + base_sta
        effective_speed = 30 + total_speed_penalty
        speed_display = f"({effective_speed})"
        root_line = (f"STR:{global_root['STR']} "
                     f"AGL:{agl_display} "
                     f"FGT:{global_root['FGT']} "
                     f"AWE:{global_root['AWE']} "
                     f"STA:{global_root['STA']} "
                     f"DEX:{dex_display} "
                     f"INT:{global_root['INT']} "
                     f"PRE:{global_root['PRE']}")
        dodge_total = global_root['Dodge'] + global_root['AGL']
        parry_total = global_root['Parry'] + global_root['FGT']
        fortitude_total = global_root['Fortitude'] + global_root['STA']
        will_total = global_root['Will'] + global_root['AWE']
        derived_line = (f"Dodge:{dodge_total} "
                        f"Parry:{parry_total} "
                        f"Fortitude:{fortitude_total} "
                        f"Toughness:{toughness_total} "
                        f"Will:{will_total} "
                        f"Speed:{speed_display}")
    else:
        root_line = ("STR: None AGL: None FGT: None AWE: None STA: None "
                     "DEX: None INT: None PRE: None")
        derived_line = ("Dodge: None Parry: None Fortitude: None Toughness: None Will: None Speed: None")
    if global_armor and len(global_armor) > 0:
        armor_lines = []
        for armor in global_armor:
            armor_lines.append(f"- {armor['name']} (Bonus: +{armor['bonus']}) [{', '.join(armor['tags'])}]")
        armor_section = "Armor:\n" + "\n".join(armor_lines)
    else:
        armor_section = "Armor:\nNone"
    if global_weapons:
        weapons_lines = []
        for weapon in global_weapons:
            base_damage = weapon['damage']
            effective_damage = base_damage
            mod_display = ""
            if global_root is not None:
                if weapon['stat'] == "STR":
                    mod = global_root['STR']
                    effective_damage = base_damage + mod
                    mod_display = f"{base_damage}+(STR){mod}({effective_damage})"
                elif weapon['stat'] == "DEX" and "finesse" in weapon['tags'].lower():
                    mod = global_root['DEX']
                    effective_damage = base_damage + mod
                    mod_display = f"{base_damage}+(DEX){mod}({effective_damage})"
                else:
                    mod_display = f"{base_damage}"
            else:
                mod_display = f"{base_damage}"
            dc_damage = effective_damage + 15
            tag_str = f", Tags: {weapon['tags']}" if weapon['tags'] else ""
            weapons_lines.append(f"- {weapon['name']} (Damage: {mod_display}(DC{dc_damage}){tag_str})")
        weapons_section = "Weapons:\n" + "\n".join(weapons_lines)
    else:
        weapons_section = "Weapons:\nNone"
    if global_powers:
        powers_lines = []
        for power in global_powers:
            alpha_str = " ALPHA" if power.get('alpha', False) else ""
            powers_lines.append(f"{power['rank']} #{power['frequency']} {power['name']}{alpha_str}")
        powers_section = "Powers:\n" + "\n".join(powers_lines)
    else:
        powers_section = "Powers:\nNone"
    output_text = f"{root_line}\n{derived_line}\n{armor_section}\n{weapons_section}\n{powers_section}\n"
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output_text)
    update_keyword_highlights()

def generate_root():
    global global_root
    STR = random.randint(-3, 4)
    AGL = random.randint(-3, 4)
    FGT = random.randint(-3, 4)
    AWE = random.randint(-3, 4)
    STA = random.randint(-3, 4)
    DEX = random.randint(-3, 4)
    INT = random.randint(-3, 4)
    PRE = random.randint(-3, 4)
    Dodge = AGL + random.randint(0, 6)
    Parry = FGT + random.randint(0, 6)
    Fortitude = STA + random.randint(0, 6)
    Will = AWE + random.randint(0, 6)
    Toughness = 0
    global_root = {
        'STR': STR, 'AGL': AGL, 'FGT': FGT, 'AWE': AWE,
        'STA': STA, 'DEX': DEX, 'INT': INT, 'PRE': PRE,
        'Dodge': Dodge, 'Parry': Parry, 'Fortitude': Fortitude,
        'Will': Will, 'Toughness': Toughness
    }
    entry_str.delete(0, tk.END); entry_str.insert(0, str(STR))
    entry_agl.delete(0, tk.END); entry_agl.insert(0, str(AGL))
    entry_fgt.delete(0, tk.END); entry_fgt.insert(0, str(FGT))
    entry_awe.delete(0, tk.END); entry_awe.insert(0, str(AWE))
    entry_sta.delete(0, tk.END); entry_sta.insert(0, str(STA))
    entry_dex.delete(0, tk.END); entry_dex.insert(0, str(DEX))
    entry_int.delete(0, tk.END); entry_int.insert(0, str(INT))
    entry_pre.delete(0, tk.END); entry_pre.insert(0, str(PRE))
    entry_dodge.delete(0, tk.END); entry_dodge.insert(0, str(Dodge))
    entry_parry.delete(0, tk.END); entry_parry.insert(0, str(Parry))
    entry_fortitude.delete(0, tk.END); entry_fortitude.insert(0, str(Fortitude))
    entry_toughness.delete(0, tk.END); entry_toughness.insert(0, str(Toughness))
    entry_will.delete(0, tk.END); entry_will.insert(0, str(Will))
    refresh_display()

def generate_weapons():
    generate_weapons_advanced()

def update_root():
    global global_root
    if global_root is None:
        return
    try:
        new_str = int(entry_str.get())
        new_agl = int(entry_agl.get())
        new_fgt = int(entry_fgt.get())
        new_awe = int(entry_awe.get())
        new_sta = int(entry_sta.get())
        new_dex = int(entry_dex.get())
        new_int = int(entry_int.get())
        new_pre = int(entry_pre.get())
        new_dodge = int(entry_dodge.get())
        new_parry = int(entry_parry.get())
        new_fortitude = int(entry_fortitude.get())
        new_will = int(entry_will.get())
    except ValueError:
        return
    try:
        new_toughness = int(entry_toughness.get())
    except ValueError:
        new_toughness = 0
    entry_toughness.delete(0, tk.END)
    entry_toughness.insert(0, str(new_toughness))
    global_root['STR'] = new_str
    global_root['AGL'] = new_agl
    global_root['FGT'] = new_fgt
    global_root['AWE'] = new_awe
    global_root['STA'] = new_sta
    global_root['DEX'] = new_dex
    global_root['INT'] = new_int
    global_root['PRE'] = new_pre
    global_root['Dodge'] = new_dodge
    global_root['Parry'] = new_parry
    global_root['Fortitude'] = new_fortitude
    global_root['Toughness'] = new_toughness
    global_root['Will'] = new_will
    refresh_display()

def clear_root():
    global global_root
    global_root = None
    entry_str.delete(0, tk.END)
    entry_agl.delete(0, tk.END)
    entry_fgt.delete(0, tk.END)
    entry_awe.delete(0, tk.END)
    entry_sta.delete(0, tk.END)
    entry_dex.delete(0, tk.END)
    entry_int.delete(0, tk.END)
    entry_pre.delete(0, tk.END)
    entry_dodge.delete(0, tk.END)
    entry_parry.delete(0, tk.END)
    entry_fortitude.delete(0, tk.END)
    entry_toughness.delete(0, tk.END)
    entry_will.delete(0, tk.END)
    refresh_display()

def clear_armor():
    global global_armor
    global_armor = []
    refresh_display()

def clear_weapons():
    global global_weapons
    global_weapons = []
    refresh_display()

def clear_powers():
    global global_powers
    global_powers = []
    refresh_display()

def clear_all():
    global global_root, global_armor, global_weapons, global_powers
    global_root = None
    global_armor = []
    global_weapons = []
    global_powers = []
    refresh_display()

def fill_root_entries(data):
    if not data:
        return
    entry_str.delete(0, tk.END); entry_str.insert(0, str(data['STR']))
    entry_agl.delete(0, tk.END); entry_agl.insert(0, str(data['AGL']))
    entry_fgt.delete(0, tk.END); entry_fgt.insert(0, str(data['FGT']))
    entry_awe.delete(0, tk.END); entry_awe.insert(0, str(data['AWE']))
    entry_sta.delete(0, tk.END); entry_sta.insert(0, str(data['STA']))
    entry_dex.delete(0, tk.END); entry_dex.insert(0, str(data['DEX']))
    entry_int.delete(0, tk.END); entry_int.insert(0, str(data['INT']))
    entry_pre.delete(0, tk.END); entry_pre.insert(0, str(data['PRE']))
    entry_dodge.delete(0, tk.END); entry_dodge.insert(0, str(data['Dodge']))
    entry_parry.delete(0, tk.END); entry_parry.insert(0, str(data['Parry']))
    entry_fortitude.delete(0, tk.END); entry_fortitude.insert(0, str(data['Fortitude']))
    entry_toughness.delete(0, tk.END); entry_toughness.insert(0, str(data['Toughness']))
    entry_will.delete(0, tk.END); entry_will.insert(0, str(data['Will']))

# ==========================
# Preset Saving/Loading Functions
# ==========================
def load_presets():
    global presets
    if os.path.exists(presets_file):
        try:
            with open(presets_file, "r") as f:
                presets = json.load(f)
        except Exception as e:
            print("Error loading presets:", e)
            presets = {"root": {}, "armor": {}, "weapon": {}, "power": {}}
    else:
        presets = {"root": {}, "armor": {}, "weapon": {}, "power": {}}
    update_all_preset_menus()

def save_presets_to_file():
    try:
        with open(presets_file, "w") as f:
            json.dump(presets, f, indent=2)
    except Exception as e:
        print("Error saving presets:", e)

# ==========================
# Keyword Saving/Loading Functions
# ==========================
def load_keywords():
    global keywords
    if os.path.exists(keywords_file):
        try:
            with open(keywords_file, "r") as f:
                keywords = json.load(f)
        except Exception as e:
            print("Error loading keywords:", e)
            keywords = {}
    else:
        keywords = {}
    detect_list_keywords()
    update_keywords_listbox()
    update_keyword_highlights()

def save_keywords_to_file():
    try:
        with open(keywords_file, "w") as f:
            json.dump(keywords, f, indent=2)
    except Exception as e:
        print("Error saving keywords:", e)

# ==========================
# Encounter Saving/Loading Functions
# ==========================
def load_encounters():
    global encounters
    if os.path.exists(encounters_file):
        try:
            with open(encounters_file, "r") as f:
                encounters = json.load(f)
        except Exception as e:
            print("Error loading encounters:", e)
            encounters = {}
    else:
        encounters = {}
    update_encounter_list()

def save_encounters_to_file():
    try:
        with open(encounters_file, "w") as f:
            json.dump(encounters, f, indent=2)
    except Exception as e:
        print("Error saving encounters:", e)

def update_encounter_list():
    if encounter_listbox is not None:
        encounter_listbox.delete(0, tk.END)
        for name in encounters.keys():
            encounter_listbox.insert(tk.END, name)
    update_encounter_char_list()

def update_encounter_char_list(enc_name=None):
    if encounter_char_listbox is None:
        return
    encounter_char_listbox.delete(0, tk.END)
    if enc_name is None:
        if encounter_listbox and encounter_listbox.curselection():
            enc_name = encounter_listbox.get(encounter_listbox.curselection()[0])
        else:
            return
    for c in encounters.get(enc_name, []):
        encounter_char_listbox.insert(tk.END, c)

def on_encounter_select(event=None):
    update_encounter_char_list()

def add_encounter():
    name = simpledialog.askstring("Add Encounter", "Enter encounter name:")
    if not name:
        return
    if name not in encounters:
        encounters[name] = []
        save_encounters_to_file()
        update_encounter_list()

def remove_encounter():
    if not encounter_listbox.curselection():
        return
    name = encounter_listbox.get(encounter_listbox.curselection()[0])
    if name in encounters:
        del encounters[name]
        save_encounters_to_file()
        update_encounter_list()

def add_encounter_character():
    if not encounter_listbox.curselection():
        return
    enc_name = encounter_listbox.get(encounter_listbox.curselection()[0])
    char_name = simpledialog.askstring("Add Character", "Character name:")
    if not char_name or char_name not in characters:
        return
    encounters[enc_name].append(char_name)
    save_encounters_to_file()
    update_encounter_char_list(enc_name)

def remove_encounter_character():
    if not encounter_listbox.curselection() or not encounter_char_listbox.curselection():
        return
    enc_name = encounter_listbox.get(encounter_listbox.curselection()[0])
    char_name = encounter_char_listbox.get(encounter_char_listbox.curselection()[0])
    if char_name in encounters.get(enc_name, []):
        encounters[enc_name].remove(char_name)
        save_encounters_to_file()
        update_encounter_char_list(enc_name)

def generate_encounter_from_group():
    if not encounter_listbox.curselection():
        return
    enc_name = encounter_listbox.get(encounter_listbox.curselection()[0])
    group = simpledialog.askstring("Generate From Group", "Group name:")
    if not group or group not in groups:
        return
    try:
        num = int(simpledialog.askstring("Generate From Group", "Number of enemies:"))
    except (TypeError, ValueError):
        return
    pool = [n for n,d in characters.items() if group in d.get('groups', [])]
    if not pool:
        return
    for _ in range(num):
        encounters[enc_name].append(random.choice(pool))
    save_encounters_to_file()
    update_encounter_char_list(enc_name)

# ==========================
# Tracker Functions
# ==========================
def update_tracker_list():
    if tracker_listbox is not None:
        tracker_listbox.delete(0, tk.END)
        for ent in tracker_entities:
            tracker_listbox.insert(tk.END, ent['name'])
    update_tracker_display()

def update_tracker_display():
    if tracker_display is None:
        return
    tracker_display.delete('1.0', tk.END)
    if not tracker_listbox or not tracker_listbox.curselection():
        return
    idx = tracker_listbox.curselection()[0]
    ent = tracker_entities[idx]
    tracker_display.insert(tk.END, character_to_text(ent))

def on_tracker_select(event=None):
    update_tracker_display()

def add_selected_to_tracker():
    if not characters_listbox.curselection():
        return
    name = get_selected_character_name()
    data = characters.get(name)
    if not data:
        return
    ent_data = create_entity_from_data(name, data)
    tracker_entities.append(ent_data)
    update_tracker_list()

def remove_selected_entity():
    if not tracker_listbox.curselection():
        return
    idx = tracker_listbox.curselection()[0]
    del tracker_entities[idx]
    update_tracker_list()

def load_entity_to_generator():
    if not tracker_listbox.curselection():
        return
    idx = tracker_listbox.curselection()[0]
    ent = tracker_entities[idx]
    global global_root, global_armor, global_weapons, global_powers
    global_root = ent['root']
    fill_root_entries(global_root)
    global_armor = [a.copy() for a in ent.get('armor', [])]
    global_weapons = [w.copy() for w in ent.get('weapons', [])]
    global_powers = [p.copy() for p in ent.get('powers', [])]
    refresh_display()

def update_entity_from_generator():
    if not tracker_listbox.curselection() or global_root is None:
        return
    idx = tracker_listbox.curselection()[0]
    ent = tracker_entities[idx]
    ent['root'] = global_root
    ent['armor'] = list(global_armor)
    ent['weapons'] = list(global_weapons)
    ent['powers'] = list(global_powers)
    update_tracker_display()

def create_entity_from_data(name, data):
    if data.get('template'):
        old_root = global_root
        old_armor = list(global_armor)
        old_weapons = list(global_weapons)
        old_powers = list(global_powers)
        global_root = data['root']
        fill_root_entries(global_root)
        if data.get('armor_preset'):
            armor_preset_var.set(data['armor_preset'])
            load_armor_preset(data['armor_preset'])
        generate_armors_advanced()
        armor = [a.copy() for a in global_armor]
        if data.get('weapon_preset'):
            weapon_preset_var.set(data['weapon_preset'])
            load_weapon_preset(data['weapon_preset'])
        generate_weapons_advanced()
        weapons = [w.copy() for w in global_weapons]
        if data.get('power_preset'):
            power_preset_var.set(data['power_preset'])
            load_power_preset(data['power_preset'])
        generate_powers_advanced()
        powers = [p.copy() for p in global_powers]
        global_root, global_armor, global_weapons, global_powers = (
            old_root, old_armor, old_weapons, old_powers)
        refresh_display()
        return {
            'name': name,
            'root': data['root'],
            'armor': armor,
            'weapons': weapons,
            'powers': powers
        }
    else:
        return {
            'name': name,
            'root': data.get('root'),
            'armor': data.get('armor', []),
            'weapons': data.get('weapons', []),
            'powers': data.get('powers', [])
        }

def update_keywords_listbox():
    global keywords_listbox
    if keywords_listbox is not None:
        keywords_listbox.delete(0, tk.END)
        for k in sorted(keywords.keys()):
            keywords_listbox.insert(tk.END, k)

class KeywordDialog(simpledialog.Dialog):
    def __init__(self, master, title=None, name="", desc=""):
        self.initial_name = name
        self.initial_desc = desc
        super().__init__(master, title=title)

    def body(self, master):
        tk.Label(master, text="Keyword:").grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(master)
        self.entry_name.grid(row=0, column=1, sticky="ew")
        self.entry_name.insert(0, self.initial_name)
        tk.Label(master, text="Description:").grid(row=1, column=0, sticky="nw")
        self.entry_desc = tk.Text(master, width=30, height=4)
        self.entry_desc.grid(row=1, column=1, sticky="ew")
        self.entry_desc.insert("1.0", self.initial_desc)
        return self.entry_name

    def apply(self):
        self.result = (
            self.entry_name.get().strip(),
            self.entry_desc.get("1.0", tk.END).strip(),
        )

def add_keyword():
    global keywords
    dialog = KeywordDialog(root, title="Add Keyword")
    if dialog.result is None:
        return
    name, desc = dialog.result
    if not name:
        return
    keywords[name] = desc
    save_keywords_to_file()
    update_keywords_listbox()
    update_keyword_highlights()

def edit_keyword():
    if keywords_listbox is None or not keywords_listbox.curselection():
        return
    old = keywords_listbox.get(keywords_listbox.curselection()[0])
    dialog = KeywordDialog(root, title="Edit Keyword", name=old, desc=keywords.get(old, ""))
    if dialog.result is None:
        return
    name, desc = dialog.result
    if not name:
        return
    if name != old:
        keywords.pop(old, None)
    keywords[name] = desc
    save_keywords_to_file()
    update_keywords_listbox()
    update_keyword_highlights()

def remove_keyword():
    if keywords_listbox is None or not keywords_listbox.curselection():
        return
    kw = keywords_listbox.get(keywords_listbox.curselection()[0])
    if kw in keywords:
        del keywords[kw]
        save_keywords_to_file()
        update_keywords_listbox()
        update_keyword_highlights()

def on_keyword_select(event=None):
    global keyword_desc_text
    if keywords_listbox is None or keyword_desc_text is None:
        return
    if not keywords_listbox.curselection():
        return
    kw = keywords_listbox.get(keywords_listbox.curselection()[0])
    keyword_desc_text.config(state=tk.NORMAL)
    keyword_desc_text.delete("1.0", tk.END)
    keyword_desc_text.insert(tk.END, keywords.get(kw, ""))
    keyword_desc_text.config(state=tk.DISABLED)

def show_tooltip(event, text):
    global tooltip_window
    if tooltip_window is not None:
        tooltip_window.destroy()
    x = event.x_root + 20
    y = event.y_root + 10
    tooltip_window = tw = tk.Toplevel(output_box)
    tw.wm_overrideredirect(True)
    tw.wm_geometry(f"+{x}+{y}")
    label = tk.Label(tw, text=text, background="yellow", relief="solid", borderwidth=1, wraplength=200)
    label.pack()

def hide_tooltip(event=None):
    global tooltip_window
    if tooltip_window is not None:
        tooltip_window.destroy()
        tooltip_window = None

def update_keyword_highlights():
    for tag in output_box.tag_names():
        if tag.startswith("kw_"):
            output_box.tag_delete(tag)
    for word, desc in keywords.items():
        start = "1.0"
        while True:
            idx = output_box.search(word, start, tk.END)
            if not idx:
                break
            end = f"{idx}+{len(word)}c"
            tag = f"kw_{idx.replace('.', '_')}"
            output_box.tag_add(tag, idx, end)
            output_box.tag_config(tag, underline=True, foreground="blue")
            output_box.tag_bind(tag, "<Enter>", lambda e, d=desc: show_tooltip(e, d))
            output_box.tag_bind(tag, "<Leave>", hide_tooltip)
            start = end

# ==========================
# Character Saving/Loading Functions
# ==========================
def load_characters():
    global characters, groups
    if os.path.exists(characters_file):
        try:
            with open(characters_file, "r") as f:
                data = json.load(f)
            if isinstance(data, dict) and "characters" in data:
                characters = data.get("characters", {})
                groups = data.get("groups", [])
            else:
                characters = data
                groups = []
            # Migrate old single-group characters
            for name, c in characters.items():
                if "group" in c and "groups" not in c:
                    if c["group"] is None:
                        c["groups"] = []
                    else:
                        c["groups"] = [c["group"]]
                    del c["group"]
        except Exception as e:
            print("Error loading characters:", e)
            characters = {}
            groups = []
    else:
        characters = {}
        groups = []
    update_character_list()
    update_group_menus()

def save_characters_to_file():
    try:
        with open(characters_file, "w") as f:
            json.dump({"characters": characters, "groups": groups}, f, indent=2)
    except Exception as e:
        print("Error saving characters:", e)

def save_character():
    global save_group_listbox
    if global_root is None:
        return
    entry = simpledialog.askstring(
        "Save Character",
        "Enter name and tags separated by ';' (e.g. Bob; hero, villain):",
    )
    if not entry:
        return
    if ';' in entry:
        name_part, tag_part = entry.split(';', 1)
    else:
        name_part, tag_part = entry, ""
    name = name_part.strip()
    tag_str = tag_part.strip()
    tags = [t.strip() for t in tag_str.split(',') if t.strip()]
    selected_idx = save_group_listbox.curselection()
    selected_groups = [save_group_listbox.get(i) for i in selected_idx]
    characters[name] = {
        "tags": tags,
        "groups": selected_groups,
        "root": global_root,
        "armor": global_armor,
        "weapons": global_weapons,
        "powers": global_powers
    }
    save_characters_to_file()
    update_character_list()

def save_template():
    global save_group_listbox
    if global_root is None:
        return
    entry = simpledialog.askstring(
        "Save Template",
        "Enter name and tags separated by ';' (e.g. Bob; hero, villain):",
    )
    if not entry:
        return
    if ';' in entry:
        name_part, tag_part = entry.split(';', 1)
    else:
        name_part, tag_part = entry, ""
    name = name_part.strip()
    tag_str = tag_part.strip()
    tags = [t.strip() for t in tag_str.split(',') if t.strip()]
    selected_idx = save_group_listbox.curselection()
    selected_groups = [save_group_listbox.get(i) for i in selected_idx]
    characters[name] = {
        "tags": tags,
        "groups": selected_groups,
        "root": global_root,
        "template": True,
        "armor_preset": armor_preset_var.get(),
        "weapon_preset": weapon_preset_var.get(),
        "power_preset": power_preset_var.get()
    }
    save_characters_to_file()
    update_character_list()

def delete_character():
    if not characters_listbox.curselection():
        return
    name = get_selected_character_name()
    if name in characters:
        del characters[name]
        save_characters_to_file()
        update_character_list()
        character_display.delete("1.0", tk.END)

def edit_character():
    if not characters_listbox.curselection():
        return
    name = get_selected_character_name()
    data = characters.get(name)
    if not data:
        return
    global global_root, global_armor, global_weapons, global_powers
    global_root = data.get("root")
    if global_root:
        fill_root_entries(global_root)
    else:
        clear_root()
    if data.get("template"):
        armor_preset_var.set(data.get("armor_preset", ""))
        weapon_preset_var.set(data.get("weapon_preset", ""))
        power_preset_var.set(data.get("power_preset", ""))
        global_armor = []
        global_weapons = []
        global_powers = []
    else:
        global_armor = data.get("armor", [])
        global_weapons = data.get("weapons", [])
        global_powers = data.get("powers", [])
    if save_group_listbox is not None:
        save_group_listbox.selection_clear(0, tk.END)
        for i in range(save_group_listbox.size()):
            item = save_group_listbox.get(i)
            if item in data.get("groups", []):
                save_group_listbox.selection_set(i)
    refresh_display()

def character_to_text(data):
    lines = []
    groups_list = data.get("groups", [])
    if groups_list:
        lines.append(f"Groups: {', '.join(groups_list)}")
    root_stats = data.get("root")
    if root_stats:
        line1 = (
            f"STR:{root_stats['STR']} AGL:{root_stats['AGL']} "
            f"FGT:{root_stats['FGT']} AWE:{root_stats['AWE']} "
            f"STA:{root_stats['STA']} DEX:{root_stats['DEX']} "
            f"INT:{root_stats['INT']} PRE:{root_stats['PRE']}"
        )
        line2 = (
            f"Dodge:{root_stats['Dodge']} Parry:{root_stats['Parry']} "
            f"Fortitude:{root_stats['Fortitude']} Toughness:{root_stats['Toughness']} "
            f"Will:{root_stats['Will']}"
        )
        lines.extend([line1, line2])
    armor_list = data.get("armor", [])
    if armor_list:
        armor_lines = [f"- {a['name']} (+{a['bonus']}) [{', '.join(a['tags'])}]" for a in armor_list]
        lines.append("Armor:\n" + "\n".join(armor_lines))
    else:
        lines.append("Armor:\nNone")
    weapon_list = data.get("weapons", [])
    if weapon_list:
        weapon_lines = [f"- {w['name']} (Damage: {w['damage']})" for w in weapon_list]
        lines.append("Weapons:\n" + "\n".join(weapon_lines))
    else:
        lines.append("Weapons:\nNone")
    power_list_data = data.get("powers", [])
    if power_list_data:
        power_lines = [f"{p['rank']} #{p['frequency']} {p['name']}" for p in power_list_data]
        lines.append("Powers:\n" + "\n".join(power_lines))
    else:
        lines.append("Powers:\nNone")
    return "\n".join(lines)

def on_character_select(event=None):
    if not characters_listbox.curselection():
        return
    name = get_selected_character_name()
    data = characters.get(name)
    if not data:
        return
    character_display.delete("1.0", tk.END)
    if data.get('template'):
        generated = create_entity_from_data(name, data)
        character_display.insert(tk.END, character_to_text(generated))
    else:
        character_display.insert(tk.END, character_to_text(data))

def update_character_list(filter_text=""):
    global filter_group_var
    characters_listbox.delete(0, tk.END)
    ft = filter_text.lower()
    group_filter = filter_group_var.get()
    for name, data in characters.items():
        tags = ' '.join(data.get('tags', []))
        groups_list = data.get('groups', [])
        if group_filter != "All" and group_filter not in groups_list:
            continue
        if ft:
            if ft in name.lower() or ft in tags.lower():
                display = name + (" (G)" if data.get('template') else "")
                characters_listbox.insert(tk.END, display)
        else:
            display = name + (" (G)" if data.get('template') else "")
            characters_listbox.insert(tk.END, display)

def get_selected_character_name():
    if not characters_listbox.curselection():
        return None
    disp = characters_listbox.get(characters_listbox.curselection()[0])
    if disp.endswith(" (G)"):
        return disp[:-4]
    return disp

def save_root_preset():
    global presets
    preset_name = simpledialog.askstring("Save Root Preset", "Enter preset name:")
    if not preset_name:
        return
    presets["root"][preset_name] = {
        "STR": entry_str.get(),
        "AGL": entry_agl.get(),
        "FGT": entry_fgt.get(),
        "AWE": entry_awe.get(),
        "STA": entry_sta.get(),
        "DEX": entry_dex.get(),
        "INT": entry_int.get(),
        "PRE": entry_pre.get(),
        "Dodge": entry_dodge.get(),
        "Parry": entry_parry.get(),
        "Fortitude": entry_fortitude.get(),
        "Toughness": entry_toughness.get(),
        "Will": entry_will.get()
    }
    save_presets_to_file()
    update_preset_menu("root")

def load_root_preset(preset_name):
    if preset_name in presets["root"]:
        data = presets["root"][preset_name]
        entry_str.delete(0, tk.END); entry_str.insert(0, data["STR"])
        entry_agl.delete(0, tk.END); entry_agl.insert(0, data["AGL"])
        entry_fgt.delete(0, tk.END); entry_fgt.insert(0, data["FGT"])
        entry_awe.delete(0, tk.END); entry_awe.insert(0, data["AWE"])
        entry_sta.delete(0, tk.END); entry_sta.insert(0, data["STA"])
        entry_dex.delete(0, tk.END); entry_dex.insert(0, data["DEX"])
        entry_int.delete(0, tk.END); entry_int.insert(0, data["INT"])
        entry_pre.delete(0, tk.END); entry_pre.insert(0, data["PRE"])
        entry_dodge.delete(0, tk.END); entry_dodge.insert(0, data.get("Dodge", ""))
        entry_parry.delete(0, tk.END); entry_parry.insert(0, data.get("Parry", ""))
        entry_fortitude.delete(0, tk.END); entry_fortitude.insert(0, data.get("Fortitude", ""))
        entry_toughness.delete(0, tk.END); entry_toughness.insert(0, data.get("Toughness", ""))
        entry_will.delete(0, tk.END); entry_will.insert(0, data.get("Will", ""))

def save_armor_preset():
    global presets
    preset_name = simpledialog.askstring("Save Armor Preset", "Enter preset name:")
    if not preset_name:
        return
    presets["armor"][preset_name] = {
        "number": entry_armor_num.get(),
        "tags": entry_armor_tag.get()
    }
    save_presets_to_file()
    update_preset_menu("armor")

def load_armor_preset(preset_name):
    if preset_name in presets["armor"]:
        data = presets["armor"][preset_name]
        entry_armor_num.delete(0, tk.END); entry_armor_num.insert(0, data["number"])
        entry_armor_tag.delete(0, tk.END); entry_armor_tag.insert(0, data["tags"])

def save_weapon_preset():
    global presets
    preset_name = simpledialog.askstring("Save Weapon Preset", "Enter preset name:")
    if not preset_name:
        return
    presets["weapon"][preset_name] = {
        "number": entry_weapon_num.get(),
        "tags": entry_weapon_tag.get()
    }
    save_presets_to_file()
    update_preset_menu("weapon")

def load_weapon_preset(preset_name):
    if preset_name in presets["weapon"]:
        data = presets["weapon"][preset_name]
        entry_weapon_num.delete(0, tk.END); entry_weapon_num.insert(0, data["number"])
        entry_weapon_tag.delete(0, tk.END); entry_weapon_tag.insert(0, data["tags"])

def save_power_preset():
    global presets
    preset_name = simpledialog.askstring("Save Power Preset", "Enter preset name:")
    if not preset_name:
        return
    presets["power"][preset_name] = {
        "base": entry_power_base.get(),
        "extra": entry_power_extra.get(),
        "extra_ranks": entry_power_ranks.get()
    }
    save_presets_to_file()
    update_preset_menu("power")

def load_power_preset(preset_name):
    if preset_name in presets["power"]:
        data = presets["power"][preset_name]
        entry_power_base.delete(0, tk.END); entry_power_base.insert(0, data["base"])
        entry_power_extra.delete(0, tk.END); entry_power_extra.insert(0, data["extra"])
        entry_power_ranks.delete(0, tk.END); entry_power_ranks.insert(0, data["extra_ranks"])

# OptionMenus for presets; these will be created after the root window exists.
# We define update functions for each panel.
def update_preset_menu(panel):
    if panel == "root":
        menu = root_preset_menu["menu"]
        menu.delete(0, "end")
        for name in presets["root"]:
            menu.add_command(label=name, command=lambda value=name: (root_preset_var.set(value), load_root_preset(value)))
    elif panel == "armor":
        menu = armor_preset_menu["menu"]
        menu.delete(0, "end")
        for name in presets["armor"]:
            menu.add_command(label=name, command=lambda value=name: (armor_preset_var.set(value), load_armor_preset(value)))
    elif panel == "weapon":
        menu = weapon_preset_menu["menu"]
        menu.delete(0, "end")
        for name in presets["weapon"]:
            menu.add_command(label=name, command=lambda value=name: (weapon_preset_var.set(value), load_weapon_preset(value)))
    elif panel == "power":
        menu = power_preset_menu["menu"]
        menu.delete(0, "end")
        for name in presets["power"]:
            menu.add_command(label=name, command=lambda value=name: (power_preset_var.set(value), load_power_preset(value)))

def update_all_preset_menus():
    update_preset_menu("root")
    update_preset_menu("armor")
    update_preset_menu("weapon")
    update_preset_menu("power")

def update_group_menus():
    global save_group_listbox, filter_group_var, filter_group_menu
    if save_group_listbox is not None:
        save_group_listbox.delete(0, tk.END)
        for g in groups:
            save_group_listbox.insert(tk.END, g)
    if filter_group_menu is not None:
        menu = filter_group_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="All", command=lambda v="All": filter_group_var.set(v))
        for g in groups:
            menu.add_command(label=g, command=lambda value=g: filter_group_var.set(value))
    update_character_list()

def add_group():
    global groups
    name = simpledialog.askstring("Add Group", "Enter group name:")
    if not name:
        return
    if name not in groups:
        groups.append(name)
        save_characters_to_file()
        update_group_menus()

def edit_group():
    if not groups:
        return
    name = simpledialog.askstring("Edit Group", "Group to edit:")
    if not name or name not in groups:
        return
    new_name = simpledialog.askstring("Edit Group", "New name:", initialvalue=name)
    if not new_name or new_name == name:
        return
    if new_name in groups:
        return
    idx = groups.index(name)
    groups[idx] = new_name
    for c in characters.values():
        if name in c.get("groups", []):
            c["groups"] = [new_name if g == name else g for g in c["groups"]]
    save_characters_to_file()
    update_group_menus()

def remove_group():
    if not groups:
        return
    name = simpledialog.askstring("Remove Group", "Group to remove:")
    if not name or name not in groups:
        return
    groups.remove(name)
    for c in characters.values():
        if name in c.get("groups", []):
            c["groups"] = [g for g in c["groups"] if g != name]
    save_characters_to_file()
    update_group_menus()

# Load presets from file.
def load_presets():
    global presets
    if os.path.exists(presets_file):
        try:
            with open(presets_file, "r") as f:
                presets = json.load(f)
        except Exception as e:
            print("Error loading presets:", e)
            presets = {"root": {}, "armor": {}, "weapon": {}, "power": {}}
    else:
        presets = {"root": {}, "armor": {}, "weapon": {}, "power": {}}
    update_all_preset_menus()

def save_presets_to_file():
    try:
        with open(presets_file, "w") as f:
            json.dump(presets, f, indent=2)
    except Exception as e:
        print("Error saving presets:", e)

# ==========================
# Main GUI Setup (Reordered Layout)
# ==========================
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Character Generator")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    generator_tab = ttk.Frame(notebook)
    characters_tab = ttk.Frame(notebook)
    encounters_tab = ttk.Frame(notebook)
    tracker_tab = ttk.Frame(notebook)
    keywords_tab = ttk.Frame(notebook)
    notebook.add(generator_tab, text="Generator")
    notebook.add(characters_tab, text="Characters")
    notebook.add(encounters_tab, text="Encounters")
    notebook.add(tracker_tab, text="Tracker")
    notebook.add(keywords_tab, text="Keywords")

    root_preset_var = tk.StringVar(root)
    armor_preset_var = tk.StringVar(root)
    weapon_preset_var = tk.StringVar(root)
    power_preset_var = tk.StringVar(root)

    main_frame = tk.Frame(generator_tab)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Right Frame: Output box and Clear All button
    output_frame = tk.Frame(main_frame)
    output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    output_box = tk.Text(output_frame, width=80, height=25)
    output_box.pack(padx=5, pady=5)
    btn_clear_all = tk.Button(output_frame, text="Clear All", command=clear_all)
    btn_clear_all.pack(pady=5)

    save_frame = tk.Frame(output_frame)
    save_frame.pack(pady=5)
    tk.Label(save_frame, text="Groups:").pack(side=tk.LEFT)
    save_group_listbox = tk.Listbox(save_frame, selectmode=tk.MULTIPLE, height=4, exportselection=False)
    save_group_listbox.pack(side=tk.LEFT, padx=5)
    btn_add_group_gen = tk.Button(save_frame, text="Add Group", command=add_group)
    btn_add_group_gen.pack(side=tk.LEFT, padx=5)
    btn_edit_group_gen = tk.Button(save_frame, text="Edit Group", command=edit_group)
    btn_edit_group_gen.pack(side=tk.LEFT, padx=5)
    btn_remove_group_gen = tk.Button(save_frame, text="Remove Group", command=remove_group)
    btn_remove_group_gen.pack(side=tk.LEFT, padx=5)
    btn_save_char_gen = tk.Button(save_frame, text="Save Character", command=save_character)
    btn_save_char_gen.pack(side=tk.LEFT, padx=5)
    btn_save_template = tk.Button(save_frame, text="Save Template", command=save_template)
    btn_save_template.pack(side=tk.LEFT, padx=5)

    # Left Frame: Controls (stacked vertically)
    control_frame = tk.Frame(main_frame)
    control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

    # --- Root Editor Subframe ---
    root_editor_frame = tk.LabelFrame(control_frame, text="Root Editor")
    root_editor_frame.pack(fill=tk.X, padx=5, pady=5)
    tk.Label(root_editor_frame, text="STR:").grid(row=0, column=0)
    entry_str = tk.Entry(root_editor_frame, width=3)
    entry_str.grid(row=0, column=1)
    tk.Label(root_editor_frame, text="AGL:").grid(row=0, column=2)
    entry_agl = tk.Entry(root_editor_frame, width=3)
    entry_agl.grid(row=0, column=3)
    tk.Label(root_editor_frame, text="FGT:").grid(row=0, column=4)
    entry_fgt = tk.Entry(root_editor_frame, width=3)
    entry_fgt.grid(row=0, column=5)
    tk.Label(root_editor_frame, text="AWE:").grid(row=0, column=6)
    entry_awe = tk.Entry(root_editor_frame, width=3)
    entry_awe.grid(row=0, column=7)
    tk.Label(root_editor_frame, text="STA:").grid(row=1, column=0)
    entry_sta = tk.Entry(root_editor_frame, width=3)
    entry_sta.grid(row=1, column=1)
    tk.Label(root_editor_frame, text="DEX:").grid(row=1, column=2)
    entry_dex = tk.Entry(root_editor_frame, width=3)
    entry_dex.grid(row=1, column=3)
    tk.Label(root_editor_frame, text="INT:").grid(row=1, column=4)
    entry_int = tk.Entry(root_editor_frame, width=3)
    entry_int.grid(row=1, column=5)
    tk.Label(root_editor_frame, text="PRE:").grid(row=1, column=6)
    entry_pre = tk.Entry(root_editor_frame, width=3)
    entry_pre.grid(row=1, column=7)

    tk.Label(root_editor_frame, text="Dodge:").grid(row=2, column=0)
    entry_dodge = tk.Entry(root_editor_frame, width=3)
    entry_dodge.grid(row=2, column=1)
    tk.Label(root_editor_frame, text="Parry:").grid(row=2, column=2)
    entry_parry = tk.Entry(root_editor_frame, width=3)
    entry_parry.grid(row=2, column=3)
    tk.Label(root_editor_frame, text="Fortitude:").grid(row=2, column=4)
    entry_fortitude = tk.Entry(root_editor_frame, width=3)
    entry_fortitude.grid(row=2, column=5)
    tk.Label(root_editor_frame, text="Toughness:").grid(row=2, column=6)
    entry_toughness = tk.Entry(root_editor_frame, width=3)
    entry_toughness.grid(row=2, column=7)
    tk.Label(root_editor_frame, text="Will:").grid(row=3, column=0)
    entry_will = tk.Entry(root_editor_frame, width=3)
    entry_will.grid(row=3, column=1)

    btn_generate_root = tk.Button(root_editor_frame, text="Generate Root", command=generate_root)
    btn_generate_root.grid(row=4, column=0, columnspan=4, pady=5)
    btn_update_root = tk.Button(root_editor_frame, text="Update Root Attributes", command=update_root)
    btn_update_root.grid(row=4, column=4, columnspan=4, pady=5)
    btn_clear_root = tk.Button(root_editor_frame, text="Clear Root", command=clear_root)
    btn_clear_root.grid(row=5, column=0, columnspan=8, pady=5)
    tk.Label(root_editor_frame, text="Save Preset:").grid(row=6, column=0, columnspan=2)
    btn_save_root = tk.Button(root_editor_frame, text="Save", command=save_root_preset)
    btn_save_root.grid(row=6, column=2, columnspan=2)
    root_preset_menu = tk.OptionMenu(root_editor_frame, root_preset_var, "")
    root_preset_menu.grid(row=6, column=4, columnspan=4)

    # --- Armor Generation Controls Subframe ---
    armor_gen_frame = tk.LabelFrame(control_frame, text="Armor Generation Controls")
    armor_gen_frame.pack(fill=tk.X, padx=5, pady=5)
    tk.Label(armor_gen_frame, text="Number of Armors:").grid(row=0, column=0)
    entry_armor_num = tk.Entry(armor_gen_frame, width=3)
    entry_armor_num.grid(row=0, column=1)
    tk.Label(armor_gen_frame, text="Specific Tags (comma delimited):").grid(row=0, column=2)
    entry_armor_tag = tk.Entry(armor_gen_frame, width=15)
    entry_armor_tag.grid(row=0, column=3)
    btn_generate_armors = tk.Button(armor_gen_frame, text="Generate Armors", command=generate_armors_advanced)
    btn_generate_armors.grid(row=0, column=4, padx=5)
    btn_clear_armor = tk.Button(armor_gen_frame, text="Clear Armors", command=clear_armor)
    btn_clear_armor.grid(row=1, column=0, columnspan=5, pady=5)
    tk.Label(armor_gen_frame, text="Save Preset:").grid(row=2, column=0, columnspan=2)
    btn_save_armor = tk.Button(armor_gen_frame, text="Save", command=save_armor_preset)
    btn_save_armor.grid(row=2, column=2, columnspan=2)
    armor_preset_menu = tk.OptionMenu(armor_gen_frame, armor_preset_var, "")
    armor_preset_menu.grid(row=2, column=4, columnspan=2)

    # --- Weapon Generation Controls Subframe ---
    weapon_gen_frame = tk.LabelFrame(control_frame, text="Weapon Generation Controls")
    weapon_gen_frame.pack(fill=tk.X, padx=5, pady=5)
    tk.Label(weapon_gen_frame, text="Number of Weapons:").grid(row=0, column=0)
    entry_weapon_num = tk.Entry(weapon_gen_frame, width=3)
    entry_weapon_num.grid(row=0, column=1)
    tk.Label(weapon_gen_frame, text="Specific Tags (comma delimited):").grid(row=0, column=2)
    entry_weapon_tag = tk.Entry(weapon_gen_frame, width=15)
    entry_weapon_tag.grid(row=0, column=3)
    btn_generate_weapons = tk.Button(weapon_gen_frame, text="Generate Weapons", command=generate_weapons_advanced)
    btn_generate_weapons.grid(row=0, column=4, padx=5)
    btn_clear_weapons = tk.Button(weapon_gen_frame, text="Clear Weapons", command=clear_weapons)
    btn_clear_weapons.grid(row=1, column=0, columnspan=5, pady=5)
    tk.Label(weapon_gen_frame, text="Save Preset:").grid(row=2, column=0, columnspan=2)
    btn_save_weapon = tk.Button(weapon_gen_frame, text="Save", command=save_weapon_preset)
    btn_save_weapon.grid(row=2, column=2, columnspan=2)
    weapon_preset_menu = tk.OptionMenu(weapon_gen_frame, weapon_preset_var, "")
    weapon_preset_menu.grid(row=2, column=4, columnspan=2)

    # --- Power Generation Controls Subframe ---
    power_gen_frame = tk.LabelFrame(control_frame, text="Power Generation Controls")
    power_gen_frame.pack(fill=tk.X, padx=5, pady=5)
    tk.Label(power_gen_frame, text="Base Powers:").grid(row=0, column=0)
    entry_power_base = tk.Entry(power_gen_frame, width=3)
    entry_power_base.grid(row=0, column=1)
    tk.Label(power_gen_frame, text="Extra Chance %:").grid(row=0, column=2)
    entry_power_extra = tk.Entry(power_gen_frame, width=3)
    entry_power_extra.grid(row=0, column=3)
    tk.Label(power_gen_frame, text="Extra Ranks %:").grid(row=0, column=4)
    entry_power_ranks = tk.Entry(power_gen_frame, width=3)
    entry_power_ranks.grid(row=0, column=5)
    btn_generate_powers = tk.Button(power_gen_frame, text="Generate Powers", command=generate_powers_advanced)
    btn_generate_powers.grid(row=0, column=6, padx=5)
    btn_clear_powers = tk.Button(power_gen_frame, text="Clear Powers", command=clear_powers)
    btn_clear_powers.grid(row=1, column=0, columnspan=7, pady=5)
    tk.Label(power_gen_frame, text="Save Preset:").grid(row=2, column=0, columnspan=2)
    btn_save_power = tk.Button(power_gen_frame, text="Save", command=save_power_preset)
    btn_save_power.grid(row=2, column=2, columnspan=2)
    power_preset_menu = tk.OptionMenu(power_gen_frame, power_preset_var, "")
    power_preset_menu.grid(row=2, column=4, columnspan=2)

    # --- Characters Tab ---
    search_var = tk.StringVar()
    search_entry = tk.Entry(characters_tab, textvariable=search_var)
    search_entry.pack(fill=tk.X, padx=5, pady=5)
    search_entry.bind("<KeyRelease>", lambda e: update_character_list(search_var.get()))

    characters_listbox = tk.Listbox(characters_tab)
    characters_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    characters_listbox.bind("<<ListboxSelect>>", on_character_select)

    character_display = tk.Text(characters_tab, height=15)
    character_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    group_frame = tk.Frame(characters_tab)
    group_frame.pack(fill=tk.X, padx=5)
    tk.Label(group_frame, text="Group:").pack(side=tk.LEFT)
    filter_group_var = tk.StringVar(value="All")
    filter_group_menu = tk.OptionMenu(group_frame, filter_group_var, "All")
    filter_group_menu.pack(side=tk.LEFT, padx=5)
    filter_group_var.trace_add("write", lambda *args: update_character_list(search_var.get()))
    btn_add_group_char = tk.Button(group_frame, text="Add Group", command=add_group)
    btn_add_group_char.pack(side=tk.LEFT, padx=5)
    btn_edit_group_char = tk.Button(group_frame, text="Edit Group", command=edit_group)
    btn_edit_group_char.pack(side=tk.LEFT, padx=5)
    btn_remove_group_char = tk.Button(group_frame, text="Remove Group", command=remove_group)
    btn_remove_group_char.pack(side=tk.LEFT, padx=5)

    char_btn_frame = tk.Frame(characters_tab)
    char_btn_frame.pack(pady=5)
    btn_delete_char = tk.Button(char_btn_frame, text="Delete Selected", command=delete_character)
    btn_delete_char.pack(side=tk.LEFT, padx=5)
    btn_track_char = tk.Button(char_btn_frame, text="Add To Tracker", command=add_selected_to_tracker)
    btn_track_char.pack(side=tk.LEFT, padx=5)

    # --- Keywords Tab ---
    keywords_listbox = tk.Listbox(keywords_tab)
    keywords_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    keywords_listbox.bind("<<ListboxSelect>>", on_keyword_select)

    keyword_desc_text = tk.Text(keywords_tab, height=5, wrap=tk.WORD, state=tk.DISABLED)
    keyword_desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    kw_btn_frame = tk.Frame(keywords_tab)
    kw_btn_frame.pack(pady=5)
    btn_add_keyword = tk.Button(kw_btn_frame, text="Add Keyword", command=add_keyword)
    btn_add_keyword.pack(side=tk.LEFT, padx=5)
    btn_edit_keyword = tk.Button(kw_btn_frame, text="Edit Keyword", command=edit_keyword)
    btn_edit_keyword.pack(side=tk.LEFT, padx=5)
    btn_remove_keyword = tk.Button(kw_btn_frame, text="Remove Keyword", command=remove_keyword)
    btn_remove_keyword.pack(side=tk.LEFT, padx=5)

    # --- Encounters Tab ---
    encounter_listbox = tk.Listbox(encounters_tab)
    encounter_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    encounter_listbox.bind("<<ListboxSelect>>", on_encounter_select)

    encounter_char_listbox = tk.Listbox(encounters_tab)
    encounter_char_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    enc_btn_frame = tk.Frame(encounters_tab)
    enc_btn_frame.pack(side=tk.RIGHT, fill=tk.Y)
    btn_add_enc = tk.Button(enc_btn_frame, text="Add Encounter", command=add_encounter)
    btn_add_enc.pack(fill=tk.X, padx=5, pady=2)
    btn_remove_enc = tk.Button(enc_btn_frame, text="Remove Encounter", command=remove_encounter)
    btn_remove_enc.pack(fill=tk.X, padx=5, pady=2)
    btn_add_enc_char = tk.Button(enc_btn_frame, text="Add Char", command=add_encounter_character)
    btn_add_enc_char.pack(fill=tk.X, padx=5, pady=2)
    btn_remove_enc_char = tk.Button(enc_btn_frame, text="Remove Char", command=remove_encounter_character)
    btn_remove_enc_char.pack(fill=tk.X, padx=5, pady=2)
    btn_gen_enc = tk.Button(enc_btn_frame, text="Generate From Group", command=generate_encounter_from_group)
    btn_gen_enc.pack(fill=tk.X, padx=5, pady=2)

    # --- Tracker Tab ---
    tracker_listbox = tk.Listbox(tracker_tab)
    tracker_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    tracker_listbox.bind("<<ListboxSelect>>", on_tracker_select)

    tracker_display = tk.Text(tracker_tab, height=15)
    tracker_display.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    tracker_btn_frame = tk.Frame(tracker_tab)
    tracker_btn_frame.pack(side=tk.RIGHT, fill=tk.Y)
    btn_remove_entity = tk.Button(tracker_btn_frame, text="Remove", command=remove_selected_entity)
    btn_remove_entity.pack(fill=tk.X, padx=5, pady=2)
    btn_load_entity = tk.Button(tracker_btn_frame, text="Load To Generator", command=load_entity_to_generator)
    btn_load_entity.pack(fill=tk.X, padx=5, pady=2)
    btn_update_entity = tk.Button(tracker_btn_frame, text="Update From Generator", command=update_entity_from_generator)
    btn_update_entity.pack(fill=tk.X, padx=5, pady=2)

    # Context menu for character list
    char_menu = tk.Menu(characters_tab, tearoff=0)
    char_menu.add_command(label="Edit", command=edit_character)
    char_menu.add_command(label="Delete", command=delete_character)

    def show_char_menu(event):
        if characters_listbox.size() == 0:
            return
        index = characters_listbox.nearest(event.y)
        if index >= 0:
            characters_listbox.selection_clear(0, tk.END)
            characters_listbox.selection_set(index)
            char_menu.tk_popup(event.x_root, event.y_root)
    characters_listbox.bind("<Button-3>", show_char_menu)

    load_presets()
    load_armor_data()
    load_weapon_data()
    load_characters()
    load_keywords()
    load_encounters()
    update_encounter_list()
    update_tracker_list()
    update_all_preset_menus()
    root.mainloop()
