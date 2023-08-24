---
title: Comma fixer
emoji: 🤗
colorFrom: red
colorTo: indigo
sdk: docker
sdk_version: 20.10.17
app_file: app.py
pinned: true
app_port: 8000
---

# Comma fixer
This repository contains a web service for fixing comma placement within a given text, for instance:

`"A sentence however, not quite good correct and sound."` -> `"A sentence, however, not quite good, correct and sound."`

It provides a webpage for testing the functionality, a REST API,
and Jupyter notebooks for evaluating and training comma fixing models.

A web demo is hosted in the [huggingface spaces](https://huggingface.co/spaces/klasocki/comma-fixer).

## Development setup

Deploying the service for local development can be done by running `docker-compose up` in the root directory.
Note that you might have to
`sudo service docker start`
first.

The application should then be available at http://localhost:8000.
For the API, see the `openapi.yaml` file.
Docker-compose mounts a volume and listens to changes in the source code, so the application will be reloaded and 
reflect them.

We use multi-stage builds to reduce the image size, ensure flexibility in requirements and that tests are run before 
each deployment.
However, while it does reduce the size by nearly 3GB, the resulting image still contains deep learning libraries and 
pre-downloaded models, and will take around 7GB of disk space.

Alternatively, you can setup a python environment by hand. It is recommended to use a virtualenv. Inside one, run
```bash
pip install -e .[test]
```
the `[test]` option makes sure to install test dependencies.

If you intend to perform training and evaluation of deep learning models, install also using the `[training]` option. 

### Running tests
To run the tests, execute
```bash
docker build -t comma-fixer --target test .
``` 
Or `python -m pytest tests/ ` if you already have a local python environment.


### Deploying to huggingface spaces
In order to deploy the application, one needs to be added as a collaborator to the space and have set up a
corresponding git remote.
The application is then continuously deployed on each push.
```bash
git remote add hub https://huggingface.co/spaces/klasocki/comma-fixer
git push hub
```

## Evaluation

In order to evaluate, run `jupyter notebook notebooks/` or copy the notebooks to a web hosting service with GPUs, 
such as Google Colab or Kaggle
and clone this repository there.

We use the [oliverguhr/fullstop-punctuation-multilang-large](https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large)
model as the baseline.
It is a RoBERTa large model fine-tuned for the task of punctuation restoration on a dataset of political speeches
in English, German, French and Italian.
That is, it takes a sentence without any punctuation as input, and predicts the missing punctuation in token 
classification fashion, thanks to which the original token structure stays unchanged.
We use a subset of its capabilities focusing solely on commas, and leaving other punctuation intact.



The authors report the following token classification F1 scores on commas for different languages on the original 
dataset:

| English | German | French | Italian |
|---------|--------|--------|---------|
| 0.819   | 0.945  | 0.831  | 0.798   |

The results of our evaluation of the baseline model out of domain on the English wikitext-103-raw-v1 validation 
dataset are as follows:

| Model    | precision | recall | F1   | support |
|----------|-----------|--------|------|---------|
| baseline | 0.79      | 0.72   | 0.75 | 10079   |
| ours*    | 0.86      | 0.85   | 0.85 | 10079   |
*details of the fine-tuning process in the next section.

We treat each comma as one token instance, as opposed to the original paper, which NER-tags the whole multiple-token 
preceding words as comma class tokens.
In our approach, for each comma from the prediction text obtained from the model:
*  If it should be there according to ground truth, it counts as a true positive.
 * If it should not be there, it counts as a false positive.
 * If a comma from ground truth is not predicted, it counts as a false negative.

## Training
The fine-tuned model can be found [here](https://huggingface.co/klasocki/roberta-large-lora-ner-comma-fixer).

To compare with the baseline, we fine-tune the same model, RoBERTa large, on the wikitext English dataset.
We use a similar approach, where we treat comma-fixing as a NER problem, and for each token predict whether a comma 
should be inserted after it. 

The biggest differences are the dataset, the fact that we focus on commas, and that we use [LoRa](https://arxiv.org/pdf/2106.09685.pdf)
for parameter-efficient fine-tuning of the base model.

The biggest advantage of this approach is that it preserves the input structure and only focuses on commas, 
ensuring that nothing else will be changed and that the model will not have to learn repeating the input back in case
no commas should be inserted.


We have also thought that trying out pre-trained text-to-text or decoder-only LLMs for this task using PEFT could be 
interesting, and wanted to check if we have enough resources for low-rank adaptation or prefix-tuning.
While the model would have to learn to not change anything else than commas and the free-form could prove evaluation
to be difficult, this approach has added flexibility in case we decide we want to fix other errors in the future not 
just commas.

However, even with the smallest model from the family, we struggled with CUDA memory errors using the free Google 
colab GPU quotas, and could only train with a batch size of two.
After a short training, it seems the loss keeps fluctuating and the model is only able to learn to repeat the 
original phrase back. 

If time permits, we plan to experiment with seq2seq pre-trained models, increasing gradient accumulation steps, and the 
percentage of 
data with commas, and trying out artificially inserting mistaken commas as opposed to removing them in preprocessing.


