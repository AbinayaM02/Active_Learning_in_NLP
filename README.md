
# Active Learning in NLP

The aim of this project is to identify if active learning can help in building better models with less good quality data in the NLP domain.
The project is undertaken as part of the Full Stack Deep Learning Course, 2021. The code is not production ready yet and it is in experimental stage.

## Initial Plan
The initial plan is to build an end-to-end project that contains the following components,
- Active learning (using custom code or available library)
- Multi-class classification model using Transformers
- Experiment tracking using MLflow or wandb
- Labeling using labelstudio
- App using streamlit/Dash
- Explainability for NLP models - stretch goal
- Unit testing using pytest/unittest
- CI/CD using Github Actions

## Components completed
Currently, the following components are present (some of which are still in not 100% complete),
- Active learning is performed using uncertainity based sampling (random, least confidence, entropy based)
- Multi-class classification of news articles is done using Simpletransformers library
- Experiments are tracked using wandb
- CLI based annotation tool
- GUI based Dash app for annotation (functionalities are not completed yet)
- Pytest and coverage (doesn't cover all the code yet)
- CI/CD using Github Actions (in progress)
- Explainability of NLP models (will be done in the future)
- Expose API using FastAPI/Flask (will be done in the future)

## Authors
- [@AbinayaM02](https://github.com/AbinayaM02)
- [@datafool](https://github.com/datafool)

## Demo

Insert gif or link to demo (will be provided later)

## Documentation

[Documentation] (will be updated later)


## Environment Variables

To run this project, you will need to add the following path to your environment variable,
``` 
export PYTHONPATH="${PYTHONPATH}:<path_to_the_project_root_dir>
```
## Running the CLI tool

To run the CLI tool, use the following command
```
python scripts/annotator.py <path_to_data_to_be_annotated> \
                                <sampling_method> \
                                <no_of_samples>  \
                                <path_to_store_the annotated_data>
```

## Running the GUI annotation tool

To run the GUI tool, use the following command
``` 
python app/index.py
```

## Train model

To train the model on the news corpus (by directly downloading it from HuggingFace Datasets), do the following
```
python scripts/download_data.py
python scripts/train.py
```
If you've downloaded the data from the Kaggle competition, then use the following commands,
```
# To prepare the data
python scripts/data.py

# To train the model
jupyter notebook
```

## Running Tests

To run tests, run the following command
```
make test
```

## Running Styling

To run the styling on this project, use the following command
```
make style
```

## Roadmap
- Fix the issues with annotation app (Dash)
- Add testcases for all the modules
- Add features to train and inference using Dash app
- Fix Github Actions
- Dockerize the application
- Add documentation


## Screenshots 

### CLI
![CLI tool](https://user-images.githubusercontent.com/28945722/118386233-ad2e1d80-b633-11eb-8b1a-326c03e398b8.png)

### Dash Tool
![Dash : Home](https://user-images.githubusercontent.com/28945722/118368098-fabc7300-b5be-11eb-8774-da6dcceab501.png)
![Dash : Annotation details](https://user-images.githubusercontent.com/28945722/118368130-20e21300-b5bf-11eb-893e-756693583463.png)
![Dash : Annotation](https://user-images.githubusercontent.com/28945722/118386173-2e38e500-b633-11eb-90e9-7a2453b448e8.png)


## Acknowledgement

- [@katherinepeterson](https://www.github.com/katherinepeterson) for development and design of README.so.
- [@GokuMohandas](https://github.com/GokuMohandas) for the course on MLOps (https://github.com/GokuMohandas/MadeWithML).

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Appendix

Any additional information goes here
