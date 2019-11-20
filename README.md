# art2hepevt


WE use `gallery` to parse the file.

## Contents of the files

```
[ tmw@dunegpvm02 art2hepevt ]$ lar -c eventdump.fcl -s /pnfs/dune/persistent/users/gardiner/nc-new/nc_out_Ev50_01_gen.root -n 1
%MSG-i MF_INIT_OK:  Early 19-Nov-2019 22:22:33 CST JobSetup
Messagelogger initialization complete.
%MSG
19-Nov-2019 22:22:42 CST  Initiating request to open input file "/pnfs/dune/persistent/users/gardiner/nc-new/nc_out_Ev50_01_gen.root"
19-Nov-2019 22:22:43 CST  Opened input file "/pnfs/dune/persistent/users/gardiner/nc-new/nc_out_Ev50_01_gen.root"
Begin processing the 1st record. run: 1 subRun: 0 event: 1 at 19-Nov-2019 22:22:45 CST
PRINCIPAL TYPE: Event
PROCESS NAME | MODULE_LABEL.. | PRODUCT INSTANCE NAME | DATA PRODUCT TYPE............ | SIZE
MarleyGen... | TriggerResults | ..................... | art::TriggerResults.......... | ...-
MarleyGen... | marley........ | ..................... | std::vector<simb::MCTruth>... | ...1
MarleyGen... | rns........... | ..................... | std::vector<art::RNGsnapshot> | ...0

Total products (present, not present): 3 (3, 0).

PRINCIPAL TYPE: Run
PROCESS NAME | MODULE_LABEL | PRODUCT INSTANCE NAME | DATA PRODUCT TYPE | SIZE
MarleyGen... | marley...... | ..................... | sumdata::RunData. | ...-

Total products (present, not present): 1 (1, 0).
```

## Set up the environment

Run `setup.sh`

    source setup.sh


which setups up the DUNE `cvmfs` repository and `gallery`.

## Convert to 'Marley-style' JSON file

Use `dump2json.py`.

```
[ tmw@dunegpvm02 art2hepevt ]$ python dump2json.py -h
usage: Convert art-root Marley file into Marley-json format
       [-h] -i INPUT -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input art-root file
  -o OUTPUT, --output OUTPUT
                        Output json file name
```