## 1. Prepare data for training

#### 1.1 Generate list of speech files

Assuming the root directory with librispeech corresponds to `<root_speech>` and we want to store the results in `<speech_meta>`.

```
python3 plan_speech.py --root <root_speech> --json json/speech.json > <speech_meta>
```

#### 1.2 Generate list of farfield files

Assuming the root directory with generated RIRs correspond to `<root_farfield>` and we want to store the results in `<farfield_meta>`.

```
python3 plan_farfield.py --root <root_farfield> --json json/farfield.json > <farfield_meta>
```

#### 1.3 Generate list of audio files

Suppose we want to generate 10,000 samples and store the list in `<audio_meta>`.

```
python3 plan_audio.py --speech <speech_meta> --farfield <farfield_meta> --count 10000 > <audio_meta>
```

## 2. Train model

#### 2.1 Initialize model

Create a model with random parameters to start training from, and save the model in the file `<model_init>`.

```
python3 train_init.py --json json/features.json --model_dst <model_init>
```

#### 2.2 Train over epochs

Train over one epoch a previous model `<model_prev>` and save the updated version to `<model_next>`.

```
python3 train_epochs.py --audio <audio_meta> --json json/features.json --model_src `<model_prev>` --model_dst `<model_next>`
```

## Evaluate with model

#### Evaluate a single sample and show result

Evaluate the sample at index `<sample_index>` from the dataset `<audio_meta>` using the trained model saved in the file `<model_trained>`

```
python3 eval_sample.py --audio <audio_meta> --json json/features.json --model_src `<model_trained>` --index `<sample_index>`
```

#### Evaluate loss for the whole dataset

(TBD)
