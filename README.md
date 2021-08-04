# Synology Remote Task Starter

Synology remote task starter

## Restriction

**Intended to start tasks that are set in Synology's task manager. Currently, an untraceable behavior prevents the execution of tasks, so the functionality has been extended to include launching commands. Once a way to start tasks is known, this procedure will be described in more detail.**

## Purpose

This project allows remote access to tasks in Synology's task manager, allowing access from internet-enabled systems.

## Reason

Currently, my NAS is checked during runtime to see if valid systems (can) access the system. However, there are situations where the check needs to be (temporarily) turned off. For this purpose, a task has been set up in the Synology task manager, which was previously started manually. This task starts a corresponding self-developed script on the NAS.

This access requires a login to the NAS and therefore has no high WAF ;)

## Functionality

A URI is offered via a web server, which corresponds to a task ID of a task set up in the task manager. Access is without login, but is secured by two obscurity factors to prevent unauthorized access:

a) a magic key for basic access.  
b) a task key that identifies the task to be executed.

Since only defined tanks can be started with this function and the task itself remains under the control of the owner, the influence is controllable. Depending on the tanks, of course, only the owner can judge the effect on the system. 

If the magic key is specified incorrectly or an unsuitable key is called for a task, the start page is displayed without a detailed error message. This is done for security reasons so as not to reveal any information about the reason for the failed attack.

## Requirements

**Note** The following description is based on a Synology system with DSM 7.0-41890 (Mid-August 2021).

### Python 3

Python 3 is required for use. 

### Python Modules

In addition, the modules specified in the requirements.txt must be installed.

`sudo -i`  
`curl -k https://bootstrap.pypa.io/get-pip.py | python3`  
`python3 -m pip install <package>`

The minimum of used modules is:

- `pip3 install Flask`  

### Rights

The script itself must be started with root privileges, since the used Synology command `synoschedtask` require these privileges.

## Installation

Ideally, the server is started via task manager when the Synology is started. In addition, proper post-farwarding must be used to ensure that the router forwards requests to this server. For this purpose, a request on the router port must be forwarded to the server port set in the configuration.

The server is started with `python3 syno_remotetask.py`. It reads it configuration from `config.json` in its directory and creates a logfile named `log.txt`.

## Configuration

In config.json all necessary parameters have to be set. After a change - if the server was not started in the debut mode - it has to be restarted.

The following settings are possible:

listen: address on which the server listens
port: Port on which the server listens
magickey: secret key to access the function. The more complex this value is, the more secure the call is against misuse.

For the tanks the following settings are possible under the hierarchy tasks:

```
"< id >": {  
    "identifier": "<key>"[,  
    "command": "<commands>"]
}[,]
```

| Field | Mandantory | Description |
| :--- | :---: | :--- |
| `<id>` | yes | Corresponds to the ID of the tank from the Synology task manager. |
| `<key>` | yes | describes a freely selectable key that is associated with the task ID. The more complex this value is, the more secure the call is against misuse. |
| `<command>` | no | if `commands` are given as an array of parts of the command, the given command is executed instead of the task id - this is due to a bug in synology that the synschedtask command may not execute tasks on the command line. The command has to been given as array like in Pythons subprocess.popen().|

### Example

http://localhost:10765/76sdf7678fds687/hjhass665s

### How to obtain task id?

Run the following command at command shell with root rights:

`sudo /usr/syno/bin/synoschedtask --get state=enabled`

Search the task (`Name`) you want to execute an note the field `ID`. This value is the configuration value for `<id>`.

## Security aspects

**Important note** The evaluation of security is the sole responsibility of the user who employs this solution! The current state does not provide comprehensive and complete protection - all users must be aware of this.

Nevertheless, the risk of attack or misuse can be significantly reduced if:

- a non-obvious port is used for the service (at the router, or at the web service in the case of an exposed web service)  
- the longest possible cryptic magic key is used to access the service  
- the magic key is changed regularly  
- the identifier for the task also uses a long and cryptic key  
- the identifier for the task is also changed regularly.  

