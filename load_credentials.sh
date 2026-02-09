#!/bin/bash
# Load Bring! credentials from Password Store

export BRING_EMAIL=$(pass show bring/email 2>/dev/null)
export BRING_PASSWORD=$(pass show bring/password 2>/dev/null)
