#!/bin/bash

CONTAINER="stem_tissue_characterisation-production"
touch `pwd`/bash_history
docker run -it --rm -v `pwd`/bash_history:/root/.bash_history -v `pwd`/data:/data:ro -v `pwd`/output:/output $CONTAINER
