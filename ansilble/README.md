Installation - Ansible Playbook
===============================

This installation method is designed to install the RPi PWM Server onto 
your Raspberry Pi and set it up in systemd as a service. 

Pre-req's
---------
- git
- [ansible](http://docs.ansible.com/ansible/intro_installation.html): 
You will only need this installed on the machine where you will run the 
playbook.  You can run the playbook from either a remote system or the 
RPi itself.  See installtion details below for each scenario.

Installation
------------
1. Clone or download the [repository](https://github.com/alanquillin/rpi_pwm_server)
2. From the repos root directory, go to the **ansible** driectory.
    
### Installing from a remote machine
**Note:** For the example below, replace the ip address 192.168.1.100 with 
the ip address of your target RPi.

Also, the below assumes that you are logging in with the default **pi** user. 
If you plan to use a different user, make sure the user has root access
```
ansible-playbook install.yml -i "192.168.1.100," --user pi --ask-pass --ask-su-pass
 
```

### Installing from the RPi (localhost)
Make sure the user you are executing this under has root access.  
```
ansible-playbook install.yml -i "localhost," -c local
 
```

**Note:** That in both the examples above, there is a "," at the end of the 
target address for the -i flag.  This is needed, so make sure you do not leave 
it out.