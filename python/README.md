This is a version of python built to run on a kobo-mini.  It includes pygame.
Some other versions of python available on the internet crash on my kobo mini
(without any error), but this one works - I think it is a problem with shared 
libraries, but have not solved it for the other distributions.

To make this work without having to copy any libraries around etc, add the 
following to /etc/profile to set the search path for shared libraries:
export LD_LIBRARY_PATH=/usr/lib:/mnt/onboard/.python/lib:/mnt/onboard/.python/pygamelibs:$QTDIR/lib:lib:$LIBRARY_PATH

Note that this assumes that you put this directory on the kobo at /mnt/onboard/.python


Note that I (Graham Jones) did not create this - it was published on the internet somewhere and linked from mobileread.com somewhere - If I find out who created
it I will add suitable attribution.

