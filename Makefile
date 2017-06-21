all: getmodules makemodules

getmodules:
	@echo "[GET MODULES] "
	@git submodule update --init --recursive
#	@git submodule foreach git pull origin master

# makemodules: components/graphmap/bin/Linux-x64/graphmap components/graphmap/bin/graphmap-not_release components/miniasm/miniasm components/racon/bin/racon
makemodules: components/graphmap/bin/Linux-x64/graphmap components/graphmap/bin/graphmap-not_release components/miniasm/miniasm components/racon/bin/racon
	@echo "[MAKE MODULES] All tools installed."

components/graphmap/bin/Linux-x64/graphmap:
	@echo [GraphMap] $@
	cd components/graphmap; make modules && make -j 4

components/graphmap/bin/graphmap-not_release:
	@echo [GraphMap not_release] $@
	@cd components/graphmap; make modules && make -j 4 testing

components/miniasm/miniasm:
	@echo [Miniasm] $@
	@cd components/miniasm; make -j 4

components/racon/bin/racon:
	@echo [Racon] $@
	@cd components/racon; make modules && make tools && make -j 4
#	@cd components/racon; git checkout b5b65d7a593a640858a8f7b8c7659a2367fb7eab; make modules && make tools && make -j 4
