# syno_remotetask
Synology remote task starter

# Purpose

This project allows remote access to tanks in Synology's task manager, allowing access from internet-enabled systems.

# Reason

Currently, my NAS is checked during runtime to see if valid systems (can) access the system. However, there are situations where the check needs to be (temporarily) turned off. For this purpose, a task has been set up in the Synology task manager, which was previously started manually. This task starts a corresponding self-developed script on the NAS. 

This access requires a login to the NAS and therefore has no high WAF ;)

# Functionality

A URI is offered via a web server, which corresponds to a task ID of a task set up in the task manager. Access is without login, but is secured by two obscurity factors to prevent unauthorized access:

a) a magic key for basic access.
b) a task key that identifies the task to be executed.

Since only defined tanks can be started with this function and the task itself remains under the control of the owner, the influence is controllable. Depending on the tanks, of course, only the owner can judge the effect on the system. 
