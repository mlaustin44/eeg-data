cd eeg-data-front/eeg
quasar build
cd ..
cd ..
rm -r eeg-data-back/spa
cp -r eeg-data-front/eeg/dist/spa eeg-data-back/spa
