# t-vecs

### Setup Environment

```
git clone https://github.com/KshitijKarthick/t-vecs.git
cd t-vecs
pip install -r requirements.txt
# Only Model needs to be downloaded and extracted in the t-vex directory
```

### Download Corpus & Models
* Models
  https://drive.google.com/file/d/0B08EScGNCpQpNkcxTnNCQmVjemc/view?usp=sharing

* Corpus
  https://drive.google.com/file/d/0B08EScGNCpQpcDlabjA4dmRYRmM/view?usp=sharing
  
### Execution

```
# Ensure Model is downloaded and extracted in the t-vex directory
python server.py
# Server is listening on http://0.0.0.0:5000
```

### Model Generation

```
# Ensure Corpus is downloaded and extracted in the t-vex directory
python model_generation.py
```

### Prerequisites
* Python 2.7 setup and installed
* Pip setup and installed
* Ensure all dependencies of requirements.txt are satisfied
* Download nltk_data using nltk.download() -> only tokenizers required
