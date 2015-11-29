# Evaluating `vagrant status` is very slow.
BOXES := centos7 \
         jessie64 \
         trusty64

define USAGE
targets:

  all       start all Vagrant machines
  cleanall  destroy all active Vagrant machines
  help      show this screen
  testall   test all Vagrant machines

machine targets:

  <machine>        start <machine>
  <machine> clean  destroy <machine>
  <machine> test   test <machine>

machines:

  $(BOXES)
endef

all:
	vagrant up --parallel

clean:
ifeq (,$(findstring $(firstword $(MAKECMDGOALS)), $(BOXES)))
	$(error `clean` requires a machine name, see `make help`)
endif
	vagrant destroy -f $(filter-out clean,$(MAKECMDGOALS))

cleanall:
	vagrant destroy -f

help:
	@echo $(info $(USAGE))

test:
ifeq (,$(findstring $(firstword $(MAKECMDGOALS)), $(BOXES)))
	$(error `test` requires a machine name, see `make help`)
endif
	vagrant provision --provision-with serverspec $(filter-out test,$(MAKECMDGOALS))

testall: all
	vagrant provision --provision-with serverspec

$(BOXES):
ifeq (,$(findstring clean,$(MAKECMDGOALS)))
	vagrant up $@
endif

.PHONY: all \
        clean \
		cleanall \
		help \
        test \
        testall \
        $(BOXES)
