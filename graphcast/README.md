# GraphCast: code and conda environment setup

<https://github.com/google-deepmind/graphcast>

## Get Started

### Code Base

If you want to get the pangu code directly from GitHub:

```bash
git clone https://github.com/google-deepmind/graphcast.git
```

---

### Environment

Create conda environment

```bash
conda create --name graphcast python=3.10
conda activate graphcast
pip install --upgrade google-cloud-storage
pip install ipywidgets
pip install cftime
pip install zarr gcsfs
```
