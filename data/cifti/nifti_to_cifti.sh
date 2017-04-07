#!/bin/bash

NIFTI=${1}
CIFTI=${2}

if [ ! -e temp ]; then
	mkdir temp
fi


wb_command -volume-to-surface-mapping $NIFTI Conte69.L.midthickness.32k_fs_LR.surf.gii temp/temp.L.shape.gii -trilinear
wb_command -volume-to-surface-mapping $NIFTI Conte69.R.midthickness.32k_fs_LR.surf.gii temp/temp.R.shape.gii -trilinear
wb_command -cifti-create-dense-timeseries temp/temp.dtseries.nii -volume ${NIFTI} /Users/marcel/projects/cognitive_gradient/analyses/cognitive_terms/nifti_to_cifti/Atlas_ROIs.2.nii.gz
wb_command -cifti-separate temp/temp.dtseries.nii COLUMN -volume-all temp/temp_volume.nii.gz
wb_command -cifti-create-dense-scalar ${CIFTI} -volume temp/temp_volume.nii.gz /Users/marcel/projects/cognitive_gradient/analyses/cognitive_terms/nifti_to_cifti/Atlas_ROIs.2.nii.gz -left-metric temp/temp.L.shape.gii -roi-left L.atlasroi.32k_fs_LR.shape.gii  -right-metric temp/temp.R.shape.gii -roi-right R.atlasroi.32k_fs_LR.shape.gii

rm -rf temp
