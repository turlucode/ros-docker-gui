ARG ARG_FROM

FROM $ARG_FROM
MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>

# Install CanUtils
RUN git clone https://github.com/linux-can/can-utils.git && \
cd ./can-utils && \
mkdir build && cd ./build && \
cmake .. && make && sudo make install

# Launch terminator
CMD ["terminator"]
