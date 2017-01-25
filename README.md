Raspberry Pi PWM Server
=======================

A simple RESTful web server used to control the hardware PWM GPIO pin for the 
Raspberry Pi.  Since the RaspberryPi requires root access to control the 
harward PWM GPIO pin, some applications, that do not have root access, cannot 
use this feature.  There is the ability to use the software PWM built into the 
[RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) library, however, the issue 
is that, since it is software emulating PWM, a tight loop must be contained 
for the emulation, and the implementation is clunky when wanting to simply 
set the PWM value and leave it (for instance, controlling an LED strip's 
brightness and leaving it on).  That is where hardware PWM is the better 
solution.  This library is designed to expose a simple RESTful API that is 
run as a service under the root account.  This gives any application the 
ability to simply call the RESTful API to turn the PWM GPIO pin on or off, 
as well as set the PWM value.

This library uses the [wiringpi](https://pypi.python.org/pypi/wiringpi) python 
module which wraps the [wiringpi](http://wiringpi.com/) C library and gives 
more low level access to the GPIO, which includes the needed ability to write 
to the hardware PWN pin.  The Raspberry Pi includes 1 hardware PWM pin (BCM 
GPIO pin 18, physical pin 12).  Therefore there is no need to specify which pin 
to output on.  

Installation
------------
### Manual Installation
1. Clone or download the [repository](https://github.com/alanquillin/rpi_pwm_server)
    1. If you downloaded the zipfile, extract the file to **/opt/rpi_pwm_server**
2. Create a virtual environment *(optional but recommended)*
    ```bash
    $ virtualenv --prompt="(RPi PWM Server) " .venv
    $ source .venv/bin/activate
     
    ```
3. pip install the library
    ```bash
    # cd into the repository if you are not already there..
    (RPi PWM Server) $ cd rpi_pwm_server
     
    (RPi PWM Server) $ pip install -e .
     
    ```
4. Start the server
    ```bash
    # You will need to run the server as root
    $ sudo .venv/bin/python server.py
     
    ```
5. *(Optional)* Run as a service
    1. Download the service file: [rpi_pwm_server.service.j2](./ansilble/roles/rpi_pwm_server/templates/rpi_pwm_server.service.j2).
    2. Modify the file, replacing the "{{ install_dir }}" text with the location you cloned/downloaded the repo too. 
    3. Rename and move the file to **/etc/systemd/system/rpi_pwm_server.service**
    4. Restart systemd and enable to service
        ```bash
        $ sudo systemctl daemon-reload
        $ sudo systemctl enable rpi_pwm_server
        $ sudo systemctl start rpi_pwm_server
         
        ```
    5. Verify that the service is running
        ```bash
        $ sudo systemctl status rpi_pwm_server
         
        ```

### Automated Installation (using ansible)
This is the easiest way to install. 
You can see the instruction [here](./ansilble/README.md).


Using the API
-------------
The API is simple (currently) and only 1 endpoint supporting to methods

```bash
# Get the current state (this is the stored and assumed state of the PWM pin, if the value was changed outside the server, this will be inaccurate
curl -X GET http://localhost:8081/ 
 
# Set the pin On or Off
curl -X POST http://localhost:8081/ -d "mode=on"
curl -X POST http://localhost:8081/ -d "mode=off"
 
# Optionally, you can also set the PWM value when setting it to On
curl -X POST http://localhost:8081/ -d "mode=on" -d "value=high" 
 
# The API can also accept json, but note you must include the Content-Type
curl -X POST http://localhost:8081/ -d '{"mode":"on", "value":"low"}' -H "Content-Type: application/json"
 
```

The optional **"value"** parameter can be:

1. An integer ranging between >= 0 and <= 1024
2. A named values:
  1. high
  2. medium_high (also: mhigh or med_high)
  3. medium (also: med)
  4. medium_low (also: mlow or med_low)
  5. low
  6. very_low (also: vlow)
