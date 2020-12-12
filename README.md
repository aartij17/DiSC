# A pluggable consensus simulator for the blockchain and cryptocurrencies course (CS291D)

## In order to run the simulator
```
python main.py <demo_files (optional)>
```
If the `demo_file` is not passed at runtime, the program defaults to `config.json`.

## In order to see the log viewer
```
cd logs_viewer
npm install
yarn start
```

## Adding new protocols
In order plug new protocols into the simulator, implement the `ProtocolBase` class.
Add the protocol initialization to `common/utils.py` file.
