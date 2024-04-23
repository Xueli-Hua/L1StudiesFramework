# Makefile for rate estimation

# Compiler
CXX = g++
CXXFLAGS = -O2 -Wall -Werror -Wextra
RCXXFLAGS := `root-config --cflags --libs`

# Linker
LD       = g++
LDFLAGS  =
LIBS     = 
#LIBS     += -stdlib=libc++

# CMSSW
ifneq ($(shell echo $$CMSSW_BASE), )
  CXXFLAGS  += -isystem $(CMSSW_BASE)/src/
  CXXFLAGS  += -isystem $(CMSSW_RELEASE_BASE)/src
  CXXFLAGS  += -isystem $(shell scram tool info boost | awk -F"=" '/BOOST_BASE=(.*)/{print $$NF}')/include
  CXXFLAGS  += -isystem $(shell scram tool info json | awk -F"=" '/JSON_BASE=(.*)/{print $$NF}')/include
  CXXFLAGS  += -isystem $(shell scram tool info fmt | awk -F"=" '/FMT_BASE=(.*)/{print $$NF}')/include
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

# MKBIN = $(CXX) $(CXXFLAGS) `root-config  --libs --cflags` -lMinuit -lGenVector

.PHONY: all submodules clean

$(BINDIR)/%: $(SRCDIR)/%.C
	@mkdir -p $(BINDIR)
	$(CXX) $(CXXFLAGS) $(CXXDEPFLAGS) $^ $(LIBS) $< -o $@

all: $(EXES)

clean:
	@rm -f $(EXES)
	@rm -f $(BINDIR)/*
