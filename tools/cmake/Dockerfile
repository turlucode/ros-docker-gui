ARG ARG_FROM

FROM $ARG_FROM
MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>

# Install (newer version of) CMake
RUN git clone https://gitlab.kitware.com/cmake/cmake.git && \
cd ./cmake && \
./bootstrap && make && sudo make install

# Launch terminator
CMD ["terminator"]
