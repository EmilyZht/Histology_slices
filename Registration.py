import czifile
import matplotlib.pyplot as plt
import numpy as np
# from tifffile import imwrite
import SimpleITK as sitk
from skimage.measure import block_reduce
# import nrrd
import pandas as pd
import skimage as ski


def af_registration(file_name, path="C:/Users/haz4006/Documents/Histology_slice/Ab3D-E1-AC01/",
                    path2ccf="C:/Users/haz4006/Documents/MouseCCF/", direction='medial', channel=3):
    excel = pd.read_csv(path + 'Ab3D-E-Screening-Ab3D-E1.csv')
    slice_info = excel[excel['Czi Filename'] == file_name]
    if direction == 'medial':
        scene = int(slice_info['Ms-Medial Scene#'].values[0]) - 1
        position = int(slice_info['Ms-Medial'].values[0])
    if direction == 'lateral':
        scene = int(slice_info['Ms-Lateral Scene#'].values[0]) - 1
        position = int(slice_info['Ms-Lateral'].values[0])

    # Get an AICSImage object
    img1 = czifile.imread(path + file_name)[scene, channel - 1, :, :, 0]  #SCYX0
    # 'S': 'Scene',  # contiguous regions of interest in a mosaic image; C: Channel, Y: Height, X: Width, 0: sample
    # plt.imshow(img1)
    # plt.show()

    # atlas, header = nrrd.read(path2ccf + "ara_nissl_10.nrrd")
    atlas = np.load(path2ccf + "template_volume_10um.npy")
    ref1 = np.rot90(atlas[:, :, int(atlas.shape[2] / 2 + 2 * position)], 3)  # 20um per slice, 10um per pixel
    # plt.imshow(ref1)
    # plt.show()

    # Down sampling
    img1_down = block_reduce(img1, int(10 / 1.376), np.mean)
    # plt.imshow(img1_down)
    # plt.show()
    # Binary thresholding
    t = ski.filters.threshold_otsu(img1_down)
    img1_down[img1_down < t] = 0
    # plt.imshow(img1_down)
    # plt.show()
    # Crop the image
    rows_to_delete = np.all(img1_down == 0, axis=1)
    columns_to_delete = np.all(img1_down == 0, axis=0)
    cropped_img1 = img1_down[~rows_to_delete, :]
    cropped_img1 = cropped_img1[:, ~columns_to_delete]
    # cv2.resize(cropped_img1, ref1.shape)
    # plt.imshow(cropped_img1, vmax=3000)
    # plt.show()
    # imwrite('C:/Users/haz4006/Documents/ZW1-Ab3D-E-AA/test.tif', img[0, 3, :, :, 0])

    annotation = np.load(path2ccf + "annotation_volume_10um_by_index.npy")
    annotation1 = np.rot90(annotation[:, :, int(annotation.shape[2] / 2 + 2 * position)], 3)

    sitk_ref1 = sitk.GetImageFromArray(ref1)
    sitk_img1 = sitk.GetImageFromArray(cropped_img1)
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetFixedImage(sitk_img1)
    elastixImageFilter.SetMovingImage(sitk_ref1)

    parameterMapVector = sitk.VectorOfParameterMap()
    parameterMapVector.append(sitk.GetDefaultParameterMap('translation'))
    parameterMapVector.append(sitk.GetDefaultParameterMap("affine"))
    parameterMapVector.append(sitk.GetDefaultParameterMap("bspline"))
    elastixImageFilter.SetParameterMap(parameterMapVector)

    elastixImageFilter.Execute()
    transformParameterMap = elastixImageFilter.GetTransformParameterMap()
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetTransformParameterMap(transformParameterMap)
    sitk_annotation = sitk.GetImageFromArray(annotation1)
    transformixImageFilter.SetMovingImage(sitk_annotation)
    transformixImageFilter.Execute()
    result = sitk.GetArrayFromImage(transformixImageFilter.GetResultImage())
    fig, ax0 = plt.subplots(1, 1)
    img_bottom = ax0.imshow(cropped_img1, vmax=3000, cmap='gray')
    img_up = ax0.imshow(result, cmap=plt.cm.hot, alpha=.2)
    fig.colorbar(img_bottom, ax=ax0)

    plt.show()
    fig.savefig(path + file_name.split('.')[0] + '-registration.png')
    return ax0


# af_registration(path="C:/Users/haz4006/Documents/Histology_slice/Ab3D-E1-AC01/", file_name='Ab3D-E1-AC-12.czi', path2ccf="C:/Users/haz4006/Documents/MouseCCF/", direction='medial', channel=3)
