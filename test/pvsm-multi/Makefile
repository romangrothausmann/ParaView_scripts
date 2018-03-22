### setting default paths of external programs
PV?=/opt/paraview-5.3.0_GL1/

export PATH:= $(PV)/bin:$(PATH)
export VGLRUN?=vglrun

### list internal programs
EXECUTABLES = pvpython
EXECUTABLES+= $(VGLRUN)

### check existance of external programs
K:= $(foreach exec,$(EXECUTABLES),\
	$(if $(shell PATH=$(PATH) which $(exec)),some string,$(error "No $(exec) in PATH")))


.PHONY: all

all: pvsm-multi_test.pvsm


pvsm-multi_test.pvsm : pvsm-multi_02.pvsm pvsm-multi_01.pvsm
%_test.pvsm :
	$(VGLRUN) pvpython ../../pvsm-multi.py -i $^ -o $@
