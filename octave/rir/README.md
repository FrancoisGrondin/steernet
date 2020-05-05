## Create the tree of directories

First step consists in creating a tree of directories to store the results in a root directory `<root_directory>`.

```
octave init.m <root_directory>
```

## Simulate room impulse responses
Compile `rir_generator.cpp` into a mex file:
```
mkoctfile --mex rir_generator.cpp 
```
The `simulate.m` script can be launched many times in different processes to reduce the task duration. 
There are multiple microphone array geometry (`pair`, `circular`).
For instance, to generate 1000 RIRs for pair of microphones and save the result in `<root_directory>`:

```
octave simulate.m <root_directory> pair 1000
```

