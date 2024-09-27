# NeuralGCM: code and conda environment setup

* <https://neuralgcm.readthedocs.io/en/latest/installation.html>
* <https://neuralgcm.readthedocs.io/en/latest/inference_demo.html>
* <https://github.com/google-research/neuralgcm>
* <https://cloud.google.com/storage/docs/public-datasets/era5>

## Get Started

### Code Base

If you want to chekout the neuralgcm code directly from GitHub:

```bash
git clone https://github.com/google-research/neuralgcm.git
```

Alternatively, go to their [quickstart notebook](https://neuralgcm.readthedocs.io/en/latest/inference_demo.html) and either open it in Colaboratory or download it and run locally.

---

### Environment

Create conda environment

```bash
# for GPUs
conda create --name neuralgcm python
conda activate neuralgcm
pip install neuralgcm ipykernel matplotlib
pip install -U "jax[cuda12]"
```

```bash
# for CPU only
conda create --name neuralgcm-cpu python
conda activate neuralgcm-cpu
pip install neuralgcm ipykernel matplotlib
pip install -U "jax"
```