# SnowDown
A feature-rich downtime notificatoin utility.

## Info
Around winter time, with heavy snow power and internet outages become more common. It is important that we stay on top of our infrastructure, and part of that is knowing when it goes down. We can't constantly check ourselves, so why not have the computers do that?

## Installation
To install the program, use our pypi package!
```
pip install snowdown
```
Make a directory for the program (it makes it's configs in whatever directory you run it in)
```
mkdir path/to/somewhere
```
Set up the package, fill in the table:
```
snowdown setup
```
Finally, add some watched services, follow the prompts and enter the info:
```
snowdown addservice
```
Make a cron job or other automated runner automatically run `snowdown run` in whatever directory you created for the service.

## Other
This is created for Siege week 13 with the theme winter. Yes, I have a wonderfully loose interpretation of the theme. I just needed something to motivate me to write this, I have been meaning to for a while.