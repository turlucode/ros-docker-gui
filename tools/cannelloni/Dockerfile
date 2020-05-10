ARG ARG_FROM

FROM $ARG_FROM
MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>

# Install Cannelloni
RUN git clone https://github.com/mguentner/cannelloni.git && \
cd ./cannelloni && \
mkdir build && cd ./build && \
cmake -DCMAKE_BUILD_TYPE=Release -DSCTP_SUPPORT=false -DCMAKE_CXX_STANDARD=11 .. && \
make && \
sudo make install

# Launch terminator
CMD ["terminator"]
