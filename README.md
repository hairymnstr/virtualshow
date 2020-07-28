# VirtualShow

Due to the COVID-19 lockdown in the UK, [Stithians Show](https://en.wikipedia.org/wiki/Stithians_Show) was cancelled in 2020.  A small online version with a few classes offering a chance to submit a photo as an entry itself, or a photo of an entry (e.g. a decorated biscuit) was [hosted here](https://virtual-stithians.show).  This repository contains the Python3, Django application that was built to manage the entries.

## Structure

The design basically just uses two views, the homepage which is presented as a list, essentially a clickable copy of the show catalog and the gallery view for each category.

## Features

The design was kept deliberately simple (I'm not really a web developer) to promote stability and performance.  However, it has a number of features:

* Gallery view is touch-friendly (thanks to [photoswipe](https://photoswipe.com/))
* Entries can be placed First, Second, Third or Highly Commended (there's also a best guinnea pig in there and the system is easy to extend)
* Support for showing ages which was used in childrens categories
* Entrant names are held in the database for administrative use but not shown on the site
* Several pictures per entry are possible
* Entry photos are annonymised on upload (the file is renamed to `classXX_entryYYY.jpg` for example)
* Automatic rotation of the images based on EXIF data
* Automatic scaling of images to a comfortable maximum resolution of 1600 x 1600 to preserve bandwidth
* The site can be embargoed via a single variable in the settings.py but logged-in admins will still see all the content

The system uses the Django admin console to allow creation of Classes (as in show classes, a class for a decorated cake for example) and Entries.  When used for Stithians Show, the site was embargoed until just after the submission deadline, entries had to be submitted via email and were manually processed and uploaded into the website.  Once all entries received by the deadline had been uploaded the embargo was lifted and the entries could be viewed with judging being carried out remotely on the site.  Results were then posted after a few days.  It's possible to create users who can log in (to see the content before the embargo was lifted) but who can't use the admin using the Django admin permissions.  Since there is no direct way for users to upload their content there was no need for captcha, email verifications etc. to work with this system.
