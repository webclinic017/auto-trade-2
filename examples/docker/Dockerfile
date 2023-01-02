#
# Building a Docker Image with
# the Latest Ubuntu Version and
# Basic Python Install
# 
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#

# latest Ubuntu version
FROM ubuntu:20.04  

# information about maintainer
LABEL MAINTAINER alphazz

COPY sources.list /etc/apt/sources.list 

# CMD ["/bin/bash"]

# add the bash script
ADD install.sh /
# change rights for the script
RUN chmod u+x /install.sh
# run the bash script
RUN sh /install.sh
# prepend the new path
ENV PATH /root/miniconda3/bin:$PATH

# execute IPython when container is run
CMD ["ipython"]

