FROM debian:buster

RUN echo deb http://mirrors.163.com/debian/ buster main non-free contrib > /etc/apt/sources.list \
	&& echo deb http://mirrors.163.com/debian/ buster-updates main non-free contrib >> /etc/apt/sources.list \
	&& echo deb http://mirrors.163.com/debian/ buster-backports main non-free contrib >> /etc/apt/sources.list \
	&& echo deb-src http://mirrors.163.com/debian/ buster main non-free contrib >> /etc/apt/sources.list \
	&& echo deb-src http://mirrors.163.com/debian/ buster-updates main non-free contrib >> /etc/apt/sources.list \
	&& echo deb-src http://mirrors.163.com/debian/ buster-backports main non-free contrib >> /etc/apt/sources.list \
	&& echo deb http://mirrors.163.com/debian-security/ buster/updates main non-free contrib >> /etc/apt/sources.list \
	&& echo deb-src http://mirrors.163.com/debian-security/ buster/updates main non-free contrib >> /etc/apt/sources.list \
	&& apt-get update && apt-get -y install wget vim procps zip gnupg \
	&& echo "deb http://files.freeswitch.org/repo/deb/freeswitch-1.8/ buster main" > /etc/apt/sources.list.d/freeswitch.list \
	&& echo "deb-src http://files.freeswitch.org/repo/deb/freeswitch-1.8/ buster main" >> /etc/apt/sources.list.d/freeswitch.list \
	&& /bin/bash -c 'echo -e "\nPATH=\$PATH:/usr/local/freeswitch/bin" >> /etc/profile' \
	&& /bin/bash -c 'echo -e "\nPATH=\$PATH:/usr/local/freeswitch/bin" >> /etc/bash.bashrc' \
	&& apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BD3189F5A2B57698 \	
	&& apt-get update \
	&& apt-get build-dep -y freeswitch \
	&& wget https://codeload.github.com/signalwire/freeswitch/zip/refs/tags/v1.10.7 -O /usr/local/src/freeswitch-1.10.zip \ 
	&& unzip -o -d /usr/local/src /usr/local/src/freeswitch-1.10.zip \
	&& mv /usr/local/src/freeswitch-1.10.7 /usr/local/src/freeswitch-master

WORKDIR /usr/local/src/freeswitch-master

RUN ./bootstrap.sh -j \ 
	&& ./configure \
	&& make -j4 && make install
CMD /bin/bash
