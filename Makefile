# can be overridden by setting command line env
imageName := "tess4"
videoDevice := "/dev/video1"

build:
	docker build -t ${imageName} .

run-shell:
	docker run --device=${videoDevice} --rm -it -v ${PWD}:${PWD} -w ${PWD} ${imageName} /bin/bash

