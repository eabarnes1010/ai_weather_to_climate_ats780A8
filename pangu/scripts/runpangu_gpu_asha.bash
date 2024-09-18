#!/bin/bash

#SBATCH --partition=<your partition>
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --gres=gpu:1

#SBATCH --job-name=pangu-run
#SBATCH --mail-user=<your email @colostate.edu>
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END 
#SBATCH --output=pangu_out.o%j

#conda init
source activate pangu_jul2024
module load cuda/11.6

#export MPLCONFIGDIR=/scratch/rschumac/.config/matplotlib

### rundir
cd <your path here> 

export init=2024072100
export input_data_dir="input_data_rt"
export output_data_dir="output_data_rt"
export output_zarr_dir="output_zarr_rt"
#export input_data_source="era5"  ### should be either 'era5' or 'ecmwf_hres'
export input_data_source="ecmwf_hres"

export step=6  ## timestep in hours
export n_steps=29

echo "preprocessing"
python get_preproc_${input_data_source}_pangu.py ${init} 
date

echo "inference"
python inference_gpu_iterative.py ${init} ${input_data_dir} ${output_data_dir} ${input_data_source}
date

echo "postprocessing"
python pangu_output_to_zarr.py ${init} ${output_data_dir} ${output_zarr_dir} ${step} ${n_steps} 

echo "done!"
date

exit

