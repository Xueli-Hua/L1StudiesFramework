# Compiler
CXX      =  g++
#CXXFLAGS =  -std=c++11
CXXFLAGS += -Wall -fPIC -O3
#CXXFLAGS  += -g -pg
#CXXFLAGS  += -Wextra
#CXXFLAGS += -Wextra -Weffc++ # asking for troubles
#CXXFLAGS += -Wno-reorder # dirty fix
CXXFLAGS += $(subst -I, -isystem , $(shell root-config --cflags))

# Linker
LD       = g++
LDFLAGS  =
LIBS     = $(shell root-config --libs)
#LIBS     += -stdlib=libc++

# Commands
MD       = mkdir -p
RM       = rm -rf

# CMSSW
ifneq ($(shell echo $$CMSSW_BASE), )
  CXXFLAGS  += -isystem $(CMSSW_BASE)/src/
  CXXFLAGS  += -isystem $(CMSSW_RELEASE_BASE)/src
  LIBS += -L$(CMSSW_BASE)/lib/$(SCRAM_ARCH)/ -L$(CMSSW_RELEASE_BASE)/lib/$(SCRAM_ARCH)/ \
		  -lFWCoreFWLite -lDataFormatsL1TGlobal 
  LIBS += -L$(shell scram tool info boost | awk -F"=" '/LIBDIR=(.*)/{print $$NF}') \
		  -lboost_program_options -lboost_system -lboost_filesystem
  LIBS += -L$(shell scram tool info fmt | awk -F"=" '/LIBDIR=(.*)/{print $$NF}') \
                  -lfmt

endif

BINDIR = ./bin
SRCDIR = ./src

SRCS = $(wildcard $(SRCDIR)/*.C)
EXES = $(patsubst $(SRCDIR)/%.C,$(BINDIR)/%,$(SRCS))

.PHONY: all submodules clean

all: $(EXES)

$(BINDIR)/%: $(SRCDIR)/%.C
	@mkdir -p $(BINDIR)
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	@rm -f $(EXES)
	@rm -f $(BINDIR)/*
