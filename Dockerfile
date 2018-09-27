FROM fedora

RUN dnf -y update && dnf clean all
RUN dnf -y install python python2-pip && dnf clean all

RUN pip install prometheus_client

COPY fakeE2EBlackbox.py /root/fakeE2EBlackbox.py
EXPOSE 8000

CMD python /root/fakeE2EBlackbox.py
