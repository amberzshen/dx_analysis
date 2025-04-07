#!/bin/bash
vcf_file="test-200-samples.vcf.gz"
igd_file="test-200-samples.igd"
out="test-200-samples.grg"

sudo apt update
sudo apt install libffi-dev
curl https://pyenv.run | bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv install 3.10.13
pyenv global 3.10.13 

pip install pygrgl

grg convert $vcf_file $igd_file
grg construct $igd_file -o $out --maf-flip
grg process stats $out