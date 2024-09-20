# GraphCast: code and conda environment setup

* <https://neuralgcm.readthedocs.io/en/latest/installation.html>
* <https://neuralgcm.readthedocs.io/en/latest/inference_demo.html>
* <https://github.com/google-research/neuralgcm>

## Get Started

### Code Base

If you want to get the neuralgcm code directly from GitHub:

```bash
git clone https://github.com/google-research/neuralgcm.git
```

---

### Environment

Create conda environment

```bash
# for CPU only
conda create --name neuralgcm-cpu python
conda activate neuralgcm-cpu
pip install neuralgcm
pip install ipykernel
pip install -U "jax"
pip install matplotlib
```

```bash
# for GPUs
conda create --name neuralgcm python
conda activate neuralgcm
pip install ipykernel
pip install -U "jax[cuda12]"
pip install matplotlib
```
