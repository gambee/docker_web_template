# Max Gambee
# 
# Copyright 2018
#
# Makefile for working with this docker-compose web template

# the override variable, if present, overide docker-compose.yml
# with docker-compose.$(O).yml
O ?=

# commands
dc = docker
dcc = docker-compose

# file names
#   dccfile is the default, (required)
#   dccfileo is the override file (optional)
dccfile = docker-compose.yml

# set dccopts based on whether overrides have been passed
# (i.e. make .... O=foo would override with docker-compose.foo.yml)
ifeq ($O,) # check if O has been set
dccopts = -f $(dccfile)
dccfileo =
else
dccopts = -f $(dccfile) -f $(dccfileo)
dccfileo = docker-compose.$(O).yml
endif

conid = $$(docker ps -aqf "name=$*") # id of container with name '%'
all_cids = $$(docker ps -qa) # list of all container ids
all_vids = $$(docker volume ls -q) # list of all volume ids

# the following variables are for setting up the shell environment when
# logging into running docker container services
cols = export COLUMNS=`tput cols`;
lines = export LINES=`tput lines`;
init_shell = bash -c "$(cols) $(lines) exec $(entrypnt)"

run_prefix = winpty # this is prepended to the run commands (windows work around)

# the command run once the shell environment is initialized, use target
# specific variable assignment to override this for specific containters,
# as is done below with db
entrypnt = bash
run-db: entrypnt = psql -U postgres

# print logs for all running containers
logs:
	$(dcc) logs


# print logs only for matching container
logs-%:
	$(dcc) logs $*


# build the images described in the docker-compose.yml file of cwd,
# and override with docker-compose.$(O).yml if override is passed
build:
	$(dcc) $(dccopts) build


# same as above, but build a specific containter
build-%:
	$(dcc) $(dccopts) build $*


# startup all docker services/containers described in dccfile
up: build
	$(dcc) $(dccopts) up -d


# same as above, but startup a specific service
up-%: build-%
	$(dcc) $(dccopts) up -d $*


# shutdown all currently running containers
down:
	$(dc) stop $(all_cids)


# remove all currently saved/built images
rm: down
	$(dc) rm $(all_cids)


# remove all volumes
rmv: down
	$(dc) volume rm $(all_vids)


# run (i.e. login to a shell prompt of) a container
run-%:
	$(run_prefix) $(dc) exec -ti $(conid) $(init_shell)


# Reset is a 'hard' reset. It shuts everything down, removes images and
# volumes, then builds images and sets up the container services
reset: rm rmv up
