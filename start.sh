#!/bin/bash
while ! nc -z elasticsearch 9200; do sleep 2; done
