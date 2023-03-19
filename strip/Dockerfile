# docker build  . --tag local/chat_i --tag local/chat_i:0.2
# docker run --name chat_c --detach --rm -p 7777:6666   local/chat_i:0.2

# the image from which we will start
FROM centos:7

# commands to run as root to modify original
RUN yum --assumeyes install \
  nmap-ncat

# tcp port in the container
EXPOSE 6666

# (default) command to run when container launches
ENTRYPOINT [  "/usr/bin/ncat", \
              "--keep-open",   \
              "--listen",      \
              "-4",            \
              "--chat"  ]

# (default) parameter to concatenate onto the command in ENTRYPOINT
CMD [ "6666"  ]
