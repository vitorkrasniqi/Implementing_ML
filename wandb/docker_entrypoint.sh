#!/bin/bash
set -e

wandb login $WANDB_TOKEN

exec "$@"

