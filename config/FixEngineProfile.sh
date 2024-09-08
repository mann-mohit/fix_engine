#!/bin/bash

# Only this should be change in case of fresh deployment
export FIX_ENGINE_HOME=/home/repos/fix_engine

export CONFIG_DIR=${FIX_ENGINE_HOME}/config
export DEP_DIR=${FIX_ENGINE_HOME}/config/deps
export HEADER_DIR=${FIX_ENGINE_HOME}/header
export SRC_DIR=${FIX_ENGINE_HOME}/src
export LIB_DIR=${FIX_ENGINE_HOME}/src/lib
export SCRIPTS_DIR=${FIX_ENGINE_HOME}/src/scripts
export TARGET_DIR=${FIX_ENGINE_HOME}/target
export THIRD_PARTY_DIR=${FIX_ENGINE_HOME}/third-party

alias fix_engine='cd ${FIX_ENGINE_HOME}'
alias config='cd ${CONFIG_DIR}'
alias dep='cd ${DEP_DIR}'
alias hdr='cd ${HEADER_DIR}'
alias src='cd ${SRC_DIR}'
alias scr='cd ${SCRIPTS_DIR}'
alias target='cd ${TARGET_DIR}'
alias third_party='cd ${THIRD_PARTY_DIR}'
