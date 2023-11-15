#!/bin/bash

set -e

time magnetocosmics runningAsymptoticDirection.g4mac

mv AsymptoticDirection*.out outputFiles
cp runningAsymptoticDirection.g4mac outputFiles
