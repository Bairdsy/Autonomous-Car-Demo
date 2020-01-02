# Hardware:
## Bill of Materials:
### For the Vehicle
| Number | Item | Indicative Cost |
| --- | --- | --- |
| 1 | Raspberry Pi Zero W (https://shop.pimoroni.com/products/raspberry-pi-zero-wh-with-pre-soldered-header) | $20.00 |
| 1 | Explorer Phat (https://shop.pimoroni.com/products/explorer-phat) | $17.00 |
| 1 | Pololu Zumo Chassis Kit (https://shop.pimoroni.com/products/zumo-chassis-kit-no-motors) | $31.00 |
| 2 | Micro Metal Gearmotor (https://shop.pimoroni.com/products/micro-metal-gearmotor-extended-back-shaft) – 50:1 or 298:1 (will impact speed) | 2 x $8.00 = $16.00 |
| 1 | 3D printed Inner Car Body (.STL 3D model included in GitHub)	| $10 (for filament) |
| 1 | 3D printed Outer Car Shell - Ambulance (.STL 3D model included in GitHub)	| $10 (for filament) |
| 1 | 3D printed Outer Car Shell - Mining Truck (.STL 3D model included in GitHub)	| $10 (for filament) |
| 1 | 3D printed Outer Car Shell - Van (.STL 3D model included in GitHub)	| $10 (for filament) |
| 1 | Power bank or battery pack capable of USB 5V 2A output – as small as possible | $20 |
| 1 | 16GB Micro SD Card | $10 |
| 1 | Sharp GP2Y0A21YK0F Reflective Sensor (https://au.rs-online.com/web/p/reflective-optical-sensors/6666564/) | $17 |
| 1 | USB to Micro USB cable (slimline, right anlge if possible) | $5
| 1 | Pkt Male to Male Jumper Jerky (https://shop.pimoroni.com/products/jumper-jerky-junior?variant=1076482173) | $4 |
| 1 | Camera module for Raspberry Pi Zero (https://shop.pimoroni.com/products/raspberry-pi-zero-camera-module) | $12 |

Estimated total cost:  $182

### For the Control Board, Monitor, Sensors & LEDs
| Number | Item | Indicative Cost |
| --- | --- | --- |
| 1 | Raspberry Pi 4 1GB (https://shop.pimoroni.com/products/raspberry-pi-4?variant=29157087379539) | $54 |
| 4 | Programmable RGB LEDs | 4 x $5 |	
| 1 | Explorer Hat Pro (https://shop.pimoroni.com/products/explorer-hat) | $31 |
| 4 | Force Sensing Resistor (https://core-electronics.com.au/search/?q=pololu-1645) | 4 x $14 |
| 1 | 7 inch monitor (or similar) | unknown |
		
Estimated total cost:  $157.00

### For the Enclosure
| Number | Item | Indicative Cost |
| --- | --- | --- |
| 2 | 900 x 1200 x 5mm Ply-Wood boards (white) | 2 x $11 |
| 8 | 3D printed corner brackets | $5 (for filament) |	
		
Estimated total cost:  $62.00

## Instructions:

### The Corner Brackets
The enclosure is held together by 3d printed corner brackets.  The STL model for these brackets is:
 - Double Bracket.stl

The original demo versions were printed on a Wanhao Duplicator i3 Plus in PLA with 0.14mm layer height.
  ![Brackets](../Images/Bracket.png?raw=true)

### Zumo Chassis Construction
1.	Check you have all components: 
  -	Zumo chassis main body
  -	1/16″ black acrylic mounting plate
  -	Two drive sprockets
  -	Two idler sprockets
  -	Two 22-tooth silicone tracks
  -	Two shoulder bolts with washers and M3 nuts
  -	Four 1/4″ #2-56 screws and nuts
  -	Battery terminals
  ![Chassis Parts](../Images/Chassis_Parts.jpg?raw=true)
2.	Place an M3 nut in each of the two side slots near the rear of the chassis. The slots are sized so that nuts will not be able to rotate within them
  ![Wheel Assembly](../Images/Chassis_A.png?raw=true)
3.	Place an idler sprocket on each shoulder bolt, followed by a washer. The protruding side of the sprocket hub should face the same direction as the threaded end of the bolt (in toward the chassis).
4.	Insert the shoulder bolts through the side of the chassis into the nut. Use a 3 mm hex key (Allen wrench) to tighten the bolts until the washers are snug against the chassis. Be careful not to overtighten the shoulder bolts as doing so can bend the washers 
5.	Solder 2 wires from the jumper jerky onto the connectors for each of the 2 gear motors before installing the motors in the chassis, as you will not be able to access the motor leads easily once the acrylic mounting plate is in place.
6.	Press the output shafts of the motors into the drive sprockets, with the raised lip on one side of the sprocket facing away from the motor. The end of the gearbox shaft should end up flush with the outside of the sprocket. A good way to do this is to set the wheel on flat surface (like a table top) and press the motor shaft into the wheel until it contacts the surface.
  ![Motor Assembly](../Images/Chassis_B.png?raw=true)
7.	Place the motors into the channel in the front of  the chassis, aligning the gearbox with the grooves in the channel. The front plate of the gearbox should be even with the edge of the chassis.
  ![Motor Assembly](../Images/Chassis_C.png?raw=true)
8.	In each of the two front tabs and your choice of the interior-nut holes along the rear, insert a  machine screw through the mounting plate and chassis and tighten it against a nut inside the chassis. You can line up the nut by feel, or you could try temporarily taping the nuts inside the recesses in the chassis.
9.	Add the silicone tracks by stretching them around the sprockets on each side of the chassis.

### The Car Bodies
The STL files for the 3D models are available in this folder of the repository.  
 - Box Chassis.stl  :  The inner compartment of the car which houses the electronics
 - Box Chassis - Lid.stl : The lid to the inner compartment
 - Ambulance Vehicle Skin.stl : The Ambulance skin
 - Van shell.stl : The Delivery Van skin
 - Mining Truck Skin.stl : The Mining Truck skin 

The original demo versions were printed on a Wanhao Duplicator i3 Plus in PLA with 0.14mm layer height.
  ![InnerShell](../Images/Inner_Body.png?raw=true)
  ![MiningTruck](../Images/Mining_Truck_Shell.png?raw=true)
  ![VanShell](../Images/Van_Shell.png?raw=true)
  ![AmbulanceShell](../Images/Ambulance_Shell.png?raw=true)
  
