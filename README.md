# GO-Charactergen
A program for creating quick, simple characters in mutants and masterminds and tracking them.

Default keyword definitions are stored in `default_keywords.json` and copied to the
user directory on first run.
Duplicate keyword entries from earlier versions have been removed.

Keywords now support variable levels.  When a keyword is marked as variable it
will be displayed in the format `Keyword(X)` in the keyword list.  Use the `{#}`
placeholder inside a keyword's description to insert the numeric level when the
tooltip is shown.  Keywords may also modify base stats by including placeholders
like `{STR(+2)}` or `{INT(-4)}` in their descriptions.  The modifier is applied
when any item bearing the keyword is equipped.

## Weapons

The default weapon list provides each weapon's bonus value and associated tags.

- Club: 2 (Medieval, Melee)
- Dagger: 3 (Medieval, Melee, Thrown, Finesse, Stealth)
- Shortsword: 5 (Medieval, Melee, Finesse, Riposte)
- Longsword: 7 (Medieval, Melee)
- Rapier: 4 (Medieval, Melee, Finesse, Improved Crit(2), Riposte, Stealth)
- Mace: 6 (Medieval, Melee, Crushing(2))
- Warhammer: 8 (Medieval, Melee, Crushing(4), Heavy)
- Battle Axe: 7 (Medieval, Melee, Cleaving, Heavy)
- Greatsword: 10 (Medieval, Melee, 2-Hand, Cleaving, Heavy, Improved Crit(1))
- Spear: 4 (Medieval, Melee, Thrown, Reach(5))
- Halberd: 9 (Medieval, Melee, 2-Hand, Reach(10), Cleaving)
- Pike: 8 (Medieval, Melee, 2-Hand, Reach(15))
- Scimitar: 6 (Medieval, Melee, Finesse, Riposte)
- Falchion: 7 (Medieval, Melee, Cleaving)
- Throwing Axe: 3 (Medieval, Thrown, Finesse)
- Hand Axe: 4 (Medieval, Thrown, Finesse)
- Short Bow: 4 (Medieval, Ranged, 2-Hand, Ammunition)
- Long Bow: 7 (Medieval, Ranged, 2-Hand, Ammunition)
- Crossbow: 8 (Medieval, Ranged, 2-Hand, Ammunition, Reload)
- Hand Crossbow: 4 (Medieval, Ranged, Ammunition, Reload, Stealth)
- Sling: 2 (Medieval, Ranged, Ammunition, Thrown)
- Javelin: 3 (Medieval, Thrown)
- Lance: 9 (Medieval, Melee, 2-Hand, Reach(10), Heavy)
- Bardiche: 9 (Medieval, Melee, 2-Hand, Cleaving, Heavy)
- Glaive: 8 (Medieval, Melee, 2-Hand, Reach(10), Cleaving)
- Quarterstaff: 2 (Medieval, Melee, Defensive)
- Morning Star: 7 (Medieval, Melee, Brutal, Crushing(3))
- Flail: 6 (Medieval, Melee, Unwieldy, Crushing(2))
- War Scythe: 8 (Medieval, Melee, 2-Hand, Cleaving, Unwieldy)
- Net: 1 (Medieval, Ranged, Thrown, Entangling)
- Bolas: 2 (Medieval, Thrown, Entangling)
- Hooked Mace: 5 (Medieval, Melee, Hooking, Crushing(2))
- Dirk: 3 (Medieval, Melee, Finesse, Stealth)
- Estoc: 6 (Medieval, Melee, Piercing(2), Finesse)
- Sickle: 4 (Medieval, Melee, Finesse)
- Maul: 12 (Medieval, Melee, 2-Hand, Crushing(6), Heavy)
- Giant's Club: 15 (Medieval, Melee, 2-Hand, Crushing(8), Heavy, Unwieldy)
- Spiked Gauntlet: 4 (Medieval, Melee, Finesse, Piercing(1))
- Repeating Crossbow: 9 (Medieval, Ranged, 2-Hand, Ammunition, Reload)
- Heavy Lance: 11 (Medieval, Melee, 2-Hand, Reach(15), Heavy)
- Spiked Club: 5 (Medieval, Melee, Crushing(3), Piercing(1))
- Executioner's Axe: 16 (Medieval, Melee, 2-Hand, Cleaving, Heavy, Brutal)
- Colossal Warhammer: 18 (Medieval, Melee, 2-Hand, Crushing(8), Heavy, Brutal)
- Great Cleaver: 17 (Medieval, Melee, 2-Hand, Cleaving, Brutal)
- Pistol: 6 (Modern, Ranged, Ammunition, Reload)
- Revolver: 7 (Modern, Ranged, Ammunition, Reload)
- Shotgun: 9 (Modern, Ranged, Ammunition, Reload, Heavy)
- Assault Rifle: 8 (Modern, Ranged, Ammunition, Reload, Multiattack(3))
- Sniper Rifle: 12 (Modern, Ranged, Ammunition, Reload, Piercing(3), Heavy)
- Submachine Gun: 7 (Modern, Ranged, Ammunition, Reload, Multiattack(4))
- Machine Gun: 10 (Modern, Ranged, Ammunition, Reload, Heavy, Multiattack(5))
- Grenade Launcher: 11 (Modern, Ranged, Ammunition, Thrown, Reload, Heavy)
- Flamethrower: 10 (Modern, Ranged, Ammunition, Reload, Heavy)
- Rocket Launcher: 15 (Modern, Ranged, Ammunition, Reload, Heavy)
- Taser: 2 (Modern, Ranged)
- Bayonet: 4 (Modern, Melee, Finesse, Piercing(1))
- Combat Knife: 5 (Modern, Melee, Finesse, Stealth, Thrown)
- Plasma Rifle: 10 (Postmodern, Ranged, Ammunition, Reload, Heavy)
- Laser Pistol: 7 (Postmodern, Ranged, Ammunition, Reload, Stealth)
- Gauss Rifle: 12 (Postmodern, Ranged, Ammunition, Reload, Piercing(4))
- Energy Sword: 9 (Postmodern, Melee, Finesse, Riposte)
- Particle Cannon: 15 (Postmodern, Ranged, Ammunition, Reload, Heavy, Brutal)
- Railgun: 14 (Postmodern, Ranged, Ammunition, Reload, Piercing(4), Heavy)
- Nano Blade: 8 (Postmodern, Melee, Finesse, Stealth)
- Photon Blaster: 9 (Postmodern, Ranged, Ammunition, Reload)
- Ionizer: 7 (Postmodern, Ranged, Ammunition, Reload)
- Gravity Hammer: 16 (Postmodern, Melee, 2-Hand, Crushing(8), Heavy, Brutal)
- Sonic Disruptor: 10 (Postmodern, Ranged, Ammunition, Reload)
- Neutrino Beam: 18 (Postmodern, Ranged, Ammunition, Reload, Heavy, Piercing(4))
- Quantum Blade: 13 (Postmodern, Melee, Finesse, Cleaving, Stealth)
- Plasma Grenade: 11 (Postmodern, Thrown, Ranged, Ammunition)
- EMP Rifle: 8 (Postmodern, Ranged, Ammunition, Reload, Piercing(1))
- Laser Cannon: 17 (Postmodern, Ranged, Ammunition, Reload, Heavy, Piercing(3))


## Armor

The default armor list provides each armor's bonus value and associated tags.

- Padded Armor: 1 (Medieval, Light)
- Leather Armor: 2 (Medieval, Light)
- Studded Leather: 3 (Medieval, Light)
- Brigandine: 4 (Medieval, Medium)
- Chain Shirt: 4 (Medieval, Medium)
- Chainmail: 6 (Medieval, Heavy)
- Scale Mail: 7 (Medieval, Medium)
- Lamellar Armor: 7 (Medieval, Medium)
- Plate Mail: 8 (Medieval, Heavy)
- Full Plate: 10 (Medieval, Heavy)
- Ballistic Vest: 12 (Modern, Light)
- Riot Armor: 14 (Modern, Medium)
- SWAT Tactical Armor: 16 (Modern, Medium)
- Military Body Armor: 18 (Modern, Heavy, Ablative)
- Bomb Disposal Suit: 20 (Modern, Heavy, Sealed)
- Canine Training Suit: 10 (Modern, Light)
- Hazmat Suit: 8 (Modern, Sealed, Light)
- EOD Suit: 22 (Modern, Heavy, Sealed, Ablative)
- Powered Exosuit: 24 (Postmodern, Power, Medium)
- Tactical Nanite Vest: 25 (Postmodern, Medium, Nanite, Ablative)
- Adaptive Nanite Armor: 28 (Postmodern, Nanite, Sealed, Ablative, Medium)
- Energy Shielded Armor: 26 (Postmodern, Power, Sealed, Light)
- Mech-Infantry Suit: 30 (Postmodern, Power, Heavy, Sealed, Ablative)
- Synthetic Bio-Armor: 28 (Postmodern, Nanite, Medium, Sealed)
- Void Suit: 26 (Postmodern, Sealed, Medium)
- Aegis-Class Titan Armor: 30 (Postmodern, Power, Heavy, Sealed, Ablative)
- Phase-Shifting Armor: 27 (Postmodern, Medium, Power)
- Dystopian Riot Gear: 22 (Postmodern, Medium, Modern)

