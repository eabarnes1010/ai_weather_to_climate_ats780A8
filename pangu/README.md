# Pangu: code and conda environment setup

<https://github.com/198808xc/Pangu-Weather>

## Get Started

### Code Base

If you want to get the pangu code directly from GitHub:

```bash
git clone https://github.com/198808xc/Pangu-Weather.git
```

---

### Environment

Create conda environment

```bash
conda create --name pangu python=3.12.4
conda activate pangu

conda install zarr gcsfs
conda install cmake

SYSTEM_VERSION_COMPAT=0 pip install --no-cache-dir "onnxruntime>=1.14.1"
pip install onnx numpy xarray cdsapi matplotlib ipykernel metpy
conda install -c conda-forge cfgrib cartopy
```
